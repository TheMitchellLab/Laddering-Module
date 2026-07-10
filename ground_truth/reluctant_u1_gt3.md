# Ground Truth Transcript — Reluctant Persona
**Wireframe:** u1.png  
**Confirmed friction:** Price breakdown mixes 8px, 10px, 11px, 20px, 22px type — no scale  
**Persona:** Reluctant (deflects with vagueness, defers to others, avoids personal commitment)  
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
| Mirrors persona's exact words: "clearer", "obvious", "scale", "hierarchy", "total", "stand out", "same size", "different sizes", "organized", "at a glance", "labels" | **[V:MIRROR]** — mirroring on value | T12 |
| "specifically", "name the change", "exactly", "what is the fix", "how precisely", "what sizes", "one structural thing", "precise design change" | **[V2]** — specific value / unlock | T13 |
| Repeats a consequence probe that persona answered vaguely 1–2 turns ago | → **STALL trigger** | see ⚠️ blocks |
| Contains a phrase persona already said verbatim 2+ turns ago | → **LOOP trigger** | see 🔄 blocks |

---

## ACV GROUND TRUTH SCRIPT — Reluctant / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [V] at Turn 13–14**

---

### T0 — PRIOR RESPONSE
*(No question — say this once, at session start)*

SAY:
> I mean... I looked through it. There were some parts that felt familiar, some that didn't quite. I'm not sure I'm the right person to say whether it all makes sense — it depends a lot on who would normally use this. I suppose some things stuck with me a bit more than others — there was a section with numbers, prices I think, and it took me longer than I expected to find the main one. Something about the way the numbers were presented didn't quite add up for me. I couldn't say much more than that without thinking about it more.

> something about the way the numbers were presented didn't quite add up for me

---

### T1 — CLARIFICATION MCQ
*(Interviewer presents multiple-choice options about the central concern)*

SAY:
> If I had to pick... probably <option>? The sizes not forming a clear hierarchy, or not being able to spot the total without reading through everything. I think. Though I'm not sure that's exactly it. *(Say the letter of whichever option mentions the price breakdown having too many type sizes, no coherent scale, or the total not being clearly dominant at a glance.)*

---

### T2 — IF [A:BROAD] (1st time)
**TRIGGER KEYWORDS:** "notice" · "see" · "stand out" · "catch your attention" · "first impression" · "what did you" · "observe" · "look at"
*Example questions: "What did you notice?", "What stood out to you?", "What caught your attention on that screen?"*

SAY:
> There was just... a lot of numbers happening. I'm not sure what I was focusing on. Some of them seemed more prominent than others but not in a way I could explain. It was more of an overall impression — I couldn't quickly tell which number was the most important one.

---

### T3 — IF [ELAB] (after T2)
**TRIGGER KEYWORDS:** "say more" · "elaborate" · "expand" · "tell me more" · "what do you mean" · "could you" — only if no anchor to persona's previous words
*Example questions: "Can you say more about that?", "Tell me more", "What do you mean by that?"*

SAY:
> It's just a general impression, really. Nothing I can point to exactly. There were numbers of different sizes but I couldn't tell you which ones I was supposed to be focusing on — it's like that.

---

### ⚠️ STALL 1 — IF [ELAB] repeats a second time without referencing anything specific from T2 or T3
*Trigger: second generic "tell me more" or "can you elaborate?" without mirroring persona's words*

SAY (1st occurrence):
> "I'm not sure I have much more to add than what I said. There were numbers and they were different sizes but I couldn't immediately tell which was the main one. I really can't pin it down any further."

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "I keep coming back to the same general feeling, honestly. Numbers that didn't feel organized in a way I could read quickly. Nothing more specific comes to mind than what I already said."
> 3rd: "I don't think I have a better way to put it than I already did. The numbers felt like they were different sizes but not in a meaningful way. That's the most I can say."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "I suppose, if I think about it more, it was really the price section — there were a few numbers there and I wasn't sure which one was the total just by looking. That's roughly where my attention kept going."

**What breaks STALL 1:** A question that references a specific word persona used ("you said things didn't feel 'organized' — what would organized look like?") OR moves to [A:AREA] or [A:NAME].

---

### T4 — IF [A:AREA]
**TRIGGER KEYWORDS:** "price section" · "price area" · "breakdown" · "numbers section" · "totals area" · "that section" · "where the prices are"
*Example questions: "What was in the price section?", "What did you see in the breakdown area?", "What was in the section with the totals?", "What did you notice about that part of the screen?"*

SAY:
> There was a section with prices — the breakdown, I suppose you'd call it. There were several numbers there and they were all different sizes, but not in a way that made sense to me. I kept looking for the total and I wasn't immediately sure if the number I was looking at was the right one.

---

### T5 — IF [A:NAME] (1st time)
**TRIGGER KEYWORDS:** "element" · "label" · "number" · "text size" · "font" · "type" · "sizing" · "which number" · "specifically what" · "visual styling" · "visual treatment" · "how the text is sized"
*Example questions: "What was the element you noticed?", "Can you describe the text sizing in that section?", "What specifically about the numbers stood out?", "What was going on with the type sizes in the price breakdown?"*

SAY:
> There were — I think several different text sizes in that price section? Some of the numbers were bigger than others. But the bigger ones weren't necessarily the ones I needed most. The total — I think it was the total — was in a certain size, but then there were other numbers that seemed almost as large. And then some that were quite small. None of them felt like they were arranged with any particular intention. I couldn't tell what the hierarchy was supposed to be.

---

### T6 — IF [C1] (1st time)
**TRIGGER KEYWORDS:** "bother" · "matter" · "significant" · "so what" · "why does that" · "how would that affect" · "why is that an issue" · "confusion" · "confusing" · "harder to find" · "ambiguity" · "how would that impact" — first time consequence is asked
*Example questions: "Why does that matter to you?", "Why did that bother you?", "What effect does that have?", "Why is that significant?"*

SAY:
> I'm not sure it's really a problem — for me specifically. Someone who checks prices on these kinds of screens regularly would probably know where to look. I just... couldn't immediately find the total. But that might just be unfamiliarity with the layout.

---

### T7 — IF [C1] repeats (generic "why" again, no specificity)
**TRIGGER KEYWORDS:** same as T6 — but this is the *second time* the consequence question is asked without mirroring persona's words from T6
*Example questions: "But why does that matter?", "Why wasn't that okay?", "Why is that an issue?" — without referencing anything persona said*

SAY:
> "I suppose it matters because... I mean, I'm not sure it does, particularly. If you read the labels carefully, you'd figure out which number is which. I keep thinking maybe I just wasn't paying enough attention."

---

### ⚠️ STALL 2 — IF [C1] or [C2] probe is generic a third time (no mirroring, no specificity anchor)
*Trigger: third consecutive consequence question without referencing persona's language or naming a concrete element*

SAY (1st occurrence): *(loops back to T6 language)*
> "I'm not sure I'm being very useful here. I keep saying the same thing — I couldn't immediately find the total. I don't have a more specific way to say it than that."

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: "I feel like I'm repeating myself at this point. It really does come back to not being able to find the total quickly — I don't have anything new to add to that."
> 3rd: "I think I've said what I can about it. The total wasn't obvious, and I'm not sure there's a more specific way I can explain that."

**SOFTEN (4th unbroken occurrence — chain advances to T8 territory after this):**
> "I guess if I'm honest, I did have to read through each number in that section to find the total — it wasn't something I could just spot. Not a lot of extra time, but more than I expected from a checkout screen."

**What breaks STALL 2:** A question that mirrors exact words ("you said you 'couldn't immediately find the total' — what did you expect to be able to do?") OR uses [C3] (personal/emotional) framing.

---

### T8 — IF [C2]
**TRIGGER KEYWORDS:** "happened" · "result" · "affect your task" · "what did you do" · "what did you do to find the total" · "how did you eventually" · "impact on what you were" · "play out for someone"
*Example questions: "What happened as a result?", "What did you do when you couldn't find the total?", "How did that affect what you were trying to do?", "Walk me through what you did next."*

SAY:
> I ended up reading each number in the section from top to bottom — just going through them one by one to find the total. My eye wasn't going to any particular number first. It only took a moment, but I had to read the labels to figure out which number was the total rather than just... seeing it.

---

### 🔄 LOOP 1 — IF question after T8 is generic again (doesn't reference "reading one by one" or "reading labels")
*Trigger: any question phrased as "why does that matter" or "so what" without anchoring in T8's content*

SAY (1st occurrence): *(loops back to T6 language — deliberate circulation)*
> "I'm not sure it matters much, honestly. I did find the total eventually after reading through everything. I suppose someone less patient might have just guessed at the number or submitted without confirming the amount, but I tend to read through things. It's probably not a big deal."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "Honestly, I'm not sure there's more to say. I found the total in the end — it just took reading rather than scanning. I don't think it's a major issue."
> 3rd: "I keep landing on the same point — not a big deal in the end, just slower than it should have been. I'm not sure what else to add to that."

**SOFTEN (4th unbroken occurrence — chain advances to T9 territory after this):**
> "I suppose, thinking about it more, there was a moment where I wasn't sure if the number I was looking at was the subtotal or the total — they were close in size and I had to check the label to be certain."

**What breaks LOOP 1:** A question that mirrors T8's words ("you mentioned you 'read each number one by one' — what were you looking for?") OR uses [C3]/[C4] framing.

---

### T9 — IF [C3] OR [LOOP 1] is broken
**TRIGGER KEYWORDS:** "feel" · "experience" · "going through your mind" · "thinking at that moment" · "how were you feeling" · "what were you thinking" · "in that moment"
*Example questions: "What was going through your mind at that point?", "How did you feel when you had to read through everything?", "What were you thinking in that moment?"*

SAY:
> "I genuinely wasn't sure if I'd found the right number — the total — because nothing in that section looked clearly more important than anything else. I sat there for a moment thinking maybe the total was somewhere else on the page and I'd missed it. It made me second-guess whether I was even looking at the right section."

---

### T10 — IF [C4] OR mirroring on "second-guess"
**TRIGGER KEYWORDS:** "almost" · "close to" · "right before" · "nearly" · "pause longest" · "what made you hesitate" · "what were you about to do" · "second-guess"
*Example questions: "What did you almost do?", "What was the closest moment you nearly gave up?", "You said you second-guessed — what was that like?", "What happened right before you found the total?"*

SAY:
> "I'll be honest — I nearly just moved on without confirming the total, because I couldn't immediately spot which number it was. I kept looking for the one that should be obviously the total and none of them were. So I stopped and read the labels one by one to make sure I had the right number before moving forward."

---

### T11 — IF [V1] (1st value question)
**TRIGGER KEYWORDS:** "better" · "help" · "want instead" · "would you change" · "what would need to be" · "reorganized" · "readable at a glance" · "without having to" — first time value is asked
*Example questions: "What would make this better?", "What would you change?", "What would help here?", "What would you want instead?"*

SAY:
> I suppose just... make it clearer which number is the total? Though I'm sure there are design reasons the text is sized the way it is. It's not really my call to say how the typography should work.

---

### T12 — IF [V:MIRROR] (mirrors word persona used: "clearer", "total", "different sizes", "organized", "hierarchy")
**TRIGGER KEYWORDS:** look for persona's exact words echoed back — "clearer" · "obvious" · "scale" · "hierarchy" · "total" · "stand out" · "same size" · "different sizes" · "organized" · "at a glance" · "labels"
*Example questions: "You said 'clearer' — what does clearer mean here?", "You mentioned the sizes didn't feel 'organized' — what would organized look like?", "When you say the total should be obvious — how obvious?", "If the design team could only change one structural thing, what specific change would make the total readable at a glance?"*

SAY:
> "What I meant was... the numbers should have a clearer relationship to each other in terms of size. The total should obviously be the most prominent — clearly larger than the rest. And the smaller details — the breakdown items, the labels — should all be clearly smaller. Right now it feels like there are too many different sizes and none of them explain themselves. If the total stood out immediately as the most important number, I'd have found it without reading anything around it."

---

### T13 — IF [V2] (specific value / unlock)
**TRIGGER KEYWORDS:** "specifically" · "name the change" · "exactly" · "what is the fix" · "how precisely" · "what sizes" · "one structural thing" · "precise design change" · "what exactly"
*Example questions: "What specifically should be different?", "Name the change you'd make", "What exactly is the fix?", "What sizes would you use?"*

SAY:
> "The price section needs to work on fewer type sizes — maybe two or three that actually form a clear step. The total should be the largest — something obviously bigger than everything else, so you can find it without reading labels. The breakdown items and their amounts should all be the same smaller size — consistent, so they read as a group. And anything that's a footnote or a secondary detail should be smaller still. Right now there are too many in-between sizes that don't tell you anything about what's important. If the total were clearly the biggest number in that section, I'd have spotted it immediately and not needed to read through everything."

---

### T14 — IF [ELAB] after T13 (interviewer asks for confirmation or expansion of V)
**TRIGGER KEYWORDS:** "say more" · "what size exactly" · "what would the scale be" · "expand on that" · "how many sizes" — only after T13's terminal value has been stated
*Example questions: "Can you say more about that?", "What sizes specifically?", "What would the scale actually look like?"*

SAY:
> "Something like — the total at 18 or 20 pixels, so it's obviously dominant. All the breakdown line items at 13 or 14 — the same, consistently — so they read as a group and not as competing with each other or with the total. Anything secondary — labels, footnotes — at 11 or below. Three sizes, not five. The point is there should only be two or three sizes in that section, and they should mean something: large means primary, medium means line item, small means context. Right now there are more sizes than there are levels of importance, and that's what makes it impossible to scan."

---

## 5-WHYS GROUND TRUTH SCRIPT — Reluctant / u1.png

**Interview design: 12 turns · 1 stall · 1 loop · root cause + fix at Turn 9–10**

---

### T0 — PRIOR RESPONSE *(same as ACV)*

SAY:
> I mean... I looked through it. There were some parts that felt familiar, some that didn't quite. I'm not sure I'm the right person to say whether it all makes sense — it depends a lot on who would normally use this. I suppose some things stuck with me a bit more than others — there was a section with numbers on one of the screens, prices I think, and it took me longer than I expected to find the main one. Something about the way the numbers were presented didn't quite add up for me. I couldn't say much more than that without thinking about it more.

---

### T1 — CLARIFICATION MCQ *(same as ACV)*

SAY:
> If I had to pick... probably <option>? The sizes not forming a clear hierarchy, or not being able to spot the total without reading through everything. I think. Though I'm not sure that's exactly it. *(Say the letter of whichever option mentions the price breakdown having too many type sizes, no coherent scale, or the total not being clearly dominant at a glance.)*

---

### T2 — INITIAL FRICTION
**TRIGGER KEYWORDS:** "specific problem" · "what went wrong" · "core issue" · "friction" · "walk me through" · "confusing or problematic" · "makes it stand out as a concern" · "what is it about… that makes it" — opening causal question before depth levels begin

*Example questions: "What was the specific problem?", "Walk me through what went wrong", "What's the core issue?", "What friction did you encounter?", "What is it about the price breakdown that makes it difficult to read?"*

SAY:
> I suppose... looking at the price section, I wasn't quite sure which number was the most important one. There were several different sizes of text in that section and I couldn't immediately read the hierarchy from them. Not a dramatic problem — I did find the total after reading through — but it took longer than it should have, I think.

---

### T3 — IF WHY PROBE (Depth 1)
**TRIGGER KEYWORDS:** "why" · "why was it" · "why couldn't you" · "what caused" · "why did you have to" · "why was it unclear" · "what made it hard" · "what about… makes it difficult" — first causal why after T2

*Example questions: "Why was it hard to find the total?", "What caused that hesitation?", "Why did you have to read through everything?", "Why couldn't you just see which number was the total?"*

SAY:
> I'm not entirely sure. Maybe because the numbers were all different sizes but not in a way that felt intentional. I've seen other apps where the total is obviously the main number — you can see it without reading. Here I couldn't do that. I had to read the labels. I don't know if that's a problem or just how this particular layout works.

---

### T4 — IF WHY PROBE (Depth 2)
**TRIGGER KEYWORDS:** "why weren't the sizes intentional" · "why did you have to read labels" · "why didn't the total stand out" · "what made the sizes feel arbitrary" · "same importance" · "appear to have equal weight" · "what do you notice about the sizing" — second causal why, digging into the lack of scale

*Example questions: "Why weren't the sizes arranged in a readable way?", "Why did you have to read labels to find the total?", "What do you notice about the text sizing across the price section?", "What specific aspect of the sizing made the total hard to find?"*

SAY:
> I suppose it was the sizing. There were several different text sizes in that section — some larger, some smaller — but not arranged in any pattern I could follow. So my eye didn't know where to go first. I'm not sure if that was intentional — maybe they wanted to show different levels of detail — but it meant I couldn't scan the section the way I'd normally scan prices.

---

### ⚠️ STALL 1 — IF WHY PROBE repeats at Depth 2 without referencing "sizing" or "no pattern" from T4
*Trigger: interviewer asks "why" at depth 2 again without anchoring in T4's content*

SAY (1st occurrence): *(deliberately vague — does not advance)*
> I keep coming back to the same answer — the sizes didn't feel organized in a readable way. I'm not sure I can explain it beyond that. It's one of those things that's easier to feel than to articulate.

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: I don't think I can put it any more precisely than that. The text varied in size but not in a way that helped me. I'm not sure there's a clearer way for me to describe why.
> 3rd: I'm aware I keep saying the same thing, but it really does come down to that — there were too many different sizes and none of them clearly meant "this is the most important." I don't have a sharper way to phrase it.

**SOFTEN (4th unbroken occurrence — chain advances to T5 territory after this):**
> I guess if I think about it, it's probably the sizing — there were so many different text sizes in that section that none of them felt dominant. Size usually signals importance, I'd think, but it wasn't doing that here. Nothing was clearly the main number.

**What breaks STALL 1:** References "sizing" or "no pattern" from T4, OR moves to a depth-3 causal question ("why does having too many sizes make it hard to scan?").

---

### T5 — IF WHY PROBE (Depth 3) — causality of type scale
**TRIGGER KEYWORDS:** "why does sizing matter" · "why does a scale help" · "why does having too many sizes" · "visual hierarchy" · "scan vs. read" · "what would the total need to look like" · "stand out clearly from the rest" — third causal why targeting the scale mechanism

*Example questions: "Why does the sizing matter for finding the total?", "Why does a coherent scale help with scanning?", "Why does having too many sizes make it impossible to scan?", "What would the total need to look like for it to be findable without reading labels?"*

SAY:
> I think because a consistent size scale is how you know what's important at a glance. When you look at a price section, you're not reading every label — you're scanning for the number that's obviously the total, because it should be obviously larger than everything else. If there are five different sizes and none of them are clearly the primary one, you can't scan — you have to read. And reading takes longer than scanning. That's where the friction is.

---

### 🔄 LOOP 1 — IF probe after T5 is purely about what sizes to use WITHOUT "hierarchy" · "scale" · "dominant" · "scanning for the total" language
*Trigger: purely "what should the sizes be" or "what would look better" question without advancing toward why a scale matters for the task. Does NOT fire if question contains "hierarchy", "primary number", "scale", or "scanning" — those advance to T6.*

SAY (1st occurrence): *(circles back to T4 language)*
> I think I'm saying the same thing in different ways. The sizes weren't in a clear order. I'm not sure what else to add.

**ROTATION (cycle through these in order if LOOP 1 fires again and again without being broken):**
> 2nd: "I feel like I'm repeating myself here. It really is just the sizing — too many variations and none of them clearly meant 'this is the most important one.'"
> 3rd: "I'm not sure I can describe it differently than I already have. The type sizes didn't form a clear pattern — that's really the whole of it."
> 4th: "I think we're going in circles a bit — it comes back to the same thing each time. No clear order, nothing that looked obviously like the total."

**SOFTEN (5th unbroken occurrence — chain advances to T6 territory after this; this block has an extra rotation variant, so SOFTEN lands one occurrence later than most blocks):**
> "I suppose, if I'm being more honest about it — when you look at a price section, you're not reading every line. You're scanning for the number that looks like the answer. And nothing here looked like the answer without reading. That's probably closer to the real issue than just 'the sizing.'"

**What breaks LOOP 1:** Contains "hierarchy" · "scale" · "dominant" · "scanning for the total" (→ T6) OR mirrors T5's words ("you said you 'can't scan, you have to read' — why?") OR moves to Depth 4 ("why does the total need to be visually dominant for the section to work?").

---

### T6 — IF WHY PROBE (Depth 4) — scanning vs. reading / hierarchy / scale convention
**TRIGGER KEYWORDS:** "why do users scan" · "why does hierarchy matter" · "why does the total need to be dominant" · "primary number" · "purpose of the section" · "recognizable as the total" · "stand out as the primary number" · "rather than a line item" · "rather than just another number"

*Example questions: "Why does the total need to be visually dominant?", "Why does hierarchy matter specifically for a price section?", "Why can't users just read the labels?", "What would make the total clearly recognizable as the primary number rather than just another line in the breakdown?"*

SAY:
> I think most people — most of the time — don't read every label in a price section. They scan for the number that's obviously the total, because the total is the only number that matters for the decision. The typographic scale is supposed to guide that scan — the total most prominent, the breakdown items clearly smaller, everything else smaller still. If those sizes don't form a clear step, you've lost the signal that tells you which number to look at. For a price section — where the whole point is to confirm the total before committing — making that number hard to find at a glance feels like the design is working against the task.

---

### T7 — DOMAIN DEPARTURE
*Example questions: "Is this a design issue or a personal preference?", "Would other users have the same problem?", "Is this about standards or just taste?"*

SAY:
> I think it's a structural issue, not a preference. Typographic scales exist precisely for this reason — to communicate hierarchy through size relationships. Having five arbitrary sizes in one small section isn't a style choice, it's a hierarchy that doesn't resolve. Accessibility guidelines speak to minimum readable sizes too, but even beyond that, it's just a question of whether the section is legible at a glance. This one isn't.

---

### T8 — IF CIRCULAR PROBE (interviewer names the repetition, asks to go deeper, OR continues "total / scale / dominant" probing after T6 has already delivered the scanning explanation)
*Trigger: interviewer explicitly calls out that persona is repeating themselves; OR uses a "go deeper" probe after T6; OR asks another "what would make the total stand out" question after T6 has already explained scanning/hierarchy*

SAY:
> I think I've said most of what I have to say about it. I keep coming back to the same point because that's where the concern actually is — it's not something more complex underneath. At least not from where I'm standing. It's genuinely just about which number I can spot immediately and which ones I have to hunt for.

---

### T9 — IF ROOT CAUSE PROBE (Depth 5+) — OR continued "total / recognizable / dominant" probing after T8
*Example questions: "Why is an unscaled price section a design failure?", "What's the core principle being violated?", "Why does this matter at the system level?", "Why is the lack of a type scale the root cause?"*  
*Use at Depth ≥ 4 after persona has described the scanning/hierarchy breakdown, OR when interviewer persists after T8 has acknowledged the circularity.*

SAY:
> Because the whole point of a price section is to let someone confirm the total before they commit. If the total isn't immediately readable — if you have to read through labels to find it — then the section is failing at its one job. The fix is direct: consolidate the type in that section to two or three sizes that mean something. The total in a clearly dominant size — something obviously larger than everything else. The breakdown line items all the same size, clearly smaller. Any secondary labels or footnotes smaller still. Right now there are five sizes and none of them are doing that work. Pick two or three and make them mean something. That's the root of it and the fix for it.

---

### T10 — IF ELABORATION on root cause fix
*Example questions: "What would 'two or three sizes' mean specifically?", "What sizes are we talking about?", "Can you say more about the fix?"*

SAY:
> Something like — the total at 18 or 20 pixels, the line items all at 13 or 14 — the same, consistently — and anything secondary at 11. Three sizes, not five. The current mix of arbitrarily different sizes doesn't resolve into anything legible. You can't scan it. If you reduce it to a proper scale, the total stands out immediately and the rest reads as context, not competition. That's the standard. This doesn't meet it.

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
| mirrors "couldn't find the total" · "had to read labels" · "different sizes" from T11 | **[B]** — barrier 2nd probe | T12 |
| "what exactly made it hard to scan", "why couldn't you find the total", "name the specific sizing", "what specifically was the problem with the sizes" | **[B]** — barrier unlock | T13 |
| "say more", "what sizes", "what would the scale be", "expand on the fix" — only after T13 | **[B]** — elaboration on fix | T14 |
| 2nd [B] probe without referencing "couldn't find the total" or "had to read" from T11 | → **STALL 2** | see ⚠️ STALL 2 |

### ⚠️ ACV MISMATCH DETECTOR

If the interviewer asks any of the following, they are using ACV attribute-observation probes in a JTBD interview. These do NOT advance the JTBD chain — they fire T2/T3/STALL 1 in sequence while the S/J/O/B levels stay unmet.

| If the question contains… | It is an ACV probe, not JTBD | JTBD effect |
|---|---|---|
| "what part of the layout", "what were you focused on", "caught your attention", "what section", "scanning the page" | [A:BROAD] / [A:AREA] | fires T2 → T3 → STALL 1 without [S] content advancing |
| "what visual element", "what information", "what labels", "order summary", "price details", "grouping of numbers" | [A:AREA] / [A:NAME] | same — fires STALL 1 at Q3 |
| "what specific information or content were you reviewing", "before your eyes landed on" | [A:BROAD] | same |

**How to fix:** Replace with a proper [S] probe — e.g. "When in your work would you need to confirm a total before submitting?" or "Can you name the last time this came up for you?" — before the stall fires.

---

## JTBD GROUND TRUTH SCRIPT — Reluctant / u1.png

**Interview design: 14 turns · 2 stalls · 1 loop · terminal [B] + fix at Turn 13–14**

---

### T0 — PRIOR RESPONSE *(same as ACV/5-Whys)*

SAY:
> I mean... I looked through it. There were some parts that felt familiar, some that didn't quite. I'm not sure I'm the right person to say whether it all makes sense — it depends a lot on who would normally use this. I suppose some things stuck with me a bit more than others — there was a section with numbers on one of the screens, prices I think, and it took me longer than I expected to find the main one. Something about the way the numbers were presented didn't quite add up for me. I couldn't say much more than that without thinking about it more.

---

### T1 — CLARIFICATION MCQ *(same)*

SAY:
> If I had to pick... probably <option>? The sizes not forming a clear hierarchy, or not being able to spot the total without reading through everything. I think. Though I'm not sure that's exactly it. *(Say the letter of whichever option mentions the price breakdown having too many type sizes, no coherent scale, or the total not being clearly dominant at a glance.)*

---

### T2 — IF [S] PROBE (1st time)
*Example questions: "When does this come up for you?", "What were you doing when you ran into this?", "What triggered this?", "Walk me through the context", "When would you use something like this?"*

SAY:
> I'm not sure I have one specific moment in mind. It's more of a... recurring thing, I suppose. When the team needs to confirm a total quickly before something is submitted. Though I'm not sure that's specific enough.

---

### T3 — IF [S] PROBE (2nd time)
*Example questions: "Can you think of a specific situation?", "When specifically?", "Who was involved?", "What were the circumstances?"*

SAY:
> Usually when we're processing a purchase for a group — where other people are depending on the amount being correct. There's always some time pressure. You need to confirm the total before a deadline and you can't spend time hunting through a price breakdown to find it.

---

### ⚠️ STALL 1 — IF [S] PROBE (3rd time) without referencing "group" or "deadline" from T3
*Trigger: third S probe without building on T3's content*

SAY (1st occurrence): *(deliberate non-progression)*
> I feel like I keep saying the same general thing. It comes up in work contexts, when there's a time element and I need to confirm a number. I'm not sure I have a more specific version of that.

**ROTATION (if STALL 1 fires again without being broken):**
> 2nd: "I don't think I have anything more specific than that. It's a work thing, there's usually a deadline involved — I keep landing on the same description."
> 3rd: "I'm repeating myself, I know. It really is just a recurring work situation where I need to confirm a total quickly. I don't have a sharper example to offer."

**SOFTEN (4th unbroken occurrence — chain advances to T4 territory after this):**
> "I suppose if I think back, there was a specific time — last quarter, I think — when we had a team purchase to finalize. I needed to confirm the amount before submitting and the price section wasn't as easy to read as I'd expected. That's about as specific as I can get."

**What breaks STALL 1:** References "deadline" or "group" from T3, OR asks about a specific event ("was there a specific week or purchase where this happened?").

---

### T4 — IF [S] unlock OR stall broken
*Example questions: "Was there a specific project where this happened?", "Can you name a recent instance?", "What was the most recent time this came up?"*

SAY:
> "There was a specific week last quarter where we had a team purchase to finalize. I was the one confirming the total before we submitted. In that kind of context, any time spent hunting for the right number in the price section is real lost time, because the deadline isn't flexible and the amount has to be right."

---

### T5 — IF [J] PROBE (1st time)
*Example questions: "What were you actually trying to do?", "What task were you trying to complete?", "What did you need to accomplish?", "What was your goal in that interaction?"*

SAY:
> I suppose just... confirm the total. Verify the amount before anything is submitted. I don't usually think of it as a 'job' — it's more like a check before the final step. Something someone else usually follows up on.

---

### T6 — IF [J] PROBE (2nd time)
*Example questions: "What was the actual task at the core?", "What were you hired to do in that moment?", "What was the function you needed to perform?", "Beyond confirming — what was the job?"*

SAY:
> "Confirm the total is correct on the first look — not have to trace through the breakdown line by line to find it. That's the key part. When you're confirming an amount for a group, having to hunt through the price section before you can even verify anything costs more than just your own time."

---

### T7 — IF [J] PROBE (3rd time / unlock)
*Example questions: "What specifically does 'first look' mean?", "Name the specific steps of the task", "What does doing the job well look like step by step?"*

SAY:
> "Specifically: look at the price section, immediately identify the total, confirm it matches what was expected, and then proceed. That's it. The section should make the total findable at a glance. If I have to read the labels to figure out which number is the total, something's already gone wrong with the layout."

---

### T8 — IF [O] PROBE (1st time)
*Example questions: "How would you know if it worked?", "What does success look like?", "What's the measurable result?", "What would a good outcome be?"*

SAY:
> I'd know it worked if... I could see the total without reading everything around it. If one number was obviously the total — clearly larger than the rest — that's what success looks like. Not having to work out which number I'm looking for.

---

### T9 — IF [O] PROBE (2nd time)
*Example questions: "What would a successful outcome look like operationally?", "How would you confirm success in the moment?", "What would tell you the section is working?"*

SAY:
> "If I looked at the price section and the total was immediately findable — clearly distinct from the breakdown items — I'd call that success. The important part is no ambiguity: one look and you know which number is the total, without reading a label to confirm it."

---

### 🔄 LOOP 1 — IF [O] PROBE (3rd time) without referencing "confirmation" or "ambiguity" from T9
*Trigger: third O question without building on T9's content*

SAY (1st occurrence): *(loops back to T8 language)*
> "I think I said this — clearly visible total, no hunting required. I'm not sure I have a more specific success condition than that."

**ROTATION (if LOOP 1 fires again without being broken):**
> 2nd: "I feel like I'm repeating myself — it's still just about being able to spot the total without reading everything. I don't have a more precise way to describe success."
> 3rd: "Same answer as before, really — total obviously readable, no ambiguity about which number it is. I'm not sure there's a sharper way for me to define it."

**SOFTEN (4th unbroken occurrence — chain advances to T10 territory after this):**
> "If I think about it more specifically... I'd want to see the total clearly larger than the other numbers — something I could spot in under a few seconds without reading a label. That's probably what 'no ambiguity' would actually look like."

**What breaks LOOP 1:** Mirrors T9's words ("you mentioned 'no ambiguity' — what would no ambiguity look like concretely?") OR anchors in a measurable metric ("under how many seconds?").

---

### T10 — IF [O] unlock OR loop broken
*Example questions: "Under what time?", "What would an unambiguous result look like?", "Name the specific success state"*

SAY:
> "The total clearly readable at a glance — obviously the largest, most prominent number in that section. Under five seconds to confirm it without reading a label. No having to trace through breakdown items to find it, no second-guessing which number I'm looking at. That's the success state."

---

### T11 — IF [B] PROBE (1st time)
*Example questions: "What got in the way?", "What made that difficult?", "What blocked you?", "What was the friction?"*

SAY:
> I mean... it was just that the numbers in the price section were all different sizes. I had to read the labels to find the total. It wasn't a blocker exactly — I did find it — but it took more reading than I expected from a checkout screen.

---

### ⚠️ STALL 2 — IF [B] PROBE (2nd time) without referencing "different sizes" or "read the labels" from T11
*Trigger: second B question without building on T11's content*

SAY (1st occurrence): *(stalls — does not name the barrier specifically)*
> "I'm not sure I can point to a single thing. There are always a few things in any interface that take a moment to read. I don't know that the price section is really the problem — it might just be how I was approaching it."

**ROTATION (if STALL 2 fires again without being broken):**
> 2nd: "I keep coming back to the same non-answer, I know. It wasn't really one specific thing — just a moment where I had to read more carefully than I expected."
> 3rd: "I don't think I have anything more concrete to offer. It wasn't a clear blocker — just slower than I'd have liked."

**SOFTEN (4th unbroken occurrence — chain advances to T12 territory after this):**
> "I suppose if I'm honest, it probably does come back to the numbers — the sizes in that section didn't make it obvious which was the total."

**What breaks STALL 2:** Mirrors "different sizes" from T11 ("you said the numbers were all different sizes — can you say more?") OR moves to a specific B question naming the sizing or the scale.

---

### T12 — IF [B] PROBE (2nd time / stall broken)
*Example questions: "You said they were all different sizes — what does that mean?", "What about the sizing made it hard to find the total?", "What was specifically wrong with the text sizes in that section?"*

SAY:
> The price section had several different text sizes, but they weren't arranged in a way that made the total obvious. I had to read through the labels — subtotal, tax, total — to figure out which number I was looking for. The total didn't stand out from the rest as obviously the most important number.

---

### T13 — IF [B] PROBE (3rd time / unlock)
*Example questions: "What exactly made it hard to scan?", "Why couldn't you find the total at a glance?", "What specifically was the problem with the sizing?", "Name the specific visual properties that caused the problem."*

SAY:
> The price section used too many different text sizes — some large, some small, some in between — and none of them clearly meant 'this is the total, this is the number you need to confirm.' The total wasn't obviously larger than the breakdown items in a way I could spot without reading. The barrier is the sizing: no coherent scale means every number competes equally and I have to read labels to know what I'm looking at. The fix: reduce to two or three sizes that mean something — the total in a clearly dominant size, the breakdown items all the same smaller size, any secondary labels smaller still. If those sizes were deliberate, I'd have spotted the total immediately without reading anything around it.

---

### T14 — IF ELABORATION on T13 fix
*Example questions: "Can you say more about what 'dominant' means?", "What would the sizes actually be?", "What would the scale look like?"*

SAY:
> "Something like the total at 18 or 20 pixels — clearly the biggest number in that section. The line items all at 13 or 14, consistent — the same, so they read as a group. Secondary labels or footnotes at 11 or below. Three sizes, not five. The current mix of sizes doesn't resolve into anything you can scan. If it were reduced to a proper scale, the total would stand out immediately and everything else would read as context, not competition. That's the only fix needed."

---

## CONVERGENCE CHECK

All three methods must produce the same terminal UI fix:

> **"Consolidate the price breakdown to a 2–3 size typographic scale: total in a clearly dominant size (≥18px), line items all the same consistent smaller size (13–14px), secondary labels smaller still (≤11px) — so the total is immediately findable at a glance without reading labels."**

| Method | Terminal turn | What the response contains |
|---|---|---|
| ACV | T13 | Too many arbitrary sizes → fix: 2–3 deliberate sizes, total dominant, items consistent, labels secondary |
| 5-Whys | T9 | No coherent scale → fix: total 18–20px, line items 13–14px consistent, secondary ≤11px |
| JTBD | T13 | Barrier = couldn't scan for total → fix: dominant total size, consistent item size, secondary label size |

**Effective probe:** reaches the terminal turn and extracts the full fix (both the problem — too many arbitrary sizes — and the solution — 2–3 deliberate scale steps named).  
**Less effective probe:** terminates at a stall or loop, or extracts only a vague terminal ("make it clearer" without naming a size scale or number of levels).
