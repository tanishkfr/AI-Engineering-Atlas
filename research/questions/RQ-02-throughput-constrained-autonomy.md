# RQ-02 — Throughput-constrained autonomy

**Status:** accepted · **ERI:** High · **Effort:** Medium
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**For sustained agentic work, does published rate-limit capacity bind before
price or quality — and if so, for which stacks and at what scale?**

## 2. Why it matters

A finding from the first evidence pass inverts the usual ranking: **the most
capable model carries the tightest throughput ceiling.**

| Tier | Claude Fable 5 ITPM | Claude Opus 5 / Sonnet 5 ITPM | Ratio |
|---|---|---|---|
| Start | 500,000 | 2,000,000 | 4.0× |
| Build | 1,500,000 | 5,000,000 | 3.3× |
| Scale | 4,000,000 | 10,000,000 | 2.5× |

If sustained agentic work consumes input tokens at a rate approaching these
ceilings, then **the "best" model may be unusable for the work it is best at** —
and a recommendation built on quality and price alone would be actively wrong.

Nobody appears to have measured sustained consumption rates against published
limits. The data to do it is free: limits are published, and consumption is
measurable from any instrumented run.

This also introduces a dimension the Atlas does not currently score:
**feasibility**. A stack can be affordable, high quality, and *not runnable at
your working intensity*. That is a distinct failure mode from "too expensive",
and readers deserve to be warned before they build on it.

**Recommendation surface affected:** every stack recommendation for
autonomy-weighted or parallel-agent personas; hard-constraint elimination
(a stack that cannot sustain the workload should be *eliminated*, not penalized).

## 3. Current evidence

| Evidence | Source | Class | Fidelity |
|---|---|---|---|
| Full ITPM/OTPM tables by tier and model | `src-anthropic-rate-limits-2026-08-03` ex.1–3 | A | verbatim |
| Cache reads excluded from ITPM | ex.4–5 | A | verbatim |
| Published limits are an **upper bound** for new accounts | ex.8 | A | verbatim |
| Opus 4.x share a combined bucket; Opus 5 separate | ex.6 | A | verbatim |
| `clm-access-anthropic-api-002/003/004` | — | — | published |

Strong on the **ceiling**. Nothing at all on the **consumption rate** — which is
the other half of the inequality.

## 4. Missing evidence

- Sustained ITPM/OTPM consumption during real agentic sessions, by stack
- Peak vs mean consumption — bursty consumption hits limits that mean rates
  suggest are safe, and the token-bucket algorithm means short bursts can trip a
  limit the per-minute average never approaches
- How consumption scales with parallel agents — the case where this most likely
  binds
- What the *actual* starting limits are for a new account, given documentation
  states they may be lower than published
- Equivalent limit data for other vendors. **Anthropic publishes clear tables;
  we have not established that others do.** Absence of published limits is itself
  a finding about comparability.
- Observed 429 behaviour: how gracefully do harnesses degrade when throttled?

## 5. Proposed experiments

### `exp-throughput-consumption-v1`

**Design.** Instrumentation-led, riding on runs performed for RQ-03/RQ-04/RQ-05.

1. Log per-request input and output token counts with timestamps.
2. Compute rolling per-minute consumption: mean, p95, peak.
3. Compare against published tier limits → **headroom ratio** per stack per tier.
4. Repeat with 2 and 4 parallel agents to establish scaling.
5. Compute the **cache-adjusted** headroom, since cache reads do not count.

**Preregistered prediction.** Single-agent interactive work stays well under
Start-tier limits for mid-tier models, but (a) parallel agents at ≥3 concurrency
and (b) the tightest-limited frontier model at ≥2 concurrency approach or exceed
Start-tier ITPM. Recorded before running.

### `exp-throttle-behaviour-v1`

Deliberately drive a harness into 429 territory and record what happens: does it
back off correctly, surface the error, lose work, or fail silently? Graceful
throttle handling is a harness quality property that nothing currently evaluates,
and silent work loss would be a serious finding.

**Safety note.** Run against our own accounts, at our own expense, at modest
concurrency. This experiment deliberately induces failure and must not be run in
a way that degrades service for anyone else.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.5** | Q3 and Q7 directly; all parallel/agentic personas |
| flip_probability | **0.55** | Feasibility is an *elimination*, not a penalty — when it binds, it changes the answer completely |
| magnitude | **4/5** | Can remove the top-ranked stack from consideration entirely |

**ERI: High.**

The asymmetry matters: for most readers this changes nothing, and for the subset
running sustained or parallel work it changes everything. That is exactly the
shape of finding a persona-scoped atlas should be good at surfacing and a
one-size ranking cannot.

## 7. Estimated effort

**Medium**, largely shared with RQ-03 instrumentation.

| Component | Effort |
|---|---|
| Rolling-consumption instrumentation | ~2 days (extends RQ-03 logging) |
| Parallel-agent test harness | ~3 days, **binding constraint** |
| Throttle-behaviour runs | ~1 day |
| Cross-vendor limit documentation research | ~1 day |

**Binding constraint:** running genuine parallel agent workloads reproducibly.
Also gated by our own account tier — we can only observe limits we can reach, so
Scale-tier behaviour may remain unmeasured and must be reported as such rather
than extrapolated.

## 8. Current confidence

**In the answer: low.** The ceilings are documented and verbatim-sourced; the
consumption side is entirely unmeasured. It is genuinely possible that real
consumption is an order of magnitude below the limits and this question resolves
to "rarely binds" — a negative result worth publishing, since it would let
readers stop worrying about it.

**In the question: high.** The ratio in §2 is real, published, and absent from
every comparison we have seen.
