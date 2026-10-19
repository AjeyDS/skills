"""
GRIM / GRIMMER: granularity consistency of reported means and SDs.

These are pure arithmetic, not probability. For data that is the mean of N
integers (Likert scales, counts), the mean must be an exact multiple of 1/N.
If a paper/report states a mean that NO integer sum over N can produce, the
number is mathematically impossible — strong evidence of error or fabrication.
GRIMMER extends the same logic to the standard deviation.

Best on small N, high granularity (few scale points), and several reported
decimals; large N admits too many achievable values to be diagnostic.

  - grim(mean, n, items, decimals)        : is the reported mean achievable?
  - grimmer(mean, sd, n, items, decimals) : is the reported (mean, SD) pair achievable?

CLI:
  python grim.py --mean 3.45 --n 20 --items 1
  python grim.py --mean 3.45 --sd 1.10 --n 20 --items 1
  python grim.py --selftest
"""
from __future__ import annotations
import argparse
import numpy as np


def grim(mean, n, items=1, decimals=None):
    """items = number of summed Likert items (granularity = 1/(n*items))."""
    if decimals is None:
        s = repr(float(mean))
        decimals = len(s.split(".")[1]) if "." in s else 0
    granularity = 1.0 / (n * items)
    tol = 0.5 * 10 ** (-decimals)            # half a reported decimal
    # nearest achievable mean to the reported one
    k = round(mean * n * items)
    achievable = k * granularity
    consistent = abs(achievable - mean) <= tol + 1e-12
    return {
        "test": "GRIM",
        "reported_mean": mean,
        "n": n, "items": items, "decimals": decimals,
        "nearest_achievable_mean": round(achievable, decimals + 2),
        "consistent": bool(consistent),
        "verdict": ("consistent" if consistent
                    else "IMPOSSIBLE — no integer data of this N yields this mean"),
    }


def grimmer(mean, sd, n, items=1, decimals=None):
    """Check that a reported (mean, SD) is achievable from integer data of size N.
    Uses the standard GRIMMER logic: the sum of squares implied by mean+SD+N must
    be an integer (within rounding) for integer-valued data."""
    g = grim(mean, n, items, decimals)
    if decimals is None:
        s = repr(float(sd))
        decimals = len(s.split(".")[1]) if "." in s else 0
    # total and sum-of-squares implied (sample SD, ddof=1)
    total = mean * n * items
    var = sd ** 2
    ss = var * (n - 1) + (total ** 2) / n      # sum of squared values
    nearest_int_ss = round(ss)
    # tolerance from SD rounding propagated (loose, conservative)
    sd_tol = 0.5 * 10 ** (-decimals)
    ss_hi = ((sd + sd_tol) ** 2) * (n - 1) + (total ** 2) / n
    ss_lo = (max(sd - sd_tol, 0) ** 2) * (n - 1) + (total ** 2) / n
    ss_consistent = any(abs(round(v) - v) < 0.5 for v in (ss_lo, ss, ss_hi)) and \
        (np.floor(ss_lo) <= nearest_int_ss <= np.ceil(ss_hi))
    consistent = g["consistent"] and ss_consistent
    return {
        "test": "GRIMMER",
        "grim": g,
        "reported_sd": sd,
        "implied_sum_of_squares": round(float(ss), 3),
        "sd_consistent": bool(ss_consistent),
        "consistent": bool(consistent),
        "verdict": ("consistent" if consistent
                    else "IMPOSSIBLE/INCONSISTENT — reported mean+SD not "
                         "achievable from integer data of this N"),
    }


def _selftest():
    # mean must be a multiple of 1/N. N=10 → achievable means are k/10.
    ok = grim(3.30, 10, 1)          # 33/10 = 3.30 → achievable
    bad = grim(3.45, 10, 1)         # 34.5/10 impossible from integers
    print("GRIM 3.30/N=10 →", ok["consistent"], "(expect True)")
    print("GRIM 3.45/N=10 →", bad["consistent"], "(expect False)")
    assert ok["consistent"] and not bad["consistent"], "GRIM self-test failed"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="GRIM/GRIMMER granularity check")
    ap.add_argument("--mean", type=float); ap.add_argument("--sd", type=float, default=None)
    ap.add_argument("--n", type=int); ap.add_argument("--items", type=int, default=1)
    ap.add_argument("--decimals", type=int, default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if a.mean is None or a.n is None:
        ap.error("need --mean and --n")
    import json
    if a.sd is None:
        print(json.dumps(grim(a.mean, a.n, a.items, a.decimals), indent=2))
    else:
        print(json.dumps(grimmer(a.mean, a.sd, a.n, a.items, a.decimals), indent=2))


if __name__ == "__main__":
    main()
