# RESEARCH STATE

**Status:** live document · **Last updated:** 2026-08-03

Where the research actually stands: what exists, what is missing, and what we
know we don't know. Updated every cycle. Once the pipeline is built, the gap
register here is **generated** from the graph (`unknown` claims + `not_scored`
dimensions); until then it is maintained by hand and marked as such.

---

## 1. Corpus status

*Updated at the M5 population pass, 2026-08-04.*

| | Count | Note |
|---|---|---|
| Entities in `/data` | 16 | 4 model, 2 access, **2 harness**, **1 protocol**, 7 institution |
| Entities identified | ~120 | `research/scan-2026-08-03.md`, unverified |
| **Published claims** | **~45** | All S-type except one T-type; all from Class A sources |
| Draft claims | 5 | Reduced-fidelity sources — cannot publish |
| Captured sources | 9 | 5 verbatim, 4 `tool_extracted` |
| **First-party experiments run** | **2** | `exp-tokenizer-normalization-v1`, `exp-normalized-cost-v1` |
| Recommendation deltas published | 5 | `research/RECOMMENDATION-DELTAS.md` |

**Structural unblock achieved in M5:** L3 harness entities now exist, so a stack
can compose across model → access → harness for the first time. The engine can
be run end to end once dimension scores exist.
| Capabilities defined | 27 | |
| Objectives defined | 5 | Metric sets declared; **zero metrics populated** |
| Usage profiles | 4 | **All `assumed`, none measured** |
| Scored entities | **0** | Scoring inputs absent — see §1.1 |
| Class B sources | **0** | |
| Class C sources | **0** | |
| Class D experiments | 0 | Suite designed, none run |
| Decision pages | 0 | |
| Gold-standard exemplar pages | 1 | `atlas/entities/model/claude-sonnet-5.mdx` |

### 1.1 Why nothing is scored

Not an oversight. EVALUATION §3 requires D1/D2/D3 to be scored *via* a named
harness; SOURCES §3 makes Class A inadmissible for comparative claims. With only
vendor documentation captured, **every input to every dimension score is
missing**. `scores: []` is the correct state, and the exemplar page says so in
place of a rating.

The corpus can currently tell you precisely what things *are*. It cannot yet tell
you whether any of them is *good*.

**Zero published claims is the correct state at the end of Milestones 1–2.** M1
built the machine that makes claims trustworthy; M2 proved it answers real
questions. Filling it before either existed is the failure mode the whole project
was structured to avoid.

**M2 reset the research order.** Priority now follows the query set
([QUERIES.md](QUERIES.md) §9) rather than category coverage:
usage profiles → pricing as temporal facts → frontend fidelity measurement →
intervention-rate measurement → continuous measurements under controlled
conditions. Comprehensive per-tool feature coverage is deliberately *not* in the
top five — the questions readers ask do not require it.

---

## 2. Research priorities

`depth_priority` on each entity, driving research order and review cadence.

| Tier | Criterion | Cadence |
|---|---|---|
| **P0** | Appears in a top-10 question; a majority of readers will consider it | 30 days |
| **P1** | Real adoption; changes an answer for at least one persona | 60 days |
| **P2** | Notable, niche, or emerging; worth placing | 120 days |
| **P3** | Tracked for completeness; stub only | 365 days |

Milestone 2 targets **~25 P0 entities across all nine layers** — deliberately
not 25 models. A stack has nine choices in it, and covering one layer deeply
while leaving the others as stubs would produce exactly the model-obsessed
content this project exists to replace.

---

## 2.5 The Research Program

Since 2026-08-03 the Atlas runs a formal research program:
**[`research/questions/`](research/questions/README.md)**.

Findings that generate original questions are written up as ranked RQ files —
research question · why it matters · current evidence · missing evidence ·
proposed experiments · expected impact · effort · confidence — and **ranked by
Expected Recommendation Impact, not novelty**.

Six flagship tracks produce longitudinal first-party datasets rather than one-off
results:

| Track | Question |
|---|---|
| [RQ-01](research/questions/RQ-01-tokenizer-normalization.md) | Are per-token prices comparable across vendors? |
| [RQ-02](research/questions/RQ-02-throughput-constrained-autonomy.md) | Does throughput bind before price or quality? |
| [RQ-03](research/questions/RQ-03-cache-economics.md) | What cache hit rates do harnesses actually achieve? |
| [RQ-04](research/questions/RQ-04-intervention-rate.md) | How much human intervention per unit of completed work? |
| [RQ-05](research/questions/RQ-05-harness-effect-size.md) | How much of observed quality is the harness, not the model? |
| [RQ-06](research/questions/RQ-06-real-world-feature-cost.md) | What do the "free" parts of a request actually cost? |

**Seven of the ten open RQs cannot be answered from any public source.** They are
gaps in the field, not gaps in our reading — which is the point at which this
project stops aggregating and starts researching.

The program also **declines** questions explicitly (README §3). Under
CONSTITUTION §14 a program that only adds work eventually lies about its own
coverage.

---

## 3. Open questions

### 3.1 Questions about the ecosystem

Ordered by how much the answer would change what people do.

| # | Question | State | Blocked on |
|---|---|---|---|
| Q1 | Does AI-assisted development actually make teams faster, and at what cost in review burden? | `contested` | Class B studies; conflicting survey evidence (scan F5) |
| Q2 | Why do benchmark scores for the same model disagree so widely, and which should you believe? | `unknown` | Primary harness/leaderboard documentation (scan F4) |
| Q3 | Does the harness matter more than the model? | `unknown` | Class D experiments holding each constant |
| Q4 | What does a month of real agentic development cost, including failed runs and rework? | `unknown` | Class D instrumentation |
| Q5 | Can a subscription be beaten by metered API access, and at what usage? | `unknown` | Verified pricing + real token accounting |
| Q6 | How maintainable is AI-generated code after six months? | `unknown` | Nobody appears to measure this; longitudinal design needed |
| Q7 | Is the open-weight gap closed for real coding work? | `unknown` | Independent evaluation; vendor claims inadmissible for C-type |
| Q8 | What is the actual security exposure of agents with system access and third-party extensions? | `unknown` | Security research; scan surfaced enough to change the rubric |
| Q9 | Index-first or agentic search for large repositories? | `unknown` | Class B evidence + Class D on a large repo |
| Q10 | Is parallel multi-agent development worth its coordination cost? | `unknown` | Class D; strong community claims, no measurement found |

Q1, Q2, and Q6 are the three where the Atlas could plausibly produce something
that does not currently exist anywhere. Q6 in particular has no incentivized
publisher: vendors won't measure it, and it takes six months to answer.

### 3.2 Questions about our own method

- **How do we detect silent model changes behind a stable endpoint name?** A
  provider can change quantization or routing without notice, invalidating every
  measurement. We currently have no detection mechanism. Candidate: a small
  fixed canary suite re-run on a schedule against stable endpoints — a Milestone
  3 design task.
- **How do we keep Class C sampling honest at scale?** METHODOLOGY §4 is
  executable by a careful human. It has not been tested under volume.
- **When does an ordinal 5-point scale stop discriminating?** If most P0
  entities score 4 on most dimensions, the scale has failed and needs anchors
  re-cut. Watch during Milestone 2.
- **What is the review cost of the whole system?** If maintenance exceeds
  capacity, coverage must shrink (CONSTITUTION §14). We don't yet know the real
  per-entity cost. Measure it during Milestone 2 and let it set the coverage
  ceiling.

### 3.3 Open taxonomy and framework questions

Carried from TAXONOMY.md §7 and EVALUATION.md §7 — not repeated here. Live
items: `app_builder` layer placement · skills as interop vs context ·
subscription-plan volatility · model-family identity across architecture changes
· whether `per-student`'s learning-value objective belongs in the rubric.

---

## 4. Gap register *(manual until generated)*

Known holes, so they cannot be mistaken for coverage.

**Structural**
- No entity in `/data` yet — everything downstream is unbuilt.
- No source capture tooling; archival and hashing are specified, not implemented.
- No validation runner; the schemas exist and nothing enforces them yet.

**Evidential**
- No primary source has been retrieved for any claim.
- No Class D experiment has been run.
- All pricing is unverified.
- Non-English sources uncovered (METHODOLOGY §9).
- Enterprise-scale evidence absent and likely to remain weak.

**Coverage**
- L8 (assurance) and L7 (orchestration) are the least-covered layers relative to
  their decision importance.
- Practice and anti-pattern entities (L9) have no evidence base at all.
- Local/self-hosted economics asserted everywhere, measured nowhere.
- Failure and abandonment evidence under-sampled — negative-case searches not yet
  run.

---

## 5. Conflict register *(manual until generated)*

| Conflict | Positions | Likely cause | Status |
|---|---|---|---|
| **RG-001 — Sonnet 5 tokenizer** | Pricing page: newer tokenizer applies to "Claude 4.7 and later models". Models overview: tooltip attached to Fable 5; "Sonnet 4.6 and earlier" use the previous one. Sonnet 5 named in neither. | `unexplained` | **Open — Class A vs Class A, same vendor.** Resolving changes effective cost by up to ~30%, more than the entire introductory discount. |
| SWE-bench Verified figures for nominally comparable subjects | six divergent values seen in one session | `harness_difference` + `measurement_definition` + `incentive` | Open — becomes decision page Q2 |
| Adoption vs. trust vs. productivity | near-universal adoption; falling trust; plateauing self-reported gains | `measurement_definition` + `sample_bias` | Open — becomes decision page Q1 |
| Registry scale vs. artifact quality | catalogs in the millions; audits reporting low quality and injection risk | `sample_bias` + `incentive` | Open — drove D13 |

All three are Class E observations. They are recorded as *research targets*, not
as findings, and none may be published until re-established from primary sources.

---

## 6. Standing research agenda

**Continuous** — release monitoring for tracked institutions · pricing watch on
P0 entities · community sentiment sampling per METHODOLOGY §4 · benchmark
leaderboard drift.

**Next pass (M3 continued)** — in value-of-information order, revised by what the
first pass found:

1. **`exp-tokenizer-normalization-v1`** — tokenize a fixed corpus with each
   vendor's tokenizer. Cheap, fast, and it unblocks *all* cross-vendor price
   comparison, which is currently invalid (F1). Nobody appears to publish this.
2. **Subscription pricing** — the largest hole against the primary questions.
   "I have $20/month" cannot be answered at all without it.
3. **Class B and Class C evidence** — the corpus has none. This is what gates
   every score and every recommendation.
4. **Harness capture** (Priority 3) — no L3 entity exists yet, so no stack can be
   composed, so the engine cannot run end to end.
5. **T-002 capture tooling** — hashing and archival, then re-capture everything
   from this window (T-090).

**Milestone 3+** — the standing experiment suite · longitudinal maintainability
study for Q6, started early because it takes the longest · security posture deep
scan · local inference economics.

---

## Update log

| Date | Change |
|---|---|
| 2026-08-03 | M2: research order reset to follow the query set. Usage profiles added as a blocking dependency for every cost question. |
| 2026-08-03 | Created at end of Milestone 1. Seeded from the landscape scan. |
