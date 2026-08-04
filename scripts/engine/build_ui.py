"""Emit the interface from the corpus.

Closes the two-sources-of-truth defect: prices were hardcoded in the UI's
JavaScript while the same numbers lived in /data with hashes and validity
intervals. CONSTITUTION §9 says a fact exists exactly once. It now does — the
HTML is a build output, not a hand-maintained file.

ENGINE PURITY: no vendor or product names in this file. Everything comes from
the corpus.

Run: python scripts/engine/build_ui.py [--out dist/aletheia.html]
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import corpus as C

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "ui" / "template.html"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "dist" / "aletheia.html"))
    a = ap.parse_args()

    g = C.load()
    models = C.priced_entities(g)
    el = C.elicitable(g)

    # the workload question drives the cost model; find it by SCOPE, not by name
    wl = next((e for e in el if e["scope"] == "workload"), None)
    hw = next((e for e in el if e["scope"] == "harness"), None)

    payload = {
        "generated": date.today().isoformat(),
        "models": [{
            "name": m["name"],
            "openness": m["openness"],
            "tokenizer_verified": m["tokenizer_verified"],
            "intervals": [{"from": i["from"], "to": i["to"], "in": i["in"],
                           "cache": i["cache"], "out": i["out"],
                           "cache_inferred": i.get("cache_inferred", False),
                           "claims": i["claims"]} for i in m["intervals"]],
        } for m in models],
        "elicit": {
            "workload": wl["elicit"] if wl else None,
            "harness": hw["elicit"] if hw else None,
        },
        "cache_hit": (hw or {}).get("value", {}).get("rate") if hw else None,
        "unknowns": C.unknowns(g),
        "counts": {
            "entities": len(g["entities"]),
            "claims": len(g["claims"]),
            "sources": len(g["sources"]),
            "priced": len(models),
            "unknowns": len(C.unknowns(g)),
        },
    }

    tpl = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__CORPUS__*/"
    if marker not in tpl:
        print(f"template missing {marker}")
        return 1
    html = tpl.replace(marker, json.dumps(payload, separators=(",", ":")))

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    print(json.dumps(payload["counts"], indent=2))
    print(f"\npriced from corpus:")
    for m in models:
        iv = m["intervals"]
        span = f"{len(iv)} interval{'s' if len(iv) > 1 else ''}"
        inf = " (cache inferred)" if any(i.get("cache_inferred") for i in iv) else ""
        print(f"  {m['name']:26s} ${iv[0]['in']:<7.3f} in   {span}{inf}")
    if wl:
        print(f"\nelicits on scope={wl['scope']}: {wl['elicit']['question']}")
    print(f"\nwritten to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
