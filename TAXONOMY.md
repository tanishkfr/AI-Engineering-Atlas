# ECOSYSTEM TAXONOMY

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Validated against:** the
2026-08-03 landscape scan (~120 entities, `research/scan-2026-08-03.md`)

How the Atlas divides the world. This is the vocabulary that `/data` and the
entire interface are built on, so it is the most expensive document in the
repository to get wrong.

---

## 0. What the scan changed

This taxonomy was drafted as a tree, tested against the real ecosystem, and
rebuilt. Four findings forced the rebuild — recorded here because the failures
are more instructive than the final structure.

**Finding 1 — a tree cannot hold this ecosystem.**
Claude Code is a CLI harness, a subscription product, an SDK, *and* a hosted
background agent. Cursor is an editor, a model vendor, and — since acquiring
Graphite — a code review tool. Kiro is an editor, a methodology, and a model
router. Sourcegraph is a code search product and an MCP server and a context
layer. Every single one of these would need to be duplicated or arbitrarily
assigned in a tree.
→ **The taxonomy is faceted. Entities carry multiple roles across multiple
layers.** A tree would have forced a lie on the first day.

**Finding 2 — identity is unstable, so aliasing is load-bearing.**
Clawdbot → Moltbot → OpenClaw, inside twelve months. Amazon CodeWhisperer →
Amazon Q Developer. Graphite absorbed into Cursor Bugbot. Gitar into Sonar. MCP
donated by Anthropic to the Agentic AI Foundation.
→ **Every entity needs stable synthetic IDs, an alias list, and lifecycle
relations** (`renamed_from`, `acquired_by`, `replaces`, `governed_by`).
Naming a record after a product is how a knowledge base dies of rebranding.

**Finding 3 — nine categories were missing from the original brief.**
The brief's list (models, harnesses, providers, IDEs, agent frameworks,
benchmarks, MCP, memory, context) omits things the scan found to be large,
active, and decision-relevant: **code review agents** · **agent orchestration
and parallel runners** · **code intelligence / retrieval** · **observability and
eval platforms** · **app builders** · **skills and extension registries** ·
**standards and protocols as entities** · **governance bodies** · **security
research on the agent ecosystem**.
→ Added. Several are where the interesting 2026 decisions actually live.

**Finding 4 — "the model" is not one thing.**
`Claude Opus 5` names a family, a version, and a set of served endpoints that
may differ in quantization, routing, and context limits by provider. The scan
found six mutually incomparable SWE-bench Verified figures in circulation
(80.6 / 80.8 / 85.5 / 87.6 / 93.4 / 95.0), differing by harness, variant,
date, and who ran them.
→ **Model, model-version, and served-endpoint are three separate entity
types.** Collapsing them is precisely how the incomparable numbers above end up
in the same table.

---

## 1. Structure: 9 stack layers + 2 meta-classes

The nine layers are **the choices you make when assembling a stack**. That is
the organizing question, because it is the reader's question.

```
                        ┌─────────────────────────────┐
   what you interact    │  L4  SURFACE                │
   with                 └─────────────────────────────┘
                        ┌─────────────────────────────┐
   how humans work      │  L9  PRACTICE               │
                        └─────────────────────────────┘
   ─────────────────────────────────────────────────────
                        ┌─────────────────────────────┐
   the agent loop       │  L3  HARNESS                │
                        └─────────────────────────────┘
        ┌──────────────┐┌──────────────┐┌─────────────┐
        │ L5 INTEROP   ││ L6 CONTEXT   ││ L7 ORCHESTR.│
        └──────────────┘└──────────────┘└─────────────┘
                        ┌─────────────────────────────┐
   did it work?         │  L8  ASSURANCE              │
                        └─────────────────────────────┘
   ─────────────────────────────────────────────────────
                        ┌─────────────────────────────┐
   how you get tokens   │  L2  ACCESS                 │
                        └─────────────────────────────┘
                        ┌─────────────────────────────┐
   the capability       │  L1  MODEL                  │
                        └─────────────────────────────┘

   meta:  M1 EVIDENCE ARTIFACT      M2 INSTITUTION
```

---

## 2. The layers

### L1 — MODEL

The capability itself.

**Types:** `model_family` · `model_version` · `model_endpoint`

The three-way split from Finding 4:

| Type | Is | Example shape |
|---|---|---|
| `model_family` | The named lineage. Stable across versions. | a vendor's coding model line |
| `model_version` | A specific release with a specific ID, date, and card | the dated, versioned release |
| `model_endpoint` | A version *as served by a specific provider* — with its own context limit, quantization, price, latency, and possible routing | provider × version |

**Every measurement attaches to a `model_endpoint`, never to a family.** This is
non-negotiable and is the single most important rule in the taxonomy. A
benchmark score without an endpoint is a number without conditions.

**Facets:** openness (closed / open-weight / open-source) · licence · modality ·
reasoning mode · context window · tool-use support · self-hostable ·
release status (preview / GA / deprecated).

**Boundary:** a fine-tune is a `model_version` with a `derived_from` edge, not a
new family. A distilled or quantized variant is a `model_version` with
`quantization` set — quantization is *not* an endpoint property when it's
published as its own artifact, and *is* when a provider applies it silently.
The distinction matters because silent provider quantization is a real and
under-reported source of quality variance.

### L2 — ACCESS

How you obtain inference. Independent of what the model is.

**Types:** `first_party_api` · `aggregator` (routers/marketplaces) ·
`inference_provider` (serverless per-token) · `gpu_platform` (per-GPU-second) ·
`local_runtime` · `subscription_plan` · `free_tier`

Two things the scan proved belong here rather than under L1:

- **Price spread on identical weights.** The same open model priced across
  providers with a wide multiple between cheapest and dearest. That spread is an
  *access* fact and one of the highest-value facts the Atlas can carry.
- **Subscription plans are entities, not attributes.** "Is a $20 subscription
  better than $20 of API credits" is one of the questions this project exists to
  answer, and it cannot be answered if plans are buried as fields on a vendor.

**Facets:** billing model · rate limits · cache support and discount ·
data retention and training policy · region and residency · SLA · free tier ·
BYOK support.

### L3 — HARNESS

The agent loop: the thing that decides what to read, what to edit, when to run a
command, when to stop. Empirically the layer that most determines whether work
gets done — and the layer most often confused with L1 in public discussion.

**Types:** `cli_agent` · `ide_agent` · `background_agent` (async/cloud,
issue-to-PR) · `app_builder` (prompt-to-deployed-app) · `agent_sdk` ·
`chat_assistant`

**Facets:** hosted vs local execution · sandboxing model · model-agnostic vs
locked · subagent support · permission and approval model · session persistence ·
headless/CI operation · cost model.

**Boundary vs L7:** a harness runs *one* agent loop. Coordinating several loops
is L7. A harness with built-in subagents is still L3 — the boundary is whether
the coordination is exposed as an independent choice.

**Boundary vs L4:** the harness is the loop; the surface is where you see it.
Cursor-the-editor is L4; Cursor's agent mode is L3. They ship together and are
still separate decisions, because you can put a different agent in that editor.

### L4 — SURFACE

Where the human meets the system.

**Types:** `ai_editor` (AI-first forks) · `ide_extension` · `terminal` ·
`web_console` · `code_host_integration` (PR/CI-resident) · `messaging_surface`
(chat platforms as an agent entry point) · `mobile`

The scan showed messaging surfaces are a real and growing entry point — the
always-on agents reach users through chat platforms rather than an editor.
That is a genuinely different interaction model with genuinely different
security properties, and it needs a category rather than a footnote.

### L5 — INTEROP

How an agent reaches beyond its own process.

**Types:** `protocol` · `server` (e.g. MCP servers) · `skill` ·
`plugin` · `hook` · `registry` · `tool_definition`

**Protocols and standards are entities.** They have versions, governance,
adoption curves, and competitors. Treating them as attributes would make it
impossible to answer "should I build on this standard?" — which is a real
decision with real switching costs.

The scan found this layer is where **quality and security collapse**: enormous
public catalogs of skills and servers, low average quality, and independent
security research finding prompt-injection vectors in a large fraction of
audited skills. A registry's *size* is therefore an anti-signal as often as a
signal, and the taxonomy separates `registry` (an index) from the artifacts it
indexes so we can say so with data.

**Facets:** transport · auth model · governance body · spec version ·
sandboxing · permission scope · audited (bool).

### L6 — CONTEXT

What the agent knows at the moment of action.

**Types:** `code_intelligence` (index/graph/search over a repo) ·
`retrieval_system` · `memory_layer` (cross-session persistence) ·
`context_format` (repo-level instruction file conventions) ·
`compaction_strategy`

The scan surfaced a live architectural split worth modelling explicitly:
**index-first** (build embeddings/graphs before the agent runs) vs
**agentic search** (expose retrieval as tools and let the model navigate).
That split is a `context_strategy` facet, and it is one of the more consequential
choices for large repositories.

**Boundary:** a memory layer is L6. A memory *feature inside a harness* is a
harness facet with a `provides` edge to the memory capability. The
concept exists once; implementations point at it.

### L7 — ORCHESTRATION

Coordinating more than one agent, run, or workspace.

**Types:** `agent_framework` · `parallel_runner` · `workspace_isolation`
(worktree tooling and sandboxes) · `scheduler` · `fleet_manager` ·
`handoff_protocol`

The scan's clearest structural finding: **workspace isolation became
load-bearing in 2026**. Once two agents touch one repo, a single working
directory stops working — lockfile races, silent overwrites. A cluster of
tooling now exists solely to give each agent its own working copy. That is not a
footnote under "frameworks"; it is a distinct thing people choose.

### L8 — ASSURANCE

How you find out whether the output is any good — the counterweight layer, and
the one most under-covered in comparison content.

**Types:** `code_review_agent` · `test_generation` · `static_analysis` ·
`security_scanner` · `eval_platform` · `observability` · `ci_gate`

This layer earns its prominence from the adoption data: developers report
spending **more time reviewing AI-generated code than writing new code**, while
trust in that output has *fallen*. If the review burden is where the time now
goes, then tooling that reduces it is a first-order decision, not an accessory.

The scan also shows this layer consolidating fast (multiple 2025–26
acquisitions), which makes L8 the highest-continuity-risk layer in the stack —
directly relevant to EVALUATION.md D12.

### L9 — PRACTICE

How humans actually work with the system. Not a product category — and a real
one.

**Types:** `workflow` · `methodology` (e.g. spec-driven development) ·
`prompting_technique` · `context_engineering_practice` ·
`team_process` · `anti_pattern`

Practices are entities with evidence, tradeoffs, and personas, exactly like
products. `anti_pattern` is a first-class type: knowing what reliably fails is
often worth more than another tool comparison, and nobody has an incentive to
publish it.

---

## 3. Meta-classes

### M1 — EVIDENCE ARTIFACT

Things that *produce evidence* rather than do work.

**Types:** `benchmark` · `leaderboard` · `dataset` · `survey` ·
`research_paper` · `experiment` (our Class D) · `incident_report`

Benchmarks are entities so their construct validity, saturation, contamination
risk, and version history live in one place and travel with every citation
(METHODOLOGY.md §5). A benchmark entity requires: what it measures, what it is
routinely misread as measuring, and its harness dependency.

Leaderboards are separate from benchmarks — a leaderboard is a *publication of*
benchmark results by a specific party under a specific harness, and the scan
found the same nominal benchmark reported with wildly different numbers by
different leaderboards. That gap only has somewhere to live if the two are
separate entities.

Surveys are entities because adoption and sentiment claims (T-type) need the
same treatment as scores: population, sample size, date, methodology, and who
paid for it.

### M2 — INSTITUTION

Who makes, funds, governs, or indexes the things.

**Types:** `vendor` · `foundation` · `standards_body` · `research_lab` ·
`registry_operator` · `community`

Needed for continuity-risk scoring, conflict-of-interest flags, and consolidation
tracking. When a standard moves from a vendor to a foundation, or a tool is
acquired by a competitor, that is a governance fact with direct bearing on
whether you should build on it.

---

## 4. Relationships

> ⚠ **Superseded by [GRAPH.md](GRAPH.md) (v1.0, 2026-08-03).** The sketch below
> is retained as the record of the original design. The formal ontology — with
> domain/range typing, inverses, cardinality, three-valued compatibility,
> capability entities, temporal validity, and inference rules — lives in
> GRAPH.md, which is authoritative. Four predicate names were retired in the
> move: `succeeded_by` → `replaces`, `requires` → `depends_on`,
> `provides_capability` → `provides`, `scored_on` → `measured_on`. Rationale in
> GRAPH.md §5.

Edges are why this is a graph and not a spreadsheet. The controlled vocabulary:

**Composition**
`runs_on` · `served_by` · `bundles` · `requires` · `optional_with` ·
`provides_capability` · `implements` (entity → protocol)

**Lineage**
`derived_from` · `fork_of` · `renamed_from` · `succeeded_by` · `version_of`

**Corporate / governance**
`made_by` · `acquired_by` · `governed_by` · `funded_by` · `donated_to`

**Competitive**
`alternative_to` · `competes_with` · `migration_target_of`
(`migration_target_of` is derived from field reports of teams actually
switching — one of the strongest adoption signals available, and it points the
opposite way from marketing.)

**Evidence**
`measured_by` · `scored_on` · `documented_in` · `contradicted_by`

**Practice**
`recommended_for` (→ persona) · `incompatible_with` · `mitigates` (→ anti-pattern)

Every edge carries `evidence`, `as_of`, and `confidence` — the same discipline as
claims. An unsourced relationship is an unsourced claim.

---

## 5. Hard cases

A taxonomy is only as good as its answers on the ambiguous entities. These are
worked examples; the classification rules above are what generated them.

| Entity shape | Placement |
|---|---|
| **Vendor CLI agent + subscription + SDK + cloud runner** | Four entities: `cli_agent` (L3), `subscription_plan` (L2), `agent_sdk` (L3), `background_agent` (L3) — joined by `bundles` and `made_by`. Scored separately; they are separately choosable. |
| **AI editor that also ships its own models and a review bot** | `ai_editor` (L4) + `ide_agent` (L3) + `model_family` (L1) + `code_review_agent` (L8), with `acquired_by` capturing the review bot's provenance. |
| **Spec-driven dev toolkit** | `methodology` (L9) as the primary entity; the CLI implementing it is a separate L3/L9 tool with `implements`. The methodology outlives any one implementation, which is the point. |
| **Always-on personal agent reached via chat** | `background_agent` (L3) + `messaging_surface` (L4) + `memory_layer` (L6). Its security posture is a scored property, not an aside. |
| **Router that picks a model per task** | `aggregator` (L2) *and* `orchestration` facet (L7). Genuinely dual — the routing decision is an orchestration behavior sold as an access product. |
| **Code search platform exposing an MCP server** | `code_intelligence` (L6) + `server` (L5) with `implements` → MCP protocol. |
| **Repo instruction-file convention** | `context_format` (L6) *and* `protocol` (L5) if it has a published spec and cross-vendor adoption. Conventions that become standards migrate; the alias chain records it. |
| **Benchmark with an official leaderboard and third-party mirrors** | One `benchmark` (M1) + N `leaderboard` entities (M1), each with its own harness, operator, and date. |

**Placement rule when in doubt:** ask *what decision does a reader make about
this thing?* If two decisions are separable, they are two entities. If they are
never separable, it is one entity with two roles.

---

## 6. Rules

1. **Facets, not folders.** Multi-layer entities are normal, not exceptions.
2. **IDs are synthetic and permanent.** `ent-` + slug, minted once, never
   changed. Products rename; IDs do not.
3. **Aliases are mandatory** for anything that has ever been called something
   else, including informal community names.
4. **Measurements bind to `model_endpoint`**, never to a family or version alone.
5. **A category with one member is a suspicious category.** Either it is
   premature or the boundary is wrong. Flag rather than keep.
6. **New types require a taxonomy amendment** with the entity that forced it. The
   scan finding that produced a category stays attached to it.
7. **Deprecated entities are retained**, marked `deprecated` with a `replaced_by`
   edge. The history of what died is part of the value of an atlas.
8. **Practices and anti-patterns are entities.** They get evidence, scores, and
   personas like everything else.

---

## 7. Open taxonomy questions

Unresolved, tracked in `RESEARCH.md`, deliberately not papered over.

- **Is `app_builder` really L3?** These collapse harness, surface, hosting, and
  deployment into one product. They may need a `platform` composite type. Held
  as L3 with multi-role tagging until a decision question forces the split.
- **Where do "agent skills" end and "context" begin?** A skill is packaged
  instructions (L5 interop) that functions as retrieved context (L6). Currently
  L5 by governance and distribution; the boundary is genuinely blurry and may
  need a `capability_package` type spanning both.
- **Security posture** appears across L2 (data handling), L3 (sandboxing), L5
  (untrusted skills), and L4 (messaging exposure). It is currently a facet
  everywhere rather than a layer. If it keeps recurring it may deserve
  promotion — see the EVALUATION.md v1.1 amendment adding D13.
- **Are subscription plans stable enough to be entities?** They change more often
  than anything else in the graph. Modelled as entities with short review
  cadence; revisit if maintenance cost proves unsustainable.
- **Model-family identity across major versions.** When a lineage changes
  architecture and naming simultaneously, family continuity becomes a judgment
  call. No rule yet; documented case-by-case.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial taxonomy, rebuilt from a tree to facets after the landscape scan. Nine layers, two meta-classes, nine categories added beyond the original brief. |
