"""
Digit-distribution forensics: Benford's Law, last-digit uniformity, round-number bias.

These screen a column of numbers for fabrication/manipulation fingerprints. They
FLAG anomalies; they never prove fraud — conformity doesn't prove honesty and a
sophisticated fabricator can mimic Benford (it failed to catch Wirecard). Treat
any flag as "requires explanation," confirm with an independent test, and weigh
benign causes (see references/forensic-integrity.md).

  - benford(...)     : first-digit (and first-two-digit) conformity via Nigrini's
                       Mean Absolute Deviation (MAD), NOT chi-square (which
                       over-rejects on large samples).
  - last_digit(...)  : terminal digits of counts should be ~uniform; excess 0s/5s
                       = human rounding, suspiciously flat = possible RNG fabrication.
  - applicability(...): Benford needs data spanning orders of magnitude; it does
                       NOT apply to assigned IDs, bounded ranges, or min/max-capped
                       values. Check before trusting a Benford result.

CLI:
  python benford.py data.csv --column amount
  python benford.py --selftest
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd

# Nigrini MAD thresholds (first digit, K=9 bins)
FIRST_DIGIT_MAD = [(0.006, "close conformity"), (0.012, "acceptable"),
                   (0.015, "marginal"), (float("inf"), "NONCONFORMITY (red flag)")]
# first-two-digit (K=90 bins)
FIRST_TWO_MAD = [(0.0012, "close conformity"), (0.0018, "acceptable"),
                 (0.0022, "marginal"), (float("inf"), "NONCONFORMITY (red flag)")]


def _verdict(mad, table):
    for thr, label in table:
        if mad <= thr:
            return label
    return "NONCONFORMITY"


def _leading_digit(x, two=False):
    x = np.abs(x[x != 0]).astype(float)
    if len(x) == 0:
        return np.array([])
    mag = np.floor(np.log10(x))
    lead = (x / 10.0 ** mag)            # in [1,10)
    if two:
        return np.floor(lead * 10).astype(int)   # 10..99
    return np.floor(lead).astype(int)             # 1..9


def applicability(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    pos = x[x > 0]
    if len(pos) == 0:
        return {"applicable": False, "reason": "no positive values"}
    orders = np.log10(pos.max() / pos.min()) if pos.min() > 0 else np.inf
    return {
        "applicable": orders >= 2,
        "orders_of_magnitude": round(float(orders), 2),
        "note": ("Spans <2 orders of magnitude — Benford may not apply. Also "
                 "exclude assigned IDs, bounded ranges, and capped values."
                 if orders < 2 else "Spans enough magnitude for Benford."),
    }


def benford(x, two=False):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    digits = _leading_digit(x, two=two)
    if len(digits) == 0:
        return {"error": "no usable values"}
    if two:
        bins = np.arange(10, 100)
        expected = np.log10(1 + 1 / bins)
    else:
        bins = np.arange(1, 10)
        expected = np.log10(1 + 1 / bins)
    actual = np.array([(digits == d).mean() for d in bins])
    mad = float(np.mean(np.abs(actual - expected)))
    table = FIRST_TWO_MAD if two else FIRST_DIGIT_MAD
    out = {
        "test": "first-two-digit" if two else "first-digit",
        "n": int(len(digits)),
        "MAD": round(mad, 5),
        "verdict": _verdict(mad, table),
    }
    if not two:
        out["expected_vs_actual"] = {
            int(d): {"expected": round(float(e), 3), "actual": round(float(a), 3)}
            for d, e, a in zip(bins, expected, actual)
        }
    return out


def last_digit(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    # integer-ish counts only
    ld = (np.round(x).astype(np.int64)) % 10
    counts = np.array([(ld == d).mean() for d in range(10)])
    # deviation from uniform 0.1
    excess_0_5 = float(counts[0] + counts[5] - 0.2)
    # chi-square vs uniform
    n = len(ld)
    obs = counts * n
    exp = n / 10
    chisq = float(np.sum((obs - exp) ** 2 / exp)) if n else 0.0
    return {
        "n": int(n),
        "digit_freq": {d: round(float(counts[d]), 3) for d in range(10)},
        "excess_zeros_and_fives": round(excess_0_5, 3),
        "chi_square_vs_uniform": round(chisq, 2),
        "flag_human_rounding": bool(excess_0_5 > 0.10),
        "flag_too_uniform": bool(abs(chisq) < 2.0 and n > 200),
        "note": "Excess 0s/5s = human rounding (often benign). Suspiciously flat "
                "uniformity in data that should round = possible RNG fabrication.",
    }


def _selftest():
    rng = np.random.default_rng(1)
    # Benford-conforming: products of uniforms span magnitudes
    conform = 10 ** (rng.uniform(0, 5, 5000))
    b = benford(conform)
    print("Conforming data → MAD", b["MAD"], "|", b["verdict"])
    # Fabricated: uniform within one magnitude (no Benford structure) + RNG last digits
    fake = rng.uniform(100, 999, 5000)
    bf = benford(fake)
    ld = last_digit(rng.integers(0, 1000, 5000))
    print("Fabricated uniform → MAD", bf["MAD"], "|", bf["verdict"])
    print("RNG last digits → too_uniform flag:", ld["flag_too_uniform"])
    assert b["MAD"] < 0.015, "conforming data should pass"
    assert bf["MAD"] > 0.015, "uniform data should flag"
    print("OK")


def main():
    ap = argparse.ArgumentParser(description="Benford / digit forensics")
    ap.add_argument("data", nargs="?"); ap.add_argument("--column")
    ap.add_argument("--two", action="store_true", help="first-two-digit test")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        _selftest(); return
    if not (a.data and a.column):
        ap.error("need data and --column")
    x = pd.read_csv(a.data)[a.column].to_numpy(float)
    import json
    out = {"applicability": applicability(x),
           "benford": benford(x, two=a.two),
           "last_digit": last_digit(x)}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
