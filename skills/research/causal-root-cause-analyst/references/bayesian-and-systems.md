# Bayesian methods, system dynamics, and integration frameworks

Read this when you need to fold in prior knowledge and quantify uncertainty
(Bayesian), build a probabilistic model over a known DAG (BBN), simulate a
feedback system over time (system dynamics), or deliberately combine qualitative
and quantitative evidence (Bayesian process tracing, nested analysis).

## Contents
- Bayesian inference for causal questions
- Bayesian Belief Networks (BBNs)
- Bayesian process tracing (qual + quant on a single case)
- System dynamics (quantifying feedback systems)
- Nested analysis (large-N + small-N)

---

## Bayesian inference for causal questions

Frequentist inference treats probability as long-run frequency and leans on
p-values. Bayesian inference treats probability as degree of belief, updated by
evidence via Bayes' theorem: `posterior ∝ likelihood × prior`. Three pieces —
the **prior** (what you believed before, where domain knowledge and
regularization enter), the **likelihood** (how probable the data is under each
parameter value), and the **posterior** (the updated belief).

Why it suits causal work: it models uncertainty explicitly (you get a full
distribution over the effect, not just a point and a CI), and it gives a
principled channel for prior knowledge — valuable with sparse data or
measurement error. Caveat: specifying high-dimensional models for nuisance
parameters (like a propensity score) can induce *regularization-induced
confounding*. Modern remedy: **generalized Bayes** — put the prior directly on
the causal estimand (e.g. the ATE) and update with an identification-driven loss
instead of a full likelihood, marrying ML flexibility to Bayesian uncertainty.

## Bayesian Belief Networks (BBNs)

A BBN is a DAG with the probabilities filled in: each node carries a conditional
probability table given its parents, so the graph defines the full joint
distribution as `P(U) = Π P(X_i | parents(X_i))`. It turns the qualitative DAG
into a computational engine.

What BBNs let you do:
- **Learn** structure and/or parameters from data.
- **Update / diagnose**: observe evidence at any node and propagate it
  backward and forward to update beliefs about every other node — including
  unobserved latent ones. Good for "given these symptoms, what's the most likely
  cause?" reasoning.
- **Counterfactual / interventional queries** via Pearl's do-operator: simulate
  "what if we forced X to this value?" — distinct from merely observing X at that
  value, which is the whole point of causal (vs. predictive) modeling.

Use a BBN when the structure is known (or learnable), variables are discrete or
discretizable, and you want to answer many what-if and diagnostic queries over
the same system.

## Bayesian process tracing (qual + quant, single case)

The rigorous version of process tracing (see `qualitative-mapping.md`). Work in
odds form:

```
P(H_M | E)     P(E | H_M)     P(H_M)
----------  =  ----------  ×  ------
P(H_A | E)     P(E | H_A)     P(H_A)
```

The engine is the **likelihood ratio** `P(E|H_M)/P(E|H_A)` — the probative weight
of clue E for your main hypothesis H_M against rival H_A. It maps onto the four
tests: a **hoop** test is evidence near-certain under H_M (`P(E|H_M)≈1`) but
uncertain under H_A — fail to find it and the ratio collapses toward 0, killing
H_M whatever the prior. A **smoking gun** is evidence near-impossible under H_A
(`P(E|H_A)≈0`) — find it and the ratio explodes, confirming H_M. This converts
archives, interviews, and logs into a transparent, reproducible calculation, and
is the right call when the conclusion will be contested and you must show your work.

## System dynamics (quantifying feedback)

Where a CLD is the qualitative map, a system-dynamics model is the running
simulation. Reformulate the loops as **stocks** and **flows**:
- **Stocks** = accumulations (population, cash balance, infected count). A stock
  is the integral of its net flow: `Stock(t) = Stock(0) + ∫ (inflow − outflow) dt`.
- **Flows** = rates that fill or drain stocks (births/deaths, deposits, infection
  rate), modulated by constants, auxiliaries, and feedback from the stocks.

Because the coupled nonlinear ODEs rarely have closed-form solutions, you
integrate numerically (Euler, Runge-Kutta) over small time steps. The payoff:
you can see *magnitude and timing* — exponential overshoot, oscillation, the
moment an intervention has maximum leverage — which a static CLD cannot give.
Use it for policy/epidemic/market dynamics where timing and nonlinearity matter.
(If you need to actually simulate, a small `scipy.integrate.odeint` / `solve_ivp`
model is usually enough; build the stock-flow equations from the CLD.)

## Nested analysis (large-N + small-N)

Lieberman's framework for combining a large-N statistical analysis (LNA) with
small-N case studies (SNA) so each fixes the other's weakness. The key move: the
regression's results *dictate* which cases to trace and why.

- If the LNA is **robust and well-specified** → **model-testing** mode: pick
  *on-the-line* cases (ones the model predicts well) and process-trace them to
  confirm the mechanism is real, not spurious or reverse-causal.
- If the LNA is **weak or contradictory** → **model-building** mode: pick
  *off-the-line* outliers (cases the model gets wrong) and trace them to find the
  omitted variable or interaction, then re-specify the quantitative model.

This cures the external-validity weakness of lone case studies while opening the
"black box" that regression alone leaves closed. Reach for it on big questions
where you have both a dataset and access to specific cases — and where a single
number won't satisfy the audience without a mechanism story behind it.
