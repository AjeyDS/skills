"""
Instrumental Variables (IV / 2SLS) estimator.

When treatment is endogenous (unobserved confounding, reverse causality, or
non-compliance), an instrument Z provides exogenous variation: Z shifts the
treatment but affects the outcome ONLY through the treatment. 2SLS uses the
part of the treatment predicted by Z, purging the endogenous part.

The estimate is a LATE (Local Average Treatment Effect) = the effect for
COMPLIERS: units whose treatment status is moved by the instrument. It says
nothing about always-takers or never-takers.

IV rests on three assumptions, two of them untestable:
  1. Relevance      - Cov(Z, treatment) != 0. TESTABLE: first-stage F-stat.
                      Rule of thumb F < 10 => weak instrument => biased, wide CIs.
  2. Exclusion      - Z affects Y only through treatment. NOT testable; argue it.
  3. Monotonicity   - no defiers; Z pushes everyone the same direction. NOT testable.

This implements:
  - tsls(...)  : general 2SLS with proper IV standard errors (statsmodels),
                 plus the first-stage F-statistic for weak-instrument diagnosis.
  - wald(...)  : the Wald estimator for a single binary instrument and binary
                 treatment = LATE = (ITT on outcome)/(ITT on treatment).

CLI:
  python iv.py data.csv --outcome y --treatment d --instrument z --controls a,b
  python iv.py --selftest
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import IV2SLS


def tsls(df, outcome, treatment, instruments, controls=None):
    controls = controls or []
    if isinstance(instruments, str):
        instruments = [instruments]
    cols = [outcome, treatment] + list(instruments) + list(controls)
    d = df[cols].dropna().copy()

    y = d[outcome].to_numpy(float)
    exog_ctrl = d[controls].to_numpy(float) if controls else np.empty((len(d), 0))
    endog = d[treatment].to_numpy(float).reshape(-1, 1)
    instr = d[instruments].to_numpy(float)

    const = np.ones((len(d), 1))
    # second stage design: const + controls + endog treatment
    X = np.column_stack([const, exog_ctrl, endog])
    # instrument matrix: const + controls + instruments
    Z = np.column_stack([const, exog_ctrl, instr])

    model = IV2SLS(y, X, Z).fit()
    # treatment coefficient is the last column
    k = X.shape[1] - 1
    coef = model.params[k]; se = model.bse[k]

    # First-stage F-stat for the excluded instruments (weak-instrument test)
    fs_X = np.column_stack([const, exog_ctrl, instr])
    fs = sm.OLS(endog.ravel(), fs_X).fit()
    # restricted model without instruments
    r_X = np.column_stack([const, exog_ctrl]) if controls else const
    fs_r = sm.OLS(endog.ravel(), r_X).fit()
    q = instr.shape[1]
    df_resid = len(d) - fs_X.shape[1]
    f_stat = ((fs_r.ssr - fs.ssr) / q) / (fs.ssr / df_resid)

    return {
        "estimate": float(coef),
        "std_error": float(se),
        "t_stat": float(coef / se) if se else None,
        "ci_95": [float(coef - 1.96 * se), float(coef + 1.96 * se)],
        "first_stage_F": float(f_stat),
        "weak_instrument": bool(f_stat < 10),
        "n_obs": int(len(d)),
        "interpretation": "LATE on compliers (effect for units moved by the instrument).",
        "warning": ("First-stage F < 10: WEAK INSTRUMENT. 2SLS is biased toward "
                    "OLS and CIs understate uncertainty. Find a stronger instrument "
                    "or use weak-IV-robust inference (Anderson-Rubin)."
                    if f_stat < 10 else None),
    }


def wald(df, outcome, treatment, instrument):
    """Wald estimator for binary Z and binary treatment.
    LATE = E[Y|Z=1]-E[Y|Z=0]  /  E[D|Z=1]-E[D|Z=0]."""
    d = df[[outcome, treatment, instrument]].dropna()
    g1 = d[d[instrument] == 1]; g0 = d[d[instrument] == 0]
    itt_y = g1[outcome].mean() - g0[outcome].mean()
    compliance = g1[treatment].mean() - g0[treatment].mean()
    if abs(compliance) < 1e-9:
        return {"error": "No first stage: instrument does not shift treatment."}
    return {
        "late": float(itt_y / compliance),
        "itt_outcome": float(itt_y),
        "complier_share": float(compliance),
        "note": "LATE is larger in magnitude than the raw ITT because it scales "
                "the ITT up by the (sub-1) complier share.",
    }


def _selftest():
    rng = np.random.default_rng(11)
    n = 5000
    z = rng.binomial(1, 0.5, n)              # instrument
    u = rng.normal(0, 1, n)                  # confounder (affects d and y)
    d = ((0.6 * z + 0.7 * u + rng.normal(0, 0.5, n)) > 0.5).astype(float)
    y = 1.0 + 2.0 * d + 1.5 * u + rng.normal(0, 0.5, n)  # true effect = 2.0
    df = pd.DataFrame({"y": y, "d": d, "z": z})
    ols = np.polyfit(df["d"], df["y"], 1)[0]
    iv = tsls(df, "y", "d", "z")
    print("OLS (confounded):", round(ols, 3),
          "| IV estimate (true=2.0):", round(iv["estimate"], 3),
          "| first-stage F:", round(iv["first_stage_F"], 1))
    assert 1.5 < iv["estimate"] < 2.5, "self-test failed"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="Instrumental Variables (2SLS)")
    ap.add_argument("data", nargs="?")
    ap.add_argument("--outcome"); ap.add_argument("--treatment")
    ap.add_argument("--instrument", help="comma-separated for multiple")
    ap.add_argument("--controls", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if not (a.data and a.outcome and a.treatment and a.instrument):
        ap.error("need data, --outcome, --treatment, --instrument")
    df = pd.read_csv(a.data)
    instruments = [s.strip() for s in a.instrument.split(",") if s.strip()]
    controls = [s.strip() for s in a.controls.split(",") if s.strip()]
    res = tsls(df, a.outcome, a.treatment, instruments, controls)
    import json; print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
