"""Corpus loader — the single source of truth, made queryable.

ENGINE PURITY: this module contains no vendor, product, or model name. It reads
whatever is in /data and knows nothing about who made it. Validator rule
ENGINE-1 greps this directory and fails the build if that stops being true.

That is what makes "absorbs new categories without redesign" a property rather
than an aspiration.
"""
from __future__ import annotations

import collections
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


def provenance(g: dict, claim_ids: set[str]) -> dict:
    """Claims and their sources, verbatim, for the ids asked for.

    The interface lets a reader open any number and read the actual sentence on
    the actual page it came from. That is only possible if the excerpt travels
    with the figure, so it does.
    """
    claims, srcs = {}, {}
    for cid in claim_ids:
        c = g["claims"].get(cid)
        if not c:
            continue
        ev = []
        for e in c.get("evidence") or []:
            sid = e.get("source")
            s = g["sources"].get(sid)
            if not s:
                continue
            ref = e.get("excerpt_ref")
            text = next((x.get("text") for x in (s.get("excerpts") or [])
                         if x.get("id") == ref), None)
            loc = next((x.get("locator") for x in (s.get("excerpts") or [])
                        if x.get("id") == ref), None)
            ev.append({"source": sid, "excerpt": text, "locator": loc,
                       "supports": e.get("supports", True)})
            if sid not in srcs:
                pub = g["entities"].get(s.get("publisher") or "", {})
                srcs[sid] = {
                    "class": s.get("class"),
                    "title": s.get("title"),
                    "publisher": pub.get("name") or s.get("publisher"),
                    "url": s.get("canonical_url") or s.get("url"),
                    "archive_url": s.get("archive_url"),
                    "retrieved": s.get("retrieved"),
                    "hash_status": s.get("hash_status"),
                    "archive_status": s.get("archive_status"),
                    "fidelity": s.get("excerpt_fidelity"),
                    "flags": s.get("flags") or [],
                }
        t = c.get("temporal") or {}
        claims[cid] = {
            "statement": (c.get("statement") or "").strip(),
            "predicate": c.get("predicate"),
            "type": c.get("type"),
            "scope": c.get("scope"),
            "kind": c.get("temporal_kind"),
            "valid_from": t.get("valid_from"),
            "valid_to": t.get("valid_to"),
            "observed_at": t.get("observed_at"),
            "supersedes": c.get("supersedes"),
            "supersession_kind": c.get("supersession_kind"),
            "conditions": c.get("conditions") or {},
            "evidence": ev,
        }
    return {"claims": claims, "sources": srcs}


def calibration(g: dict) -> dict:
    """What the corpus knows about its own skew. Reported, not buried."""
    # Citations, not sources — one heavily-cited page skews a corpus more than
    # one lightly-cited one. Same metric the standing bias report tracks.
    pub = collections.Counter()
    for c in g["claims"].values():
        for e in c.get("evidence") or []:
            s = g["sources"].get(e.get("source") or "")
            if not s:
                continue
            name = g["entities"].get(s.get("publisher") or "", {}).get("name") or s.get("publisher")
            if name:
                pub[name] += 1
    published = [c for c in g["claims"].values() if c.get("status") == "published"]
    unk = [c for c in published if c.get("value") == "unknown"]
    top, n = pub.most_common(1)[0] if pub else (None, 0)
    return {
        "dominant_publisher": top,
        "dominant_share": round(n / sum(pub.values()), 4) if pub else None,
        "distinct_publishers": len(pub),
        "published_claims": len(published),
        "explicit_unknowns": len(unk),
        "unknown_ratio": round(len(unk) / len(published), 4) if published else None,
        "citations": pub.most_common(),
    }


def unknowns(g: dict) -> list[dict]:
    """Published claims whose value is an established unknown."""
    return [{"id": c["id"], "subject": c.get("_subject"), "statement": c.get("statement", "")}
            for c in g["claims"].values()
            if c.get("value") == "unknown" and c.get("status") == "published"]
