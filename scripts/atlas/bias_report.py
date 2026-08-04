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

# This report draws bar charts. A default Windows console is cp1252 and raised
# UnicodeEncodeError instead of printing the bias metric.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def main() -> int:
    cites = collections.Counter()
    entities = collections.Counter()
    unknowns = 0
    published = 0

    for p in DATA.rglob("*.yaml"):
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r"source: (src-[a-z0-9]+)", t):
            cites[m.group(1).split("-", 1)[1]] += 1
        for m in re.finditer(r"made_by: ent-institution-([a-z0-9-]+)", t):
            entities[m.group(1)] += 1
        unknowns += len(re.findall(r"^\s*value: unknown", t, re.M))
        published += len(re.findall(r"status: published", t))

    total = sum(cites.values()) or 1
    top = cites.most_common(1)[0] if cites else ("none", 0)

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
