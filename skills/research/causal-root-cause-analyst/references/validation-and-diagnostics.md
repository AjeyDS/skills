# Validation and diagnostics

A causal estimate is only as good as the assumption you can defend, so every
analysis must include the falsification test that *could* have shown it wrong.
This is the consolidated checklist. For each method: the key assumption, the
test that interrogates it, and the threats that invalidate the claim.

The mindset: try to break your own result. State what you checked, what would
change the conclusion, and how confident you are after the checks — not just the
number.

## Per-method checklist

### Difference-in-Differences
- **Assumption**: parallel trends (treated and control would have moved together
  absent treatment).
- **Test**: event study — pre-treatment lead coefficients should be ~0 and
  non-significant. Plot them. (`did.py: event_study`)
- **Threats**: diverging pre-trends; staggered adoption + heterogeneous effects
  (naive TWFE bias — the script warns); a time-varying confounder that hits one
  group only (e.g. another policy); anticipation effects before the official
  start; compositional change in who's in each group over time.

### Regression Discontinuity
- **Assumption**: no precise manipulation of the running variable at the cutoff.
- **Tests**: density/manipulation check (`rdd.py: manipulation_check`; confirm
  with McCrary / `rddensity`); covariate smoothness — pre-determined covariates
  should NOT jump at the cutoff; bandwidth sensitivity — estimate stable at 0.5×
  and 2× bandwidth; placebo cutoffs — no jump at fake thresholds away from c.
- **Threats**: sorting/manipulation around c; other policies sharing the same
  cutoff; too few observations in-bandwidth; over-claiming beyond the local
  neighborhood.

### Instrumental Variables
- **Assumption**: relevance, exclusion, monotonicity.
- **Tests**: first-stage F (weak if < 10; `iv.py` reports it); over-identification
  test (Sargan/Hansen) if you have more instruments than endogenous regressors;
  reduced-form sanity check (Z should move Y); plausibility argument for
  exclusion (this is qualitative — write it out).
- **Threats**: weak instrument (bias toward OLS, false precision); exclusion
  violation (Z affects Y through another channel) — the silent killer; defiers
  breaking monotonicity; treating LATE as if it were the ATE.

### Propensity Score Matching
- **Assumption**: selection on observables (no unobserved confounding) + overlap.
- **Tests**: post-match balance — standardized mean differences |SMD| < 0.1 on
  every covariate (`psm.py` reports before/after); common-support / overlap
  inspection (how many treated dropped off support?); sensitivity analysis
  (Rosenbaum bounds): how strong must a hidden confounder be to overturn the
  result?
- **Threats**: unobserved confounding (PSM cannot touch it — always caveat);
  poor overlap; model-dependence of the propensity specification; conditioning a
  covariate that is actually a collider or mediator (re-check roles vs. the DAG).

### DAG-based adjustment (regression/weighting)
- **Assumption**: the DAG is correct and the adjustment set satisfies the
  back-door criterion with all members observed.
- **Tests**: testable implications of the DAG — d-separation predicts certain
  conditional independencies; check them in the data (they can falsify the
  graph); confirm no adjustment-set member is a descendant of treatment
  (collider/mediator guard).
- **Threats**: a missing arrow (unmeasured confounder); a wrongly included
  collider/mediator; reverse causation not encoded.

### Process tracing / Bayesian process tracing
- **Assumption**: the evidence is correctly classified (necessary/sufficient) and
  rival hypotheses are genuinely specified.
- **Tests**: did you actually look for the hoop-test evidence that could
  eliminate H_M? Are likelihood ratios defensible to a skeptic? Is there a rival
  H_A you tried to confirm, not just a strawman?
- **Threats**: confirmation bias (only seeking supporting clues); unstated
  rivals; over-reading a straw-in-the-wind as a smoking gun.

## Cross-cutting threats to always consider
- **Reverse causality**: does Y cause X rather than the reverse? (DiD/RDD/IV all
  help here; plain regression does not.)
- **Selection bias**: was the sample chosen on a collider? (e.g. only studying
  survivors, only converted users.)
- **Measurement error** in treatment or confounders (attenuates or biases).
- **Effect heterogeneity**: whose effect is this (ATE vs ATT vs LATE)? Don't
  generalize a local effect to the whole population.
- **Multiple comparisons / specification search**: did the result survive only
  one of many specifications? Report robustness across reasonable choices.

## Calibrated confidence language
Tie the conclusion to what survived the checks:
- *Strong*: a credible design (RDD/IV/clean DiD) with its key falsification test
  passed and robustness holding.
- *Suggestive*: selection-on-observables (PSM/regression) with good balance but
  unaddressable unobserved confounding, or a single passed test.
- *Associational only*: assumptions cannot be defended — say it is a correlation
  and name what evidence would upgrade it. Refusing to overclaim is part of the
  job.
