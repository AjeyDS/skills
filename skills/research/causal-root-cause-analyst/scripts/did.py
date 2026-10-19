"""
Difference-in-Differences (DiD) estimator.

DiD identifies a causal effect by comparing the change in a treated group
against the change in a control group. It differences out any time-invariant
difference between the groups and any common time shock. The identifying
assumption is PARALLEL TRENDS: absent treatment, the two groups would have
moved in parallel. This script estimates the effect AND helps you interrogate
that assumption with an event study (pre-trend test), because a DiD point
estimate is meaningless if you cannot defend parallel trends.

Two entry points:
  - did_twfe(...)      : two-way fixed-effects DiD on a long panel.
  - event_study(...)   : leads/lags around the treatment time to inspect
                         pre-trends (falsification) and dynamic effects.

IMPORTANT CAVEAT (staggered adoption): if different units are treated at
different times AND effects are heterogeneous, the naive TWFE estimator can be
badly biased (it uses already-treated units as controls and can put negative
weights on cohorts, even flipping the sign). This script detects staggered
timing and warns you. In that case prefer a modern estimator
(Callaway & Sant'Anna, de Chaisemartin & D'Haultfoeuille, Sun & Abraham,
Borusyak et al.) rather than trusting the single TWFE coefficient.

CLI:
  python did.py data.csv --outcome y --unit firm --time year --treat-post D
  python did.py --selftest
"""
from __future__ import annotations
import argparse
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def _detect_staggered(df: pd.DataFrame, unit: str, time: str, treat_post: str) -> dict:
    """Find, per unit, the first period where treat_post == 1. Multiple distinct
    first-treatment times => staggered adoption."""
    treated_rows = df[df[treat_post] == 1]
    if treated_rows.empty:
        return {"staggered": False, "adoption_times": [], "never_treated": int(df[unit].nunique())}
    first_treat = treated_rows.groupby(unit)[time].min()
    adoption_times = sorted(first_treat.unique().tolist())
    n_units = df[unit].nunique()
    n_treated_units = first_treat.index.nunique()
    return {
        "staggered": len(adoption_times) > 1,
        "adoption_times": adoption_times,
        "never_treated": int(n_units - n_treated_units),
    }


def did_twfe(df, outcome, unit, time, treat_post, cluster=None):
    """Two-way fixed-effects DiD.

    treat_post is a 0/1 column equal to 1 only for treated units in post periods
    (i.e. the interaction Treated x Post). Returns the coefficient on treat_post,
    which is the DiD/ATT estimate under parallel trends, with cluster-robust SEs.
    """
    cluster = cluster or unit
    d = df[[outcome, unit, time, treat_post]].dropna().copy()
    info = _detect_staggered(d, unit, time, treat_post)

    formula = f"{outcome} ~ {treat_post} + C({unit}) + C({time})"
    model = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[cluster]}
    )
    coef = model.params[treat_post]
    se = model.bse[treat_post]
    ci = model.conf_int().loc[treat_post].tolist()
    return {
        "estimate": float(coef),
        "std_error": float(se),
        "t_stat": float(coef / se) if se else np.nan,
        "p_value": float(model.pvalues[treat_post]),
        "ci_95": [float(ci[0]), float(ci[1])],
        "n_obs": int(model.nobs),
        "staggered_adoption": info["staggered"],
        "adoption_times": info["adoption_times"],
        "never_treated_units": info["never_treated"],
        "warning": (
            "STAGGERED ADOPTION DETECTED. The TWFE coefficient may be biased under "
            "heterogeneous effects. Use a modern estimator (Callaway-Sant'Anna, "
            "de Chaisemartin-D'Haultfoeuille, Sun-Abraham, Borusyak et al.) and "
            "treat this number as a diagnostic only."
            if info["staggered"] else None
        ),
    }


def event_study(df, outcome, unit, time, cohort_time, treat_group,
                lead_lags=(-4, 4), ref=-1, cluster=None):
    """Event-study DiD. Estimates effects at each relative period k = time - cohort_time
    for treated units, omitting k = ref (usually -1) as the baseline.

    Pre-period coefficients (k < 0) should be ~0 if parallel trends holds; that is
    your falsification test. Post-period coefficients trace the dynamic effect.

    treat_group: 0/1 column, 1 if the unit is ever treated.
    cohort_time: the period in which the unit became treated (NaN/<=0 for never-treated).
    """
    cluster = cluster or unit
    d = df.copy()
    d["_rel"] = np.where(d[treat_group] == 1, d[time] - d[cohort_time], np.nan)
    lo, hi = lead_lags
    d["_rel"] = d["_rel"].clip(lower=lo, upper=hi)

    terms = []
    for k in range(lo, hi + 1):
        if k == ref:
            continue
        name = f"k_m{abs(k)}" if k < 0 else f"k_p{k}"
        d[name] = ((d["_rel"] == k) & (d[treat_group] == 1)).astype(int)
        terms.append((k, name))

    rhs = " + ".join(n for _, n in terms)
    formula = f"{outcome} ~ {rhs} + C({unit}) + C({time})"
    model = smf.ols(formula, data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d[cluster]}
    )

    out = []
    for k, name in terms:
        out.append({
            "rel_period": k,
            "estimate": float(model.params[name]),
            "std_error": float(model.bse[name]),
            "p_value": float(model.pvalues[name]),
            "is_pre": k < 0,
        })
    pre = [r for r in out if r["is_pre"]]
    max_pre = max((abs(r["estimate"]) for r in pre), default=0.0)
    return {
        "reference_period": ref,
        "coefficients": out,
        "pretrend_concern": bool(any(r["p_value"] < 0.05 for r in pre)),
        "largest_pre_estimate": float(max_pre),
        "note": ("At least one pre-period effect is significant at 5%: parallel "
                 "trends is in doubt." if any(r["p_value"] < 0.05 for r in pre)
                 else "No significant pre-trends detected (necessary, not sufficient)."),
    }


def _selftest():
    rng = np.random.default_rng(7)
    units, periods = 60, 8
    treat_start = 5
    rows = []
    for u in range(units):
        treated = u < 30
        ui = rng.normal(0, 1)
        for t in range(periods):
            te = 0.4 * t  # common trend (parallel)
            post = t >= treat_start
            effect = 2.0 if (treated and post) else 0.0
            y = 3 + ui + te + effect + rng.normal(0, 0.5)
            rows.append({"y": y, "firm": u, "year": t,
                         "D": int(treated and post),
                         "ever": int(treated),
                         "cohort": treat_start if treated else np.nan})
    df = pd.DataFrame(rows)
    res = did_twfe(df, "y", "firm", "year", "D")
    print("DiD estimate (true=2.0):", round(res["estimate"], 3),
          "95% CI", [round(c, 3) for c in res["ci_95"]])
    es = event_study(df, "y", "firm", "year", "cohort", "ever", lead_lags=(-3, 2))
    print("Pre-trend concern:", es["pretrend_concern"], "|", es["note"])
    assert 1.5 < res["estimate"] < 2.5, "self-test failed"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="Difference-in-Differences")
    ap.add_argument("data", nargs="?", help="CSV path (long panel)")
    ap.add_argument("--outcome"); ap.add_argument("--unit")
    ap.add_argument("--time"); ap.add_argument("--treat-post", dest="treat_post")
    ap.add_argument("--cluster", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if not (a.data and a.outcome and a.unit and a.time and a.treat_post):
        ap.error("need data, --outcome, --unit, --time, --treat-post")
    df = pd.read_csv(a.data)
    res = did_twfe(df, a.outcome, a.unit, a.time, a.treat_post, a.cluster)
    import json; print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
