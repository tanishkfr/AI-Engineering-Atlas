"""Replication validator for RQ-18/19.

Given the originating result plus one or more independent --share payloads,
classifies replication status against the PREREGISTERED thresholds and states
what the cost correction is licensed to claim.

Thresholds are fixed in REPLICATION-AUDIT-RQ-18 §5 and are NOT adjustable here.

Run: python scripts/evidence/replication_check.py replications/*.json
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Originating result — frozen. RQ-18 is closed; this is a constant, not an input.
ORIGIN = {"operator": "origin", "cache_hit_rate": 0.9432, "io_ratio": 197.69, "turns": 18604}

# Preregistered. Do not edit to accommodate a result.
T_REPLICATE = 0.85
T_PARTIAL = 0.70
MIN_TURNS = 200          # below this a payload is underpowered, not evidence
MIN_INDEPENDENT = 1      # replications required beyond origin


def classify(rate: float) -> str:
    if rate >= T_REPLICATE:
        return "replicates"
    if rate >= T_PARTIAL:
        return "partial"
    return "falsified"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("payloads", nargs="*", help="paths to --share JSON files")
    a = ap.parse_args()

    reps = []
    for p in a.payloads:
        try:
            # utf-8-sig: replicators send files from unknown editors and shells;
            # a BOM must not be grounds for discarding a replication.
            d = json.loads(Path(p).read_text(encoding="utf-8-sig"))
        except Exception as e:  # noqa: BLE001
            print(f"skip {p}: {e}", file=sys.stderr)
            continue
        if d.get("replication_of") != "RQ-18/19":
            print(f"skip {p}: not an RQ-18/19 payload", file=sys.stderr)
            continue
        rate, turns = d.get("cache_hit_rate"), d.get("turns", 0)
        if rate is None:
            continue
        reps.append({
            "source": Path(p).stem,
            "cache_hit_rate": rate,
            "io_ratio": d.get("io_ratio"),
            "turns": turns,
            "underpowered": turns < MIN_TURNS,
            "classification": classify(rate),
        })

    powered = [r for r in reps if not r["underpowered"]]

    if len(powered) < MIN_INDEPENDENT:
        verdict = "AWAITING_REPLICATION"
        licensed = "operator-scoped only"
        rq28 = "open — unresolved"
        detail = (f"{len(powered)} usable independent replication(s); "
                  f"{MIN_INDEPENDENT} required. The cost correction remains "
                  "labelled operator-derived and must not be published unscoped.")
    else:
        rates = [r["cache_hit_rate"] for r in powered]
        cls = [r["classification"] for r in powered]
        if all(c == "replicates" for c in cls):
            verdict = "REPLICATED"
            licensed = "harness-level — publish scoped to this harness"
            rq28 = "resolved — cache rate is harness-determined, not operator-determined"
            detail = "All independent replications at or above 0.85."
        elif any(c == "falsified" for c in cls):
            verdict = "FALSIFIED"
            licensed = "operator-scoped only — REVERT"
            rq28 = "resolved — 0.9432 is idiosyncratic; cache rate varies by operator"
            detail = ("At least one independent replication below 0.70. The "
                      "correction does not generalize. Relabel all cost figures "
                      "and publish a correction delta.")
        else:
            lo, hi = min(rates + [ORIGIN["cache_hit_rate"]]), max(rates + [ORIGIN["cache_hit_rate"]])
            verdict = "PARTIAL"
            licensed = f"publish as a RANGE ({lo:.3f}–{hi:.3f}), never a point"
            rq28 = "partially resolved — direction holds, magnitude varies"
            detail = "Replications span classifications. Point estimates are not supported."

    all_rates = [ORIGIN["cache_hit_rate"]] + [r["cache_hit_rate"] for r in powered]
    result = {
        "study": "RQ-18/19 replication check",
        "thresholds": {"replicates": f">={T_REPLICATE}", "partial": f">={T_PARTIAL}",
                       "falsified": f"<{T_PARTIAL}", "min_turns": MIN_TURNS},
        "origin": ORIGIN,
        "independent_replications": reps,
        "usable_count": len(powered),
        "verdict": verdict,
        "detail": detail,
        "cost_correction_licensed_as": licensed,
        "RQ-28_status": rq28,
        "spread": {
            "n": len(all_rates),
            "min": min(all_rates),
            "max": max(all_rates),
            "median": round(statistics.median(all_rates), 4),
        } if len(all_rates) > 1 else None,
        "note": ("io_ratio is NOT a falsification target — classified "
                 "operator-specific in REPLICATION-AUDIT §2. Divergence there is "
                 "expected and carries no evidential weight."),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
