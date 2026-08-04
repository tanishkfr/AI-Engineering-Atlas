# RQ-10 — How do you measure frontend generation quality at all?

**Status:** accepted · **ERI:** High · **Effort:** High
**Flagship track:** no *(candidate — see §6)* · **Opened:** 2026-08-03

---

## 1. Research question

**What is a defensible, repeatable measurement of frontend generation quality —
and does any model or stack differ meaningfully on it?**

Two questions deliberately joined, because the first must be answered before the
second is meaningful. **Constructing the instrument is the research.**

## 2. Why it matters

Two of the seven standard queries — *"I am a UI/UX designer who barely codes"*
(Q2) and *"I need the best frontend generation"* (Q5) — currently return
`NO_MEASUREMENTS`. The Atlas refuses to answer them.

That refusal is correct and it is also a gap. The wider ecosystem answers these
questions constantly, using **repository-patching benchmarks that measure nothing
about interface quality**. `obj-frontend-generation` explicitly declares those
inadmissible, which is why the engine refuses rather than producing a fluent
wrong answer.

The refusal is arguably more accurate than any published ranking. But an atlas
whose answer to a common question is permanently "we don't know" has ceded the
question to worse sources.

**Recommendation surface affected:** Q2 and Q5 entirely; the designer persona,
for whom no recommendation of any kind is currently possible.

## 3. Current evidence

| Evidence | Source | Class |
|---|---|---|
| `obj-frontend-generation` metric set declared | internal | — |
| Frontend arenas exist in the wider ecosystem | `research/scan-2026-08-03.md` | E — pointer only |

**No admissible measurement.** Four declared metrics, zero populated. The scan
noted frontend-specific arenas exist; we have not evaluated their construct
validity and cannot cite them.

## 4. Missing evidence

- Any admissible frontend quality measurement
- Whether existing public frontend arenas have defensible construct validity —
  worth evaluating *before* building our own, since adopting a sound external
  instrument is cheaper than inventing one
- Inter-rater reliability for visual quality judgments — the crux
- Whether "visual fidelity to brief" is measurable at all without human raters,
  or whether automated proxies (layout diffing, accessibility linting) capture
  enough
- How much of frontend quality is *iteration* rather than first output — a model
  producing mediocre output that converges in two rounds may beat one producing
  better first output that resists correction

## 5. Proposed experiments

### Stage 1 — `exp-frontend-instrument-v1` *(instrument construction)*

Do not measure anything yet. Build and validate the ruler.

1. **Brief set**: 8–12 fixed design briefs spanning marketing page, dashboard,
   form-heavy flow, data display, mobile-first layout. Each with explicit
   acceptance criteria written *before* any generation.
2. **Rubric**, fixed before outputs are seen:
   - visual fidelity to brief (human-rated, anchored)
   - responsive correctness (automated: breakpoint assertions)
   - accessibility baseline (automated: axe-style audit)
   - framework-idiomatic structure (human-rated)
   - iterations to acceptable (counted)
3. **Inter-rater reliability**: multiple raters score a sample blind to which
   stack produced it. **Below a preregistered agreement threshold, the rubric is
   revised before any results are published.**
4. **Prior-art evaluation**: assess public frontend arenas against this rubric's
   construct. If one is sound, adopt it and say so — inventing an instrument that
   already exists would be waste dressed as rigour.

**Stage 1 succeeds if it produces a rubric with acceptable inter-rater
agreement.** If it does not, the honest published output is *"frontend quality is
not reliably measurable by our method"*, which is a real contribution given how
confidently others rank it.

### Stage 2 — `exp-frontend-fidelity-v1` *(measurement)*

Only after Stage 1 passes. Run the brief set across stacks, blind-score, publish
raw outputs and screenshots alongside scores so readers can disagree with the
rating and still use the artifacts.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.3** | Q2 and Q5; concentrated in one persona |
| flip_probability | **0.9** | Currently *no* answer exists; nearly any result changes the output |
| magnitude | **5/5** | Converts a permanent refusal into a recommendation |

**ERI: High.** Narrow breadth, exceptional depth — the classic profile of a
persona-scoped finding, and precisely what a persona-aware atlas should be
better at than a general ranking.

**Flagship candidacy:** promote to flagship **only if Stage 1 succeeds.** A track
built on an unreliable instrument would generate confident numbers with no
validity, which is worse than the current honest refusal.

## 7. Estimated effort

**High.**

| Component | Effort |
|---|---|
| Brief set + acceptance criteria | ~3 days |
| Rubric design and anchoring | ~2 days |
| Inter-rater reliability rounds | **substantial human time — binding constraint** |
| Automated checks (responsive, a11y) | ~3 days |
| Stage 2 runs and blind scoring | substantial |

**Binding constraint:** human raters, plural, for reliability testing. A
single-rater instrument would measure our taste and call it a finding — the
failure mode METHODOLOGY §9 already names as our biggest bias.

## 8. Current confidence

**In the answer: very low.** No measurement exists, and it is genuinely uncertain
whether a reliable one *can* be built for visual quality.

**In the question: high** — with the strongest caveat in the portfolio:
**this may be unanswerable at acceptable reliability.** Publishing that negative
result would still be more useful than another leaderboard built on the wrong
benchmark.
