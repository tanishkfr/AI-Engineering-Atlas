# RECOMMENDATION ENGINE

**Status:** v2.0 · **Last reviewed:** 2026-08-03 · **Depends on:**
[DECISION.md](DECISION.md), [GRAPH.md](GRAPH.md), [TEMPORAL.md](TEMPORAL.md),
[EVALUATION.md](EVALUATION.md), [PERSONAS.md](PERSONAS.md) ·
**Proof:** [QUERIES.md](QUERIES.md)

A core subsystem, not a UI feature. The Atlas is a **constraint solver over a
knowledge graph**, and this is the solver.

```
recommend : (Query, Graph, Date) → Recommendation | Refusal
```

Formally: assign entities to stack slots, subject to compatibility edges,
capability requirements, and a budget, maximizing a risk-adjusted objective under
uncertainty. Constrained combinatorial optimization — not a sort.

Deterministic: same graph, query, and date → identical output, forever. No model
in the loop at serve time. The reasoning *is* the graph and the rubric, both
inspectable, because an unauditable recommendation destroys the only thing this
project has.

> **v2 changes.** v1.0 was filter → weighted sum → band, which is a ranker with
> good manners. v2 adds the decision layer: uncertainty propagates as
> distributions, dominance prunes before any weight is applied, the choice
> criterion varies with risk posture, and the engine reports opportunity cost,
> option value, sensitivity, and what to research next. Rationale in
> [DECISION.md](DECISION.md) §0.

---

## 1. Query model

A structured object. Natural-language questions map to it by deterministic
template, never by generation, so a question always resolves to the same query.

```yaml
objective:
  kind: maximize | satisfice | minimize_subject_to | compare | enumerate |
        marginal_value                              # ← v2: "what does my next $X buy?"
  target: dimension | metric | cost | fit
  scoped_to: obj-…                                  # required for ratio queries
  subject_to: [ … ]
  apply_implied_guards: true

context:
  persona: per-…
  overrides: { … }
  usage_profile: use-…
  horizon_months: 12                                # ← v2: drives option value

constraints: [ … ]        # hard eliminations, expressed against capabilities
preferences: [ … ]        # re-rank, stay visible, get priced

budget:
  ceiling_usd_month: 20
  shape: hard | soft | variable

scope:
  slots: [ … ]
  required_slots: [model, access, harness]
  fixed: { harness: ent-… }                         # ← v2: single-tool queries

evidence_floor:
  confidence: moderate
  freshness: aging
  allow_unverified_compatibility: true

decision_criterion: auto                            # ← v2: auto | p_best |
                                                    #   expected_value | minimax_regret
reference_date: 2026-08-03
```

`decision_criterion: auto` derives from persona risk posture (DECISION §4).
Explicit values let a reader ask "what if I'm willing to gamble?" and see the
answer change — which is itself informative.

---

## 2. Stacks and slots

**The unit of recommendation is a stack** (DECISION §10). Single-tool queries are
the degenerate case: `scope.fixed` pins the other slots, leaving one open. One
code path.

| Slot | Layer | Required | Cardinality |
|---|---|---|---|
| `model` | L1 | yes | 1..n |
| `access` | L2 | yes | 1..n |
| `harness` | L3 | yes | 1 |
| `surface` | L4 | no | 0..n |
| `interop` | L5 | no | 0..n |
| `context` | L6 | no | 0..1 |
| `orchestration` | L7 | no | 0..1 |
| `assurance` | L8 | no | 0..n |
| `practice` | L9 | no | 0..n |

Cardinality `1..n` on `model` and `access` is what makes portfolio allocation
(DECISION §11) expressible rather than a special case bolted on later.

---

## 3. Pipeline

Thirteen stages. Any stage may terminate in a refusal.

```
   1  RESOLVE       query → context, graph_at(reference_date)
   2  CANDIDATES    populate slots from the taxonomy
   3  ELIMINATE     hard constraints — never penalties
   4  COMPOSE       generate stacks; prune combinatorially
   5  COMPATIBLE    three-valued edge check, pairwise
   6  COST          usage profile × temporal pricing
  ─────────────────────────────────────────────────── decision layer ───
   7  UNCERTAINTY   scores → belief distributions
   8  DOMINANCE     weight-free pruning → Pareto set
   9  PERFORM       frontier ratios (continuous metrics only)
  10  DECIDE        criterion by risk posture → P(best) / regret
  11  POSITION      option value, switching cost, decay over horizon
  12  FRONTIER      budget curve, knees, marginal value per dollar
  13  EXPLAIN       six mandatory components + sensitivity + VOI
```

Stages 1–6 establish *what is possible*. Stages 7–12 establish *what is wise*.
Stage 13 makes both arguable.

---

## 4. Stage 3 — Elimination

Constraints remove candidates. They **never** trade off against quality
(EVALUATION §4 rule 4). A team that cannot send code to a third party does not
want a slightly-penalized cloud option; it wants those options gone.

Constraints are expressed against **capabilities**, not entity types
(GRAPH §3) — which is what lets a constraint written today apply to a category
that does not exist yet:

```yaml
constraints:
  - requires_capability: cap-no-training-on-input
  - forbids_capability:  cap-telemetry-default-on
  - facet: licence
    in: [mit, apache-2.0]
```

**Elimination is reported, not silent.** The output states how many candidates
each constraint removed. A constraint that eliminated everything is the finding —
"nothing in the graph satisfies this combination" is a real answer, and
`cap.negates` (capability schema) detects self-contradictory constraint sets
before they silently return zero.

---

## 5. Stage 5 — Compatibility

For every ordered pair in a candidate stack:

| Edge state | Effect |
|---|---|
| `incompatible_with` | Stack rejected. Failure mode reported. |
| `works_with` | Pair verified. |
| `depends_on` unsatisfied | Rejected unless the dependency fits an open slot. |
| **no edge** | **`unverified`** — retained, flagged, confidence penalized |

**Absence of evidence is not compatibility.** A stack containing unverified pairs
is labeled *untested combination* and can never be presented as verified. Most
stacks will be in this state early, and saying so plainly beats a confident guess.

---

## 6. Stage 6 — Cost

Cost is **computed**, never scored. EVALUATION D6 rates cost-effectiveness as a
judgment; this produces a number.

### Usage profiles

Cost is meaningless without a usage model.

```yaml
id: use-solo-founder-typical
tokens_in_month: 0
tokens_out_month: 0
cache_hit_rate: 0.0
retry_rate: 0.0
status: assumed                # assumed | measured
confidence: low
assumptions: [ … ]             # surfaced with every figure derived from it
```

**Until Class D experiments run, every profile is `assumed` with low confidence,
and every cost answer says so.** This is the single largest source of error in
the system and it is exposed rather than hidden — a cost figure resting on an
invented token count is a fabrication with a decimal point on it.

### Cost function

```
cost(stack, profile, date) = Σ over components:

  metered:       in·(1−h)·p_in + in·h·p_cached + out·p_out
  subscription:  base + overage(usage beyond allowance)
  free_tier:     0 up to cap, then defined fallback
  local:         amortized_hardware/months + energy    [always flagged estimated]
  seat-based:    seats × price

  × (1 + retry_rate)          ← work that had to be redone is work you paid for
```

The retry term matters: a component needing four attempts is not cheap, and
per-token comparisons that omit rework are the standard way cost analysis in this
domain misleads.

Every result carries the profile, its status, the pricing reference date, and
`cost_confidence` = **floor**(pricing confidence, profile confidence).

### Crossover

Subscription vs metered is computed, not asserted: evaluate both and report the
**usage at which the cheaper option flips**. The crossover is more useful than
either number, because the reader knows their own usage better than we do.

---

## 7. Stage 7 — Uncertainty propagation

Scores become belief distributions over {1..5}, derived from evidence strength
and **widened by age** (DECISION §1). Costs become distributions over pricing and
usage uncertainty. Measurements carry their variance where runs were repeated,
and a disclosed default band where they were not.

Nothing downstream sees a point estimate.

---

## 8. Stage 8 — Dominance, before any weighting

Stack A dominates B if A is at least as good on every dimension and on cost, and
strictly better on one. Dominated stacks are eliminated **with no weights
applied**.

What survives is the **Pareto set** — the defensible choices, established without
opinion. Weights enter only at stage 10, and only to order options already shown
to be defensible.

This separation is the epistemic core of v2: dominance is a fact about the
evidence, ranking is a judgment about the reader, and the output keeps them
apart.

Probabilistic dominance requires p ≥ 0.9 by default, so nothing is discarded on
noise.

---

## 9. Stage 9 — Performance and the frontier

For ratio queries ("at least 90% of frontier"):

> **Percentage-of-frontier is computed only from continuous measurements.
> Ordinal rubric scores never produce a ratio.**

`0.9 × 5` is not a value on an ordinal scale, and the gaps between rubric points
are not equal by construction. Computing a percentage from them yields a number
that looks rigorous and means nothing.

```
objective O  →  metric_set M_O            declared in data/objectives/
normalize    n_m(e) = (v_m(e) − floor_m) / (frontier_m − floor_m)
perf(e,O)    = Σ w_m·n_m(e) / Σ w_m       over metrics with data
ratio(e,O)   = perf(e,O) / max_e perf(e,O)
```

Guards: **absolute floors** rather than min-max across candidates (min-max shifts
every score when a weak candidate is added) · **condition compatibility** —
metrics from different harnesses are never pooled · **coverage floor**, below
which an entity is `not_ratio_comparable` rather than extrapolated · **the
frontier is dated** · **noise band** from measured variance.

If the measurements do not exist, the engine refuses and names them. That refusal
is a research task, not a failure.

---

## 10. Stage 10 — Decide

Criterion selected by persona risk posture unless overridden:

| Posture | Criterion | Output |
|---|---|---|
| `high` | Maximize P(best) | "62% likely the best choice for you" |
| `medium` | Expected value with a regret cap | ranked, with worst-case bounded |
| `low` | Minimax regret | "never badly wrong under any plausible reading" |

Rules:

- Weights are always displayed.
- Coverage travels with the answer: "ranked on 8 of 13 dimensions."
- Confidence propagates as a **floor**, never a mean.
- **Near-ties are ties.** Differences inside the noise band are a band, not a
  podium.
- If no candidate exceeds a diffuse-probability threshold, return
  `INDISTINGUISHABLE` rather than a winner produced by rounding.
- Multi-objective queries return the **Pareto frontier**, not a single winner.
  Choosing among Pareto-equivalent options is the reader's call.

---

## 11. Stage 11 — Position

A stack is a position, not a purchase (DECISION §6):

```
position_value = present_fit
               − expected_decay(horizon)        ← D12 + observed release velocity
               − switching_cost                 ← from depends_on / bundles edges
               + option_value(substitutability) ← compatible alternatives per slot
```

Horizon comes from the query. A reader shipping in six weeks should weight option
value near zero, and can.

The reportable output: *"equal today; one has three drop-in substitutes per
layer, the other is one vendor across four layers. If you'll still be running
this in a year, they are not the same decision."*

---

## 12. Stage 12 — Budget frontier

For `marginal_value` queries, and computed for every budgeted query regardless:

```
  $0    baseline
  $20   large jump — KNEE, best value per dollar in range
  $25   marginal; the extra $5 buys ~nothing
  $45   next meaningful step — KNEE
  $90+  plateau
```

Derived and reported: **marginal capability per dollar** at the current spend ·
**cost of the road not taken** · **dominated spending ranges** where no stack
beats a cheaper one.

Telling someone their planned spend sits in a dead zone is among the most
valuable outputs available here, and nothing in this ecosystem currently does it.

---

## 13. Stage 13 — Explain

Six mandatory components, all generated from the computation, none hand-written.
**A recommendation missing any of them does not render.**

| # | Component | Generated from |
|---|---|---|
| 1 | Why this won | Dimension contributions ranked by marginal effect on the outcome |
| 2 | What was assumed | Usage profile, weights, horizon, criterion, reference date |
| 3 | What tradeoffs were accepted | What the runner-up was better at, in its own units |
| 4 | What evidence supports it | Claim → source → excerpt, with class and freshness per link |
| 5 | What uncertainty remains | P(best), distribution widths, unverified pairs, gaps |
| 6 | What would change it | Sensitivity margins (DECISION §7) |

Plus **value of information** (DECISION §8): which unknowns, if resolved, would
most change this answer — written into the gap register as research tasks.

---

## 14. Refusal

The engine must be able to say no. Refusal is a first-class output.

| Code | Meaning |
|---|---|
| `NO_CANDIDATES` | Constraints eliminated everything. Names the constraint. |
| `NO_MEASUREMENTS` | Objective needs continuous metrics that do not exist. Names them. |
| `INSUFFICIENT_COVERAGE` | Too few scored dimensions to compare. |
| `INDISTINGUISHABLE` | Within the noise band, or probability mass too diffuse. |
| `EVIDENCE_EXPIRED` | Everything relevant is past its decay window. |
| `BELOW_EVIDENCE_FLOOR` | Nothing meets the query's confidence/freshness floor. |
| `UNVERIFIED_ONLY` | Only untested combinations available. |
| `UNDER_DETERMINED` | Query lacks an input it cannot be answered without (e.g. a budget question with no usage model). |

Every refusal names **what evidence would resolve it**, and that list feeds the
gap register. The engine's failures become the research agenda.

---

## 15. Output

```yaml
result: recommendation | refusal
reference_date: 2026-08-03
criterion: minimax_regret
query_echo: { … }

pareto_set: [ … ]                # defensible choices, weight-free (stage 8)

stacks:
  - slots: { model: …, access: …, harness: … }
    p_best: 0.62
    max_regret: { cost_usd: 0, metric_points: 0, ordinal_ranks: 0 }
    coverage: "8/13 dimensions"
    confidence: moderate
    compatibility: verified | partially_unverified | untested
    cost:
      monthly_usd: 0
      usage_profile: use-…
      profile_status: assumed
      cost_confidence: low
      crossover_note: …
    position:
      option_value: …
      switching_cost: …
      expected_decay: …
    explanation:                 # all six, mandatory
      why_won: [ … ]
      assumptions: [ … ]
      tradeoffs_accepted: [ … ]
      evidence: [clm-…]
      uncertainty: { … }
      what_would_change_it: [ … ]

budget_frontier:
  points: [ … ]
  knees: [ … ]
  marginal_value_per_dollar: …
  dominated_ranges: [ … ]

value_of_information: [ … ]
weights_used: { … }
weights_status: opinion
eliminated: [ { constraint: …, removed: n } ]
```

---

## 16. Invariants

Enforced by tests, not convention.

1. **No entity, vendor, or product name appears in engine code.** It operates on
   slots, capabilities, constraints, dimensions, metrics, and costs.
   Grep-checkable. This is the extensibility guarantee.
2. Deterministic: same graph, query, date → identical output (fixed RNG seed for
   the Monte Carlo, recorded in the output).
3. Reversible: every number traces to claims to sources to excerpts. A broken
   chain means it does not render.
4. Weights always shown; never inferred from data.
5. Constraints eliminate; they never become soft penalties.
6. Confidence propagates as a floor.
7. Cost never appears without its usage profile and pricing date.
8. **Ratios never computed from ordinal scores.**
9. **Dominance is computed before any weight is applied.**
10. **All six explanation components present, or no render.**
11. Refusal always available; the engine is never forced to rank.
12. Historical replay: running against `graph_at(D)` reproduces what the Atlas
    would have said on D.

Invariant 12 makes the engine auditable against itself — replay past
recommendations against past evidence and check whether they held up. Publishing
the cases where they did not is the strongest available evidence that the
methodology is real.

---

## 17. Known weaknesses

- **Usage profiles are the weak link.** Every cost answer inherits their
  uncertainty.
- **Dimension independence is assumed and false.** Correlation between scores is
  unmodelled, which makes P(best) over-confident.
- **Stack effects are not additive.** Pairwise compatibility misses three-way
  interactions. Only Class D runs of assembled stacks fix this.
- **Combinatorial explosion.** Nine slots require aggressive pruning; pruning can
  hide good stacks. Rules are published and dated.
- **Personas encode our judgment.** Weights are opinion; overrides exist and
  weights are always visible.
- **The frontier is only as good as its measurements**, and early on there are
  very few. `NO_MEASUREMENTS` will be the most common refusal for months.
- **The decision layer degrades to a weighted sum when evidence is thin.** With
  one source per dimension, distributions are wide, dominance prunes nothing, and
  P(best) is flat. The sophistication earns its place only as the corpus fills —
  and showing that honestly early is correct behavior, not a deficiency to
  engineer around.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-08-03 | Reformulated as a constraint solver. Added the decision layer (DECISION.md): uncertainty propagation, dominance-before-weighting, risk-posture criteria, option value, budget frontier, sensitivity, VOI. Explanation contract made mandatory. Stacks-not-products enforced with single-tool queries as a degenerate case. |
| 1.0 | 2026-08-03 | Initial specification. |
