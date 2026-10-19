"""
E-value (VanderWeele & Ding 2017): robustness of a causal claim to hidden confounding.

This is the quantitative form of the "too good to be true?" question for an
observational effect. The E-value is the minimum strength of association (on the
risk-ratio scale) that an unmeasured confounder would need with BOTH the
treatment and the outcome to fully explain away the observed effect. A large
E-value means a hidden cause would have to be implausibly strong to overturn the
finding (robust); a small one means a modest unmeasured confounder could erase it
(fragile). Pairs naturally with PSM/regression results that rely on
selection-on-observables.

  - evalue(rr, lo=None, hi=None)  : E-value for a risk ratio (and for the CI limit
                                    nearest the null, testing significance robustness).
  - from_or(or_, common=True)     : convert an odds ratio to an approximate RR first.

CLI:
  python evalue.py --rr 1.8 --lo 1.3 --hi 2.5
  python evalue.py --or 3.0 --common
  python evalue.py --selftest
"""
from __future__ import annotations
import argparse
import math


def _e(rr):
    if rr < 1:
        rr = 1.0 / rr
    return rr + math.sqrt(rr * (rr - 1))


def from_or(or_, common=True):
    """Common-outcome (>15%) approximation RR ≈ sqrt(OR)."""
    return math.sqrt(or_) if common else or_


def evalue(rr, lo=None, hi=None):
    out = {"rr": rr, "evalue_point": round(_e(rr), 3)}
    # E-value for the confidence limit nearest the null (1.0)
    limit = None
    if lo is not None and hi is not None:
        if rr > 1:
            limit = lo
        elif rr < 1:
            limit = hi
        if limit is not None:
            crosses_null = (rr > 1 and limit <= 1) or (rr < 1 and limit >= 1)
            out["ci_limit_nearest_null"] = limit
            out["evalue_ci"] = 1.0 if crosses_null else round(_e(limit), 3)
            if crosses_null:
                out["note_ci"] = "CI crosses the null; E-value for the limit is 1."
    out["interpretation"] = (
        f"An unmeasured confounder associated with both treatment and outcome by a "
        f"risk ratio of {out['evalue_point']}× each (above measured covariates) "
        f"could explain away the point estimate; weaker confounding could not. "
        + ("The same for the CI limit: " + str(out.get('evalue_ci')) + "×."
           if 'evalue_ci' in out else "")
    )
    out["caveat"] = ("E-value quantifies robustness, not correctness — it assumes "
                     "the model is otherwise right and says nothing about selection "
                     "bias or measurement error.")
    return out


def _selftest():
    e = evalue(2.0)
    print("E-value for RR=2.0 →", e["evalue_point"], "(expect ~3.414)")
    assert abs(e["evalue_point"] - 3.414) < 0.01, "E-value self-test failed"
    e2 = evalue(1.8, lo=1.3, hi=2.5)
    print("E-value for RR=1.8 (point/CI) →", e2["evalue_point"], "/", e2["evalue_ci"])
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="E-value for unmeasured confounding")
    ap.add_argument("--rr", type=float, default=None)
    ap.add_argument("--or", dest="or_", type=float, default=None)
    ap.add_argument("--common", action="store_true", help="OR→RR common-outcome approx")
    ap.add_argument("--lo", type=float, default=None); ap.add_argument("--hi", type=float, default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    rr = a.rr if a.rr is not None else (from_or(a.or_, a.common) if a.or_ else None)
    if rr is None:
        ap.error("need --rr or --or")
    import json; print(json.dumps(evalue(rr, a.lo, a.hi), indent=2))


if __name__ == "__main__":
    main()
