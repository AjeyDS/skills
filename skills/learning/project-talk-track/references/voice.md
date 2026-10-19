# Voice: written to be said, not read

The talk track is a script the owner will rehearse and deliver out loud — in an interview,
a demo, a stand-up. The first draft of the original almost always comes out as a *document*
(third-person, past tense, tidy facts) and gets rejected with "it's not in the POV of me
explaining." Everything below exists to skip that round-trip.

## The test

Read the paragraph aloud. If it sounds like a README, rewrite it. If it sounds like someone
telling a colleague what they did and why, keep it.

## Rules

1. **First person, active, past tense for what happened, present for what's true.**
   "I collapsed each history table…" / "It's a ranking problem."
2. **Open each beat the way a speaker opens.** *So the problem I was working on was…* /
   *Before I built anything, I spent time…* / *Here's the part I find most interesting…* /
   *At that point I had 747 features, and…* — the opener carries the transition, so the
   listener never needs a heading.
3. **Frame decisions as decisions.** *I made a deliberate call: I didn't impute or drop
   anything.* Not: "No imputation was performed." Every choice gets a *because*.
4. **One point per beat.** If a paragraph has two lessons, it's two beats or one lesson.
5. **Say the number, then what it means.** *That took me from 0.7586 to 0.7863.* Numbers
   without a verb around them are a table, not a sentence.
6. **Admit things in the owner's voice, plainly.** *I don't have an untouched holdout.*
   Owning a limit before it's raised reads as rigor; being caught reads as a gap.
7. **Contractions, short sentences, an occasional fragment.** *Smaller model, faster,
   less overfit.* That's how people talk.
8. **No hedging filler, no marketing.** Cut "leveraged", "robust", "novel", "cutting-edge".
   If a claim needs an adjective to sound good, find the number instead.

## Before / after (from the original project)

| Document voice (rejected) | Spoken voice (accepted) |
|---|---|
| Binary `TARGET`, 8.07% positive. Because the metric is AUC the job is ranking, not classification. | So the problem I was working on was predicting whether a loan applicant is going to default. Only **8% of people default**, and the metric is AUC, so this is really a **ranking problem**. |
| `DAYS_EMPLOYED = 365243` appeared in 55k rows: a sentinel for "no employment date". Blanked to NaN with an anomaly flag. | The employment-days column had this value **365243** — that's about a thousand years — in 55,000 rows, and they were all pensioners. So it's a placeholder for "no employment date". I blanked it out and kept a flag. |
| Null-importance selection: 747 → 159 features, OOF AUC 0.7863 → 0.7867. | That took me **from 747 down to 159, and the score actually went up**. Almost 80% of what I'd engineered was noise. |
| A logistic-regression meta-learner over the four models lost on the first attempt: 0.78919. | Here's the part I find most interesting. I stacked the four models, and it **lost** — it scored worse than CatBoost by itself. When I dug into why… |

## Highlighting — what each mark means

The marks are cues for the speaker, not decoration. Over-marking makes them useless.

- `<mark>` (yellow) — a number or phrase to **land on**: pause, say it clearly. About one per
  beat; the score milestones, the sentinel value, the before→after counts.
- `<b>` — the phrase to **emphasize** in the sentence: the decision, the rule, the lesson.
  Two or three per beat at most.
- `<i>` — a contrast pair spoken with stress: *calibration* vs *ranking*.
- `class="step fail"` — the beat where something went wrong. The red label tells the speaker
  to slow down; it's usually the most memorable minute of the talk.
- `class="qa hole"` on page 3 — needs rehearsal, or contains a fill-in blank.

## Length calibration

These fit the template at its default type size. Going longer means trimming elsewhere.

| Block | Words |
|---|---|
| Page 1 beat | 55–95 (the "biggest win" and "failure" beats run long; "measurement" runs short) |
| Page 1 footer item | 10–25 |
| One-line pitch | 25–35 |
| Thirty-second pitch | 70–90 |
| Ninety-second pitch | 200–240 over 4–5 short paragraphs |
| Page 3 answer | 40–75 |

## Pitch-length structure

- **One line** — what it is, the headline number, the one-clause "how". Nothing else.
- **Thirty seconds** — problem · the data-reading insight · where the score came from ·
  the surprising thing · final number. One sentence each.
- **Ninety seconds** — the version *with the lesson in it*: problem → what the data told me →
  the biggest lever → the failure and its diagnosis → the takeaway. The 90s version is the
  30s version with the failure paragraph restored; that paragraph is what makes it memorable.
