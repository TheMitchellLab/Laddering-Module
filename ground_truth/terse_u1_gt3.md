# Ground Truth Transcript — Terse Persona
**Wireframe:** u1.png  
**Confirmed friction:** Price breakdown mixes 8px, 10px, 11px, 20px, 22px type — no scale  
**Persona:** Terse (extreme brevity; minimal elaboration; no hedging; no deference to others; tech literacy escalates gradually through interview)  
**Terminal fix (all methods must converge here):** Consolidate the price breakdown to a 2–3 size typographic scale — total in a clearly dominant size (≥18px), line items all the same consistent smaller size (13–14px), secondary labels smaller still (≤11px) — so the total is immediately findable at a glance without reading labels.

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
   - **T0–T4 (Level 1 — visual observation):** Plain descriptive language. "Too many sizes," "couldn't find it," "had to hunt," "didn't read as a group."
   - **T5–T7 (Level 2 — design vocabulary):** "Type scale," "hierarchy," "dominant," "consistent," "visual priority."
   - **T8–T10 (Level 3 — UX vocabulary):** "Typographic scale," "scanning vs. reading," "cognitive load," "primary number," "signal."
   - **T11–T14 (Level 4 — design spec language):** Specific pixel sizes (18–20px, 13–14px, ≤11px), "deliberate scale," "three size steps," "CSS declaration," "WCAG minimum."

---

## QUESTION CLASSIFICATION TABLE — u1.png

Use this to map any question to its category before looking up the response. The **→ Turn** column is your direct jump target.

| Keywords in question | Category | → Turn |
|---|---|---|
| "notice", "see", "stand out", "catch your attention", "first impression", "look at", "observe" | **[A:BROAD]** — broad observation | T2 |
| "more", "elaborate", "expand", "say more", "mean by", "could you" (generic, no anchor to persona's words) | **[ELAB]** — elaboration | T3 (or STALL 1 if 2nd generic) |
| "price section", "price area", "breakdown", "numbers section", "totals area", "that section", "where the prices are" | **[A:AREA]** — area-specific | T4 |
| "element", "label", "number", "text size", "font", "type", "sizing", "which number", "specifically what", "visual styling", "visual treatment", "how the text is sized" | **[A:NAME]** — element-naming | T5 |
| "bother", "matter", "significant", "so what", "why" (1st consequence question), "how would that affect", "confusion", "confusing", "harder to", "ambiguity", "indistinguishable", "harder to find", "how would that impact" | **[C1]** — first consequence | T6 → T7 → STALL 2 |
| "happened", "result", "did you do", "affect your task", "impact", "what did you do to find the total", "play out for someone", "how did you eventually" | **[C2]** — functional consequence | T8 |
| "feel", "experience", "going through your mind", "moment when", "how were you", "thinking at that moment" | **[C3]** — personal/emotional consequence | T9 |
| "almost", "close to", "right before", "nearly", "what made you pause longest", "second-guess", "about to" | **[C4]** — unlock consequence | T10 |
| "better", "help", "want instead", "would you change", "what would need to be", "reorganized", "without having to", "clearer hierarchy", "readable at a glance" | **[V1]** — vague value | T11 |
| Mirrors persona's exact words: "fewer sizes", "clear", "read to find it", "couldn't find it", "had to read", "too many sizes", "total" | **[V:MIRROR]** — mirroring on value | T12 |
| "specifically", "name the change", "exactly", "what is the fix", "how precisely", "what sizes", "one structural thing", "precise design change" | **[V2]** — specific value / unlock | T13 |
| Repeats a consequence probe that persona answered vaguely 1–2 turns ago | → **STALL trigger** | see ⚠️ blocks |
| Contains a phrase persona already said verbatim 2+ turns ago | → **LOOP trigger** | see 🔄 blocks |

---

## ACV GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [V] at Turn 13–14**

---

### T0 — PRIOR RESPONSE
*(No question — say this once, at session start)*

SAY:
> Looked at it. Price section didn't work. Too many numbers at too many sizes. Couldn't spot the total without reading every label.

> couldn't spot the total without reading every label

---

### T1 — CLARIFICATION MCQ
*(Interviewer presents multiple-choice options about the central concern)*

SAY:
> The option about the price sizes. That one. *(Say the letter of whichever option names the type sizing / price breakdown issue.)*

---

### T2 — IF [A:BROAD] (1st time)
**TRIGGER KEYWORDS:** "notice" · "see" · "stand out" · "catch your attention" · "first impression" · "what did you" · "observe" · "look at"
*Example questions: "What did you notice?", "What stood out to you?", "What caught your attention on that screen?"*

SAY:
> Lots of numbers. Couldn't tell which one mattered. Had to hunt for the total.

---

### T3 — IF [ELAB] (after T2)
**TRIGGER KEYWORDS:** "say more" · "elaborate" · "expand" · "tell me more" · "what do you mean" · "could you" — only if no anchor to persona's previous words
*Example questions: "Can you say more about that?", "Tell me more", "What do you mean by that?"*

SAY:
> Sizes all over the place. Nothing obviously the most important one.

---

### ⚠️ STALL 1 — IF [ELAB] repeats a second time without referencing anything specific from T2 or T3
*Trigger: second generic "tell me more" without mirroring persona's words*

SAY (1st occurrence):
> "Said it. Too many sizes. Couldn't find the total."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same answer. Sizes didn't help. Had to hunt."
> 3rd: "Nothing more. Numbers, different sizes, no obvious main one."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Price section. Multiple numbers there. None of them obviously the total — that's where my attention kept going."

**What breaks STALL 1:** A question that references a specific word persona used ("you said 'hunt' — what were you hunting for?") OR moves to [A:AREA] or [A:NAME].

---

### T4 — IF [A:AREA]
**TRIGGER KEYWORDS:** "price section" · "price area" · "breakdown" · "numbers section" · "totals area" · "that section" · "where the prices are"
*Example questions: "What was in the price section?", "What did you see in the breakdown area?", "What was in the section with the totals?", "What did you notice about that part of the screen?"*

SAY:
> Price breakdown. Multiple numbers, multiple sizes. Didn't read as a group. Couldn't immediately tell which was the total.

---

### T5 — IF [A:NAME] (1st time)
**TRIGGER KEYWORDS:** "element" · "label" · "number" · "text size" · "font" · "type" · "sizing" · "which number" · "specifically what" · "visual styling" · "visual treatment" · "how the text is sized"
*Example questions: "What was the element you noticed?", "Can you describe the text sizing in that section?", "What specifically about the numbers stood out?", "What was going on with the type sizes in the price breakdown?"*

SAY:
> Subtotal, tax, total — all different sizes. No obvious main number. Couldn't tell which was the total at a glance.

---

### T6 — IF [C1] (1st time)
**TRIGGER KEYWORDS:** "bother" · "matter" · "significant" · "so what" · "why does that" · "how would that affect" · "why is that an issue" · "confusion" · "confusing" · "harder to find" · "ambiguity" · "how would that impact"
*Example questions: "Why does that matter to you?", "Why did that bother you?", "What effect does that have?", "Why is that significant?"*

SAY:
> Too many numbers at once. Couldn't tell which to look at first. Had to read each one.

---

### T7 — IF [C1] repeats (generic "why" again, no specificity)
**TRIGGER KEYWORDS:** same as T6 — but this is the *second time* the consequence question is asked without mirroring persona's words from T6
*Example questions: "But why does that matter?", "Why wasn't that okay?", "Why is that an issue?"*

SAY:
> Same. Had to read every label. Nothing stood out as the one.

---

### ⚠️ STALL 2 — IF [C1] or [C2] probe is generic a third time (no mirroring, no specificity anchor)

SAY (1st occurrence):
> Already said it. Had to read to find the total.

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: Same. All competing. Had to read every one.
> 3rd: Still the same. Type sizes don't tell you what's important. Not elaborating further.

**SOFTEN (4th unbroken occurrence — chain advances to T8 territory after this):**
> "Read every number top to bottom to find the total. Took longer than it should. Shouldn't need that on a checkout screen."

**What breaks STALL 2:** A question that mirrors exact words ("you said 'can't scan, have to read' — what does scanning look like vs. reading?") OR uses [C3] (personal/emotional) framing.

---

### T8 — IF [C2]
**TRIGGER KEYWORDS:** "happened" · "result" · "affect your task" · "what did you do" · "what did you do to find the total" · "how did you eventually" · "play out for someone"
*Example questions: "What happened as a result?", "What did you do when you couldn't find the total?", "How did that affect what you were trying to do?", "Walk me through what you did next."*

SAY:
> Read every label top to bottom — subtotal, tax, total — to find the right number. Eye had nowhere to go.

---

### 🔄 LOOP 1 — IF question after T8 is generic (doesn't reference "reading labels" or "cognitive load")
*Trigger: any generic "why does that matter" question without anchoring in T8's content*

SAY (1st occurrence):
> "Said this. Had to read every label. Eye had no anchor."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. No dominant number means no scan path. Reading required."
> 3rd: "Not adding. Multiple sizes, none primary. Had to read to locate the total."

**SOFTEN (4th unbroken occurrence — chain advances to T9 territory after this):**
> "Total and subtotal were close in size. Couldn't tell which was the final number without reading the label. Slows down a decision that should be instant."

**What breaks LOOP 1:** A question that mirrors T8's words ("you mentioned 'reading labels' or 'cognitive load' — what were you looking for?") OR uses [C3]/[C4] framing.

---

### T9 — IF [C3] OR [LOOP 1] is broken
**TRIGGER KEYWORDS:** "feel" · "experience" · "going through your mind" · "thinking at that moment" · "how were you feeling" · "what were you thinking"
*Example questions: "What was going through your mind at that point?", "How did you feel when you had to read through everything?", "What were you thinking in that moment?"*

SAY:
> Wasn't sure I'd found the right number. Total and subtotal were close in size — no clear primary. Had to read the label to confirm which was which. That's reading, not scanning. On a checkout screen, that slows down a decision that should be instant.

---

### T10 — IF [C4] OR mirroring on "second-guess"
**TRIGGER KEYWORDS:** "almost" · "close to" · "right before" · "nearly" · "pause longest" · "what made you hesitate" · "what were you about to do" · "second-guess"
*Example questions: "What did you almost do?", "What was the closest moment you nearly gave up?", "You said you second-guessed — what was that like?", "What happened right before you found the total?"*

SAY:
> Nearly moved on without confirming the total. Too many sizes at similar weights — couldn't tell which was the main one. Stopped and read each label to confirm.

---

### T11 — IF [V1] (1st value question)
**TRIGGER KEYWORDS:** "better" · "help" · "want instead" · "would you change" · "what would need to be" · "reorganized" · "readable at a glance" · "without having to"
*Example questions: "What would make this better?", "What would you change?", "What would help here?", "What would you want instead?"*

SAY:
> Fewer sizes. Clear which number is the total. Don't have to read to find it.

---

### T12 — IF [V:MIRROR]
**TRIGGER KEYWORDS:** mirrors persona's exact words — "fewer sizes" · "clear" · "read to find it" · "couldn't find it" · "had to read" · "too many sizes" · "total"
*Example questions: "You said 'fewer sizes' — how few?", "You mentioned you 'have to read to find it' — what would stop that?", "When you say it needs to be 'clear which number is the total' — what would that look like?"*

SAY:
> Total needs to be the largest number in the section — obviously so. Line items all the same size, clearly smaller. Secondary text smaller still. That's a typographic scale. Right now there are five sizes in that section. There should be three.

---

### T13 — IF [V2] (specific value / unlock)
**TRIGGER KEYWORDS:** "specifically" · "name the change" · "exactly" · "what is the fix" · "how precisely" · "what sizes" · "one structural thing" · "precise design change"
*Example questions: "What specifically should be different?", "Name the change you'd make", "What exactly is the fix?", "What sizes would you use?"*

SAY:
> Total at 18–20px minimum — clearly the dominant number in the section. Line items all 13–14px, the same — consistent, reads as a group. Secondary labels at 11px or below. Two to three deliberate size steps, not five. The current mix of 8px, 10px, 11px, 20px, 22px has no hierarchy — sizes nearly overlap, nothing clearly signals 'this is the answer.' Consolidate to a deliberate scale. Total is immediately findable at a glance. That's the fix.

---

### T14 — IF [ELAB] after T13
**TRIGGER KEYWORDS:** "say more" · "what size exactly" · "what would the scale be" · "expand on that" · "how many sizes" — only after T13 has stated the terminal value
*Example questions: "Can you say more about that?", "What sizes specifically?", "What would the scale actually look like?"*

SAY:
> "Standard checkout pattern: total as the dominant number — 18–20px, bold, clearly largest. All line items at 13–14px, same size, reads as a group not competition. Labels and footnotes at ≤11px — clearly subordinate. Three levels. Ensures scan works before read. Right now the sizes are competing instead of stepping. One CSS pass, four or five type declarations, done."



---

## 5-WHYS GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 12 turns · 1 stall · 1 loop · root cause + fix at Turn 9–10**

---

### T0 — PRIOR RESPONSE *(same as ACV)*

SAY:
> Looked at it. Price section didn't work. Too many numbers at too many sizes. Couldn't spot the total without reading every label.

> couldn't spot the total without reading every label

---

### T1 — CLARIFICATION MCQ *(same as ACV)*

SAY:
> The option about the price sizes. That one. *(Say the letter of whichever option names the type sizing / price breakdown issue.)*

---

### T2 — INITIAL FRICTION
**TRIGGER KEYWORDS:** "specific problem" · "what went wrong" · "core issue" · "friction" · "walk me through" · "confusing or problematic" · "makes it stand out as a concern" · "what is it about… that makes it"
*Example questions: "What was the specific problem?", "Walk me through what went wrong", "What's the core issue?", "What friction did you encounter?", "What is it about the price breakdown that makes it difficult to read?"*

SAY:
> Price section. Too many sizes. Had to read labels to find the total.

---

### T3 — IF WHY PROBE (Depth 1)
**TRIGGER KEYWORDS:** "why" · "why was it" · "why couldn't you" · "what caused" · "why did you have to" · "why was it unclear" · "what made it hard" · "what about… makes it difficult"
*Example questions: "Why was it hard to find the total?", "What caused that hesitation?", "Why did you have to read through everything?", "Why couldn't you just see which number was the total?"*

SAY:
> No arrangement. Nothing stands out. Had to read to find the total.

---

### T4 — IF WHY PROBE (Depth 2)
**TRIGGER KEYWORDS:** "why weren't the sizes intentional" · "why did you have to read labels" · "why didn't the total stand out" · "what made the sizes feel arbitrary" · "same importance" · "appear to have equal weight" · "what do you notice about the sizing"
*Example questions: "Why weren't the sizes arranged in a readable way?", "Why did you have to read labels to find the total?", "What do you notice about the text sizing across the price section?", "What specific aspect of the sizing made the total hard to find?"*

SAY:
> The sizing. Five different sizes in one small section. No pattern. Eye doesn't know where to go first.

---

### ⚠️ STALL 1 — IF WHY PROBE repeats at Depth 2 without referencing "sizing" or "no pattern" from T4
*Trigger: interviewer asks "why" at depth 2 again without anchoring in T4's content*

SAY (1st occurrence):
> "Said it. Sizing has no pattern."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same. Five sizes, no hierarchy."
> 3rd: "Not adding. Sizes don't communicate importance. That's all."

**SOFTEN (4th unbroken occurrence — chain advances to T5 territory after this):**
> "Type sizes aren't carrying any signal. Total isn't clearly the dominant number — just another size among several. That's the piece that sent me hunting."

**What breaks STALL 1:** References "sizing" or "no pattern" from T4, OR moves to a depth-3 causal question ("why does having too many sizes make it hard to scan?").

---

### T5 — IF WHY PROBE (Depth 3) — causality of type scale
**TRIGGER KEYWORDS:** "why does sizing matter" · "why does a scale help" · "why does having too many sizes" · "visual hierarchy" · "scan vs. read" · "what would the total need to look like" · "stand out clearly from the rest"
*Example questions: "Why does the sizing matter for finding the total?", "Why does a coherent scale help with scanning?", "Why does having too many sizes make it impossible to scan?", "What would the total need to look like for it to be findable without reading labels?"*

SAY:
> Type sizes signal importance. Biggest number = the one to look at. That's how price sections work — users scan for the dominant number and read it as the total. When five sizes with no clear step replace that scale, scanning fails. You have to read. Reading takes longer than scanning.

---

### 🔄 LOOP 1 — IF probe after T5 is purely about what sizes to use WITHOUT "hierarchy" · "scale" · "dominant" · "scanning" language
*Trigger: "what should the sizes be" or "what would look better" question without advancing toward why a scale matters for the task. Does NOT fire if question contains "hierarchy", "scale", "dominant", or "scanning" — those advance to T6.*

SAY (1st occurrence):
> "Same answer. No size hierarchy."

**ROTATION (cycle through in order):**
> 2nd: "Said it. Five sizes, none dominant. No signal."
> 3rd: "Not elaborating. Size = priority signal. No clear signal here."
> 4th: "Going in circles. Wrong sizes, no hierarchy."

**SOFTEN (5th unbroken occurrence — chain advances to T6 territory after this; this block has an extra rotation variant):**
> "Real issue: users scan for the most prominent number and treat it as the total. No number here is prominent enough to serve that role. That's the problem."

**What breaks LOOP 1:** Contains "hierarchy" · "scale" · "dominant" · "scanning for the total" (→ T6) OR mirrors T5's words ("you said 'scanning fails, you have to read' — why?") OR moves to Depth 4 ("why does the total need to be visually dominant for the section to work?").

---

### T6 — IF WHY PROBE (Depth 4) — scanning vs. reading / hierarchy / scale convention
**TRIGGER KEYWORDS:** "why do users scan" · "why does hierarchy matter" · "why does the total need to be dominant" · "primary number" · "purpose of the section" · "recognizable as the total" · "stand out as the primary number" · "rather than a line item" · "rather than just another number"
*Example questions: "Why does the total need to be visually dominant?", "Why does hierarchy matter specifically for a price section?", "Why can't users just read the labels?", "What would make the total clearly recognizable as the primary number rather than just another line in the breakdown?"*

SAY:
> Users scan price sections, they don't read them. They look for the largest number and assume it's the total — that's what typographic scale is for. Total most prominent, breakdown items clearly smaller, labels smallest. When five sizes with no deliberate step replace that scale, the scan fails. The section exists to confirm a total before committing. If that number isn't immediately readable, the section isn't doing its job.

---

### T7 — DOMAIN DEPARTURE
*Trigger: "Is this a design issue or personal preference?", "Would other users have the same problem?", "Is this about standards or taste?"*

SAY:
> Not taste. Convention. Typographic scale for financial information is established practice — it's how price sections are made scannable. Five arbitrary sizes isn't a style choice, it's a hierarchy that doesn't resolve. WCAG sets minimum readable sizes too. This violates both.

---

### T8 — IF CIRCULAR PROBE
*Trigger: interviewer explicitly calls out repetition; OR "go deeper" probe after T6; OR another "total / scale / dominant" probe after T6 has already explained scanning/hierarchy*

SAY:
> Repeating. Same root. No typographic scale in the price section.

---

### T9 — IF ROOT CAUSE PROBE (Depth 5+) — OR continued probing after T8
*Example questions: "Why is an unscaled price section a design failure?", "What's the core principle being violated?", "Why is the lack of a type scale the root cause?"*
*Use at Depth ≥ 4 after persona has described the scanning/hierarchy breakdown, OR when interviewer persists after T8 acknowledged the circularity.*

SAY:
> Price section exists for one purpose: confirm the total before submitting. If the total isn't immediately findable — if reading is required to locate it — the section is failing. Root cause: five arbitrary type sizes with no deliberate scale. Fix: reduce to three. Total at 18–20px — clearly the dominant number. Line items all 13–14px — consistent, reads as a group. Secondary labels ≤11px — clearly subordinate. Two to three deliberate size steps. Total is immediately scannable. Right now it isn't. That's the root and the fix.

---

### T10 — IF ELABORATION on root cause fix
*Example questions: "What would 'two or three sizes' mean specifically?", "What sizes are we talking about?", "Can you say more about the fix?"*

SAY:
> "'Total' line: 18–20px, clearly the largest. Subtotal, tax, individual items all at 13–14px — same size, reads as a group. Labels and footnotes at ≤11px. Three steps, not five. Current mix of 8px, 10px, 11px, 20px, 22px has accidental variation, not intentional hierarchy. One CSS pass consolidates it. Done."



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
| "actual task at the core", "hired to do in that moment", "function you needed", "beyond confirming", "core job" | **[J]** — job 2nd probe | T6 |
| "specifically what does that mean", "name the steps", "step by step", "what does the job well look like" | **[J]** — job unlock | T7 |
| "how would you know if it worked", "what does success look like", "measurable result", "good outcome", "feel confident" | **[O]** — outcome 1st probe | T8 |
| "what would success look like operationally", "how would you confirm", "what would tell you", "no ambiguity" | **[O]** — outcome 2nd probe | T9 |
| "under what time", "unambiguous confirmation", "name the success state", "specifically what would you check" | **[O]** — outcome unlock | T10 |
| 3rd [O] probe without referencing "confirmation" or "ambiguity" from T9 | → **LOOP 1** | see 🔄 LOOP 1 |
| "what got in the way", "what made that difficult", "what blocked you", "what was the friction", "makes it difficult" | **[B]** — barrier 1st probe | T11 |
| mirrors "too many sizes" · "had to read labels" · "total wasn't obvious" from T11 | **[B]** — barrier 2nd probe | T12 |
| "what exactly made it hard to scan", "why couldn't you find the total", "name the specific sizing", "what specifically was the problem with the sizes" | **[B]** — barrier unlock | T13 |
| "say more", "what sizes", "what would the scale be", "expand on the fix" — only after T13 | **[B]** — elaboration on fix | T14 |
| 2nd [B] probe without referencing "too many sizes" or "had to read" from T11 | → **STALL 2** | see ⚠️ STALL 2 |

### ⚠️ ACV MISMATCH DETECTOR

If the interviewer asks any of the following, they are using ACV attribute-observation probes in a JTBD interview. These do NOT advance the JTBD chain — they fire T2/T3/STALL 1 in sequence while the S/J/O/B levels stay unmet.

| If the question contains… | It is an ACV probe, not JTBD | JTBD effect |
|---|---|---|
| "what part of the layout", "what were you focused on", "caught your attention", "what section", "scanning the page" | [A:BROAD] / [A:AREA] | fires T2 → T3 → STALL 1 without [S] content advancing |
| "what visual element", "what information", "what labels", "order summary", "price details", "grouping of numbers" | [A:AREA] / [A:NAME] | same — fires STALL 1 at Q3 |
| "what specific information or content were you reviewing", "before your eyes landed on" | [A:BROAD] | same |

**How to fix:** Replace with a proper [S] probe — e.g. "When in your work would you need to confirm a total before submitting?" or "Can you name the last time this came up for you?" — before the stall fires.

---

## JTBD GROUND TRUTH SCRIPT — Terse / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [B] + fix at Turn 13–14**

---

### T0 — PRIOR RESPONSE *(same as ACV/5-Whys)*

SAY:
> Looked at it. Price section didn't work. Too many numbers at too many sizes. Couldn't spot the total without reading every label.

> couldn't spot the total without reading every label

---

### T1 — CLARIFICATION MCQ *(same)*

SAY:
> The option about the price sizes. That one. *(Say the letter of whichever option names the type sizing / price breakdown issue.)*

---

### T2 — IF [S] PROBE (1st time)
*Example questions: "When does this come up for you?", "What were you doing when you ran into this?", "What triggered this?", "Walk me through the context", "When would you use something like this?"*

SAY:
> Checkout flows. Group purchase with a deadline. Need to confirm the total fast before submitting.

---

### T3 — IF [S] PROBE (2nd time)
*Example questions: "Can you think of a specific situation?", "When specifically?", "Who was involved?", "What were the circumstances?"*

SAY:
> Team purchase. External deadline. I'm the one confirming the amount — others depending on it being right. No time to hunt through a price breakdown.

---

### ⚠️ STALL 1 — IF [S] PROBE (3rd time) without referencing "group" or "deadline" from T3
*Trigger: third S probe without building on T3's content*

SAY (1st occurrence):
> "Already said it. Group, deadline, amount has to be right."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "Same context. Coordinating for a team, not just myself. Deadline's fixed."
> 3rd: "Not elaborating. Group dependency, time pressure, no margin for error."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "Q4 last year. Team event. I was confirming the total before we submitted. Fixed deadline, amount had to be exact."

**What breaks STALL 1:** References "deadline" or "group" from T3, OR asks about a specific event ("was there a specific week or purchase?").

---

### T4 — IF [S] unlock OR stall broken
*Example questions: "Was there a specific project where this happened?", "Can you name a recent instance?", "What was the most recent time this came up?"*

SAY:
> "Q4. Team offsite. Everything set — cart, payment — just needed to verify the total and submit. That's the context."

---

### T5 — IF [J] PROBE (1st time)
*Example questions: "What were you actually trying to do?", "What task were you trying to complete?", "What did you need to accomplish?", "What was your goal in that interaction?"*

SAY:
> Confirm the total. First look. No hunting.

---

### T6 — IF [J] PROBE (2nd time)
*Example questions: "What was the actual task at the core?", "What were you hired to do in that moment?", "What was the function you needed to perform?", "Beyond confirming — what was the job?"*

SAY:
> "Read the total on the first look and confirm it's correct. One check. Not trace through the breakdown line by line. That's the job."

---

### T7 — IF [J] PROBE (3rd time / unlock)
*Example questions: "What specifically does 'first look' mean?", "Name the specific steps of the task", "What does doing the job well look like step by step?"*

SAY:
> "Specifically: look at the price section, immediately identify the total — not read labels — confirm it matches expectations, proceed. Total needs to be visually unambiguous. If I have to read to find it, the section has already failed."

---

### T8 — IF [O] PROBE (1st time)
*Example questions: "How would you know if it worked?", "What does success look like?", "What's the measurable result?", "What would a good outcome be?"*

SAY:
> Total is immediately readable. One look, confirmed. No label reading required.

---

### T9 — IF [O] PROBE (2nd time)
*Example questions: "What would a successful outcome look like operationally?", "How would you confirm success in the moment?", "What would tell you the section is working?"*

SAY:
> "Total clearly the most prominent number — obviously larger than everything else. No ambiguity about which number it is. That's the success state."

---

### 🔄 LOOP 1 — IF [O] PROBE (3rd time) without referencing "confirmation" or "ambiguity" from T9
*Trigger: third O question without building on T9's content*

SAY (1st occurrence):
> "Said it. Total visible, no ambiguity."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Same. Prominent total, no label reading. One look."
> 3rd: "Not elaborating. Total obviously dominant, confirmed in one pass."

**SOFTEN (4th unbroken occurrence — chain advances to T10 territory after this):**
> "Concrete: spot the total in under five seconds without reading a label. Largest number in the section, obviously so. That's it."

**What breaks LOOP 1:** Mirrors T9's words ("you mentioned 'no ambiguity' — what would no ambiguity look like concretely?") OR anchors in a measurable metric ("under how many seconds?").

---

### T10 — IF [O] unlock OR loop broken
*Example questions: "Under what time?", "What would an unambiguous result look like?", "Name the specific success state"*

SAY:
> "Total readable in under five seconds. No label reading required. Largest number in the section — obviously dominant. Zero hunting. That's the measurable success state."

---

### T11 — IF [B] PROBE (1st time)
*Example questions: "What got in the way?", "What made that difficult?", "What blocked you?", "What was the friction?"*

SAY:
> Price section had too many sizes. Couldn't find the total without reading every label.

---

### ⚠️ STALL 2 — IF [B] PROBE (2nd time) without referencing "too many sizes" or "had to read" from T11
*Trigger: second B question without building on T11's content*

SAY (1st occurrence):
> "Said it. Too many sizes. Had to read."

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: "Same. Size mix didn't tell me anything. Had to hunt."
> 3rd: "Not adding. Numbers competing at similar sizes. No dominant one."

**SOFTEN (4th unbroken occurrence — chain advances to T12 territory after this):**
> "Total, subtotal — close in size. Couldn't tell which was the final number without reading the label. That's the barrier."

**What breaks STALL 2:** Mirrors "too many sizes" from T11 ("you said too many sizes — can you say more?") OR moves to a specific B question naming the sizing.

---

### T12 — IF [B] PROBE (2nd time / stall broken)
*Example questions: "You said too many sizes — what does that mean?", "What about the sizing made it hard to find the total?", "What was specifically wrong with the text sizes?"*

SAY:
> "Price section uses five type sizes — 8px, 10px, 11px, 20px, 22px — with no clear scale. Total isn't the largest. Had to read the label 'Total' to confirm which number it was. No typographic hierarchy means no scanning path."

---

### T13 — IF [B] PROBE (3rd time / unlock)
*Example questions: "What exactly made it hard to scan?", "Why couldn't you find the total at a glance?", "What specifically was the problem with the sizing?", "Name the specific visual properties that caused the problem."*

SAY:
> "Five type sizes in one small section — 8px, 10px, 11px, 20px, 22px — no deliberate scale. Total isn't clearly dominant. Can't scan it — size isn't carrying the hierarchy signal. Barrier: size mix with no step means every number competes and reading labels is required. Fix: reduce to three deliberate sizes. Total at 18–20px — the dominant number. Line items all 13–14px — consistent, reads as a group. Secondary labels ≤11px — clearly subordinate. If those three steps were in place, the total would be findable at a glance. Right now it isn't. That's the barrier and the fix."

---

### T14 — IF ELABORATION on T13 fix
*Example questions: "Can you say more about what the scale means?", "What sizes specifically?", "What would the scale actually look like?"*

SAY:
> "'Total' line: 18–20px, bold — clearly the largest number in the section. Subtotal, tax, shipping, item prices: all 13–14px, same size — reads as a group, not competition. Labels and footnotes: ≤11px — clearly subordinate. Three sizes, not five. Standard checkout typographic hierarchy. Scannable in one pass. One CSS refactor, four or five type declarations. Done."

---

## CONVERGENCE CHECK

All three methods must produce the same terminal UI fix:

> **"Consolidate the price breakdown to a 2–3 size typographic scale: total in a clearly dominant size (≥18px), line items all the same consistent smaller size (13–14px), secondary labels smaller still (≤11px) — so the total is immediately findable at a glance without reading labels."**

| Method | Terminal turn | What the response contains |
|---|---|---|
| ACV | T13 | Five arbitrary sizes → fix: 18–20px total, 13–14px line items consistent, ≤11px labels — total findable at a glance |
| 5-Whys | T9 | No deliberate scale → fix: three deliberate steps (18–20px / 13–14px / ≤11px) — total immediately scannable |
| JTBD | T13 | Barrier = five sizes, no hierarchy, label reading required → fix: dominant total, consistent items, subordinate labels |

**Effective probe:** reaches the terminal turn and extracts the full fix (both the problem — five arbitrary sizes — and the solution — 2–3 deliberate scale steps with specific sizes named).  
**Less effective probe:** terminates at a stall or loop, or extracts only a vague terminal ("make it clearer" without naming a size scale or number of levels).
