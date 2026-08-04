# SOURCE QUALITY FRAMEWORK

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Governs:** every `source`
and `evidence` object in `/data`

This document defines what counts as a source, how sources are graded, and — the
part most frameworks skip — **which kinds of claims a given source is allowed to
support**.

> This is the source-quality framework. The *research process* that uses it is
> in [METHODOLOGY.md](METHODOLOGY.md). The *scoring rubric* that consumes its
> output is in [EVALUATION.md](EVALUATION.md).

---

## 0. The correction this framework makes

The obvious design is a single ladder: official docs at the top, community chatter
at the bottom, confidence tracking position on the ladder.

That design is wrong, and wrong in a way that would quietly corrupt the whole
Atlas.

Anthropic's pricing page is the single best source on Earth for what Anthropic
charges. It is a *terrible* source for whether Claude is the best model for
refactoring a legacy Django monolith. Same source. Same tier. Opposite
reliability — because the claim type changed.

Meanwhile a Reddit thread is weak evidence for a context-window number and
**the strongest evidence available** for "this harness silently truncates
context at 60% and you only notice three hours in." No vendor will ever
document that. No benchmark measures it. Community reporting is not a
downgrade there; it is the correct instrument.

So the framework has two independent dimensions:

| Dimension | Question it answers |
|---|---|
| **Source class (A–D)** | What *kind* of artifact is this? |
| **Claim type (S/M/X/C/T/F)** | What *kind* of assertion is being made? |

Authority is the **intersection** of the two, defined in §3. A source is never
"reliable" in the abstract. It is reliable *for a claim type*.

---

## 1. Source classes

Source class describes the artifact's nature and provenance. It is descriptive,
not a quality score.

### Class A — Primary / official

The entity's own authoritative publications about itself.

- Vendor documentation, API references, pricing pages, model cards
- Official changelogs, release notes, deprecation notices
- Official repositories, licenses, `LICENSE` and `pyproject.toml`-level facts
- Official status pages and incident reports
- Terms of service and data-handling policies

**Properties:** definitive for self-facts, structurally non-independent, subject
to silent revision, frequently incomplete about limitations.

**Mandatory flags:** `self_interested: true` on any claim about quality,
performance, or comparison.

### Class B — Independent structured evaluation

Work by a third party with a stated method that another party could repeat.

- Peer-reviewed and preprint academic papers
- Benchmark suites and their published harnesses (SWE-bench, Terminal-Bench, etc.)
- Independent evaluation orgs and labs
- Engineering blogs **that publish methodology and raw numbers** — methodology is
  the qualifier, not the domain name
- Reproducible open-source evaluations
- Third-party latency/uptime/price telemetry

**Properties:** the strongest evidence for measurable properties; often narrow;
frequently stale; vulnerable to contamination and to optimizing-for-the-metric.

**Required sub-fields:** `method_published`, `harness_version`,
`contamination_risk`, `run_by`, `funded_by`.

### 1.5 Methodology Depth — how Class B is actually assessed

*Added v1.1, 2026-08-04, after the Artificial Analysis evaluation nearly
produced a wrong admissibility verdict.*

> **Principle: capture depth is an implementation detail. Methodology depth is a
> research property. The Atlas evaluates the latter.**

Which page we happened to fetch first is an artefact of how we searched. It has
no bearing on whether a source has a methodology. Assessing admissibility from
the capture page therefore measures our search path, not the source.

**The rule:** a source's class is determined from the **deepest available
methodology documentation**, not from the page where the claim was found.

This cuts both ways, and the second direction is the dangerous one:

| Failure mode | Consequence |
|---|---|
| **False rejection** — a good source's landing page lacks detail | A usable independent source is wrongly excluded |
| **False acceptance** — a source has a page *titled* methodology with no methodology *content* | A weak source enters the corpus wearing a Class B label |

The observed case was a near-miss on the first. The second is more damaging at
scale, because nothing downstream re-checks it.

**Procedure — mandatory before assigning Class B:**

1. From the capture page, follow every link plausibly leading to methodology
   (`/methodology`, `/about`, `/how-we-*`, `/faq`, linked papers, repository
   `README`).
2. Assess completeness (§1.6) at the **deepest** page found.
3. Record `methodology.assessed_at_url` — the page actually used — and
   `methodology.depth_searched` (how far the search went).
4. If methodology is spread across several pages, record **all** of them and
   which supplied each completeness element.
5. If the search terminates without finding methodology, record
   `methodology.searched: true` and `found: false`. **That is a finding, not an
   omission** — it means the source claims independence without showing its work.

**Stopping rule:** search terminates at depth 3 from the capture page, or when a
page satisfying §1.6 is found, whichever comes first. Depth is recorded so a
reviewer can extend it.

### 1.6 Class B completeness checklist

A methodology page existing is not a methodology being published. Seven elements
are assessed; three are **core** and mandatory.

| # | Element | Core? | Question it answers |
|---|---|---|---|
| 1 | **Methodology disclosure** | ✅ core | Is there a stated procedure at all? |
| 2 | **Measurement procedure** | ✅ core | What exactly was measured, and how? |
| 3 | **Statistical treatment** | ✅ core | Mean, median, percentile? Over what window? |
| 4 | Sampling strategy | | What was sampled, how often, how selected? |
| 5 | Update cadence | | How current is a published figure? |
| 6 | Limitations | | What does the publisher say it cannot measure? |
| 7 | Reproducibility | | Could a third party repeat it? Code, data, or procedure released? |

**Grading:**

| Grade | Requirement | Admissibility |
|---|---|---|
| **B-full** | All 3 core + ≥3 supporting | Class B, no restriction |
| **B-partial** | All 3 core + 1–2 supporting | Class B, flagged `methodology_partial`; cannot alone carry a claim at `high` confidence |
| **Fails Class B** | Any core element missing | **Reclassified Class E — pointer only.** Not a downgrade to C: C is field reporting, which this is not |

Element 6 (limitations) carries disproportionate weight in practice. A publisher
who states what their measurement cannot do is demonstrating the self-awareness
that separates measurement from marketing, and its **absence** is the most
common tell of a promotional benchmark.

**Recording:** every Class B source carries a `completeness` block listing which
of the seven were found and where.

### Class C — Field reporting / community evidence

Practitioner accounts of real-world use.

- GitHub issues, discussions, and post-mortems
- Reddit, Hacker News, X, Discord, forums
- Practitioner blog posts without formal methodology
- Conference talks, changelogs of downstream projects, migration write-ups
- Sustained-use reports from identifiable long-term users

**Properties:** the *only* source for friction, failure modes, and whether a
thing survives contact with a real codebase. Noisy, non-representative,
recency-biased, vulnerable to hype cycles and astroturfing.

**Required sub-fields:** `sample_type` (single-report / recurring-theme /
consensus), `population` (who these users are), `time_window`,
`hype_risk`.

Class C is graded on **convergence**, not volume. One thoughtful post-mortem
from someone who shipped with the tool for six months outweighs forty launch-week
reactions. Fifty independent reports of the same specific failure is strong
evidence; fifty upvotes on one report is one report.

### Class D — First-party experiment

Experiments run inside this project, per the protocol in METHODOLOGY.md §7.

- Standardized task suites executed against models, harnesses, and stacks
- Cost, token, latency, and intervention accounting
- Qualitative output review against a fixed rubric

**Properties:** the only class where we control the method fully and can hold
conditions constant across subjects. Small-n, single-operator, and at permanent
risk of our own bias.

**Required sub-fields:** `experiment_id`, `runs`, `seeds`, `harness_config`,
`raw_output_ref`, `operator`, `preregistered` (bool).

Class D is **not** automatically superior to B. An n=1 unblinded run by an
interested party is weaker than a well-run public benchmark, and the Atlas says
so. D earns its weight through repetition, preregistration, and publishing
failures.

### Class E — Derived / secondary aggregation

Added because the scan will otherwise force it in through the back door.

- News articles, newsletters, and roundups reporting on primary sources
- Aggregators, leaderboard mirrors, "awesome" lists, model directories
- LLM-generated summaries, including our own

**Rule:** Class E is a **pointer, never a citation**. It may be used to *find* a
primary source and must be replaced by that source before a claim ships. A claim
whose only support is Class E does not render.

This rule exists because secondary aggregation is how a single vendor
press-release number becomes "widely reported" without anyone re-verifying it.

---

## 2. Claim types

Every claim in `/data` declares a `claim_type`. This determines which sources can
support it and how fast it decays.

| Code | Type | Examples | Decays in |
|---|---|---|---|
| **S** | Specification | price, context window, license, availability, rate limits, release date, API surface | 30–90 days |
| **M** | Measurement | benchmark score, latency, throughput, cost-per-task, token efficiency | 90–180 days |
| **X** | Experience | reliability, failure modes, DX, autonomy under load, maintenance burden | 90–180 days |
| **C** | Comparative judgment | "better than", "preferable for", "not suitable for" | 60–120 days |
| **T** | Trend / adoption | market share, momentum, community growth, hiring signal | 90 days |
| **F** | Forecast | "likely to", "expect that" | Always labeled opinion; never a fact |

Decay windows are defaults; per-entity overrides live in the entity's
`review_cadence`. Anything touching a model in active release rotation gets the
short end of its range.

---

## 3. The authority matrix

Which source class is *sufficient*, *supporting*, or *inadmissible* for which
claim type.

| | **A** Official | **B** Independent | **C** Community | **D** First-party | **E** Derived |
|---|---|---|---|---|---|
| **S** Specification | **Authoritative** | Corroborating | Contradiction signal only | Corroborating | Pointer only |
| **M** Measurement | Admissible, flagged `self_reported` | **Authoritative** | Anomaly signal only | Supporting | Pointer only |
| **X** Experience | Inadmissible | Supporting | **Authoritative** (on convergence) | Supporting | Pointer only |
| **C** Comparative | **Inadmissible** | Supporting | Supporting | Supporting | Pointer only |
| **T** Trend | Supporting, flagged | Supporting | **Authoritative** (on convergence) | Inadmissible | Pointer only |
| **F** Forecast | — | — | — | — | — |

Reading the matrix:

- **Authoritative** — this class alone can carry the claim.
- **Corroborating / Supporting** — raises confidence, cannot carry the claim alone.
- **Contradiction / anomaly signal** — cannot establish the claim, but *can*
  trigger re-verification. A pile of users reporting a different rate limit than
  the docs state does not overturn the docs; it opens a ticket.
- **Inadmissible** — must not appear as the basis of the claim.

Two consequences worth stating plainly:

1. **No comparative claim may rest on official documentation.** Vendor A's
   benchmark table comparing itself to Vendor B is a marketing artifact. It may
   be *reported as a vendor claim* (an S-type claim about what the vendor
   asserts) but never as evidence that the comparison is true.
2. **No experience claim may rest on official documentation.** Documentation
   describes intent. Experience claims describe behavior. These diverge, and the
   divergence is often the most useful thing on the page.

---

## 3.5 The corroboration model — what a second source can and cannot buy

The authority matrix says which class may *support* a claim type. It does not
say whether a second source adds **independent** support. Those are different
questions, and conflating them is how a corpus manufactures false confidence.

| Type | Authority model | A second source buys |
|---|---|---|
| **S** Specification | **Constitutive** — the vendor does not report the price, it *constitutes* it | Transcription assurance only. Catches stale captures and typos. **Never independent corroboration.** |
| **M** Measurement | **Observational** — an external fact exists to observe | Genuine corroboration, by replication |
| **X** Experience | Observational, convergent | Corroboration across independent practitioners |
| **T** Trend | Observational, convergent | Corroboration on convergence |
| **C** Comparative | **Interpretive** — synthesised, never observed | Nothing. Attributed, not corroborated |
| **F** Forecast | Interpretive | Never published as fact |

Three situations look identical in a source list and are not:

- **Corroboration** — independent causal access to the fact. Real.
- **Duplication** — two sources, one publisher. A pricing page and an overview
  agreeing is one source with two URLs.
- **Derivation** — two publishers, one upstream of the other. A reseller quoting
  a vendor. More dangerous than duplication, because the names differ.

**Rule.** Support counts only where a source has a causal path to the fact that
does not pass through another counted source.

**Consequence for reading this corpus.** A type-S claim with one source is
*sole authority* — correct, not fragile. A type-M claim with one source is
*under-corroborated* — genuinely fragile. Marking both "1 source" tells you
nothing. See [DEPENDENCE.md](DEPENDENCE.md).

### `construct_stable` — the axis corroboration cannot reach

A stable, replicable measurement of the wrong thing replicates perfectly.

Two instances already in this corpus: TTFT measured as request-to-first-token
includes the entire reasoning phase for a reasoning model; SWE-bench Verified
filters instances for solvability, so the score is partly selected by the thing
it measures.

Where `construct_stable: false`, replication is not the remedy and a replication
count is misleading. The honest state is **replication will not fix this**.

---

## 4. Independence and bias flags

Orthogonal to class. Every source record carries these:

| Flag | Meaning |
|---|---|
| `self_interested` | Source benefits commercially/reputationally if the claim is believed |
| `funded_by` | Named funder of the evaluation, if any |
| `early_access` | Author received preview access, credits, or hardware |
| `affiliation` | Author's employer or project affiliation relevant to the claim |
| `promotional_context` | Published as launch material, keynote, or marketing |
| `astroturf_risk` | Community source with signs of coordinated promotion |
| `contamination_risk` | Benchmark plausibly present in training data |
| `metric_gaming_risk` | Subject is known to optimize specifically for this metric |
| `anonymous` | Author unidentifiable — caps contribution to `weak` |

Flags do not disqualify a source. They travel with it, are visible in the UI at
the point of use, and reduce computed confidence. A flagged source with a
published method beats an unflagged source with none.

---

## 5. Confidence — computed, not asserted

Claim confidence is **derived** from evidence, never hand-set. Hand-set
confidence is how a framework like this dies: the labels drift until they mean
"how much the author liked writing the sentence."

Inputs:

1. **Admissibility** — is there at least one authoritative-class source for this
   claim type? If no → confidence caps at `low` regardless of volume.
2. **Corroboration** — count of *independent* supporting sources. Independent
   means not derived from each other; three articles citing one press release
   count as one.
3. **Convergence** — for X/T claims, do independent reports describe the same
   specific behavior?
4. **Conflict** — presence and severity of contradicting evidence.
5. **Freshness** — age relative to the claim type's decay window.
6. **Flag load** — weighted count of bias flags on supporting sources.

Output states:

| Confidence | Meaning |
|---|---|
| `high` | Authoritative source, corroborated, fresh, no unresolved conflict |
| `moderate` | Authoritative but uncorroborated, **or** strong convergent non-authoritative evidence |
| `low` | Single source, or aging, or unresolved conflict, or heavy flag load |
| `contested` | Credible evidence on both sides; the conflict *is* the finding |
| `unknown` | We looked and could not establish it — a publishable state |

`contested` and `unknown` are first-class outcomes. A page that reports
"benchmarks and sustained users disagree sharply about this, here is why" is more
useful than one that picks a side to seem decisive.

---

## 6. Conflict handling

When sources disagree, the Atlas records the disagreement as a structured object
rather than resolving it silently. Required fields: the positions, their
sources, and a `likely_cause` drawn from a controlled vocabulary:

`version_drift` · `config_difference` · `harness_difference` ·
`contamination` · `measurement_definition` · `sample_bias` ·
`time_window` · `incentive` · `unexplained`

`unexplained` is permitted and honest. Fabricating a tidy explanation is not.

Resolution rules: prefer the source whose *conditions are stated*; prefer the
more recent when the subject changed under it; never average incompatible
measurements into a single number.

---

## 7. Capture and archival

The web rots, and vendor pages are edited in place without notice — this
ecosystem's most-cited facts live on pages designed to change silently.

Every source is captured at ingestion with: canonical URL, publisher, author,
publication date, retrieval date, content hash, archive URL, and a verbatim
excerpt of the passage supporting the claim.

- **Excerpt, not summary.** The exact text that supports the claim, quoted, so a
  future reviewer can check our reading without refetching.
- **Content hash** so silent edits are detectable on re-verification.
- **Archive URL** (web.archive.org or local snapshot) for every Class A and B
  source.
- Excerpts stay within fair-use length. We cite and quote narrowly; we do not
  mirror documentation.

Re-verification compares the hash. A changed hash marks every dependent claim
`needs_review` automatically — the correct default, since the change may be
exactly the fact we care about.

---

## 8. Source record shape

Canonical definition lives in `data/schema/source.schema.json`. Shape:

```yaml
id: src-anthropic-pricing-2026-08-03
url: https://…
canonical_url: https://…
archive_url: https://web.archive.org/…
title: …
publisher: anthropic
author: null
class: A                      # A | B | C | D | E
published: 2026-07-14         # null if unknown — never guessed
retrieved: 2026-08-03
content_hash: sha256:…
excerpt: "…verbatim passage…"
flags: [self_interested]
methodology:                  # required for class B and D
  published: true
  url: …
  contamination_risk: low
notes: …
```

---

## 9. Rules that are enforced by the build

Not guidelines. Validation failures.

1. Every claim has ≥1 source admissible for its claim type.
2. No claim ships with only Class E support.
3. Every Class B and D source has a methodology reference.
4. Every source has `retrieved`, `content_hash`, and an `excerpt`.
5. Comparative (C-type) claims sourced only to Class A fail the build.
6. Confidence is computed; a hand-written confidence field fails the build.
7. Any claim past its decay window renders with a staleness state, and expired
   claims do not render as current.
8. Every benchmark-derived claim names the harness and version.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-08-04 | Added §1.5 Methodology Depth and §1.6 the Class B completeness checklist, after the Artificial Analysis evaluation showed admissibility was being assessed at an arbitrary capture depth. A source failing a core element is reclassified Class E, not Class C. |
| 1.0 | 2026-08-03 | Initial framework. Split source class from claim type; added Class E; made confidence computed. |
