---
name: project-talk-track
description: Turn any project repo into a rehearsable 3-page "talk track" PDF in the owner's own spoken voice — page 1 a step-by-step first-person walkthrough of what they did and why (with a headline-numbers band and highlighted figures to land on), page 2 the same pitch at three lengths (one line / 30s / 90s) plus ready answers, page 3 the weak links an interviewer will push on with prepared answers and fill-in blanks for facts the repo lacks. Use this whenever the user wants to explain, present, pitch, or defend a project they built — "help me explain this project", "interview prep for this repo", "make a script for talking through what I did", "one-pager / talk track / pitch for this project", "what would an interviewer ask about this", "how do I present this" — even if they don't say "PDF" or "script". Also use it when they ask for a concise end-to-end explanation of a repo's choices and process, or want ready-made answers for weak points in their work.
license: MIT
compatibility: Python 3 with pypdf (pypdfium2 optional) and a local Chrome or Chromium for PDF rendering.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Project talk track

Produce `talk-track.pdf` (and its `talk-track.html` source) for a repo: three US-Letter pages
the owner can rehearse from. It is a **script**, not a report — the reader is the person who
built the thing, preparing to say it out loud. Everything here follows from that.

| Page | What it is |
|---|---|
| 1 — Talk track | ~8 numbered beats, chronological, first person, one point each; a headline-numbers band; a footer of prep notes (limits to volunteer, numbers to have ready, "what I learned") |
| 2 — The short version | The same pitch at one line, thirty seconds, ninety seconds; the band repeated; three ready answers |
| 3 — Weak links | ~12 questions a sharp interviewer will ask, grouped Rigor / Design / Scope, with answers in the owner's voice; red-marked items that need rehearsal or a fill-in blank |

Bundled: `assets/template.html` (tuned CSS + slot skeleton), `scripts/` (notebook dumper,
page-fit measurer, PDF builder), `references/voice.md` (how to write spoken lines — read it
before writing), `references/example-home-credit.html` (a finished one, for calibrating
density and tone; do not copy its facts).

## 1. Research first — build a fact sheet before writing a word

The pages are only as good as the facts under them, and the facts are scattered. Read in
this order and write a fact sheet in your scratchpad as you go:

1. **README, reports, write-ups, `docs/`** — the owner's own narrative and headline numbers.
2. **Notebooks** — `python3 scripts/dump_notebook.py <nb> --max-chars 2500`. It prints
   *outputs* as well as source; fold scores, shapes and printed metrics live in outputs.
3. **Code and scripts** — what was actually done, which may differ from what the prose says.
4. **`git log --oneline`** — the sequence of work and abandoned directions.
5. **Deploy / infra / test folders** — usually where the best "what went wrong" stories are.
6. **Any project memory or plan docs** — designed-but-not-run phases, negative results.

The fact sheet needs, at minimum:

- **Problem & metric** — what's predicted/built, how success is scored, why that metric.
- **Headline result and its journey** — 4-5 milestones with numbers, in order. This is the
  band. If the project has no progression metric, one headline fact replaces the band.
- **Decisions with their *because*** — each non-obvious choice and the evidence behind it.
  Prefer the owner's stated reason; note where code shows a different reason.
- **The failure that was diagnosed** — the attempt that lost and *why*. Every project has
  one; it's the most memorable beat and the best "what did you learn" answer.
- **Limits the docs don't state** — no holdout, selection outside CV, an untested table,
  something torn down. Verify by reading code, not by trusting the report; reports
  overstate rigor.
- **What's not done** — designed-not-run phases, unused data, tuning skipped.
- **Facts the repo does not contain** — leaderboard score, latency, user counts, cost.
  These become **fill-in blanks**, never guesses.

Never invent a number. If it isn't in the repo, it's a blank with a fallback line.

## 2. Choose the beats

Eight beats fit the page. They're archetypes; map them to the project, keep the order
logic (chronological, each beat sets up the next), keep the labels to one or two short
words that fit a 46pt gutter.

| # | Archetype | ML / data project | Software / product | Research |
|---|---|---|---|---|
| 1 | Problem | task, data shape, metric, why it's a ranking/threshold problem | user, pain, constraint that shaped design | question, why it matters |
| 2 | Read the data / the ground | EDA findings that changed cleaning | prior art, what existing tools got wrong | prior work, gap |
| 3 | Biggest lever | feature engineering | core architecture decision | main method |
| 4 | Second lever | selection / pruning | the simplification that removed most complexity | key ablation |
| 5 | How I measured | CV design, why it's honest | tests, benchmarks, observability | evaluation protocol |
| 6 | Alternatives tried | other model families | approaches considered and rejected | baselines |
| 7 | **The failure** (`step fail`) | the attempt that lost and its diagnosis | the bug/outage/wrong abstraction and what it revealed | the negative result |
| 8 | Takeaway | ranking of levers by payoff | what I'd build first next time | what generalizes |

Beat 7 exists in every project. If the owner's docs don't mention one, look harder — the
git log and the deploy folder usually have it.

## 3. Write in the owner's voice

Read `references/voice.md` now. The short version: first person, spoken openers,
decisions framed as decisions with a *because*, numbers inside sentences, limits admitted
plainly. Read each paragraph aloud; if it sounds like a README it's wrong.

Highlight sparingly: `<mark>` on the one number per beat to land on, `<b>` on the phrase to
stress, `<i>` on a contrast pair. Over-marking makes the cues useless.

## 4. Fill the template

```bash
cp <skill>/assets/template.html <repo>/talk-track.html
```

Replace every `{{SLOT}}`. When done, `grep -n '{{' talk-track.html` must return nothing.

- **Band**: 4-5 milestones, last cell is the final result (it renders inverted). Labels
  must fit on one line at ~6.6pt — shorten labels, not the band.
- **Page 1 footer**: three columns — limits phrased as things *I'd say before they ask*;
  numbers in my pocket (4 bullets of figures for follow-ups); a "what I learned" line.
- **Page 2 footer**: one thing to remember; a "why no ___" answer for the obvious omission
  (tuning, tests, a table, a benchmark — whatever the repo skipped); why should I care.
- **Page 3**: Rigor group first, red. Put a `qa hole` with a `.fill` blank on any fact the
  repo lacks, with a fallback line in `.note`. Put a second `qa hole` on the answer that
  reads worst if delivered vaguely (fairness, security, cost, scale — whichever applies).
  Design group: the "why X not Y" questions. Scope group: what didn't work, the black-box
  dependency, where next.
- Use plain ASCII for operators (`>>`, `->`) — glyphs like `≫` fall back to the wrong
  character in Helvetica and print as `»`.

## 5. Fit and render — measure, don't guess

Spoken prose runs long; the template fits ~550 words on page 1. Iterating by re-rendering
and eyeballing wastes cycles, so measure:

```bash
python3 <skill>/scripts/measure.py talk-track.html          # per-page height vs 10.2in
python3 <skill>/scripts/build_pdf.py talk-track.html --png-dir previews   # PDF + page PNGs
```

`measure.py` prints each page's overflow in inches. Close it in this order: trim prose →
`body font-size` (9.1 → 8.85pt) → `line-height` (1.37 → 1.34) → `.step margin-bottom`.
Aim for 0.15–0.5in of slack; under 0.1in can flip to an extra page in the print pass.
`build_pdf.py` exits non-zero unless the PDF is exactly 3 pages.

Then **look at the PNGs** — the failures below are invisible in text:

- gutter labels wrapping to three lines (shorten the label)
- a band label wrapping and pushing its number down (shorten the label)
- a footer heading wrapping (shorten it)
- a whole block jumping to the next page because of `break-inside: avoid` (trim above it)
- a fallback glyph (`»` where `>>` was meant)

## 6. Deliver

Save `talk-track.pdf` and `talk-track.html` in the repo root unless told otherwise. If a
file-delivery tool exists (`SendUserFile`), send the PDF. In the summary, list every
fill-in blank and red-marked item and ask for the missing facts — those are the user's next
action. Don't commit unless asked.

Offer, in one line, the longer companion: a `WALKTHROUGH.md` with the same beats at full
length (what · why · what it moved), for reading rather than saying.

## Pitfalls seen on the original

- **Document voice.** The first draft read like a report and was rejected. Write spoken
  lines from the start; see `references/voice.md`.
- **Overstating state.** "The model runs behind an endpoint" when it was deployed, verified,
  then torn down. Say what is true now; past-tense verbs are free.
- **Trusting the report over the code.** The report said "leak-free"; the code ran feature
  selection on all training rows. The page-1 footer and page-3 Rigor answers are where that
  honesty lives — they're what makes the owner sound rigorous instead of caught.
- **Two-column body on page 1.** Reads well but rehearses badly; a script is read top to
  bottom. Page 1 is single-column with a label gutter; only page 3 uses columns.
- **Fitting by feel.** Three render cycles were spent guessing before measuring. Measure
  first.
