"""Backfill provenance for every source in the corpus.

Exercises scripts/atlas/capture.py across all source records and writes the
results back in place. Targeted line edits preserve the YAML comments, which
carry the admissibility reasoning.

Run: python scripts/atlas/backfill_capture.py [--dry-run] [--no-archive]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "data" / "sources"
UA = "AI-Engineering-Atlas-Research/0.1 (source capture; verification)"


class StrDateLoader(yaml.SafeLoader):
    pass


StrDateLoader.add_constructor(
    "tag:yaml.org,2002:timestamp", lambda l, n: l.construct_scalar(n)
)


def fetch_hash(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        return {"ok": True, "hash": hashlib.sha256(body).hexdigest(),
                "bytes": len(body), "status": r.status}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"{type(e).__name__}: {str(e)[:100]}"}


def archive(url: str) -> dict:
    try:
        avail = json.loads(urllib.request.urlopen(
            urllib.request.Request(
                f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}",
                headers={"User-Agent": UA}), timeout=30).read())
        snap = (avail.get("archived_snapshots") or {}).get("closest")
        if snap and snap.get("url"):
            return {"archive_status": "archived", "archive_url": snap["url"]}
    except Exception:  # noqa: BLE001
        pass
    try:
        with urllib.request.urlopen(
            urllib.request.Request(f"https://web.archive.org/save/{url}",
                                   headers={"User-Agent": UA}), timeout=120) as r:
            return {"archive_status": "archived", "archive_url": r.geturl()}
    except Exception as e:  # noqa: BLE001
        return {"archive_status": "failed", "archive_url": None,
                "error": f"{type(e).__name__}: {str(e)[:80]}"}


def patch_block(text: str, sid: str, hashval: str | None, arch: dict) -> tuple[str, bool]:
    """Replace provenance fields inside one source's block, comments intact."""
    start = text.find(f"- id: {sid}\n")
    if start == -1:
        return text, False
    nxt = text.find("\n  - id: src-", start + 1)
    end = nxt if nxt != -1 else len(text)
    block = text[start:end]
    orig = block

    if hashval:
        block = re.sub(r"content_hash: .*", f"content_hash: sha256:{hashval}", block, count=1)
        block = re.sub(r"hash_status: .*", "hash_status: hashed", block, count=1)
        block = re.sub(r"reverification: .*", "reverification: hash_triggered", block, count=1)
    if arch.get("archive_url"):
        block = re.sub(r"archive_url: .*", f"archive_url: {arch['archive_url']}", block, count=1)
        block = re.sub(r"archive_status: .*", "archive_status: archived", block, count=1)
    elif arch.get("archive_status") == "failed":
        block = re.sub(r"archive_status: .*", "archive_status: failed", block, count=1)

    return text[:start] + block + text[end:], block != orig


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-archive", action="store_true")
    a = ap.parse_args()

    summary = []
    for path in sorted(SRC_DIR.glob("*.yaml")):
        doc = yaml.load(path.read_text(encoding="utf-8"), Loader=StrDateLoader)
        text = path.read_text(encoding="utf-8")
        touched = False

        for s in doc.get("sources") or []:
            sid, url = s.get("id"), s.get("url")
            if not sid or not url:
                continue
            if s.get("hash_status") == "hashed" and s.get("archive_status") == "archived":
                summary.append({"id": sid, "result": "already_captured"})
                continue

            f = fetch_hash(url)
            arch = {} if a.no_archive else archive(url)
            time.sleep(1.5)  # polite

            rec = {"id": sid, "url": url,
                   "fetch": "ok" if f["ok"] else f.get("error"),
                   "hash": f.get("hash", "")[:16] + "..." if f["ok"] else None,
                   "archive": arch.get("archive_status", "skipped")}
            summary.append(rec)

            if f["ok"] or arch.get("archive_url"):
                text, ch = patch_block(text, sid, f.get("hash") if f["ok"] else None, arch)
                touched = touched or ch

        if touched and not a.dry_run:
            path.write_text(text, encoding="utf-8")
            print(f"updated {path.name}", file=sys.stderr)

    ok = sum(1 for r in summary if r.get("fetch") == "ok")
    archived = sum(1 for r in summary if r.get("archive") == "archived")
    already = sum(1 for r in summary if r.get("result") == "already_captured")
    print(json.dumps({
        "run_date": date.today().isoformat(),
        "sources_seen": len(summary),
        "already_captured": already,
        "hashed_now": ok,
        "archived_now": archived,
        "detail": summary,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
