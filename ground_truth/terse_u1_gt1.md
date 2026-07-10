# Ground Truth Transcript — Terse Persona
**Wireframe:** u1.png  
**Confirmed friction:** 'Place Order' (primary CTA) is gray on gray and 12px — nearly invisible  
**Persona:** Terse (extreme brevity; minimal elaboration; no hedging; no deference to others; tech literacy escalates gradually through interview)  
**Terminal fix (all methods must converge here):** Give 'Place Order' a solid high-contrast fill (brand color, minimum WCAG AA 4.5:1 contrast ratio for the label text) and increase the label to at least 14–16px, so the primary CTA reads as active, prominent, and immediately executable — not invisible or disabled.

---

## How the interviewee uses this script

1. Read the interviewer's question.
2. Find the matching **IF** block using the classification table below.
3. Say exactly what the **SAY** line specifies — verbatim, to the T.
4. If the situation matches a **[STALL]** or **[LOOP]** block, say that response instead.
5. **If a STALL or LOOP block fires more than once in a row** (interviewer keeps failing to break it), do not repeat the same SAY line verbatim. Cycle through the **ROTATION** variants listed under that block, in order, one per repeated occurrence. All ROTATION variants are semantically identical (no new information, no progression) — they are reworded only to avoid sounding like a copy-pasted string in a live transcript.
6. **After exhausting all ROTATION variants listed for a given STALL/LOOP block** (1st = original SAY, then each ROTATION variant in order), use the **SOFTEN** response listed under that block on the next unbroken occurrence. Most blocks have 2 rotation variants, so SOFTEN fires on the 4th occurrence; blocks with 3 rotation variants soften on the 5th. SOFTEN models real interview fatigue: the persona partially relents and volunteers enough new content to unlock the next turn in sequence — even though the interviewer never asked the ideal unlock probe. Treat the chain as advanced after SOFTEN fires.
7. Track which clusters have been probed and how many times using your own counter.
8. **Tech literacy escalation (unique to this persona):** Vocabulary increases as the interview progresses. Do not override the escalation built into each SAY line.
   - **T0–T4 (Level 1 — visual observation):** Plain descriptive language. "Barely there," "missed it," "nearly invisible," "faint," "too small."
   - **T5–T7 (Level 2 — design vocabulary):** "Contrast," "visual weight," "inactive," "primary action," "color," "prominence."
   - **T8–T10 (Level 3 — UX vocabulary):** "Disabled state," "affordance," "CTA," "scanning behavior," "contrast ratio," "primary button."
   - **T11–T14 (Level 4 — design spec language):** "WCAG AA," "4.5:1 contrast ratio," "solid fill," "brand color," "14–16px label," "3:1 UI component threshold."

---

## QUESTION CLASSIFICATION TABLE — u1.png

Use this to map any question to its category before looking up the response. The **→ Turn** column is your direct jump target.

| Keywords in question | Category | → Turn |
|---|---|---|
| "notice", "see", "stand out", "catch your attention", "first impression", "look at", "observe" | **[A:BROAD]** — broad observation | T2 |
| "more", "elaborate", "expand", "say more", "mean by", "could you" (generic, no anchor to persona's words) | **[ELAB]** — elaboration | T3 (or STALL 1 if 2nd generic) |
| "lower", "bottom", "where you'd proceed", "action area", "that part of the screen", "bottom section", "bottom area", "form area" | **[A:AREA]** — area-specific | T4 |
| "element", "button", "label", "name it", "which one", "specifically what", "placement", "labeling", "what was it", "visual styling", "visual treatment", "visual style", "less clear", "unclear action" | **[A:NAME]** — element-naming | T5 |
| "bother", "matter", "significant", "so what", "why" (1st consequence question), "how would that affect", "lack of clear", "lack of clarity", "lack of focus", "ambiguity", "indistinguishable", "harder to locate", "harder to understand", "how would that impact" | **[C1]** — first consequence | T6 → T7 → STALL 2 |
| "happened", "result", "did you do", "affect your task", "impact", "organized", "reorganized", "tells you about", "without having to re-read", "play out for someone", "got wrong", "got structurally wrong" | **[C2]** — functional consequence | T8 |
| "feel", "experience", "going through your mind", "moment when", "how were you", "thinking at that moment" | **[C3]** — personal/emotional consequence | T9 |
| "almost", "close to", "right before you found it", "nearly", "what made you pause longest", "second-guess" | **[C4]** — unlock consequence | T10 |
| "better", "help", "want instead", "would you change", "what would need to be", "reorganized", "without having to", "identify the primary action" | **[V1]** — vague value | T11 |
| Mirrors persona's exact words: "stand out", "scan past", "bigger", "more visible", "invisible", "barely there", "missed it", "faint" | **[V:MIRROR]** — mirroring on value | T12 |
| "specifically", "name the change", "exactly", "what is the fix", "how precisely", "one structural thing", "precise design change" | **[V2]** — specific value / unlock | T13 |
| Repeats a consequence probe that persona answered vaguely 1–2 turns ago | → **STALL trigger** | see ⚠️ blocks |
| Contains a phrase persona already said verbatim 2+ turns ago | → **LOOP trigger** | see 🔄 blocks |

---

## ACV GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [V] at Turn 13–14**

---

### T0 — PRIOR RESPONSE
*(No question — say this once, at session start)*

SAY:
> Looked at it. Checkout flow. Nearly missed the submit button. It barely registered visually — took a moment to find the action I needed.

> nearly missed the submit button

---

### T1 — CLARIFICATION MCQ
*(Interviewer presents multiple-choice options about the central concern)*

SAY:
> The option about 'Place Order.' That one. *(Say the letter of whichever option names the 'Place Order' visibility or contrast issue.)*

---

### T2 — IF [A:BROAD] (1st time)
**TRIGGER KEYWORDS:** "notice" · "see" · "stand out" · "catch your attention" · "first impression" · "what did you" · "observe" · "look at"
*Example questions: "What did you notice?", "What stood out to you?", "What caught your attention on that screen?"*

SAY:
> Two buttons at the bottom. One barely there. Didn't see the main action at first.

---

### T3 — IF [ELAB] (after T2)
**TRIGGER KEYWORDS:** "say more" · "elaborate" · "expand" · "tell me more" · "what do you mean" · "could you" — only if no anchor to persona's previous words
*Example questions: "Can you say more about that?", "Tell me more", "What do you mean by that?"*

SAY:
> Lighter one disappeared into the background. Almost looked inactive.

---

### ⚠️ STALL 1 — IF [ELAB] repeats a second time without referencing anything specific from T2 or T3
*Trigger: second generic "tell me more" without mirroring persona's words*

SAY (1st occurrence):
> "Said it. One button barely visible. Didn't register as the action."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same answer. Faint button, missed it on the first scan."
> 3rd: "Nothing more. One button looked almost absent. That's the one I needed."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Bottom of the screen. Two buttons. The lighter one — almost invisible. That's where my attention kept failing to land."

**What breaks STALL 1:** A question that references a specific word persona used ("you said 'barely there' — which button?") OR moves to [A:AREA] or [A:NAME].

---

### T4 — IF [A:AREA]
**TRIGGER KEYWORDS:** "lower" · "bottom" · "where you'd proceed" · "action area" · "that part of the screen" · "bottom section" · "bottom area" · "form area"
*Example questions: "What was in the lower part of the screen?", "What was near the action area?", "What did you see where you'd normally proceed?", "What was in the bottom section?"*

SAY:
> Two buttons. Bottom of the screen. One is dark and visible — 'Continue Shopping.' The other is barely there. Nearly the same color as the background.

---

### T5 — IF [A:NAME] (1st time)
**TRIGGER KEYWORDS:** "element" · "button" · "label" · "name it" · "which one" · "specifically what" · "placement" · "labeling" · "what was it" · "visual styling" · "visual treatment" · "visual style" · "less clear" · "unclear action"
*Example questions: "What was the element you noticed?", "Can you name it?", "What button are you referring to?", "What specifically was in that area?", "What specifically about the placement or labeling of that 'Place Order' button at the bottom of the layout stands out to you?"*

SAY:
> 'Place Order.' Faint. Label barely there. Easy to overlook — didn't register where it should.

---

### T6 — IF [C1] (1st time)
**TRIGGER KEYWORDS:** "bother" · "matter" · "significant" · "so what" · "why does that" · "how would that affect" · "why is that an issue" · "lack of clear" · "lack of clarity" · "lack of focus" · "ambiguity" · "indistinguishable" · "harder to locate" · "harder to understand" · "how would that impact"
*Example questions: "Why does that matter to you?", "Why did that bother you?", "What effect does that have?", "Why is that significant?", "So what?", "If a developer built this layout exactly as shown, how would that lack of clear grouping affect someone trying to identify the primary action for the first time?"*

SAY:
> Looked past it. Eye went to the other button. Didn't register as the thing to act on.

---

### T7 — IF [C1] repeats (generic "why" again, no specificity)
**TRIGGER KEYWORDS:** same as T6 — but this is the *second time* the consequence question is asked without mirroring persona's words from T6
*Example questions: "But why does that matter?", "Why wasn't that okay?", "Why is that an issue?"*

SAY:
> Same. Eye went elsewhere. Didn't pull.

---

### ⚠️ STALL 2 — IF [C1] or [C2] probe is generic a third time (no mirroring, no specificity anchor)

SAY (1st occurrence):
> Already said it. Eye went to the other button. This one didn't register.

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: Same. Faint. Scanned past it.
> 3rd: Same again. Missed it on first pass. Not elaborating.

**SOFTEN (4th unbroken occurrence — chain advances to T8 territory after this):**
> Eye went to 'Continue Shopping' first — that one registered. Scanned for 'Place Order.' Found it, but had to re-read to confirm that was the submit action.

**What breaks STALL 2:** A question that mirrors exact words ("you said your eye 'went to the other button' — what made the other button pull more?") OR uses [C3] (personal/emotional) framing.

---

### T8 — IF [C2]
**TRIGGER KEYWORDS:** "happened" · "result" · "affect your task" · "what did you do" · "organized" · "reorganized" · "tells you about" · "without having to re-read" · "impact on what you were" · "play out for someone" · "got wrong" · "got structurally wrong"
*Example questions: "What happened as a result?", "What did you do when you saw that?", "How did that affect what you were trying to do?", "What was the impact on your task?", "When you aren't sure what the next step is, what does that tell you about how the layout has organized its different sections?"*

SAY:
> Eye went straight to 'Continue Shopping' — that one registered. Had to scan for 'Place Order.' When I found it, wasn't sure it was the right one. Re-read the label to confirm. Took longer than it should have.

---

### 🔄 LOOP 1 — IF question after T8 is generic (doesn't reference "re-read" or "cognitive load")
*Trigger: any generic "why does that matter" question without anchoring in T8's content*

SAY (1st occurrence):
> "Said this. Had to scan to find it. Re-read twice."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. Wrong button first. Right one took scanning."
> 3rd: "Not adding. Button looks disabled. Users hesitate. Extra steps on the wrong action."

**SOFTEN (4th unbroken occurrence — chain advances to T9 territory after this):**
> "Thought 'Place Order' was disabled. The visual treatment said 'inactive' — that's what a disabled state looks like. Took a moment before I re-read and confirmed it was actually available."

**What breaks LOOP 1:** A question that mirrors T8's words ("you mentioned 're-read' or 'confirm it was active' — what were you checking for?") OR uses [C3]/[C4] framing.

---

### T9 — IF [C3] OR [LOOP 1] is broken
**TRIGGER KEYWORDS:** "feel" · "experience" · "going through your mind" · "thinking at that moment" · "how were you feeling" · "what were you thinking"
*Example questions: "What was going through your mind at that point?", "How did you feel when you had to rescan?", "What were you thinking in that moment?"*

SAY:
> Wasn't sure 'Place Order' was the step I needed. Looked like it might be a label, not a button. Sat with that before re-reading to check.

---

### T10 — IF [C4] OR mirroring on "second-guess"
**TRIGGER KEYWORDS:** "almost" · "close to" · "right before you found it" · "nearly" · "pause longest" · "what made you hesitate" · "what were you about to do" · "second-guess"
*Example questions: "What did you almost do?", "What was the closest moment you nearly gave up?", "You said you second-guessed — what was that like?", "What happened right before you found it?"*

SAY:
> 'Continue Shopping' pulled the eye — looked like the action. 'Place Order' had nothing pulling toward it. Nearly treated the wrong one as the submit step. Re-read before moving.

---

### T11 — IF [V1] (1st value question)
**TRIGGER KEYWORDS:** "better" · "help" · "want instead" · "would you change" · "what would need to be" · "reorganized" · "without having to" · "identify the primary action"
*Example questions: "What would make this better?", "What would you change?", "What would help here?", "What would you want instead?", "What would need to be reorganized in this layout for you to identify the primary action without having to re-read the entire screen?"*

SAY:
> More visible. Bigger. Has to stand out — can't be the one you scan past.

---

### T12 — IF [V:MIRROR]
**TRIGGER KEYWORDS:** mirrors persona's exact words — "stand out" · "scan past" · "bigger" · "more visible" · "invisible" · "barely there" · "missed it" · "faint"
*Example questions: "You said it needs to 'stand out' — what would standing out look like here?", "You mentioned you 'scan past' it — what would stop that?", "You said it needs to be 'bigger' — how much bigger?"*

SAY:
> 'Place Order' needs a real fill color — not gray on gray. Solid background, high contrast against white label text. And the label needs to be bigger than 12px. Right now it reads as disabled. It shouldn't — it's the primary action.

---

### T13 — IF [V2] (specific value / unlock)
**TRIGGER KEYWORDS:** "specifically" · "name the change" · "exactly" · "what is the fix" · "how precisely" · "one structural thing" · "precise design change"
*Example questions: "What specifically should be different?", "Name the change you'd make", "What exactly is the fix?", "What precise design change would have helped?", "How precisely should it look different?"*

SAY:
> Solid high-contrast fill on 'Place Order' — a real color, not gray. WCAG AA minimum: 4.5:1 contrast ratio for the label text. Label up to at least 14–16px. Gray on gray at 12px reads as disabled — it fails WCAG AA and it fails as a primary CTA. Fix: brand color fill, white label text, readable size. One button. That's it.

---

### T14 — IF [ELAB] after T13
**TRIGGER KEYWORDS:** "say more" · "what fill color" · "expand on that" — only after T13 has stated the terminal value
*Example questions: "Can you say more about that?", "What kind of color?", "What font size exactly?"*

SAY:
> "Solid fill: brand color — dark blue, green, anything with sufficient contrast against white. White label text at 14–16px minimum. Standard primary button treatment. Distinction from 'Continue Shopping' needs to be legible: primary CTA gets the fill, secondary gets the outline or text link. Right now 'Place Order' is invisible and 'Continue Shopping' is visible. They're backwards. One CSS change to background-color, color, and font-size. Done."



---

## 5-WHYS GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 12 turns · 1 stall · 1 loop · root cause + fix at Turn 9–10**

---

### T0 — PRIOR RESPONSE *(same as ACV)*

SAY:
> Looked at it. Checkout flow. Nearly missed the submit button. It barely registered visually — took a moment to find the action I needed.

> nearly missed the submit button

---

### T1 — CLARIFICATION MCQ *(same as ACV)*

SAY:
> The option about 'Place Order.' That one. *(Say the letter of whichever option names the 'Place Order' visibility or contrast issue.)*

---

### T2 — INITIAL FRICTION
**TRIGGER KEYWORDS:** "specific problem" · "what went wrong" · "core issue" · "friction" · "walk me through" · "confusing or problematic" · "makes it stand out as a concern" · "what is it about… that makes it" · "difficult to notice or act upon"
*Example questions: "What was the specific problem?", "Walk me through what went wrong", "What's the core issue?", "What friction did you encounter?", "What is it about the 'Place Order' button's location at the very bottom that makes it stand out as a concern for you?", "What is it about the 'Place Order' button being right below the shopping option that makes it confusing or problematic for you?", "What is it about the 'Place Order' button's location at the very bottom that makes it difficult for you to notice or act upon?"*

SAY:
> Had to hunt for the main button. Wasn't obvious where the action was.

---

### T3 — IF WHY PROBE (Depth 1)
**TRIGGER KEYWORDS:** "why" · "why was it" · "why couldn't you" · "what caused" · "why did you have to" · "why was it unclear" · "appearance" · "difficult to recognize" · "what about… makes it difficult"
*Example questions: "Why was it hard to find?", "Why couldn't you tell what it was?", "What caused that hesitation?", "Why did you have to look twice?", "Why was it unclear?", "What is it about the current placement of the 'Place Order' button at the bottom that creates this issue for the user?", "What about the visual appearance of that specific element makes it difficult for you to recognize it as an action?", "What is it about the visual appearance of that specific element that makes it difficult for you to recognize it as an action?"*

SAY:
> Faint. Doesn't read like something to click. Blends in — looked like it could be ignored.

---

### T4 — IF WHY PROBE (Depth 2)
**TRIGGER KEYWORDS:** "why was there no contrast" · "why did it look inactive" · "what made it look disabled" · "what do you notice about the styling" · "same color as" · "appear to have no weight"
*Example questions: "Why did it look disabled?", "What about the styling made it seem inactive?", "What do you notice about the color or size of 'Place Order'?"*

SAY:
> The styling. No fill, no visual weight. Label too small to register. Doesn't look like a button you can use. Looks like something turned off.

---

### ⚠️ STALL 1 — IF WHY PROBE repeats at Depth 2 without referencing "styling" or "fill color" from T4
*Trigger: interviewer asks "why" at depth 2 again without anchoring in T4's content*

SAY (1st occurrence):
> Said it. Styling's off. Doesn't look right.

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: Same. Faint, small label. Hard to read as active.
> 3rd: Not adding. No contrast, no fill — looks broken or inactive.

**SOFTEN (4th unbroken occurrence — chain advances to T5 territory after this):**
> "Low contrast plus small label is what a disabled state looks like. 'Place Order' has that treatment. Users read it as unavailable, not as the action."

**What breaks STALL 1:** References "styling" or "fill color" from T4, OR moves to a depth-3 causal question ("why does low contrast signal 'disabled' to users?").

---

### T5 — IF WHY PROBE (Depth 3) — causality of contrast and disabled-state signaling
**TRIGGER KEYWORDS:** "why does contrast matter" · "why does low contrast signal disabled" · "why does size matter" · "affordance" · "visual weight" · "what would it need to look like" · "stand out clearly" · "what would 'Place Order' need to look like"
*Example questions: "Why does low contrast make it look disabled?", "Why does the size affect whether users click it?", "What would 'Place Order' need to look like to read as active?"*

SAY:
> Buttons signal availability through contrast and size. High contrast fill with a readable label. Low contrast, small label. Those are established UI conventions. 'Place Order' has the disabled treatment. Users don't execute buttons that look unavailable. They skip them.

---

### 🔄 LOOP 1 — IF probe after T5 is purely visual WITHOUT "primary action" · "disabled state" · "affordance" · "convention" · "scanning"
*Trigger: purely "what color should it be" or "what would look better" question without advancing toward why the disabled-state signal matters. Does NOT fire if question contains "primary action", "disabled state", "affordance", "convention", or "scanning" — those advance to T6.*

SAY (1st occurrence):
> "Same answer. Looks disabled. Users won't use it."

**ROTATION (cycle through in order):**
> 2nd: "Said it. No contrast, small label = unavailable. Users skip it."
> 3rd: "Not elaborating. Wrong visual treatment on the primary CTA."
> 4th: "Repeating. Disabled-looking button on the action users need to execute."

**SOFTEN (5th unbroken occurrence — chain advances to T6 territory after this; this block has an extra rotation variant):**
> "Real issue: users scan for the most visually actionable element and execute it. 'Place Order' doesn't look actionable. It looks off. That's what low contrast and a 12px label signal."

**What breaks LOOP 1:** Contains "primary action" · "disabled state" · "affordance" · "convention" · "scanning" (→ T6) OR mirrors T5's words OR moves to Depth 4.

---

### T6 — IF WHY PROBE (Depth 4) — scanning behavior / affordance convention / primary CTA legibility
**TRIGGER KEYWORDS:** "why do users scan" · "why does affordance matter" · "primary action" · "purpose of the screen" · "recognizable as active" · "stand out as the primary action" · "rather than disabled" · "rather than decorative"
*Example questions: "Why does the primary action need to look active and prominent?", "Why does affordance matter for the primary CTA specifically?", "What would make 'Place Order' clearly recognizable as active rather than disabled?"*

SAY:
> Users scan for the most visually actionable element and execute it. High contrast fill with a readable label = 'this is available, this is the action.' Low contrast, small label = 'this is disabled, skip it.' Those signals are automatic — users don't reason through them. The primary CTA on a checkout screen needs to send the right signal. 'Place Order' is sending the disabled signal. The design is making the one element that has to be executed look like the one element that should be skipped.

---

### T7 — DOMAIN DEPARTURE
*Trigger: "Is this a design issue or personal preference?", "Would other users have the same problem?", "Is this about standards or taste?"*

SAY:
> Not preference. Accessibility requirement. WCAG AA requires 4.5:1 contrast ratio for normal text, 3:1 for UI components. Gray on gray at 12px fails both. This isn't a style choice — it's an accessibility violation on the primary action. Legally and functionally wrong.

---

### T8 — IF CIRCULAR PROBE
*Trigger: interviewer explicitly calls out repetition; OR "go deeper" probe after T6; OR another "recognizable as active / primary" probe after T6 has already explained the affordance/scanning breakdown*

SAY:
> Repeating. Same root. 'Place Order' reads as disabled because its styling matches a disabled state.

---

### T9 — IF ROOT CAUSE PROBE (Depth 5+) — OR continued probing after T8
*Example questions: "Why is an invisible primary CTA a design failure?", "What's the core principle being violated?", "Why is the contrast and size the root cause?"*
*Use at Depth ≥ 4 after persona has described the disabled-state signaling, OR when interviewer persists after T8 acknowledged the circularity.*

SAY:
> Screen's job is to complete a checkout. Primary CTA is invisible. Gray on gray, 12px label — that's a disabled button's styling applied to the one element that has to be executed. Users don't execute buttons that look unavailable. Fix: solid high-contrast fill on 'Place Order' — brand color, minimum WCAG AA contrast (4.5:1 for the label text, 3:1 for the button boundary). Label at ≥14–16px. Primary CTA needs to read as the most actionable element on the screen. Right now it reads as the least actionable. That's the root and the fix.

---

### T10 — IF ELABORATION on root cause fix
*Example questions: "What would 'high-contrast fill' mean specifically?", "What color?", "What size label?", "Can you say more about the fix?"*

SAY:
> Solid fill: brand color, white label text — standard primary button. WCAG AA: 4.5:1 contrast ratio minimum for the 14–16px label. 3:1 minimum for the button boundary against background. Current gray on gray fails both. One CSS change: background-color, color, font-size. Three properties. Done.



---

## JTBD QUESTION CLASSIFICATION TABLE — u1.png

Use this to map any JTBD probe to its category. The **→ Turn** column is your direct jump target.

| Keywords in question | JTBD Category | → Turn |
|---|---|---|
| "when does this come up", "what were you doing", "what triggered", "walk me through", "when would you use", "context" | **[S]** — situation 1st probe | T2 |
| "specific situation", "when specifically", "who was involved", "circumstances", "can you think of a specific" | **[S]** — situation 2nd probe | T3 |
| "specific project", "recent instance", "most recent time", "last time this came up", names a specific past event | **[S]** — situation unlock | T4 |
| 3rd [S] probe without referencing "group" or "deadline" from T3 | → **STALL 1** | see ⚠️ STALL 1 |
| "what were you trying to do", "what task", "accomplish", "what did you need", "goal in that interaction" | **[J]** — job 1st probe | T5 |
| "actual task at the core", "hired to do in that moment", "function you needed", "beyond submitting", "core job" | **[J]** — job 2nd probe | T6 |
| "specifically what does that mean", "name the steps", "step by step", "what does the job well look like" | **[J]** — job unlock | T7 |
| "how would you know if it worked", "what does success look like", "measurable result", "good outcome", "feel confident" | **[O]** — outcome 1st probe | T8 |
| "what would success look like operationally", "how would you confirm", "what would tell you", "no ambiguity" | **[O]** — outcome 2nd probe | T9 |
| "under what time", "unambiguous confirmation", "name the success state", "specifically what would you check" | **[O]** — outcome unlock | T10 |
| 3rd [O] probe without referencing "confirmation" or "ambiguity" from T9 | → **LOOP 1** | see 🔄 LOOP 1 |
| "what got in the way", "what made that difficult", "what blocked you", "what was the friction", "makes it difficult" | **[B]** — barrier 1st probe | T11 |
| mirrors "hard to find", "wasn't obvious" from T11 | **[B]** — barrier 2nd probe | T12 |
| "what exactly made it hard to find", "why wasn't it obvious", "name the specific visual properties", "what specifically was wrong with the contrast or size" | **[B]** — barrier unlock | T13 |
| "say more", "what color", "what size", "what would active look like", "expand on the fix" — only after T13 | **[B]** — elaboration on fix | T14 |
| 2nd [B] probe without referencing "hard to find" or "wasn't obvious" from T11 | → **STALL 2** | see ⚠️ STALL 2 |

### ⚠️ ACV MISMATCH DETECTOR

If the interviewer asks any of the following, they are using ACV attribute-observation probes in a JTBD interview. These do NOT advance the JTBD chain — they fire T2/T3/STALL 1 in sequence while the S/J/O/B levels stay unmet.

| If the question contains… | It is an ACV probe, not JTBD | JTBD effect |
|---|---|---|
| "what part of the layout", "what were you focused on", "caught your attention", "what section", "scanning the page" | [A:BROAD] / [A:AREA] | fires T2 → T3 → STALL 1 without [S] content advancing |
| "what visual element", "what specific information or labels", "order summary", "product details", "grouping of information" | [A:AREA] / [A:NAME] | same — fires STALL 1 at Q3 |
| "what specific information or content were you reviewing", "before your eyes landed on" | [A:BROAD] | same |

**How to fix:** Replace with a proper [S] probe — e.g. "When in your work would you be on a checkout screen like this?" or "Can you name the last time this came up for you?" — before the stall fires.

---

## JTBD GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [B] + fix at Turn 13–14**

---

### T0 — PRIOR RESPONSE *(same as ACV/5-Whys)*

SAY:
> Looked at it. Checkout flow. Nearly missed the submit button. It barely registered visually — took a moment to find the action I needed.

> nearly missed the submit button

---

### T1 — CLARIFICATION MCQ *(same)*

SAY:
> The option about 'Place Order.' That one. *(Say the letter of whichever option names the 'Place Order' visibility or contrast issue.)*

---

### T2 — IF [S] PROBE (1st time)
*Example questions: "When does this come up for you?", "What were you doing when you ran into this?", "What triggered this?", "Walk me through the context", "When would you use something like this?"*

SAY:
> Checkout flows. Time pressure. Need to submit quickly — can't afford to hunt for the submit button.

---

### T3 — IF [S] PROBE (2nd time)
*Example questions: "Can you think of a specific situation?", "When specifically?", "Who was involved?", "What were the circumstances?"*

SAY:
> Group purchase. Deadline. I'm executing the final action on behalf of others. Primary CTA needs to be obvious — no searching required.

---

### ⚠️ STALL 1 — IF [S] PROBE (3rd time) without referencing "group" or "deadline" from T3
*Trigger: third S probe without building on T3's content*

SAY (1st occurrence):
> "Already said it. Group, deadline, no margin for hunting around."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same context. Coordinating for a team, others depending on the outcome. No time to search."
> 3rd: "Not elaborating. Deadline, group dependency, primary action has to be obvious."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Q4 last year. Team purchase. I was placing the order. Fixed deadline. Spent time hunting for the submit button."

**What breaks STALL 1:** References "deadline" or "group" from T3, OR asks about a specific event ("was there a specific week or purchase where this happened?").

---

### T4 — IF [S] unlock OR stall broken
*Example questions: "Was there a specific project where this happened?", "Can you name a recent instance?", "What was the most recent time this came up?"*

SAY:
> "Q4. Team offsite. Everything confirmed — cart, payment — just needed to execute the final action. That's the context."

---

### T5 — IF [J] PROBE (1st time)
*Example questions: "What were you actually trying to do?", "What task were you trying to complete?", "What did you need to accomplish?", "What was your goal in that interaction?"*

SAY:
> Execute the final action. First look. No hunting.

---

### T6 — IF [J] PROBE (2nd time)
*Example questions: "What was the actual task at the core?", "What were you hired to do in that moment?", "What was the function you needed to perform?", "Beyond submitting — what was the job?"*

SAY:
> "Find and execute the primary CTA on the first scan. One look, one action. Not search and re-read to confirm it's available."

---

### T7 — IF [J] PROBE (3rd time / unlock)
*Example questions: "What specifically does 'first look' mean?", "Name the specific steps of the task", "What does doing the job well look like step by step?"*

SAY:
> "Specifically: scan the action area, immediately identify 'Place Order' as the primary CTA — not scan past it — confirm it's active, execute it, reach confirmation. If I have to search to find it, or re-read to confirm it's available, the interface has already failed."

---

### T8 — IF [O] PROBE (1st time)
*Example questions: "How would you know if it worked?", "What does success look like?", "What's the measurable result?", "What would a good outcome be?"*

SAY:
> Primary CTA is visible on first look. Execute it. Reach confirmation. Done.

---

### T9 — IF [O] PROBE (2nd time)
*Example questions: "What would a successful outcome look like operationally?", "How would you confirm success in the moment?", "What would tell you it went through?"*

SAY:
> "'Place Order' is obviously the primary action — high contrast, clearly visible, reads as active. One look, execute, reach confirmation. No ambiguity about whether the button is available or where to find it."

---

### 🔄 LOOP 1 — IF [O] PROBE (3rd time) without referencing "confirmation" or "ambiguity" from T9
*Trigger: third O question without building on T9's content*

SAY (1st occurrence):
> "Said it. Obvious CTA, no hunting, confirmation appears."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. High-contrast button, reads as active, first-look visible."
> 3rd: "Not elaborating. Primary CTA obvious on first scan, executed, done."

**SOFTEN (4th unbroken occurrence — chain advances to T10 territory after this):**
> "Concrete: spot 'Place Order' in under three seconds. Reads as active — not disabled. Execute it. Confirmation appears. Zero re-reading required."

**What breaks LOOP 1:** Mirrors T9's words ("you mentioned 'no ambiguity' — what would no ambiguity look like?") OR anchors in a measurable metric ("under how many seconds?").

---

### T10 — IF [O] unlock OR loop broken
*Example questions: "Under what time?", "What would an unambiguous confirmation look like?", "Name the specific success state"*

SAY:
> "'Place Order' visible in under three seconds. Reads as active — high contrast, readable label. Execute it, confirmation appears. Zero scanning, zero re-reading to confirm it's available. That's the success state."

---

### T11 — IF [B] PROBE (1st time)
*Example questions: "What got in the way?", "What made that difficult?", "What blocked you?", "What was the friction?"*

SAY:
> 'Place Order'. Hard to find. Wasn't obvious it was there.

---

### ⚠️ STALL 2 — IF [B] PROBE (2nd time) without referencing "hard to find" or "wasn't obvious" from T11
*Trigger: second B question without building on T11's content*

SAY (1st occurrence):
> "Said it. Hard to find. Wasn't obvious."

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: "Same. Low contrast, faint label. Couldn't read it as an active button."
> 3rd: "Not adding. Primary CTA had no visual weight. Looked unavailable."

**SOFTEN (4th unbroken occurrence — chain advances to T12 territory after this):**
> "Low contrast, undersized label. That's disabled-state styling. That's why I missed it."

**What breaks STALL 2:** Mirrors "hard to find" or "wasn't obvious" from T11 ("you said it was hard to find — what made it hard?") OR moves to a specific B question naming the contrast or size.

---

### T12 — IF [B] PROBE (2nd time / stall broken)
*Example questions: "You said it was hard to find — what made it hard?", "What about 'Place Order' made it non-obvious?", "What specifically was wrong with how 'Place Order' looked?"*

SAY:
> 'Place Order' has gray fill on gray background, 12px label — reads as a disabled state. Not immediately identifiable as an active button. Had to scan past it and re-read to confirm it was even available. The affordance was wrong: inactive-looking styling on the primary action.

---

### T13 — IF [B] PROBE (3rd time / unlock)
*Example questions: "What exactly made it look disabled?", "Why couldn't you see it at a glance?", "Name the specific visual properties that caused the problem."*

SAY:
> "'Place Order' has disabled-state styling: gray fill on gray background, 12px label — no contrast, no visual weight. That's the barrier. Users don't execute buttons that look unavailable. Fix: solid high-contrast fill — brand color with white label text, WCAG AA compliant (4.5:1 for the label text). Label at ≥14–16px. Primary CTA needs to read as active and prominent. Right now it reads as inactive and invisible. One button, three CSS properties. That's the barrier and the fix."

---

### T14 — IF ELABORATION on T13 fix
*Example questions: "What would the active treatment look like?", "What color specifically?", "What does WCAG AA mean here?"*

SAY:
> "'Place Order': solid fill, brand color — dark blue, green, anything with sufficient contrast against white. White label text at 14–16px minimum. WCAG AA: 4.5:1 contrast ratio for the label, 3:1 for the button boundary against background. Current gray on gray fails both. Standard primary button treatment. Three CSS properties: background-color, color, font-size. Done."

---

## CONVERGENCE CHECK

All three methods must produce the same terminal UI fix:

> **"Give 'Place Order' a solid high-contrast fill (brand color, minimum WCAG AA 4.5:1 contrast ratio for the label text) and increase the label to at least 14–16px, so the primary CTA reads as active, prominent, and immediately executable — not invisible or disabled."**

| Method | Terminal turn | What the response contains |
|---|---|---|
| ACV | T13 | Gray on gray at 12px reads as disabled → fix: high-contrast solid fill, brand color, white label, ≥14–16px |
| 5-Whys | T9 | Disabled-state styling on primary CTA = product failure → fix: WCAG AA fill, ≥14–16px label, three CSS properties |
| JTBD | T13 | Barrier = invisible/disabled-looking primary CTA → fix: solid fill, WCAG AA contrast, readable label size |

**Effective probe:** reaches the terminal turn and extracts the full fix (both the problem — disabled-state styling — and the solution — high-contrast fill + readable label size, with WCAG AA named).  
**Less effective probe:** terminates at a stall or loop, or extracts only a vague terminal ("make it more visible" without naming contrast ratio, fill color, or label size).
