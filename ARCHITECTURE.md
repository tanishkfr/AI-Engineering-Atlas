# SYSTEM ARCHITECTURE

**Status:** v1.0 · **Last reviewed:** 2026-08-03

Five layers. Each depends only on the ones beneath it. The dependency direction
is the whole design — invert it anywhere and the Atlas becomes a website with a
database attached instead of a database with a website attached.

```
  ┌───────────────────────────────────────────────────────────┐
  │  5  UPDATE PIPELINE      keeps 1–4 true over time         │
  ├───────────────────────────────────────────────────────────┤
  │  4  INTERFACE            presents; holds no knowledge      │
  ├───────────────────────────────────────────────────────────┤
  │  3  RECOMMENDATION       persona + graph → ranked answers  │
  ├───────────────────────────────────────────────────────────┤
  │  2  RESEARCH ENGINE      validates, computes, derives      │
  ├───────────────────────────────────────────────────────────┤
  │  1  KNOWLEDGE GRAPH      /data — the source of truth       │
  └───────────────────────────────────────────────────────────┘
```

**The test:** delete layer 4 and the Atlas still exists and is still valuable.
Delete layer 1 and nothing remains. If that ever stops being true, something has
been built in the wrong place.

---

## Layer 1 — Knowledge graph

`/data`. YAML, human-authored, machine-validated (SCHEMA.md). Plain files in git
so that history, review, and contribution work with tools that already exist.

Not a database because the properties that matter here — diffable review,
blame, offline editing, zero-infrastructure contribution — belong to git, and
querying is cheap to add on top. A build step compiles YAML into a queryable
index; the reverse (a database as the authoring surface) would trade away all of
those for query convenience we can get anyway.

```
data/
  schema/          JSON Schema — the enforceable contract
  entities/        by layer: model/ access/ harness/ surface/ interop/
                   context/ orchestration/ assurance/ practice/
  institutions/    M2 — vendors, foundations, registries
  evidence/        M1 — benchmarks, surveys, papers, leaderboards
  sources/         captured, hashed, deduplicated
  claims/          cross-entity claims only (single-entity claims live inline)
  personas/        weight vectors + hard constraints
  experiments/     Class D definitions, configs, raw outputs
  benchmarks/      imported results, harness-tagged
```

---

## Layer 2 — Research engine

Everything between raw records and usable knowledge. Deterministic, testable,
runs in CI.

| Stage | Does |
|---|---|
| **Validate** | JSON Schema + the cross-record rules in SCHEMA.md §11. Fails the build. |
| **Resolve** | Dereference IDs, build the bidirectional edge index, detect cycles and dangling refs. |
| **Compute confidence** | Per SOURCES.md §5, from admissibility, corroboration, convergence, conflict, freshness, flag load. Never authored. |
| **Compute freshness** | `verified + cadence_days` → fresh/aging/stale/expired. |
| **Detect conflict** | Surface contradictions across claims on the same predicate, including ones nobody flagged by hand. |
| **Derive** | Comparison tables, pricing tables, capability matrices, timelines, registers. |
| **Index** | Search index over entities, aliases, claims, narrative. |
| **Report** | Freshness dashboard, gap register, conflict register, coverage report. |

Two of these deserve emphasis because they invert the usual relationship between
a knowledge base and its own weaknesses:

- **Conflict detection is automated and adversarial.** It looks for
  contradictions we did not notice. Finding one is a success, not a defect.
- **The gap register is generated, not written.** Every `unknown` claim and
  every `not_scored` dimension becomes a published, queryable gap. The system
  reports on its own ignorance without anyone remembering to.

---

## Layer 3 — Recommendation engine

A **constraint solver**, not a ranker. Turns `(question, persona, date)` into an
explained, traceable answer — or an informative refusal. What a conclusion
owes its reader is specified in [DEPENDENCE.md](DEPENDENCE.md) §7.

```
persona ──> HARD CONSTRAINTS ──> eliminate candidates
                                        │
                                        ▼
                              COMPOSE STACKS + compatibility
                                        │
                                        ▼
                              COST (usage × temporal pricing)
                                        │
                                        ▼
                              UNCERTAINTY → belief distributions
                                        │
                                        ▼
                              DOMINANCE → Pareto set    ← no weights yet
                                        │
                                        ▼
                              DECIDE (criterion from risk posture)
                                        │
                                        ▼
                              POSITION + BUDGET FRONTIER
                                        │
                                        ▼
                              EXPLAIN (six mandatory components + VOI)
```

Non-negotiable properties:

1. **Every recommendation is reversible to evidence** — one path from ranking →
   dimension scores → claims → sources → excerpts. If the chain breaks, the
   recommendation does not render.
2. **Weights are always visible.** A ranking without its weighting is a
   leaderboard, and we don't publish those.
3. **Coverage travels with the answer.** "Ranked on 8 of 13 dimensions" is part
   of the answer, not a footnote.
4. **It can decline.** When evidence is insufficient to separate candidates, the
   correct output is "these are not distinguishable on the evidence we have,
   here is what would distinguish them." That output is a feature.
5. **It is deterministic.** No model in the loop at serve time. The reasoning is
   the rubric and the graph, both inspectable. An LLM-generated recommendation
   would be unauditable, and auditability is the entire proposition.
6. **Dominance precedes opinion.** What is *defensible* is computed without
   weights; weights only order what already survived. The output keeps the two
   separable.
7. **It explains itself or it does not render.** Six mandatory machine-generated
   components, including what it assumed and what would change its mind.

---

## Layer 4 — Interface

A projection. Detailed in [INFORMATION-ARCHITECTURE.md](INFORMATION-ARCHITECTURE.md).

Rules that bind it to the layers below:

- No fact originates here. Prose interpolates from the graph or the build fails.
- Evidence level, confidence, and freshness are rendered **at the point of
  use**, not in a footer. A stale number must look stale where it is read.
- Fact / interpretation / opinion have distinct visual treatments
  (CONSTITUTION §3).
- Every number is clickable to its source.
- The site builds statically. It must remain readable and correct with
  JavaScript disabled — the content is text and tables, and treating that as a
  progressive enhancement question keeps it fast and archivable.

Stack is **deliberately undecided** until Milestone 4. Committing to a framework
before the data model is exercised is how presentation concerns leak into
schemas. Constraints already fixed: static generation, MDX with structured data
interpolation, client-side search over a prebuilt index, no runtime dependency
on any external service.

---

## Layer 5 — Update pipeline

The layer that decides whether this is an atlas or an archive.

**Nightly** — recompute freshness; enqueue due claims; re-fetch tracked source
URLs and diff `content_hash`; flag dependent claims `needs_review`; publish the
freshness report.

**Weekly** — sweep release feeds and changelogs of tracked institutions; mint
stubs for new entities; refresh benchmark leaderboards; recompute confidence.

**Monthly** — the full cycle in METHODOLOGY.md §6, ending in a dated public
changelog of what changed, what it invalidated, and what we got wrong.

**Event-driven** — model release, pricing change, deprecation notice, benchmark
update, or a spike in contradicting field reports pulls re-verification forward.

Automation boundary, stated plainly: **the pipeline detects and enqueues; it
never publishes a claim.** Fetching, hashing, diffing, and flagging are
mechanical. Deciding what a change means is research, and research is reviewed
before it ships.

---

## Future ingestion

Designed for, not built yet. Each is an importer that writes normal source and
claim records — no privileged path into the graph, no exemption from validation.

- **Benchmark imports** — leaderboard APIs → `benchmark_result` records, always
  harness-tagged and operator-tagged.
- **Pricing feeds** — provider pricing endpoints → S-claims with automatic
  supersession of the prior claim and a history entry.
- **Release feeds** — GitHub releases, changelogs → entity stubs.
- **Community signal** — sampled per METHODOLOGY.md §4 with the query and window
  recorded, never scraped indiscriminately.
- **Public read API** — the graph served as JSON so others can check our work,
  build on it, or contradict it. An atlas that cannot be independently audited is
  asking for the trust it claims to have earned.

---

## Repository layout

```
AI-Engineering-Atlas/
  CONSTITUTION.md          non-negotiable principles
  METHODOLOGY.md           how research is done
  SOURCES.md               source quality + claim-type authority matrix
  EVALUATION.md            scoring rubric
  TAXONOMY.md              ecosystem structure
  GRAPH.md                 relationship ontology
  TEMPORAL.md              bitemporal fact model
  SCHEMA.md                data model
  DEPENDENCE.md            the thesis: support, load, withdrawal
  QUERIES.md               query proofs / acceptance tests
  ARCHITECTURE.md          this file
  INFORMATION-ARCHITECTURE.md   site structure
  RESEARCH.md              inventory, gaps, open questions
  CLAUDE.md                how agents work in this repo
  STUDIO.md                visual system — deferred to Milestone 4

  data/                    layer 1
  scripts/                 layer 2 + 5
  atlas/                   MDX narrative — layer 4 content
  research/                scan notes, working documents, raw findings
```

`research/` is a working directory, not a publication surface. Nothing in it is
citable until it becomes a source or claim record — otherwise our own notes
become a self-citation loop, which CONSTITUTION §2 forbids.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial architecture. |
