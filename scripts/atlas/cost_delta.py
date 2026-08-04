"""Recompute D6 cost under measured vs assumed usage profiles.

Quantifies every recommendation delta caused by RQ-18/RQ-19 resolution.
Prices are captured Class A facts; usage is the variable under test.

Run: python scripts/atlas/cost_delta.py
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "research" / "evidence" / "usage"

# Captured Class A pricing, per MTok. pricing_as_of 2026-08-03/04.
PRICES = {
    "claude-sonnet-5 (from 2026-09-01)": {"in": 3.00, "cache_read": 0.30, "out": 15.00},
    "claude-sonnet-5 (introductory, to 2026-08-31)": {"in": 2.00, "cache_read": 0.20, "out": 10.00},
    "claude-opus-5": {"in": 5.00, "cache_read": 0.50, "out": 25.00},
    "claude-fable-5": {"in": 10.00, "cache_read": 1.00, "out": 50.00},
    "claude-haiku-4-5": {"in": 1.00, "cache_read": 0.10, "out": 5.00},
    "deepseek-v4-pro": {"in": 0.435, "cache_read": 0.003625, "out": 0.87},
    "deepseek-v4-flash": {"in": 0.14, "cache_read": 0.0028, "out": 0.28},
}

# ASSUMED (use-solo-founder-typical, pre-measurement)
ASSUMED = {"label": "assumed", "presented_in": 25_000_000, "out": 2_000_000, "hit": 0.50}

# MEASURED (RQ-18/19, 56-day retrospective, single operator)
# Same presented-input volume held constant so the comparison isolates the two
# parameters actually measured: cache hit rate and I/O ratio.
MEASURED_HIT = 0.9432
MEASURED_IO = 197.69
MEASURED = {"label": "measured", "presented_in": 25_000_000,
            "out": 25_000_000 / MEASURED_IO, "hit": MEASURED_HIT}


def monthly(profile: dict, p: dict) -> float:
    presented, hit = profile["presented_in"], profile["hit"]
    uncached = presented * (1 - hit)
    cached = presented * hit
    return (uncached * p["in"] + cached * p["cache_read"] + profile["out"] * p["out"]) / 1_000_000


def main() -> int:
    rows = []
    for name, p in PRICES.items():
        a, m = monthly(ASSUMED, p), monthly(MEASURED, p)
        rows.append({
            "model": name,
            "assumed_usd_month": round(a, 2),
            "measured_usd_month": round(m, 2),
            "delta_usd": round(m - a, 2),
            "delta_pct": round((m - a) / a * 100, 1) if a else None,
        })

    rank_a = [r["model"] for r in sorted(rows, key=lambda r: r["assumed_usd_month"])]
    rank_m = [r["model"] for r in sorted(rows, key=lambda r: r["measured_usd_month"])]

    # Which models fit a $20/month ceiling under each profile?
    fits_a = [r["model"] for r in rows if r["assumed_usd_month"] <= 20]
    fits_m = [r["model"] for r in rows if r["measured_usd_month"] <= 20]

    result = {
        "study": "RQ-18/19 cost delta",
        "pricing_as_of": "2026-08-04",
        "assumed_profile": {k: v for k, v in ASSUMED.items()},
        "measured_profile": {**{k: v for k, v in MEASURED.items()}, "io_ratio": MEASURED_IO},
        "rows": rows,
        "ranking_assumed": rank_a,
        "ranking_measured": rank_m,
        "ranking_changed": rank_a != rank_m,
        "fits_20_usd_assumed": fits_a,
        "fits_20_usd_measured": fits_m,
        "newly_affordable_at_20": sorted(set(fits_m) - set(fits_a)),
        "mean_delta_pct": round(sum(r["delta_pct"] for r in rows) / len(rows), 1),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cost-delta-2026-08-04.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
