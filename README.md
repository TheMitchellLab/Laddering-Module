# LadderChat — Human-in-the-Loop Interview Tool
> Companion code for **"{{LadderTeam: Dual-Agent Laddering Elicitation Framework}}"** - {{Venue: ACM AI Summit 2026}}.
> 📄 Paper pdf: ({{https://arxiv.org/html/2608.17029v1}}) | ✉️ {{Manjushree.aithal@cuanschutz.edu}}
>
** Authors:** {{Manjushree Aithal}}, {{Alexander Kotz}}, {{James Mitchell}}

---
## About
LadderTeam is a research prototype for running **structured qualitative interviews** where an LLM acts a the interviewer and a human answers. It implements the Reynolds & Gutman (1988) laddering methodology with three probing strategies (ACV, 5-Whys, JTBD) and a separate judge LLM that scores interview quality in real time. Built to study whether LLM interviews can surface actionable design insight from wireframe evaluations.

---

## How it works

```
Wireframe image(s)
      │
      ▼
Interviewer LLM ──► Question displayed in terminal
                          │
                    Human types answer
                          │
                    Judge LLM scores silently
                          │
                    Interviewer LLM generates next question
                          │
                    ... repeats until chain is complete ...
                          │
                    Judge LLM writes end-of-session report
                          │
                    Results saved to results/results_{screen}_{method}_{model}_iterN.json
```

---

## Prerequisites

```markdown
**Python:** 3.10 or later

**Install:**
```bash
pip install -r requirements

Or manually:
```bash
pip install "openai>=1.40" "httpx>=0.27" "anthropic>=0.34"

`httpx` is only needed for local Ollama runs. `anthropic` is only needed if using Anthropic as the judge provider directly (the built-in shim handles most cases via the OpenAI-compatible layer).

**API keys (cloud mode):**

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

**Local mode:** requires [Ollama](https://ollama.com) running with models pulled:

```bash
ollama pull gemma4:12b
ollama pull qwen3.6:27b
ollama serve
```

---

## Running an interview

### Basic command

```bash
python pipeline_p3.py \
  --cloud \
  --provider openai --model gpt-5.5 \
  --judge-provider anthropic --judge-model claude-sonnet-4-6 \
  --laddering-method acv \
  --wireframe-images u1.png
```

### With multiple wireframe screens

```bash
python pipeline_p3.py \
  --cloud \
  --provider openai --model gpt-5.5 \
  --judge-provider anthropic --judge-model claude-sonnet-4-6 \
  --laddering-method jtbd \
  --wireframe-images screen1.png screen2.png screen3.png
```

### Local models (Ollama)

```bash
python pipeline_p3.py \
  --local \
  --model gemma4:12b \
  --judge-model qwen3.6:27b \
  --laddering-method 5whys \
  --wireframe-images u1.png
```

### Skip judge

```bash
python pipeline_p3.py \
  --cloud \
  --provider openai --model gpt-5.5 \
  --laddering-method acv \
  --wireframe-images u1.png \
  --skip-judge
```

---

## What happens at runtime

**Step 1 — Initial reaction**

The terminal shows the wireframe path(s) and prompts you to type a 3–5 sentence surface-level first impression. Be vague and mixed — something seems to work, something is uncertain.

**Step 2 — Vague seed**

You pick a short phrase (3–12 words) from your initial reaction for the interviewer to probe. Press Enter to auto-extract.

**Step 3 — Interview**

The interviewer LLM generates a clarification question, then proceeds with the chosen laddering method. Each question is shown in a box:

```
------------------------------------------------------------
  INTERVIEWER ASKS
-───────────────────────────────────────────────────────────
  What is it about the layout that feels off to you?
------------------------------------------------------------

  ▶ You >
```

Type your answer and press Enter. Repeat until the chain terminates naturally.

---

## Laddering methods

| Method | Flag | What it surfaces |
|---|---|---|
| ACV | `--laddering-method acv` | Attribute → Consequence → Value: actionable design requirements |
| 5-Whys | `--laddering-method 5whys` | Causal chain from friction point to root cause |
| JTBD | `--laddering-method jtbd` | Situation → Job → Outcome → Barrier chain |

---

## CLI flags

| Flag | Default | Description |
|---|---|---|
| `--laddering-method` | `acv` | `acv`, `5whys`, or `jtbd` |
| `--wireframe-images PATH…` | required | One or more image paths (PNG, JPG, GIF, WebP) in flow order |
| `--cloud` | default | Use cloud API providers |
| `--local` | — | Use Ollama local models |
| `--provider` | `openai` | Interviewer provider: `openai`, `anthropic`, `gemini`, `ollama`, `openrouter`, `together`, `dashscope` |
| `--model` | `gpt-5.5` | Interviewer model ID |
| `--judge-provider` | `anthropic` | Judge provider |
| `--judge-model` | `claude-sonnet-4-6` | Judge model ID |
| `--judge-active` | — | Judge injects tactic feedback into each next question |
| `--judge-shadow` | default | Judge scores silently, no injection |
| `--skip-judge` | — | Disable judge entirely |
| `--output-dir DIR` | `results` | Where to save the JSON result |
| `--output-filename NAME` | `results_{screen}_{method}_{model}.json` | Override the base output filename (an `_iterN` suffix is always appended) |
| `--vague-seed TEXT` | — | Skip the seed prompt, use this text directly |
| `--prior-response TEXT` | — | Skip the initial reaction prompt, use this text directly |
| `--prior-response-file PATH` | — | Load prior response from a file (safer than `--prior-response` for long/special-char text) |
| `--iterations N` | `1` | Number of complete interview runs. Prior response and vague seed are collected once and reused across all iterations |
| `--seed-only` | — | Collect prior response + vague seed, print as JSON, then exit (no interview) |
| `--fast` | — | Debug mode (with `--local` only): swaps both roles to `qwen2.5:7b` for fast parsing verification |

---

## Default model pairing

| Mode | Interviewer | Judge |
|---|---|---|
| Cloud | `gpt-5.5` (OpenAI) | `claude-sonnet-4-6` (Anthropic) |
| Local | `gemma4:12b` (Ollama) | `qwen3.6:27b` (Ollama) |

The judge must always use a different model than the interviewer — the pipeline exits with an error if they match.

Wireframe interviews require a **vision-capable model**. `qwen2.5:7b` does not support vision and cannot be used as the interviewer.

---

## Output

Results are saved to `results/results_{screen}_{method}_{model}_iterN.json` (or the name passed via `--output-filename`, with an `_iterN` suffix appended) and contain:

- `prior_response` — your initial wireframe reaction
- `vague_seed` — the phrase that was probed
- `turns` — list of `{turn, question, answer}` objects
- `interview_summary` — LLM-generated summary of the chain
- `judge_log` — per-turn scores (ladder score, deflection score, tactic, composite)
- `judge_report` — end-of-session efficiency score and missed opportunities

---

## File structure

```
manual_ladder/
├── pipeline_p3.py              # CLI entry point and orchestration
├── ladderchat_interview_p3.py  # Interview engine (all LLM calls, state machines)
├── README.md                   # This file
└── results/                    # JSON outputs (created on first run)
```
