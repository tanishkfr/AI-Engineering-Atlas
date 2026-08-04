"""One-off repair: strip BOMs and mojibake introduced by PowerShell 5.1 file edits.

PS5.1 `Get-Content -Raw` decodes UTF-8 as ANSI and `Set-Content -Encoding utf8`
writes a BOM. Both corrupt JSON. Recorded as a tooling lesson: never edit
UTF-8 data files through PS5.1 text cmdlets.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MOJIBAKE = {
    "Â§": "§",           # Â§ -> §
    "â€”": "—",     # â€" -> —
    "â€™": "'",          # â€™ -> '
    "â‰¥": "≥",     # â‰¥ -> ≥
}

changed = []
for p in sorted((ROOT / "data" / "schema").glob("*.json")):
    raw = p.read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    fixed = text
    for bad, good in MOJIBAKE.items():
        fixed = fixed.replace(bad, good)
    if had_bom or fixed != text:
        p.write_bytes(fixed.encode("utf-8"))
        changed.append(f"{p.name} (bom={had_bom}, mojibake={fixed != text})")

# Data fix: benchmark construct validity and selection bias are `step` facts —
# they hold until the benchmark itself changes. `static` means true by
# definition and forever, which forces cadence >= 3650 and is wrong here.
swe = ROOT / "data" / "entities" / "evidence" / "swe-bench.yaml"
s = swe.read_text(encoding="utf-8")
before = s
for pred in ("benchmark.construct_validity", "benchmark.selection_bias"):
    s = s.replace(
        f"temporal_kind: static\n        subject: ent-benchmark-swe-bench\n        predicate: {pred}",
        f"temporal_kind: step\n        subject: ent-benchmark-swe-bench\n        predicate: {pred}",
    )
if s != before:
    swe.write_text(s, encoding="utf-8")
    changed.append("swe-bench.yaml (static -> step)")

print("\n".join(changed) if changed else "nothing to repair")
