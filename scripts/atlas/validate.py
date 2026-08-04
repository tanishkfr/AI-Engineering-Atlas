"""Atlas validator — turns SCHEMA.md §11 from prose into an executable gate.

Exits non-zero on any error. This is the "the build fails" that the documents
have been asserting in the present tense since M2.

Run: python scripts/atlas/validate.py [--corpus data]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "data" / "schema"

# Which top-level list key holds which record type.
COLLECTIONS = {
    "entities": "entity.schema.json",
    "sources": "source.schema.json",
    "capabilities": "capability.schema.json",
    "objectives": "objective.schema.json",
    "profiles": "usage-profile.schema.json",
}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict[str, int] = {}

    def error(self, rule: str, where: str, msg: str) -> None:
        self.errors.append(f"[{rule}] {where}: {msg}")

    def warn(self, rule: str, where: str, msg: str) -> None:
        self.warnings.append(f"[{rule}] {where}: {msg}")


def build_registry() -> Registry:
    reg = Registry()
    for p in SCHEMA_DIR.glob("*.json"):
        contents = json.loads(p.read_text(encoding="utf-8"))
        res = Resource.from_contents(contents, default_specification=DRAFT202012)
        # register under both the bare filename and the declared $id
        reg = reg.with_resource(p.name, res)
        if "$id" in contents:
            reg = reg.with_resource(contents["$id"], res)
    return reg


class StrDateLoader(yaml.SafeLoader):
    """YAML 1.1 auto-casts unquoted ISO dates to datetime.date. The schema is
    string-typed (JSON has no date type), so dates are loaded as strings.
    This is a serialization concern, not a data concern."""


StrDateLoader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    lambda loader, node: loader.construct_scalar(node),
)


def load_docs(corpus: Path) -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(corpus.rglob("*.yaml")):
        if "schema" in p.parts:
            continue
        try:
            doc = yaml.load(p.read_text(encoding="utf-8"), Loader=StrDateLoader)
        except yaml.YAMLError as e:
            out.append((p, {"__yaml_error__": str(e)[:200]}))
            continue
        if isinstance(doc, dict):
            out.append((p, doc))
    return out


def iter_records(doc: dict) -> list[tuple[str, dict]]:
    """Yield (schema_name, record) for every record in a document."""
    recs: list[tuple[str, dict]] = []
    for key, schema in COLLECTIONS.items():
        if isinstance(doc.get(key), list):
            for r in doc[key]:
                if isinstance(r, dict):
                    recs.append((schema, r))
    # single-record documents
    if not recs and isinstance(doc.get("id"), str):
        rid = doc["id"]
        if rid.startswith("ent-"):
            recs.append(("entity.schema.json", doc))
        elif rid.startswith("per-"):
            recs.append(("persona.schema.json", doc))
    return recs


def validate(corpus: Path) -> Report:
    rep = Report()
    registry = build_registry()
    docs = load_docs(corpus)

    entity_ids: set[str] = set()
    source_ids: set[str] = set()
    capability_ids: set[str] = set()
    claim_ids: list[str] = []
    all_claims: list[tuple[str, dict]] = []
    all_entities: list[tuple[str, dict]] = []
    source_class: dict[str, str] = {}

    # ---- pass 1: structure + index ----
    for path, doc in docs:
        where = str(path.relative_to(ROOT))
        if "__yaml_error__" in doc:
            rep.error("STRUCT", where, f"YAML parse failure: {doc['__yaml_error__']}")
            continue
        for schema_name, rec in iter_records(doc):
            rid = rec.get("id", "<no id>")
            if schema_name == "entity.schema.json":
                if rid in entity_ids:
                    rep.error("ID-UNIQUE", where, f"duplicate entity id {rid}")
                entity_ids.add(rid)
                all_entities.append((where, rec))
                for c in rec.get("claims") or []:
                    all_claims.append((f"{where}#{rid}", c))
            elif schema_name == "source.schema.json":
                if rid in source_ids:
                    rep.error("ID-UNIQUE", where, f"duplicate source id {rid}")
                source_ids.add(rid)
                source_class[rid] = rec.get("class", "?")
            elif schema_name == "capability.schema.json":
                capability_ids.add(rid)

            # JSON Schema conformance
            try:
                v = Draft202012Validator(
                    {"$ref": schema_name}, registry=registry
                )
                for err in sorted(v.iter_errors(rec), key=lambda e: list(e.path)):
                    loc = "/".join(str(x) for x in err.path) or "<root>"
                    rep.error("SCHEMA", f"{where}#{rid}", f"{loc}: {err.message[:160]}")
            except Exception as e:  # noqa: BLE001
                rep.warn("SCHEMA", f"{where}#{rid}", f"validator error: {type(e).__name__}: {e}")

    # ---- pass 2: cross-record rules (SCHEMA §11) ----
    for where, claim in all_claims:
        cid = claim.get("id", "<no id>")
        loc = f"{where}#{cid}"
        if cid in claim_ids:
            rep.error("ID-UNIQUE", loc, "duplicate claim id")
        claim_ids.append(cid)

        status = claim.get("status")
        ctype = claim.get("type")
        evidence = claim.get("evidence") or []

        # R-EVID-1: published claim needs at least one evidence ref
        if status == "published" and not evidence:
            rep.error("EVID-1", loc, "published claim with no evidence")

        # R-EVID-2: dangling source reference
        for ev in evidence:
            src = ev.get("source")
            if src and src not in source_ids:
                rep.error("EVID-2", loc, f"evidence cites unknown source {src}")

        # R-EVID-3: no Class-E-only published claims (SOURCES §1)
        if status == "published" and evidence:
            classes = {source_class.get(e.get("source"), "?") for e in evidence}
            if classes and classes <= {"E"}:
                rep.error("EVID-3", loc, "published claim supported only by Class E sources")

        # R-EVID-4: comparative claims need >= 2 independent sources
        if ctype == "C" and len({e.get("source") for e in evidence}) < 2:
            rep.error("EVID-4", loc, "comparative (C) claim with fewer than 2 distinct sources")

        # R-INTEG-1: confidence and freshness are COMPUTED, never authored
        for field in ("confidence", "freshness"):
            if field in claim:
                rep.error("INTEG-1", loc, f"'{field}' is computed; authoring it is forbidden")

        # R-TEMP-1: measurement/series claims require conditions
        if claim.get("temporal_kind") in ("measurement", "series") and not claim.get("conditions"):
            rep.error("TEMP-1", loc, "measurement/series claim without conditions block")

        # R-TEMP-2: bitemporal completeness
        t = claim.get("temporal") or {}
        for field in ("valid_from", "asserted_from", "observed_at"):
            if field not in t:
                rep.error("TEMP-2", loc, f"temporal.{field} missing")

        # R-CLAIM-1: F-type claims never publish
        if ctype == "F" and status == "published":
            rep.error("CLAIM-1", loc, "forecast (F) claims may not be published")

    # ---- pass 2.5: assumption register (ASSUMPTIONS.md) ----
    # ASSUM-1: any record carrying status: assumed must name the RQ that would
    # replace it. An assumption without a path to measurement is a permanent
    # guess wearing a temporary label.
    for path, doc in docs:
        where = str(path.relative_to(ROOT))
        for key in ("profiles", "entities", "sources"):
            for rec in doc.get(key) or []:
                if not isinstance(rec, dict):
                    continue
                if rec.get("status") == "assumed" and not rec.get("rq"):
                    rep.error("ASSUM-1", f"{where}#{rec.get('id')}",
                              "status: assumed requires an 'rq:' field naming the "
                              "research question that would replace it")

    # ---- pass 3: graph integrity ----
    for where, ent in all_entities:
        eid = ent.get("id")
        loc = f"{where}#{eid}"
        mb = ent.get("made_by")
        if mb and mb not in entity_ids:
            rep.error("GRAPH-1", loc, f"made_by references unknown entity {mb}")
        for rel in ent.get("relationships") or []:
            obj = rel.get("object", "")
            pred = rel.get("predicate")
            if obj == eid:
                rep.error("GRAPH-2", loc, f"self-edge on {pred}")
            known = entity_ids | capability_ids | source_ids
            if obj.startswith(("ent-", "cap-")) and obj not in known:
                rep.warn("GRAPH-3", loc, f"{pred} -> unknown object {obj}")
            if pred in ("recommended_for", "unsuitable_for") and not rel.get("derived"):
                rep.error("GRAPH-4", loc, f"{pred} must be engine-derived, not authored")
        # active entities must carry claims
        if ent.get("status") == "active" and not (ent.get("claims") or []):
            rep.error("GRAPH-5", loc, "active entity with zero claims")

    rep.stats = {
        "documents": len(docs),
        "entities": len(entity_ids),
        "claims": len(claim_ids),
        "sources": len(source_ids),
        "capabilities": len(capability_ids),
        "errors": len(rep.errors),
        "warnings": len(rep.warnings),
    }
    return rep


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "data"))
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rep = validate(Path(a.corpus))

    print(json.dumps(rep.stats, indent=2))
    if rep.warnings and not a.quiet:
        print(f"\n--- {len(rep.warnings)} warnings ---")
        for w in rep.warnings[:25]:
            print(f"  {w}")
    if rep.errors:
        print(f"\n--- {len(rep.errors)} ERRORS ---")
        for e in rep.errors[:60]:
            print(f"  {e}")
        print("\nVALIDATION FAILED")
        return 1
    print("\nVALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
