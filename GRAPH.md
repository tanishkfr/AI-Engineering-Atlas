# GRAPH ONTOLOGY

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Supersedes:** TAXONOMY.md
§4 · **Machine form:** `data/schema/relationship.schema.json`,
`data/schema/predicates.yaml`

The formal relationship layer. TAXONOMY.md says what things *are*; this says how
they *connect*, with enough rigor that the connections are checkable and
traversable rather than decorative.

---

## 1. What the edges are for

A relationship earns its place only if it answers a question a reader has. Every
predicate below traces to one:

| Reader question | Edge |
|---|---|
| Can I use these two things together? | `works_with` / `incompatible_with` |
| What do I need in place first? | `depends_on` |
| What is this an alternative to? | `alternative_to`, `competes_with` |
| Where can I actually get this model? | `available_through`, `hosted_by` |
| What happens if this dies? | `replaces`, `replaced_by`, `acquired_by` |
| Who says it's good? | `measured_on`, `measured_by`, `evaluated_by` |
| What does it actually do? | `provides` → capability |
| Who is behind it? | `made_by`, `governed_by`, `funded_by` |
| Are people leaving it? | `migration_target_of` |

Edges with no reader question behind them are ornamentation, and this ontology
has none.

---

## 2. Ontology principles

**Every edge is a fact.** Same treatment as claims: evidence, confidence, and
bitemporal validity (TEMPORAL.md §4). An unsourced edge is an unsourced claim.

**Every edge is typed by domain and range.** A predicate declares which entity
roles may appear on each end. Violations fail validation, which is what stops
the graph decaying into a tangle of untyped associations.

**Compatibility is three-valued.** `compatible` · `incompatible` · **`unverified`**.
The absence of a `works_with` edge means *we have not checked*, never *it works*.
This distinction is load-bearing for the recommendation engine — a stack built
from unverified pairs is marked as untested rather than silently presented as
working.

**Edges are directional with declared inverses.** Stored once on the subject,
indexed both ways at build time.

**Inference is explicit and labeled.** Derived edges (§6) are materialized with
`derived: true` and the rule that produced them. A derived edge is never
indistinguishable from an observed one.

---

## 3. Capabilities as entities

A new entity class, introduced here because the recommendation engine needs it.

A **capability** is a normalized, entity-independent feature: `prompt_caching`,
`byok`, `tool_use`, `vision_input`, `subagents`, `sandboxed_execution`,
`offline_operation`, `mcp_client`, `mcp_server`, `worktree_isolation`,
`session_persistence`, `headless_ci`, `structured_output`, `no_training_on_input`,
`data_residency_control`, `spec_workflow`, `parallel_agents`.

```yaml
id: cap-prompt-caching
name: Prompt caching
definition: >
  Reuse of previously-submitted context across requests at reduced cost
  and/or latency.
measurement: cost_reduction_ratio        # how it is evidenced, if at all
substitutable_by: [cap-context-compaction]
```

Why this matters more than it looks:

Without capabilities, every constraint must be written against a *facet of a
specific role* — `harness.sandboxing`, `provider.retention_policy`,
`editor.offline`. That means every new entity role requires new engine code, and
the model has to be redesigned each time the ecosystem grows a category. That
is exactly the failure the brief asks to avoid.

With capabilities, **constraints are expressed against capabilities, not entity
types.** "I need offline operation" filters correctly across models, runtimes,
harnesses, and editors — including categories that do not exist yet. A new class
of tool participates the moment it declares `provides` edges.

Capabilities are also where honest substitution lives: `substitutable_by` lets
the engine say "this stack lacks prompt caching but compensates with context
compaction" rather than eliminating it.

---

## 4. Relationship catalog

Cardinality is per direction. `sym` = symmetric, `trans` = transitive.
All edges are `step` temporal kind unless noted.

### 4.1 Composition and interoperation

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `works_with` | any → any | `works_with` | sym · **three-valued** · requires evidence of actual use |
| `incompatible_with` | any → any | `incompatible_with` | sym · requires a stated failure mode |
| `depends_on` | any → any | `dependency_of` | trans · hard requirement |
| `optional_with` | any → any | `optional_with` | sym · enhances, not required |
| `bundles` | any → any | `bundled_by` | ships together as one product |
| `provides` | any → capability | `provided_by` | the extensibility hinge (§3) |
| `implements` | any → protocol | `implemented_by` | with spec version qualifier |
| `extends` | any → any | `extended_by` | plugin/skill/server → host |

`works_with` demands evidence that the pair has actually been run together — a
vendor compatibility matrix (Class A) or field reports (Class C). Inferring it
from "both support MCP" is not permitted; protocol support is necessary and
routinely insufficient.

### 4.2 Access and hosting

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `available_through` | model_version, harness → access entity | `offers` | 1..n · **commercial** availability |
| `hosted_by` | model_endpoint → inference_provider, gpu_platform | `hosts` | 1..n · **who runs the compute** |
| `resells` | aggregator → access entity | `resold_by` | trans |
| `runs_on` | any → local_runtime, platform | `runs` | execution substrate |
| `priced_under` | any → subscription_plan, billing model | `prices` | |

**`available_through` and `hosted_by` are deliberately separate.** A router sells
you access to a model it does not host. When a provider silently changes
quantization or routing, the fault lies with the *host*, not the seller — and
that distinction is only expressible if the two edges are distinct. This is one
of the more useful things the Atlas can surface and it is invisible in every
model-centric comparison.

### 4.3 Lineage and succession

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `replaces` | any → any | `replaced_by` | trans · succession |
| `version_of` | model_version → model_family | `has_version` | |
| `endpoint_of` | model_endpoint → model_version | `has_endpoint` | |
| `derived_from` | any → any | `derivative_of` | fine-tunes, distillations, quantizations |
| `fork_of` | any → any | `forked_into` | |
| `renamed_from` | any → any | `renamed_to` | `point` kind · identity continuity |

### 4.4 Corporate and governance

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `made_by` | any → institution | `makes` | 1 |
| `acquired_by` | any → institution | `acquired` | `point` kind |
| `governed_by` | protocol, project → institution | `governs` | |
| `funded_by` | any → institution | `funds` | bias-relevant |
| `donated_to` | any → institution | `received` | `point` kind |

### 4.5 Competition and substitution

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `alternative_to` | any → any | `alternative_to` | sym · same slot, same job |
| `competes_with` | institution → institution | `competes_with` | sym · commercial |
| `migration_target_of` | any → any | `migrated_to` | **directional, evidence-heavy** |

`migration_target_of` requires Class C evidence of teams *actually switching*,
with direction and stated reason. It is the strongest adoption signal available
and the one that most often contradicts marketing, so its evidence bar is the
highest in the catalog: recurring-theme or consensus sampling, never a single
report.

### 4.6 Evidence and evaluation

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `measured_on` | any → benchmark | `measures` | `measurement` kind · conditions required |
| `measured_by` | any → institution | `measured` | who ran it |
| `published_in` | measurement → leaderboard | `publishes` | separates result from publisher |
| `evaluated_by` | any → institution, publication | `evaluated` | third-party review |
| `documented_in` | any → source | `documents` | |
| `contradicted_by` | fact → fact | `contradicts` | feeds the conflict register |

The `measured_on` / `measured_by` / `published_in` triple exists because M1
scan finding F4 showed the same nominal benchmark reported with wildly different
numbers by different publishers. Collapsing these three into "has a score" is
precisely how that confusion propagates.

### 4.7 Practice and fit

| Predicate | Domain → Range | Inverse | Props |
|---|---|---|---|
| `recommended_for` | any → persona | `recommends` | **derived** from the engine, never authored |
| `unsuitable_for` | any → persona | `avoids` | derived; anti-recommendations |
| `mitigates` | any → anti_pattern | `mitigated_by` | |
| `exhibits` | any → anti_pattern | `exhibited_by` | evidence-heavy |
| `requires_practice` | any → practice | `practice_for` | e.g. tool needs a workflow to pay off |

`recommended_for` is **computed by the recommendation engine and written back as
a derived edge**. It is never hand-authored — a hand-authored recommendation
edge is an unscoped opinion, which CONSTITUTION §6 forbids.

---

## 6. Derived edges

Materialized by the build with `derived: true` and a named rule. Inference is
narrow by design — an ontology that infers aggressively produces confident
nonsense.

| Rule | Derivation |
|---|---|
| `R1` transitive availability | `A endpoint_of B` ∧ `B available_through C` → `A available_through C` |
| `R2` reseller chain | `A resells B` ∧ `B offers C` → `A offers C`, capped at depth 2 |
| `R3` capability inheritance | `A bundles B` ∧ `B provides C` → `A provides C` |
| `R4` slot rivalry | same layer ∧ same role ∧ overlapping capability set → `alternative_to` (candidate, needs confirmation) |
| `R5` incompatibility propagation | `A depends_on B` ∧ `B incompatible_with C` → `A incompatible_with C` |
| `R6` recommendation | engine output → `recommended_for` / `unsuitable_for` |

**Not inferred, deliberately:** `works_with` is never derived from shared
protocol support. Two things both speaking MCP is not evidence they work
together, and asserting otherwise would be the single most damaging inference
this graph could make.

R4 produces *candidates* for human confirmation, not published edges.

---

## 7. Integrity rules

Validation failures, not warnings.

1. Domain and range conform to the predicate declaration.
2. No self-edges except `alternative_to` on a family (explicitly disallowed).
3. Symmetric predicates are stored once; the build materializes the inverse.
4. `depends_on` and `replaces` chains are acyclic.
5. Every edge has evidence, `asserted_from`, and a temporal kind.
6. `works_with` requires evidence of observed co-use, not inferred compatibility.
7. `incompatible_with` requires a stated failure mode.
8. `migration_target_of` requires Class C sampling metadata.
9. `recommended_for` must carry `derived: true` and a persona reference.
10. A `model_endpoint` must have exactly one `endpoint_of` and at least one
    `hosted_by`.
11. Derived edges are never hand-authored; hand-authored `derived: true` fails.
12. An edge asserted valid over an interval where its subject or object did not
    exist fails temporal integrity.

---

## 8. Traversals the engine relies on

Acceptance criteria for the graph layer.

| Traversal | Path |
|---|---|
| Every way to obtain model M | `M ← endpoint_of ← * → hosted_by/available_through → access` |
| Everything a harness can run | `H → works_with → model_version`, plus R1/R2 for access |
| Full stack validity | pairwise `works_with` / `incompatible_with` / unverified across all chosen slots |
| Capability satisfaction | `stack → provides → capability` ⊇ required capability set, with `substitutable_by` fallback |
| Blast radius of a vendor failing | `institution ← made_by ← * → dependency_of →* ` (transitive) |
| Substitutes for a component | `alternative_to` ∪ same-slot candidates ∩ compatible with the rest |
| Evidence chain for any score | `score → claims → sources → excerpts` |
| Historical state | all of the above against `graph_at(date)` (TEMPORAL.md §4) |

"Blast radius of a vendor failing" deserves a mention: it is directly
computable here and answers a question — *what breaks if this company is
acquired or shuts down* — that nothing in this ecosystem currently answers, and
that feeds EVALUATION.md D12 with something better than a judgment call.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial ontology. Supersedes TAXONOMY §4. Adds capability entities, three-valued compatibility, split `benchmarked_by` into three, separated `hosted_by` from `available_through`. |
