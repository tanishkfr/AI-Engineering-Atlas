"""Probe first-party discussion platforms for primary-source retrieval.

Determines empirically which platforms can be queried directly, without going
through secondary summaries. Read-only. Single request per platform. Respects
robots/ToS by using documented public APIs where they exist.

Run: python scripts/evidence/probe_platforms.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request

UA = "AI-Engineering-Atlas-Research/0.1 (evidence collection; contact: repo maintainer)"
TIMEOUT = 20

PROBES = [
    {
        "platform": "hacker_news",
        "method": "Algolia public API",
        "url": "https://hn.algolia.com/api/v1/search?query=claude%20code&tags=story&hitsPerPage=2",
        "auth": "none",
    },
    {
        "platform": "reddit_json",
        "method": "public .json endpoint",
        "url": "https://www.reddit.com/r/ClaudeAI/search.json?q=switched&restrict_sr=1&limit=2",
        "auth": "none",
    },
    {
        "platform": "reddit_old",
        "method": "old.reddit .json endpoint",
        "url": "https://old.reddit.com/r/ChatGPTCoding/search.json?q=switched&restrict_sr=1&limit=2",
        "auth": "none",
    },
    {
        "platform": "lobsters",
        "method": "public JSON",
        "url": "https://lobste.rs/search.json?q=claude&what=stories&order=newest",
        "auth": "none",
    },
    {
        "platform": "stackexchange",
        "method": "Stack Exchange API v2.3",
        "url": "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=aider&site=stackoverflow&pagesize=2",
        "auth": "none (quota-limited)",
    },
]


def probe_http(p: dict) -> dict:
    req = urllib.request.Request(p["url"], headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(200_000)
            status = r.status
        try:
            data = json.loads(body)
            shape = list(data.keys())[:6] if isinstance(data, dict) else f"list[{len(data)}]"
            n = None
            for key in ("hits", "items", "data"):
                if isinstance(data, dict) and key in data:
                    v = data[key]
                    if isinstance(v, list):
                        n = len(v)
                    elif isinstance(v, dict) and "children" in v:
                        n = len(v["children"])
            return {**p, "status": status, "ok": True, "json": True, "top_keys": shape, "results": n}
        except json.JSONDecodeError:
            return {**p, "status": status, "ok": True, "json": False,
                    "note": "200 but not JSON — likely an HTML wall"}
    except urllib.error.HTTPError as e:
        return {**p, "status": e.code, "ok": False, "error": f"HTTPError {e.code} {e.reason}"}
    except Exception as e:  # noqa: BLE001
        return {**p, "status": None, "ok": False, "error": f"{type(e).__name__}: {str(e)[:120]}"}


def probe_gh_cli() -> dict:
    out = {"platform": "github_discussions", "method": "gh CLI + GraphQL", "auth": "gh auth"}
    try:
        r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=25)
        authed = r.returncode == 0
        out["gh_installed"] = True
        out["gh_authenticated"] = authed
        if not authed:
            out["ok"] = False
            out["error"] = "gh present but not authenticated"
            return out
        q = (
            'query{search(query:"repo:Aider-AI/aider switched",type:DISCUSSION,first:2)'
            "{discussionCount}}"
        )
        r2 = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}"],
                            capture_output=True, text=True, timeout=40)
        if r2.returncode == 0:
            out["ok"] = True
            out["sample"] = r2.stdout.strip()[:200]
        else:
            out["ok"] = False
            out["error"] = r2.stderr.strip()[:200]
    except FileNotFoundError:
        out.update({"gh_installed": False, "ok": False, "error": "gh not installed"})
    except Exception as e:  # noqa: BLE001
        out.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:120]}"})
    return out


def main() -> int:
    results = [probe_http(p) for p in PROBES]
    results.append(probe_gh_cli())
    print(json.dumps({"probe_date": "2026-08-04", "results": results}, indent=2))
    usable = [r["platform"] for r in results if r.get("ok") and r.get("json", True)]
    print(f"\nUSABLE: {usable}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
