# RQ-09 — Can one cost model represent incompatible cache billing shapes?

**Status:** accepted · **ERI:** Moderate · **Effort:** Low
**Flagship track:** no · **Opened:** 2026-08-03 · **Tracked as:** RG-004

---

## 1. Research question

**What cost-model structure represents time-based cache storage billing and
multiplier-based cache write billing without privileging either?**

The only question in the portfolio that is primarily about **our own
architecture** rather than the ecosystem.

## 2. Why it matters

The first evidence pass found two structurally different cache billing shapes:

| Vendor | Cache billing shape | Punishes |
|---|---|---|
| Anthropic | Multiplier on writes (1.25× / 2×), read at 0.1×, time-limited validity | cache misses |
| Google | Per-token cache price **plus $1.00 / 1M tokens per hour storage** | idle sessions |

These are not the same product with different numbers. Google's storage term
accrues **while you are doing nothing** — a long session with think-time between
turns costs money in a way Anthropic's model does not. Anthropic's TTL means a
gap longer than the window silently forfeits the write cost instead.

The current cost function (RECOMMENDATION §6) has a single cache term and
**cannot express the storage shape at all.** Any Google cost figure produced
today would be wrong in a direction that flatters or penalizes depending purely
on session shape.

This is the M3 finding that touched architecture. It was surfaced by data rather
than by reasoning, which is the intended behaviour of a population phase.

**Recommendation surface affected:** any cross-vendor cost comparison involving
a vendor with time-based cache billing.

## 3. Current evidence

| Evidence | Source | Class | Fidelity |
|---|---|---|---|
| Anthropic cache multipliers and TTLs | `src-anthropic-pricing-2026-08-03` ex.3–4 | A | verbatim |
| Google per-hour cache storage pricing | `src-google-gemini-pricing-2026-08-03` ex.0–2 | A | **tool_extracted** |

The Google evidence is reduced-fidelity and its claims are `draft`. **Confirming
the storage term verbatim is a prerequisite** — building a cost-model extension
on a restructured extraction would be exactly the error the fidelity rules exist
to prevent.

## 4. Missing evidence

- Verbatim confirmation of Google's cache storage billing
- Whether other vendors use additional shapes we have not yet encountered
- Typical idle time in real agentic sessions — the variable that determines
  which shape wins, and currently unmeasured (RQ-03 dependency)

## 5. Proposed work

### `spec-cost-model-v2` — extend, do not special-case

Add a **time-based storage term** to the per-component cost function, defaulting
to zero:

```
component_cost = token_terms
               + cache_write_terms
               + (cached_tokens × storage_rate × cache_resident_hours)
```

Requires a new usage-profile field: `cache_resident_hours` (or derivable from
session duration and idle time). Vendors without storage billing set
`storage_rate: 0` and the term vanishes.

**Why additive rather than a vendor branch:** a `if vendor == X` branch in the
cost model would violate the extensibility invariant (RECOMMENDATION §16.1 — no
vendor names in engine code). A general term with a zero default preserves it,
and absorbs the next unfamiliar billing shape without a redesign.

### `exp-cache-shape-crossover-v1`

Once idle-time data exists (RQ-03), compute the session profile at which each
shape wins. Deliverable is a crossover surface over session length × idle
fraction × context size.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.35** | Cross-vendor cost queries only |
| flip_probability | **0.4** | Can reverse which vendor is cheaper for long, idle-heavy sessions |
| magnitude | **3/5** | Corrects a currently-inexpressible cost component |

**ERI: Moderate.** Ranked as a **correctness prerequisite** rather than a
discovery: without it the Atlas cannot honestly publish Google cost figures at
all, which caps coverage regardless of how much else we research.

## 7. Estimated effort

**Low.** Days.

| Component | Effort |
|---|---|
| Verbatim re-capture of Google pricing | ~0.5 day, **prerequisite** |
| Cost-model extension + tests | ~2 days |
| Usage-profile field + assumptions | ~0.5 day |
| Crossover modelling | blocked on RQ-03 |

## 8. Current confidence

**In the answer: moderate.** The structural fix is clear and low-risk — an
additive term with a zero default is the obvious correct shape. Confidence in the
*inputs* is low: the Google evidence is reduced-fidelity and idle-time data does
not exist.

**In the question: high.** The gap is real and currently blocks honest
cross-vendor cost reporting.
