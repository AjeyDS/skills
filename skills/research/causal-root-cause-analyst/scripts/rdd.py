"""
Regression Discontinuity Design (RDD) estimator.

RDD exploits a threshold: units just below the cutoff on a continuous running
variable are treated as a credible counterfactual for units just above it,
because near the cutoff treatment status flips while everything else varies
smoothly. The estimate is a LOCAL effect at the cutoff (LATE), so external
validity is limited to that neighborhood.

This implements:
  - sharp_rdd(...) : local linear regression with a triangular kernel on each
                     side of the cutoff within a bandwidth; the jump at the
                     cutoff is the estimate.
  - fuzzy_rdd(...) : when crossing the cutoff only shifts treatment PROBABILITY
                     (imperfect compliance); estimated as IV/Wald = (jump in
                     outcome) / (jump in treatment).
  - manipulation_check(...) : a simplified density test for sorting/manipulation
                     around the cutoff (the core RDD threat). For publication
                     use the McCrary test / `rddensity`; this is a fast screen.

The decisive RDD assumption is that units cannot precisely manipulate the
running variable to sort themselves across the cutoff. If they can, the jump
reflects selection, not the treatment. Always run manipulation_check and inspect
covariate balance at the cutoff before trusting the estimate.

CLI:
  python rdd.py data.csv --outcome y --running x --cutoff 0 --bandwidth 0.5
  python rdd.py --selftest
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd


def _triangular_weights(x, c, h):
    return np.clip(1.0 - np.abs(x - c) / h, 0.0, None)


def _rot_bandwidth(x, c):
    """Rule-of-thumb bandwidth: Silverman-ish scaled by spread near cutoff.
    A pragmatic default when the user gives none; report it and try alternatives."""
    s = np.std(x)
    n = len(x)
    return 1.84 * s * n ** (-1 / 5)


def _wls_jump(y, x, c, h):
    """Weighted local linear on both sides; returns intercept jump at cutoff."""
    w = _triangular_weights(x, c, h)
    m = w > 0
    xx, yy, ww = x[m], y[m], w[m]
    right = (xx >= c).astype(float)
    xc = xx - c
    X = np.column_stack([np.ones_like(xc), right, xc, right * xc])
    W = np.diag(ww)
    XtW = X.T @ W
    beta = np.linalg.solve(XtW @ X, XtW @ yy)
    # robust-ish SE
    resid = yy - X @ beta
    bread = np.linalg.inv(XtW @ X)
    meat = X.T @ np.diag(ww ** 2 * resid ** 2) @ X
    cov = bread @ meat @ bread
    return beta[1], np.sqrt(cov[1, 1]), int(m.sum())


def sharp_rdd(df, outcome, running, cutoff=0.0, bandwidth=None):
    d = df[[outcome, running]].dropna()
    y = d[outcome].to_numpy(float); x = d[running].to_numpy(float)
    h = bandwidth or _rot_bandwidth(x, cutoff)
    jump, se, n_eff = _wls_jump(y, x, cutoff, h)
    return {
        "design": "sharp",
        "estimate": float(jump),
        "std_error": float(se),
        "t_stat": float(jump / se) if se else None,
        "ci_95": [float(jump - 1.96 * se), float(jump + 1.96 * se)],
        "bandwidth": float(h),
        "n_effective": n_eff,
        "note": "LATE at the cutoff only. Re-run with 0.5x and 2x bandwidth to "
                "check sensitivity; estimate should be stable.",
    }


def fuzzy_rdd(df, outcome, running, treatment, cutoff=0.0, bandwidth=None):
    d = df[[outcome, running, treatment]].dropna()
    y = d[outcome].to_numpy(float); x = d[running].to_numpy(float)
    tr = d[treatment].to_numpy(float)
    h = bandwidth or _rot_bandwidth(x, cutoff)
    num, num_se, n_eff = _wls_jump(y, x, cutoff, h)      # reduced form
    den, den_se, _ = _wls_jump(tr, x, cutoff, h)         # first stage
    if abs(den) < 1e-6:
        return {"design": "fuzzy", "error": "First-stage jump ~0: threshold does "
                "not shift treatment. Fuzzy RDD not identified."}
    late = num / den
    return {
        "design": "fuzzy",
        "estimate": float(late),
        "reduced_form_jump": float(num),
        "first_stage_jump": float(den),
        "bandwidth": float(h),
        "n_effective": n_eff,
        "note": "Wald/IV estimate = (outcome jump)/(treatment jump) = LATE on "
                "compliers at the cutoff. Weak first-stage jump => fragile.",
    }


def manipulation_check(df, running, cutoff=0.0, bin_width=None):
    """Simplified density discontinuity screen. Compares observation counts in
    symmetric bins just below vs just above the cutoff with a two-proportion z-test.
    A significant imbalance suggests sorting/manipulation."""
    x = df[running].dropna().to_numpy(float)
    bw = bin_width or (np.std(x) / 10)
    below = np.sum((x >= cutoff - bw) & (x < cutoff))
    above = np.sum((x >= cutoff) & (x < cutoff + bw))
    n = below + above
    if n == 0:
        return {"error": "No observations near cutoff."}
    p = above / n
    se = np.sqrt(0.25 / n)
    z = (p - 0.5) / se
    return {
        "count_just_below": int(below),
        "count_just_above": int(above),
        "z_stat": float(z),
        "suspicious": bool(abs(z) > 1.96),
        "note": "Heuristic screen only; |z|>1.96 hints at sorting. Confirm with "
                "the McCrary density test (rddensity) before drawing conclusions.",
    }


def _selftest():
    rng = np.random.default_rng(3)
    n = 4000
    x = rng.uniform(-1, 1, n)
    treat = (x >= 0).astype(float)
    y = 1.0 + 0.8 * x + 1.5 * treat + rng.normal(0, 0.3, n)  # true jump = 1.5
    df = pd.DataFrame({"y": y, "x": x, "t": treat})
    s = sharp_rdd(df, "y", "x", 0.0)
    print("Sharp RDD (true=1.5):", round(s["estimate"], 3),
          "CI", [round(c, 3) for c in s["ci_95"]], "h=", round(s["bandwidth"], 3))
    mc = manipulation_check(df, "x", 0.0)
    print("Manipulation suspicious:", mc["suspicious"], "z=", round(mc["z_stat"], 2))
    assert 1.2 < s["estimate"] < 1.8, "self-test failed"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="Regression Discontinuity Design")
    ap.add_argument("data", nargs="?")
    ap.add_argument("--outcome"); ap.add_argument("--running")
    ap.add_argument("--treatment", default=None)
    ap.add_argument("--cutoff", type=float, default=0.0)
    ap.add_argument("--bandwidth", type=float, default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if not (a.data and a.outcome and a.running):
        ap.error("need data, --outcome, --running")
    df = pd.read_csv(a.data)
    import json
    if a.treatment:
        res = fuzzy_rdd(df, a.outcome, a.running, a.treatment, a.cutoff, a.bandwidth)
    else:
        res = sharp_rdd(df, a.outcome, a.running, a.cutoff, a.bandwidth)
    res["manipulation_check"] = manipulation_check(df, a.running, a.cutoff)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
