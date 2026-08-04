"""Sensitivity + crossover engine.

Fixes the defect surfaced 2026-08-04: the Atlas reported a point estimate
("$13.23, fits $20") computed from an OPERATOR-SPECIFIC input, without saying
that the answer flips at a threshold the reader was never asked about.

Principle: when an answer is sensitive to an undeclared parameter, the crossover
IS the answer. Report the threshold, not the point.

Run: python scripts/atlas/sensitivity.py [--budget 20]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Same cp1252 console hazard as bias_report: this prints a '✗' marker.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(__file__).resolve().parents[2] / "research" / "evidence" / "usage"

PRESENTED = 25e6
CACHE_HIT = 0.9432          # measured, harness-scoped, unreplicated (RQ-28)

MODELS = {
    "claude-sonnet-5 (std)":   (3.00, 0.30, 15.00),
    "claude-sonnet-5 (intro)": (2.00, 0.20, 10.00),
    "claude-haiku-4-5":        (1.00, 0.10, 5.00),
    "deepseek-v4-pro":         (0.435, 0.003625, 0.87),
    "deepseek-v4-flash":       (0.14, 0.0028, 0.28),
}

# Workload shapes. The measured value is ONE of these, not the default for all.
SHAPES = {
    "doc_heavy_research": 197.7,   # <- what we actually measured, n=1
    "mixed": 100.0,
    "code_leaning": 50.0,
    "heavy_codegen": 20.0,
}


def monthly(pin, pcache, pout, io, hit=CACHE_HIT):
    return (PRESENTED * (1 - hit) * pin
            + PRESENTED * hit * pcache
            + (PRESENTED / io) * pout) / 1e6


def crossover_io(pin, pcache, pout, budget, hit=CACHE_HIT):
    """I/O ratio at which this model exactly hits the budget. None = always/never."""
    if monthly(pin, pcache, pout, 1e6, hit) > budget:
        return None                      # over budget even with ~zero output
    if monthly(pin, pcache, pout, 1.0, hit) <= budget:
        return 0.0                       # under budget even at 1:1
    lo, hi = 1.0, 1e6
    for _ in range(80):
        mid = (lo + hi) / 2
        if monthly(pin, pcache, pout, mid, hit) > budget:
            lo = mid
        else:
            hi = mid
    return hi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=20.0)
    a = ap.parse_args()

    rows = []
    for name, (i, c, o) in MODELS.items():
        by_shape = {k: round(monthly(i, c, o, r), 2) for k, r in SHAPES.items()}
        x = crossover_io(i, c, o, a.budget)
        fits = {k: v <= a.budget for k, v in by_shape.items()}
        robust = all(fits.values())
        never = not any(fits.values())
        rows.append({
            "model": name,
            "cost_by_workload": by_shape,
            "fits_budget": fits,
            "crossover_io_ratio": None if x in (None, 0.0) else round(x, 1),
            "verdict": ("robust — fits at every workload shape" if robust else
                        "never — exceeds budget at every shape" if never else
                        f"CONDITIONAL — fits only above {x:.0f}:1 input/output"),
            "sensitive": not (robust or never),
        })

    sensitive = [r for r in rows if r["sensitive"]]
    result = {
        "study": "cost sensitivity to workload shape",
        "budget_usd_month": a.budget,
        "fixed_inputs": {"presented_input_tokens": PRESENTED, "cache_hit_rate": CACHE_HIT},
        "undeclared_parameter": "input:output ratio — NOT asked of the reader",
        "measured_value_scope": "operator-specific (doc-heavy research, n=1)",
        "rows": rows,
        "answer_flips_for": [r["model"] for r in sensitive],
        "engine_requirement": (
            "Where 'sensitive' is true the engine MUST NOT emit a point estimate. "
            "It must either elicit the parameter from the reader or report the "
            "crossover as the answer."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"sensitivity-{int(a.budget)}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    w = max(len(m) for m in MODELS)
    print(f"BUDGET ${a.budget:.0f}/mo   ·   varying the ONE parameter we never asked about\n")
    print(f"{'model':{w}}" + "".join(f"{k.replace('_',' '):>20}" for k in SHAPES))
    print("-" * (w + 20 * len(SHAPES)))
    for r in rows:
        print(f"{r['model']:{w}}" + "".join(
            f"{('$'+format(v,'.2f')) + ('  ' if r['fits_budget'][k] else ' ✗'):>20}"
            for k, v in r["cost_by_workload"].items()))
    print()
    for r in rows:
        print(f"  {r['model']:{w}}  {r['verdict']}")
    print(f"\nanswer flips for {len(sensitive)} of {len(rows)} models — "
          f"these must not be reported as point estimates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
