"""
Propensity Score Matching (PSM) estimator.

When treatment is non-random but driven by OBSERVED covariates, PSM balances
the groups on a single scalar - the propensity score e(X) = P(treat=1 | X), the
estimated probability of treatment given covariates. Matching treated to control
units with similar scores reproduces, on observables, the balance a randomized
experiment would give. It removes OVERT bias only; it cannot fix unobserved
confounding (its core limitation - state this in every conclusion).

Pipeline implemented here:
  1. Estimate e(X) with logistic regression.
  2. Match on the LOGIT of the score (more nearly linear/normal than the raw
     probability), nearest-neighbour, within a CALIPER of 0.2 * SD(logit) - the
     width supported by Monte-Carlo work as a good bias/variance trade-off.
  3. Enforce COMMON SUPPORT (drop treated units with no control inside caliper).
  4. Report covariate BALANCE via standardized mean differences (SMD); |SMD|<0.1
     after matching is the usual target.
  5. Estimate the ATT as the mean outcome gap over matched pairs.

CLI:
  python psm.py data.csv --treatment d --outcome y --covariates age,income,prior
  python psm.py --selftest
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def _logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def _smd(treated_vals, control_vals):
    mt, mc = np.mean(treated_vals), np.mean(control_vals)
    vt, vc = np.var(treated_vals, ddof=1), np.var(control_vals, ddof=1)
    pooled = np.sqrt((vt + vc) / 2)
    return (mt - mc) / pooled if pooled > 0 else 0.0


def psm_att(df, treatment, outcome, covariates, caliper_sd=0.2, replacement=True):
    cols = [treatment, outcome] + list(covariates)
    d = df[cols].dropna().reset_index(drop=True).copy()

    X = StandardScaler().fit_transform(d[covariates].to_numpy(float))
    t = d[treatment].to_numpy(int)
    y = d[outcome].to_numpy(float)

    lr = LogisticRegression(max_iter=1000)
    lr.fit(X, t)
    ps = lr.predict_proba(X)[:, 1]
    lp = _logit(ps)
    caliper = caliper_sd * np.std(lp)

    treated_idx = np.where(t == 1)[0]
    control_idx = np.where(t == 0)[0]
    control_lp = lp[control_idx]

    matches = []          # (treated_i, control_j)
    used = set()
    for i in treated_idx:
        dists = np.abs(control_lp - lp[i])
        order = np.argsort(dists)
        for o in order:
            j = control_idx[o]
            if dists[o] > caliper:
                break
            if (not replacement) and (j in used):
                continue
            matches.append((i, j)); used.add(j); break

    if not matches:
        return {"error": "No matches within caliper. Overlap/common support fails."}

    matched_treated = [m[0] for m in matches]
    matched_control = [m[1] for m in matches]
    att = float(np.mean(y[matched_treated] - y[matched_control]))

    # balance before vs after, on original (unscaled) covariates
    balance = {}
    raw = d[covariates].to_numpy(float)
    for k, name in enumerate(covariates):
        before = _smd(raw[treated_idx, k], raw[control_idx, k])
        after = _smd(raw[matched_treated, k], raw[matched_control, k])
        balance[name] = {"smd_before": round(float(before), 3),
                         "smd_after": round(float(after), 3),
                         "balanced_after": bool(abs(after) < 0.1)}

    n_unmatched = len(treated_idx) - len(matches)
    return {
        "att": att,
        "n_treated_total": int(len(treated_idx)),
        "n_matched": int(len(matches)),
        "n_treated_off_support": int(n_unmatched),
        "caliper_logit": float(caliper),
        "replacement": replacement,
        "balance": balance,
        "all_covariates_balanced": all(b["balanced_after"] for b in balance.values()),
        "caveat": "ATT removes bias from OBSERVED covariates only. Unobserved "
                  "confounding is not addressed; pair with a sensitivity analysis "
                  "(e.g. Rosenbaum bounds) before claiming a causal effect.",
        "support_note": (f"{n_unmatched} treated units had no control within the "
                         "caliper and were dropped; the ATT applies only to the "
                         "on-support region." if n_unmatched else
                         "All treated units matched on common support."),
    }


def _selftest():
    rng = np.random.default_rng(5)
    n = 3000
    age = rng.normal(40, 10, n)
    income = rng.normal(50, 15, n)
    # treatment depends on covariates (selection on observables)
    lin = -6 + 0.06 * age + 0.04 * income
    p = 1 / (1 + np.exp(-lin))
    t = rng.binomial(1, p)
    # outcome depends on covariates and treatment; true ATT = 3.0
    y = 10 + 0.2 * age + 0.1 * income + 3.0 * t + rng.normal(0, 2, n)
    df = pd.DataFrame({"d": t, "y": y, "age": age, "income": income})
    naive = df[df.d == 1].y.mean() - df[df.d == 0].y.mean()
    res = psm_att(df, "d", "y", ["age", "income"])
    print("Naive diff (biased):", round(naive, 3),
          "| PSM ATT (true=3.0):", round(res["att"], 3),
          "| matched:", res["n_matched"], "| balanced:", res["all_covariates_balanced"])
    assert 2.0 < res["att"] < 4.0, "self-test failed"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="Propensity Score Matching (ATT)")
    ap.add_argument("data", nargs="?")
    ap.add_argument("--treatment"); ap.add_argument("--outcome")
    ap.add_argument("--covariates", help="comma-separated")
    ap.add_argument("--caliper-sd", type=float, default=0.2)
    ap.add_argument("--no-replacement", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if not (a.data and a.treatment and a.outcome and a.covariates):
        ap.error("need data, --treatment, --outcome, --covariates")
    df = pd.read_csv(a.data)
    covs = [s.strip() for s in a.covariates.split(",") if s.strip()]
    res = psm_att(df, a.treatment, a.outcome, covs,
                  caliper_sd=a.caliper_sd, replacement=not a.no_replacement)
    import json; print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
