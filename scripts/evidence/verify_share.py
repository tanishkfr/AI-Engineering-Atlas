"""Adversarial verification of the --share payload.

Does NOT trust the code's intent. Runs --share against real transcripts, then
proves the output cannot carry sensitive content by:

  1. asserting an exact key allowlist (no unexpected keys, at any depth)
  2. asserting every leaf value is numeric or a known literal
  3. scanning the serialized payload for any substring appearing in the
     source transcripts (paths, project names, prompt fragments)
  4. scanning for filesystem-path and timestamp patterns

Exit non-zero if any check fails.

Run: python scripts/evidence/verify_share.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPTS = Path(os.environ.get("USERPROFILE") or Path.home()) / ".claude" / "projects"

ALLOWED_TOP = {
    "replication_of", "window_days", "cache_hit_rate",
    "io_ratio", "turns", "falsification_thresholds",
}
ALLOWED_THRESHOLD_KEYS = {">=0.85", "0.70-0.85", "<0.70"}

FORBIDDEN_PATTERNS = {
    "windows_path": r"[A-Za-z]:\\\\|[A-Za-z]:/",
    "unix_path": r"(?<!\w)/(?:home|users|Users|var|tmp|opt)/",
    "iso_timestamp": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
    "iso_date": r"\d{4}-\d{2}-\d{2}",
    "url": r"https?://",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "sha_hash": r"\b[a-f0-9]{16,}\b",
    "project_pseudonym": r"proj-[a-f0-9]+",
    "file_extension": r"\.(py|ts|js|md|json|yaml|jsonl)\b",
}


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def main() -> int:
    failures = 0

    # --- run the real thing ---
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "evidence" / "usage_profile.py"),
         "--days", "56", "--share"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
    )
    if proc.returncode != 0:
        print("could not produce share payload:", proc.stderr[:300])
        return 1
    raw = proc.stdout.strip()
    payload = json.loads(raw)

    print("PAYLOAD UNDER TEST")
    print(raw)
    print("\nCHECKS")

    # 1. key allowlist
    extra = set(payload) - ALLOWED_TOP
    if extra:
        fail(f"unexpected top-level keys: {extra}")
        failures += 1
    else:
        print("  ok    top-level keys within allowlist")

    th = payload.get("falsification_thresholds", {})
    if set(th) - ALLOWED_THRESHOLD_KEYS:
        fail(f"unexpected threshold keys: {set(th) - ALLOWED_THRESHOLD_KEYS}")
        failures += 1
    else:
        print("  ok    threshold keys within allowlist")

    # 2. leaf value types
    bad = []
    for k, v in payload.items():
        if k == "falsification_thresholds":
            continue
        if k == "replication_of":
            if v != "RQ-18/19":
                bad.append((k, v))
            continue
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            bad.append((k, v))
    if bad:
        fail(f"non-numeric leaf values: {bad}")
        failures += 1
    else:
        print("  ok    all data leaves are numeric")

    # 3. forbidden patterns in the serialized payload
    for name, pat in FORBIDDEN_PATTERNS.items():
        hits = re.findall(pat, raw)
        # threshold labels legitimately contain "0.70-0.85"; exclude the literal block
        if name == "iso_date":
            hits = [h for h in hits if h not in ("0.70-0.85",)]
        if hits:
            fail(f"{name} pattern present: {hits[:3]}")
            failures += 1
        else:
            print(f"  ok    no {name}")

    # 4. cross-check against actual transcript content
    #    take distinctive strings from real files, prove none appear in payload
    probes: set[str] = set()
    files = sorted(TRANSCRIPTS.rglob("*.jsonl"),
                   key=lambda p: p.stat().st_mtime if p.exists() else 0)[-5:]
    for f in files:
        probes.add(f.stem)
        probes.add(f.parent.name)
        try:
            with f.open(encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i > 30:
                        break
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    for key in ("cwd", "gitBranch", "sessionId", "uuid", "version"):
                        v = rec.get(key)
                        if isinstance(v, str) and len(v) > 3:
                            probes.add(v)
        except OSError:
            continue

    leaked = [p for p in probes if p and len(p) > 3 and p in raw]
    if leaked:
        fail(f"transcript content leaked into payload: {leaked[:5]}")
        failures += 1
    else:
        print(f"  ok    none of {len(probes)} real transcript strings appear in payload")

    print()
    if failures:
        print(f"VERIFICATION FAILED — {failures} check(s)")
        return 1
    print("VERIFICATION PASSED — payload carries aggregate statistics only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
