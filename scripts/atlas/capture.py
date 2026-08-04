"""Source capture — fetch, hash, archive. Closes Trust Audit item #4.

Hashes the RAW response body, not a rendered version. A hash of a rendering
changes when the renderer changes, not when the page changes, which defeats the
entire purpose (SOURCES §7).

Run: python scripts/atlas/capture.py --url URL [--archive]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date

UA = "AI-Engineering-Atlas-Research/0.1 (source capture; verification)"
TIMEOUT = 30


def fetch_raw(url: str) -> tuple[bytes, int, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read(), r.status, dict(r.headers)


def archive(url: str) -> dict:
    """Submit to the Wayback Machine's save endpoint."""
    save = f"https://web.archive.org/save/{url}"
    req = urllib.request.Request(save, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            final = r.geturl()
        return {"archive_status": "archived", "archive_url": final}
    except urllib.error.HTTPError as e:
        # Wayback often 4xx/5xx while still having captured; probe availability.
        try:
            avail = json.loads(
                urllib.request.urlopen(
                    urllib.request.Request(
                        f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}",
                        headers={"User-Agent": UA},
                    ),
                    timeout=30,
                ).read()
            )
            snap = (avail.get("archived_snapshots") or {}).get("closest")
            if snap and snap.get("url"):
                return {"archive_status": "archived", "archive_url": snap["url"],
                        "note": f"save returned {e.code}; existing snapshot used"}
        except Exception:  # noqa: BLE001
            pass
        return {"archive_status": "failed", "archive_url": None, "error": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"archive_status": "failed", "archive_url": None,
                "error": f"{type(e).__name__}: {str(e)[:120]}"}


def main() -> int:
    import urllib.parse  # noqa: PLC0415  (used by archive())

    globals()["urllib"].parse = urllib.parse
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--archive", action="store_true")
    a = ap.parse_args()

    body, status, headers = fetch_raw(a.url)
    digest = hashlib.sha256(body).hexdigest()

    out = {
        "url": a.url,
        "http_status": status,
        "retrieved": date.today().isoformat(),
        "bytes": len(body),
        "content_type": headers.get("Content-Type"),
        "content_hash": f"sha256:{digest}",
        "hash_status": "hashed",
        "reverification": "hash_triggered",
        "archive_status": "pending",
        "archive_url": None,
    }

    if a.archive:
        time.sleep(1)
        out.update(archive(a.url))

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
