"""Standing bias metric.

The Trust Audit found evidence density correlating with documentation quality
rather than with importance — a selection effect wearing coverage's clothes.
That is invisible unless it is measured, so it is measured here and reported
every time the corpus changes.

Run: python scripts/atlas/bias_report.py
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
import corpus as C  # noqa: E402

# This report draws bar charts. A default Windows console is cp1252 and raised
# UnicodeEncodeError instead of printing the bias metric.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def main() -> int:
    # The metric is DEFINED in corpus.calibration and only rendered here.
    # It used to be re-derived by regex, which made the interface and this
    # report disagree about the same number. CONSTITUTION §9: one fact, one place.
    cal = C.calibration(C.load())
    cites = collections.Counter(dict(cal["citations"]))
    unknowns = cal["explicit_unknowns"]
    published = cal["published_claims"]

    entities = collections.Counter()
    for p in DATA.rglob("*.yaml"):
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r"made_by: ent-institution-([a-z0-9-]+)", t):
            entities[m.group(1)] += 1

    total = sum(cites.values()) or 1
    top = (cal["dominant_publisher"] or "none", cites[cal["dominant_publisher"]] if cal["dominant_publisher"] else 0)

    print("EVIDENCE CONCENTRATION — citations by publisher\n" + "-" * 52)
    for k, v in cites.most_common():
        bar = "█" * round(v / total * 34)
        print(f"  {k:18s} {v:3d}  {v/total*100:5.1f}%  {bar}")

    print("\nENTITIES BY MAKER\n" + "-" * 52)
    for k, v in entities.most_common():
        print(f"  {k:18s} {v:3d}")

    share = top[1] / total
    print("\nSKEW\n" + "-" * 52)
    print(f"  dominant publisher   {top[0]} at {share*100:.1f}% of all citations")
    print(f"  distinct publishers  {len(cites)}")
    print(f"  published claims     {published}")
    print(f"  explicit unknowns    {unknowns}")
    print(f"  unknown ratio        {unknowns/max(published,1)*100:.1f}% of published claims say 'we do not know'")

    print()
    if share > 0.60:
        print(f"  ⚠ SKEWED — one publisher supplies {share*100:.0f}% of evidence.")
        print("    Read every cross-vendor statement with that in mind: the corpus is")
        print("    most confident about whoever documents most thoroughly, which is not")
        print("    the same as whoever matters most.")
    elif share > 0.40:
        print(f"  · CONCENTRATED — {share*100:.0f}% from one publisher. Improving.")
    else:
        print("  ✓ REASONABLY DISTRIBUTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
