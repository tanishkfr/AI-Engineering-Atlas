"""Scored-dimension report.

For six milestones this printed zero. Kept running anyway, because a metric you
only publish once it flatters you is not a metric.

Run: python scripts/atlas/coverage.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "engine"))
import corpus as C  # noqa: E402

DIMS = {
    "D1": "Output quality", "D2": "Autonomy", "D3": "Engineering output",
    "D4": "Reliability", "D5": "Maintainability", "D6": "Cost",
    "D7": "Developer experience", "D8": "Speed", "D9": "Flexibility",
    "D10": "Ecosystem maturity", "D11": "Data & licensing", "D12": "Continuity risk",
    "D13": "Security posture",
}


def main() -> int:
    g = C.load()
    scores = []
    for e in g["entities"].values():
        for s in e.get("scores") or []:
            scores.append((e.get("name"), s))

    by_dim = {}
    for name, s in scores:
        by_dim.setdefault(s.get("dimension"), []).append((name, s))

    print("DIMENSION COVERAGE\n" + "-" * 62)
    for d, label in DIMS.items():
        rows = by_dim.get(d, [])
        if rows:
            for name, s in rows:
                second = "single-rater" if not s.get("second_pass") else "re-scored"
                print(f"  {d:4s} {label:22s} {s['value']}/5  {name}  [{second}]")
        else:
            print(f"  {d:4s} {label:22s}  —   not_scored")

    n = len(by_dim)
    print("-" * 62)
    print(f"  {n} of {len(DIMS)} dimensions scored")

    unrated = [d for d in DIMS if d not in by_dim]
    print(f"\n  still unscored: {', '.join(unrated)}")

    single = [f"{d}" for d, rows in by_dim.items() if not rows[0][1].get("second_pass")]
    if single:
        print(f"\n  ⚠ single-rater, no independent re-score: {', '.join(single)}")
        print("    EVALUATION §6 requires a second pass. These are provisional.")

    if n == 0:
        print("\n  No dimension is scored. The engine cannot rank anything, and")
        print("  saying so is more useful than a number with nothing behind it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
