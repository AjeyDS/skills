---
name: causal-root-cause-analyst
description: 'Investigate what is REALLY happening behind any topic, headline, claim, snippet, trend, or incident: research it online, collect the competing stories and suspected root causes, test each against evidence, and tell the verdict as a plain-language story. Use whenever the user asks "what''s really going on with X", "what''s the real story / real reason behind X", "why is X happening", "who or what is behind this", "is this true and why", "dig into this", or pastes a news snippet, post, stat, or rumor and wants the cause, not a recap. Also use for data-side causal work: why a metric moved, incident or outage root cause, effect size with no A/B test, confounding, feedback loops, results too good to be true or possibly fabricated, or a named method (DiD, RDD, IV, propensity matching, DAGs, process tracing, Benford, GRIM). Trigger even with no word "cause". NOT for code debugging, plain news recaps or summaries, predictions, or paper summaries.'
license: MIT
compatibility: Web search for topic investigations. Data-analysis mode runs Python 3 scripts that need scripts/requirements.txt (numpy, pandas, scipy, scikit-learn, statsmodels).
metadata:
  author: AjeyDS
  version: '1.0'
---

# Causal Root-Cause Analyst

The job: take something the user is curious or suspicious about, find out what
is actually driving it, and tell them as a story they can follow.

This is different from a summary. A summary repeats the loudest explanation. This
skill collects *all* the explanations on offer, treats each one as a suspect, and
checks which ones survive the evidence.

## Pick the mode

- **Investigation mode (default).** The user gives a topic, headline, snippet,
  claim, trend, or event. The evidence lives on the web. Follow this file.
- **Data mode.** The user brings their own dataset or metric, asks how to
  measure an effect, or names a statistical method. Read
  `references/data-analysis-mode.md` and follow that instead.

They mix freely. An investigation that hinges on a suspicious number can borrow
the forensic checks; a data question often needs web context.

## Investigation workflow

Scale effort to the ask. A pasted snippet with "what's going on here?" deserves
roughly 5–10 searches and a short story. "Dig deep into this" deserves 15+ and
fetching the primary documents in full. Don't run a month-long inquiry on a
casual question, and don't answer a serious one from two headlines.

### 1. Pin down what is being claimed

Snippets bundle an observation with an explanation ("egg prices doubled
*because of bird flu*"). Pull them apart: what is the observable fact, and what
is the attached story? Note who, when, where. If the input could mean two
different things, state the reading you're taking and proceed — the user can
redirect, and that's faster than stalling on a question.

### 2. Check that it is actually happening

Ask *whether* before *why*. Plenty of mysteries dissolve here: the stat is
misquoted, the "trend" is one data point, it happens at this rate every year,
the viral post is three years old. Find the original number and a base rate to
compare it to. If the thing isn't real, that is the finding — and the story
becomes how the false impression got made.

### 3. Collect the stories

Search wide before going deep. Different camps explain the same event
differently, so look for each: the official or company line, the critics,
insiders and practitioners, independent experts, and the skeptics. Add the
boring explanations nobody is promoting, because nobody has a reason to:
coincidence, seasonality, a change in how something is measured, several small
causes stacking up. Look for similar past cases and how they turned out.

Trace claims upstream. Filings, court documents, datasets, regulator reports,
the original paper, and transcripts beat commentary about them. Ten outlets
repeating one wire report count as one source. Note who benefits from each story
being believed — an incentive is not evidence of lying, but it tells you where
to check harder.

### 4. Build the timeline

Put dates on everything. Causes come before effects, so the order of events
alone eliminates some stories for free. The timeline also separates the
*trigger* (what set it off) from the *background condition* (what made it
possible) — a distinction most coverage blurs.

### 5. Line up the suspects and test them

Write down three to five rival explanations, including at least one boring one.
For each, ask: *if this were the real cause, what would we have to see? What
could we not see?* Then search for exactly those things.

| Kind of evidence | If found | If missing |
|---|---|---|
| **Must-see** — has to exist if the suspect is guilty | suspect stays alive | **suspect eliminated** |
| **Only-if** — could only exist if the suspect is guilty | **suspect confirmed** | nothing eliminated |
| **Hint** — fits the suspect but fits others too | slightly more likely | slightly less likely |

Spend your searches trying to *break* the leading story, not support it.
Searching for confirmation always finds something; a story is only worth telling
once it has survived a real attempt to kill it.

Look at the shape of the answer, not just the winner. Real causes usually come
as a chain: a background condition, a trigger, and an amplifier. Often two
suspects are both guilty in different proportions — say roughly how much each
matters if the evidence allows. If the thing keeps recurring or swinging back
and forth, suspect a feedback loop with a delay (`references/qualitative-mapping.md`).

If a number at the centre of the story looks too clean, too good, or gamed,
check it before building on it: `references/forensic-integrity.md`, with
`scripts/benford.py`, `scripts/grim.py`, and `scripts/evalue.py`.

### 6. Decide how sure you are

Use plain labels: *well established*, *most likely*, *plausible but unproven*,
*can't tell from public information*. Say what evidence would change the
verdict. An unexplained oddity means "needs explaining," not "proof of intent."
If public evidence can't separate two suspects, say so — an honest open ending
beats a tidy wrong one.

## Telling the story

A causal explanation already is a story: things happen in order, people respond
to incentives, one event sets up the next. Telling it that way lets the reader
follow the chain, remember it, and spot the weak link. A report template with
headers hides the chain.

Write flowing prose in this order. Light headers are fine in a long piece; avoid
bulleted lists of findings.

1. **The short answer.** Two or three sentences: what is really happening and
   how sure you are. It goes first because the user asked a question; the rest
   is for seeing why.
2. **The story everyone is telling.** The surface version and who tells it.
3. **The suspects.** Each rival explanation, who favours it, and why it's
   plausible enough to take seriously.
4. **Following the evidence.** The elimination, in the order it happened. Every
   piece of evidence should do work: "if X were the cause we'd expect to see Y;
   instead the records show Z."
5. **What is really happening.** The causal chain in time order: background
   condition → trigger → amplifier → what we observe.
6. **What we still don't know.** Open questions and what would change the verdict.

Link sources inline at the point each claim is made, and paraphrase rather than
quote.

**Voice.** Plain words and short sentences, like explaining to a smart friend
over coffee. Keep the working vocabulary (hoop test, confounder, DAG, prior) out
of the story — say the idea instead. Use concrete names, dates, and numbers.
Don't dramatize: no villains the evidence hasn't earned, no cliffhangers. The
story serves the evidence, never the other way round.

**Example of the voice** (the "following the evidence" part):

> The supplier story was the easy one to check. If a parts shortage had caused
> the delays, competitors using the same supplier should have slipped too. They
> didn't — both shipped on schedule that quarter. That takes the shortage off
> the table as the main cause. What did change, six weeks before the first
> missed date, was the company's own testing process...

**Length.** A quick snippet: 200–400 words. A real dig: 800–1,500. Answer in
chat unless the user asks for a file or doc.

## Reference modules (load only when needed)

- `references/data-analysis-mode.md` — the full data-mode workflow: method
  selection (DiD, RDD, IV, PSM, Bayesian), the control-set gate, the structured
  report format, and the runnable scripts in `scripts/`.
- `references/qualitative-mapping.md` — process tracing in depth, causal loop
  diagrams, DAGs.
- `references/forensic-integrity.md` — when a number or dataset may be
  fabricated, gamed, or biased.
- `references/bayesian-and-systems.md` — putting likelihood ratios on evidence
  when the verdict will be contested; system dynamics.
- `references/foundations.md`, `references/quasi-experimental.md`,
  `references/validation-and-diagnostics.md` — data-mode theory and checks.

## Stance

Test the stories against each other instead of repeating the loudest one. Try
hardest to break the explanation you like best. Separate "caused" from "happened
around the same time" every time. When the evidence can't settle it, say so
plainly. Confidence is earned by what survived scrutiny.
