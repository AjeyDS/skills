# Forensic integrity: is the evidence real before it's causal?

Read this when a portrayal looks **too good to be true, suspicious, or odd** —
when something "should have been different," a result is implausibly clean or
strong, a metric that's now a target may be gamed, or the data is scraped /
self-reported / strategically reported. Causal methods assume honest data; this
module checks that assumption first. A precise effect estimated on fabricated
data just launders a lie into a confident number.

The whole discipline: **no single test proves fraud or intent.** Tests flag
anomalies and shift probabilities. A defensible verdict comes from *layering
independent tests that converge*, updated with Bayes, while guarding against
false positives. Frame findings as "statistically anomalous, requires
explanation" — never an accusation of intent.

## Contents
- The suspicion → prior → triage workflow
- Triage A: fabricated / manipulated data
- Triage B: hidden / misattributed cause
- Triage C: bad / biased data (incl. online/scraped)
- The epistemics that stop you being naive in the other direction
- Scripts

---

## Suspicion → prior → triage

1. **Name the suspicion as a hypothesis and a rough prior.** What specifically
   looks too good to be true, and what are the rival explanations? Writing the
   prior down disciplines the analysis and blunts confirmation bias.
2. **Triage the problem type** — the answer decides which toolbox to open:
   (A) the data are **fabricated/manipulated**, (B) a real but **hidden cause**
   is producing the surprising pattern, or (C) the data are simply **bad/biased**
   (common with scraped/online/self-reported data). Don't run a Benford test on
   assigned ID numbers, or an instrument when you actually suspect fabrication.
3. **Match tools to the data structure**, run ≥2 independent tests, seek an
   external ground truth, then update and reach a calibrated verdict.

## Triage A — fabricated / manipulated data

Fingerprints of numbers that were invented or doctored rather than observed.

- **Benford's Law (`scripts/benford.py`).** Natural numbers spanning orders of
  magnitude follow P(d)=log₁₀(1+1/d) for the leading digit (1→30.1% … 9→4.6%).
  Judge conformity by **Nigrini's MAD** (mean absolute deviation), *not*
  chi-square (which over-rejects on big samples): first-digit MAD <0.006 close,
  <0.012 acceptable, <0.015 marginal, >0.015 a red flag. Caveats that matter:
  doesn't apply to assigned IDs / bounded ranges / capped values; it flagged
  Greek deficit data but *failed* on Wirecard (few fabricated entries in a huge
  set barely move the distribution); a sophisticated fabricator can mimic it.
  Conformity is not innocence.
- **Last-digit / round-number (`benford.py last_digit`).** Terminal digits of
  large counts should be ~uniform. Excess 0s/5s = human rounding (often benign);
  *suspiciously flat* uniformity where rounding is expected = possible
  random-number-generator fabrication (the Gino/Ariely tell).
- **GRIM / GRIMMER (`scripts/grim.py`).** Pure arithmetic: a mean of N integers
  must be a multiple of 1/N; a reported mean (or mean+SD) that no integer dataset
  of that N can produce is *mathematically impossible*. Powerful on small N,
  granular (Likert) scales, several reported decimals.
- **SPRITE** (not scripted): reconstruct datasets consistent with a reported
  mean/SD/N/bounds; if the only possibilities are bizarre (impossible bimodal
  shapes), the stats are wrong/fabricated.
- **Carlisle method** (RCT baseline tables): in real randomization, baseline
  comparison p-values are uniform; clustering near 0 (too imbalanced) or near 1
  (**too balanced — "too good to be true"**) signals fabrication. Works better on
  sets of trials than one trial (baseline vars are correlated).
- **Variance forensics — TIVA** and "too-clean" data: across independent studies,
  z-scores should have variance ≥1; variance well below 1 means results are *too
  consistent* (selective reporting / QRPs).
- **p-curve & statcheck** (literatures): a real effect right-skews significant
  p-values; p-hacking flattens or left-skews them near .05. statcheck recomputes
  reported p-values and catches inconsistencies.
- **Domain scores** (financial): **Beneish M-Score** > −1.78 flags earnings
  manipulation; **Altman Z** < 1.81 distress; **Dechow F** > 1 above-base-rate
  misstatement; **Montier C** sums six "cooking the books" flags. Rules of thumb,
  not constants.

## Triage B — hidden / misattributed cause

The surprising pattern is real but not what it's portrayed as. These are the
bundle's causal tools, used adversarially (full detail in
`quasi-experimental.md`):
- **Placebo / falsification is the unifying logic** — apply your method where the
  effect should be zero (pre-treatment periods, untreated units, fake cutoffs);
  finding an "effect" there means the design (or the claim) is broken.
- **IV** isolates exogenous variation to expose a confounded/gamed "effect";
  **RDD + McCrary density test** catches strategic sorting at a threshold (a
  pile-up just past a cutoff = gaming, e.g. firms/cities maneuvering across a
  rule); **DiD pre-trend tests**; **synthetic control** with permutation placebos.
- **E-value (`scripts/evalue.py`) / Rosenbaum bounds** quantify the "too good to
  be true" instinct directly: how strong would a hidden confounder have to be to
  explain the result away? Small E-value = fragile.
- **Goodhart/Campbell watch:** when a measure becomes a target it stops measuring
  — a metric that improved suspiciously fast right after it started being tracked
  or incentivized is a prime gaming suspect.

## Triage C — bad / biased data (incl. online/scraped)

The data may be honest but unrepresentative or corrupted at the source.
- **Triangulate against an external ground truth** that's "hard to fake": night-
  lights luminosity vs. reported GDP, web-scraped prices vs. official CPI (the
  Billion Prices Project caught Argentina's CPI manipulation), the Li Keqiang
  index. Disagreement among sources that *should* agree signals error or manipulation.
- **Interrogate the sampling frame:** who/what is in the data and who's missing?
  Survivorship and selection at the collection step are a collider by another name.
- **Online/engagement fraud:** bots, fake reviews, click fraud show up as
  duplicate/copy-paste fingerprints, timing bursts, and lockstep account clusters
  (network/graph anomalies) — distributional checks plus graph structure.

## The epistemics (so you're not naive in the *other* direction)

Being skeptical of fraud naively is its own failure mode. Guard against it:
- **Anomaly ≠ intent.** A flag is consistent with fraud, honest error, an
  unusual-but-real process, or bad methodology (Reinhart-Rogoff was an Excel
  error, not fraud). Report "requires explanation," not "guilty."
- **Prosecutor's fallacy.** P(anomaly | innocent) ≠ P(innocent | anomaly). A
  1-in-1,000 false-positive test on 10,000 honest datasets yields ~10 false
  accusations. The base rate of fraud must enter the Bayesian update.
- **Multiple comparisons.** Running many forensic tests manufactures the very
  false positives you're hunting (20 tests at α=.05 → ~1 "hit" by chance).
  Pre-specify tests; correct with Bonferroni/FDR.
- **Absence of evidence ≠ evidence of absence** *unless the test was powerful*. A
  passed hoop test keeps a hypothesis alive; it doesn't clear it.
- **The escalation standard:** a single anomaly is a *lead*, not a conclusion.
  Promote to a "case" only on ≥2 independent, individually-unlikely-under-innocence
  anomalies that converge AND survive correction AND have no benign explanation —
  the quantitative analog of combining smoking guns into a doubly-decisive verdict
  (see process tracing in `qualitative-mapping.md`). Always let the accused respond.

## Scripts
- `scripts/benford.py` — Benford (MAD), last-digit uniformity, round-number bias,
  applicability check.
- `scripts/grim.py` — GRIM / GRIMMER impossibility checks for reported mean / SD.
- `scripts/evalue.py` — E-value robustness to unmeasured confounding.
(IV/RDD-McCrary/DiD/synthetic-control placebos live in `scripts/` + `quasi-experimental.md`.)
