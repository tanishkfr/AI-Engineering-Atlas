# DATA SCHEMA

**Status:** v2.0 · **Last reviewed:** 2026-08-03 · **Machine definitions:**
`data/schema/*.schema.json`

The knowledge graph. `/data` is the source of truth; everything else — pages,
tables, charts, recommendations — is a projection of it.

> **v2 changes.** Facts became immutable and bitemporal
> ([TEMPORAL.md](TEMPORAL.md)); the v1 `history[]` array is retired. Relationships
> were formalized into a typed ontology ([GRAPH.md](GRAPH.md)). Three object
> types were added — `capability`, `usage_profile`, `objective` — each forced by
> a query the model could not otherwise answer ([QUERIES.md](QUERIES.md) §8).

---

## 1. Design commitments

1. **A fact exists once.** If a number appears in two files, one of them is
   wrong by construction.
2. **Nothing is asserted without evidence.** Claims carry sources; sources carry
   excerpts; excerpts carry hashes.
3. **Everything is dated.** Every fact knows when it was verified and when it
   goes stale.
4. **IDs are permanent and meaningless.** Names change; IDs do not.
5. **Confidence is computed, never authored.**
6. **Additive evolution.** New fields may be added; existing fields are never
   repurposed. A repurposed field silently corrupts every historical record.
7. **Human-writable, machine-validated.** YAML for authoring, JSON Schema for
   enforcement, in CI.

---

## 2. Object model

Seven object types. Everything in the Atlas is one of these.

```
   SOURCE ──────────< EVIDENCE >────────── CLAIM
                                             │
                                             │ describes
                                             ▼
   PERSONA >───── SCORE ──────────────────ENTITY
                                             │
                                             │ relationships
                                             ▼
                                          ENTITY

   EXPERIMENT ──produces──> SOURCE (class D)
```

| Object | Is | Lives in |
|---|---|---|
| `entity` | A thing in the ecosystem (TAXONOMY.md) | `data/entities/<layer>/` |
| `claim` | One immutable, bitemporal, sourced fact | inside its entity; cross-entity claims in `data/claims/` |
| `source` | A citable artifact, captured | `data/sources/` |
| `evidence` | The link between a claim and a source, with the supporting excerpt | inside the claim |
| `score` | One rubric dimension applied to one entity | inside its entity |
| `relationship` | A typed, evidenced, temporal edge (GRAPH.md) | on the subject entity |
| `persona` | A weight vector + hard constraints | `data/personas/` |
| `capability` | A normalized, entity-independent feature | `data/capabilities/` |
| `usage_profile` | Monthly consumption for a working pattern | `data/usage/` |
| `objective` | What a reader optimizes for + its admissible metrics | `data/objectives/` |

Supporting records: `experiment` (`data/experiments/`), `benchmark_result`
(`data/benchmarks/`), `metric` (`data/metrics/`).

The three v2 additions each exist because a query broke without them:

- **`capability`** — constraints must be expressible against features rather than
  entity types, or every new category requires engine changes (GRAPH.md §3).
- **`usage_profile`** — no cost question is answerable without a usage model, and
  inventing one is fabrication (QUERIES.md §8.1).
- **`objective`** — without declared metric sets, the engine will answer a
  frontend question with a repository-patching benchmark (QUERIES.md §8.2).

---

## 3. Identifiers

```
ent-<layer>-<slug>        ent-harness-example-cli
clm-<entity-slug>-<n>     clm-example-cli-014
src-<publisher>-<slug>-<yyyy-mm-dd>
rel-<subject>-<predicate>-<object>
scr-<entity-slug>-<dimension>
per-<slug>                per-solo-founder
exp-<slug>-v<n>           exp-greenfield-app-v2
bmk-<slug>                bmk-swe-bench-verified
```

Rules:

- Minted once. **Never** changed, even on rename, acquisition, or rebrand.
- Slugs derive from the name *at creation time* and are then frozen. A stale
  slug is correct; a renamed ID is a broken link in every direction.
- Deleted entities are not deleted — status becomes `retired`, with
  `replaced_by` where applicable.

---

## 4. Entity

```yaml
id: ent-harness-example-cli
schema_version: 1
name: Example CLI
aliases: [Formerly Known As, community-nickname]
slug_frozen_at: 2026-08-03

layers: [L3]                    # multi-layer is normal
roles: [cli_agent]
facets:
  execution: local
  model_agnostic: true
  sandboxing: container
  headless: true

made_by: ent-institution-example-co
status: active                  # stub | researching | active | deprecated | retired
depth_priority: P1              # P0..P3 — drives review cadence
first_seen: 2026-08-03
canonical_url: https://…
repo_url: https://…

summary: >                      # ≤ 2 sentences. Placement, not evaluation.
  …

decision_questions:             # the questions this entity exists to answer
  - q: Should I use Example CLI instead of its bundled alternative?
    page: atlas/harness/example-cli-vs-alternative.mdx

claims: [ … ]                   # §5
scores: [ … ]                   # §7
relationships: [ … ]            # §8

review:
  cadence_days: 60
  last_reviewed: 2026-08-03
  next_due: 2026-10-02

revisions:
  - date: 2026-08-03
    change: Created as stub from landscape scan.
    by: scan-2026-08-03
```

`summary` is deliberately constrained to placement. Evaluation lives in scores
and claims, where it can be sourced. A free-text summary is where unsourced
opinion leaks into a graph, so the field is too small to hold any.

---

## 5. Claim

The atomic unit (METHODOLOGY.md §1). **Immutable and bitemporal** — full model in
[TEMPORAL.md](TEMPORAL.md).

```yaml
- id: clm-example-cli-014
  type: S                        # S | M | X | C | T | F  (SOURCES.md §2)
  temporal_kind: step            # static|point|step|measurement|series|interval
  subject: ent-harness-example-cli
  predicate: pricing.input_per_mtok
  statement: >
    Priced at $X per million input tokens on the first-party API.
  value: {amount: 0.00, currency: USD, unit: per_mtok}

  temporal:
    valid_from: 2026-07-14       # when it became true in the world
    valid_to: null               # open interval
    valid_precision: day
    asserted_from: 2026-08-03    # when the Atlas began believing it
    asserted_to: null
    observed_at: 2026-08-03

  supersedes: clm-example-cli-009
  supersession_kind: change      # change | correction | refinement | retraction

  qualifiers: {tier: standard, region: global, via: null}

  evidence:
    - {source: src-example-pricing-2026-08-03, excerpt_ref: 0, supports: true}
    - {source: src-thirdparty-teardown-2026-07-11, excerpt_ref: 2, supports: true}

  conflicts:
    - positions:
        - {value: 0.00, sources: [src-a]}
        - {value: 0.00, sources: [src-b]}
      likely_cause: version_drift

  confidence: high               # COMPUTED — authored values fail validation
  freshness: fresh               # COMPUTED, kind-aware
  cadence_days: 30
  status: published
```

Notes:

- **Claims are never edited.** A change or a correction appends a new record and
  closes the prior assertion. `supersession_kind` is what distinguishes *the
  world changed* from *we were wrong* — the v1 `history[]` array could not, and
  that made corrections invisible (CONSTITUTION §11).
- `temporal_kind` governs carry-forward. `measurement` and `series` facts are
  **never** carried forward: there is no "current benchmark score", only a score
  measured on a date under stated conditions.
- `conditions` (harness, version, operator, runs, variance) is **mandatory** for
  `measurement` and `series` kinds.
- `predicate` comes from `data/schema/predicates.yaml`, which also declares each
  predicate's temporal kind.
- `confidence` and `freshness` are written by the build. A hand-set value is a
  validation error, not a warning.
- **`unknown` is a legal value** with `status: published`.
- `qualifiers.via` is **required** for M-type and X-type claims about models —
  the model/harness confounding rule from EVALUATION.md §3.

---

## 6. Source

Full definition in SOURCES.md §8. Sources are shared and deduplicated: one
source record, referenced by many claims. Excerpts are indexed so a claim points
at the exact passage it rests on.

```yaml
id: src-example-pricing-2026-08-03
class: A
url: …
archive_url: …
publisher: ent-institution-example-co
published: 2026-07-14
retrieved: 2026-08-03
content_hash: sha256:…
excerpts:
  - id: 0
    text: "…verbatim…"
    locator: "Pricing table, standard tier"
flags: [self_interested]
methodology: null                # required for class B and D
```

A `content_hash` change on re-verification flags every dependent claim
`needs_review` automatically.

---

## 7. Score

One rubric dimension, one entity (EVALUATION.md).

```yaml
- id: scr-example-cli-d2
  dimension: D2
  value: 4                       # 1–5 | null
  not_scored_reason: null        # required when value is null
  rationale: >                   # one sentence, mandatory
    …
  via:                           # conditions the score depends on
    model: ent-model-endpoint-…
    version: …
  evidence: [clm-…, clm-…]
  confidence: moderate           # COMPUTED, floor of inputs
  as_of: 2026-08-03
  scored_by: …
  second_pass:
    value: 4
    divergence: 0
  history: [ … ]
```

`rationale` is mandatory and `evidence` must be non-empty. A score without both
is an opinion in a numeric costume, and the validator rejects it.

---

## 8. Relationship

Full ontology — domains, ranges, inverses, inference rules — in
[GRAPH.md](GRAPH.md). Edges are facts and carry the same temporal and evidential
discipline as claims.

```yaml
- id: rel-example-cli-works-with-example-model
  predicate: works_with
  object: ent-model-version-…
  temporal_kind: step
  temporal: {valid_from: 2026-05-01, valid_to: null,
             asserted_from: 2026-08-03, asserted_to: null,
             observed_at: 2026-08-03}
  co_use_evidence: field_reports    # required for works_with
  evidence: [clm-…]
  confidence: high                  # COMPUTED
```

Edges are stored on the subject and indexed bidirectionally at build time.
Vocabulary is closed; unknown predicates fail validation.

Three rules that carry disproportionate weight:

- **Compatibility is three-valued.** No edge means `unverified`, never
  compatible. Stacks built from unverified pairs are labeled untested.
- **`works_with` requires evidence of observed co-use.** Shared protocol support
  is never sufficient — that inference would be the most damaging one this graph
  could make.
- **`recommended_for` is engine output**, materialized with `derived: true`.
  A hand-authored recommendation edge is an unscoped opinion.

---

## 9. Persona

```yaml
id: per-solo-founder
name: Solo founder shipping a product
schema_version: 1

context:
  budget_month_usd: {min: 0, typical: 100, max: 300}
  team_size: 1
  codebase: {age: greenfield, size: small, languages: [ts, python]}
  task_mix: {feature_work: 0.5, frontend: 0.25, debugging: 0.15, ops: 0.10}
  risk_tolerance: high
  compliance: none

hard_constraints:                # eliminations, never penalties
  - {facet: billing_model, not: enterprise_only}

weights:                         # EVALUATION.md dimensions
  D1: 0.8
  D2: 1.0
  # …
weights_rationale: >
  …
weights_status: opinion          # per CONSTITUTION §3
weights_author: …
weights_dated: 2026-08-03
```

Weights are labeled `opinion` in the data itself, so the interface cannot render
them as findings even by accident.

---

## 10. Derived artifacts

Generated at build, never authored. This list *is* the argument for the schema —
each item is something that would otherwise be hand-maintained and silently rot.

| Artifact | Built from |
|---|---|
| Comparison tables | entities + claims filtered by predicate |
| Pricing tables | S-claims on `model_endpoint` + `subscription_plan` |
| Capability matrices | facets + claims |
| Timelines | `first_seen`, release claims, lifecycle edges |
| Stack Builder | persona constraints → filter → weight → rank |
| Search index | entities + aliases + claims + narrative |
| Freshness dashboard | `observed_at` + `cadence_days` + `temporal_kind` |
| Conflict register | every `conflicts` block in the graph |
| Gap register | `unknown` claims + `not_scored` dimensions + engine refusals |
| Corrections register | claims with `supersession_kind: correction` / `retraction` |
| Monthly changelog | claims whose `asserted_from` falls in the window |
| Price history | `step` claims on a pricing predicate, ordered by `valid_from` |
| Historical replay | the engine run against `graph_at(past_date)` |

Three of these are unusual enough to be the point. The **conflict** and **gap**
registers are normally invisible byproducts of research; here they are queryable
pages. The **corrections register** is only possible because supersession
distinguishes a change from an error — and publishing your own error rate is the
strongest available evidence that a methodology is real.

**Historical replay** deserves separate mention: because the graph is bitemporal,
past recommendations can be re-run against past evidence and checked against what
actually happened. The Atlas can audit itself.

---

## 11. Validation

CI-enforced. All are errors, not warnings.

**Structural** — schema conformance · unique IDs · no dangling references ·
closed vocabularies for `predicate`, `role`, `layer`, `flags`, `likely_cause`.

**Evidentiary** — every published claim has admissible evidence for its claim
type · no Class-E-only claims · comparative claims have ≥2 independent sources ·
every source has `retrieved` + `content_hash` + ≥1 excerpt · every Class B/D
source has methodology.

**Integrity** — no authored `confidence` or `freshness` · every score has
`rationale` + `evidence` · M/X model claims have `qualifiers.via` · no expired
claim rendered as current · no orphan numbers in MDX prose.

**Temporal** — every claim has a complete bitemporal interval · no claim record
is ever modified after assertion · `correction` and `retraction` carry a reason ·
`measurement` and `series` claims have `conditions` · no `measurement` value
carried forward · no two open assertions on the same subject+predicate ·
no fact asserted valid over an interval where its subject did not exist ·
comparison tables computed at a single reference date.

**Graph** — domain/range conformance per predicate · no self-edges · no
contradictory edge pairs · `depends_on` and `replaces` chains acyclic ·
`works_with` has `co_use_evidence` · `incompatible_with` has a `failure_mode` ·
`migration_target_of` has sampling metadata · derived edges carry a rule and are
never hand-authored · every `model_endpoint` has exactly one `endpoint_of` and
≥1 `hosted_by` · no entity with zero claims in `active` status.

**Engine** — no entity, vendor, or product name appears in engine code
(grep-checked) · no ratio computed from an ordinal score · no cost figure without
a usage profile and pricing date · every recommendation reversible to sources.

---

## 12. Evolution

- `schema_version` on every record; migrations are scripts in `scripts/migrations/`,
  never manual edits.
- Fields are added, never repurposed.
- Deprecated fields are marked and read-only for one release cycle before
  removal.
- Every schema change ships with a migration and a validation run against the
  full corpus before merge.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-08-03 | Immutable bitemporal claims (TEMPORAL.md); `history[]` retired. Typed relationship ontology (GRAPH.md). Added `capability`, `usage_profile`, `objective`. Temporal, graph, and engine validation rules. |
| 1.0 | 2026-08-03 | Initial schema. Seven object types; claims co-located with entities; sources deduplicated. |
