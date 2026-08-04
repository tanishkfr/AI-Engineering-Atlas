"""Probe local agent transcripts for RQ-18 feasibility.

Determines whether the four assumptions RQ-18/19/20/21 can be answered from data
that ALREADY EXISTS, before building any prospective logger.

Read-only. Reports structure and field availability only — no content, no
message text, no file paths beyond counts.

Run: python scripts/evidence/probe_transcripts.py
"""
from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(os.environ.get("USERPROFILE") or Path.home()) / ".claude" / "projects"


def main() -> int:
    files = sorted(ROOT.rglob("*.jsonl"))
    if not files:
        print(json.dumps({"error": f"no transcripts under {ROOT}"}))
        return 1

    record_types = Counter()
    usage_fields = Counter()
    top_keys = Counter()
    models = Counter()
    sampled_records = 0
    files_with_usage = 0
    sample = files[-40:]  # most recent, enough to characterise structure

    for f in sample:
        has_usage = False
        try:
            with f.open(encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i > 400:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    sampled_records += 1
                    for k in rec:
                        top_keys[k] += 1
                    record_types[rec.get("type", "<none>")] += 1
                    msg = rec.get("message")
                    if isinstance(msg, dict):
                        if msg.get("model"):
                            models[msg["model"]] += 1
                        u = msg.get("usage")
                        if isinstance(u, dict):
                            has_usage = True
                            for k in u:
                                usage_fields[k] += 1
        except OSError:
            continue
        files_with_usage += has_usage

    need = {
        "input_tokens": "RQ-18 token volume",
        "output_tokens": "RQ-18 token volume",
        "cache_read_input_tokens": "RQ-19 cache hit rate",
        "cache_creation_input_tokens": "RQ-19 cache write cost",
    }
    coverage = {f: {"present": usage_fields.get(f, 0) > 0, "answers": why}
                for f, why in need.items()}

    print(json.dumps({
        "transcript_root": str(ROOT),
        "total_files": len(files),
        "files_sampled": len(sample),
        "records_sampled": sampled_records,
        "files_with_usage_block": files_with_usage,
        "record_types": dict(record_types.most_common(10)),
        "top_level_keys": dict(top_keys.most_common(14)),
        "usage_fields_found": dict(usage_fields.most_common()),
        "distinct_models_seen": len(models),
        "rq_field_coverage": coverage,
        "verdict": (
            "RETROSPECTIVE_VIABLE" if all(c["present"] for c in coverage.values())
            else "PARTIAL — some fields absent; prospective logger needed for those"
        ),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
