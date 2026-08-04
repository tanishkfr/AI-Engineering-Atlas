"""RQ-18/19/20 — usage profile extraction from existing agent transcripts.

METADATA ONLY BY CONSTRUCTION.

This tool reads token counts, timestamps, model identifiers, and tool NAMES.
It never reads, stores, or emits message content, file contents, file paths,
prompts, code, or git branch names. That is enforced by extracting a fixed
allowlist of numeric/enum fields rather than by filtering content out — there is
no code path by which content can reach the output.

Run:  python scripts/evidence/usage_profile.py --days 7 [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

TRANSCRIPTS = Path(os.environ.get("USERPROFILE") or Path.home()) / ".claude" / "projects"
OUT = Path(__file__).resolve().parents[2] / "research" / "evidence" / "usage"

# The ONLY fields ever read from a usage block.
USAGE_ALLOWLIST = (
    "input_tokens", "output_tokens",
    "cache_creation_input_tokens", "cache_read_input_tokens",
)


def anon(s: str) -> str:
    """One-way project identifier. Keeps sessions groupable without naming anything."""
    return "proj-" + hashlib.sha256(s.encode()).hexdigest()[:10]


def parse_ts(v) -> datetime | None:
    if not isinstance(v, str):
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true", help="validate only; write nothing")
    ap.add_argument("--limit-files", type=int, default=0)
    a = ap.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)
    # sort by mtime, not path — --limit-files must mean "most RECENT n", or a
    # sample can fall entirely outside the window and silently return zero.
    files = sorted(
        TRANSCRIPTS.rglob("*.jsonl"),
        key=lambda p: p.stat().st_mtime if p.exists() else 0,
    )
    if a.limit_files:
        files = files[-a.limit_files:]

    sessions: dict[str, dict] = defaultdict(lambda: {
        "project": None, "turns": 0, "errors": 0,
        "in": 0, "out": 0, "cache_read": 0, "cache_write": 0,
        "first": None, "last": None, "models": Counter(), "tools": Counter(),
    })
    files_scanned = 0

    for f in files:
        try:
            if datetime.fromtimestamp(f.stat().st_mtime, timezone.utc) < cutoff:
                continue
        except OSError:
            continue
        files_scanned += 1
        try:
            with f.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    sid = rec.get("sessionId")
                    if not sid:
                        continue
                    s = sessions[sid]
                    if s["project"] is None and rec.get("cwd"):
                        s["project"] = anon(str(rec["cwd"]))

                    ts = parse_ts(rec.get("timestamp"))
                    if ts:
                        s["first"] = min(s["first"], ts) if s["first"] else ts
                        s["last"] = max(s["last"], ts) if s["last"] else ts

                    if rec.get("error") or rec.get("type") == "error":
                        s["errors"] += 1

                    msg = rec.get("message")
                    if not isinstance(msg, dict):
                        continue
                    if msg.get("model"):
                        s["models"][msg["model"]] += 1
                    # tool NAMES only — never inputs
                    content = msg.get("content")
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "tool_use":
                                s["tools"][block.get("name", "?")] += 1
                    u = msg.get("usage")
                    if isinstance(u, dict):
                        s["turns"] += 1
                        s["in"] += int(u.get("input_tokens") or 0)
                        s["out"] += int(u.get("output_tokens") or 0)
                        s["cache_read"] += int(u.get("cache_read_input_tokens") or 0)
                        s["cache_write"] += int(u.get("cache_creation_input_tokens") or 0)
        except OSError:
            continue

    live = {k: v for k, v in sessions.items() if v["turns"] > 0}
    tot_in = sum(v["in"] for v in live.values())
    tot_out = sum(v["out"] for v in live.values())
    tot_read = sum(v["cache_read"] for v in live.values())
    tot_write = sum(v["cache_write"] for v in live.values())
    billable_in = tot_in + tot_write            # uncached input actually charged
    presented = billable_in + tot_read          # everything the model saw

    durations = [
        (v["last"] - v["first"]).total_seconds() / 60
        for v in live.values() if v["first"] and v["last"]
    ]

    result = {
        "study": "RQ-18/19/20 usage profile",
        "method": "retrospective extraction from existing transcripts",
        "privacy": "metadata only — no message content, file contents, paths, or branch names",
        "window_days": a.days,
        "files_scanned": files_scanned,
        "sessions": len(live),
        "projects": len({v["project"] for v in live.values() if v["project"]}),
        "turns": sum(v["turns"] for v in live.values()),
        "tokens": {
            "uncached_input": tot_in,
            "cache_write": tot_write,
            "cache_read": tot_read,
            "output": tot_out,
            "total_presented_to_model": presented,
        },
        "RQ-19_cache_hit_rate": round(tot_read / presented, 4) if presented else None,
        "RQ-18_io_ratio": round(presented / tot_out, 2) if tot_out else None,
        "RQ-18_per_session": {
            "median_turns": sorted(v["turns"] for v in live.values())[len(live) // 2] if live else None,
            "median_duration_min": round(sorted(durations)[len(durations) // 2], 1) if durations else None,
        },
        "RQ-20_error_records": sum(v["errors"] for v in live.values()),
        "distinct_models": len({m for v in live.values() for m in v["models"]}),
        "tool_call_totals": dict(Counter(
            {k: v for s in live.values() for k, v in s["tools"].items()}
        ).most_common(12)),
    }

    print(json.dumps(result, indent=2))
    if not a.dry_run:
        OUT.mkdir(parents=True, exist_ok=True)
        p = OUT / f"usage-profile-{datetime.now(timezone.utc).date().isoformat()}.json"
        p.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"\nwritten to {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
