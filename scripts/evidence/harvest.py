"""Primary-source community evidence retriever.

Fetches threads DIRECTLY from first-party discussion platforms. Never from
secondary summaries — COMMUNITY-EVIDENCE-PROTOCOL §7 classifies those as Class E.

Operational platforms (probe_platforms.py, 2026-08-04):
  - hacker_news        Algolia public API, no auth
  - github_discussions gh CLI + GraphQL, authenticated
  - stackexchange      API v2.3, quota-limited

Blocked: reddit (HTTP 403 without OAuth). See COMMUNITY-EVIDENCE-PROTOCOL §3.1.

Usage:
  python scripts/evidence/harvest.py --query "claude code" --since 2026-02-01
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "research" / "evidence" / "raw"
UA = "AI-Engineering-Atlas-Research/0.1 (evidence collection)"
TIMEOUT = 25
POLITE_DELAY_S = 1.0  # deliberate rate limiting; we are a guest on these APIs


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read())


def harvest_hn(query: str, since: str, limit: int = 30) -> list[dict]:
    """Hacker News via Algolia. Returns stories AND comments — comments are where
    friction reports live, which title-only search systematically misses."""
    ts = int(datetime.fromisoformat(since).replace(tzinfo=timezone.utc).timestamp())
    out = []
    for tag in ("story", "comment"):
        url = (
            "https://hn.algolia.com/api/v1/search_by_date?"
            + urllib.parse.urlencode(
                {"query": query, "tags": tag, "numericFilters": f"created_at_i>{ts}",
                 "hitsPerPage": limit}
            )
        )
        try:
            data = _get_json(url)
        except Exception as e:  # noqa: BLE001
            out.append({"platform": "hacker_news", "error": f"{type(e).__name__}: {e}"})
            continue
        for h in data.get("hits", []):
            out.append({
                "platform": "hacker_news",
                "kind": tag,
                "id": h.get("objectID"),
                "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                "title": h.get("title") or h.get("story_title"),
                "author": h.get("author"),
                "created_at": h.get("created_at"),
                "points": h.get("points"),
                "num_comments": h.get("num_comments"),
                "text": (h.get("comment_text") or h.get("story_text") or "")[:4000],
            })
        time.sleep(POLITE_DELAY_S)
    return out


def harvest_github(query: str, limit: int = 25) -> list[dict]:
    """GitHub issues + discussions via authenticated gh CLI.

    Searches issue/discussion BODIES, not just titles — Harvest 001's corrective
    action. No label filter: labels encode the maintainer's taxonomy, not the
    user's experience.
    """
    out = []
    for kind, gql_type in (("discussion", "DISCUSSION"), ("issue", "ISSUE")):
        q = (
            f'query{{search(query:"{query}",type:{gql_type},first:{limit}){{'
            "nodes{"
            "...on Discussion{title url createdAt bodyText author{login} comments{totalCount} repository{nameWithOwner}}"
            "...on Issue{title url createdAt bodyText author{login} comments{totalCount} repository{nameWithOwner}}"
            "}}}"
        )
        try:
            r = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={q}"],
                capture_output=True, text=True, timeout=60,
                encoding="utf-8", errors="replace",   # Windows cp1252 default breaks on UTF-8 bodies
            )
            if r.returncode != 0 or not r.stdout:
                out.append({"platform": "github", "kind": kind, "error": r.stderr.strip()[:200]})
                continue
            nodes = json.loads(r.stdout)["data"]["search"]["nodes"]
        except Exception as e:  # noqa: BLE001
            out.append({"platform": "github", "kind": kind, "error": f"{type(e).__name__}: {e}"})
            continue
        for n in nodes:
            if not n:
                continue
            out.append({
                "platform": "github",
                "kind": kind,
                "url": n.get("url"),
                "title": n.get("title"),
                "author": (n.get("author") or {}).get("login"),
                "created_at": n.get("createdAt"),
                "repo": (n.get("repository") or {}).get("nameWithOwner"),
                "num_comments": (n.get("comments") or {}).get("totalCount"),
                "text": (n.get("bodyText") or "")[:4000],
            })
        time.sleep(POLITE_DELAY_S)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--since", default="2026-02-01")
    ap.add_argument("--label", default=None, help="output file label")
    a = ap.parse_args()

    records = harvest_hn(a.query, a.since) + harvest_github(a.query)
    threads = [r for r in records if "error" not in r]
    errors = [r for r in records if "error" in r]
    authors = {r.get("author") for r in threads if r.get("author")}
    by_platform: dict[str, int] = {}
    for r in threads:
        by_platform[r["platform"]] = by_platform.get(r["platform"], 0) + 1

    result = {
        "harvest_date": datetime.now(timezone.utc).date().isoformat(),
        "declared_query": a.query,
        "executed_query": a.query,          # recorded verbatim — Harvest 001 fix
        "window_start": a.since,
        "platforms_attempted": ["hacker_news", "github"],
        "platforms_blocked": {"reddit": "HTTP 403 without OAuth credentials"},
        "counts": {
            "threads": len(threads),
            "distinct_authors": len(authors),
            "by_platform": by_platform,
        },
        "protocol_thresholds": {
            "min_independent_threads": 5,
            "min_distinct_participants": 50,
            "min_platforms": 2,
            "max_single_thread_share": 0.40,
        },
        "errors": errors,
        "records": threads,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    label = a.label or urllib.parse.quote_plus(a.query)[:40]
    path = OUT_DIR / f"harvest-{result['harvest_date']}-{label}.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2))
    print(f"\n{len(threads)} records -> {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
