# Qualitative logic and mapping

Read this to build the *structure* of the problem before touching estimators:
to draw the DAG that tells you what to control for, to map feedback systems that
DAGs can't represent, or to root-cause a single case from evidence.

## Contents
- DAGs and d-separation (what to control for)
- Back-door and front-door criteria (identification strategies)
- Causal Loop Diagrams (feedback systems)
- Process tracing (single-case mechanism + the four evidence tests)

---

## Directed Acyclic Graphs (DAGs)

A DAG is the formal language for stating causal assumptions: nodes are
variables, arrows are direct causes, and "acyclic" means nothing causes itself
through a loop. Its value is that it makes your assumptions *visible and
falsifiable* and then mechanically tells you which variables to adjust for.
Draw it before estimating. When presenting, render it (Mermaid or a diagram
tool) so the reader can attack the assumptions.

**d-separation** governs whether association flows along a path:
- A **chain** (A → B → C) or a **fork** (A ← B → C) transmits association, and
  is **blocked by conditioning on the middle node B**.
- A **collider** (A → B ← C) is **naturally blocked**, and is **opened by
  conditioning on B** (or any descendant of B, including by sample selection).

A path is *open* if every node on it is a non-collider you did not condition on,
plus every collider you DID condition on. The treatment→outcome effect is
identified when every non-causal (back-door) path is blocked and the causal path
is left open.

### Back-door criterion (the usual identification route)
A set Z is sufficient to identify the effect of T on Y if Z blocks every path
from T to Y that starts with an arrow *into* T (the back-door, confounding
paths) and Z contains **no descendant of T** (which would risk conditioning on a
mediator or collider). If such a Z is fully observed, adjust for it (regression,
matching, weighting) and you are done. The whole game in observational inference
is finding an observed, valid back-door set.

### Front-door criterion (when confounders are unobserved)
If an unmeasured confounder makes the back-door impossible, but there is a
mediator M fully on the path T → M → Y that is *shielded* from the confounder,
you can still identify the effect in two stages: estimate T → M, estimate
M → Y (adjusting for T), and compose them. Rare in practice because the shielded
mediator is demanding, but it is the canonical answer to "everything is
confounded, am I stuck?" — sometimes you are not.

## Causal Loop Diagrams (CLDs)

DAGs forbid cycles, but many real systems — economies, ecosystems, epidemics,
product growth, team dynamics — *are* feedback. A CLD maps variables with signed
arrows that form closed loops:
- **Reinforcing (R) loop**: a change amplifies itself. Engine of exponential
  growth or collapse (more users → more content → more users; or debt →
  interest → more debt).
- **Balancing (B) loop**: a change triggers a counter-response toward
  equilibrium (price rises → demand falls → price settles).
- **Delays**: lags between cause and effect. Delays are why systems *overshoot*
  and oscillate — actors over-correct because the feedback hasn't arrived yet.
  Always mark them; they are usually where the surprising behavior comes from.

Use a CLD when the root-cause story has loops ("the metric drop fed on
itself"), when intervention timing matters, or as the qualitative front end to a
System Dynamics simulation (see `bayesian-and-systems.md`). A CLD finds
high-leverage intervention points and likely unintended consequences; it does
not give magnitudes — that needs the stock-and-flow model.

## Process tracing (single-case root cause)

When you have *one* case and need the actual mechanism — "why did THIS outage /
deal / outbreak / decision happen?" — statistics on a population won't help.
Process tracing opens the black box: assemble fine-grained diagnostic evidence
("causal-process observations") along the hypothesized chain and use it to
confirm or eliminate explanations, like a detective.

The discipline comes from classifying each piece of evidence by what passing or
failing it implies. Necessary = the hypothesis *requires* this evidence to
exist; Sufficient = this evidence *alone* would confirm it.

| Test | Necessary? | Sufficient? | Pass implies | Fail implies |
|---|---|---|---|---|
| **Straw-in-the-wind** | No | No | Slightly raises plausibility | Slightly lowers it; eliminates nothing |
| **Hoop** | Yes | No | Stays alive (not confirmed) | **Eliminated** — failed a necessary condition |
| **Smoking gun** | No | Yes | **Confirmed** | Not eliminated — other paths possible |
| **Doubly decisive** | Yes | Yes | Confirms AND eliminates rivals | Eliminated |

Detective intuition: a receipt hinting at motive = straw-in-the-wind; a verified
alibi placing the suspect elsewhere = a failed hoop test (guilt eliminated); the
suspect holding the smoking weapon = smoking gun (guilt confirmed, but its
absence proves nothing).

To make this rigorous rather than vibes, formalize with **Bayesian process
tracing**: state a prior odds on hypothesis H_M vs. a rival H_A, and for each
clue E compute the likelihood ratio `P(E|H_M) / P(E|H_A)` — the clue's probative
weight. A hoop test is evidence near-certain under H_M; failing to find it drives
the ratio toward 0 and kills H_M regardless of prior. A smoking gun is evidence
near-impossible under H_A; finding it sends the ratio toward infinity. This turns
narrative into an auditable calculation and is the right tool when stakeholders
will contest the conclusion. Details in `bayesian-and-systems.md`.
