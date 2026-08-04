# RESEARCH METHODOLOGY

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Depends on:**
[CONSTITUTION.md](CONSTITUTION.md), [SOURCES.md](SOURCES.md)

How research actually gets done here: what triggers it, how sources are
gathered, how claims move from draft to published to retired, and how the whole
corpus stays current without a full rewrite every quarter.

The design goal is a process that a stranger — or a future agent with no memory
of this session — can execute and reach the same result.

---

## 1. The unit of work is a claim, not a page

Pages are compiled views. The atomic unit is a **claim**: one assertion, one
claim type, its evidence, its confidence, its dates.

This matters more than it sounds. Page-centric research produces documents that
must be rewritten wholesale when one number changes, so they aren't, so they rot.
Claim-centric research means a price change touches one record and propagates to
every page that references it.

**Rule:** if you find yourself editing prose to change a fact, stop. The fact was
in the wrong place.

---

## 2. Research cycle

Five phases. Each has an exit condition; work does not advance without it.

```
INTAKE → SCAN → DEEP RESEARCH → SYNTHESIS → REVIEW → (publish) → MAINTENANCE
                    ↑                                                  │
                    └──────────────────  re-verification  ─────────────┘
```

### 2.1 Intake

Something enters the Atlas's field of view: a new model, a harness, a provider, a
pricing change, a paper, a shift in community sentiment.

Every candidate is registered in `data/entities/` as a **stub** with: stable ID,
name, aliases, category, canonical URL, first-seen date, and status
`stub`. Nothing more.

Stubs are cheap and are the mechanism that prevents recency bias — the thing you
heard about today and the thing you heard about in March get the same treatment.

**Exit:** entity has a stable ID and a category. If it doesn't fit a category,
that's a taxonomy finding — log it in `RESEARCH.md`, don't force the fit.

### 2.2 Scan

Bounded, breadth-first. For each entity: what is it, who makes it, what does it
compete with, what does it cost, is it alive, and which of our decision questions
does it touch.

A scan is complete when the entity can be **placed** — not when it is understood.
Placement means: category assigned, relationships to other entities recorded,
a rough sense of whether it warrants deep research.

Deliberately time-boxed. The failure mode of scanning is falling into one
interesting entity and emerging four hours later with one excellent page and no
map. Scan produces the map.

**Exit:** entity classified, relationships recorded, `depth_priority` assigned
(P0–P3).

### 2.3 Deep research

Per-claim, per-entity. Governed by the **source ladder** (§3).

**Exit:** every claim on the entity has admissible evidence per the authority
matrix, computed confidence, and a verified date. Claims we could not establish
are recorded as `unknown` — not omitted.

### 2.4 Synthesis

Claims become answers. This is where interpretation and opinion are permitted,
and where they must be labeled as such (Constitution §3).

Synthesis is also where **the decision question is validated**: if the assembled
claims do not actually let a reader decide, the research is incomplete regardless
of how many claims exist.

**Exit:** every narrative assertion either (a) references a claim ID, (b) is
labeled `interpretation` with its supporting claim IDs, or (c) is labeled
`opinion` with author and date.

### 2.5 Review

Gates in §8. Nothing publishes without passing them.

### 2.6 Maintenance

Continuous, scheduled, and event-driven. §6.

---

## 3. The source ladder

Order of search for any claim. Working out of order is the single most common way
to import a false consensus.

1. **Primary first.** The vendor's own docs, repo, changelog, pricing page.
   Establishes S-type facts and gives you exact terminology for later searches.
2. **Independent measurement second.** Benchmarks, papers, third-party telemetry.
   Note who ran it and whether the method is published.
3. **Field reporting third.** GitHub issues before social media — issues are
   specific, versioned, and attached to reproductions. Then long-form
   practitioner accounts. Then discussion threads.
4. **First-party experiment last**, and only when the first three leave a gap
   that matters to a decision. Experiments are expensive; run them where they
   change an answer.

### Anti-anchoring rules

- **Never source a claim from the first result.** Minimum two independent
  retrievals for any published claim, three for comparative claims.
- **Search for the negative case explicitly.** For every entity, run searches
  designed to surface failure: `<entity> problems`, `<entity> limitations`,
  `<entity> migrated away`, `<entity> issues`. Launch coverage is
  systematically positive; issue trackers are systematically honest.
- **Never let a secondary source stand in for a primary one.** If a newsletter
  says the price is X, go read the pricing page. (SOURCES.md §1, Class E.)
- **Record what you searched**, not just what you found. Null results are data
  and prevent the next person repeating the search.

---

## 4. Community sentiment method

Class C evidence is the Atlas's differentiator and its biggest integrity risk.
Cherry-picking threads produces whatever conclusion you started with. The
protocol:

**Sample, don't browse.**
- Define the population before reading: which subreddits/repos/forums, what time
  window, what query.
- Read the top N by engagement *and* the most recent N. Hype lives in the first;
  reality lives in the second.
- Record the query and window in the source record so the sample is reproducible.

**Weight by durability, not volume.**
- A report from someone six months into daily use outweighs launch-week
  reactions by a wide margin.
- Distinguish *first impressions* from *sustained use*. Tag every Class C source
  with `time_window`. Most online enthusiasm is week one; most abandonment is
  never posted about at all.

**Look for convergence on specifics.**
- "It's amazing" from 200 people is one data point about sentiment.
- "It silently drops the last file in a multi-file edit" from 8 people is a
  finding.
- Only specific, reproducible, independently-arrived-at reports become claims.

**Separate hype from adoption.** Explicit signals we track:
- Sustained issue and PR activity vs. launch spike
- Downstream dependents and integrations built by others
- Migration posts *away* from a tool (strongest negative signal available)
- Whether enthusiastic accounts have any stake in the project

**Correct for structural bias.** These communities over-represent early
adopters, English speakers, greenfield projects, and people with time to post.
They under-represent enterprise, legacy codebases, and everyone quietly getting
work done. Note this on any T-type claim.

---

## 5. Benchmark handling

Benchmarks enter the graph as **measurements with conditions attached**, never as
rankings.

Required for every benchmark-derived claim:

| Field | Why |
|---|---|
| `benchmark_id` + version | Suites change; scores across versions aren't comparable |
| `harness` + version | The scaffold often matters more than the model |
| `run_by` | Self-reported vs. independent is a different claim |
| `date` | Contamination and model updates both move with time |
| `config` | Thinking budget, tool access, retries, temperature, pass@k |
| `contamination_risk` | Public benchmarks leak into training data |

Rules:
- Scores from different harnesses are **never** placed in the same column
  without an explicit warning annotation.
- Vendor-reported scores render with a persistent `self-reported` marker.
- Every benchmark gets a **construct-validity note**: what it actually measures,
  and what it is routinely misread as measuring. This note is attached to the
  benchmark entity and travels with every citation of it.
- A benchmark's saturation state is tracked. Saturated benchmarks stop
  discriminating and must be labeled, not quietly dropped.

---

## 6. Maintenance and re-verification

### Scheduled

Every claim has a `review_cadence` from its claim type (SOURCES.md §2), tightened
per-entity for fast-moving subjects. A nightly job computes freshness and
enqueues due claims.

| State | Condition | Behavior |
|---|---|---|
| `fresh` | within cadence | renders normally |
| `aging` | 100–150% of cadence | renders with a subtle date marker |
| `stale` | 150–300% | renders with explicit "as of" treatment; queued |
| `expired` | >300% | does not render as current; page shows a gap |

Expiry causing a visible gap is intentional. A gap is honest; a stale number
presented as current is not.

### Event-driven

Re-verification triggers ahead of schedule on: content-hash change on a cited
source, a new model or version release from a tracked vendor, a pricing change,
a benchmark suite update, a deprecation notice, or a spike in community reports
contradicting a claim.

### Monthly cycle

1. Run freshness report; triage `stale` and `expired`.
2. Re-verify all S-type claims for P0 entities (prices and limits move quietly).
3. Sweep tracked sources for new releases; intake new entities as stubs.
4. Refresh community sentiment on P0/P1 entities using the §4 protocol.
5. Import new benchmark results; recompute affected scores.
6. Recompute confidence across the graph.
7. Publish a dated changelog of what changed and what it invalidated.

The changelog is public and is itself a useful artifact — a month-by-month record
of how this ecosystem actually moved.

---

## 7. First-party experiments (Class D)

An experiment is a **preregistered, versioned, reproducible procedure**. Anything
less is an anecdote and is labeled one.

### Protocol

1. **Preregister.** Write the question, the procedure, the metrics, and — before
   running — what result would change our recommendation. A predicted outcome is
   recorded. This is the guard against post-hoc storytelling.
2. **Fix conditions.** Exact model IDs, harness versions, prompts, repo state,
   seeds where available, date, region, and pricing snapshot.
3. **Run.** Multiple runs where nondeterminism matters. Single runs are labeled
   n=1 and cannot carry a comparative claim.
4. **Instrument.** Wall-clock time, input/output/cached tokens, cost at
   snapshot pricing, human interventions (count and type), retries, failures.
5. **Score.** Against a rubric fixed *before* seeing outputs (EVALUATION.md).
6. **Publish everything.** Prompts, configs, raw outputs, transcripts, and
   failures. Especially failures.

### Standing experiment suite

Versioned task definitions in `data/experiments/`, designed for re-running
against future models so results become a longitudinal dataset rather than a
snapshot:

- **Greenfield app** — small full-stack app from spec
- **Frontend fidelity** — polished landing page from a design brief
- **Large-repo comprehension** — answer questions requiring cross-file reasoning
- **Refactor under constraint** — non-trivial refactor without breaking tests
- **Debug an unfamiliar break** — planted bug, no pointer to location
- **Long-horizon autonomy** — multi-hour task, measuring intervention rate
- **Agent construction** — build a working agent with tools
- **Context retrieval at depth** — retrieval and reasoning at large context

Metrics collected identically across all: time, tokens, cost, task success,
quality score, defect count, intervention count, autonomy duration.

### Honesty constraints

- Prompts are held constant across subjects. Prompt tuning per-subject is a
  different experiment and is labeled one.
- The operator's expectations are recorded pre-run.
- Inconclusive results publish as inconclusive.
- No experiment is re-run until it gives a nicer answer. Re-runs are additive
  to the dataset, never replacements.

---

## 8. Review gates

Automated and manual gates before publication.

**Automated (build fails):**
1. Every claim has admissible evidence for its claim type
2. No Class-E-only claims
3. Every source has retrieval date, hash, excerpt
4. No hand-set confidence values
5. No orphan facts in prose (numbers not interpolated from the graph)
6. Every narrative assertion resolves to a claim ID, or is labeled
   interpretation/opinion
7. No entity referenced that doesn't exist in the graph
8. Comparative claims have ≥2 independent supporting sources
9. Expired claims are not rendered as current

**Manual (editorial):**
10. **Decision test** — does this page change what someone does?
11. **Adversary test** — could a well-informed skeptic of this recommendation
    read the page and feel their position was represented fairly?
12. **Steelman test** — is the strongest case for the alternative present?
13. **Persona test** — is the recommendation scoped to who it's for?
14. **Filler test** — remove any section that doesn't improve understanding.
15. **Freshness test** — would this page embarrass us in six months, and does its
    metadata make that self-evident when it happens?

---

## 9. Known methodological limitations

Stated because a methodology that doesn't name its weaknesses is marketing.

- **Single-operator bias.** Experiments are run by one team with one working
  style on a limited set of codebases. Class D results generalize less than
  they appear to.
- **Community sampling is not representative.** §4 mitigates; it does not solve.
- **English-language and Western-platform bias** in source selection, which
  materially under-covers parts of the ecosystem — notably the Chinese
  open-weight model community, where much primary discussion happens off the
  platforms we sample.
- **Vendor opacity.** Routing, quantization, and silent model updates on hosted
  endpoints mean "the same model" may not be the same model between runs. We
  flag where we suspect this and often cannot prove it.
- **Closed-weight vendors are structurally unverifiable on token billing.**
  Established empirically by the M4 studies, not assumed. Anthropic and Google
  publish no offline tokenizer, so the unit their prices are denominated in
  cannot be independently measured without a funded API account; and at least one
  vendor publishes subscription allowances only as relative multipliers with no
  absolute base. Prices are published to five significant figures; the units are
  not. **We can report what these vendors charge and cannot verify what a charge
  corresponds to.** See `research/experiments/M4-POST-STUDY-REVIEW.md` §1 L1.
- **We cannot test at enterprise scale.** Claims about large-org adoption rest
  on Class B/C evidence and are weaker than our claims about individual use.
- **Recency asymmetry.** New things get researched because they're new. We
  counter with scheduled re-verification of incumbents, imperfectly.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial methodology. |
