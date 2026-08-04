# EVIDENCE COLLECTION FRAMEWORK

**Status:** v1.0 · **Opened:** 2026-08-04 · **Depends on:**
[SOURCES.md](SOURCES.md), [EVALUATION.md](EVALUATION.md), [METHODOLOGY.md](METHODOLOGY.md)

How the Atlas gets from "we can describe things" to "we can rate things."

---

## 0. The situation

Thirteen dimensions. **Nine have zero evidence of any kind.** Four have Class A
specification data only, which SOURCES §3 makes inadmissible for the comparative
judgments scoring requires.

The consequence is stark and worth stating without softening: **the Atlas cannot
currently score anything, and 20 of its 29 unanswerable benchmark questions fail
for that single reason.** More vendor documentation will not change this. Class A
sources are authoritative for what a thing *is* and structurally incapable of
establishing whether it is *good*.

This document defines what would change that.

---

## 1. Per-dimension evidence requirements

For each dimension: what evidence would satisfy it, what Class B and Class C look
like specifically, what public data exists and why it falls short, and what we
would have to run ourselves.

### D1 — Output quality
**Current evidence:** none.
**Required:** blind-rated output against a fixed rubric, across task classes,
with the harness held constant.
**Class B looks like:** a published evaluation with released prompts, raw
outputs, and a rater protocol. Not a leaderboard position.
**Class C looks like:** convergent practitioner reports naming *specific*
recurring quality failures — not "it's good."
**Public data:** repository-patching benchmarks. **Limitation:** they score
test-passing on a solvability-filtered set, which is a narrow proxy for quality
and says nothing about frontend, prose, or design work.
**Original experiment required:** yes — blind rubric scoring within the standard
task suite.
**Effort:** High (human raters, plural).

### D2 — Autonomy
**Current evidence:** none.
**Required:** interventions per unit of *completed* work, by intervention type.
**Class B looks like:** an independent long-horizon study logging interventions
under a published policy.
**Class C looks like:** sustained-use reports describing where agents reliably
get stuck — the failure-mode taxonomy that no vendor documents.
**Public data:** essentially none. Benchmarks score final state, which
structurally hides intervention count.
**Original experiment required:** yes — RQ-04. This is the clearest case in the
whole framework of a dimension that public evidence cannot supply.
**Effort:** High (supervised operator hours; does not parallelize).

### D3 — Engineering output
**Current evidence:** none.
**Required:** does the output constitute shippable engineering — tests, error
handling, conventions — not merely code that runs.
**Class B:** studies rating produced artifacts against engineering criteria.
**Class C:** code review reports from teams merging agent output.
**Public data:** none found. Benchmarks stop at "tests pass."
**Original experiment required:** yes — rides on the D1 rubric with additional
criteria.
**Effort:** Medium (marginal on top of D1).

### D4 — Reliability
**Current evidence:** none.
**Required:** run-to-run variance on identical inputs; failure and error rates;
graceful degradation under throttling.
**Class B:** third-party uptime/latency telemetry; published variance studies.
**Class C:** incident reports, issue trackers, status-page histories.
**Public data:** provider status pages (Class A, self-interested). Third-party
telemetry exists commercially but was not captured.
**Original experiment required:** partly — repeated identical runs to measure
variance, plus the throttle-behaviour test in RQ-02.
**Effort:** Low–Medium (mostly instrumentation on runs done anyway).

### D5 — Maintainability of output
**Current evidence:** none.
**Required:** what the code looks like after months of accumulated agent
contributions.
**Class B:** longitudinal studies of codebases with heavy agent contribution.
**Class C:** engineer reports on maintaining agent-written code.
**Public data:** none. **Nobody has an incentive to measure this** — it takes
months, and the result is unflattering to everyone.
**Original experiment required:** yes, and it is the longest-running one we have.
**Effort:** Very High (months of elapsed time; must start earliest).

### D6 — Cost
**Current evidence:** Class A pricing across several vendors; two first-party
tokenizer experiments.
**Required:** cost per *completed unit of work*, including retries and rework.
**Class B:** independent cost studies with published token accounting.
**Class C:** practitioner spend reports with usage context.
**Public data:** vendor pricing (captured). **Limitation:** price ≠ cost. Missing
the denominator — completed work.
**Original experiment required:** yes — measured usage profiles. This is the most
frequently-blocking gap in the corpus.
**Effort:** Low–Medium (instrumentation).

### D7 — Developer experience
**Current evidence:** none.
**Required:** friction between intent and result.
**Class B:** structured usability studies. Rare in this domain.
**Class C:** **authoritative here** — convergent practitioner reports are the
right instrument, per the SOURCES §3 authority matrix.
**Public data:** abundant but unsampled. This is the one dimension where the
evidence largely *exists* and simply has not been collected under a protocol.
**Original experiment required:** no. Requires disciplined Class C sampling
(METHODOLOGY §4), not new measurement.
**Effort:** Low — **the cheapest dimension to unblock.**

### D8 — Speed
**Current evidence:** none.
**Required:** latency and throughput as felt — time to first token, time to
completed task.
**Class B:** independent latency benchmarking across providers.
**Class C:** reports of perceived slowness under real load.
**Public data:** third-party latency trackers exist; not captured.
**Original experiment required:** no, if a credible Class B source can be
captured and its methodology verified.
**Effort:** Low.

### D9 — Flexibility
**Current evidence:** Class A capability data (partial).
**Required:** how far the thing bends before breaking — non-standard workflows,
configuration limits.
**Class B:** rare.
**Class C:** authoritative — reports of people pushing tools past intended use.
**Original experiment required:** no.
**Effort:** Low–Medium.

### D10 — Ecosystem maturity
**Current evidence:** none.
**Required:** integrations, docs quality, community durability.
**Class B:** repository and download telemetry with stated methodology.
**Class C:** sustained-activity signals; **migration-away reports are the
strongest available and point opposite to marketing.**
**Public data:** repository metrics are freely available.
**Original experiment required:** no.
**Effort:** Low. **But: the M2.5 VOI analysis flagged this dimension as changing
no recommendation at any plausible value. Collect it cheaply or not at all.**

### D11 — Data & licensing posture
**Current evidence:** Class A partial.
**Required:** actual data handling, not stated policy.
**Class B:** third-party audits, compliance certifications.
**Class C:** reports of policy-practice divergence.
**Public data:** vendor policies (Class A, self-interested by construction).
**Original experiment required:** no — but Class A alone cannot establish that
practice matches policy, and we should say so on every such claim.
**Effort:** Low.

### D12 — Continuity risk
**Current evidence:** none.
**Required:** funding durability, governance, licence forkability, deprecation
history.
**Class B:** funding disclosures, foundation governance records.
**Class C:** maintainer-count signals, bus-factor observations.
**Public data:** substantial and uncollected. **Deprecation track record is the
single most predictive input and is fully public.**
**Original experiment required:** no.
**Effort:** Low–Medium.

### D13 — Security posture
**Current evidence:** Class A partial (MCP's own security disclaimer).
**Required:** blast radius, sandboxing, approval gates, extension supply chain.
**Class B:** **authoritative** — independent security audits of agent runtimes
and extension ecosystems.
**Class C:** incident reports; prompt-injection findings.
**Public data:** security research exists; the M1 scan surfaced enough to justify
adding the dimension.
**Original experiment required:** no initially — capture existing Class B first.
**Effort:** Low–Medium.

### Summary

| Needs original experiment | Unblockable from existing public evidence |
|---|---|
| D1, D2, D3, D5, D6 | D7, D8, D9, D10, D11, D12, D13, D4 (partly) |

**Eight of thirteen dimensions can be unblocked without running anything.** That
reframes the milestone: the bottleneck is not only measurement capacity, it is
**collection discipline on evidence that already exists**.

---

## 2. Evidence pipelines

Each pipeline is a repeatable path from raw evidence to a scored dimension, with
a gate that can fail.

### Pipeline A — Frontend quality
```
brief set (fixed, published)
  → generation across stacks, harness held constant
  → blind scoring: raters do not know which stack produced which output
  → INTER-RATER AGREEMENT GATE ── fails → revise rubric, do not publish
  → rubric scores + iterations-to-acceptable
  → publish raw outputs, screenshots, rubric, scores
  → D1/D3 scores with `via` context
```
**Gate:** agreement below the preregistered threshold blocks publication. A
single-rater result measures our taste.

### Pipeline B — Autonomy
```
standard task suite (versioned)
  → supervised runs under a fixed intervention policy
  → intervention log: timestamp, type, context position
  → INTER-RATER GATE on intervention classification
  → normalize per unit of COMPLETED work
  → failure-mode taxonomy from clustered interventions
  → D2 score + published failure modes
```
**Gate:** intervention taxonomy must survive independent re-classification from
transcripts. **Approvals are counted separately from corrections** — a safety
gate is not an autonomy failure.

### Pipeline C — Context engineering
```
identical task + identical model + identical harness
  → vary ONE context strategy (index-first / agentic search / naive / compacted)
  → measure: task success, tokens to answer, wall-clock, retries
  → repeat ≥3 per cell
  → controlled comparison → strategy recommendation
```
**Gate:** if variance between repeats exceeds variance between strategies, the
result is inconclusive and publishes as such.

### Pipeline D — Harness effect
```
N models × M harnesses × task suite, fully crossed
  → ≥3 replications per cell
  → minimal baseline harness included as control
  → variance decomposition: model / harness / interaction
  → D1/D2/D3 scores, and a finding about attribution itself
```
**Gate:** reduced coverage weakens the interaction term specifically; if the
design must shrink, report which terms became unidentifiable.

### Pipeline E — Class C sampling *(no experiment required)*
```
declare population + query + time window BEFORE reading
  → sample top-by-engagement AND most-recent
  → tag every source: usage_duration, sample_type, population
  → require convergence on SPECIFIC behaviours, not sentiment
  → ≥3 independent reports of the same specific failure → X-type claim
  → D4, D7, D9, D10, D12 scores
```
**Gate:** volume is not convergence. Fifty upvotes on one report is one report.

### Pipeline F — Class B capture *(no experiment required)*
```
identify candidate independent study
  → verify methodology is published
  → record run_by, funded_by, contamination_risk
  → capture verbatim with excerpts
  → admissibility check against claim type
  → D8, D11, D13 scores
```
**Gate:** a study without published methodology is Class E, not Class B,
regardless of who published it.

---

## 3. Repeatable benchmark suites

Suites are versioned artifacts designed to be **re-run on a trigger**, so results
become longitudinal rather than snapshots.

| Suite | Measures | Re-run trigger |
|---|---|---|
| `suite-agentic-core` | task success, interventions, cost, tokens | new model · harness release · provider change |
| `suite-frontend` | visual fidelity, responsive, a11y, iterations | new model · quarterly |
| `suite-large-repo` | cross-file accuracy, tokens to answer | new model · context-layer change |
| `suite-longhorizon` | autonomous duration, failure points | new model · harness release |
| `suite-canary` | token counts, latency, output shape on fixed inputs | **nightly** — detects silent endpoint changes |
| `suite-tokenizer` | token counts on the fixed corpus | new tokenizer or model family |

**`suite-canary` deserves emphasis.** It is cheap, automatable, and the only
defence against a provider silently changing quantization, routing, or model
behind a stable endpoint name — a risk the taxonomy identified in M1 and which
nothing else in the framework detects.

**Versioning rule:** a suite change creates a new version. Results across
versions are never pooled. The suite's own history is part of the dataset.

---

## 4. Minimum evidence thresholds for scoring

**Until a dimension meets its threshold, the Atlas refuses to score it.** These
are hard gates, not guidelines.

| Tier | Requirement | Renders as |
|---|---|---|
| **Not scored** | Below threshold | `not_scored` with reason — current state for all 13 |
| **Provisional** | 1 admissible source, single condition set, no corroboration | Score shown with `low` confidence and a provisional marker |
| **Scored** | ≥2 independent admissible sources **or** ≥1 Class D experiment with ≥3 replications; conditions recorded | Normal render |
| **Well-evidenced** | ≥3 independent sources spanning ≥2 classes; convergent | Normal render, `high` confidence available |

### Per-dimension minimums

| Dimension | Minimum to leave `not_scored` |
|---|---|
| D1, D3 | Blind rubric scores, ≥2 raters, agreement above threshold, `via` harness recorded |
| D2 | ≥3 supervised runs per stack, intervention taxonomy passing inter-rater check |
| D4 | ≥3 repeated identical runs (variance) **or** ≥3 convergent Class C incident reports |
| D5 | Longitudinal observation ≥3 months **or** ≥3 convergent Class C maintenance reports |
| D6 | Measured usage profile (not `assumed`) + captured pricing + retry rate |
| D7, D9 | ≥3 independent Class C reports converging on specific behaviours, sampled per Pipeline E |
| D8 | ≥1 Class B latency source with published methodology |
| D10, D12 | ≥2 public signals + deprecation/governance history |
| D11 | Class A policy **plus** ≥1 independent corroboration — policy alone never suffices |
| D13 | ≥1 Class B security audit **or** ≥3 convergent incident reports |

**Composite gate:** a stack-level recommendation requires ≥6 of 13 dimensions
scored, including D6, and states its coverage. Below that, the engine returns
`INSUFFICIENT_COVERAGE`.

**No exceptions for convenience.** If a launch is imminent and evidence is thin,
the correct output is a refusal that names what is missing.

---

## 5. Honest limits of this framework

- **Human raters are the bottleneck** for D1, D2, D3, D5, and they do not
  parallelize. Every high-value dimension routes through the scarcest resource.
- **Single-operator bias persists.** Blind scoring and inter-rater gates reduce
  it; a second independent team would be needed to eliminate it, and we do not
  have one.
- **Class D is not automatically superior to Class B.** An n=3 in-house run is
  weaker than a well-run public study. Where good Class B exists, capturing it
  beats running our own — Priority 1 identifies eight dimensions where that is
  true.
- **D5 cannot be shortcut.** It requires elapsed months. Any faster proxy
  measures something else and should be labelled as such.
- **Thresholds may prove too strict.** If the corpus sits at zero scored
  dimensions for two quarters, the thresholds — not the standards — should be
  re-examined, publicly, with the reasoning recorded.
