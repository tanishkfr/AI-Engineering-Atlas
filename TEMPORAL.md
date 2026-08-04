# TEMPORAL MODEL

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Supersedes:** SCHEMA.md v1.0
`history[]` · **Machine form:** `data/schema/temporal.schema.json`

How the Atlas represents facts that change. This is the difference between a
knowledge base and a snapshot with a date on it.

---

## 0. The defect this fixes

SCHEMA.md v1.0 stored a current value plus a `history[]` array of previous ones.
That is the design almost everyone reaches for, and it is wrong in three ways
that only become visible later:

1. **It cannot distinguish a change from a correction.** If a price record moves
   from $3 to $4, did the vendor raise the price, or were we wrong about $3?
   Those are completely different facts about the world, and the reader deserves
   to know which. CONSTITUTION §11 requires corrections to be visible; `history[]`
   makes them indistinguishable from updates.

2. **It cannot answer time-scoped questions.** "What was the cheapest stack in
   March?" and "what did the Atlas recommend in March?" are both legitimate and
   both unanswerable when the past is a footnote on the present.

3. **It treats all changing facts identically.** A price and a benchmark score
   both change over time, but a price *persists until superseded* while a
   benchmark score is *a sample that is never valid at any other moment*. Storing
   them the same way is what produces "current benchmark score" — a phrase that
   should not exist.

The fix: **facts are immutable, bitemporal, and typed by how they change.**

---

## 1. Two time axes

Every fact carries two independent intervals. This is standard bitemporal
modelling, and it is not optional here.

| Axis | Question | Fields |
|---|---|---|
| **Valid time** | When was this true *in the world*? | `valid_from`, `valid_to` |
| **Assertion time** | When did *the Atlas* believe it? | `asserted_from`, `asserted_to` |

```
   a price rises 2026-07-14, and we notice on 2026-08-03
   ────────────────────────────────────────────────────────
   fact A   valid [2026-03-01 → 2026-07-14)   asserted [2026-03-05 → open)
   fact B   valid [2026-07-14 → open)         asserted [2026-08-03 → open)

   → a CHANGE. Fact A stays valid for its interval, forever.


   we discover our March figure was wrong
   ────────────────────────────────────────────────────────
   fact A   valid [2026-03-01 → 2026-07-14)   asserted [2026-03-05 → 2026-08-03)
   fact A'  valid [2026-03-01 → 2026-07-14)   asserted [2026-08-03 → open)

   → a CORRECTION. Same valid interval, superseded assertion.
     The reader who acted on A in April can see that we were wrong.
```

The shapes are unambiguously different, which is the entire point. A change
extends the record; a correction retracts an assertion over the *same* valid
interval and says why.

**Nothing is ever edited or deleted.** A claim record, once asserted, is
immutable. New knowledge appends. `asserted_to` closing is the only mutation the
system performs, and it is performed by the build, never by hand.

---

## 2. Temporal kinds

Not all changing facts change the same way. Every predicate declares a
`temporal_kind`, and the kind governs interpolation, staleness semantics, query
behavior, and rendering.

| Kind | Behavior | Examples | Carry-forward? |
|---|---|---|---|
| `static` | No temporal dimension. True by definition. | entity ID, creator, licence at release | n/a |
| `point` | Instantaneous event. Immutable once recorded. | release date, acquisition, deprecation notice | n/a |
| `step` | Piecewise constant. Holds until superseded. | price, context window, rate limit, licence, availability | **Yes**, until contradicted or expired |
| `measurement` | A sample under stated conditions. Valid only at its instant. | benchmark score, latency, task-success rate, cost-per-task | **Never** |
| `series` | Repeated sampling of a noisy quantity. | community sentiment, adoption share, issue velocity | **Never**; trend only |
| `interval` | Holds over a stated span, with no claim outside it. | preview availability, incident window, promotional pricing | Within interval only |

### The rule that matters most

> **`measurement` and `series` facts are never carried forward. There is no
> "current" value for either.**

A benchmark score is not a property of a model. It is a property of *one run, of
one model version, on one harness, at one date*. The graph will refuse to answer
"what is Model X's SWE-bench score" and will instead answer "here are the
measurements we have, with their conditions" — which is the honest response and
the one that makes M1 scan finding F4 impossible to reproduce here.

Similarly, sentiment sampled in March is not sentiment now. A `series` renders
as a trend with its sampling windows visible, never as a point fact.

`step` facts carry forward, which is what makes "the current price" a meaningful
concept — but carry-forward is bounded by the decay window (METHODOLOGY §6).
A step fact past expiry stops being "current" and becomes "last known, as of".

---

## 3. Fact record

Claims become **temporal facts**. Shape:

```yaml
- id: clm-example-cli-014
  subject: ent-harness-example-cli
  predicate: pricing.input_per_mtok
  temporal_kind: step
  type: S                       # claim type, SOURCES.md §2

  value: {amount: 0.00, currency: USD, unit: per_mtok}

  valid_from: 2026-07-14
  valid_to: null                # open interval — still in force
  valid_precision: day          # day | month | quarter | unknown

  asserted_from: 2026-08-03
  asserted_to: null             # open — this is what we currently believe

  observed_at: 2026-08-03       # when we actually retrieved it

  supersedes: clm-example-cli-009
  supersession_kind: change     # change | correction | refinement | retraction

  conditions:                   # required for measurement/series
    via: null
    harness: null
    harness_version: null
    sample_window: null

  evidence: [...]
  confidence: high              # COMPUTED
  freshness: fresh              # COMPUTED
  status: published
```

### `supersession_kind` — the field that carries the honesty

| Kind | Means | Effect on the reader |
|---|---|---|
| `change` | The world changed. Prior fact remains true for its interval. | Prior fact stays visible as history |
| `correction` | We were wrong. Prior assertion retracted over the same valid interval. | **Surfaced in the corrections register** |
| `refinement` | Same fact, better precision (e.g. a guessed month resolved to a day). | Quiet; logged |
| `retraction` | Withdrawn with no replacement. Reverts to `unknown`. | Surfaced; page shows a gap |

Only `correction` and `retraction` reach the corrections register. Conflating
them with `change` — which is what a single `history[]` array does — is how a
knowledge base hides its own error rate.

---

## 4. Temporal relationships

Edges are facts too, and get the same treatment. "Available through provider Y"
starts and ends. "Acquired by" is a point event. "Competes with" is a step fact
that becomes false when one party dies.

```yaml
- id: rel-…
  subject: ent-model-…
  predicate: available_through
  object: ent-access-…
  temporal_kind: step
  valid_from: 2026-05-01
  valid_to: null
  asserted_from: 2026-08-03
  asserted_to: null
  evidence: [clm-…]
```

Consequence: **the graph is queryable at a date.** `graph_at(2026-03-01)` returns
the subgraph of facts and edges valid then and asserted then. That single
capability is what makes historical analysis possible at all, and it comes free
once edges are temporal.

---

## 5. Queries the model must support

These are the acceptance criteria for the temporal layer.

| Query | Uses |
|---|---|
| What is true now? | `valid_to is null OR valid_to > today`, latest assertion, kind-aware carry-forward |
| What was true on date D? | valid interval contains D; latest assertion as of today |
| What did the Atlas *say* on date D? | valid interval contains D; assertion interval contains D |
| What changed this month? | facts with `asserted_from` in window, grouped by `supersession_kind` |
| Where have we been wrong? | `supersession_kind: correction` — the corrections register |
| How has X's price moved? | all `step` facts on the predicate, ordered by `valid_from` |
| How has sentiment shifted? | `series` facts with sampling windows, rendered as trend |
| What did the frontier look like in Q1? | `measurement` facts with `valid_from` in Q1, grouped by conditions |
| Would the recommendation have differed in March? | run the engine against `graph_at(2026-03-01)` |

That last one is the strongest argument for the whole design. It lets the Atlas
audit *itself* — replay past recommendations against past evidence and check
whether they held up. No comparison site can do that, because none of them keep
the past.

---

## 6. Freshness, restated temporally

Freshness (METHODOLOGY §6) is now a function of temporal kind:

| Kind | Freshness means |
|---|---|
| `step` | Time since `observed_at`, against the decay window. Expired → no longer "current", degrades to "last known". |
| `measurement` | Time since `valid_from`. Never "current" at any age; older measurements are shown with more prominent conditions, not hidden. |
| `series` | Time since the last sample. A series with no recent sample renders as a stalled trend, explicitly. |
| `point` | Never stale. A release date does not decay. |
| `static` | Never stale. |
| `interval` | Stale once `valid_to` has passed and no successor exists. |

The practical effect: **release dates and acquisitions never rot, prices rot
fast, and benchmark scores are born stale.** That is correct, and a uniform
freshness rule cannot express it.

---

## 7. Rendering rules

Binding on the interface (INFORMATION-ARCHITECTURE §4):

1. `measurement` values **always** render with their conditions attached —
   harness, version, date, operator. No exceptions, no compact mode that drops
   them.
2. `step` values past expiry render as "last known: X, as of DATE", never as X.
3. `series` values render as trends with sample windows. A single point from a
   series is never quoted as a fact.
4. Corrections are visible where the corrected fact was previously shown.
5. Every value links to its temporal history, not just its source.
6. Comparison tables are computed at a single reference date, and that date is
   displayed. Mixing reference dates in one table is a validation error.

---

## 8. Costs of this design

Stated plainly, because they are real.

- **Storage and authoring grow monotonically.** Nothing is ever deleted. A P0
  entity's price predicate will accumulate dozens of records over years.
  Mitigation: facts are small; the corpus is text; this is an acceptable trade
  for auditability.
- **Query complexity.** Every read is now "as of when, believed when". The build
  materializes a current-view index so ordinary reads stay cheap, but the
  complexity is real and will produce bugs.
- **Authoring burden.** Contributors must think about validity intervals, and
  `valid_from` is frequently unknown — a vendor changes a price silently and the
  true date is unavailable. Handled by `valid_precision` and by permitting
  `valid_from: unknown` with `observed_at` as a lower bound. Never guessed.
- **It is over-engineered for a corpus of zero facts.** True today. It is
  under-engineered for a corpus of ten thousand facts across three years, and
  retrofitting bitemporality onto an existing corpus is a migration nobody
  completes.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial temporal model. Replaces SCHEMA v1.0 `history[]` with immutable bitemporal facts; adds temporal kinds and supersession semantics. |
