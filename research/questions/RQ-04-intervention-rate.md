# RQ-04 — Intervention rate

**Status:** accepted · **ERI:** High · **Effort:** High
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**How many human interventions does a stack require per unit of completed work,
and what kind are they?**

## 2. Why it matters

Autonomy (D2) is the highest-weighted dimension for several personas and is
currently **unscorable** — no admissible measurement exists.

Benchmarks cannot supply it. They score the **final state**: did the tests pass.
That is precisely the accounting that hides the thing a user experiences. An
agent that reaches the same final state after six corrections and one that
reaches it unaided score identically, and are completely different products to
work with.

The "intervention" framing also exposes a second, better-hidden cost. Survey
evidence surfaced in the M1 scan suggests review time now rivals or exceeds
writing time. If true, **the binding cost of AI-assisted development is human
attention, not tokens** — and a stack that costs more per token while requiring
fewer interventions may be dramatically cheaper in the only currency that is
actually scarce.

**Recommendation surface affected:** D2 for every stack, `obj-long-horizon-autonomy`
(currently zero populated metrics), Q3 in the standard query set, and any claim
about "autonomous" operation.

## 3. Current evidence

| Evidence | Source | Class |
|---|---|---|
| Review time vs writing time; falling trust despite rising adoption | `research/scan-2026-08-03.md` F5 | E — **pointer only** |
| `obj-long-horizon-autonomy` declares the metric set | internal | — |

**No admissible evidence.** The scan observation is Class E and cannot support a
claim. `met-interventions-per-completed-task` is declared and unpopulated.

## 4. Missing evidence

- Any measurement of interventions per completed task, for any stack
- A defensible **taxonomy of intervention types** — these are not equivalent:
  - *correction* — the agent was wrong and was redirected
  - *clarification* — the agent asked, appropriately, and was answered
  - *unblocking* — an environmental failure the agent could not resolve
  - *approval* — a permission gate, which is a safety feature, not a failure
  - *abandonment* — the human took over
- Whether intervention rate scales with task length, or spikes at specific
  failure points (context exhaustion is the obvious candidate)
- How much intervention is attributable to harness rather than model — this
  question and RQ-05 share instrumentation and should share runs

## 5. Proposed experiments

### `exp-intervention-rate-v1`

**The hard part is definitional, not technical.** "Intervention" is a judgment
call, and an unexamined definition would make the headline metric of the autonomy
track unfalsifiable.

**Protocol.**

1. **Preregister the intervention taxonomy** above, with worked examples of each
   category and explicit boundary cases, before any run.
2. **Operator discipline:** the human follows a fixed policy — intervene only
   when the agent is stuck, has gone materially wrong, or requests input. No
   "helpful" steering. The policy is published; deviations are logged as protocol
   violations rather than quietly smoothed.
3. **Log every intervention** with timestamp, category, elapsed session time,
   token position in context, and a one-line description.
4. **Normalize per unit of completed work**, not per session — a session that
   completes twice as much work should not look worse for having twice the
   interventions.
5. **Record approvals separately** from corrections. Counting a safety gate as an
   autonomy failure would penalize exactly the behaviour we want (D13).

**Preregistered prediction.** Intervention rate is non-linear in task length —
low early, rising sharply near context exhaustion — and correction-type
interventions cluster around cross-file changes.

**Blinding.** Not achievable — the operator knows which stack they are running.
This is a real and unfixable limitation of the design; it is recorded, and it is
why inter-operator agreement (below) matters.

**Inter-rater reliability.** A second operator classifies a sample of logged
interventions from transcripts alone. Agreement below a preregistered threshold
means the taxonomy is not yet usable and must be revised before results publish.
This gate is the difference between a measurement and an impression.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.55** | Q3 directly; every autonomy-weighted persona; stack scoring broadly |
| flip_probability | **0.6** | D2 is top-weighted for several personas and is currently absent entirely |
| magnitude | **4/5** | Converts an unscorable dimension into a scored one |

**ERI: High.** Slightly below the Decisive tier only because it does not touch
purely cost-driven queries.

Second-order: if the review-burden framing holds, this experiment produces the
input for a **human-time cost model** — an axis the Atlas does not yet have and
which may matter more than dollars for most readers.

## 7. Estimated effort

**High**, and human-time-bound rather than compute-bound.

| Component | Effort |
|---|---|
| Taxonomy design and preregistration | ~2 days |
| Instrumentation and logging | ~3 days |
| Supervised runs | **substantial operator time — binding constraint** |
| Inter-rater reliability pass | ~2 days per round |

**Binding constraint:** supervised human hours. Every run needs an operator
present and disciplined, which does not parallelize and cannot be automated
without destroying the measurement.

## 8. Current confidence

**In the answer: very low.** No measurement exists, ours or anyone's. Even the
shape of the distribution is a guess.

**In the question: high** — but with an honest caveat: **the metric's validity
depends entirely on the taxonomy holding up under inter-rater testing.** If
agreement is poor, this track produces a well-instrumented opinion rather than a
measurement, and we should say so rather than publish the numbers anyway.
