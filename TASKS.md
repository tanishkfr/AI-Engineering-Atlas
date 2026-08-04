# TASKS

**Current milestone:** M3 — Evidence base
**Last updated:** 2026-08-03

Task IDs are stable. Definition of Done is not optional — a task without a met
DoD is not done, regardless of how much work went into it.

Status: `todo` · `doing` · `blocked` · `done`

**Research order is set by [QUERIES.md](QUERIES.md) §9, not by intuition.**
The queries readers actually ask determine what gets researched first, which is
why usage profiles and pricing outrank comprehensive tool coverage.

---

## M2 — Formalization ✅ done

| ID | Task | Status |
|---|---|---|
| T-100 | GRAPH.md — typed relationship ontology | done |
| T-101 | TEMPORAL.md — bitemporal fact model | done |
| T-102 | RECOMMENDATION.md — engine specification | done |
| T-103 | QUERIES.md — six query proofs | done |
| T-104 | Schema v2: temporal claims, relationships, capability, usage_profile, objective, query | done |
| T-105 | Reconcile SCHEMA/ROADMAP/TASKS | done |

---

## M2.5 — Decision layer ✅ done

| ID | Task | Status |
|---|---|---|
| T-110 | DECISION.md — decision-science framework | done |
| T-111 | RECOMMENDATION v2 — solver reformulation, 13 stages | done |
| T-112 | `recommendation.schema.json` — mandatory six-part explanation | done |
| T-113 | Belief distributions on scores; `marginal_value` + `decision_criterion` on queries | done |
| T-114 | QUERIES Q7 — marginal spend proof | done |

---

## M3.1 — Research program ✅ done

| ID | Task | Status |
|---|---|---|
| T-120 | `research/questions/` program with ERI scoring method | done |
| T-121 | Six flagship track write-ups (RQ-01–06) | done |
| T-122 | Supporting questions (RQ-07, 08, 09, 10) | done |
| T-123 | Decline list with recorded reasons | done |

### Research program execution — in ERI order

| ID | Task | Status | DoD |
|---|---|---|---|
| T-130 | **RQ-01** `exp-tokenizer-normalization-v1` ⚡ | todo | Fixed corpus published; token counts per vendor tokenizer per stratum; `met-effective-token-multiplier` populated; models without a public tokenizer marked `not_normalizable` and excluded rather than estimated |
| T-131 | **RQ-07** Sonnet 5 tokenizer identity ⚡ | todo | `clm-claude-sonnet-5-090` moves from `unknown` to a sourced value, or the conflict is confirmed unresolvable |
| T-132 | **RQ-08** Subscription capture + crossover ⚡ | todo | Subscription plans as temporal step facts; crossover surface over hit rate × model tier; dominated ranges identified |
| T-133 | **RQ-03** Cache economics instrumentation | todo | Per-request token accounting across ≥3 harnesses; realized hit rates; counterfactual no-cache cost |
| T-134 | **RQ-06** Cost decomposition | todo | Overhead share of total spend per stack; effective price multiplier vs headline |
| T-135 | **RQ-02** Throughput consumption | todo | Rolling p95 consumption vs published limits; headroom ratio per stack; throttle-behaviour findings |
| T-136 | **RQ-04** Intervention rate | todo | Taxonomy preregistered; inter-rater agreement above threshold **before** any result publishes |
| T-137 | **RQ-05** Harness effect size | todo | Factorial ≥3 models × ≥3 harnesses incl. a minimal baseline; variance decomposition published with the interaction term |
| T-138 | **RQ-09** Cost model v2 storage term | todo | Additive term with zero default; no vendor branch (invariant 16.1 holds); Google pricing re-captured verbatim first |
| T-139 | **RQ-10** Frontend instrument Stage 1 | todo | Rubric with acceptable inter-rater agreement, **or** a published negative result that visual quality is not reliably measurable by our method |

---

## M3.A — Tooling

The framework is currently enforced by good intentions. These tasks make it
enforced by CI.

| ID | Task | Status | DoD |
|---|---|---|---|
| T-001 | Validation runner over `data/schema/*.schema.json` | todo | `npm run validate` fails on a deliberately broken fixture for each rule in SCHEMA §11 |
| T-002 | Source capture tool: fetch → hash → archive → excerpt | todo | Produces a schema-valid source record from a URL, including archive link and content hash |
| T-003 | Confidence computation | todo | Implements SOURCES §5; authored `confidence` fields are rejected; unit-tested against hand-worked cases |
| T-004 | Kind-aware freshness computation | todo | Implements TEMPORAL §6; `measurement`/`series` never marked current at any age; `point`/`static` never stale |
| T-005 | Cross-record rule checks | todo | Claim-type admissibility, Class-E-only rejection, comparative ≥2 sources, `via` on M/X model claims |
| T-006 | Report generators: gap, conflict, freshness, coverage, **corrections** | todo | Each generated from the graph with zero hand-maintained content |
| T-007 | Predicate vocabulary `data/schema/predicates.yaml` | todo | Every predicate declares claim type, temporal kind, domain, range; unknown predicates fail validation |
| T-008 | Per-role facet schemas `data/schema/facets/<role>.schema.json` | todo | Every role used by a P0 entity has a facet schema |
| T-009 | Source re-verification job: diff hash → flag dependents | todo | A changed hash marks every dependent claim `needs_review` |
| T-010 | **Bitemporal store operations** | todo | Append, supersede, close-assertion, and `graph_at(date)` implemented; claim records provably never mutated after assertion |
| T-011 | **Graph integrity checks** | todo | Domain/range conformance, acyclicity, `works_with` co-use evidence, derived-edge provenance — all enforced per SCHEMA §11 Graph |
| T-012 | **Inference rules R1–R5** | todo | Derived edges materialized with `derived: true` and rule id; R4 emits candidates only; protocol support never yields `works_with` |

---

## M3.B — Materialize the scan

| ID | Task | Status | DoD |
|---|---|---|---|
| T-020 | Convert scan entities to stubs in `data/entities/` | todo | Every entity from `research/scan-2026-08-03.md` has a stub with stable ID, aliases, layers, roles, `first_seen`, provenance |
| T-021 | Institution records for every vendor/foundation/registry named | todo | Every `made_by` reference resolves |
| T-022 | Assign `depth_priority` across the corpus | todo | ~25 P0 entities, spread across all nine layers, each with a written justification |
| T-023 | Benchmark entities with **declared constructs** | todo | Every benchmark we intend to cite declares: its construct, what it is misread as measuring, harness dependency, contamination and saturation state. Construct is machine-matched against objectives (QUERIES §8.2) |
| T-024 | **Capability catalogue** | todo | Every capability referenced by a persona constraint exists, with a definition precise enough that two researchers classify entities identically |
| T-025 | **Objective definitions with metric sets** | todo | At minimum: repository patching, long-horizon autonomy, frontend generation, large-repo comprehension. Each with metric set, floors, directions, coverage floor, implied guards |

---

## M3.C — Primary research

**Ordered by the query set** (QUERIES §9). The first two gate every cost
question, which is most of what readers ask.

| ID | Task | Status | DoD |
|---|---|---|---|
| T-030 | **Usage profiles per persona** | todo | One profile per persona with written assumptions. `status: assumed` until M4 experiments; every cost figure derived from them displays the profile and its confidence |
| T-031 | **Pricing as temporal step facts** | todo | For every P0 access entity: metered rates, cache terms, allowances, overage, rate limits — each with `valid_from` and `observed_at`, sourced to first-party pages |
| T-032 | **Subscription-vs-metered crossover** | todo | Computed per persona; crossover usage point reported, not just two totals (RECOMMENDATION §6) |
| T-040 | Retrieve and capture primary sources for P0 entities | todo | Every P0 entity has ≥1 Class A source captured with hash, archive, and excerpts |
| T-041 | **Q2 — why benchmark scores disagree** | todo | Every divergent figure from scan F4 traced to its harness, variant, operator, and date; conflict object written with `likely_cause`; decision page published |
| T-042 | Negative-case corpus | todo | METHODOLOGY §3 negative searches run for every P0 entity; findings captured as X-type claims or recorded as null results |
| T-043 | **Compatibility edges across P0 entities** | todo | `works_with` only where co-use evidence exists; `incompatible_with` only with a stated failure mode; everything else left `unverified` and visibly so |
| T-044 | Community sentiment pass on P0 entities | todo | METHODOLOGY §4 protocol followed; query, window, and population recorded in every Class C source record |
| T-045 | **Q1 — does this actually help?** evidence gathering | todo | Class B studies retrieved; survey methodologies compared; conflict object written. Published only if the evidence supports a page — `contested` is an acceptable outcome |
| T-046 | Security posture research (D13 inputs) | todo | Sandboxing, permission, and extension supply-chain evidence for every P0 harness |

---

## M3.D — Scoring and writing

| ID | Task | Status | DoD |
|---|---|---|---|
| T-060 | Score P0 entities on applicable dimensions | todo | Every score has rationale, evidence, `via`, `as_of`, second pass; divergences ≥2 logged and resolved |
| T-061 | Remaining 8 persona records | todo | Each schema-valid with weights rationale; divergence rule checked once the engine exists |
| T-062 | 8–10 decision pages | todo | Every page has all eight required sections including WHEN THIS IS WRONG and WHAT WE DON'T KNOW; passes all 15 review gates (METHODOLOGY §8) |
| T-063 | P0 entity pages | todo | Header generated from graph; no orphan numbers in prose |
| T-064 | Evidence pages for cited benchmarks | todo | One per benchmark, per IA §2.6 |

---

## M3.E — Measurement of ourselves

| ID | Task | Status | DoD |
|---|---|---|---|
| T-080 | Measure per-entity research and maintenance cost | todo | Hours per entity recorded for research, scoring, and one re-verification cycle |
| T-081 | Set the coverage ceiling from T-080 | todo | Maximum sustainable entity count computed and written into ROADMAP; corpus scope adjusted to fit |
| T-082 | Check score-scale discrimination | todo | Distribution of scores across P0 entities reviewed; anchors re-cut if most cluster on one value |
| T-083 | **Re-run the seven query proofs against real data** | todo | Each of QUERIES.md Q1–Q7 executes and returns either an answer or a refusal whose reason code matches the predicted verdict. Divergence from the predicted verdict is a schema finding and is logged |
| T-084 | **Publish the first VOI ranking** | todo | Computed from the seed question index; drives the next research cycle. Items marked `negligible` are formally dropped from the backlog, not silently carried |
| T-085 | **Belief-distribution heuristics v1** | todo | Published, versioned mapping from evidence strength and age to distribution shape; sensitivity of outputs to the heuristic itself is measured and reported (DECISION §12) |

---

## Backlog — M4+

Class D experiment harness · **frontend fidelity experiment** (unblocks Q2 and
Q5; highest priority because it is unanswerable from public evidence) ·
long-horizon autonomy experiment for intervention rates (unblocks Q3) ·
greenfield-app experiment · longitudinal maintainability study design (start
early, it takes the longest) · **recommendation engine implementation with all
ten invariants under test** · persona divergence validation · canary suite for
silent endpoint changes · STUDIO.md · interface build · monthly pipeline ·
public read API · contribution process.

---

## Blocked / deferred

| Item | Reason |
|---|---|
| Website implementation | Gated on M2 and M3 (ROADMAP sequencing principle 1) |
| STUDIO.md | Deferred to M4 — the visual system must serve the data model, not precede it |
| Framework choice for the site | Deliberately undecided (ARCHITECTURE layer 4) |
| Persona composition | Deferred until real usage shows the fixed set is too coarse |
