"""Corpus loader — the single source of truth, made queryable.

ENGINE PURITY: this module contains no vendor, product, or model name. It reads
whatever is in /data and knows nothing about who made it. Validator rule
ENGINE-1 greps this directory and fails the build if that stops being true.

That is what makes "absorbs new categories without redesign" a property rather
than an aspiration.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


class StrDate(yaml.SafeLoader):
    """Dates load as strings — the schema is string-typed; JSON has no date."""


StrDate.add_constructor("tag:yaml.org,2002:timestamp",
                        lambda l, n: l.construct_scalar(n))

OPEN = "9999-12-31"


def _docs():
    for p in sorted(DATA.rglob("*.yaml")):
        if "schema" in p.parts:
            continue
        d = yaml.load(p.read_text(encoding="utf-8"), Loader=StrDate)
        if isinstance(d, dict):
            yield p, d


def load() -> dict:
    """Return {entities, claims, sources} indexed by id."""
    ents, claims, srcs = {}, {}, {}
    for _, d in _docs():
        for e in d.get("entities") or []:
            if isinstance(e, dict) and e.get("id"):
                ents[e["id"]] = e
                for c in e.get("claims") or []:
                    c["_subject"] = e["id"]
                    claims[c["id"]] = c
        for c in d.get("claims") or []:
            if isinstance(c, dict) and c.get("id"):
                c["_subject"] = c.get("subject")
                claims[c["id"]] = c
        for s in d.get("sources") or []:
            if isinstance(s, dict) and s.get("id"):
                srcs[s["id"]] = s
        if isinstance(d.get("id"), str) and d["id"].startswith("ent-"):
            ents[d["id"]] = d
            for c in d.get("claims") or []:
                c["_subject"] = d["id"]
                claims[c["id"]] = c
    return {"entities": ents, "claims": claims, "sources": srcs}


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def price_intervals(g: dict, entity_id: str) -> list[dict]:
    """Every pricing interval for an entity, from its claims.

    Handles both shapes present in the corpus: separate input/output claims,
    and a single combined claim. Returns [] when pricing is incomplete — an
    entity that cannot be priced is not priced, never estimated.
    """
    # Base pricing only. A premium or accelerated tier is a DIFFERENT PRODUCT at
    # the same moment, not another interval of the same one — merging them by
    # date silently overwrites the base rate. (Found by the first build: one
    # entity reported its premium tier as its base price.)
    BASE = {
        "pricing.input_per_mtok":       "in",
        "pricing.output_per_mtok":      "out",
        "pricing.cache_read_per_mtok":  "cache",
        "pricing.per_mtok":             "*",   # combined record
    }
    # value-key → slot, for combined records. Explicit; no inference.
    KEYS = {"input": "in", "input_miss": "in", "output": "out",
            "cache_read": "cache", "input_hit": "cache", "cache": "cache"}

    rows: dict[tuple, dict] = {}
    for c in g["claims"].values():
        if c.get("_subject") != entity_id:
            continue
        pred = c.get("predicate", "")
        slot = BASE.get(pred)
        if slot is None or c.get("status") not in ("published", "draft"):
            continue
        v = c.get("value")
        if not isinstance(v, dict):
            continue
        t = c.get("temporal") or {}
        key = (t.get("valid_from"), t.get("valid_to"))
        r = rows.setdefault(key, {"from": t.get("valid_from"), "to": t.get("valid_to"),
                                  "in": None, "cache": None, "out": None, "claims": []})
        r["claims"].append(c["id"])
        if slot == "*":
            for k, val in v.items():
                n = _num(val)
                if n is not None and k.lower() in KEYS:
                    r[KEYS[k.lower()]] = n
        else:
            n = _num(v.get("amount"))
            if n is None:
                for k in ("input", "output", "cache_read"):
                    n = _num(v.get(k))
                    if n is not None:
                        break
            if n is not None:
                r[slot] = n

    out = []
    for r in rows.values():
        if r["in"] is None or r["out"] is None:
            continue
        if r["cache"] is None:
            r["cache"] = round(r["in"] * 0.1, 6)   # documented convention where unstated
            r["cache_inferred"] = True
        r["from"] = r["from"] if isinstance(r["from"], str) and r["from"] != "unknown" else "2026-01-01"
        r["to"] = r["to"] if isinstance(r["to"], str) and r["to"] != "unknown" else OPEN
        out.append(r)
    return sorted(out, key=lambda r: r["from"])


def priced_entities(g: dict) -> list[dict]:
    """Entities the corpus can actually price, with their intervals."""
    res = []
    for eid, e in g["entities"].items():
        if "L1" not in (e.get("layers") or []):
            continue
        iv = price_intervals(g, eid)
        if not iv:
            continue
        res.append({"id": eid, "name": e.get("name"), "intervals": iv,
                    "openness": (e.get("facets") or {}).get("openness"),
                    "tokenizer_verified": (e.get("facets") or {}).get("tokenizer_verified", False)})
    return sorted(res, key=lambda m: m["intervals"][0]["in"])


def elicitable(g: dict) -> list[dict]:
    """Claims whose scope makes them non-transferable — each carries its question."""
    out = []
    for c in g["claims"].values():
        if c.get("scope") in ("harness", "operator", "workload") and c.get("elicit"):
            out.append({"id": c["id"], "scope": c["scope"], "predicate": c.get("predicate"),
                        "value": c.get("value"), "elicit": c["elicit"]})
    return out


def unknowns(g: dict) -> list[dict]:
    """Published claims whose value is an established unknown."""
    return [{"id": c["id"], "subject": c.get("_subject"), "statement": c.get("statement", "")}
            for c in g["claims"].values()
            if c.get("value") == "unknown" and c.get("status") == "published"]
