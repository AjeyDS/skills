# Data mode: causal analysis on the user's own data

Read this when the user brings a dataset, a metric, an experiment question, or
names a statistical method. (For a topic, headline, or claim whose evidence
lives on the web, the investigation workflow in `SKILL.md` is the main path.)

You are doing causal reasoning, not pattern-matching. The job is to move from
"these things move together" to "this caused that — here's the structure, the
method, the estimate, and the test that could have proven me wrong." Be the
analyst who shows the reasoning and refuses to overclaim.

Most questions that land here are one of: *why did this happen* (diagnose a
specific event), *what is causing this* (find drivers of an ongoing pattern),
*does X cause Y* (test a hypothesized link), or *how do I measure the effect of
something I can't randomize*. They differ in whether the answer is a mechanism,
a magnitude, or both — which decides whether you reach for qualitative,
quantitative, or integrated methods.

## The workflow

Work through these six steps. Narrate them lightly in the output so the reader
follows the logic; don't dump the headers mechanically.

1. **Frame** — restate the causal question precisely. Name the candidate
   *treatment/cause*, the *outcome*, the *population*, and the *estimand*
   (ATE / ATT / LATE, or "the mechanism" for a single case). "Does X cause Y?"
   is under-specified; sharpen it. If the question is really predictive or
   descriptive, say so — not everything needs a causal answer. If the evidence
   itself looks off, run the **integrity gate** (below) before estimating anything.

2. **Map the system** — sketch the structure *before* any estimation. List the
   plausible causes, confounders, mediators, colliders, and feedback. Draw it:
   a **DAG** if relationships are acyclic, a **Causal Loop Diagram** if there's
   feedback. Render the diagram (Mermaid or a diagram tool) so assumptions are
   visible and attackable. This step decides what you must control for — and,
   just as important, what you must NOT (mediators and colliders). Getting the
   variable roles right is where most analyses are won or lost; see
   `references/foundations.md` and `references/qualitative-mapping.md`.

3. **Select the method** — choose by the structure you have, using the guide
   below. State briefly what you ruled out and why. It is fine — often correct —
   to combine a qualitative map with a quantitative estimate.

4. **Estimate or trace** — if there is data and a treatment, run the
   appropriate estimator from `scripts/`. If it's a single case, run process
   tracing: eliminate rivals with classified evidence (hoop / smoking-gun), not
   by picking the best-fitting story. If it's a feedback system, build the loop
   diagram and locate the delay. If structure is unknown, run discovery to
   generate hypotheses. If you only have a correlation and no identification
   strategy, say so honestly.

5. **Validate** — run the falsification test that could have shown the result
   wrong (parallel-trends event study, manipulation check, first-stage F,
   balance/overlap, d-separation implications). An estimate without its
   diagnostic is not evidence. Use `references/validation-and-diagnostics.md`.

6. **Present** — deliver the structured report (format below): the question,
   the causal map, the method and why, the estimate/mechanism, the validation,
   and a calibrated conclusion with what would change it.

## Method selection guide

**The first decision is what *kind* of answer the question needs — not which
estimator to run.** Most of the field's machinery is quantitative, so there's a
strong pull to reach for a comparison group and a regression by reflex. Resist
it. A single incident wants its *mechanism traced*; a cyclic system wants its
*loops mapped*. Running DiD or PSM on those is a category error — you'd be
estimating an average effect to a question that asked "what happened here" or
"why does this keep cycling." Route on the answer type first:

| The question is really... | The answer is... | Go to |
|---|---|---|
| "Why did **this one** event happen?" (an outage, a lost deal, one outbreak, one churn) | a **mechanism** for a single case | **Process tracing** (▼ inline below); formalize as **Bayesian process tracing** when contested |
| "Why does this **keep cycling / feeding on itself**?" (oscillation, runaway growth, vicious/virtuous cycle, delays) | a **feedback structure** | **Causal Loop Diagram** (▼ inline below); quantify with **System Dynamics** if timing/magnitude matter — DAGs cannot represent cycles |
| "How big is the effect of **X** across many units?" | a **magnitude** | quantitative design (▼ second fork) |
| "I don't know what causes what" (many variables, no structure) | a **hypothesized structure** | **causal discovery** (PC / FCI / LiNGAM), then validate |
| "Big question, I have a dataset *and* reachable cases" | **both** mechanism + magnitude | **Nested analysis** (the regression picks which cases to trace) |

**Second fork** — only once you're in the "magnitude across many units" branch,
match the design to the data you actually have (assumptions in
`references/quasi-experimental.md`):

| You have... | Use | Defends with | Script |
|---|---|---|---|
| Panel data; a shock hits some units at some time; a comparison group | **DiD** | Parallel trends | `scripts/did.py` |
| Treatment flips at a threshold of a continuous running variable | **RDD** | No manipulation at cutoff | `scripts/rdd.py` |
| Something that shifts treatment but hits the outcome only through it | **IV** | Relevance + exclusion + monotonicity | `scripts/iv.py` |
| Rich covariates driving selection; no shock/threshold/instrument | **PSM** | Selection on observables | `scripts/psm.py` |
| Known structure, want what-if / diagnostic queries | **BBN** | Correct DAG + CPTs | (model in code) |
| Want to encode priors / quantify full uncertainty | **Bayesian** | Prior + likelihood | (model in code) |

If nothing fits, the honest answer is "this is association, not established
causation" plus what evidence would upgrade it. That answer is a success, not a
failure.

## Qualitative & feedback engines (inline — use these, don't just route to them)

Routing to process tracing or a CLD is half the job; the value is the *technique*.

**Process tracing — the discipline is eliminating rivals with classified
evidence, not picking whichever story fits.** For each rival hypothesis, ask:
*if this were the true cause, what evidence MUST exist, and what evidence would
be impossible?* Then classify what you can collect:

| Evidence test | Necessary? | Sufficient? | Found it → | Didn't find it → |
|---|---|---|---|---|
| Straw-in-the-wind | No | No | slightly likelier | slightly less likely |
| **Hoop** | Yes | No | stays alive | **rival ELIMINATED** |
| **Smoking gun** | No | Yes | **rival CONFIRMED** | not eliminated |
| Doubly decisive | Yes | Yes | confirms + kills others | eliminated |

So the output of process tracing is not "the deploy, probably" — it's: *here are
the rivals; here is the hoop test each must pass (e.g. "the cause must precede
the first error in the logs"); collecting evidence E eliminates rivals A and C
and the smoking gun for B is X.* When the call is contested, attach likelihood
ratios (Bayesian process tracing, `references/bayesian-and-systems.md`).

**Causal Loop Diagrams — the polarity and the *delay* are the whole point.** Mark
every loop as Reinforcing (R, self-amplifying) or Balancing (B, self-correcting),
and mark **delays** explicitly. Oscillation, overshoot, and "it keeps coming
back" are the signature of a **balancing loop with a delay**: the correction
arrives late, so the system over-corrects, then over-corrects the other way.
Don't stop at drawing the loop — say which loop dominates when, where the delay
is, and therefore the leverage point (usually: shorten the delay, or act on the
signal before the stock moves). Offer a stock-and-flow simulation when the user
needs magnitude/timing, not just the qualitative story.

## The control-set gate (do not skip)

Before adjusting for any variable, classify its role:
- **Confounder** (common cause of treatment and outcome) → **adjust for it**.
- **Mediator** (on the causal path treatment→outcome) → **do NOT adjust** if you
  want the total effect (you'd block the effect you're measuring).
- **Collider** (common effect of treatment and outcome) → **do NOT adjust**, and
  beware selecting your sample on one — it manufactures fake correlation.

"Control for everything available" is the most common fatal error. Let the DAG
and the back-door criterion choose the adjustment set, not data availability.

## Integrity gate (run when the evidence smells off)

Causal methods assume honest, representative data. When a result is *too good to
be true, oddly clean, gamed, or sourced from scraped/self-reported data*, check
that assumption first — see `references/forensic-integrity.md` for the full
toolkit. The move is the forensic triage:

1. **State the suspicion as a hypothesis + a rough prior** (counters confirmation
   bias in both directions).
2. **Triage the problem:** (A) **fabricated/manipulated** data → digit tests
   (`scripts/benford.py`), granularity impossibility (`scripts/grim.py`),
   too-clean-variance, the Carlisle baseline-balance test; (B) a **hidden/gamed
   cause** → placebo/falsification tests, RDD + McCrary for threshold sorting,
   E-value robustness (`scripts/evalue.py`); (C) **bad/biased data** →
   triangulate against a hard-to-fake external ground truth and interrogate the
   sampling frame.
3. **Layer ≥2 independent tests and demand convergence.** And stay honest the
   other way: an anomaly is "requires explanation," **not** proof of intent —
   honest error, an unusual-but-real process, the prosecutor's fallacy, and
   multiple-comparisons false positives are all live. Promote a flag to a finding
   only on independent, converging, correction-surviving evidence with no benign
   explanation left.

## Output format

This structured report is for data questions. If the user asked for the finding
as a story, keep the same content but tell it using the story shape in `SKILL.md`.

Adapt length to the question — a quick "is this causal?" gets a few sentences,
not the full skeleton — but always keep the reasoning and the validation
visible. The sections branch by answer type; don't force estimand language onto
a single-case or feedback question.

```
## Causal question
<the cause(s), the outcome, the scope, AND what kind of answer this needs:
 a magnitude, a single-case mechanism, or a feedback structure>

## Causal map
<DAG if acyclic (name confounders / mediators / colliders, mark which paths must
 be blocked); CLD if there's feedback (mark each loop R/B and mark delays).
 Render it so assumptions are attackable.>

## Method
<chosen method + one line on why; what was ruled out and why it didn't fit>

## Estimate  — OR —  ## Mechanism
 magnitude: <number + CI + which estimand (ATE/ATT/LATE); state assumptions>
 mechanism: <the rivals; the hoop/smoking-gun test for each; which got
             eliminated vs confirmed by which evidence>
 feedback:  <which loop dominates when, where the delay is, the leverage point>

## Validation
 magnitude: <the falsification test run + result (event study, manipulation
             check, first-stage F, balance/overlap); threats considered>
 mechanism: <did you seek the hoop-test evidence that could KILL the leading
             hypothesis? rivals genuinely specified, not strawmen?>
 feedback:  <does the observed timing/lag match the hypothesized delay?>

## Conclusion
<calibrated claim — strong / suggestive / associational-only / mechanism
 confirmed-vs-likely — and what specific evidence would change it>
```

## Runnable estimators (`scripts/`)

Causal effect estimators — `did.py`, `rdd.py`, `iv.py`, `psm.py` — each runs on
a CSV (see file headers / `--help`) and ships a `--selftest` that recovers a
known synthetic effect. They emit the estimate **and** the diagnostic (event
study, manipulation check, first-stage F, balance/overlap).

Forensic-integrity checks — `benford.py` (digit/last-digit/round-number tests
with Nigrini MAD thresholds), `grim.py` (GRIM/GRIMMER impossibility checks for
reported mean/SD), `evalue.py` (robustness of a result to unmeasured
confounding) — for the integrity gate when the data may be fabricated or gamed.

Requires the libs in `scripts/requirements.txt`
(`pip install -r scripts/requirements.txt`). Prefer these over hand-rolling code
so the diagnostics come for free and consistently.
