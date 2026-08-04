"""Repair mojibake and BOMs introduced by PowerShell 5.1 file edits.

PS5.1 `Get-Content -Raw` decodes UTF-8 as ANSI and `Set-Content -Encoding utf8`
writes a BOM. Both corrupt JSON. Recorded as a tooling lesson: never edit
UTF-8 data files through PS5.1 text cmdlets.

Originally scoped to data/schema/*.json. Widened after 89 corrupted sequences
were found across nine files, including the shipped interface and NOW.md — the
two things a reader sees first. A one-off fix for a recurring tooling fault was
the wrong shape; this sweeps every text file in the repo.

Run: python scripts/atlas/repair_encoding.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MOJIBAKE = {
    # Longest first. No sequence is a prefix of another, so order is not load-bearing.
    "â”€": "─",     # box drawing, used in the ASCII rules across the docs
    "â€”": "—",     # em dash
    "â€“": "–",     # en dash
    "â€™": "'",          # right single quote -> plain apostrophe
    "â‰¥": "≥",     # greater-or-equal
    "Â§": "§",           # section sign
    "Â·": "·",           # middle dot
}

SKIP_DIRS = {".git", "__pycache__", ".venv", "dist"}
SUFFIXES = {".md", ".html", ".yaml", ".yml", ".json", ".py", ".txt"}
# This file's own mapping table IS the mojibake. Repairing it would destroy the keys.
SELF = Path(__file__).resolve()


def repair(text: str) -> str:
    for bad, good in MOJIBAKE.items():
        text = text.replace(bad, good)
    return text


changed = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.suffix.lower() not in SUFFIXES:
        continue
    if p.resolve() == SELF or any(part in SKIP_DIRS for part in p.parts):
        continue
    try:
        raw = p.read_bytes()
        text = raw.decode("utf-8-sig")
    except (UnicodeDecodeError, OSError):
        continue
    # A BOM is only stripped where it cannot change how the file is decoded.
    # HTML served over HTTP relies on it unless the document declares a charset.
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    strip_bom = had_bom and (p.suffix.lower() != ".html" or "<meta charset" in text.lower())
    fixed = repair(text)
    if fixed != text or strip_bom:
        p.write_bytes(fixed.encode("utf-8" if strip_bom else "utf-8-sig" if had_bom else "utf-8"))
        changed.append(
            f"{p.relative_to(ROOT)} (bom_stripped={strip_bom}, mojibake={fixed != text})"
        )

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
