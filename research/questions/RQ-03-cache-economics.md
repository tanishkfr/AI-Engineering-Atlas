# RQ-03 — Cache economics

**Status:** accepted · **ERI:** Decisive · **Effort:** Medium
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**What cache hit rates do real harnesses achieve on real agentic work, and what
do those rates buy in cost and in throughput?**

## 2. Why it matters

`cache_hit_rate` is the most load-bearing number in the cost model and the least
evidenced. It was already flagged as our weakest assumption (`usage-profiles.yaml`).
The first evidence pass then showed it operates on **two axes at once**:

1. **Cost** — a cache hit costs 0.1× base input. For context-heavy agentic work
   that re-sends a stable system prompt and repository context every turn, this
   is plausibly the largest single cost lever available, larger than choosing a
   cheaper model.
2. **Throughput** — cache reads do **not** count toward input-token-per-minute
   rate limits. Anthropic's own worked example: a 2M ITPM limit at an 80% hit
   rate processes an effective 10M tokens/minute.

So caching determines both what a stack costs *and whether it can run at all*.

The decisive consequence: **two harnesses at the same nominal model price are not
the same product.** A harness that caches well and one that does not differ in
effective cost by up to ~10× on the cached portion, and in effective throughput
by roughly `1/(1−hit_rate)`. No comparison anywhere reports this. It is invisible
in every per-token price table.

**Recommendation surface affected:** every cost output, the budget frontier,
feasibility assessment under rate limits, and D6 for every harness.

## 3. Current evidence

| Evidence | Source | Class | Fidelity |
|---|---|---|---|
| Cache multipliers 1.25×/2× write, 0.1× read | `src-anthropic-pricing-2026-08-03` ex.3 | A | verbatim |
| Payback after 1 read (5m) or 2 reads (1h) | ex.4 | A | verbatim |
| Cache reads excluded from ITPM | `src-anthropic-rate-limits-2026-08-03` ex.4 | A | verbatim |
| 80% hit rate → 5× effective throughput (vendor example) | ex.5 | A | verbatim |
| Google bills cache **storage per hour**; shape differs from Anthropic's | `src-google-gemini-pricing-2026-08-03` ex.0 | A | tool_extracted |

Strong on **mechanism**. Zero evidence on **realized hit rates** — the vendor's
80% is an illustrative example, not a measurement of anything.

## 4. Missing evidence

- Actual hit rates achieved by real harnesses on real repositories
- How hit rate varies with session length, repository size, and task type
- Whether harnesses that advertise caching achieve materially different rates
  from those that do not mention it
- Cache invalidation behaviour under file edits — an agent that edits a cached
  file presumably invalidates part of the prefix; how much, and how often, is
  unknown and directly determines the achievable ceiling
- Whether 5-minute vs 1-hour TTL choice matters in practice for typical
  inter-turn gaps
- Cross-vendor: Google's per-hour storage billing means an idle session accrues
  cost. Nobody appears to have modelled the crossover between the two shapes.

## 5. Proposed experiments

### `exp-cache-economics-v1`

**Design.** Instrumentation-led — no new task suite required; it rides on runs
performed for other experiments, which makes it unusually cheap for its impact.

1. Instrument every agentic run to log, per request:
   `input_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`,
   `output_tokens`, and wall-clock gap since previous request.
2. Compute realized hit rate per session, per harness, per task class.
3. Compute **counterfactual cost**: what the same token trace would have cost
   with zero caching. The delta is the cache's realized value in dollars.
4. Compute **effective throughput multiplier** and compare against the tier's
   ITPM ceiling to identify where throughput would have bound without caching.

**Controls.** Same repository, same task, same model across harnesses. Inter-turn
gaps recorded because they determine TTL applicability.

**Preregistered prediction.** Realized hit rates on multi-turn agentic sessions
span a range of at least 30 percentage points across harnesses, and at least one
widely-used harness achieves under 40%.

### `exp-cache-economics-v2` *(cross-vendor shapes)*

Model Google's per-hour storage billing against Anthropic's write-multiplier
billing for the same session trace, and find the session profile at which each
wins. Deliverable is a **crossover surface** (session length × idle time ×
context size), not a single number. Feeds RQ-09.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **1.0** | Every cost query; plus feasibility for throughput-bound work |
| flip_probability | **0.65** | Hit-rate differences across harnesses plausibly exceed price differences across models |
| magnitude | **4/5** | Up to ~10× on the cached portion of spend |

**ERI: Decisive.**

Notable second-order effect: this may promote **harness caching behaviour into a
scored property**. If confirmed, the Atlas would be recommending harnesses partly
on a dimension nobody currently evaluates.

## 7. Estimated effort

**Medium**, and unusually leveraged — most of it is instrumentation that other
experiments need anyway.

| Component | Effort |
|---|---|
| Token-accounting instrumentation | ~2 days |
| Harness integration for logging | ~3 days, **binding constraint** |
| Analysis and crossover modelling | ~2 days |
| Runs | rides on RQ-04 / RQ-05 runs |

**Binding constraint:** getting per-request token accounting out of harnesses
that do not expose it. Some may require proxying the API to capture usage
fields, which risks perturbing the behaviour being measured — a limitation to
record rather than engineer around silently.

## 8. Current confidence

**In the answer: low.** Mechanism is documented and verbatim-sourced; realized
rates are entirely unknown. The 30-point-spread prediction is a prior with no
supporting data.

**In the question: high.** Both cost and feasibility depend on it, and the
absence of any public measurement is well established.
