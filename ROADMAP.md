# ROADMAP

**Status:** v1.0 · **Last reviewed:** 2026-08-03

Milestones are gated: each has an exit condition, and work does not advance
until it is met. The gates exist because the tempting failure — build the
website, fill it later — produces something that looks finished and decays
immediately.

---

## M1 — Foundations ✅ *complete 2026-08-03*

Design the research system before doing any research.

**Shipped:** CONSTITUTION · SOURCES (source-class × claim-type authority matrix)
· METHODOLOGY · EVALUATION (13 dimensions, no stored composites) · TAXONOMY
(faceted, 9 layers + 2 meta-classes, scan-validated) · SCHEMA + JSON Schemas ·
ARCHITECTURE · INFORMATION-ARCHITECTURE · PERSONAS + worked example · RESEARCH ·
landscape scan (~120 entities, 4 structural fixes).

**Exit condition met:** taxonomy stress-tested against the real ecosystem and
revised; schema expresses every relationship the scan surfaced; every framework
document names its own weaknesses.

**Deliberately zero published claims.** See RESEARCH.md §1.

---

## M2 — Formalization ✅ *complete 2026-08-03*

Formalize the knowledge graph and the recommendation engine before populating
anything. Inserted ahead of the evidence base after M1, on the reasoning that a
schema proven against real questions is cheaper to fill than one proven against
intuition.

**Shipped:** GRAPH (typed ontology — domains, ranges, inverses, three-valued
compatibility, capability entities, six inference rules) · TEMPORAL (immutable
bitemporal facts, six temporal kinds, supersession semantics) · RECOMMENDATION
(nine-stage engine spec, cost model, frontier computation, refusal codes,
ten invariants) · QUERIES (six queries traced end to end) · schema v2 (11 JSON
Schemas, three new object types).

**Exit condition met:** all six named queries traced without requiring a
redesign. Four additive extensions were surfaced *by the queries* and applied —
usage profiles, objective metric-sets with construct gating, preferences as
distinct from constraints, and implied guards on single-dimension maximization.

**The extensibility invariant:** no entity, vendor, or product name appears in
engine code. It operates on slots, capabilities, constraints, dimensions,
metrics, and costs — which is what makes "absorbs new categories without
redesign" a checkable property rather than a hope.

---

## M2.5 — Decision layer ✅ *complete 2026-08-03*

Population paused a second time. The M2 engine was filter → weighted sum → band —
a ranker with good manners, which threw away the uncertainty the schema had just
been built to carry.

**Shipped:** DECISION.md (uncertainty as belief distributions; dominance before
weighting; probability-of-best; minimax regret; opportunity cost and budget-
frontier knees; option value and switching cost; sensitivity analysis; value of
information; portfolio allocation) · RECOMMENDATION v2 (reformulated as
constrained combinatorial optimization, 13 stages, 12 invariants) ·
`recommendation.schema.json` with the mandatory six-part explanation object ·
belief distributions on scores · QUERIES Q7.

**Exit condition met:** Q7 — *"how do I spend my next $25 most effectively?"* —
traced end to end. The v1.0 engine could not express marginal value, opportunity
cost, or dominated spending at all; v2 answers with **"spend $20 and hold the
$5, your $21–$44 range is dominated"** rather than a product name.

**What changed structurally:**
- Weights no longer touch anything until after dominance pruning, so *defensible*
  and *recommended* are separable in the output.
- `risk_tolerance` now selects the decision criterion, so an enterprise team and
  a solo founder get different answers from identical evidence for a stated
  reason.
- The engine computes what to research next (VOI) — and licenses skipping what
  changes no recommendation, which matters under CONSTITUTION §14.

---

## M3 — Evidence base

Turn the machine on. The first real test of whether the framework survives
contact with primary sources.

**Build**
- Source capture tooling: fetch, hash, archive, excerpt
- Validation runner over `data/schema/` in CI
- Confidence and freshness computation
- Gap, conflict, and freshness reports

**Research — ordered by the query set, not by intuition** (QUERIES §9)
- **Usage profiles** — gates every cost question. Nothing about money works
  without them, and they cannot be invented.
- **Pricing as temporal step facts** — with cache terms and allowances
- ~25 P0 entities to `active`, spread across all nine layers — not 25 models
- Primary sources retrieved and captured for every published claim
- Negative-case corpus (METHODOLOGY §3): failures, limitations, migrations away
- Answer Q2 — why benchmark scores for the same model disagree

Note what this order does *not* prioritize: comprehensive per-tool feature
coverage. The questions readers actually ask do not require it, and researching
breadth first would have been the obvious move and the wrong one.

**Write**
- 8–10 decision pages, starting with Q2 and Q1
- Every P0 entity page
- Evidence pages for the benchmarks we cite

**Exit:** every published claim traces to a captured primary source; validation
passes; the gap and conflict registers are generated, not hand-written; the
per-entity maintenance cost is measured and recorded.

**Risk:** the schema will be wrong somewhere. Expect one migration. Better to
find it at 25 entities than 250.

---

## M3.1 — Research program ✅ *complete 2026-08-03*

Broad population paused after ten entities, because the first evidence pass
generated original research questions faster than it generated facts — the signal
that the project had crossed from aggregation into research.

**Shipped:** [`research/questions/`](research/questions/README.md) — a ranked
portfolio of ten research questions, each with the eight-section standard, plus
an Expected Recommendation Impact scoring method that operationalizes the
value-of-information concept from DECISION §8.

**Six flagship tracks** designated: tokenizer normalization · throughput-
constrained autonomy · cache economics · intervention rate · harness effect size ·
real-world feature cost. Each produces a longitudinal dataset that compounds
rather than a one-off result.

**Three questions carry JUMP QUEUE** (high impact, low effort, no public answer).
RQ-01 tokenizer normalization is the standout: deterministic, needs no model
access, and gates every cross-vendor cost claim the Atlas will ever make.

**Three questions declined** with reasons recorded. A program that only ever adds
work eventually lies about its coverage (CONSTITUTION §14).

**Exit condition met:** every M3 finding is either an RQ with an ERI estimate and
a proposed protocol, or explicitly declined.

---

## M4 — Experiments and engine implementation

**Experiments — order now set by the research program's ERI ranking**, not by the
earlier guess. Run in this sequence:

1. **RQ-01 tokenizer normalization** — decisive, low effort, no model access
   required. Gates every cross-vendor cost claim.
2. **RQ-07 Sonnet 5 tokenizer identity** — trivial; a pilot for RQ-01's method.
3. **RQ-08 subscription crossover** — low effort; unblocks the single most-asked
   question in the project.
4. **RQ-03 cache economics** — instrumentation that RQ-02, RQ-04, RQ-05 all ride
   on, so it is built once and reused three times.
5. **RQ-06 real-world feature cost** — pure analysis over RQ-03's data.
6. **RQ-05 harness effect size** and **RQ-04 intervention rate** — the expensive
   flagship tracks, sharing runs and instrumentation.
7. **RQ-10 frontend fidelity Stage 1** — build and validate the instrument
   before measuring anything with it.

Every instrumented run also produces measured usage profiles, upgrading cost
answers from `assumed` to `measured`. Start the longitudinal maintainability
study early — it takes the longest.

**Engine implementation** — build the spec in RECOMMENDATION.md. All twelve
invariants under test, including the grep-checkable one (no product names in
engine code) and the two added by the decision layer: dominance computed before
any weight, and all six explanation components present or no render.

**Exit:** at least three experiments with published raw data; the seven queries
in QUERIES.md executing against real data and returning either answers or
informative refusals; recommendations that trace end-to-end to sources; the
persona divergence rule run, with personas that never change an answer deleted;
the VOI ranking published and driving the next research cycle.

---

## M5 — Interface

Only now. Everything before this was the product; this makes it usable.

- STUDIO.md — the visual system, written here rather than earlier because it must
  serve the data model, not the reverse
- Question index, decision pages, entity pages, generated comparisons
- Evidence rendering: fact/interpretation/opinion, confidence, freshness at point
  of use
- Search and faceted filtering, including filter-by-evidence-strength
- Stack Builder
- Register pages — conflicts, gaps, freshness, changelog, corrections

**Exit:** no fact originates in the interface; every number links to its source;
a stale claim is visibly stale; the site is correct and readable without
JavaScript.

**Design gate:** if the interface makes a `low`-confidence six-month-old
self-reported number look like a fresh corroborated one, it fails review
regardless of how good it looks.

---

## M6 — Evidence layer ✅ *framework complete 2026-08-04*

```
Coverage        7 / 50
                  ↓
Goal           12 / 50
```

**Shipped:** [EVIDENCE.md](EVIDENCE.md) — per-dimension evidence requirements for
all 13 dimensions, six evidence pipelines with failure gates, six repeatable
benchmark suites with re-run triggers, and hard minimum thresholds below which
the Atlas refuses to score. Plus
[EVIDENCE-ROADMAP.md](research/EVIDENCE-ROADMAP.md) ranking twelve evidence
streams by questions-unblocked.

**The finding that reset the plan:** four of the top six evidence streams
**require no experiment at all**. M5.1 concluded the bottleneck was missing
Class B/C evidence and implied that meant running experiments. Half right — the
larger and cheaper half is that we have not gone and collected the independent
and field evidence already sitting in public. Eight of thirteen dimensions can
leave `not_scored` without running anything.

**Two tracks established.** Track A (evidence) and Track B (reference
population) run in parallel, neither subordinate. Recorded correction: M5.1
argued against populating entities that would not move coverage — correct about
the metric, wrong about the product.

---

## M7 — Sustainment

The milestone that decides whether this is an atlas or an archive.

- Nightly freshness and source-diff jobs
- Weekly release sweeps and stub minting
- Monthly cycle with a published changelog
- Benchmark and pricing importers
- Canary suite for detecting silent endpoint changes (RESEARCH §3.2)

**Exit:** a full monthly cycle completes with the pipeline enqueueing and a human
publishing; corpus freshness holds above target for three consecutive months.

---

## M8 — Openness

- Public read API over the graph
- Contribution process: how a stranger proposes a claim, a correction, or an
  entity
- Reproduction guide for the experiment suite
- Corrections process with public accountability

**Exit:** an external contributor lands a sourced claim through the documented
process, and an external party reproduces one experiment.

---

## Beyond

Sequenced by evidence need, not novelty: longitudinal datasets as the primary
long-term asset · regional coverage to correct the English-language bias
(METHODOLOGY §9) · enterprise evidence, currently our weakest area · historical
analysis of how the ecosystem actually moved, which only becomes possible after
a year of dated claims.

---

## Sequencing principles

1. **Research before implementation, and formalization before research.** The
   M1→M2→M3→M5 order is the point. M2 was inserted after M1 precisely because a
   schema proven against real questions is far cheaper to fill than one proven
   against intuition — and it surfaced four gaps that would have been expensive
   to find with 500 facts already in the graph.
2. **Depth before breadth.** 25 well-sourced entities beat 200 stubs.
3. **All nine layers at every depth.** Covering models deeply and orchestration
   not at all reproduces the bias the project exists to correct.
4. **Coverage is capped by maintenance capacity** (CONSTITUTION §14). If M2's
   measured per-entity cost implies we cannot sustain the corpus, the corpus
   shrinks. That is a real possible outcome and an acceptable one.
5. **No deadlines.** Gates, not dates. A milestone is done when its exit
   condition is met.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.4 | 2026-08-04 | Inserted M6 Evidence layer (framework complete). Renumbered sustainment M7, openness M8. Adopted coverage-first milestone reporting and the Track A / Track B split. |
| 1.3 | 2026-08-03 | Inserted M3.1 Research program (complete). M4 experiment order reset to follow the program's ERI ranking. |
| 1.2 | 2026-08-03 | Inserted M2.5 Decision layer (complete). M4 exit conditions extended for the solver and VOI. |
| 1.1 | 2026-08-03 | Inserted M2 Formalization (complete). Renumbered downstream: evidence base M3, experiments M4, interface M5, sustainment M6, openness M7. Research order in M3 reset to follow the query set. |
| 1.0 | 2026-08-03 | Initial roadmap. M1 complete. |
