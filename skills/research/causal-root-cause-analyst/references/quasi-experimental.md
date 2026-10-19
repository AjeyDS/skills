# Quantitative measurement: quasi-experimental designs

Read this to estimate the *magnitude* of an effect from observational data when
you cannot run an RCT. Each method buys identification with a different
assumption and exploits a different feature of the data. Match the method to the
structure you actually have — picking the design is the hard part; the
estimation is bundled in `scripts/`.

## Contents
- Which design fits which data
- Difference-in-Differences (DiD) — `scripts/did.py`
- Regression Discontinuity (RDD) — `scripts/rdd.py`
- Instrumental Variables (IV) — `scripts/iv.py`
- Propensity Score Matching (PSM) — `scripts/psm.py`

---

## Which design fits which data

| You have... | Use | Identifying assumption (the thing to defend) | Estimand |
|---|---|---|---|
| Panel data; a policy/shock hits some units at some time; a comparison group | **DiD** | Parallel trends (groups would have moved together absent treatment) | ATT |
| Treatment switches at a threshold of a continuous "running" variable | **RDD** | No precise manipulation of the running variable at the cutoff | LATE at cutoff |
| A variable that shifts treatment but affects outcome only through it | **IV** | Relevance + exclusion + monotonicity | LATE (compliers) |
| Rich covariates that drive selection; no shock/threshold/instrument | **PSM** | Selection on observables (no unobserved confounding) | ATT |

If none fit, you may be stuck with association — say so plainly rather than
dressing a correlation up as a cause.

## Difference-in-Differences — `scripts/did.py`

Compares the *change* in a treated group to the *change* in a control group,
differencing out time-invariant group differences and common time shocks.

- **Identification rests entirely on parallel trends.** A point estimate without
  a parallel-trends defense is not evidence. Test it with the event study
  (`event_study`): pre-treatment lead coefficients should be ~0. Significant
  pre-trends = the control group is not a valid counterfactual.
- **Staggered-adoption trap**: if units adopt at different times AND effects are
  heterogeneous, naive two-way fixed effects (TWFE) is biased — it uses
  already-treated units as controls and can apply negative weights, even
  flipping the sign so a beneficial policy looks harmful. `did.py` detects
  staggered timing and warns. When warned, use a modern estimator
  (Callaway & Sant'Anna, de Chaisemartin & D'Haultfoeuille, Sun & Abraham,
  Borusyak et al.) — the script's TWFE number becomes a diagnostic, not the answer.
- Cluster standard errors by unit (the script does this by default).

## Regression Discontinuity — `scripts/rdd.py`

Units just below the cutoff are a credible counterfactual for those just above,
because treatment flips at the threshold while everything else varies smoothly.

- **Sharp** RDD: crossing the cutoff deterministically assigns treatment
  (`sharp_rdd`). **Fuzzy** RDD: crossing only changes the *probability* of
  treatment — estimated as IV with "above cutoff" instrumenting for treatment
  (`fuzzy_rdd`).
- **The decisive assumption is no precise manipulation** of the running
  variable. If units can sort themselves across the cutoff, the jump is
  selection, not effect. Run `manipulation_check` (a fast density screen;
  confirm with the McCrary test / `rddensity` for anything serious) and check
  that pre-determined covariates are smooth at the cutoff.
- **Bandwidth** is a bias/variance trade-off: narrow = less bias, less power;
  wide = more power, more bias. The estimate should be stable when you halve and
  double the bandwidth — report that sensitivity. A triangular kernel
  up-weights points near the cutoff (built in).
- **External validity is local**: the LATE applies only near the cutoff. Don't
  extrapolate to units far from it.

## Instrumental Variables — `scripts/iv.py`

Isolates exogenous variation in an endogenous treatment via an instrument Z that
moves treatment but touches the outcome only through treatment. 2SLS uses the
Z-predicted part of treatment.

- Three assumptions: **Relevance** (testable: first-stage F — rule of thumb
  F < 10 means a *weak instrument*, biasing 2SLS toward OLS with deceptively
  tight CIs; the script flags it), **Exclusion** (untestable — argue that Z has
  no other path to Y), **Monotonicity** (untestable — no defiers).
- The estimate is a **LATE on compliers**, larger in magnitude than the raw
  intent-to-treat because it scales ITT up by the (sub-1) complier share
  (Wald estimator, `wald`). It does not describe always-takers or never-takers.
- Be ruthless about the exclusion restriction; it is where most IV claims die.

## Propensity Score Matching — `scripts/psm.py`

Collapses many covariates into one balancing score e(X) = P(treat | X) and
matches treated to control units with similar scores, reproducing experiment-like
balance *on observables*.

- Pipeline (all in `psm_att`): logistic propensity → match on the **logit** of
  the score within a **caliper of 0.2 × SD(logit)** (the Monte-Carlo-supported
  width) → enforce **common support** (drop treated units with no control in
  caliper; the ATT then applies only to the on-support region) → check
  **balance** via standardized mean differences (target |SMD| < 0.1 after
  matching) → estimate ATT.
- With vs. without **replacement**: with replacement lowers bias (best control
  can match many treated), without raises precision (more unique controls). The
  script defaults to with-replacement.
- **The fundamental limitation**: PSM removes only *overt* bias from measured
  covariates. It cannot detect or fix unobserved confounding. Every PSM
  conclusion must carry that caveat and ideally a sensitivity analysis
  (e.g. Rosenbaum bounds: how strong would a hidden confounder have to be to
  overturn this?).

---

## Running the scripts

Each script self-tests on synthetic data with a known effect:
```bash
python scripts/did.py --selftest
python scripts/rdd.py --selftest
python scripts/iv.py  --selftest
python scripts/psm.py --selftest
```
On real data, pass a CSV and column names (see each file's header / `--help`).
Requires: numpy, pandas, scikit-learn, scipy, statsmodels (see
`scripts/requirements.txt`).
