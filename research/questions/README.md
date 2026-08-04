# RESEARCH PROGRAM

**Status:** v1.0 · **Opened:** 2026-08-03 · **Governs:** `research/questions/`

The Atlas's original research agenda. Not a backlog of interesting topics — a
ranked portfolio of questions whose answers change what the recommendation
engine outputs.

---

## 1. Why this exists

The first ten entities produced more original questions than facts. That is the
signal that the project has crossed from aggregation into research: the
interesting problems stopped being "what does the documentation say" and became
"nobody has measured this, and the answer determines the recommendation."

Three of the six flagship questions below cannot be answered from any public
source. They are not gaps in our reading. They are gaps in the field.

**The organizing principle:** the Atlas should be able to improve its own
recommendation engine by running experiments, not only by reading faster than
its readers. A research atlas that only aggregates is a bibliography.

---

## 2. Ranking: Expected Recommendation Impact

Questions are ranked by **ERI**, not by novelty, difficulty, or how interesting
they are to work on. ERI operationalizes the value-of-information concept in
[DECISION.md](../../DECISION.md) §8.

```
ERI = breadth × flip_probability × magnitude
```

| Component | Definition | Scale |
|---|---|---|
| **breadth** | Share of the standard query set (QUERIES.md Q1–Q7) whose answer depends on this | 0–1 |
| **flip_probability** | P(the recommended stack changes for at least one persona once resolved) | 0–1 |
| **magnitude** | Size of the change if it flips — dollars, ranks, or feasibility | 1–5 |

Rendered as a band:

| Band | Meaning |
|---|---|
| **Decisive** | Changes the recommended stack for a majority of personas |
| **High** | Changes recommendations for some personas, or materially moves a headline number |
| **Moderate** | Narrows confidence bands; rarely flips a choice |
| **Low** | Improves a page; does not change an answer |
| **Negligible** | Changes nothing at any plausible value — **do not research** |

**The Negligible band is load-bearing.** CONSTITUTION §14 caps coverage at
maintenance capacity, so a program that only ever adds work is a program that
eventually lies. Explicitly declining questions is part of the method.

**ERI components are estimates with stated priors, not measurements.** They are
recorded in each file so they can be argued with, and revised as evidence
arrives. Early ERI estimates are themselves low-confidence — a fact the program
should not hide while using them to allocate effort.

### Effort is ranked separately, and does not reorder the list

Effort is shown so sequencing is informed, never so a hard question gets demoted
for being hard. Where a question is both high-ERI and low-effort, it is flagged
**JUMP QUEUE** — that combination is rare and should be exploited immediately.

---

## 3. The portfolio

Ranked by ERI. Effort shown separately.

| # | Question | ERI | Effort | Answerable from public sources? |
|---|---|---|---|---|
| [RQ-01](RQ-01-tokenizer-normalization.md) | Are per-token prices comparable across vendors? | **Decisive** | **Low** ⚡ | No |
| [RQ-05](RQ-05-harness-effect-size.md) | How much of observed quality is the harness, not the model? | **Decisive** | High | No |
| [RQ-03](RQ-03-cache-economics.md) | What cache hit rates do real harnesses achieve, and what do they buy? | **Decisive** | Medium | No |
| [RQ-04](RQ-04-intervention-rate.md) | How much human intervention does a unit of completed work require? | **High** | High | No |
| [RQ-08](RQ-08-subscription-crossover.md) | At what usage does a subscription beat metered API access? | **High** | Low ⚡ | Partly |
| [RQ-02](RQ-02-throughput-constrained-autonomy.md) | Does throughput bind before price or quality for agentic work? | **High** | Medium | No |
| [RQ-06](RQ-06-real-world-feature-cost.md) | What do the "free" parts of a request actually cost? | **Moderate–High** | Low ⚡ | Partly |
| [RQ-10](RQ-10-frontend-fidelity.md) | How do you measure frontend generation quality at all? | **High** | High | No |
| [RQ-07](RQ-07-sonnet-5-tokenizer.md) | Does Claude Sonnet 5 use the newer tokenizer? | Moderate | **Trivial** ⚡ | No |
| [RQ-09](RQ-09-cache-storage-cost-model.md) | Can one cost model represent incompatible cache billing shapes? | Moderate | Low | Yes |

**Three questions carry the ⚡ JUMP QUEUE flag** — high impact, low effort, no
public answer. RQ-01 in particular is the single best available move: it is
cheap, deterministic, requires no model access, and it unblocks every
cross-vendor cost claim the Atlas will ever make.

### Declined

| Question | Band | Reason |
|---|---|---|
| Ecosystem maturity scoring for P0 entities | Negligible | Changes no recommendation at any plausible value (surfaced by the Q7 VOI trace) |
| Leaderboard position tracking | Negligible | Position is not a finding; the underlying measurement already enters via RQ-05 |
| Parameter-count and architecture cataloguing | Low | No decision depends on it; readers who care can get it from model cards |

---

## 4. Flagship tracks

**Cap: 5 active flagship tracks.** A new flagship must replace a lower-ERI
question, wait in the backlog, or justify interrupting evidence population.

Flagship tracks are sustained programs with versioned protocols and longitudinal
datasets, not one-off experiments. Each is chosen because its data compounds — a
re-run against a new model is immediately comparable to every prior run.

### Active (5 / 5)

| Track | Produces | Status |
|---|---|---|
| **Cache economics** (RQ-03) | Per-harness cache hit rates and their cost/throughput yield | active |
| **Intervention rate** (RQ-04) | Interventions per completed unit of work, per stack | active |
| **Harness effect size** (RQ-05) | Variance decomposition: how much is model, how much is scaffold | active |
| **Real-world feature cost** (RQ-06) | Per-request overhead accounting across vendors | active |
| **Throughput-constrained autonomy** (RQ-02) | Sustained-consumption profiles vs published rate limits | active |

### Demoted 2026-08-04 — **RQ-01 Tokenizer normalization**

Demoted from flagship to **maintained**, on the evidence of its own follow-up
study.

RQ-01 was designated flagship on an estimated Decisive ERI. `exp-normalized-cost-v1`
(RQ-01a) then measured the effect **among models that actually have prices**, and
found effective token multipliers of **1.03–1.11×** — not the 1.33× that RQ-01
reported, which was driven by an older tokenizer generation belonging to no
currently-priced model. Normalization **changed no cost ranking in any of five
strata**, because posted prices span 263× while token counts span 11%.

Its realized rule — *normalization changes a ranking only when posted prices
differ by less than ~11%* — is genuine and useful, and it does not require a
sustained longitudinal program to maintain. A periodic refresh when tokenizers
change is sufficient.

**This is the cap working as intended:** a track was demoted because evidence
shrank its impact, not because something newer arrived. RQ-01 remains an open
question at Moderate ERI, in maintained status, with its follow-ups (RQ-01a–i)
in the backlog.

**Promoted into the vacancy:** RQ-02, previously High/non-flagship. Its
longitudinal consumption-vs-limits dataset compounds in exactly the way flagship
status is meant to select for.

---

## 5. Question lifecycle

```
  proposed → accepted → active → answered → maintained
                   ↘ declined (with reason)
                   ↘ blocked (on capability or access)
```

- **proposed** — written up, ERI estimated, not yet committed
- **accepted** — ERI justifies the effort; protocol to be designed
- **active** — protocol preregistered, running
- **answered** — result published, including negative and inconclusive results
- **maintained** — flagship tracks re-run on a cadence; the dataset is the asset
- **declined** — explicitly not pursued, with the reason recorded

A question does not move to `active` without a **preregistration**
(METHODOLOGY §7): the procedure, the metrics, the predicted outcome, and what
result would change our recommendation — written before any run.

---

## 6. File template

Every question file carries the same eight sections, in this order:

1. **Research question** — one sentence, answerable, falsifiable
2. **Why it matters** — which recommendation changes, for whom
3. **Current evidence** — what we have, with claim and source IDs
4. **Missing evidence** — what is absent, specifically
5. **Proposed experiments** — protocol, conditions, controls
6. **Expected impact on recommendations** — ERI components, stated
7. **Estimated effort** — with the binding constraint named
8. **Current confidence** — in the *answer*, not in the question

Section 8 is usually `unknown`, and saying so is the point.

---

## 7. Honest limits of this program

- **ERI estimates are guesses right now.** Breadth is computable from the query
  set; flip probability and magnitude are judgment until there is a corpus and a
  query log. The ranking is directionally useful and numerically soft.
- **We are one team with one working style.** Every experiment below inherits
  the single-operator bias in METHODOLOGY §9. Protocols publish prompts and
  configs so others can contradict us; that is mitigation, not a fix.
- **Some flagship tracks need model access we may not sustain.** RQ-05 is
  combinatorially expensive (N models × M harnesses) and may have to run at
  reduced coverage, which weakens variance decomposition specifically.
- **A program that produces its own evidence can fool itself.** Class D is not
  automatically superior to Class B (SOURCES §1). Preregistration, published
  raw outputs, and publishing failures are the guards. They are necessary and
  not sufficient.
