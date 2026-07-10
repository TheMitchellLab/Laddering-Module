"""
LadderTeam Interview Engine Human-in-the-Loop
Runs a structured laddering interview
Supports ACV, 5-Whys, and JTBD laddering methods.
"""
import os as _os
import re as _re
import base64 as _base64
import mimetypes as _mimetypes
from enum import Enum
from typing import Optional
import asyncio
import json
import logging
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import httpx as _httpx
import os as _os
import logging as _logging
import asyncio as _asyncio
import concurrent.futures as _futures
import httpx as _sync_httpx
import logging as _logging
from openai import APITimeoutError


class InterviewType(str, Enum):
    WIREFRAME = "wireframe"
class LadderingMethod(str, Enum):
    ACV       = "acv"
    FIVE_WHYS = "5whys"
    JTBD      = "jtbd"

def encode_image(image_path: str) -> tuple:
    media_type, _ = _mimetypes.guess_type(image_path)
    if not media_type or not media_type.startswith("image/"):
        media_type = "image/png"
    with open(image_path, "rb") as f:
        b64 = _base64.b64encode(f.read()).decode("utf-8")
    return b64, media_type

_THINK_PATTERN = _re.compile(
    r'<think>.*?</think>'                       
    r'|<thinking>.*?</thinking>'                   
    r'|\[THINKING\].*?\[/THINKING\]'              
    r'|<\|channel>thought.*?<channel\|>'          
    r'|<\|think\|>.*?<\|/think\|>',
    _re.DOTALL | _re.IGNORECASE,
)


def _clean_response(raw: str) -> str:
    if not raw:
        return ""
    return _THINK_PATTERN.sub("", raw).strip()


async def _ollama_native_call(
    model: str,
    messages: list,
    temperature: float,
    num_predict: int,
    num_ctx: int,
    timeout: float,
) -> str:
    _log = _logging.getLogger(__name__)

    base_url = _os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    base_url = base_url.rstrip("/").removesuffix("/v1")
    native_messages = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if isinstance(content, str):
            native_messages.append({"role": role, "content": content})
        elif isinstance(content, list):
            text_parts = []
            images = []
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item["text"])
                    elif item.get("type") == "image_url":
                        url = item.get("image_url", {}).get("url", "")
                        if ";base64," in url:
                            b64_data = url.split(";base64,", 1)[1]
                            images.append(b64_data)
            native_msg = {"role": role, "content": "\n".join(text_parts)}
            if images:
                native_msg["images"] = images
            native_messages.append(native_msg)

    payload = {
        "model": model,
        "messages": native_messages,
        "stream": False,
        "think": False,  # Qwen3 classic, Gemma4
        "options": {
            "num_ctx": num_ctx,
            "num_predict": num_predict,
            "temperature": temperature,
        },
    }
    _model_lower = model.lower()
    if "qwen3.6" in _model_lower or "qwen3_6" in _model_lower:
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    _log.debug(
        f"[ollama_native] model={model} num_predict={num_predict} "
        f"num_ctx={num_ctx} think=False n_messages={len(native_messages)} "
        f"has_images={any('images' in m for m in native_messages)}"
    )
    def _sync_request():
        tc = _sync_httpx.Timeout(connect=10.0, read=timeout, write=30.0, pool=10.0)
        with _sync_httpx.Client(timeout=tc) as http:
            r = http.post(f"{base_url}/api/chat", json=payload)
            r.raise_for_status()
            return r.json()

    loop = _asyncio.get_running_loop()
    executor = _futures.ThreadPoolExecutor(max_workers=1)
    future = loop.run_in_executor(executor, _sync_request)
    try:
        data = await _asyncio.wait_for(future, timeout=timeout)
    except _asyncio.TimeoutError:
        executor.shutdown(wait=False, cancel_futures=True)
        raise _httpx.TimeoutException(
            f"[ollama_native] absolute timeout ({timeout}s) exceeded for model={model}"
        )
    raw = data.get("message", {}).get("content", "")
    done_reason = data.get("done_reason", "unknown")
    if not raw.strip():
        _log.warning(
            f"[ollama_native] EMPTY response. done_reason={done_reason}, "
            f"total_duration={data.get('total_duration', 'N/A')}, "
            f"eval_count={data.get('eval_count', 'N/A')}"
        )
    return _clean_response(raw)


async def _llm_call(
    client,
    model: str,
    messages: list,
    temperature: float,
    max_tokens: int,
    is_ollama: bool = False,
    has_image: bool = False,
    ollama_num_ctx: Optional[int] = None,
    ollama_skip_floor: bool = False,
) -> str:
    #CLOUD path (is_ollama=False):Single call via OpenAI client. No extra_body, no token inflation
    #LOCAL path (is_ollama=True):Routes through _ollama_native_call() which hits Ollama's native /api/chatendpoint directly
    _log = _logging.getLogger(__name__)
    _OLLAMA_MIN_TOKENS        = 512
    _OLLAMA_VISION_MIN_TOKENS = 1024
    _OLLAMA_TIMEOUT_TEXT      = 300
    _OLLAMA_TIMEOUT_VISION    = 600  # absolute ceiling via asyncio.wait_for
    if is_ollama:
        if ollama_skip_floor:
            floor = 0
        else:
            floor = _OLLAMA_VISION_MIN_TOKENS if has_image else _OLLAMA_MIN_TOKENS
        t_out = _OLLAMA_TIMEOUT_VISION    if has_image else _OLLAMA_TIMEOUT_TEXT
        effective_tokens = max(max_tokens, floor)
        _num_ctx = ollama_num_ctx if ollama_num_ctx is not None else (12288 if has_image else 8192)

        for attempt in range(2):
            if attempt > 0:
                tokens = effective_tokens * 2
            else:
                tokens = effective_tokens
            try:
                result = await _ollama_native_call(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    num_predict=tokens,
                    num_ctx=_num_ctx,
                    timeout=t_out,
                )
                if result:
                    return result
                if attempt == 0:
                    _log.warning(
                        f"[local] {model}: empty response (attempt 1, "
                        f"num_predict={tokens}, has_image={has_image}) "
                        f"— retrying with num_predict={tokens * 2}"
                    )
            except Exception as exc:
                _log.warning(f"[ollama_native] error (attempt {attempt + 1}): {exc}")
        return ""
    effective_tokens = max_tokens
    try:
        _is_gpt5 = "gpt-5" in model.lower()
        _tokens_key = "max_completion_tokens" if _is_gpt5 else "max_tokens"
        create_kwargs = dict(
            model=model, messages=messages,
            **{_tokens_key: effective_tokens},
        )
        if not _is_gpt5:
            create_kwargs["temperature"] = temperature
        if _is_gpt5:
            create_kwargs["reasoning_effort"] = "none"
        resp = await client.chat.completions.create(**create_kwargs)
        raw = (resp.choices[0].message.content or "") if resp.choices else ""
        return _clean_response(raw)
    except Exception as exc:
        _log = _logging.getLogger(__name__)
        _log.warning(f"LLM call error: {exc}")
    return ""

class _AnthropicCompletions:
    def __init__(self, anthropic_client):
        self._client = anthropic_client

    async def create(self, model, messages, temperature, max_tokens, **kwargs):
        # Extract system message from Anthropic takes it as a top-level param
        system = ""
        user_msgs = []
        for msg in messages:
            if msg.get("role") == "system":
                c = msg["content"]
                system = c if isinstance(c, str) else str(c)
            else:
                # Convert OpenAI image_url content → Anthropic image source format
                content = msg.get("content", "")
                if isinstance(content, list):
                    converted = []
                    for item in content:
                        if (isinstance(item, dict)
                                and item.get("type") == "image_url"):
                            url = item.get("image_url", {}).get("url", "")
                            if ";base64," in url:
                                media_type, b64 = url.split(";base64,", 1)
                                media_type = media_type.split("data:", 1)[-1]
                                converted.append({
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": b64,
                                    },
                                })
                            else:
                                converted.append(item)
                        else:
                            converted.append(item)
                    user_msgs.append({**msg, "content": converted})
                else:
                    user_msgs.append(msg)

        if not user_msgs:
            user_msgs = [{"role": "user", "content": "(no content)"}]

        call_kwargs: dict = dict(
            model=model, max_tokens=max_tokens,
            temperature=temperature, messages=user_msgs,
        )
        if system:
            call_kwargs["system"] = system

        resp = await self._client.messages.create(**call_kwargs)
        text = next((b.text for b in resp.content if hasattr(b, "text")), "")
        msg_obj    = type("Message", (), {"content": text})()
        choice_obj = type("Choice",  (), {"message": msg_obj})()
        return type("Response", (), {"choices": [choice_obj]})()


class _AnthropicChat:
    def __init__(self, client):
        self.completions = _AnthropicCompletions(client)

class _AnthropicClientShim:
    def __init__(self, api_key: str):
        try:
            import anthropic as _anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. "
                "Run: pip install anthropic --break-system-packages"
            )
        self._anthropic = _anthropic.AsyncAnthropic(api_key=api_key)
        self.chat = _AnthropicChat(self._anthropic)


def _build_image_content(
    image_b64: str,
    image_media_type: str,
    text: str,
    is_ollama: bool = False,
):
    return [{
            "type": "image_url",
            "image_url": {"url": f"data:{image_media_type};base64,{image_b64}"},},{"type": "text", "text": text},
    ]

sys.path.insert(0, str(Path(__file__).resolve().parent))
logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    turn: int
    role: str
    content: str
    weight: float = 1.0   # decays over time

class DecayingMemoryBuffer:
    #Maintains conversation history with exponential decay on older turns
    def __init__(self, decay_rate: float = 0.85, max_turns: int = 20):
        self.entries: List[MemoryEntry] = []
        self.decay_rate = decay_rate
        self.max_turns = max_turns

    def add(self, turn: int, role: str, content: str):
        self.entries.append(MemoryEntry(turn=turn, role=role, content=content))
        self._apply_decay()

    def _apply_decay(self):
        n = len(self.entries)
        for i, entry in enumerate(self.entries):
            distance = n - 1 - i   # 0 = most recent
            entry.weight = self.decay_rate ** distance

    def get_messages(self, system_content: str) -> List[dict]:
        messages = [{"role": "system", "content": system_content}]
                    # {"role": "user",   "content": user_content},]
        for entry in self.entries[-self.max_turns:]:
            role = "user" if entry.role == "interviewer" else "assistant"
            messages.append({"role": role, "content": entry.content})
        return messages

    def get_ladder_chain(self) -> List[Tuple[str, str]]:
        pairs = []
        q = None
        for entry in self.entries:
            if entry.role == "interviewer":
                q = entry.content
            elif entry.role == "persona" and q:
                pairs.append((q, entry.content))
                q = None
        return pairs

    def summary(self) -> str:
        chain = self.get_ladder_chain()
        lines = [f"  Q{i+1}: {q[:80]}\n  A{i+1}: {a[:80]}" for i, (q, a) in enumerate(chain)]
        return "\n".join(lines) if lines else "(empty)"

    def get_interviewer_messages(self, system_content: str) -> List[dict]:
        messages = [{"role": "system", "content": system_content}]
        for entry in self.entries[-self.max_turns:]:
            role = "assistant" if entry.role == "interviewer" else "user"
            messages.append({"role": role, "content": entry.content})
        return messages


#Interviewer Agent

CLARIFICATION_SYSTEM = """\
You are conducting a {interview_phase_label} feedback interview.

The participant was shown: {product_label}

Their initial reaction (verbatim — do NOT paraphrase):
"{prior_response}"

The researcher identified this phrase as the specific vague element to explore:
"{vague_seed}"

{phase_clarification_note}

Your task: present the prior response verbatim, name the vague element, and offer four
{interview_phase_label}-appropriate interpretations for the participant to choose from.

Use EXACTLY this format (no preamble, start immediately with the recap):

  Your response was: "{prior_response}"

  We want to understand what you meant by "{vague_seed}", so let's go a bit deeper. \
Which of these best captures what you were pointing at?

  A) [a specific, observable element from the {artifact_noun} — one sentence]
  B) [a different specific element — one sentence]
  C) [a third distinct element — one sentence]
  D) None of the above — but only if A, B, and C genuinely miss what you meant \
(you must still name the specific element you were referring to)

  Select A, B, C, or D to continue.

Rules for the four options:
{option_rules}

- Options must be meaningfully distinct from one another
- ALL options must be grounded in the participant's actual prior response — do not introduce
  new interpretations unrelated to what they said
- Frame them through the participant's professional lens where relevant
- Do NOT open with "Thank you", "Great", or any filler affirmation before the recap
- If the participant selects a letter OR clearly implies one, ACCEPT IT immediately
- Re-ask ONCE if the response contains no letter and is genuinely ambiguous. After that, proceed.
- The participant CANNOT take back or contradict what they already said — selection must
  stay anchored to the prior response, not introduce a new position

Conversation so far:
{chain}
"""

# Phase-specific injections for CLARIFICATION_SYSTEM
_CLARIFICATION_PHASE_NOTES = {
    InterviewType.WIREFRAME: (
        "interview_phase_label", "wireframe",
        "artifact_noun", "wireframe",
        "phase_clarification_note", (
            "IMPORTANT — WIREFRAME CONSTRAINTS:\n"
            "The participant saw a skeletal layout, not a working interface.\n"
            "Options must describe things VISIBLE in a static wireframe:\n"
            "  • placement and positioning of elements\n"
            "  • section or area labelling\n"
            "  • navigation structure and grouping\n"
            "  • information hierarchy (what appears prominent vs buried)\n"
            "  • missing elements or gaps in the layout\n"
            "NEVER reference interactions ('when they tap', 'clicking this button'),\n"
            "animations, colour, or anything requiring a working prototype."
        ),
        "option_rules", (
            "- Each option names a specific, observable element of the wireframe layout\n"
            "  (a section placement, a label, a structural grouping, an absent element)\n"
            "- Do NOT reference any interaction, animation, colour, or working functionality"
        ),
    ),
}

def _build_clarification_system(
    interview_type: InterviewType,
    product_label: str,
    prior_response: str,
    vague_seed: str,
    chain: str,
) -> str:
    """Format CLARIFICATION_SYSTEM with the correct phase injections."""
    pt = _CLARIFICATION_PHASE_NOTES[interview_type]
    # pt is a flat tuple of (key, val, key, val, ...) pairs
    d = dict(zip(pt[0::2], pt[1::2]))
    return CLARIFICATION_SYSTEM.format(
        interview_phase_label=d["interview_phase_label"],
        product_label=product_label,
        prior_response=prior_response,
        vague_seed=vague_seed,
        artifact_noun=d["artifact_noun"],
        phase_clarification_note=d["phase_clarification_note"],
        option_rules=d["option_rules"],
        chain=chain if chain else "(interview just started)",
    )
'''
Three focused prompts (one LLM call per job)
Call 1 EXTRACTOR:  reads raw persona answer >> one classified statement
Call 2 QUESTIONER: reads chain state + extraction >> one clean question
Call 3 SUMMARISER: fires only when Python chain gate is met >> termination block

'''

EXTRACTOR_SYSTEM = """\
You are an ACV analyst for a product feedback laddering interview.

Your only job: read the participant's response and extract the single most grounded,
concrete statement it contains, then classify it in product feedback terms.

ACV levels — PRODUCT FEEDBACK CONTEXT:
  [A] Attribute   — a concrete, observable feature, element, or interaction pattern in the
                    product. Answers "what specifically about the product is the participant
                    describing?"
                    Examples: "the onboarding flow has seven screens before reaching the main view",
                    "the search bar is not visible on the home screen",
                    "the button labels use internal system names the user does not recognise",
                    "there is no confirmation step before a destructive action"

  [C] Consequence — a functional or experiential impact on the user that follows from the
                    product attribute. Answers "what does that make the participant do,
                    avoid, or experience when using the product?"
                    Examples: "I lose track of where I am in the checkout",
                    "I have to guess which section contains what I need",
                    "the task takes longer than expected and I abandon it before finishing",
                    "I cannot tell whether my action was registered"

  [V] Value       — a stable functional requirement the product MUST meet for this user.
                    Answers "what must the product do, by design, that it currently fails to do?"
                    This is ACTIONABLE and DESIGN-DIRECTED — a concrete requirement a product
                    team could implement. It is not a personal feeling but a design standard.
                    Examples: "the app must complete any core task in three steps or fewer",
                    "navigation must follow platform conventions so users do not have to learn
                    a new system", "information must be grouped by task, not by the system's
                    internal category structure",
                    "any destructive action must require explicit user confirmation"

STEP 0 — PARROTING CHECK (run this before any classification):
Read the participant's response and the interviewer question that preceded it (provided below).
If the response opens with vocabulary directly lifted from the question — especially phrasing
such as "the fundamental requirement is", "what must be in place is", "the non-negotiable is" —
check whether the participant added substantive new reasoning beyond the question's framing.

  IF the key phrasing appears mirrored from the question AND the participant did NOT add
  new concrete reasoning, a specific example, or independent rationale:
  → `Classify as [C] (or stay at the current chain level), NOT [V].
  → Note in REASONING: "Response appears to mirror question vocabulary — treating as [C]."

  IF the participant used similar vocabulary BUT grounded it with their own concrete
  reasoning, a specific product interaction, or named something not in the question:
  → Proceed to normal V-detection — the value is authentic even if vocabulary overlaps.

  TERSE EXCEPTION: If the response is very short (fewer than 15 words), do NOT apply
  the parroting check — short responses rarely mirror question vocabulary meaningfully,
  and treating them as parrotted discards genuine terse V-level answers.
  Go directly to STEP 1.

STEP 1 — V-DETECTION (check this after Step 0 clears):
Classify as [V] if the response contains ANY of the following patterns in the participant's
own words. These cover BOTH personal and product/design requirement language.

PERSONAL PRODUCT VALUE patterns:
  - "I need [X] to work that way regardless of anything else"
  - "X is non-negotiable for me in any app like this"
  - "What ultimately matters is X" / "The one thing is X"
  - Direct one-concept answers to "what has to be there?" — e.g. "Speed." "Clarity."

PRODUCT / DESIGN REQUIREMENT patterns (equally valid as [V]):
  - REJECTION LANGUAGE: "I wouldn't use an app that doesn't [do X]" — X is the design requirement
    Example: "I wouldn't trust this if it doesn't give me a clear confirmation step"
    → Extract: X (the named design requirement) is the value
  - MINIMUM ACCEPTABLE STANDARD: "The minimum I'd expect from any app doing this is X" /
    "Any product like this should X" — where X names a design pattern or behaviour
  - DESIGN NON-NEGOTIABLE: "X has to be built in / X has to work that way / X is required
    for me to complete [task]" — where X names a design behaviour, not just a desired outcome
  - UNDERLYING PRODUCT NEED: "What this product really needs to do is X" /
    "The product needs X built in" / "The real problem is that X is missing"
  - STABLE REPEATED REQUIREMENT: If a specific design requirement (e.g. "one-tap access",
    "consistent navigation", "visible confirmation") has been named in 2+ previous answers
    and appears again as something the participant needs, classify as [V]
  - COMPARATIVE STANDARD: "Every app I trust does X — this one doesn't" where X names
    a concrete design pattern or behaviour
  - UI CONVENTION CITATION: Participant cites an established industry convention as the
    standard this product must conform to. Forms: "Most apps use X", "That's the convention
    for a reason", "The standard for [this kind of UI] is X", "Any app following conventions
    would have X", "Every app does X — it's just expected". Explicit contrast with the current
    product is NOT required — citing the convention as the standard IS the design requirement.
    Example: "Most apps use a filled background — blue, green, brand color — with white text.
              That's the convention for a reason."
    → Extract: the named visual convention (filled button, brand color fill, white text contrast)
    Note: must name a SPECIFIC VISUAL PROPERTY (fill type, color type, contrast approach),
    not a generic quality ("it should look better").
  - VISUAL SPECIFICATION: Participant names a concrete, implementable visual standard for
    a UI element — specific enough that a developer could implement it directly without
    asking follow-up questions. No imperative verb required.
    Forms: "[element] should have [fill type] / [color] / [contrast]", "a [filled/solid/outlined]
    [element] with [color] text", "[button style] — [color] background with [text color]"
    Example: "A filled button — solid color background, not gray, not a ghost outline. White
              text on a brand color." → [V]: button requires solid color fill with white text
    Example: "Blue background, white text — that's what says 'press me'" → [V]: solid color
    contrast is the design requirement
    Key test: could a developer implement this directly? If yes → [V].
  - TERMINAL SELF-ASSESSMENT: Participant signals they have fully and completely stated the
    requirement and there is nothing more. Forms: "That's all it needs to do", "That's it",
    "That's the only thing", "Nothing else", "That's all", "That's the fix".
    WHY this is [V]: the participant is declaring their requirement is stated and complete —
    this is the endpoint of the ladder, not a mid-chain consequence.
    Example: "If it looked like a button, I'd have known immediately. That's all it needs to do."
    → Extract: the design requirement stated just before the terminal phrase.
  - IMPERATIVE DESIGN DIRECTIVE: A short, direct command naming a SPECIFIC ELEMENT
    and what SPECIFIC PROPERTY should change. This is common in terse or clipped responses.
    Forms: "Remove X", "Move X to Y", "Rename X", "Add a label for X",
    "X should not be there", "Drop X", "X needs to go", "Hide X until Y",
    "make the button have a solid fill", "use a filled background"
    WHY this is [V]: the participant is not describing a consequence — they are stating
    a specific design action. "Remove 'Upload Image.' Irrelevant here." = the design
    requirement is that the Upload Image option should not appear in this layout.
    Extract the requirement implied by the command, not the command itself.
    Example: "Remove 'Upload Image.' Irrelevant here."
    → EXTRACT: "The Upload Image option should be removed from this layout", LEVEL: V

  VAGUE QUALITY DIRECTIVES — these look like imperatives but are NOT [V]:
    "Make it clearer", "make it more obvious", "make it easier to understand",
    "make it stand out more", "make it better", "improve visibility",
    "make it clearer where you're supposed to go" — these name a DESIRED QUALITY
    (clarity, obviousness, visibility) but do NOT specify which element or which
    design property should change. They describe the end state, not the mechanism.
    Classify these as [C] — they are a consequence the participant wants, not a
    design action a developer can implement.
    KEY TEST: Does the directive name (a) a specific element AND (b) a specific
    property (fill, color, size, contrast, placement, label, hierarchy)?
      "Make it clearer" → fails both tests → [C]
      "Make the button have a solid fill" → passes both → [V]
      "Make the Place Order button larger and filled" → passes both → [V]

  - SINGLE-ELEMENT VERDICT: When the participant's response to "what would you change?"
    or "what would fix this?" consists of naming exactly one element with a clear
    disposition (remove, move, rename, add) and nothing else — that IS the V.
    Do not require elaboration. The brevity of the answer is a personality trait,
    not a signal that the answer is incomplete.

CRITICAL EXTRACTION RULE for [V]:
When rejection language is used ("I wouldn't use this if it doesn't [do X]"),
extract the NAMED DESIGN REQUIREMENT (X), not the rejection sentence itself.
Example: "I wouldn't trust this if it doesn't give me a clear confirmation before deleting"
→ EXTRACT: "explicit confirmation before destructive actions is a required design behaviour",
  LEVEL: V

CRITICAL: A value declaration followed by consequence reasoning is STILL [V].
Extract the value declaration, not the trailing consequence.

STEP 2 — LOWEST-LEVEL RULE (apply only if Steps 0 and 1 found no V):
If the response spans multiple levels, extract the LOWEST level present (A beats C beats V).
The higher levels must still be earned through probing.
EXCEPTION: If Step 1 matched an IMPERATIVE DESIGN DIRECTIVE pattern, classify as [V]
even if the response also names an attribute. An imperative directive ("reduce X",
"separate X from Y") referencing an attribute does NOT get pulled down to [A] —
the action taken on the attribute is the value, not the attribute itself.

STEP 3 — FALLBACK:
If the response is vague, evasive, or rambling, classify as [A] and extract the
most concrete phrase present — even a partial example or product analogy counts.
If the response is entirely off-topic or unintelligible, output LEVEL: UNCLEAR.

IMPORTANT — TERSE RESPONSE HANDLING:
A very short response (1–3 words, a single sentence fragment, a bare imperative)
is NOT automatically vague. It may be the most precise thing the participant has
said. Apply V-detection to short responses with the same rigour as long ones.
"Remove 'Upload Image.'" is more precise than a paragraph that circles the topic.
Never require length as a condition for classification as [V].

Output format — no other text, no preamble:
LEVEL: [A / C / V / UNCLEAR]
EXTRACT: "the extracted statement in one sentence, using participant's own words where possible"
REASONING: one sentence explaining why this level, not another
"""

QUESTIONER_SYSTEM = """\
You are conducting a {interview_phase_label} feedback interview.

ANTI-REPETITION — READ THIS BEFORE GENERATING ANYTHING:
These questions have already been asked. Do NOT repeat or rephrase any of them.
If your intended question is similar to one below, stop and use a completely
different probe technique (contrast / scenario / specificity / absence / comparison).
{asked_questions_block}

Product being evaluated: {product_label}
Interview phase: {interview_phase_label}
Confirmed concern: "{confirmed_concern}"

{phase_questioner_note}

Chain so far:
{chain_summary}

Most recent participant statement has been classified as [{current_level}].
Extracted core: "{extraction}"

{override_instruction}

Your job: generate exactly ONE probing question for [Ladder {next_ladder_num}].

Level-specific probe instructions:
{probe_instruction}

Hard rules:
- Output ONLY the question text. Nothing else.
- No preamble, no chain annotations, no "[Ladder N]" label in your output.
- No filler: no "Thank you", "Great", "That's interesting", "That makes sense".
- One or two short sentences maximum.
- Never literally ask "but why?" — vary phrasing every turn.
- Reference specific elements the participant already mentioned — ground the probe
  in something concrete from their previous answer, not a generic UX question.
- BANNED VOCABULARY: "fundamental", "core value", "key principle", "essential",
  "non-negotiable", "must always be true", "underlying principle", "underlying value",
  "underlying need", "what do you ultimately", "what ultimately matters".
"""

_QUESTIONER_PHASE_NOTES = {
    InterviewType.WIREFRAME: (
        "WIREFRAME PHASE — CRITICAL CONSTRAINTS:\n"
        "The participant is reacting to a STATIC LAYOUT — no interactivity, no colour, \n"
        "no working functionality. You can see the same wireframe image they were shown.\n"
        "Your questions MUST stay within what a static layout can communicate:\n"
        "  Layout placement and visual hierarchy\n"
        "  Section and area labelling\n"
        "  Navigation grouping and information architecture\n"
        "  What is present or absent in the layout\n"
        "  What each section communicates about priority\n"
        "  Mental model alignment ('where would you look for X in this layout?')\n"
        "  NEVER: 'when you tap/click/scroll', 'how did it feel to use', 'what happened when',\n"
        "           'did you find it', 'were you able to complete', any interaction framing\n"
        "When generating a probe, look at the wireframe and reference the specific region\n"
        "or section the participant described. Keep probes grounded in visible layout elements."
    ),
}

def _build_questioner_system(
    interview_type: InterviewType,
    product_label: str,
    confirmed_concern: str,
    chain_summary: str,
    current_level: str,
    extraction: str,
    next_ladder_num: int,
    probe_instruction: str,
    override_instruction: str,
    asked_questions: Optional[List[str]] = None,
) -> str:
    phase_labels = {
        InterviewType.WIREFRAME: "Wireframe Review",
    }
    if asked_questions:
        block = "\n".join(
            f"  {i+1}. \"{q}\"" for i, q in enumerate(asked_questions)
        )
    else:
        block = "  (none yet — this is the first question)"
    return QUESTIONER_SYSTEM.format(
        interview_phase_label=phase_labels[interview_type],
        product_label=product_label,
        phase_questioner_note=_QUESTIONER_PHASE_NOTES[interview_type],
        confirmed_concern=confirmed_concern,
        chain_summary=chain_summary,
        current_level=current_level,
        extraction=extraction,
        next_ladder_num=next_ladder_num,
        probe_instruction=probe_instruction,
        override_instruction=override_instruction,
        asked_questions_block=block,
    )

PROBE_INSTRUCTIONS = {
    InterviewType.WIREFRAME: {
        "A": """\
The participant named something they noticed in the layout. Goal: make it specific
and concrete — which region, which label, which structural choice — before exploring impact.
Good wireframe probes at [A]:
- "Which part of the layout are you pointing at — the navigation area, the main content
  section, something near the top, or elsewhere?"
- "What specifically about how that area is arranged draws your attention?"
- "If you were looking for [a task the product seems to support], where in this layout
  would you start looking?"
- "What does the way that section is positioned tell you about what the product
  thinks is most important?"
- "Is that something that stands out immediately, or only once you look more closely?"
NEVER ask: "when you tap/click", "what happened when", "how did it feel to use".\
""",
        "C": """\
The participant named a functional or cognitive consequence of the layout. Goal: explore
its depth and real impact on how someone would use the product.
Good wireframe probes at [C]:
- "What would that mean for the first task someone would try with this layout?"
- "If a developer built this layout exactly as shown — how would that play out for
  someone encountering it for the first time?"
- "Does that make the main task harder to locate, or just harder to understand once
  you find it?"
- "What would someone need to know already before they could make sense of that section?"
- "Is that something they'd figure out on their own, or would it keep creating friction?"
NEVER ask: "when you tapped/clicked", "did you find it", "were you able to complete".\
""",
        "V": """\
The participant is expressing something that sounds like a stable layout requirement.
Goal: verify it holds as a design standard for this type of product.
Good wireframe probes at [V] (no banned vocabulary):
- "Would that still matter even if every other part of the layout was exactly right?"
- "Is that something you'd expect from any product doing this job, or specific
  to this layout?"
- "If the design team said that structural choice couldn't be changed — what would
  that mean for whether this layout was ready to build?"
- "Have you seen this same problem in layouts for similar products before?"
NEVER ask using: "fundamental", "non-negotiable", "principle", "core value".\
""",
        "UNCLEAR": """\
The participant's response was unclear. Ground back to the wireframe layout.
- "When you mentioned [X], which part of the layout were you referring to?"
- "Can you point to an area — top, middle, left, or right — where that stood out to you?"\
""",
        "V_ELICIT": """\
IMPORTANT OVERRIDE: Stop exploring new consequences. Surface the stable layout requirement
the product would need to meet for this participant to consider it structurally sound.

Do this INDIRECTLY through scenario, contrast, or layout-specific framing:
- "What would need to be reorganised in this layout for that not to be an issue?"
- "If the design team could only change one structural thing before it went to
  development — what would actually make the difference for you?"
- "What's the version of this layout that you'd hand to a developer and say 'yes, build this'?"
- "What would you never accept as a workaround if this layout went to build as-is?"
- "Imagine this was rearranged exactly the way you'd expect — what specifically would
  be in a different place?"
NEVER use: "fundamental", "non-negotiable", "principle", "underlying need".\
""",
        "V_ELICIT_FROM_ANCHOR": """\
IMPORTANT OVERRIDE: Re-anchor to the specific confirmed consequence (shown above).
Probe what stable layout requirement makes THAT consequence matter — through scenario or
contrast framing. Do NOT ask directly about requirements or principles.

- "If [anchor C] was completely fixed in this layout — would your concern disappear,
  or is there something deeper that would still bother you?"
- "When [anchor C] happens, what does it tell you about what the layout got structurally wrong?"
- "What would the correct version of that part of the layout actually look like?"
- "What would you never accept as a layout workaround for [anchor C]?"
NEVER use: "fundamental", "non-negotiable", "principle".\
""",
    },

}

# Redirect instruction injected when user drifts to a new attribute
A_REDIRECT_INSTRUCTION = """\
IMPORTANT: The participant has introduced a new element. Do NOT follow it.
The original confirmed attribute is: "{first_A}"
Bring the participant back to exploring the FUNCTIONAL CONSEQUENCES of that original \
attribute — what it causes them to do, avoid, or experience.
{phase_note}
Do not ask about the new element they introduced.\
"""

A_REDIRECT_PHASE_NOTES = {
    InterviewType.WIREFRAME: "Ask how that layout element would affect someone's ability to find or understand what they need — no interaction framing.",
}

C_ANCHOR_REDIRECT_INSTRUCTION = """\
IMPORTANT: The participant has been exploring multiple consequence angles rather than going deeper.
Re-anchor to this specific confirmed consequence: "{best_c}"
Ask what makes THAT specific consequence matter — through scenario, contrast, or \
{phase_framing} framing.
Do NOT use words like 'fundamental', 'principle', 'non-negotiable', 'core', 'must always', or 'regardless'.
Do NOT ask about new consequences.\
"""

C_ANCHOR_PHASE_FRAMINGS = {
    InterviewType.WIREFRAME: "layout-specific",
}

ABSENCE_PROBE_INSTRUCTION = """\
STRATEGY SHIFT — ABSENCE PROBING:
The anchor-redirect approach has not surfaced the underlying design requirement. Switch technique.
Ask what would specifically BREAK DOWN or FAIL in the {task_context} if the anchor \
consequence simply didn't exist. This forces the participant to articulate what the \
consequence is protecting — indirectly revealing the design requirement.

Anchor consequence: "{best_c}"
Root attribute: "{first_a}"

Good absence probe forms:
{absence_forms}

One sentence only. No filler. No trigger vocabulary (fundamental, non-negotiable, principle).\
"""

ABSENCE_PROBE_FORMS = {
    InterviewType.WIREFRAME: (
        "user's first encounter with the layout",
        [
            "If [anchor C] simply didn't exist in this layout — what's the first thing that would break for someone trying to use it?",
            "Picture someone opening this product and [anchor C] just isn't there. What outcome would they be most stuck by?",
            "If [anchor C] was never fixable in this layout no matter what — what would users permanently have to accept?",
        ]
    ),
}

def _build_a_redirect(interview_type: InterviewType, first_A: str) -> str:
    return A_REDIRECT_INSTRUCTION.format(
        first_A=first_A,
        phase_note=A_REDIRECT_PHASE_NOTES[interview_type],
    )

def _build_c_anchor_redirect(interview_type: InterviewType, best_c: str) -> str:
    return C_ANCHOR_REDIRECT_INSTRUCTION.format(
        best_c=best_c,
        phase_framing=C_ANCHOR_PHASE_FRAMINGS[interview_type],
    )

def _build_absence_probe(interview_type: InterviewType, best_c: str, first_a: str) -> str:
    task_context, forms = ABSENCE_PROBE_FORMS[interview_type]
    forms_text = "\n".join(f"- \"{f}\"" for f in forms)
    return ABSENCE_PROBE_INSTRUCTION.format(
        task_context=task_context,
        best_c=best_c,
        first_a=first_a,
        absence_forms=forms_text,
    )

SUMMARISER_SYSTEM = """\
You are completing a product feedback laddering interview.

Product evaluated: "{product_description}"
Participant's initial reaction (verbatim): "{prior_response}"
Vague element identified by researcher: "{vague_seed}"
Confirmed concern: "{confirmed_concern}"

You have been given the full classified chain. Your job is to write the structured
termination block. Be precise — do not invent steps that were not in the chain.

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Original response: "{prior_response}"
Vague seed: "{vague_seed}"
Confirmed attribute: {confirmed_concern}

CHAIN 1:
{chain_steps}

Endpoint type: [UX requirement / functional requirement / design constraint /
  usability standard / interaction requirement / core use case /
  accessibility need / performance requirement]

Total chains: 1
Total ladder steps: {total_steps}
Stopping reason: {stopping_reason}

Interview complete.
"""

FORCED_ENDPOINT_SUMMARISER_SYSTEM = """\
You are completing a product feedback laddering interview that has reached maximum consequence \
depth. The participant was not able to explicitly articulate an underlying design requirement.

Following Reynolds & Gutman (1988): the deepest confirmed consequence is accepted as the \
chain endpoint. Do NOT invent a requirement. Instead, write a one-sentence inference of what the \
chain implies, clearly labelled as inferred.

Product evaluated: "{product_description}"
Participant's initial reaction (verbatim): "{prior_response}"
Vague element identified: "{vague_seed}"
Confirmed concern: "{confirmed_concern}"
Full chain: {chain_steps}
Deepest consequence: "{deepest_c}"

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Original response: "{prior_response}"
Vague seed: "{vague_seed}"
Confirmed attribute: {confirmed_concern}

CHAIN 1:
{chain_steps}

Endpoint type: functional consequence (depth limit reached — design requirement not explicitly stated)
Inferred requirement: [one sentence: the chain suggests the product must X — this is inferred \
from the consequence pattern, not stated directly by the participant]

Total chains: 1
Total ladder steps: {total_steps}
Stopping reason: {stopping_reason}

Interview complete.
"""

FIVE_WHYS_EXTRACTOR_SYSTEM = """\
You are analyzing a participant's response in a product development 5-Whys interview about a wireframe UI.

Your job: classify the response as either INTERMEDIATE or ROOT_CAUSE.

{chain_context}

CLASSIFICATION RULES — read ALL rules carefully, then pick the BEST fit:

INTERMEDIATE — the response diagnoses or describes a problem but does NOT yet state
  what should be built or changed to fix it. A developer reading this answer would still
  need to ask "but what exactly should we do differently?"
  Examples of INTERMEDIATE (keep probing):
    "Because the navigation is confusing"
    "Because users don't know where to look"
    "The onboarding doesn't explain the core workflow"
    "The colors are all the same palette — nothing contrasts"        ← INTERMEDIATE
    "The button doesn't stand out from surrounding content"          ← INTERMEDIATE
    "There's no visual hierarchy — everything looks equal weight"    ← INTERMEDIATE
    "The button blends in with everything else on the screen"        ← INTERMEDIATE
    "Nothing on the screen signals that this is the main action"     ← INTERMEDIATE

ROOT_CAUSE — the response meets ONE of these criteria:

  1. ACTIONABLE DESIGN DIRECTIVE: The participant states what the UI should look like
     or do differently — specific enough that a developer could implement it without
     asking another clarifying question. The answer must be PRESCRIPTIVE (a fix),
     not just DIAGNOSTIC (a problem observation).

     CRITICAL TEST: Ask yourself — "Could a front-end developer implement this
     directly, without asking any follow-up questions?"
       YES → ROOT_CAUSE
       NO  → INTERMEDIATE (keep probing for the prescription)

     Examples (prescriptive → ROOT_CAUSE):
       "The button needs a filled background with a contrasting color, not an outline"
       "The text needs to be at least 16 pixels and pass contrast accessibility checks"
       "There should be one dominant accent color used only for the primary CTA"
       "The button label should be bold and the button itself needs a solid fill"
       "A filled button with a real background color. Text 16px minimum. Sufficient
        contrast so it passes basic accessibility checks."

     Counter-examples (diagnostic only → INTERMEDIATE, keep probing):
       "The button blends in" → no prescription, keep going
       "The color palette is too uniform" → identifies problem, no fix stated
       "There's no visual hierarchy" → identifies problem, no fix stated
       "The colors are all the same palette" → identifies element, no fix stated

  2. DOMAIN DEPARTURE: The answer shifts from design/UI to organizational process,
     team structure, business strategy, leadership decisions, or company priorities.
     If further "why" probing would leave the product scope → ROOT_CAUSE.
     Examples:
       "It comes down to how the company prioritizes its core objectives"
       "Trade-offs are made by leadership based on launch timelines"

  3. CIRCULAR + PRESCRIPTIVE: The answer restates a cause already given earlier in the
     chain AND that restated content is itself prescriptive (states a specific fix).
     Pure repetition of a DIAGNOSTIC observation is NOT ROOT_CAUSE — classify as
     INTERMEDIATE, even if the participant signals exhaustion.

     CRITICAL — exhaustion language does NOT substitute for a prescription:
     "I think I'm saying the same thing... I'm not sure what else to add" while
     repeating a diagnostic-only observation (e.g. "the coloring makes everything
     look the same") is STILL INTERMEDIATE. The participant running out of new
     things to say is not the same as reaching an actionable fix. Do not classify
     ROOT_CAUSE just because the participant seems stuck or apologetic — only
     classify ROOT_CAUSE if the actual content is prescriptive.

  4. EXPLICIT MARKER: The participant says "that's the real problem" or similar AND
     the statement is prescriptive.

Current why depth: {current_depth}

OUTPUT FORMAT — REASONING first, then LEVEL. No preamble, no other text:
REASONING: one sentence explaining why you chose this level
LEVEL: [INTERMEDIATE / ROOT_CAUSE]
EXTRACT: "the core cause in one sentence, using participant's words where possible"
"""

FIVE_WHYS_QUESTIONER_SYSTEM = """\
You are conducting a {interview_phase_label} feedback interview using the 5-Whys technique.

Product being evaluated: {product_label}
Confirmed concern: "{confirmed_concern}"

Why chain so far:
{chain_summary}

Current problem statement (the cause just identified by the participant):
  "{current_problem}"

Current why depth: {why_depth}
{domain_drift_warning}
{judge_injection}

ANTI-REPETITION — do NOT repeat or rephrase any of these already-asked questions:
{asked_questions_block}

Your job: generate exactly ONE question that probes WHY the current problem statement occurs,
from the perspective of a USER observing the interface — not a designer or engineer.
This is Why #{next_why_num} in the chain.

CRITICAL FRAMING RULE:
  The participant is a REAL USER, not a designer or engineer. They cannot answer questions
  about design decisions, team choices, or why developers built something a certain way.
  NEVER ask "What design decision led to X?" or "What design choice is behind X?" —
  the user has no access to that information.
  Instead, ask what they SEE, NOTICE, or EXPERIENCE when looking at the screen.

PROBE RULES:
- Never literally ask "But why?" — vary phrasing every single turn
- Reference the SPECIFIC element or quality the participant just mentioned
- This is a STATIC prototype image — the participant LOOKED at it, they never used it.
  Never frame questions as if they interacted with the app. BANNED: "tap", "click",
  "scroll", "proceed", "move forward", "complete", "navigate to", "before deciding",
  "whether to proceed", "did you find it", "were you able to".
- Frame every question from the user's observational perspective ("what do you notice",
  "what makes it hard", "what draws your eye", "what stands out or doesn't")
- Good probe forms (ROTATE — use a DIFFERENT form each turn):
    * "What is it about [specific element] that makes it [problem] for you?"
    * "When you look at [element], what specifically makes it hard to [task]?"
    * "What does [element] look like to you compared to the other items on the screen?"
    * "What would [element] need to look like for [X] not to be a problem?"
    * "Which part of what you're seeing on screen makes [X] happen?"
    * "How does [element] appear to you — what's your eye drawn to or not drawn to?"
- Follow the causal thread naturally — let the participant's answers guide the depth
- Do not pressure toward closure; if the cause has a deeper cause, probe it
- No filler: no "Thank you", "Great", "That makes sense"
- One or two short sentences maximum
- Output ONLY the question text. Nothing else.

BANNED question patterns — NEVER use these:
  * "What design decision..." — the user doesn't know design decisions
  * "What design choice..." — same
  * "What design gap..." — same
  * "Why did the designers..." — same
  * "What specific [organizational/internal/constraints]..." — outside user's knowledge
  * "What specific factors within..." — too abstract
  * "What specific criteria or metrics..." — leaves the user's experience domain
  * Any question about leadership, team processes, sprint planning, or company strategy

{prescription_note}{phase_questioner_note}
"""

FIVE_WHYS_SUMMARISER_SYSTEM = """\
You are completing a product feedback 5-Whys interview.

Product evaluated: "{product_description}"
Confirmed concern: "{confirmed_concern}"

Full Why chain:
{chain_steps}

Root cause: "{root_cause}"
Stopping reason: {stopping_reason}

Write the structured termination block. Be precise — do not invent steps not in the chain.

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Confirmed concern: {confirmed_concern}

5-WHYS CHAIN:
{chain_steps}

Root cause: "{root_cause}"

Design implication: [one sentence — what the product must do differently to resolve this root cause]

Total why steps: {total_steps}
Stopping reason: {stopping_reason}

Interview complete.
"""

FIVE_WHYS_FORCED_ENDPOINT_SUMMARISER_SYSTEM = """\
You are completing a product feedback 5-Whys interview.

Product evaluated: "{product_description}"
Confirmed concern: "{confirmed_concern}"

Full Why chain:
{chain_steps}

Last diagnostic statement from participant: "{root_cause}"
Stopping reason: {stopping_reason}

The participant got stuck repeating a diagnostic observation (identifying what is
wrong) without stating an actionable fix, even after being offered concrete choices.
Your job: INFER the most plausible actionable design fix from the whole chain's
content — do NOT just echo the participant's last diagnostic statement as if it
were a fix.

Look at the full chain. If the participant mentioned a design property (color,
contrast, fill, size, placement, weight), infer the most direct, concrete fix for
that property. Label it clearly as inferred.

Write the structured termination block. Be precise — do not invent details not
supported by the chain.

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Confirmed concern: {confirmed_concern}

5-WHYS CHAIN:
{chain_steps}

Root cause: "[inferred]: one sentence stating the most direct actionable design fix
implied by the chain — e.g. 'The button needs a solid-fill background in a color that
contrasts with the surrounding palette, with text at minimum 16px for legibility.'"

Design implication: [one sentence — what the product must build differently to resolve this]

Total why steps: {total_steps}
Stopping reason: {stopping_reason}

Interview complete.
"""


_JTBD_LEVEL_DEFS = {
    "S": (
        "[S] SITUATION — the real-world triggering circumstance or context.\n"
        "TWO VALID FORMS — either counts as [S]:\n"
        "  (a) Screen observation: participant says what they were looking at when the\n"
        "      concern caught their eye. Signals: 'when I saw...', 'looking at...',\n"
        "      'as I was reviewing...', 'at this point in the layout...'\n"
        "  (b) Real-world context: participant describes the work/life situation that\n"
        "      brings them to this type of task. Signals: 'when the team needs to...',\n"
        "      'usually when...', 'in situations where...', 'there's a time element',\n"
        "      'when coordinating...', 'when we're working under a deadline',\n"
        "      'it comes up in work contexts', 'when I'm responsible for...'\n"
        "BOTH forms give the 'when/where' context — accept either.\n"
        "UNCLEAR ONLY if: response describes what is broken ([B]) or what they want\n"
        "to see ([O]) with no situational context at all."
    ),
    "J": (
        "[J] JOB — WHAT the participant was trying to DO. Functional task or goal.\n"
        "The participant should state what they needed to ACCOMPLISH, VERIFY, or CHECK.\n"
        "Key signals: \"I was trying to...\", \"I needed to...\", "
        "\"my goal was...\", \"I wanted to figure out...\"\n"
        "Must be solution-free — the need, not a product feature.\n"
        "UNCLEAR if the response gives context without a goal, or describes "
        "the design problem/solution instead of a task."
    ),
    "O": (
        "[O] DESIRED OUTCOME — What SUCCESS looks like. The improvement sought.\n"
        "The participant should describe what BETTER would look like, not what is wrong now.\n"
        "Key signals: \"if X were changed...\", \"it would help if...\", "
        "\"ideally...\", \"I'd want to see...\", \"should feel more...\"\n"
        "Suggestions for improvement ARE outcomes.\n"
        "UNCLEAR if the response describes only the current problem with no "
        "desired state, or just gives context/goals."
    ),
    "B": (
        "[B] BARRIER — What is CURRENTLY WRONG with the specific design property,\n"
        "stated precisely enough that a developer could implement a fix directly.\n"
        "The participant must name the SPECIFIC VISUAL PROPERTY that is broken:\n"
        "  color, fill style (solid vs. ghost/outline), contrast, visual weight,\n"
        "  size, label text, shape, border, hierarchy.\n"
        "Key signals: \"no fill\", \"gray background\", \"ghost outline\", \"low contrast\",\n"
        "\"same color as everything else\", \"no border\", \"looks disabled\",\n"
        "\"same visual weight as the text around it\"\n"
        "   PERCEPTION METAPHORS without a named property → UNCLEAR, keep probing:\n"
        "  'It looked like a label' → UNCLEAR (WHY does it look like a label? fill? color?)\n"
        "  'Looked like static text' → UNCLEAR (what makes it read as text? no fill? size?)\n"
        "  'Didn't read as interactive' → UNCLEAR (what property causes that? no border?)\n"
        "  'Didn't register as a button' → UNCLEAR (is it the fill? color? outline style?)\n"
        "  'Not visible enough' → UNCLEAR (what property makes it hard to see?)\n"
        "  'Wasn't prominent' → UNCLEAR (what property? color? fill? size?)\n"
        "  'Hard to notice' → UNCLEAR (color? contrast? visual weight?)\n"
        "  'Didn't stand out' → UNCLEAR (what about it doesn't stand out?)\n"
        "   Metaphors describing perceptual outcome ('looked like X') only qualify as [B]\n"
        "  if the response ALSO names the specific property causing that perception.\n"
        "  Example of [B]: 'looked like a label because it had no fill and no border'\n"
        "  Example of UNCLEAR: 'it looked like a label' (no property named)\n"
        "  If the participant describes what SHOULD change or what would be better,\n"
        "  that is [O], not [B] — UNLESS they also name the specific broken property.\n"
        "UNCLEAR if: response is a vague complaint, a perception metaphor without a\n"
        "named property, a desired-state description, or context/goals."
    ),
}

JTBD_EXTRACTOR_SYSTEM = """\
You are verifying whether a participant's JTBD interview response contains
content for one specific level of the Job Story chain.

{chain_context}

━━━ TARGET LEVEL ━━━
We are probing for: {target_label}
{target_definition}

TASK: Does the participant's response contain {target_label} content?

Decision rules:
- YES → output LEVEL: {target_level}
- NO  → output LEVEL: UNCLEAR
- Do NOT output any other level.
- Hedging words ("I think", "probably", "maybe") are normal — do not penalise.
- EXTRACT must be a concrete phrase from the participant's words. If no single
  phrase fits, write one sentence paraphrasing the relevant content.
  Never leave EXTRACT empty.
- SPECIAL RULE FOR [B] BARRIER: The response must name a SPECIFIC DESIGN PROPERTY
  (color, fill, contrast, visual weight, style, size, border, label) that is broken.
  Two categories that are NOT enough — output UNCLEAR for both:
  (1) Vague complaints: "wasn't prominent", "hard to notice", "didn't stand out",
      "not visible enough", "hard to find"
  (2) Perception metaphors: "looked like a label", "looked like static text",
      "didn't read as a button", "didn't register as interactive", "looked inactive" —
      these describe a perceptual OUTCOME, not the design PROPERTY causing it.
  A metaphor only qualifies as [B] if the response ALSO names the specific property:
    UNCLEAR: "it looked like a label"
    [B]: "it looked like a label — no fill, no border, same color as the surrounding text"
  If you cannot point to a concrete property in the participant's words, output UNCLEAR.

Output format (REASONING first):
REASONING: one sentence — does this response contain {target_label} content, and why?
EXTRACT: "the key phrase using the participant's own words"
LEVEL: [{target_level} or UNCLEAR]
"""

JTBD_PROBE_INSTRUCTIONS = {
    "S": (
        "WE ARE PROBING FOR [S] SITUATION — the triggering context or circumstance.\n"
        "[S] has TWO valid forms: a screen-observation moment OR a real-world work context.\n"
        "Do NOT force a screen-observation answer if the participant is naturally describing\n"
        "their real-world context — that IS a valid [S].\n"
        "Good probe forms (real-world context — preferred first):\n"
        '  * "When does this kind of task typically come up for you?"\n'
        '  * "What kind of work situation usually brings you to a screen like this?"\n'
        '  * "Walk me through what was going on — what were you trying to get done?"\n'
        '  * "What was happening that made you need to use something like this?"\n'
        "Good probe forms (screen-observation — use if participant has been talking about\n"
        "the layout specifically):\n"
        '  * "What were you looking at when that first caught your attention?"\n'
        '  * "Which part of the layout were you focused on when you noticed this?"\n'
        "Accept either form as [S] — do NOT insist on screen-observation if the participant\n"
        "is giving real-world context. Both are valid triggering circumstances."
    ),
    "J": (
        "WE ARE PROBING FOR [J] JOB — the functional task the participant was trying to do.\n"
        "We need what they were trying to ACCOMPLISH, VERIFY, or CHECK when they SAW the screen.\n"
        "CRITICAL: This is a STATIC prototype image — the participant never interacted with it.\n"
        "Do NOT frame the job as something they were 'about to do' or 'deciding whether to do'.\n"
        "Frame it as what they were LOOKING FOR or HOPING TO CONFIRM when reviewing the layout.\n"
        "Good probe forms:\n"
        '  * "What were you trying to verify or check from looking at that part of the screen?"\n'
        '  * "What information were you hoping to see confirmed on this screen?"\n'
        '  * "What were you trying to understand about the layout when you noticed that?"\n'
        '  * "What question were you trying to answer for yourself from what was visible?"\n'
        "BANNED phrasings: 'before deciding', 'whether to proceed', 'move forward', 'complete',\n"
        "'navigate to', 'use the app' — these imply live interaction, not static review.\n"
        "Push toward a concrete TASK or NEED grounded in what was VISIBLE, not what was clickable."
    ),
    "O": (
        "WE ARE PROBING FOR [O] DESIRED OUTCOME — what success looks like.\n"
        "We need what the participant would WANT to see, not what is wrong now.\n"
        "Good probe forms:\n"
        '  * "What would \'working well\' look like for you here?"\n'
        '  * "If this were redesigned, what would you want it to achieve?"\n'
        '  * "How would you know this layout succeeded at its purpose?"\n'
        '  * "What specific improvement would make this feel right?"\n'
        "Push toward a DESIRED STATE — something a product team could aim for."
    ),
    "B": (
        "WE ARE PROBING FOR [B] BARRIER — the specific visual property that is broken.\n"
        "We need the participant to name the EXACT PROPERTY: fill (solid vs. ghost/outline),\n"
        "color, contrast, visual weight, size, border, or label style.\n"
        "CRITICAL: Frame questions from the USER's observational perspective — they are\n"
        "LOOKING at the screen. Do NOT ask about design decisions or team choices.\n"
        "CRITICAL: Do NOT drift to placement, position, or layout questions — those are\n"
        "already known. Stay on visual appearance: what does the element LOOK LIKE that\n"
        "makes it fail? Fill? Color? Contrast? Style?\n"
        "BRIDGE PROBE — use when participant gave a perception metaphor\n"
        "('looked like a label', 'didn't read as a button', 'not visible enough'):\n"
        '  * "What is it about how it looks — its fill, color, or border — that makes it\n'
        '     read like a label instead of a button?"\n'
        '  * "Is it that the button has no fill — it looks hollow or outline-only? Or is it\n'
        '     more about the color — too gray, too light, blending into the background?"\n'
        '  * "You said it looked like a label — is that because of the way it\'s colored?\n'
        '     The style of the border? Or is there no visible distinction at all from the text?"\n'
        "FORCED-CHOICE PROBE — offer 2–3 concrete visual options when stuck:\n"
        '  * "Would it help if the button had a solid color fill, or is it more about\n'
        '     the contrast — the colors are too similar to the background?"\n'
        '  * "Is the issue that it looks like an outline-only button with no fill,\n'
        '     or that the color itself is too muted to register as an action?"\n'
        "General probe forms:\n"
        '  * "What is it about the way it looks right now — color, fill, border — that\n'
        '     makes it hard to identify as the main action?"\n'
        '  * "When you look at the button, what specifically about its appearance doesn\'t\n'
        '     say \'press me\'?"\n'
        "Do NOT accept metaphors ('looked like a label', 'didn't register', 'not visible')\n"
        "— push for the specific visual property (fill, color, contrast, outline style).\n"
        "A developer needs to know WHAT to change: not 'it looked wrong' but 'no fill,\n"
        "gray text on gray background, ghost outline on white page' — that level of specificity."
    ),
}

JTBD_QUESTIONER_SYSTEM = """\
You are conducting a {interview_phase_label} feedback interview using the JTBD Job Story method.

Product being evaluated: {product_label}
Confirmed concern: "{confirmed_concern}"

Job Story chain so far:
{chain_summary}

Target level: [{target_level}]  ← your next question MUST probe for this level
{judge_injection}

{phase_probe_instruction}

ANTI-REPETITION — do NOT repeat or rephrase any of these already-asked questions:
{asked_questions_block}

If your question is semantically similar to ANY question above, DISCARD it and try
a completely different angle. "Walk me through the specific moment/situation/scenario"
counts as the SAME question in different words.

PROBE RULES:
- Reference the SPECIFIC element the participant just mentioned — ground the question
- No filler: no "Thank you", "Great", "That makes sense"
- One or two short sentences maximum
- This is a STATIC prototype image — the participant LOOKED at it, they never used it
- No interaction framing: BANNED words and phrases: "tap", "click", "scroll", "proceed",
  "move forward", "complete", "navigate to", "before deciding", "whether to proceed",
  "use the app", "go through", "when using" — reference visible layout only
- Output ONLY the question text. Nothing else.

{phase_questioner_note}
"""

JTBD_SUMMARISER_SYSTEM = """\
You are completing a product feedback JTBD (Jobs to be Done) interview.

Product evaluated: "{product_description}"
Confirmed concern: "{confirmed_concern}"

Full Job Story chain (extracted by classifier):
{chain_steps}

Conversation context:
{conversation_context}

Stopping reason: {stopping_reason}

Write the structured termination block.

RULES:
- Use the participant's own words where possible.
- If an extracted [S]/[J]/[O] slot says "(not identified)" or is clearly a barrier
  restated as a situation/job/outcome (misclassification), INFER the best value
  from the conversation context instead. Prefix inferred values with "[inferred]:".
- Only write "(not identified)" if there is genuinely no basis for inference
  anywhere in the conversation.
- [B] BARRIER must describe the current design problem, not the desired fix.
- [O] DESIRED OUTCOME must describe what success looks like, not the problem.

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Confirmed concern: {confirmed_concern}

SITUATION: {situation}
JOB: {job}
DESIRED OUTCOME: {outcome}
BARRIER: {barrier}

JOB STORY: When {situation}, I want to {job}, so I can {outcome}, but {barrier}.

Design implication: [one sentence — the actionable design requirement this job story reveals]

Total turns: {total_turns}
Stopping reason: {stopping_reason}

Interview complete.
"""

JTBD_FORCED_ENDPOINT_SUMMARISER_SYSTEM = """\
You are completing a product feedback JTBD interview that reached maximum outcome depth
WITHOUT the participant naming a concrete barrier.

Product evaluated: "{product_description}"
Confirmed concern: "{confirmed_concern}"

Full Job Story chain:
{chain_steps}

Conversation context:
{conversation_context}

The participant identified situations, jobs, and outcomes but could not articulate
a specific barrier. This is acceptable — some users cannot ladder beyond outcomes.

INFER the most likely barrier from the deepest outcome. Frame it as a design gap.
If any slot says "(not identified)", infer from the conversation context and prefix with "[inferred]:".

Output format (start immediately, no preamble):

INTERVIEW_COMPLETE

Confirmed concern: {confirmed_concern}

SITUATION: {situation}
JOB: {job}
DESIRED OUTCOME: {outcome}
BARRIER (inferred): [infer from deepest outcome — what design gap prevents this outcome?]

JOB STORY: When {situation}, I want to {job}, so I can {outcome}, but [inferred barrier].

Design implication: [one sentence — the actionable design requirement]

Total turns: {total_turns}
Stopping reason: forced-endpoint — maximum outcome depth without barrier

Interview complete.
"""

@dataclass
class ChainExtraction:
    ladder_num: int
    level: str          # "A", "C", "V", "UNCLEAR"
    extract: str
    reasoning: str
    turn: int


@dataclass
class ChainState:
    extractions: List[ChainExtraction] = field(default_factory=list)
    asked_questions: List[str] = field(default_factory=list)
    c_cycling_redirect_count: int = field(default=0)
    asked_questions: List[str] = field(default_factory=list)

    # Escalation thresholds
    C_ESCALATION_THRESHOLD: int = field(default=2, init=False, repr=False)
    C_CYCLING_THRESHOLD: int = field(default=2, init=False, repr=False)

    # Hard ceiling from Reynolds & Gutman (1988)
    MAX_C_BEFORE_FORCED_ENDPOINT: int = field(default=5, init=False, repr=False)

    @property
    def confirmed_levels(self) -> List[str]:
        return [e.level for e in self.extractions if e.level != "UNCLEAR"]

    @property
    def has_A(self) -> bool:
        return "A" in self.confirmed_levels

    @property
    def has_C(self) -> bool:
        return "C" in self.confirmed_levels

    @property
    def has_V(self) -> bool:
        return "V" in self.confirmed_levels

    @property
    def first_confirmed_A(self) -> Optional[ChainExtraction]:
        for e in self.extractions:
            if e.level == "A":
                return e
        return None

    @property
    def total_c_count(self) -> int:
        return sum(1 for e in self.extractions if e.level == "C")

    @property
    def consecutive_c_count(self) -> int:
        count = 0
        for e in reversed(self.extractions):
            if e.level == "C":
                count += 1
            elif e.level in ("A", "V"):
                break
        return count

    @property
    def force_v_elicit(self) -> bool:
        """True when user is STUCK at same C level (consecutive threshold hit)...
        Only fires when c_cycling hasn't already taken over"""
        return (
            self.has_A
            and self.has_C
            and not self.has_V
            and self.consecutive_c_count >= self.C_ESCALATION_THRESHOLD
            and not self.c_cycling_detected   # c_cycling takes priority
        )

    @property
    def c_cycling_detected(self) -> bool:
        #True when user BROADENING (total C threshold hit) without V
        return (
            self.has_A
            and not self.has_V
            and self.total_c_count >= self.C_CYCLING_THRESHOLD
        )

    @property
    def use_absence_probe(self) -> bool:
        #True when the anchor redirect has been tried twice without producing V
        return self.c_cycling_detected and self.c_cycling_redirect_count >= 2

    @property
    def forced_endpoint_reached(self) -> bool:
        #True when maximum C depth has been hit without V
        return (
            self.has_A
            and self.has_C
            and not self.has_V
            and self.total_c_count >= self.MAX_C_BEFORE_FORCED_ENDPOINT
        )

    @property
    def best_anchor_c(self) -> Optional[ChainExtraction]:
        for e in self.extractions:
            if e.level == "C":
                return e
        return None

    @property
    def next_ladder_num(self) -> int:
        return len([e for e in self.extractions if e.level != "UNCLEAR"]) + 1

    @property
    def current_level(self) -> str:
        confirmed = [e for e in self.extractions if e.level != "UNCLEAR"]
        return confirmed[-1].level if confirmed else "A"

    def is_topic_drift(self, new_level: str, new_extract: str) -> bool:
        return new_level == "A" and self.has_A

    def chain_summary(self) -> str:
        lines = []
        for e in self.extractions:
            if e.level != "UNCLEAR":
                lines.append(f"  [Ladder {e.ladder_num}] [{e.level}] {e.extract}")
        return "\n".join(lines) if lines else "  (no confirmed steps yet)"

    def termination_chain_steps(self) -> str:
        lines = []
        for e in self.extractions:
            if e.level != "UNCLEAR":
                lines.append(f"-> [Ladder {e.ladder_num}] [{e.level}] {e.extract}")
        return "\n".join(lines)

    def ready_to_terminate(self, min_ladder_turns: int) -> Tuple[bool, str]:
        """Python gate: returns (can_terminate, reason). LLM never decides this."""
        confirmed = [e for e in self.extractions if e.level != "UNCLEAR"]
        if self.forced_endpoint_reached:
            return True, (
                "chain-endpoint-forced: maximum consequence depth reached "
                f"({self.total_c_count} C extractions) — participant cannot "
                "ladder beyond consequence level; accepting deepest operational "
                "requirement as chain endpoint"
            )

        if len(confirmed) < min_ladder_turns:
            return False, f"only {len(confirmed)} confirmed steps, need {min_ladder_turns}"
        if not self.has_A:
            return False, "no [A] confirmed yet"
        if not self.has_C:
            return False, "no [C] confirmed yet"
        if not self.has_V:
            return False, "no [V] confirmed yet — keep probing toward value"

        levels = self.confirmed_levels
        first_v_idx = next((i for i, l in enumerate(levels) if l == "V"), None)
        if first_v_idx is None:
            return False, "no [V] in confirmed levels"
        c_before_v = sum(1 for l in levels[:first_v_idx] if l == "C")
        if c_before_v < 1:
            return False, "no [C] before [V] — A→C→V structure not yet satisfied"
        return True, "A→C→V chain complete with minimum depth satisfied"

    def last_v_index(self) -> int:
        for i in range(len(self.extractions) - 1, -1, -1):
            if self.extractions[i].level == "V":
                return i
        return len(self.extractions) - 1


@dataclass
class JudgeFeedback:
    turn: int
    ladder_score: int
    deflection_score: int
    unlock_proximity: str
    repetition_flag: bool
    extracted_signal: bool
    suggested_tactic: str
    prohibited_patterns: List[str]
    composite_score: int


@dataclass
class JudgeLog:
    scores: list = field(default_factory=list)
    tactic_history: List[str] = field(default_factory=list)
    escalation_triggered: bool = False
    escalation_at_turn: Optional[int] = None


@dataclass
class FiveWhysState:
    why_chain: List[dict] = field(default_factory=list)
    # Each entry: {"why_num": int, "question": str, "answer": str,
    #              "level": "INTERMEDIATE" | "ROOT_CAUSE"}

    current_problem: str = ""       # the cause currently being interrogated ("why does X happen?")
    root_cause_found: bool = False
    asked_questions: List[str] = field(default_factory=list)
    SOFT_CEILING: int = field(default=10, init=False, repr=False)
    MIN_DEPTH: int = field(default=3, init=False, repr=False)  # don't accept ROOT_CAUSE before depth 3
    non_prescriptive_streak: int = field(default=0)
    FORCED_CHOICE_THRESHOLD: int = field(default=1, init=False, repr=False)
    MAX_NON_PRESCRIPTIVE_STREAK: int = field(default=3, init=False, repr=False)

    @property
    def depth(self) -> int:
        return len(self.why_chain)

    @property
    def can_terminate(self) -> bool:
        if self.root_cause_found and self.depth >= self.MIN_DEPTH:
            return True
        if self.depth >= self.MIN_DEPTH and self.non_prescriptive_streak >= self.MAX_NON_PRESCRIPTIVE_STREAK:
            return True
        return False

    def _is_circular(self) -> bool:
        if len(self.why_chain) < 2:
            return False
        last = self.why_chain[-1]["answer"].lower().strip()
        last_words = set(last.split())
        if not last_words:
            return False
        # Check 1: Adjacent overlap >60%
        prev = self.why_chain[-2]["answer"].lower().strip()
        prev_words = set(prev.split())
        if prev_words:
            overlap = len(last_words & prev_words) / max(len(last_words), len(prev_words))
            if overlap > 0.6:
                return True
        # Check 2: Recurring hedge phrases across entire chain
        _hedge_phrases = [
            "it usually comes down to",
            "it often comes down to",
            "from what i understand",
            "i think it's probably",
            "it's probably a bit hard for me to speak on",
            "how the company prioritizes",
            "core objectives",
        ]
        all_answers = [e["answer"].lower() for e in self.why_chain]
        for phrase in _hedge_phrases:
            count = sum(1 for a in all_answers if phrase in a)
            if count >= 3:
                return True
        # Check 3: Distant overlap last answer vs ANY earlier (not just prev)
        if len(self.why_chain) >= 4:
            for entry in self.why_chain[:-2]:  # skip last 2 (already checked adjacent)
                earlier_words = set(entry["answer"].lower().strip().split())
                if earlier_words:
                    overlap = len(last_words & earlier_words) / max(len(last_words), len(earlier_words))
                    if overlap > 0.50:
                        return True
        return False

    def chain_summary(self) -> str:
        if not self.why_chain:
            return "  (no why steps yet — about to ask Why 1)"
        lines = []
        for entry in self.why_chain:
            n = entry["why_num"]
            lines.append(f"  Why {n}: {entry['question'][:80]}")
            lines.append(f"  → {entry['answer'][:80]}")
        return "\n".join(lines)
    def termination_chain_steps(self) -> str:
        lines = []
        for entry in self.why_chain:
            n = entry["why_num"]
            lines.append(f"WHY {n}:")
            lines.append(f"Q: {entry['question']}")
            lines.append(f"A: {entry['answer']}")
            lines.append("")
        return "\n".join(lines)


@dataclass
class JTBDExtraction:
    ladder_num: int       # sequential extraction number
    level: str            # S / J / O / B / UNCLEAR
    extract: str          # the extracted phrase
    reasoning: str        # LLM's classification reasoning
    turn: int             # which interview turn

@dataclass
class JTBDState:
    extractions: List[JTBDExtraction] = field(default_factory=list)
    asked_questions: List[str] = field(default_factory=list)
    #after this many consecutive UNCLEAR at the same target level, auto-promote
    MAX_CONSECUTIVE_UNCLEAR: int = field(default=3, init=False, repr=False)
    #hard stall limit: if total turns exceeds this with 0 confirmed steps, abort
    MAX_STALL_TURNS: int = field(default=8, init=False, repr=False)
    #resets when any level is confirmed
    consecutive_unclear_count: int = field(default=0)
    #user answers collected during UNCLEAR streak
    unclear_answer_candidates: List[str] = field(default_factory=list)
    @property
    def confirmed_levels(self) -> List[str]:
        return [e.level for e in self.extractions if e.level != "UNCLEAR"]
    @property
    def has_S(self) -> bool:
        return "S" in self.confirmed_levels
    @property
    def has_J(self) -> bool:
        return "J" in self.confirmed_levels
    @property
    def has_O(self) -> bool:
        return "O" in self.confirmed_levels
    @property
    def has_B(self) -> bool:
        return "B" in self.confirmed_levels
    @property
    def current_level(self) -> str:
        confirmed = [e for e in self.extractions if e.level != "UNCLEAR"]
        return confirmed[-1].level if confirmed else "S"
    @property
    def next_ladder_num(self) -> int:
        return len([e for e in self.extractions if e.level != "UNCLEAR"]) + 1
    @property
    def next_expected_level(self) -> str:
        """First unfilled level in canonical S→J→O→B order. Empty when all confirmed."""
        confirmed_set = set(self.confirmed_levels)
        for level in ("S", "J", "O", "B"):
            if level not in confirmed_set:
                return level
        return ""
    @property
    def unclear_auto_promote(self) -> bool:
        """True when consecutive UNCLEAR threshold exceeded."""
        return self.consecutive_unclear_count >= self.MAX_CONSECUTIVE_UNCLEAR
    @property
    def first_confirmed_S(self) -> Optional[JTBDExtraction]:
        for e in self.extractions:
            if e.level == "S":
                return e
        return None
    def ready_to_terminate(self, min_ladder_turns: int = 4) -> Tuple[bool, str]:
        confirmed = [e for e in self.extractions if e.level != "UNCLEAR"]
        #stall detection
        total_turns = len(self.asked_questions)
        if total_turns >= self.MAX_STALL_TURNS and len(confirmed) == 0:
            return True, (
                f"chain-stall-abort: {total_turns} questions asked with 0 confirmed "
                f"JTBD steps — extractor unable to classify responses. "
                f"Consecutive UNCLEAR: {self.consecutive_unclear_count}"
            )
        if not self.has_S:
            return False, "no [S] confirmed yet"
        if not self.has_J:
            return False, "no [J] confirmed yet"
        if not self.has_O:
            return False, "no [O] confirmed yet"
        if not self.has_B:
            return False, "no [B] confirmed yet"
        return True, "S→J→O→B chain complete"

    def chain_summary(self) -> str:
        lines = []
        for e in self.extractions:
            if e.level != "UNCLEAR":
                lines.append(f"  [Ladder {e.ladder_num}] [{e.level}] {e.extract}")
        return "\n".join(lines) if lines else "  (no confirmed steps yet)"

    def termination_chain_steps(self) -> str:
        lines = []
        for e in self.extractions:
            if e.level != "UNCLEAR":
                lines.append(f"-> [Ladder {e.ladder_num}] [{e.level}] {e.extract}")
        return "\n".join(lines)

    def get_best_for_level(self, level: str) -> str:
        for e in self.extractions:
            if e.level == level:
                return e.extract
        return ""

def _extract_choice(text: str) -> Optional[str]:
    """
    Extract the MCQ letter (A-D) the persona selected.
    Strategy: collect ALL candidate matches across tiers, return the LAST one
    by position
    """
    candidates = []
    stripped = text.strip()

    #P-multi: detect explicit multi-select ("both B and C", "B or C", "B, C").
    for m in _re.finditer(
        r'\b([A-D])\s*(?:,\s*(?:and\b\s+)?|(?:\s+and\b|\s+or\b)\s+)([A-D])\b',
        text, _re.IGNORECASE
    ):
        candidates.append((m.start(2), m.group(2).upper()))

    #P0a: entire response is a single letter
    m = _re.match(r'^([A-D])[\.!\?\)]?\s*$', stripped, _re.IGNORECASE)
    if m:
        return m.group(1).upper()

    #P0b: letter appears alone at the START of a line
    for m in _re.finditer(
        r'(?:^|\n)\s*([A-D])[\.!\?]?\s*(?:\n|$)',
        text, _re.IGNORECASE
    ):
        candidates.append((m.start(), m.group(1).upper()))

    #P1: letter immediately followed by ), ., :, or separator-hyphen
    for m in _re.finditer(r'(?<![A-Za-z])([A-D])\s*(?:[\)\.:] | -(?![A-Za-z]))', text, _re.IGNORECASE):
        candidates.append((m.start(), m.group(1).upper()))

    #P2: explicit selection verb + letter e.g. "probably B", "I'd say C", "option A", "go with D"
    for m in _re.finditer(
        r'\b(?:option|choose|select|go\s+with|pick|probably|think|feel|'
        r'closest\s+to|closer\s+to|resonates|would\s+say|suggest|lean\s+toward|maybe|'
        r'i\'d\s+say|i\s+think|i\s+would|most\s+likely|more\s+like|leaning\s+toward|'
        r'more\s+toward|pointing\s+to|pointing\s+toward|aligns\s+with|more\s+of)\s+([A-D])\b',
        text, _re.IGNORECASE
    ):
        letter_char = m.group(1)
        #article guard: lowercase 'a' right after a trigger word is almost
        if letter_char == 'a' and _re.match(r'\s+[a-z]', text[m.end():]):
            continue
        candidates.append((m.start(), letter_char.upper()))

    #P3: isolated standalone letter as subject followed by qualifier verb e.g. "B would be closest", "C seems right", "A is the best fit"
    for m in _re.finditer(
        r'(?<![A-Za-z])([A-D])(?![A-Za-z])\s+(?:would|might|seems|is|could|appears)\b',
        text, _re.IGNORECASE
    ):
        letter_char = m.group(1)
        if letter_char == 'a' and _re.match(r'\s+[a-z]', text[m.end():]):
            continue
        candidates.append((m.start(), letter_char.upper()))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[-1][1]

def _strip_chain_annotations(text: str) -> tuple:
    """Remove any chain-tracking annotations the model appended after the question
    """
    m = _re.search(
        r'\n\s*\n\s*(Trigger:|CHAIN\s+\d+|Next question)',
        text, _re.IGNORECASE
    )
    if m:
        return text[:m.start()].strip(), text[m.start():].strip()
    return text, ""


def _parse_extraction(raw: str) -> Tuple[str, str, str]:
    level, extract, reasoning = "UNCLEAR", "", ""
    LABELS = ("LEVEL:", "EXTRACT:", "REASONING:")
    sections: Dict[str, str] = {}
    current_label = None
    current_lines: List[str] = []

    for line in raw.splitlines():
        stripped = line.strip()
        matched = None
        for lbl in LABELS:
            if stripped.upper().startswith(lbl):
                matched = lbl
                break
        if matched:
            if current_label:
                sections[current_label] = " ".join(current_lines).strip()
            current_label = matched.upper()
            # Capture text on the same line as the label
            after = stripped[len(matched):].strip()
            current_lines = [after] if after else []
        elif current_label:
            current_lines.append(stripped)

    if current_label:
        sections[current_label] = " ".join(current_lines).strip()
    # Parse LEVEL
    raw_level = sections.get("LEVEL:", "").upper().strip("[] \"'")
    # Accept ACV levels, JTBD levels, 5-Whys levels, and UNCLEAR
    if raw_level in ("A", "C", "V", "S", "J", "O", "B",
                      "INTERMEDIATE", "ROOT_CAUSE", "UNCLEAR"):
        level = raw_level
    extract = sections.get("EXTRACT:", "").strip("\"'")
    reasoning = sections.get("REASONING:", "").strip("\"'")
    return level, extract, reasoning


async def extract_from_response(
    client,
    model: str,
    persona_answer: str,
    chain_state: "ChainState",
    preceding_question: Optional[str] = None,
    temperature: float = 0.1,
    is_ollama: bool = False,
) -> Tuple[str, str, str]:
    confirmed = chain_state.confirmed_levels
    if not confirmed:
        anchoring_note = (
            "IMPORTANT: The chain has NO confirmed levels yet. "
            "Do NOT apply V-detection regardless of how the response is phrased. "
            "A strong declarative statement like 'X is non-negotiable' or 'The principle is Y' "
            "is the persona's stated position — classify it as [A] (their attribute/stance), "
            "not [V]. [V] can only be assigned after [A] and [C] are already confirmed. "
            "If the response contains ANY concrete, observable fact, example, or stated position "
            "classify it as [A] and extract that fact. "
            "Only classify as [C] if the response contains zero observable attributes "
            "and describes purely abstract consequences or impacts."
        )
    elif "A" in confirmed and "C" not in confirmed:
        anchoring_note = (
            "The chain has a confirmed [A] but no [C] yet. "
            "Do NOT apply V-detection — [V] cannot be assigned until [C] is confirmed. "
            "A strong principled statement at this stage is still [C] at most — "
            "it describes the impact or implication of the attribute. "
            "Look for a consequence or impact (so what does that cause?). "
            "Classify as [C] if present; otherwise stay at [A]."
        )
    elif "A" in confirmed and "C" in confirmed and "V" not in confirmed:
        c_depth = chain_state.total_c_count
        deep_note = ""
        if c_depth >= 3:
            deep_note = (
                f" CHAIN DEPTH: {c_depth} consequences confirmed. "
                "At this depth the participant is very likely stating a requirement, not just "
                "describing an impact. Treat ANY actionable directive as [V] — do not require "
                "formal requirement language or universal scope. "
                "EXCEPTION: vague quality directives ('make it clearer', 'make it more obvious', "
                "'make it easier to find', 'make it stand out more') are still [C] even at this "
                "depth — they name a desired quality without specifying which element or design "
                "property to change. [V] requires naming WHAT (element) + HOW (specific property: "
                "fill, color, size, contrast, placement, label, hierarchy)."
            )
        anchoring_note = (
            "The chain has [A] and [C] confirmed. "
            "V-detection is now ACTIVE. In this ACV reframing [V] = an ACTIONABLE DESIGN "
            "REQUIREMENT — something a product team could implement. It does NOT need to be "
            "a universal principle or hold across all contexts. It can be specific to this "
            "element or layout. "
            "Classify as [V] if the response contains ANY of: "
            "(a) an imperative design directive — 'reduce X', 'separate X from Y', "
            "'make the button solid fill', 'group X with Y', 'remove X', 'add X' — even if "
            "followed by a consequence explanation. "
            "CRITICAL EXCLUSION: 'make it clearer', 'make it more obvious', 'make it easier "
            "to find', 'make it stand out more', 'make it clear where to go' are NOT [V] — "
            "these are VAGUE QUALITY DIRECTIVES that name the desired quality but not the "
            "design mechanism. Classify them as [C]. "
            "[V] requires: (1) a named element ('the button', 'the label', 'the header') AND "
            "(2) a named property ('solid fill', 'brand color', '16px', 'high contrast'). "
            "If either is missing, it is [C]. "
            "Examples: 'make it clearer where you're supposed to go' → [C]; "
            "'make the Place Order button have a solid fill' → [V]; "
            "(b) a stated design requirement — 'this needs to do X', 'the product must X', "
            "'it should do X by default'; "
            "(c) a minimum standard — 'any design like this should X'; "
            "(d) a UI convention citation — 'most apps use X', 'that's the convention', "
            "'any app following conventions would have X', 'the standard is X' — where X "
            "names a SPECIFIC VISUAL PROPERTY (fill type, color, contrast, style); "
            "(e) a visual specification — participant names a concrete visual standard a "
            "developer could implement directly: 'filled button', 'solid color background', "
            "'brand color with white text', 'ghost outline vs solid fill', 'high contrast'. "
            "No imperative verb required — naming the spec IS the requirement; "
            "(f) a terminal self-assessment — 'that's all it needs to do', 'that's it', "
            "'that's the only thing', 'nothing else', 'that's the fix' — the participant "
            "is declaring the requirement complete. Extract the design statement preceding it. "
            "CRITICAL: If the response contains BOTH a design action AND a consequence "
            "explanation ('reduce X so that Y' / 'create X so users can Y'), classify as [V] "
            "— extract the design action, NOT the trailing consequence. "
            "Stay at [C] ONLY if the response describes a pure impact or experience with "
            "zero actionable directive and zero visual specification ('it makes me lose track', "
            "'it slows me down', 'I can't find it')."
            + deep_note
        )
    else:
        anchoring_note = (
            f"Confirmed levels so far: {confirmed}. Apply the lowest-level rule: "
            "extract the single most concrete, specific statement present."
        )
    if preceding_question:
        parroting_context = (
            f"\nInterviewer's preceding question:\n\"{preceding_question}\"\n\n"
            "Apply Step 0 (parroting check) before classifying."
        )
    else:
        parroting_context = "\n(No preceding question available — skip Step 0.)"

    user_content = (
        f"Participant response:\n\"{persona_answer}\"\n"
        f"{parroting_context}\n\n"
        f"{anchoring_note}"
    )
    messages = [
        {"role": "system", "content": _prepend_no_think(EXTRACTOR_SYSTEM, model, is_ollama)},
        {"role": "user",   "content": user_content},
    ]
    raw = await _llm_call(client, model, messages, temperature, 200, is_ollama, has_image=False)
    level, extract, reasoning = _parse_extraction(raw)
    return level, extract, reasoning


async def generate_question(
    client,
    model: str,
    memory: DecayingMemoryBuffer,
    chain_state: "ChainState",
    confirmed_concern: str,
    interview_type: InterviewType = InterviewType.WIREFRAME,
    product_label: str = "Wireframe UI",
    image_b64: str = "",
    image_media_type: str = "image/png",
    wireframe_images: list = None,
    topic_drifted: bool = False,
    temperature: float = 0.4,
    is_ollama: bool = False,
    ladder_depth: int = 0,
    judge_feedback: Optional["JudgeFeedback"] = None,
    shadow_mode: bool = True,
) -> str:
    phase_probes = PROBE_INSTRUCTIONS[interview_type]

    if topic_drifted and chain_state.first_confirmed_A:
        probe_instr = phase_probes["C"]
        override = _build_a_redirect(interview_type, chain_state.first_confirmed_A.extract)
    elif chain_state.use_absence_probe and chain_state.best_anchor_c and chain_state.first_confirmed_A:
        probe_instr = phase_probes["V_ELICIT"]
        override = _build_absence_probe(
            interview_type,
            chain_state.best_anchor_c.extract,
            chain_state.first_confirmed_A.extract,
        )
    elif chain_state.c_cycling_detected and chain_state.best_anchor_c:
        probe_instr = phase_probes["V_ELICIT_FROM_ANCHOR"]
        override = _build_c_anchor_redirect(interview_type, chain_state.best_anchor_c.extract)
    elif chain_state.force_v_elicit:
        probe_instr = phase_probes["V_ELICIT"]
        override = "IMPORTANT OVERRIDE: Stop exploring consequences. Pivot to underlying design requirement now."
    else:
        probe_instr = phase_probes.get(chain_state.current_level, phase_probes["A"])
        override = ""

    c_depth_note = ""
    if chain_state.total_c_count >= 3 and not chain_state.has_V:
        phase_labels = {
            InterviewType.WIREFRAME: "layout requirements",
        }
        c_depth_note = (
            f"\nNOTE: {chain_state.total_c_count} consequence turns confirmed without "
            f"reaching a stable {phase_labels[interview_type]}. Do NOT ask another "
            "consequence question. Force a positional statement about what must change."
        )

    raw_system = _build_questioner_system(
        interview_type=interview_type,
        product_label=product_label,
        confirmed_concern=confirmed_concern,
        chain_summary=chain_state.chain_summary(),
        current_level=chain_state.current_level,
        extraction=chain_state.extractions[-1].extract if chain_state.extractions else "",
        next_ladder_num=chain_state.next_ladder_num,
        probe_instruction=probe_instr,
        override_instruction=override + c_depth_note,
        asked_questions=chain_state.asked_questions,
    )

    if judge_feedback is not None and not shadow_mode:
        raw_system += (
            f"\n\nMANDATORY JUDGE OVERRIDE — you MUST follow this:\n"
            f"TACTIC: {judge_feedback.suggested_tactic}\n"
            f"Your next question MUST implement this tactic. Do NOT ignore it.\n"
            f"Unlock proximity: {judge_feedback.unlock_proximity}\n"
        )
        if judge_feedback.prohibited_patterns:
            raw_system += (
                "BANNED question patterns (using any of these is a failure): "
                + ", ".join(judge_feedback.prohibited_patterns)
                + "\n"
            )
    system = _prepend_no_think(raw_system, model, is_ollama)
    messages = memory.get_interviewer_messages(system)
    trigger_text = "Generate your next laddering question now. One question only. No preamble."
    _wf_images = wireframe_images or ([( image_b64, image_media_type)] if image_b64 else [])
    send_image = (
        interview_type == InterviewType.WIREFRAME
        and bool(_wf_images)
        and (not is_ollama or ladder_depth == 0)
    )
    if send_image:
        content = []
        for idx, (b64, mtype) in enumerate(_wf_images, 1):
            content.append({"type": "text",
                            "text": f"[Wireframe screen {idx} of {len(_wf_images)} — shown to participant]"})
            content.append({"type": "image_url",
                            "image_url": {"url": f"data:{mtype};base64,{b64}"}})
        content.append({"type": "text", "text": trigger_text})
        messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": trigger_text})
    question = await _llm_call(
        client, model, messages, temperature, 120, is_ollama,
        has_image=send_image,
    )
    question = _re.sub(r'^\[Ladder\s*\d+\]\s*', '', question).strip()
    question = _re.sub(r'^\[Ladder\s*\d+\]\s*', '', question).strip()
    if not question:
        raise RuntimeError(
            f"[generate_question] Model '{model}' returned empty output after retry.\n"
            "No hardcoded probe questions — fix the model connection and re-run.\n"
            "Check: (1) ollama serve is running, (2) model is pulled,\n"
            f"  ollama pull {model}"
        )
    return question


def _parse_judge_output(raw: str, turn: int) -> "JudgeFeedback":
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = _re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = _re.sub(r'\s*```\s*$', '', cleaned)
        data = json.loads(cleaned)
        ladder = int(data.get("ladder_score", 1))
        defl = int(data.get("deflection_score", 1))
        rep = bool(data.get("repetition_flag", False))
        return JudgeFeedback(
            turn=data.get("turn", turn),
            ladder_score=ladder,
            deflection_score=defl,
            unlock_proximity=str(data.get("unlock_proximity", "far")),
            repetition_flag=rep,
            extracted_signal=bool(data.get("extracted_signal", True)),
            suggested_tactic=str(data.get("suggested_tactic", "Continue current approach")),
            prohibited_patterns=list(data.get("prohibited_patterns", [])),
            composite_score=int(data.get("composite_score", ladder + defl - (1 if rep else 0))),
        )
    except Exception:
        return JudgeFeedback(
            turn=turn,
            ladder_score=1,
            deflection_score=1,
            unlock_proximity="far",
            repetition_flag=False,
            extracted_signal=True,
            suggested_tactic="Continue current approach",
            prohibited_patterns=[],
            composite_score=2,
        )


async def judge_turn(
    probe_text: str,
    persona_answer: str,
    chain_state: "ChainState",
    vague_seed: str,
    prior_response: str,
    judge_log: "JudgeLog",
    is_ollama: bool,
    judge_model: str,
    judge_client,                  # openai.AsyncOpenAI OR _AnthropicClientShim
    laddering_method: LadderingMethod = LadderingMethod.ACV,
    method_state: object = None,   # FiveWhysState or JTBDState when applicable
) -> "JudgeFeedback":
    """
    Evaluate a single probe+answer pair. Returns structured JudgeFeedback
    Method-aware: rubric adapts to ACV, 5-Whys, or JTBD
    """
    turn = len(judge_log.scores) + 2
    if laddering_method == LadderingMethod.FIVE_WHYS and method_state is not None:
        chain_snapshot = {
            "method": "5whys",
            "depth": method_state.depth,
            "current_problem": method_state.current_problem,
            "chain_summary": method_state.chain_summary(),
            "root_cause_found": method_state.root_cause_found,
        }
        rubric = (
            "## Evaluation Rubric — 5-WHYS METHOD:\n\n"
            "1. **Causal depth** (0-3): Did the probe push DEEPER into the causal chain? "
            "Probing organizational/business process (leaving design scope) scores 0. "
            "Staying in the design domain and probing a deeper design cause scores 1-2. "
            "Probing toward a specific design decision (color, font, layout, spacing) scores 3.\n\n"
            "2. **Probe quality** (0-3): Did the probe open a new angle or rephrase an old one? "
            "Ignoring a prior deflection scores 0. "
            "Partially redirecting scores 1-2. Sharp, targeted probe scores 3.\n\n"
            "3. **Unlock proximity** (\"far\" | \"approaching\" | \"near\"): How close is the "
            "chain to a specific, actionable design decision?\n\n"
            "4. **Repetition penalty**: Is the probe semantically similar to any prior "
            "asked question? If near-duplicate, set repetition_flag to true.\n\n"
            "5. **Signal quality**: Did the participant's answer contain a genuine design-specific "
            "cause, or did they deflect to organizational process? "
            "Design cause = extracted_signal true. Org deflection = extracted_signal false.\n\n"
            "## CRITICAL: 5-Whys specific tactics:\n"
            "- If the participant's answer identifies a SPECIFIC DESIGN DECISION (button color, "
            "font weight, element placement, spacing), your suggested_tactic should say: "
            "\"The participant identified a specific design decision — this is likely the root cause. "
            "Probe for the design implication (what should change).\"\n"
            "- If the persona's answer drifts to organizational process (company priorities, "
            "team structure, leadership, sprint planning), your suggested_tactic should say: "
            "\"Redirect to the wireframe — ask about a specific element in the layout.\"\n"
            "- Do NOT suggest 'pivot to underlying value' — that is ACV, not 5-Whys.\n"
        )
    elif laddering_method == LadderingMethod.JTBD and method_state is not None:
        _confirmed = list(set(method_state.confirmed_levels)) if hasattr(method_state, 'confirmed_levels') else []
        _missing = [l for l in ("S", "J", "O", "B") if l not in _confirmed]
        _next_target = (
            method_state.next_expected_level
            if hasattr(method_state, 'next_expected_level')
            else (_missing[0] if _missing else "")
        )
        _chain_depth = len(method_state.extractions) if hasattr(method_state, 'extractions') else 0
        chain_snapshot = {
            "method": "jtbd",
            "confirmed_levels": _confirmed,
            "missing_levels": _missing,
            "next_target_level": _next_target,
            "chain_depth": _chain_depth,
        }
        _level_tactic_hints = {
            "S": (
                "The interviewer needs to surface the SITUATION — the specific moment or "
                "context on screen that made the concern stand out. Suggest an approach to "
                "get the persona to describe what they were LOOKING AT when they noticed it. "
                "Example: 'Ask them to describe the specific part of the layout that caught "
                "their eye — ground it in a visible element, not an abstract feeling.'"
            ),
            "J": (
                "The interviewer needs to surface the JOB — what the persona was trying to "
                "ACCOMPLISH or VERIFY when they looked at this screen. Suggest an approach "
                "that elicits a concrete functional task, not a goal statement. "
                "Example: 'Ask what they were trying to check or confirm before moving on — "
                "what question were they trying to answer for themselves?'"
            ),
            "O": (
                "The interviewer needs to surface the DESIRED OUTCOME — what SUCCESS looks "
                "like for the persona. Suggest an approach that gets a concrete vision of "
                "better, not just 'what's wrong'. "
                "Example: 'Ask what a fixed version of this would make easier — what would "
                "they be able to do or know that they can't do or know right now?'"
            ),
            "B": (
                "The interviewer needs to surface the BARRIER — a specific, current design "
                "friction that prevents the outcome. Suggest an approach that pins the "
                "persona to a concrete element, not a vague complaint. "
                "Example: 'Ask them to point to the specific thing in the layout that makes "
                "it hard — name an element, a label, a placement choice.'"
            ),
            "": (
                "The Job Story chain is complete. Suggest probing for the design implication — "
                "what one change would resolve the barrier and let the job get done."
            ),
        }
        _tactic_hint = _level_tactic_hints.get(_next_target, _level_tactic_hints[""])
        rubric = (
            "## Evaluation Rubric — JTBD METHOD:\n\n"
            "The JTBD (Jobs-to-be-Done) interview goal is to surface the complete Job Story:\n"
            "  \"When [situation], I want to [job], so I can [outcome], but [barrier].\"\n\n"
            f"**Chain status**: Confirmed: {_confirmed or '(none yet)'}, Missing: {_missing}\n"
            f"**NEXT TARGET LEVEL**: [{_next_target}] — the interviewer is currently "
            f"probing for [{_next_target}] content from the participant.\n\n"
            "1. **Probe alignment** (0-3): Did the probe effectively try to elicit "
            f"[{_next_target}] content from the participant?\n"
            f"  0 = Probe asked about a completely different level or drifted off-topic\n"
            f"  1 = Probe was loosely aimed at [{_next_target}] but too abstract or generic\n"
            f"  2 = Probe targeted [{_next_target}] concretely but used an angle the participant deflected\n"
            f"  3 = Probe was well-targeted at [{_next_target}] with a fresh angle that elicited "
            f"clear [{_next_target}] content\n\n"
            "2. **Probe freshness** (0-3): Did the probe introduce a new angle or just rephrase a prior question? "
            "Near-duplicate scores 0. Fresh angle scores 3.\n\n"
            f"3. **Unlock proximity** (\"far\" | \"approaching\" | \"near\"): How close is the "
            f"chain to completing all four JTBD levels?\n\n"
            "4. **Repetition penalty**: Is the probe semantically similar to any prior "
            "asked question? If near-duplicate, set repetition_flag to true.\n\n"
            "5. **Signal quality**: Did the participant's answer contain genuine "
            f"[{_next_target}] content, or did they deflect? "
            f"Clear [{_next_target}] content = extracted_signal true. Deflection = false.\n\n"
            f"## CRITICAL: suggested_tactic for [{_next_target}]\n"
            f"The next question MUST still target [{_next_target}]. Do NOT suggest switching "
            f"to a different level. Your suggested_tactic should advise HOW to ask a better "
            f"[{_next_target}] probe — the approach or angle to try next.\n\n"
            f"{_tactic_hint}\n\n"
            "Do NOT suggest 'pivot to underlying value' — that is ACV methodology, not JTBD.\n"
        )
    else:
        chain_snapshot = {
            "method": "acv",
            "confirmed_levels": chain_state.confirmed_levels,
            "has_A": chain_state.has_A,
            "has_C": chain_state.has_C,
            "has_V": chain_state.has_V,
            "total_c_count": chain_state.total_c_count,
            "consecutive_c_count": chain_state.consecutive_c_count,
            "current_level": chain_state.current_level,
            "chain_summary": chain_state.chain_summary(),
        }
        rubric = (
            "## Evaluation Rubric — ACV METHOD:\n\n"
            "The ACV interview goal is to surface actionable DESIGN REQUIREMENTS by climbing:\n"
            "  [A] Attribute — a concrete, observable UI element the user reacted to\n"
            "  [C] Consequence — the functional or experiential UX IMPACT of that element\n"
            "  [V] Value — the actionable DESIGN REQUIREMENT the product must meet\n"
            "The end value [V] is a specific design principle or requirement (e.g., "
            "'typography must create clear information hierarchy', 'primary CTA must be "
            "visually dominant over secondary actions'). It is NOT an abstract personal "
            "value or organizational goal.\n\n"
            "1. **Design-ladder fidelity** (0-3): Did the probe push the conversation "
            "toward a concrete DESIGN REQUIREMENT?\n"
            "  0 = Probe drifted into organizational process, business strategy, or abstract "
            "values (company priorities, leadership decisions, team structure, sprint planning). "
            "These leave the design domain and produce no actionable design insight.\n"
            "  1 = Probe stays in design territory but laterally (A→A: asking about another "
            "attribute without connecting to UX impact) or regresses (C→A: back to surface).\n"
            "  2 = Probe moves upward in the chain: A→C (from element to its UX impact) or "
            "C→C (deepening the consequence — narrowing toward the core UX friction).\n"
            "  3 = Probe deliberately targets the design requirement [V]: asks what the design "
            "MUST do differently, what principle is violated, or what specific design rule "
            "would resolve all the consequences discussed.\n\n"
            "2. **Probe freshness** (0-3): Did the probe open a new angle or repeat a prior question? "
            "Near-duplicate scores 0. Fresh angle or technique (contrast, scenario, absence) scores 3.\n\n"
            "3. **Unlock proximity** (\"far\" | \"approaching\" | \"near\"): How close is the "
            "chain to reaching a stable design requirement [V]?\n\n"
            "4. **Repetition penalty**: Is the probe semantically similar to any prior "
            "asked question? If near-duplicate, set repetition_flag to true.\n\n"
            "5. **Signal quality**: Did the participant's answer contain a genuine design insight "
            "(a specific UI element, a UX impact, or a design requirement)? "
            "Design-specific content = extracted_signal true. "
            "Organizational deflection or abstract platitudes = extracted_signal false.\n\n"
            "## CRITICAL: ACV-specific suggested_tactic rules:\n"
            "Your suggested_tactic must steer the interviewer toward the DESIGN REQUIREMENT, "
            "not abstract values or organizational reasons.\n\n"
            "- If chain has [A] but no [C]: suggest probing the UX IMPACT — "
            "'Ask what happens to the user experience because of [specific element]. "
            "What does it make harder, confusing, or slower?'\n"
            "- If chain has [C] but no [V]: suggest probing the DESIGN REQUIREMENT — "
            "'Ask what design principle or rule this element violates. What must the "
            "design do differently to resolve this UX friction?'\n"
            "- If the participant drifted to organizational process (team decisions, company "
            "priorities, leadership strategy): suggest REDIRECTING to the wireframe — "
            "'The participant left the design domain. Redirect: ask about a specific visual "
            "element in the layout and its impact on the user.'\n"
            "- Do NOT suggest probing 'personal values', 'professional values', or "
            "'why this matters to you personally' — the end value [V] is a DESIGN "
            "requirement, not a life philosophy.\n"
        )
    system_prompt = (
        "You are a Judge agent evaluating the quality of an interviewer's probe "
        f"in a {laddering_method.value.upper()} laddering interview.\n\n"
        f"## Interview Origin\n"
        f"Vague seed (the phrase being explored): \"{vague_seed}\"\n"
        f"Prior response (participant's initial reaction): \"{prior_response}\"\n\n"
        f"## Current Turn\n"
        f"Probe being evaluated: \"{probe_text}\"\n"
        f"Participant's answer to this probe: \"{persona_answer}\"\n\n"
        f"## Chain State\n{json.dumps(chain_snapshot, indent=2)}\n\n"
        f"## Tactic History\n"
        f"{json.dumps(judge_log.tactic_history) if judge_log.tactic_history else '[]'}\n\n"
        + rubric +
        "## Output Instruction\n"
        "Output ONLY a valid JSON object with these exact fields. "
        "No prose, no markdown fences, no explanation:\n"
        "{\n"
        f"  \"turn\": {turn},\n"
        "  \"ladder_score\": <0-3>,\n"
        "  \"deflection_score\": <0-3>,\n"
        "  \"unlock_proximity\": \"<far|approaching|near>\",\n"
        "  \"repetition_flag\": <true|false>,\n"
        "  \"extracted_signal\": <true|false>,\n"
        "  \"suggested_tactic\": \"<1-2 sentence directive for the next probe>\",\n"
        "  \"prohibited_patterns\": [\"<phrase to avoid>\"],\n"
        "  \"composite_score\": <ladder_score + deflection_score "
        "- (1 if repetition_flag else 0)>\n"
        "}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Evaluate the probe now. Output only the JSON object."},
    ]
    raw = await _llm_call(
        judge_client, judge_model, messages,
        temperature=0.2, max_tokens=500,
        is_ollama=is_ollama, has_image=False,
        ollama_num_ctx=8192, ollama_skip_floor=True,
    )
    return _parse_judge_output(raw, turn)


async def generate_judge_report(
    judge_log: "JudgeLog",
    chain_state: "ChainState",
    actual_turns: int,
    min_depth: int,
    is_ollama: bool,
    judge_model: str,
    judge_client,
) -> dict:
    import openai as _openai
    laddering_efficiency = min((min_depth + 1) / max(actual_turns, 1), 1.0)
    turn_scores = []
    for fb in judge_log.scores:
        turn_scores.append({
            "turn": fb.turn,
            "composite": fb.composite_score,
            "ladder": fb.ladder_score,
            "deflection": fb.deflection_score,
            "unlock_proximity": fb.unlock_proximity,
        })
    system_prompt = (
        "You are producing a post-session debriefing report for a laddering "
        "interview judge.\n\n"
        f"## Session Data\n"
        f"Actual turns: {actual_turns}\n"
        f"Minimum depth: {min_depth}\n"
        f"Laddering efficiency: {laddering_efficiency:.3f} "
        "(computed as (min_depth + 1) / actual_turns, capped at 1.0)\n\n"
        f"## Turn-by-Turn Scores\n{json.dumps(turn_scores, indent=2)}\n\n"
        f"## Tactic History\n{json.dumps(judge_log.tactic_history)}\n\n"
        f"## Escalation\n"
        f"Triggered: {judge_log.escalation_triggered}\n"
        f"At turn: {judge_log.escalation_at_turn}\n\n"
        f"## Chain State\n{chain_state.chain_summary()}\n\n"
        "## Task\n"
        "Produce a structured JSON report with these fields:\n"
        "- turn_scores: list of {\"turn\": N, \"composite\": N, \"ladder\": N, "
        "\"deflection\": N, \"unlock_proximity\": \"...\"}\n"
        "- escalation_triggered: bool\n"
        "- missed_unlock_opportunities: list of strings "
        "(natural language descriptions)\n"
        "- deflection_patterns_uncountered: list of strings\n"
        f"- laddering_efficiency: {laddering_efficiency:.3f} "
        "(given — include exactly as provided)\n"
        "- overall_assessment: 1-2 sentence summary of interview quality\n\n"
        "Output ONLY valid JSON. No prose, no markdown fences."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Generate the debriefing report now."},
    ]
    try:
        raw = await _llm_call(
            judge_client, judge_model, messages,
            temperature=0.2, max_tokens=1000,
            is_ollama=is_ollama, has_image=False,
            ollama_num_ctx=8192, ollama_skip_floor=True,
        )
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = _re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = _re.sub(r'\s*```\s*$', '', cleaned)
        report = json.loads(cleaned)
        report["laddering_efficiency"] = laddering_efficiency
        return report
    except Exception:
        return {
            "turn_scores": turn_scores,
            "escalation_triggered": judge_log.escalation_triggered,
            "missed_unlock_opportunities": [],
            "deflection_patterns_uncountered": [],
            "laddering_efficiency": laddering_efficiency,
            "overall_assessment": "Report generation failed — scores available in turn_scores.",
        }


async def generate_termination_summary(
    client,
    model: str,
    chain_state: "ChainState",
    confirmed_concern: str,
    stopping_reason: str,
    product_description: str = "",
    prior_response: str = "",
    vague_seed: str = "",
    temperature: float = 0.2,
    is_ollama: bool = False,
) -> str:
    total_steps = len([e for e in chain_state.extractions if e.level != "UNCLEAR"])
    chain_steps = chain_state.termination_chain_steps()

    if chain_state.forced_endpoint_reached:
        c_extractions = [e for e in chain_state.extractions if e.level == "C"]
        deepest_c = c_extractions[-1].extract if c_extractions else "(no consequence confirmed)"
        _raw_sum = FORCED_ENDPOINT_SUMMARISER_SYSTEM.format(
            product_description=product_description,
            prior_response=prior_response,
            vague_seed=vague_seed,
            confirmed_concern=confirmed_concern,
            chain_steps=chain_steps,
            deepest_c=deepest_c,
            total_steps=total_steps,
            stopping_reason=stopping_reason,
        )
        system = _prepend_no_think(_raw_sum, model, is_ollama)
    else:
        _raw_sum = SUMMARISER_SYSTEM.format(
            product_description=product_description,
            prior_response=prior_response,
            vague_seed=vague_seed,
            confirmed_concern=confirmed_concern,
            chain_steps=chain_steps,
            total_steps=total_steps,
            stopping_reason=stopping_reason,
        )
        system = _prepend_no_think(_raw_sum, model, is_ollama)

    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": "Write the termination block now."},
    ]
    return await _llm_call(client, model, messages, temperature, 600, is_ollama, has_image=False)

def _build_five_whys_questioner_system(
    interview_type: InterviewType,
    product_label: str,
    confirmed_concern: str,
    five_whys_state: "FiveWhysState",
    judge_feedback: Optional["JudgeFeedback"] = None,
    shadow_mode: bool = True,
) -> str:
    phase_labels = {
        InterviewType.WIREFRAME: "Wireframe Review",
    }
    phase_notes = {
        InterviewType.WIREFRAME: (
            "WIREFRAME PHASE — CRITICAL CONSTRAINTS:\n"
            "The participant is reacting to a STATIC PROTOTYPE IMAGE — they LOOKED at it,\n"
            "they never tapped, clicked, navigated, or completed any action within it.\n"
            "Every question must be framed as reviewing a layout, not using a live app.\n"
            "BANNED phrases: 'tap', 'click', 'scroll', 'proceed', 'move forward', 'complete',\n"
            "'navigate to', 'before deciding', 'whether to proceed', 'use the app',\n"
            "'did you find it', 'were you able to', 'what happened when', 'go through'.\n"
            "Reference visible layout only: placement, labelling, visual weight, hierarchy."
        ),
    }
    if five_whys_state.asked_questions:
        aq_block = "\n".join(
            f"  {i+1}. \"{q}\"" for i, q in enumerate(five_whys_state.asked_questions)
        )
    else:
        aq_block = "  (none yet — this is the first Why question)"
    domain_drift_warning = ""
    if five_whys_state.depth >= 3:
        _last_answer = five_whys_state.why_chain[-1]["answer"].lower() if five_whys_state.why_chain else ""
        _org_signals = [
            "company prioriti", "leadership", "executive team", "sprint planning",
            "high-pressure", "aggressive launch", "time-to-market", "competitive landscape",
            "market share", "organizational", "resource allocation", "internal strategy",
            "trade-offs are made", "internal guidelines", "happy path",
        ]
        _org_count = sum(1 for sig in _org_signals if sig in _last_answer)
        if _org_count >= 2:
            domain_drift_warning = (
                "\nDOMAIN DRIFT DETECTED — the participant's last answer left the design "
                "domain and entered organizational/business territory.\n"
                "REDIRECT BACK TO THE WIREFRAME. Your next question MUST reference a specific "
                "element in the layout (button, font, spacing, placement, color, hierarchy).\n"
                "Example: \"Coming back to the wireframe — what about the [element]'s "
                "[specific property] makes it contribute to this issue?\"\n"
            )
    prescription_note = ""
    if five_whys_state.depth >= 3:
        _last_answer = (five_whys_state.why_chain[-1]["answer"] if five_whys_state.why_chain else "").lower()
        _prescriptive_signals = [
            "should be", "needs to be", "needs a", "should have", "must be",
            "would need", "change to", "replace with", "use a ", "add a ",
            "minimum", " px", "contrast ratio", "accessible", "filled",
            "solid fill", "background color", "font size", "bold",
        ]
        _is_already_prescriptive = any(sig in _last_answer for sig in _prescriptive_signals)
        if not _is_already_prescriptive:
            prescription_note = (
                "\nPRESCRIPTION MODE — the participant has identified what is wrong "
                "but has not yet stated what should be built differently. "
                "Your next question MUST ask for the specific fix, not another 'why'.\n"
                "Preferred question forms:\n"
                "  * \"What would [element] need to look like for this not to be a problem?\"\n"
                "  * \"If you were fixing this, what specifically would you change about [element]?\"\n"
                "  * \"What should [element] do or look like instead?\"\n"
                "  * \"What would make [element] clearly recognizable as [its purpose]?\"\n"
                "Do NOT ask another causal 'why' question — the problem is identified. "
                "Probe for the concrete prescription.\n"
            )

    if five_whys_state.non_prescriptive_streak >= five_whys_state.FORCED_CHOICE_THRESHOLD:
        prescription_note = (
            "\nFORCED-CHOICE MODE — the participant has repeated the same diagnostic "
            "observation without stating a fix, even when asked directly. Open-ended "
            "questions are not working. Do NOT ask another open 'what would need to change' "
            "question.\n"
            "Instead, generate a question that offers 2–3 CONCRETE, SPECIFIC design options "
            "grounded in what they already mentioned, and ask them to pick the closest one or "
            "name what's missing.\n"
            "Example pattern: \"Would it help if [specific concrete option A — e.g. a solid "
            "color fill with high contrast], or is it more about [specific concrete option B — "
            "e.g. the text size or label]? Or is there something else specific you'd point to?\"\n"
            "Ground the options in their own words (color, contrast, size, fill, placement) — "
            "do not invent unrelated design concepts.\n"
        )

    judge_injection = ""
    if judge_feedback and not shadow_mode:
        judge_injection = (
            f"\n\nMANDATORY JUDGE OVERRIDE — you MUST follow this:\n"
            f"TACTIC: {judge_feedback.suggested_tactic}\n"
            f"Your next question MUST implement this tactic. Do NOT ignore it.\n"
        )
        if judge_feedback.prohibited_patterns:
            judge_injection += (
                "BANNED question patterns (using any of these is a failure): "
                + ", ".join(judge_feedback.prohibited_patterns)
                + "\n"
            )
    return FIVE_WHYS_QUESTIONER_SYSTEM.format(
        interview_phase_label=phase_labels[interview_type],
        product_label=product_label,
        confirmed_concern=confirmed_concern,
        chain_summary=five_whys_state.chain_summary(),
        current_problem=five_whys_state.current_problem,
        why_depth=five_whys_state.depth,
        asked_questions_block=aq_block,
        next_why_num=five_whys_state.depth + 1,
        phase_questioner_note=phase_notes[interview_type],
        judge_injection=judge_injection,
        domain_drift_warning=domain_drift_warning,
        prescription_note=prescription_note,
    )


def _build_five_whys_chain_context(five_whys_state: "FiveWhysState") -> str:
    if not five_whys_state.why_chain:
        return "Chain so far: (starting — this is the first response after the confirmed concern)"
    lines = ["Chain so far:"]
    for entry in five_whys_state.why_chain:
        lines.append(f"  Why {entry['why_num']}: {entry['answer'][:100]}")
    depth = five_whys_state.depth
    if depth >= 3:
        lines.append(
            f"\nDepth is {depth} — the chain has enough causal steps. "
            "ROOT_CAUSE is appropriate ONLY if this answer is PRESCRIPTIVE: it states "
            "a specific, implementable UI change (e.g. 'use a filled button with contrasting "
            "color', 'minimum 16px text', 'accessible contrast ratio'). "
            "If the answer merely identifies a problem element or describes what is wrong "
            "without stating the fix, classify as INTERMEDIATE."
        )
    if depth >= 6:
        lines.append(
            "WARNING: Chain is very deep. Accept ROOT_CAUSE for: "
            "(a) a concrete implementable UI directive, OR "
            "(b) domain departure into org/process territory."
        )
    return "\n".join(lines)


async def extract_five_whys_response(
    client,
    model: str,
    persona_answer: str,
    current_depth: int,
    five_whys_state: "FiveWhysState",
    temperature: float = 0.1,
    is_ollama: bool = False,
) -> Tuple[str, str, str]:
    chain_context = _build_five_whys_chain_context(five_whys_state)
    system = _prepend_no_think(
        FIVE_WHYS_EXTRACTOR_SYSTEM.format(
            current_depth=current_depth,
            chain_context=chain_context,
        ),
        model, is_ollama,
    )
    user_content = f'Participant response:\n"{persona_answer}"'
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": user_content},
    ]
    raw = await _llm_call(client, model, messages, temperature, 300, is_ollama, has_image=False)
    level, extract, reasoning = _parse_extraction(raw)
    if level == "V":
        level = "ROOT_CAUSE"
    elif level in ("A", "C", "S", "J", "O", "B"):
        level = "INTERMEDIATE"
    elif level == "UNCLEAR":
        level = "INTERMEDIATE"
    if level == "INTERMEDIATE" and current_depth >= 4:
        _answer_lower = persona_answer.lower()
        _reasoning_lower = reasoning.lower()
        _domain_departure_signals = [
            "company prioriti",
            "leadership decision",
            "leadership feels",
            "leadership team",
            "executive team",
            "sprint planning",
            "high-pressure cycle",
            "aggressive launch",
            "time-to-market",
            "competitive landscape",
            "market share",
            "organizational",
            "resource allocation",
            "resource limitation",
            "internal strategy",
            "trade-offs are made by",
            "internal guidelines",
            "it usually comes down to how the company",
            "it often comes down to how the company",
        ]
        _departure_count = sum(
            1 for sig in _domain_departure_signals
            if sig in _answer_lower or sig in _reasoning_lower
        )
        if _departure_count >= 2:
            print(f"    [5W-EXTRACTOR] AUTO-PROMOTE to ROOT_CAUSE: "
                  f"{_departure_count} domain-departure signals detected")
            level = "ROOT_CAUSE"
    return level, extract, reasoning


async def generate_five_whys_question(
    client,
    model: str,
    five_whys_state: "FiveWhysState",
    confirmed_concern: str,
    interview_type: InterviewType = InterviewType.WIREFRAME,
    product_label: str = "",
    temperature: float = 0.4,
    is_ollama: bool = False,
    judge_feedback: Optional["JudgeFeedback"] = None,
    shadow_mode: bool = True,
) -> str:
    raw_system = _build_five_whys_questioner_system(
        interview_type=interview_type,
        product_label=product_label,
        confirmed_concern=confirmed_concern,
        five_whys_state=five_whys_state,
        judge_feedback=judge_feedback,
        shadow_mode=shadow_mode,
    )
    system = _prepend_no_think(raw_system, model, is_ollama)
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": "Generate the next Why question now. One question only. No preamble."},
    ]
    question = await _llm_call(client, model, messages, temperature, 120, is_ollama, has_image=False)
    question = question.strip()
    if not question:
        raise RuntimeError(
            f"[generate_five_whys_question] Model '{model}' returned empty output after retry."
        )
    return question


async def generate_five_whys_summary(
    client,
    model: str,
    five_whys_state: "FiveWhysState",
    confirmed_concern: str,
    stopping_reason: str,
    product_description: str = "",
    temperature: float = 0.2,
    is_ollama: bool = False,
    force_inferred_implication: bool = False,
) -> str:
    chain_steps = five_whys_state.termination_chain_steps()
    total_steps = five_whys_state.depth
    root_cause = five_whys_state.current_problem

    if force_inferred_implication:
        system_template = FIVE_WHYS_FORCED_ENDPOINT_SUMMARISER_SYSTEM
    else:
        system_template = FIVE_WHYS_SUMMARISER_SYSTEM
    raw_sum = system_template.format(
        product_description=product_description,
        confirmed_concern=confirmed_concern,
        chain_steps=chain_steps,
        root_cause=root_cause,
        total_steps=total_steps,
        stopping_reason=stopping_reason,
    )
    system = _prepend_no_think(raw_sum, model, is_ollama)
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": "Write the termination block now."},
    ]
    return await _llm_call(client, model, messages, temperature, 600, is_ollama, has_image=False)


def _parse_five_whys_summary(raw: str) -> dict:
    text = raw.replace("[ROOT_CAUSE_REACHED]", "").strip()
    summary = {
        "method": "5whys",
        "confirmed_concern": "",
        "why_chain": [],
        "root_cause": "",
        "design_implication": "",
        "total_chains": 1,
        "total_steps": 0,
        "stopping_reason": "",
        # Backward-compat keys used by pipeline summary display
        "specific_concern": "",
        "confirmed_attribute": "",
        "chains": [],
        "original_response": "",
        "vague_seed": "",
        "trigger": "",
    }
    m = _re.search(r'Confirmed concern:\s*(.+?)(?=\n\n5-WHYS|\nRoot cause|\nTotal|\Z)', text, _re.DOTALL)
    if m:
        summary["confirmed_concern"] = m.group(1).strip()
        summary["specific_concern"] = summary["confirmed_concern"]
        summary["confirmed_attribute"] = summary["confirmed_concern"]
    for wm in _re.finditer(
        r'WHY\s+(\d+):\nQ:\s*(.+?)\nA:\s*(.+?)(?=\nWHY\s+\d+|\nRoot cause|\Z)',
        text, _re.DOTALL
    ):
        summary["why_chain"].append({
            "why_num": int(wm.group(1)),
            "question": wm.group(2).strip(),
            "answer": wm.group(3).strip(),
        })

    m = _re.search(r'Root cause:\s*["“]?(.+?)["”]?\s*(?:\n|$)', text)
    if m:
        summary["root_cause"] = m.group(1).strip()

    m = _re.search(r'Design implication:\s*(.+?)(?:\n|$)', text)
    if m:
        summary["design_implication"] = m.group(1).strip()

    m = _re.search(r'Total why steps:\s*(\d+)', text)
    if m:
        summary["total_steps"] = int(m.group(1))

    m = _re.search(r'Stopping reason:\s*(.+?)(?:\n|$)', text)
    if m:
        summary["stopping_reason"] = m.group(1).strip()
    if summary["why_chain"]:
        steps = [{"ladder": e["why_num"], "type": "W", "text": e["answer"]}
                 for e in summary["why_chain"]]
        summary["chains"] = [{"steps": steps, "endpoint_type": "root cause"}]

    return summary


def _format_five_whys_display(s: dict) -> str:
    lines = [
        f'Confirmed concern: {s.get("confirmed_concern", "")}',
        "",
    ]
    for entry in s.get("why_chain", []):
        lines.append(f"  Why {entry['why_num']}: {entry['question']}")
        lines.append(f"  → {entry['answer']}")
        lines.append("")
    lines += [
        f'Root cause: {s.get("root_cause", "")}',
        f'Design implication: {s.get("design_implication", "")}',
        "",
        "Summary:",
        f'  * Total why steps: {s["total_steps"]}',
        f'  * Stopping reason: {s["stopping_reason"]}',
        "",
        "Interview complete.",
    ]
    return "\n".join(lines)

def _build_jtbd_questioner_system(
    interview_type: InterviewType,
    product_label: str,
    confirmed_concern: str,
    jtbd_state: "JTBDState",
    judge_feedback: Optional["JudgeFeedback"] = None,
    shadow_mode: bool = True,
) -> str:
    phase_notes = {
        InterviewType.WIREFRAME: (
            "This is a STATIC wireframe prototype — the participant LOOKED at it, they never "
            "tapped, clicked, navigated, or completed any action. Every question must be framed "
            "from the perspective of REVIEWING a layout, not using a live app. "
            "BANNED: 'tap', 'click', 'scroll', 'proceed', 'move forward', 'complete', "
            "'navigate to', 'before deciding', 'whether to proceed', 'use the app', 'go through'. "
            "Reference visible layout only: placement, labelling, groupings, visual hierarchy."
        ),
    }
    target_level = jtbd_state.next_expected_level or "S"
    probe_instr = JTBD_PROBE_INSTRUCTIONS.get(target_level, JTBD_PROBE_INSTRUCTIONS["S"])
    if jtbd_state.consecutive_unclear_count > 0:
        probe_instr += (
            f"\n\nRETRY (attempt {jtbd_state.consecutive_unclear_count + 1}) — "
            f"the last question at [{target_level}] got an unclear answer. "
            "Try a COMPLETELY DIFFERENT angle: if you asked about context, ask about "
            "a specific visible element; if you asked abstractly, ask concretely. "
            "Do not rephrase any banned question."
        )
    aq = jtbd_state.asked_questions
    aq_block = "\n".join(f"  - {q}" for q in aq) if aq else "  (none yet)"
    judge_injection = ""
    if judge_feedback and not shadow_mode:
        judge_injection = (
            f"\n\nMANDATORY JUDGE OVERRIDE — you MUST follow this:\n"
            f"TACTIC: {judge_feedback.suggested_tactic}\n"
            f"Your next question MUST implement this tactic. Do NOT ignore it.\n"
        )
        if judge_feedback.prohibited_patterns:
            judge_injection += (
                "BANNED question patterns (using any of these is a failure): "
                + ", ".join(judge_feedback.prohibited_patterns)
                + "\n"
            )
    return JTBD_QUESTIONER_SYSTEM.format(
        interview_phase_label=interview_type.value,
        product_label=product_label,
        confirmed_concern=confirmed_concern,
        chain_summary=jtbd_state.chain_summary(),
        target_level=target_level,
        phase_probe_instruction=probe_instr,
        asked_questions_block=aq_block,
        phase_questioner_note=phase_notes[interview_type],
        judge_injection=judge_injection,
    )


def _build_jtbd_chain_context(jtbd_state: "JTBDState") -> str:
    confirmed = jtbd_state.confirmed_levels
    if not confirmed:
        return "CHAIN STATUS: Empty — no levels confirmed yet."
    lines = ["CHAIN STATUS (already confirmed):"]
    for e in jtbd_state.extractions:
        if e.level != "UNCLEAR":
            lines.append(f"  [{e.level}] {e.extract[:80]}")
    next_level = jtbd_state.next_expected_level
    if next_level:
        lines.append(f"\nNEXT TARGET: [{next_level}]")
    else:
        lines.append("\nAll levels confirmed.")
    return "\n".join(lines)


async def extract_jtbd_response(
    client,
    model: str,
    persona_answer: str,
    jtbd_state: "JTBDState",
    target_level: str,
    preceding_question: Optional[str] = None,
    temperature: float = 0.1,
    is_ollama: bool = False,
) -> Tuple[str, str, str]:
    chain_context = _build_jtbd_chain_context(jtbd_state)
    level_def = _JTBD_LEVEL_DEFS.get(target_level, "")
    base_system = JTBD_EXTRACTOR_SYSTEM.format(
        chain_context=chain_context,
        target_level=target_level,
        target_label=f"[{target_level}]",
        target_definition=level_def,
    )
    system = _prepend_no_think(base_system, model, is_ollama)
    user_content = f'Participant response:\n"{persona_answer}"'
    if preceding_question:
        user_content = (
            f'Interviewer question:\n"{preceding_question}"\n\n'
            f'Participant response:\n"{persona_answer}"'
        )
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": user_content},
    ]
    raw = await _llm_call(client, model, messages, temperature, 200, is_ollama, has_image=False)
    level, extract, reasoning = _parse_extraction(raw)
    if level not in (target_level, "UNCLEAR"):
        reasoning = f"[LEVEL-DRIFT: model returned [{level}] but target was [{target_level}]] {reasoning}"
        level = "UNCLEAR"
    return level, extract, reasoning


async def generate_jtbd_question(
    client,
    model: str,
    memory: "DecayingMemoryBuffer",
    jtbd_state: "JTBDState",
    confirmed_concern: str,
    interview_type: InterviewType = InterviewType.WIREFRAME,
    product_label: str = "Wireframe UI",
    wireframe_images: list = None,
    temperature: float = 0.4,
    is_ollama: bool = False,
    ladder_depth: int = 0,
    judge_feedback: Optional["JudgeFeedback"] = None,
    shadow_mode: bool = True,
) -> str:
    raw_system = _build_jtbd_questioner_system(
        interview_type=interview_type,
        product_label=product_label,
        confirmed_concern=confirmed_concern,
        jtbd_state=jtbd_state,
        judge_feedback=judge_feedback,
        shadow_mode=shadow_mode,
    )
    system = _prepend_no_think(raw_system, model, is_ollama)
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": "Generate the next interview question now. One question only. No preamble."},
    ]
    question = await _llm_call(client, model, messages, temperature, 120, is_ollama, has_image=False)
    question = question.strip()
    if not question:
        raise RuntimeError(
            f"[generate_jtbd_question] Model '{model}' returned empty output after retry."
        )
    return question


async def generate_jtbd_summary(
    client,
    model: str,
    jtbd_state: "JTBDState",
    confirmed_concern: str,
    stopping_reason: str,
    product_description: str = "",
    prior_response: str = "",
    vague_seed: str = "",
    conversation_context: str = "",
    temperature: float = 0.2,
    is_ollama: bool = False,
) -> str:
    chain_steps = jtbd_state.termination_chain_steps()
    total_turns = len([e for e in jtbd_state.extractions if e.level != "UNCLEAR"])
    situation = jtbd_state.get_best_for_level("S") or "(not identified)"
    job = jtbd_state.get_best_for_level("J") or "(not identified)"
    outcome = jtbd_state.get_best_for_level("O") or "(not identified)"
    barrier = jtbd_state.get_best_for_level("B") or "(not identified)"
    raw_sum = JTBD_SUMMARISER_SYSTEM.format(
        product_description=product_description,
        confirmed_concern=confirmed_concern,
        chain_steps=chain_steps,
        conversation_context=conversation_context or "(not available)",
        situation=situation,
        job=job,
        outcome=outcome,
        barrier=barrier,
        total_turns=total_turns,
        stopping_reason=stopping_reason,
    )
    system = _prepend_no_think(raw_sum, model, is_ollama)
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": "Write the termination block now."},
    ]
    return await _llm_call(client, model, messages, temperature, 600, is_ollama, has_image=False)


def _parse_jtbd_summary(raw: str) -> dict:
    text = raw.replace("[JOB_STORY_COMPLETE]", "").strip()
    summary = {
        "method": "jtbd",
        "confirmed_concern": "",
        "situation": "",
        "job": "",
        "desired_outcome": "",
        "barrier": "",
        "job_story": "",
        "design_implication": "",
        "total_chains": 1,
        "total_steps": 0,
        "stopping_reason": "",
        # Backward-compat keys used by pipeline summary display
        "specific_concern": "",
        "confirmed_attribute": "",
        "chains": [],
        "original_response": "",
        "vague_seed": "",
        "trigger": "",
    }
    m = _re.search(r'Confirmed concern:\s*(.+?)(?=\n\n|\nSITUATION|\Z)', text, _re.DOTALL)
    if m:
        summary["confirmed_concern"] = m.group(1).strip()
        summary["specific_concern"] = summary["confirmed_concern"]
        summary["confirmed_attribute"] = summary["confirmed_concern"]
    m = _re.search(r'SITUATION:\s*(.+?)(?=\nJOB:|\Z)', text, _re.DOTALL)
    if m:
        summary["situation"] = m.group(1).strip()
    m = _re.search(r'JOB:\s*(.+?)(?=\nDESIRED OUTCOME:|\Z)', text, _re.DOTALL)
    if m:
        summary["job"] = m.group(1).strip()
    m = _re.search(r'DESIRED OUTCOME:\s*(.+?)(?=\nBARRIER|\Z)', text, _re.DOTALL)
    if m:
        summary["desired_outcome"] = m.group(1).strip()
    m = _re.search(r'BARRIER(?:\s*\(inferred\))?:\s*(.+?)(?=\nJOB STORY:|\Z)', text, _re.DOTALL)
    if m:
        summary["barrier"] = m.group(1).strip()
    m = _re.search(r'JOB STORY:\s*(.+?)(?=\nDesign implication:|\Z)', text, _re.DOTALL)
    if m:
        summary["job_story"] = m.group(1).strip()
    m = _re.search(r'Design implication:\s*(.+?)(?=\nTotal turns:|\Z)', text, _re.DOTALL)
    if m:
        summary["design_implication"] = m.group(1).strip()
    m = _re.search(r'Total turns:\s*(\d+)', text)
    if m:
        summary["total_steps"] = int(m.group(1))
    m = _re.search(r'Stopping reason:\s*(.+?)(?:\n|$)', text)
    if m:
        summary["stopping_reason"] = m.group(1).strip()
    steps = []
    for level_tag, level_name in [("S", "situation"), ("J", "job"), ("O", "desired_outcome"), ("B", "barrier")]:
        val = summary.get(level_name, "")
        if val:
            steps.append({"ladder": len(steps) + 1, "type": level_tag, "text": val})
    if steps:
        summary["chains"] = [{"steps": steps, "endpoint_type": "job story"}]
    return summary


def _format_jtbd_display(s: dict) -> str:
    lines = [
        f'Confirmed concern: {s.get("confirmed_concern", "")}',
        "",
        f'  [S] Situation:      {s.get("situation", "")}',
        f'  [J] Job:            {s.get("job", "")}',
        f'  [O] Desired Outcome: {s.get("desired_outcome", "")}',
        f'  [B] Barrier:        {s.get("barrier", "")}',
        "",
        f'Job Story: {s.get("job_story", "")}',
        "",
        f'Design implication: {s.get("design_implication", "")}',
        "",
        "Summary:",
        f'  * Total turns: {s["total_steps"]}',
        f'  * Stopping reason: {s["stopping_reason"]}',
        "",
        "Interview complete.",
    ]
    return "\n".join(lines)

async def clarification_turn(
    client,
    model: str,
    memory: DecayingMemoryBuffer,
    depth: int,
    seed_topic: str,
    interview_type: InterviewType = InterviewType.WIREFRAME,
    product_label: str = "Wireframe UI",
    prior_response: str = "",
    vague_seed: str = "",
    image_b64: str = "",
    image_media_type: str = "image/png",
    clarification_attempts: int = 0,
    temperature: float = 0.3,
    is_ollama: bool = False,
) -> str:
    chain = memory.summary()

    effective_prior = prior_response if prior_response else seed_topic
    effective_seed  = vague_seed if vague_seed else effective_prior[:80]

    raw_clsys = _build_clarification_system(
        interview_type=interview_type,
        product_label=product_label,
        prior_response=effective_prior,
        vague_seed=effective_seed,
        chain=chain if chain else "(interview just started)",
    )
    system = _prepend_no_think(raw_clsys, model, is_ollama)

    def _make_user_msg(text: str):
        if interview_type == InterviewType.WIREFRAME and image_b64:
            img = _build_image_content(image_b64, image_media_type, text, is_ollama=is_ollama)
            return {"role": "user", "content": img}
        return {"role": "user", "content": text}
    if clarification_attempts == 0:
        base_text = (
            "Generate the clarification question now. "
            "Quote the prior response verbatim and name the vague seed exactly."
        )
        user_msg = _make_user_msg(base_text)
    else:
        last = memory.entries[-1].content if memory.entries else ""
        follow_text = (
            f"Participant responded: \"{last}\"\n\n"
            "If they selected or clearly implied an option — including a bare letter like "
            "'B' or 'C' on its own — ACCEPT IT immediately. Do not re-ask. "
            "Only re-ask if the response contains no letter and is genuinely ambiguous. "
            "No affirmations."
        )
        user_msg = _make_user_msg(follow_text)
    messages = [{"role": "system", "content": system}, user_msg]
    _has_img = interview_type == InterviewType.WIREFRAME and bool(image_b64)
    result = await _llm_call(client, model, messages, temperature, 400, is_ollama, has_image=_has_img)
    if not result:
        raise RuntimeError(
            f"[clarification_turn] Model '{model}' returned empty output after retry.\n"
            "No hardcoded MCQ — fix the model connection and re-run.\n"
            "Check: (1) ollama serve is running, (2) model is pulled and supports vision,\n"
            f"  ollama pull {model}"
        )
    return result

def _is_qwen36_model(model_name: str) -> bool:
    name = model_name.lower()
    return "qwen3.6" in name or "qwen3_6" in name

def _is_qwen3_classic_model(model_name: str) -> bool:
    if _is_qwen36_model(model_name):
        return False
    name = model_name.lower()
    return any(x in name for x in ["qwen3:", "qwen3-", "qwen3.5", "qwen3/"])


def _is_qwen3_model(model_name: str) -> bool:
    name = model_name.lower()
    return any(x in name for x in ["qwen3", "qwen3.5", "qwen3.6", "qwen3-"])


def _prepend_no_think(system: str, model: str, is_ollama: bool) -> str:
    if not is_ollama:
        return system
    if _is_qwen36_model(model):
        return system
    if _is_qwen3_classic_model(model):
        return "/no_think\n\n" + system
    return system

def human_turn(question: str) -> str:
    import sys as _sys
    _sys.stdout.flush()
    _sys.stderr.flush()
    while True:
        try:
            raw = input("\n  ▶ You > ").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit(0)
        if raw:
            break
        print("  (Please type a response and press Enter.)")
    print()
    return raw

def _parse_interview_summary(raw: str) -> dict:
    text = raw.replace("[ROOT_CAUSE_REACHED]", "").strip()
    summary = {
        "original_response": "",  #prior_response verbatim
        "vague_seed": "",         #researcher-identified vague phrase
        "confirmed_attribute": "", #what clarification resolved to
        "trigger": "",            #kept for backward compat
        "specific_concern": "",
        "chains": [],
        "total_chains": 0,
        "total_steps": 0,
        "stopping_reason": "",
    }
    m = _re.search(r'Original response:\s*["\u201c\u201d]?(.+?)["\u201c\u201d]?\s*(?:\n|$)', text)
    if m:
        summary["original_response"] = m.group(1).strip()
        summary["trigger"] = summary["original_response"]  # backward compat
    m = _re.search(r'Vague seed:\s*["\u201c\u201d]?(.+?)["\u201c\u201d]?\s*(?:\n|$)', text)
    if m:
        summary["vague_seed"] = m.group(1).strip()
    m = _re.search(r'Confirmed attribute:\s*(.+?)(?=\n\nCHAIN|\nTotal|\Z)', text, _re.DOTALL)
    if m:
        summary["confirmed_attribute"] = m.group(1).strip()
        summary["specific_concern"] = summary["confirmed_attribute"]  # backward compat
    for chain_block in _re.split(r'CHAIN\s+\d+[^\n]*\n', text)[1:]:
        steps = []
        for sm in _re.finditer(
            r'->\s*\[Ladder\s*(\d+)\]\s*\[([ACV])\]\s*(.+?)(?=\s*->|\s*\n\nEndpoint|\s*\nEndpoint|\Z)',
            chain_block, _re.DOTALL
        ):
            steps.append({
                "ladder": int(sm.group(1)),
                "type": sm.group(2),
                "text": sm.group(3).strip(),
            })
        em = _re.search(r'Endpoint type:\s*(.+?)(?:\n|$)', chain_block)
        if steps:
            summary["chains"].append({
                "steps": steps,
                "endpoint_type": em.group(1).strip() if em else "",
            })
    m = _re.search(r'Total chains:\s*(\d+)', text)
    if m:
        summary["total_chains"] = int(m.group(1))
    m = _re.search(r'Total ladder steps:\s*(\d+)', text)
    if m:
        summary["total_steps"] = int(m.group(1))
    m = _re.search(r'Stopping reason:\s*(.+?)(?:\n|$)', text)
    if m:
        summary["stopping_reason"] = m.group(1).strip()
    return summary


def _format_summary_display(s: dict) -> str:
    lines = [
        f'Original response: "{s.get("original_response", s.get("trigger", ""))}"',
        f'Vague seed: "{s.get("vague_seed", "")}"',
        f'Confirmed attribute: {s.get("confirmed_attribute", s.get("specific_concern", ""))}',
        "",
    ]
    for i, chain in enumerate(s["chains"], 1):
        arrow_chain = " \u2192 ".join(
            f'[Ladder {st["ladder"]}] [{st["type"]}] {st["text"]}'
            for st in chain["steps"]
        )
        lines += [
            f"CHAIN {i}:",
            f"  {arrow_chain}",
            f'  Endpoint type: {chain["endpoint_type"]}',
            "",
        ]
    lines += [
        "Summary:",
        f'  * Total chains: {s["total_chains"]}',
        f'  * Total ladder steps: {s["total_steps"]}',
        f'  * Stopping reason: {s["stopping_reason"]}',
        "",
        "Interview complete.",
    ]
    return "\n".join(lines)

@dataclass
class InterviewSession:
    persona_name: str
    seed_topic: str
    prior_response: str = ""
    vague_seed: str = ""
    interview_type: str = "wireframe"
    product_label: str = "Wireframe UI"
    image_path: str = ""
    product_description: str = ""
    laddering_method: str = "acv"
    turns: List[dict] = field(default_factory=list)
    drift_events: List[dict] = field(default_factory=list)
    final_depth: int = 0
    terminated_naturally: bool = False
    interview_summary: dict = field(default_factory=dict)
    judge_log: Optional["JudgeLog"] = None
    judge_report: Optional[dict] = None

async def run_interview(
    client,
    model: str,
    interview_type: InterviewType,
    product_label: str,
    prior_response: str,
    vague_seed: str,
    image_b64: str = "",
    image_media_type: str = "image/png",
    wireframe_images: list = None,
    product_description: str = "",
    image_path: str = "",
    is_ollama: bool = False,
    max_depth: int = 100,
    min_depth: int = 3,
    temperature_interviewer: float = 0.3,
    skip_judge: bool = False,
    shadow_mode: bool = True,
    judge_model: str = "",
    judge_client=None,
    laddering_method: "LadderingMethod" = None,
    interviewer_vision: bool = True,
) -> InterviewSession:
    if laddering_method is None:
        laddering_method = LadderingMethod.ACV
    _iw_image_b64        = image_b64        if interviewer_vision else ""
    _iw_wireframe_images = wireframe_images if interviewer_vision else []
    vague_seed = vague_seed.strip().strip('"').strip("'")
    memory = DecayingMemoryBuffer()
    chain_state = ChainState()
    five_whys_state = FiveWhysState()
    jtbd_state = JTBDState()
    judge_log = JudgeLog()
    judge_feedback = None
    session = InterviewSession(
        persona_name="Human",
        seed_topic=prior_response,
        prior_response=prior_response,
        vague_seed=vague_seed,
        interview_type=interview_type.value,
        product_label=product_label,
        image_path=image_path,
        product_description=product_description,
        laddering_method=laddering_method.value,
    )
    clarification_done = False
    confirmed_concern = ""
    clarification_attempts = 0
    ladder_depth = 0
    phase_labels = {
        InterviewType.WIREFRAME: "WIREFRAME REVIEW",
    }
    method_labels = {
        LadderingMethod.ACV:       "ACV (Attribute → Consequence → Value)",
        LadderingMethod.FIVE_WHYS: "5-Whys (sequential causal chain)",
        LadderingMethod.JTBD:      "JTBD (Job Story Ladder: Situation → Job → Outcome → Barrier)",
    }
    print(f"\n{'═'*60}")
    print(f"  INTERVIEW START")
    print(f"  Phase:  {phase_labels[interview_type]}")
    print(f"  Method: {method_labels[laddering_method]}")
    print(f"  Product: {product_label}")
    if image_path:
        print(f"  Image: {image_path}")
    print(f"  Prior response: {prior_response[:80]}{'…' if len(prior_response) > 80 else ''}")
    print(f"  Vague seed: {vague_seed}")
    print(f"{'═'*60}")
    memory.add(-1, "interviewer",
        f"We've just shown you: {product_label}. What are your initial thoughts?")
    memory.add(-1, "persona", prior_response)
    depth = 0
    while True:
        if depth > 0 and depth % max_depth == 0:
            print(f"\n SOFT CEILING WARNING: {depth} turns completed without "
                  f"chain gate firing. Chain state: {chain_state.chain_summary()}")
            print(f" Continuing — interview runs until valid V is confirmed.")
        if not clarification_done:
            output = await clarification_turn(
                client, model, memory, depth,
                seed_topic=prior_response,
                interview_type=interview_type,
                product_label=product_label,
                prior_response=prior_response,
                vague_seed=vague_seed,
                image_b64=_iw_image_b64,
                image_media_type=image_media_type,
                clarification_attempts=clarification_attempts,
                temperature=temperature_interviewer,
                is_ollama=is_ollama,
            )
            print(f"\n  [CLARIFY Q{depth+1}]\n  {output}")
            memory.add(depth, "interviewer", output)
            answer = human_turn(output)
            memory.add(depth, "persona", answer)
            session.turns.append({
                "turn": depth + 1,
                "question": output,
                "answer": answer,
                "drift_active": False,
                "is_summary": False,
            })
            choice = _extract_choice(answer)
            if choice:
                if choice == "D":
                    raw_d = _re.sub(
                        r"^(?:i'?ll?\s+go\s+with\s+[Dd][\.,]?\s*|[Dd][\.)\-:]\s*|"
                        r"option\s+[Dd][\.,]?\s*|so\s+[Dd][\.,]?\s*)",
                        "", answer, flags=_re.IGNORECASE
                    ).strip()
                    confirmed_concern = raw_d[:200] if raw_d else answer[:200]
                else:
                    opt_match = _re.search(
                        rf'{choice}\)\s*(.+?)(?:\n|$)', output, _re.IGNORECASE
                    )
                    confirmed_concern = opt_match.group(1).strip() if opt_match else answer[:120]
                clarification_done = True
                print(f"\n  → Clarification resolved: option {choice} — \"{confirmed_concern[:80]}\"")
            else:
                clarification_attempts += 1
                if clarification_attempts >= 2:
                    confirmed_concern = answer[:120]
                    print(f"\n  → Clarification inferred after {clarification_attempts} attempts")
                    clarification_done = True
            continue
        if laddering_method == LadderingMethod.FIVE_WHYS:
            last_persona_answer = memory.entries[-1].content if memory.entries else ""
            if not five_whys_state.current_problem:
                five_whys_state.current_problem = confirmed_concern
                print(f"\n  [5-WHYS] Starting chain. Problem: \"{confirmed_concern[:80]}\"")
            else:
                level, extract, reasoning = await extract_five_whys_response(
                    client, model, last_persona_answer,
                    current_depth=five_whys_state.depth,
                    five_whys_state=five_whys_state,
                    temperature=0.1,
                    is_ollama=is_ollama,
                )
                if not extract:
                    extract = last_persona_answer[:120]
                last_q = five_whys_state.asked_questions[-1] if five_whys_state.asked_questions else ""
                five_whys_state.why_chain.append({
                    "why_num": five_whys_state.depth,
                    "question": last_q,
                    "answer": extract,
                    "level": level,
                })
                five_whys_state.why_chain[-1]["why_num"] = len(five_whys_state.why_chain)
                five_whys_state.current_problem = extract
                if level == "ROOT_CAUSE":
                    five_whys_state.root_cause_found = True
                    five_whys_state.non_prescriptive_streak = 0
                else:
                    if five_whys_state.depth >= 2 and five_whys_state._is_circular():
                        five_whys_state.non_prescriptive_streak += 1
                    else:
                        five_whys_state.non_prescriptive_streak = 0
                print(f"\n  [5-WHYS EXTRACTOR] level={level} | {extract[:80]}")
                print(f"                     reason: {reasoning}")
            _circular = five_whys_state._is_circular() if five_whys_state.depth >= 2 else False
            print(f"  [5-WHYS GATE] can_terminate={five_whys_state.can_terminate} "
                  f"| depth={five_whys_state.depth} (min={five_whys_state.MIN_DEPTH}) "
                  f"| root_cause={five_whys_state.root_cause_found} "
                  f"| circular={_circular} "
                  f"| non_prescriptive_streak={five_whys_state.non_prescriptive_streak}"
                  f"/{five_whys_state.MAX_NON_PRESCRIPTIVE_STREAK}")
            _forced_endpoint = (
                not five_whys_state.root_cause_found
                and five_whys_state.non_prescriptive_streak >= five_whys_state.MAX_NON_PRESCRIPTIVE_STREAK
            )
            if five_whys_state.can_terminate:
                if five_whys_state.root_cause_found:
                    stopping_reason = "root-cause-identified"
                elif _forced_endpoint:
                    stopping_reason = f"forced-endpoint-non-prescriptive (depth {five_whys_state.depth})"
                else:
                    stopping_reason = f"organic-termination (depth {five_whys_state.depth})"
                print(f"\n  5-WHYS GATE PASSED — generating termination summary")
                termination_block = await generate_five_whys_summary(
                    client, model, five_whys_state, confirmed_concern,
                    stopping_reason,
                    product_description=product_label,
                    temperature=0.2,
                    is_ollama=is_ollama,
                    force_inferred_implication=_forced_endpoint,
                )
                output = termination_block.replace("INTERVIEW_COMPLETE", "[ROOT_CAUSE_REACHED]", 1)
                structured = _parse_five_whys_summary(output)
                structured["stopping_reason"] = stopping_reason
                session.interview_summary = structured
                session.terminated_naturally = ("root-cause" in stopping_reason)
                session.final_depth = depth + 1
                print(f"\n{_format_five_whys_display(structured)}")
                if not skip_judge and judge_model and judge_log.scores:
                    print(f"  [JUDGE] Generating post-session report...")
                    session.judge_report = await generate_judge_report(
                        judge_log=judge_log,
                        chain_state=chain_state,
                        actual_turns=depth + 1,
                        min_depth=five_whys_state.MIN_DEPTH,
                        is_ollama=is_ollama,
                        judge_model=judge_model,
                        judge_client=judge_client,
                    )
                    print(f"  [JUDGE] Report generated — efficiency: "
                          f"{session.judge_report.get('laddering_efficiency', 'N/A')}")
                break

            judge_feedback = None
            if not skip_judge and judge_model and five_whys_state.asked_questions:
                _prev_probe = five_whys_state.asked_questions[-1]
                judge_feedback = await judge_turn(
                    probe_text=_prev_probe,
                    persona_answer=last_persona_answer,
                    chain_state=chain_state,
                    vague_seed=vague_seed,
                    prior_response=prior_response,
                    judge_log=judge_log,
                    is_ollama=is_ollama,
                    judge_model=judge_model,
                    judge_client=judge_client,
                    laddering_method=LadderingMethod.FIVE_WHYS,
                    method_state=five_whys_state,
                )
                judge_log.scores.append(judge_feedback)
                judge_log.tactic_history.append(judge_feedback.suggested_tactic)
                if (len(judge_log.tactic_history) >= 3
                        and len(set(judge_log.tactic_history[-3:])) == 1
                        and not judge_log.escalation_triggered):
                    judge_log.escalation_triggered = True
                    judge_log.escalation_at_turn = judge_feedback.turn
                    judge_feedback.suggested_tactic = (
                        "Fundamental probe restructure needed — switch probe type entirely"
                    )
            question = await generate_five_whys_question(
                client, model, five_whys_state,
                confirmed_concern=confirmed_concern,
                interview_type=interview_type,
                product_label=product_label,
                temperature=temperature_interviewer,
                is_ollama=is_ollama,
                judge_feedback=judge_feedback,
                shadow_mode=shadow_mode,
            )
            five_whys_state.asked_questions.append(question)
            print(f"\n  [WHY Q{five_whys_state.depth + 1}]\n  {question}")
            memory.add(depth, "interviewer", question)

            answer = human_turn(question)
            memory.add(depth, "persona", answer)
            session.turns.append({
                "turn": depth + 1,
                "question": question,
                "answer": answer,
                "drift_active": False,
                "is_summary": False,
                "why_depth": five_whys_state.depth + 1,
            })
            depth += 1
            continue
        if laddering_method == LadderingMethod.JTBD:
            last_persona_answer = memory.entries[-1].content if memory.entries else ""
            _jtbd_target_level = jtbd_state.next_expected_level or "S"
            _jtbd_extracted = "none"
            if not jtbd_state.extractions and not jtbd_state.asked_questions:
                print(f"\n  [JTBD] Starting Job Story chain. Concern: \"{confirmed_concern[:80]}\"")
                print(f"  [JTBD TARGET] [{_jtbd_target_level}] — first probe")
            else:
                preceding_q = None
                if len(memory.entries) >= 2 and memory.entries[-2].role == "interviewer":
                    preceding_q = memory.entries[-2].content
                if jtbd_state.consecutive_unclear_count == 0:
                    print(f"\n  [JTBD TARGET] [{_jtbd_target_level}]")
                else:
                    _attempt_num = jtbd_state.consecutive_unclear_count + 1
                    print(f"\n  [JTBD TARGET] [{_jtbd_target_level}] retry {_attempt_num}/{jtbd_state.MAX_CONSECUTIVE_UNCLEAR}")
                level, extract, reasoning = await extract_jtbd_response(
                    client, model, last_persona_answer, jtbd_state,
                    target_level=_jtbd_target_level,
                    preceding_question=preceding_q,
                    temperature=0.1,
                    is_ollama=is_ollama,
                )
                if not extract:
                    extract = last_persona_answer[:120]
                print(f"  [JTBD EXTRACT] target=[{_jtbd_target_level}] result=[{level}] | {extract[:80]}")
                if reasoning:
                    print(f"                 reason: {reasoning[:120]}")
                if level == _jtbd_target_level:
                    jtbd_state.extractions.append(JTBDExtraction(
                        ladder_num=jtbd_state.next_ladder_num,
                        level=level,
                        extract=extract,
                        reasoning=reasoning,
                        turn=depth + 1,
                    ))
                    jtbd_state.consecutive_unclear_count = 0
                    jtbd_state.unclear_answer_candidates = []
                    ladder_depth += 1
                    _jtbd_extracted = level
                    print(f"  [{level}] confirmed — chain: {' → '.join('[' + e.level + ']' for e in jtbd_state.extractions if e.level != 'UNCLEAR')}")
                else:
                    _jtbd_extracted = "UNCLEAR"
                    jtbd_state.unclear_answer_candidates.append(last_persona_answer)
                    jtbd_state.consecutive_unclear_count += 1
                    if jtbd_state.consecutive_unclear_count >= jtbd_state.MAX_CONSECUTIVE_UNCLEAR:
                        candidates = jtbd_state.unclear_answer_candidates or [last_persona_answer]
                        best_answer = max(candidates, key=lambda x: len(x.strip()))
                        inferred_extract = f"[inferred]: {best_answer[:150].strip()}"
                        jtbd_state.extractions.append(JTBDExtraction(
                            ladder_num=jtbd_state.next_ladder_num,
                            level=_jtbd_target_level,
                            extract=inferred_extract,
                            reasoning=f"[AUTO-PROMOTED after {jtbd_state.consecutive_unclear_count} UNCLEAR]",
                            turn=depth + 1,
                        ))
                        jtbd_state.consecutive_unclear_count = 0
                        jtbd_state.unclear_answer_candidates = []
                        ladder_depth += 1
                        _jtbd_extracted = f"{_jtbd_target_level}[inferred]"
                        print(f" AUTO-PROMOTE [{_jtbd_target_level}] — {jtbd_state.MAX_CONSECUTIVE_UNCLEAR} consecutive UNCLEAR, using best of {len(candidates)} candidates")
                    else:
                        print(f" UNCLEAR ({jtbd_state.consecutive_unclear_count}/{jtbd_state.MAX_CONSECUTIVE_UNCLEAR}) — rephrasing [{_jtbd_target_level}] probe")
            can_terminate, gate_reason = jtbd_state.ready_to_terminate(min_depth)
            print(f"  [JTBD GATE] can_terminate={can_terminate} | {gate_reason}")
            print(f"  [JTBD STATE] {jtbd_state.chain_summary()}")
            if can_terminate:
                stopping_reason = gate_reason
                if "chain-stall-abort" in gate_reason:
                    print(f"\n  JTBD STALL ABORT — interview terminated with no confirmed chain steps")
                    session.interview_summary = {
                        "confirmed_concern": confirmed_concern,
                        "situation": "(not extracted — stall abort)",
                        "job": "(not extracted — stall abort)",
                        "outcome": "(not extracted — stall abort)",
                        "barrier": "(not extracted — stall abort)",
                        "job_story": "(stall abort — extractor could not classify responses)",
                        "design_implication": "(no data — review raw transcript)",
                        "total_turns": depth + 1,
                        "stopping_reason": stopping_reason,
                    }
                    session.terminated_naturally = False
                    session.final_depth = depth + 1
                    break
                print(f"\n  JTBD GATE PASSED — generating termination summary")
                _conv_lines = []
                for _e in memory.entries:
                    _role_label = "Q" if _e.role == "interviewer" else "A"
                    _conv_lines.append(f"[{_role_label}] {_e.content[:200]}")
                _conv_context = "\n".join(_conv_lines[-20:])
                termination_block = await generate_jtbd_summary(
                    client, model, jtbd_state, confirmed_concern,
                    stopping_reason,
                    product_description=product_label,
                    prior_response=prior_response,
                    vague_seed=vague_seed,
                    conversation_context=_conv_context,
                    temperature=0.2,
                    is_ollama=is_ollama,
                )
                output = termination_block.replace("INTERVIEW_COMPLETE", "[JOB_STORY_COMPLETE]", 1)
                structured = _parse_jtbd_summary(output)
                session.interview_summary = structured
                session.terminated_naturally = True
                session.final_depth = depth + 1
                print(f"\n{_format_jtbd_display(structured)}")
                if not skip_judge and judge_model and judge_log.scores:
                    print(f"  [JUDGE] Generating post-session report...")
                    session.judge_report = await generate_judge_report(
                        judge_log=judge_log,
                        chain_state=chain_state,
                        actual_turns=depth + 1,
                        min_depth=min_depth,
                        is_ollama=is_ollama,
                        judge_model=judge_model,
                        judge_client=judge_client,
                    )
                    print(f"  [JUDGE] Report generated — efficiency: "
                          f"{session.judge_report.get('laddering_efficiency', 'N/A')}")
                break

            judge_feedback = None
            if not skip_judge and judge_model and jtbd_state.asked_questions:
                _prev_probe = jtbd_state.asked_questions[-1]
                judge_feedback = await judge_turn(
                    probe_text=_prev_probe,
                    persona_answer=last_persona_answer,
                    chain_state=chain_state,
                    vague_seed=vague_seed,
                    prior_response=prior_response,
                    judge_log=judge_log,
                    is_ollama=is_ollama,
                    judge_model=judge_model,
                    judge_client=judge_client,
                    laddering_method=LadderingMethod.JTBD,
                    method_state=jtbd_state,
                )
                judge_log.scores.append(judge_feedback)
                judge_log.tactic_history.append(judge_feedback.suggested_tactic)
                if (len(judge_log.tactic_history) >= 3
                        and len(set(judge_log.tactic_history[-3:])) == 1
                        and not judge_log.escalation_triggered):
                    judge_log.escalation_triggered = True
                    judge_log.escalation_at_turn = judge_feedback.turn
                    judge_feedback.suggested_tactic = (
                        "Fundamental probe restructure needed — switch probe type entirely"
                    )
            _question_target = jtbd_state.next_expected_level or "S"
            question = await generate_jtbd_question(
                client, model, memory, jtbd_state,
                confirmed_concern=confirmed_concern,
                interview_type=interview_type,
                product_label=product_label,
                wireframe_images=_iw_wireframe_images,
                temperature=temperature_interviewer,
                is_ollama=is_ollama,
                ladder_depth=depth,
                judge_feedback=judge_feedback,
                shadow_mode=shadow_mode,
            )
            jtbd_state.asked_questions.append(question)
            print(f"\n  [JTBD Q{depth+1}]\n  {question}")
            memory.add(depth, "interviewer", question)

            answer = human_turn(question)
            memory.add(depth, "persona", answer)
            session.turns.append({
                "turn": depth + 1,
                "target_level": _question_target,
                "confirmed_level": _jtbd_extracted,
                "extract": (
                    jtbd_state.extractions[-1].extract[:120]
                    if jtbd_state.extractions
                    and _jtbd_extracted not in ("none", "UNCLEAR")
                    else ""
                ),
                "question": question,
                "answer": answer,
                "drift_active": False,
                "is_summary": False,
            })

            depth += 1
            continue

        last_persona_answer = memory.entries[-1].content if memory.entries else ""
        preceding_q = None
        if len(memory.entries) >= 2 and memory.entries[-2].role == "interviewer":
            preceding_q = memory.entries[-2].content
        level, extract, reasoning = await extract_from_response(
            client, model, last_persona_answer, chain_state,
            preceding_question=preceding_q,
            temperature=0.1,
            is_ollama=is_ollama,
        )
        print(f"\n  [EXTRACTOR] level={level} | {extract[:80]}")
        print(f"              reason: {reasoning}")
        topic_drifted = False
        if level != "UNCLEAR":
            if chain_state.has_V and level in ("C", "A"):
                print(f"  POST-V REGRESSION — [{level}] extracted after [V] confirmed.")
                print(f"  Discarding '{extract[:60]}' — chain gate will fire next iteration.")
                level = "UNCLEAR"
            elif chain_state.is_topic_drift(level, extract):
                topic_drifted = True
                print(f"  TOPIC DRIFT — persona introduced new [A]: \"{extract[:60]}\"")
                print(f"  Redirecting to original A: \"{chain_state.first_confirmed_A.extract[:60]}\"")
            else:
                chain_state.extractions.append(ChainExtraction(
                    ladder_num=chain_state.next_ladder_num,
                    level=level,
                    extract=extract,
                    reasoning=reasoning,
                    turn=depth + 1,
                ))
                ladder_depth += 1
        else:
            print(f"  Response classified UNCLEAR — rephrasing at same level")
        if chain_state.force_v_elicit:
            print(f"  V-ELICIT OVERRIDE — {chain_state.consecutive_c_count} consecutive [C] turns")
        if chain_state.use_absence_probe:
            print(f"  ABSENCE PROBE — anchor redirect failed {chain_state.c_cycling_redirect_count}x, "
                  f"switching to absence technique")
        elif chain_state.c_cycling_detected:
            best = chain_state.best_anchor_c
            print(f"  C-CYCLING (redirect #{chain_state.c_cycling_redirect_count + 1}) — "
                  f"{chain_state.total_c_count} total [C] | anchor: \"{best.extract[:50] if best else 'none'}\"")
            chain_state.c_cycling_redirect_count += 1
        can_terminate, gate_reason = chain_state.ready_to_terminate(min_depth)
        print(f"  [CHAIN GATE] can_terminate={can_terminate} | {gate_reason}")
        print(f"  [CHAIN STATE] {chain_state.chain_summary()}")

        if can_terminate:
            stopping_reason = gate_reason
            last_v = chain_state.last_v_index()
            if last_v < len(chain_state.extractions) - 1:
                trimmed = chain_state.extractions[last_v + 1:]
                chain_state.extractions = chain_state.extractions[:last_v + 1]
                print(f"  Trimmed {len(trimmed)} post-V step(s) before summary generation.")
            print(f"\n  CHAIN GATE PASSED — generating termination summary")
            termination_block = await generate_termination_summary(
                client, model, chain_state, confirmed_concern,
                stopping_reason,
                product_description=product_label,
                prior_response=prior_response,
                vague_seed=vague_seed,
                temperature=0.2,
                is_ollama=is_ollama,
            )
            output = termination_block.replace("INTERVIEW_COMPLETE", "[ROOT_CAUSE_REACHED]", 1)
            structured = _parse_interview_summary(output)
            session.interview_summary = structured
            session.terminated_naturally = True
            session.final_depth = depth + 1
            print(f"\n{_format_summary_display(structured)}")
            if not skip_judge and judge_model and judge_log.scores:
                print(f"  [JUDGE] Generating post-session report...")
                session.judge_report = await generate_judge_report(
                    judge_log=judge_log,
                    chain_state=chain_state,
                    actual_turns=depth + 1,
                    min_depth=min_depth,
                    is_ollama=is_ollama,
                    judge_model=judge_model,
                    judge_client=judge_client,
                )
                print(f"  [JUDGE] Report generated — efficiency: "
                      f"{session.judge_report.get('laddering_efficiency', 'N/A')}")
            break

        judge_feedback = None
        if not skip_judge and judge_model and len(chain_state.asked_questions) >= 1:
            _prev_probe = chain_state.asked_questions[-1]
            judge_feedback = await judge_turn(
                probe_text=_prev_probe,
                persona_answer=last_persona_answer,
                chain_state=chain_state,
                vague_seed=vague_seed,
                prior_response=prior_response,
                judge_log=judge_log,
                is_ollama=is_ollama,
                judge_model=judge_model,
                judge_client=judge_client,
            )
            judge_log.scores.append(judge_feedback)
            judge_log.tactic_history.append(judge_feedback.suggested_tactic)
            if (len(judge_log.tactic_history) >= 3
                    and len(set(judge_log.tactic_history[-3:])) == 1
                    and not judge_log.escalation_triggered):
                judge_log.escalation_triggered = True
                judge_log.escalation_at_turn = judge_feedback.turn
                judge_feedback.suggested_tactic = (
                    "Fundamental probe restructure needed — switch probe type "
                    "entirely (e.g., forced-choice instead of open, or anchor to "
                    "a single named element)"
                )
        question = await generate_question(
            client, model, memory, chain_state, confirmed_concern,
            interview_type=interview_type,
            product_label=product_label,
            image_b64=_iw_image_b64,
            image_media_type=image_media_type,
            wireframe_images=_iw_wireframe_images,
            topic_drifted=topic_drifted,
            temperature=temperature_interviewer,
            is_ollama=is_ollama,
            ladder_depth=depth,
            judge_feedback=judge_feedback,
            shadow_mode=shadow_mode,
        )
        chain_state.asked_questions.append(question)
        print(f"\n  [LADDER Q{depth+1}]\n  {question}")
        memory.add(depth, "interviewer", question)
        answer = human_turn(question)
        memory.add(depth, "persona", answer)
        session.turns.append({
            "turn": depth + 1,
            "question": question,
            "answer": answer,
            "drift_active": False,
            "is_summary": False,
        })
        depth += 1
    session.judge_log = judge_log
    session.final_depth = len(session.turns)
    print(f"\n{'═'*60}")
    print(f"  INTERVIEW END — depth {session.final_depth} | "
          f"natural={session.terminated_naturally}")
    print(f"{'═'*60}\n")

    if not session.terminated_naturally:
        print(f"\n  WARNING: Interview ended without natural termination. "
              f"Chain state: {chain_state.chain_summary()}")
    return session