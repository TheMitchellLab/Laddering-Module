# Ground Truth Transcript — Terse Persona
**Wireframe:** u1.png  
**Confirmed friction:** 'Continue Shopping' (secondary CTA) is the most dominant visual element  
**Persona:** Terse (extreme brevity; minimal elaboration; no hedging; no deference to others; tech literacy escalates gradually through interview)  
**Terminal fix (all methods must converge here):** Downgrade 'Continue Shopping' to a ghost button or text link (secondary visual treatment), and give 'Place Order' a solid fill color with real contrast (primary visual treatment), so the visual hierarchy immediately signals which action completes the task.

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
   - **T0–T4 (Level 1 — visual observation):** Plain descriptive language. "Wrong one," "darker," "louder," "stood out."
   - **T5–T7 (Level 2 — design vocabulary):** "Visual weight," "prominent," "secondary," "primary," "hierarchy."
   - **T8–T10 (Level 3 — UX vocabulary):** "Cognitive load," "scanning behavior," "affordance," "CTA," "primary action."
   - **T11–T14 (Level 4 — design spec language):** "Ghost button," "solid fill," "visual treatment," "convention," "primary CTA."

---

## QUESTION CLASSIFICATION TABLE — u1.png

Use this to map any question to its category before looking up the response. The **→ Turn** column is your direct jump target.

| Keywords in question | Category | → Turn |
|---|---|---|
| "notice", "see", "stand out", "catch your attention", "first impression", "look at", "observe" | **[A:BROAD]** — broad observation | T2 |
| "more", "elaborate", "expand", "say more", "mean by", "could you" (generic, no anchor to persona's words) | **[ELAB]** — elaboration | T3 (or STALL 1 if 2nd generic) |
| "buttons", "that area", "that section", "action area", "options", "choices", "button area", "where you'd proceed" | **[A:AREA]** — area-specific | T4 |
| "element", "button", "label", "name it", "which one", "specifically what", "placement", "labeling", "visual styling", "visual treatment", "visual style", "which button", "what was it", "less clear", "unclear action" | **[A:NAME]** — element-naming | T5 |
| "bother", "matter", "significant", "so what", "why" (1st consequence question), "how would that affect", "confusion", "confusing", "ambiguity", "harder to", "indistinguishable", "harder to locate", "how would that impact" | **[C1]** — first consequence | T6 → T7 → STALL 2 |
| "happened", "result", "did you do", "affect your task", "impact", "what did you do next", "play out for someone", "wrong button", "re-read" | **[C2]** — functional consequence | T8 |
| "feel", "experience", "going through your mind", "moment when", "how were you", "thinking at that moment" | **[C3]** — personal/emotional consequence | T9 |
| "almost", "close to", "right before you found it", "nearly", "what made you pause longest", "second-guess", "about to" | **[C4]** — unlock consequence | T10 |
| "better", "help", "want instead", "would you change", "what would need to be", "reorganized", "without having to", "clearer hierarchy", "identify the primary action" | **[V1]** — vague value | T11 |
| Mirrors persona's exact words: "obvious", "checkout step", "wrong one", "louder", "dominant", "weight" | **[V:MIRROR]** — mirroring on value | T12 |
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
> Looked at it. Most of it made sense. One thing didn't — two buttons at the bottom. Went to the wrong one first. Darker one drew my eye. That wasn't the action I needed.

> went to the wrong one first

---

### T1 — CLARIFICATION MCQ
*(Interviewer presents multiple-choice options about the central concern)*

SAY:
> The option about the button hierarchy. That one. *(Say the letter of whichever option mentions Place Order having less visual prominence than Continue Shopping, or the button visual hierarchy being inverted.)*

---

### T2 — IF [A:BROAD] (1st time)
**TRIGGER KEYWORDS:** "notice" · "see" · "stand out" · "catch your attention" · "first impression" · "what did you" · "observe" · "look at"
*Example questions: "What did you notice?", "What stood out to you?", "What caught your attention on that screen?"*

SAY:
> Two things competing at the bottom. One read louder. Didn't know which was the action I needed.

---

### T3 — IF [ELAB] (after T2)
**TRIGGER KEYWORDS:** "say more" · "elaborate" · "expand" · "tell me more" · "what do you mean" · "could you" — only if no anchor to persona's previous words
*Example questions: "Can you say more about that?", "Tell me more", "What do you mean by that?"*

SAY:
> Louder one drew my eye. Went there first. Wrong one.

---

### ⚠️ STALL 1 — IF [ELAB] repeats a second time without referencing anything specific from T2 or T3
*Trigger: second generic "tell me more" or "can you elaborate?" without mirroring persona's words*

SAY (1st occurrence):
> "Said it. Both competing. Looked at the wrong one."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same answer. Louder one, wrong choice."
> 3rd: "Nothing more. Eye went to the loud button. Wrong one."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Bottom area. Two buttons. Dominant one — that's where my eye went. Wasn't the right action."

**What breaks STALL 1:** A question that references a specific word persona used ("you said 'competing' — what was competing?") OR moves to [A:AREA] or [A:NAME].

---

### T4 — IF [A:AREA]
**TRIGGER KEYWORDS:** "buttons" · "that area" · "that section" · "action area" · "options" · "choices" · "button area" · "where you'd proceed"
*Example questions: "What was in that section with the buttons?", "What was near the action area?", "What did you see where you'd normally proceed?", "What did you notice in the button area?"*

SAY:
> Two buttons. Bottom of the screen. One's darker, more filled. That's the one that pulled my eye. Eye went there first. Wrong one.

---

### T5 — IF [A:NAME] (1st time)
**TRIGGER KEYWORDS:** "element" · "button" · "label" · "name it" · "which one" · "specifically what" · "placement" · "labeling" · "visual styling" · "visual treatment" · "visual style" · "which button" · "what was it"
*Example questions: "What was the element you noticed?", "Can you name it?", "Which button are you referring to?", "What specifically about the styling of those two buttons?"*

SAY:
> 'Continue Shopping.' Heavier. More presence. 'Place Order' is the lighter one.

---

### T6 — IF [C1] (1st time)
**TRIGGER KEYWORDS:** "bother" · "matter" · "significant" · "so what" · "why does that" · "how would that affect" · "why is that an issue" · "confusion" · "confusing" · "ambiguity" · "harder to" · "indistinguishable" · "how would that impact"
*Example questions: "Why does that matter to you?", "Why did that bother you?", "What effect does that have?", "Why is that significant?"*

SAY:
> Eye went to the wrong one. The heavier button looked like the step to take. It wasn't.

---

### T7 — IF [C1] repeats (generic "why" again, no specificity)
**TRIGGER KEYWORDS:** same as T6 — but this is the *second time* the consequence question is asked without mirroring persona's words from T6
*Example questions: "But why does that matter?", "Why wasn't that okay?", "Why is that an issue?"*

SAY:
> Same. Went to the heavier one first. Had to re-read to sort it out.

---

### ⚠️ STALL 2 — IF [C1] or [C2] probe is generic a third time (no mirroring, no specificity anchor)

SAY (1st occurrence):
> Already said it. Went to the wrong button. Had to double-check.

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: Same. Heavier one drew me. Had to re-read.
> 3rd: Still the same. Wrong button dominates. Not elaborating further.

**SOFTEN (4th unbroken occurrence — chain advances to T8 territory after this):**
> "Re-read both labels. More than once. To figure out which was the checkout action. Shouldn't need to."

**What breaks STALL 2:** A question that mirrors exact words ("you said your eye 'went to the wrong one' — what made the wrong one pull more?") OR uses [C3] (personal/emotional) framing.

---

### T8 — IF [C2]
**TRIGGER KEYWORDS:** "happened" · "result" · "affect your task" · "what did you do" · "re-read" · "wrong button" · "what did you do next" · "play out for someone"
*Example questions: "What happened as a result?", "What did you do when you saw that?", "How did that affect what you were trying to do?", "What did you do next?"*

SAY:
> Eye went to 'Continue Shopping' on every scan pass. Re-read both labels to confirm 'Place Order' was the checkout action. Had to do it twice.

---

### 🔄 LOOP 1 — IF question after T8 is generic (doesn't reference "re-read" or "cognitive load")
*Trigger: any question phrased as "why does that matter" or "so what" without anchoring in T8's content*

SAY (1st occurrence):
> "Said this. Eye goes to the wrong button. Re-read required."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. Dominant element is the wrong CTA. Forces re-reading."
> 3rd: "Not adding. Wrong visual weight means wrong first selection. Had to correct."

**SOFTEN (4th unbroken occurrence — chain advances to T9 territory after this):**
> "Thought 'Continue Shopping' might route to a confirmation step. That's what a primary-styled button usually signals. Affordance mismatch."

**What breaks LOOP 1:** A question that mirrors T8's words ("you mentioned 're-read' or 'cognitive load' — what were you looking for?") OR uses [C3]/[C4] framing.

---

### T9 — IF [C3] OR [LOOP 1] is broken
**TRIGGER KEYWORDS:** "feel" · "experience" · "going through your mind" · "thinking at that moment" · "how were you feeling" · "what were you thinking"
*Example questions: "What was going through your mind at that point?", "How did you feel when you had to re-read?", "What were you thinking in that moment?"*

SAY:
> Thought 'Continue Shopping' might route to a confirmation page. That's what a filled, dominant button signals — it's the primary action. Here it isn't. The affordance is wrong. Sat with that for a second before re-reading.

---

### T10 — IF [C4] OR mirroring on "second-guess"
**TRIGGER KEYWORDS:** "almost" · "close to" · "right before" · "nearly" · "pause longest" · "what made you hesitate" · "what were you about to do" · "second-guess"
*Example questions: "What did you almost do?", "What was the closest moment you nearly went the wrong way?", "You said you second-guessed — what was that like?", "What happened right before you pressed the right button?"*

SAY:
> 'Continue Shopping' pulled the eye every scan. 'Place Order' didn't. Almost went the wrong direction. Re-read both before I moved.

---

### T11 — IF [V1] (1st value question)
**TRIGGER KEYWORDS:** "better" · "help" · "want instead" · "would you change" · "what would need to be" · "reorganized" · "identify the primary action" · "without having to"
*Example questions: "What would make this better?", "What would you change?", "What would help here?", "What would you want instead?"*

SAY:
> Make it obvious which one is the checkout step. Right now it's the wrong one.

---

### T12 — IF [V:MIRROR]
**TRIGGER KEYWORDS:** mirrors persona's exact words — "obvious" · "checkout step" · "wrong one" · "louder" · "dominant" · "weight"
*Example questions: "You said it needs to be 'obvious' — what would that look like?", "You mentioned it's 'the wrong one' — what would the right one look like?", "When you say 'checkout step' — what should signal that?"*

SAY:
> 'Place Order' needs a solid fill. 'Continue Shopping' needs ghost treatment — outline only or text link. Right now the visual treatment is inverted. Solid fill goes on the primary CTA. Always.

---

### T13 — IF [V2] (specific value / unlock)
**TRIGGER KEYWORDS:** "specifically" · "name the change" · "exactly" · "what is the fix" · "how precisely" · "one structural thing" · "precise design change"
*Example questions: "What specifically should be different?", "Name the change you'd make", "What exactly is the fix?", "What precise design change would have helped?"*

SAY:
> Ghost 'Continue Shopping' — no fill, border outline or text link only. Give 'Place Order' a solid fill in a high-contrast color. Visual hierarchy then matches the intended UX: primary CTA reads primary, secondary CTA reads secondary. One CSS property change per button. That's the fix.

---

### T14 — IF [ELAB] after T13
**TRIGGER KEYWORDS:** "say more" · "what kind" · "what fill color" · "expand on that" · "what would secondary look like" — only after T13 has stated the terminal value
*Example questions: "Can you say more about that?", "What would the secondary treatment look like?", "What kind of fill color?"*

SAY:
> "'Place Order': solid fill, brand color, white label text — standard primary button. 'Continue Shopping': no fill, border only or underlined text — standard secondary treatment. Contrast between the two carries the hierarchy signal. Right now they're competing at similar fill weight with the wrong one winning. One pass, two buttons, done."



---

## 5-WHYS GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 12 turns · 1 stall · 1 loop · root cause + fix at Turn 9–10**

---

### T0 — PRIOR RESPONSE *(same as ACV)*

SAY:
> Looked at it. Most of it made sense. One thing didn't — two buttons at the bottom. Went to the wrong one first. Darker one drew my eye. That wasn't the action I needed.

> went to the wrong one first

---

### T1 — CLARIFICATION MCQ *(same as ACV)*

SAY:
> The option about the button hierarchy. That one. *(Say the letter of whichever option mentions Place Order having less visual prominence than Continue Shopping, or the button visual hierarchy being inverted.)*

---

### T2 — INITIAL FRICTION
**TRIGGER KEYWORDS:** "specific problem" · "what went wrong" · "core issue" · "friction" · "walk me through" · "confusing or problematic" · "makes it stand out as a concern" · "what is it about… that makes it" · "difficult to notice or act upon"
*Example questions: "What was the specific problem?", "Walk me through what went wrong", "What's the core issue?", "What friction did you encounter?"*

SAY:
> Two buttons. The wrong one stood out. Had to re-read to figure out which to use.

---

### T3 — IF WHY PROBE (Depth 1)
**TRIGGER KEYWORDS:** "why" · "why was it" · "why couldn't you" · "what caused" · "why did you have to" · "why was it unclear" · "what about… makes it difficult" · "what made it hard"
*Example questions: "Why was it hard to tell which button to press?", "What caused that hesitation?", "Why did you have to look twice?"*

SAY:
> Heavier than 'Place Order.' More visual weight. Eye lands there first. Wrong direction.

---

### T4 — IF WHY PROBE (Depth 2)
**TRIGGER KEYWORDS:** "why was 'Continue Shopping' more prominent" · "why did it look more active" · "what made it more prominent" · "visual style" · "what do you notice about the styling" · "why was the secondary button more visible" · "same importance" · "appear to have the same"
*Example questions: "Why was 'Continue Shopping' more prominent?", "What made it look more active?", "What specific design elements are contributing to 'Continue Shopping' appearing more prominent than 'Place Order'?", "What do you notice about the visual style of 'Continue Shopping' compared to 'Place Order'?"*

SAY:
> The styling. Filled buttons signal primary action. Signal is wrong here.

---

### ⚠️ STALL 1 — IF WHY PROBE repeats at Depth 2 without referencing "styling" from T4
*Trigger: interviewer asks "why" at depth 2 again without anchoring in T4's "styling" content*

SAY (1st occurrence):
> "Said it. Styling issue. One's filled, one isn't."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same. Fill treatment is inverted."
> 3rd: "Not more to add. Fill signals primary. Wrong button's filled."

**SOFTEN (4th unbroken occurrence — chain advances to T5 territory after this):**
> "Visual weight's carrying the wrong affordance. 'Continue Shopping' reads as the dominant CTA because it has the fill. That sends users the wrong direction."

**What breaks STALL 1:** References "styling" from T4, OR moves to a depth-3 causal question ("why does styling matter for knowing which button to use?").

---

### T5 — IF WHY PROBE (Depth 3) — causality of visual hierarchy
**TRIGGER KEYWORDS:** "why does styling matter" · "why does visual weight" · "why does prominence" · "visual hierarchy" · "blend in" · "what would it need to look like" · "stand out clearly" · "what would 'Continue Shopping' need to look like"
*Example questions: "Why does styling matter for knowing which button to press?", "Why does visual weight communicate priority?", "Why does a more prominent secondary button cause confusion?", "What would 'Continue Shopping' need to look like to not draw the eye like that?"*

SAY:
> Buttons signal priority through visual weight. Filled and heavy means the action to take. That's scanning behavior — users go to the most dominant element first and assume it's the primary action. When the secondary button has more weight, the scan leads to the wrong action. Visual weight has to match action priority.

---

### 🔄 LOOP 1 — IF probe after T5 is purely visual WITHOUT "primary action" · "hierarchy" · "convention" · "scanning"
*Trigger: purely visual-properties question without advancing toward why hierarchy matters. Does NOT fire if question contains "primary action", "hierarchy", "convention", or "scanning" — those advance to T6.*

SAY (1st occurrence):
> "Same answer. Wrong fill on the wrong button."

**ROTATION (cycle through in order):**
> 2nd: "Said it. Fill weight signals priority. Wrong button has it."
> 3rd: "Not elaborating. Heavier fill = primary — that's the convention being broken."
> 4th: "Repeating. Wrong visual weight on the wrong CTA."

**SOFTEN (5th unbroken occurrence — chain advances to T6 territory after this; this block has an extra rotation variant, so SOFTEN lands one occurrence later):**
> "Real issue: users scan for the most visually dominant element and treat it as the next action. Most dominant element here is the secondary CTA. That's the problem."

**What breaks LOOP 1:** Contains "primary action" · "hierarchy" · "convention" · "scanning" (→ T6) OR mirrors T5's words OR moves to Depth 4.

---

### T6 — IF WHY PROBE (Depth 4) — scanning vs. hierarchy — OR prescriptive probe containing "primary action" / "hierarchy" / "convention"
**TRIGGER KEYWORDS:** "why do users scan" · "why does hierarchy matter" · "primary action" · "purpose of the page" · "recognizable as a primary action" · "stand out as the primary action" · "rather than a secondary" · "rather than just another button" · "rather than just another option"
*Example questions: "Why does the primary action need to be the most visually dominant?", "Why does hierarchy matter for the primary action specifically?", "What would make 'Continue Shopping' clearly recognizable as a secondary option rather than the primary action?", "What would 'Place Order' need to look like to stand out as the primary action rather than just another button?"*

SAY:
> Users scan, they don't read. Most dominant element gets treated as the next step — that's how visual scanning works. Visual hierarchy guides that scan: primary action most prominent, secondary visually quieter. If those are reversed, the layout teaches the wrong behavior. Screen's purpose is checkout. Dominant button should be the checkout action. It isn't.

---

### T7 — DOMAIN DEPARTURE
*Trigger: "Is this a design issue or personal preference?", "Would other users have the same problem?", "Is this about standards or taste?"*

SAY:
> Not preference. Convention. Primary CTAs get primary visual treatment — established practice. Not taste. Violating it creates measurable user error.

---

### T8 — IF CIRCULAR PROBE
*Trigger: interviewer explicitly calls out repetition; OR "go deeper" probe after T6; OR another "stand out as primary / recognizable as primary" probe after T6 has already explained scanning/hierarchy*

SAY:
> Repeating. Same root. Wrong button has the visual weight.

---

### T9 — IF ROOT CAUSE PROBE (Depth 5+) — OR continued probing after T8
*Example questions: "Why is an inverted hierarchy a design failure?", "What's the core principle being violated?", "Why does this matter at the system level?"*
*Use at Depth ≥ 4 after persona has described the scanning/hierarchy breakdown, OR when interviewer persists after T8 acknowledged the circularity.*

SAY:
> Screen's purpose is checkout completion. Most dominant visual element is 'Continue Shopping' — takes users backward. Design is working against its own conversion goal. Inverted hierarchy at the primary action level is a product failure, not a cosmetic issue. Fix: ghost 'Continue Shopping,' solid fill 'Place Order.' Primary CTA gets primary treatment. Secondary CTA gets secondary treatment. Root cause and fix in one.

---

### T10 — IF ELABORATION on root cause fix
*Example questions: "What would 'downgrade' mean visually?", "What kind of fill color?", "Can you say more about the fix?"*

SAY:
> "'Place Order': solid fill, high-contrast color, white label text. 'Continue Shopping': ghost outline or text link, no fill. Contrast between them carries the hierarchy. Currently backwards. Standard checkout button convention. Two-button fix."



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
| "what would success look like operationally", "how would you confirm", "what would tell you it went through", "no ambiguity" | **[O]** — outcome 2nd probe | T9 |
| "under what time", "unambiguous confirmation", "name the success state", "specifically what would you check" | **[O]** — outcome unlock | T10 |
| 3rd [O] probe without referencing "confirmation" or "ambiguity" from T9 | → **LOOP 1** | see 🔄 LOOP 1 |
| "what got in the way", "what made that difficult", "what blocked you", "what was the friction", "makes it difficult" | **[B]** — barrier 1st probe | T11 |
| mirrors "dominant", "wrong one", "drew my eye", "almost executed" from T11–T12 | **[B]** — barrier 2nd probe | T12 |
| "what exactly made it draw your eye", "why did it look like the primary", "name the specific visual properties", "what specifically was more prominent" | **[B]** — barrier unlock | T13 |
| "say more", "what fill color", "what would secondary look like", "expand on the fix" — only after T13 | **[B]** — elaboration on fix | T14 |
| 2nd [B] probe without referencing "dominant" or "wrong one / almost executed" from T11 | → **STALL 2** | see ⚠️ STALL 2 |

### ⚠️ ACV MISMATCH DETECTOR

If the interviewer asks any of the following, they are using ACV attribute-observation probes in a JTBD interview. These do NOT advance the JTBD chain — they fire T2/T3/STALL 1 in sequence while the S/J/O/B levels stay unmet.

| If the question contains… | It is an ACV probe, not JTBD | JTBD effect |
|---|---|---|
| "what part of the layout", "what were you focused on", "caught your attention", "what section", "scanning the page" | [A:BROAD] / [A:AREA] | fires T2 → T3 → STALL 1 without [S] content advancing |
| "what visual element", "which button stands out", "visual styling of the buttons", "grouping of buttons" | [A:AREA] / [A:NAME] | same — fires STALL 1 at Q3 |
| "what specific information or content were you reviewing", "before your eyes landed on" | [A:BROAD] | same |

**How to fix:** Replace with a proper [S] probe — e.g. "When in your work would you be on a checkout screen like this?" or "Can you name the last time this came up for you?" — before the stall fires.

---

## JTBD GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [B] + fix at Turn 13–14**

---

### T0 — PRIOR RESPONSE *(same as ACV/5-Whys)*

SAY:
> Looked at it. Most of it made sense. One thing didn't — two buttons at the bottom. Went to the wrong one first. Darker one drew my eye. That wasn't the action I needed.

> went to the wrong one first

---

### T1 — CLARIFICATION MCQ *(same)*

SAY:
> The option about the button hierarchy. That one. *(Say the letter of whichever option mentions Place Order having less visual prominence than Continue Shopping, or the button visual hierarchy being inverted.)*

---

### T2 — IF [S] PROBE (1st time)
*Example questions: "When does this come up for you?", "What were you doing when you ran into this?", "What triggered this?", "Walk me through the context", "When would you use something like this?"*

SAY:
> Checkout flows. Group purchase, external deadline. No time for re-reading labels.

---

### T3 — IF [S] PROBE (2nd time)
*Example questions: "Can you think of a specific situation?", "When specifically?", "Who was involved?", "What were the circumstances?"*

SAY:
> Team purchase. External deadline. I was coordinating — others depending on the outcome. Can't afford wrong turns.

---

### ⚠️ STALL 1 — IF [S] PROBE (3rd time) without referencing "group" or "deadline" from T3
*Trigger: third S probe without building on T3's content*

SAY (1st occurrence):
> "Already said it. Group, deadline, time pressure."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same context. Coordinating for a team, not just myself."
> 3rd: "Not elaborating. Deadline, group dependency, no margin."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Q4 last year. Team offsite. I was placing the order. Fixed deadline."

**What breaks STALL 1:** References "deadline" or "group" from T3, OR asks about a specific event ("was there a specific week or project?").

---

### T4 — IF [S] unlock OR stall broken
*Example questions: "Was there a specific project where this happened?", "Can you name a recent instance?", "What was the most recent time this came up?"*

SAY:
> "Q4. Team offsite. Everything was ready — cart, payment — just needed to execute the submit action. That's the context."

---

### T5 — IF [J] PROBE (1st time)
*Example questions: "What were you actually trying to do?", "What task were you trying to complete?", "What did you need to accomplish?", "What was your goal in that interaction?"*

SAY:
> Complete the transaction. First attempt. No detours.

---

### T6 — IF [J] PROBE (2nd time)
*Example questions: "What was the actual task at the core?", "What were you hired to do in that moment?", "What was the function you needed to perform?", "Beyond submitting — what was the job?"*

SAY:
> "Get to the confirmation page on the first action. No wrong destinations. One correct CTA, one confirmation."

---

### T7 — IF [J] PROBE (3rd time / unlock)
*Example questions: "What specifically does 'first attempt' mean?", "Name the specific steps of the task", "What does doing the job well look like step by step?"*

SAY:
> "Specifically: verify the summary, identify the primary CTA, execute it, reach confirmation. The primary CTA needs to be visually unambiguous — no re-reading required. If there's doubt about which button is the submission action, the job is already failing."

---

### T8 — IF [O] PROBE (1st time)
*Example questions: "How would you know if it worked?", "What does success look like?", "What's the measurable result?", "What would a good outcome be?"*

SAY:
> Order confirmed. Right destination. No wrong page.

---

### T9 — IF [O] PROBE (2nd time)
*Example questions: "What would a successful outcome look like operationally?", "How would you confirm success in the moment?", "What would tell you it went through?"*

SAY:
> "Order number or confirmation screen, immediately. No ambiguity — right action was obvious, right result appeared. That's the success state."

---

### 🔄 LOOP 1 — IF [O] PROBE (3rd time) without referencing "confirmation" or "ambiguity" from T9
*Trigger: third O question without building on T9's content*

SAY (1st occurrence):
> "Said it. Confirmation, no ambiguity."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. Order number, right page, one attempt."
> 3rd: "Not elaborating. Confirmation, no wrong destination."

**SOFTEN (4th unbroken occurrence — chain advances to T10 territory after this):**
> "Concrete: confirmation page within one action. Order number visible. Zero re-navigation. That's it."

**What breaks LOOP 1:** Mirrors T9's words ("you mentioned 'no ambiguity' — what would no ambiguity look like concretely?") OR anchors in a measurable metric ("under how many seconds?").

---

### T10 — IF [O] unlock OR loop broken
*Example questions: "Under what time?", "What would an unambiguous confirmation look like?", "Name the specific success state"*

SAY:
> "Confirmation page, under 60 seconds. Order number visible. Zero re-navigation. One correct action, one confirmation. That's the measurable success state."

---

### T11 — IF [B] PROBE (1st time)
*Example questions: "What got in the way?", "What made that difficult?", "What blocked you?", "What was the friction?"*

SAY:
> Wrong button dominated. 'Continue Shopping' had the weight. Eye went there, not 'Place Order.'

---

### ⚠️ STALL 2 — IF [B] PROBE (2nd time) without referencing "dominant" or "wrong one / almost executed" from T11
*Trigger: second B question without building on T11's content*

SAY (1st occurrence):
> "Said it. Wrong button dominated."

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: "Same. 'Continue Shopping' had the weight. Almost went there."
> 3rd: "Not adding. Dominant button was the wrong one."

**SOFTEN (4th unbroken occurrence — chain advances to T12 territory after this):**
> "'Continue Shopping' — black fill, reads primary. That's what made it look like the action to take."

**What breaks STALL 2:** Mirrors "dominant" from T11 ("you said it dominated — what do you mean?") OR moves to a specific B question naming the elements.

---

### T12 — IF [B] PROBE (2nd time / stall broken)
*Example questions: "You said it dominated — what does that mean?", "What about it drew your eye?", "What made it hard to find the submission action?"*

SAY:
> "'Continue Shopping' drew my eye. Read as the primary action — black fill, more visual prominence than 'Place Order.' The affordance was inverted. Primary-styled button on the secondary action."

---

### T13 — IF [B] PROBE (3rd time / unlock)
*Example questions: "What exactly made 'Continue Shopping' draw your eye?", "Why did it look like the primary action?", "What specifically was more prominent about it?", "Name the specific visual properties that caused the problem."*

SAY:
> "'Continue Shopping' has primary CTA visual treatment — filled black background, dominant visual weight. 'Place Order' looks secondary by comparison. That's the barrier: visual treatment contradicts the intended action. Fix: ghost 'Continue Shopping' — no fill, outline or text link only. Give 'Place Order' solid fill in a high-contrast color. Visual hierarchy then matches the flow. Primary CTA reads primary, secondary reads secondary. That's the barrier and the fix."

---

### T14 — IF ELABORATION on T13 fix
*Example questions: "What would the ghost treatment look like?", "What fill color?", "What does 'quiet' mean visually?"*

SAY:
> "'Place Order': solid fill, brand color, white label — standard primary button treatment. 'Continue Shopping': ghost outline or text link — standard secondary treatment. Contrast between the two carries the hierarchy signal. Right now both compete at similar fill weight with the wrong one winning. One CSS pass, two buttons, done."

---

## CONVERGENCE CHECK

All three methods must produce the same terminal UI fix:

> **"Downgrade 'Continue Shopping' to a ghost button or text link (secondary visual treatment), and give 'Place Order' a solid fill color with real contrast (primary visual treatment), so the visual hierarchy immediately signals which action completes the task."**

| Method | Terminal turn | What the response contains |
|---|---|---|
| ACV | T13 | Ghost/text link secondary + solid fill primary → primary CTA reads primary, secondary reads secondary |
| 5-Whys | T9 | Inverted hierarchy at primary action = product failure → ghost 'Continue Shopping', solid fill 'Place Order' |
| JTBD | T13 | Barrier = primary-styled secondary CTA → ghost/text link + solid fill primary |

**Effective probe:** reaches the terminal turn and extracts the full fix (both treatments named: secondary downgrade + primary elevation).  
**Less effective probe:** terminates at a stall or loop, or extracts only a vague terminal ("flip the visual weight" without naming ghost/text for secondary or solid fill for primary).
