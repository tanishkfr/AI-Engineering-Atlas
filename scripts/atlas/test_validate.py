"""Test suite for the validator.

A validation rule that has never failed is a rule you cannot trust. Every test
here builds a corpus that DELIBERATELY violates one rule and asserts the
validator catches it â€” plus a clean corpus that must pass.

Run: python scripts/atlas/test_validate.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from validate import validate  # noqa: E402

PASS, FAIL = "  ok  ", "  FAIL"
results = []


def corpus(files: dict[str, str]) -> Path:
    d = Path(tempfile.mkdtemp(prefix="atlas-test-"))
    (d / "schema").mkdir()
    for f in (ROOT / "data" / "schema").glob("*.json"):
        shutil.copy(f, d / "schema" / f.name)
    for name, body in files.items():
        p = d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return d


def check(name: str, files: dict[str, str], expect_rule: str | None):
    d = corpus(files)
    try:
        rep = validate(d)
        codes = {e.split("]")[0].lstrip("[") for e in rep.errors}
        if expect_rule is None:
            ok = not rep.errors
            detail = "clean" if ok else f"unexpected: {sorted(codes)}"
        else:
            ok = expect_rule in codes
            detail = "caught" if ok else f"MISSED â€” got {sorted(codes) or 'nothing'}"
        results.append((ok, name, detail))
        print(f"{PASS if ok else FAIL}  {name:44s} {detail}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


SRC = """
sources:
  - id: src-example-2026-08-04
    schema_version: 1
    class: A
    url: https://example.com/x
    title: Example
    retrieved: 2026-08-04
    content_hash: null
    hash_status: unavailable_pending_tooling
    excerpt_fidelity: verbatim
    excerpts: [{id: 0, text: "an excerpt"}]
"""

def ENT(claims: str = "", extra: str = "") -> str:
    return f"""
entities:
  - id: ent-thing-example
    schema_version: 1
    name: Example
    layers: [L1]
    roles: [model_version]
    status: stub
    first_seen: 2026-01-01
    summary: A test entity used only by the validator test suite.
{extra}
{claims}
"""

CLAIM_OK = """    claims:
      - id: clm-example-001
        schema_version: 2
        type: S
        temporal_kind: step
        subject: ent-thing-example
        predicate: pricing.input
        statement: Priced at two dollars per million tokens.
        temporal: {valid_from: 2026-01-01, valid_to: null, asserted_from: 2026-08-04, asserted_to: null, observed_at: 2026-08-04}
        evidence: [{source: src-example-2026-08-04, excerpt_ref: 0, supports: true}]
        cadence_days: 30
        status: published
"""

print("\nCLEAN CORPUS\n" + "-" * 74)
check("clean corpus passes", {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK)}, None)

print("\nEVIDENTIARY RULES\n" + "-" * 74)
check("EVID-1  published claim with no evidence",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK.replace(
          "evidence: [{source: src-example-2026-08-04, excerpt_ref: 0, supports: true}]",
          "evidence: []"))}, "SCHEMA")
check("EVID-2  evidence cites unknown source",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK.replace(
          "src-example-2026-08-04, excerpt_ref", "src-ghost-2026-01-01, excerpt_ref"))}, "EVID-2")
check("EVID-4  comparative claim with one source",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK.replace("type: S", "type: C")
          .replace("predicate:", "objects: [ent-thing-other]\n        predicate:"))}, "EVID-4")

print("\nINTEGRITY RULES\n" + "-" * 74)
check("INTEG-1 authored confidence is forbidden",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK + "        confidence: high\n")}, "INTEG-1")
check("CLAIM-1 forecast published",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK.replace("type: S", "type: F"))}, "SCHEMA")

print("\nSCOPE RULES\n" + "-" * 74)
check("SCOPE-1 non-transferable claim without elicit",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK + "        scope: workload\n")}, "SCHEMA")

print("\nTEMPORAL RULES\n" + "-" * 74)
dup = CLAIM_OK + CLAIM_OK.replace("clm-example-001", "clm-example-002").replace("    claims:\n", "")
check("TEMP-3  two simultaneously-open assertions",
      {"s.yaml": SRC, "e.yaml": ENT(dup)}, "TEMP-3")
check("TEMP-2  incomplete bitemporal interval",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK.replace(
          "asserted_from: 2026-08-04, asserted_to: null, observed_at: 2026-08-04",
          "asserted_to: null"))}, "SCHEMA")

print("\nSOURCE RULES\n" + "-" * 74)
check("SRC-2   source with no excerpts",
      {"s.yaml": SRC.replace('excerpts: [{id: 0, text: "an excerpt"}]', "excerpts: []"),
       "e.yaml": ENT(CLAIM_OK)}, "SCHEMA")
check("SRC-4   null hash without pending status",
      {"s.yaml": SRC.replace("hash_status: unavailable_pending_tooling", "hash_status: hashed"),
       "e.yaml": ENT(CLAIM_OK)}, "SRC-4")

print("\nGRAPH RULES\n" + "-" * 74)
check("GRAPH-1 made_by references unknown entity",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK, "    made_by: ent-institution-ghost")}, "GRAPH-1")
check("GRAPH-5 active entity with zero claims",
      {"s.yaml": SRC, "e.yaml": ENT("", "").replace("status: stub", "status: active")}, "SCHEMA")

print("\nID RULES\n" + "-" * 74)
check("ID-UNIQUE duplicate entity id",
      {"s.yaml": SRC, "e.yaml": ENT(CLAIM_OK) + ENT(CLAIM_OK.replace("001", "003"))
       .replace("entities:", "")}, "ID-UNIQUE")

print("\n" + "=" * 74)
passed = sum(1 for ok, _, _ in results if ok)
print(f"{passed} / {len(results)} rules verified to fire")
if passed < len(results):
    print("\nUNVERIFIED RULES â€” these cannot be trusted:")
    for ok, n, d in results:
        if not ok:
            print(f"  {n}: {d}")
raise SystemExit(0 if passed == len(results) else 1)
