# Foundations: what a causal claim requires

Read this when you need to define the estimand precisely, decide what to control
for, judge whether identification is even possible, or when the structure is
unknown and must be discovered from data.

## Contents
- The potential-outcomes frame and what you can actually estimate
- The assumptions every observational claim leans on
- Confounder / collider / mediator — the control-set decision
- Causal inference vs. causal discovery
- Discovery algorithms at a glance

---

## The potential-outcomes frame (Rubin Causal Model)

For a unit `i` and a binary treatment `D_i ∈ {0,1}`, imagine two potential
outcomes: `Y_i(1)` if treated, `Y_i(0)` if not. The unit-level effect is
`Y_i(1) − Y_i(0)`. The catch — the "fundamental problem of causal inference" —
is that you only ever observe one of them. The other is counterfactual. So you
cannot get an individual effect; you estimate population averages by comparing
groups that stand in for each other's missing half.

The two estimands you will name most often:
- **ATE** = `E[Y(1) − Y(0)]` — average effect across the whole population.
- **ATT** = `E[Y(1) − Y(0) | D = 1]` — average effect among the treated. This is
  usually what matching and DiD give you, and often what a decision-maker
  actually wants ("did the program help the people who took it?").
- **LATE / CACE** — the effect for *compliers* only. This is what IV and fuzzy
  RDD recover. It is not the ATE; be explicit that it generalizes only to the
  subpopulation the instrument or threshold actually moved.

Always pin down the estimand before choosing a method. "Does X cause Y?" is
under-specified. "What is the ATT of X on Y for this population over this
horizon?" tells you which method can answer it.

## The assumptions every observational claim leans on

These are the load-bearing assumptions. If one fails, the estimate is not
causal no matter how clean the regression looks. Name them explicitly in every
analysis and say which are testable.

- **SUTVA**, two parts:
  - *No interference*: one unit's outcome is unaffected by others' treatment.
    Violated by spillovers — contagion, network effects, market equilibria,
    word-of-mouth. If treating one user changes an untreated user's behavior,
    SUTVA breaks and naive comparisons are contaminated.
  - *Consistency / no hidden versions of treatment*: "the treatment" is one
    well-defined thing. If "received the drug" hides wildly varying doses, the
    counterfactual is ambiguous and the effect is ill-defined.
- **Conditional exchangeability (ignorability)**: given measured covariates X,
  treatment is independent of the potential outcomes —
  `(Y(1), Y(0)) ⊥ D | X`. In plain terms: once you adjust for X, who got
  treated is as-good-as-random. This is the big one, and it is **untestable**.
  Unmeasured confounding is exactly its failure.
- **Positivity / overlap**: every covariate profile has a non-zero chance of
  both treatment and control, `0 < P(D=1 | X=x) < 1`. Without overlap the model
  extrapolates into regions with no data. This one IS checkable (inspect the
  propensity-score distributions; look for common support).

## Confounder / collider / mediator — the control-set decision

This single distinction prevents the most common fatal error in applied causal
work: "control for everything you can measure." That is wrong. What you adjust
for is dictated by the variable's role, not its availability.

- **Confounder** — a common cause of *both* treatment and outcome (T ← C → Y).
  It opens a spurious back-door path. You **must** adjust for it. Classic case:
  age drives both income and cancer risk; omit it and you mistake age's effect
  for income's (omitted-variable bias).
- **Mediator** — sits *on* the causal path (T → M → Y); it is how the treatment
  works. If you want the **total** effect, **do not** control for it —
  conditioning on a mediator blocks part of the very effect you are measuring.
  (You adjust for it only when you deliberately want the *direct* effect in a
  mediation analysis.)
- **Collider** — a common *effect* of two variables (T → K ← Y). A collider is
  naturally blocked, so it transmits nothing — until you condition on it (or on
  its descendant, or by selecting your sample on it), which **opens** a spurious
  path and manufactures a correlation that isn't real. This is collider /
  selection bias. The "low-birthweight paradox" is the textbook example:
  conditioning on a collider produces a statistically robust but physiologically
  false finding.

Operational rule: draw the graph first (see `qualitative-mapping.md`), then let
the back-door criterion tell you the adjustment set. Controlling for a collider
or a mediator is worse than omitting a confounder, because it introduces bias
that looks like signal.

## Causal inference vs. causal discovery

Two different jobs:
- **Inference (deductive)**: you already have a hypothesized structure (a DAG, a
  treatment, an outcome) and you want to *estimate the magnitude* of a known
  effect. Everything in `quasi-experimental.md` is inference.
- **Discovery (inductive)**: you do *not* know the structure and want to learn
  it from data — which variables cause which. Use this to generate hypotheses,
  then validate them; do not treat a discovered edge as a confirmed cause
  without theory and, ideally, an experiment or quasi-experiment.

## Discovery algorithms at a glance

| Algorithm | Family | Key assumptions | What it does / when |
|---|---|---|---|
| **PC** | Constraint-based | Causal sufficiency (no hidden confounders), Markov, faithfulness | Prunes a fully-connected graph via conditional-independence tests; returns a Markov-equivalence class (some edges undirected). Fast, but assumes you measured all common causes. |
| **FCI** | Constraint-based | Markov, faithfulness; **allows latent confounders** | Generalizes PC to tolerate unobserved common causes. More robust, more computationally expensive. Prefer when hidden confounding is plausible (usually). |
| **LiNGAM** | Functional / SEM | Linear effects, **non-Gaussian** noise, acyclic, no hidden confounders | Uses independent component analysis; the non-Gaussianity lets it orient edge *direction* without time order. Powerful when its functional assumptions hold. |

All discovery output is a hypothesis. Validate against domain theory and the
variable taxonomy above before promoting any edge to a causal claim.
