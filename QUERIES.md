# QUERY PROOFS

**Status:** v1.1 · **Last reviewed:** 2026-08-03 · **Purpose:** prove the data
model answers real questions *before* any research is done

Seven named questions, traced end to end through the schema, the graph, and the
engine. No data exists yet — the point is to establish that the *structure*
works and to find where it doesn't.

It didn't, in five places. Four are in §8. The fifth was Q7, which could not be
expressed at all and forced the entire decision layer
([DECISION.md](DECISION.md)).

---

## How to read a proof

Each query gives: the query object · the pipeline trace · the output shape ·
the data required · a verdict.

**Verdicts**

| | Meaning |
|---|---|
| ✅ **Structurally answerable** | The model produces a correct answer once the named data exists. No redesign needed. |
| ⚠ **Answerable with a caveat** | Answerable, but the honest answer differs from the question as asked. |
| ⛔ **Refuses, informatively** | The engine returns a refusal that names exactly what is missing. This is a success, not a failure. |

---

## Q1 — "I have $20/month. What's the best stack?"

```yaml
objective:  { kind: maximize, target: fit }
context:    { persona: null }
budget:     { ceiling_usd_month: 20, shape: hard }
scope:      { required_slots: [model, access, harness] }
```

**Trace**

1. **Resolve** — no persona given. Engine cannot weight dimensions without one,
   and cannot compute cost without a usage profile.
2. **Eliminate** — budget is a hard ceiling, but cost is a *function of usage*.
   $20 buys a subscription outright, or a wildly variable amount of metered
   inference.
3. **Cost** — this is where the query breaks as posed.

**The finding:** a budget query without a usage model is **under-determined**.
$20/month of metered access at light usage and at heavy usage are different
products. Answering with a single stack would require inventing a token count —
exactly the fabrication CLAUDE.md §1 prohibits.

The model's correct response is not a single answer but a
**usage-parameterized** one:

```
  at ~1M tokens/month   → subscription and metered are close; metered wins on flexibility
  at ~5M tokens/month   → subscription wins; metered exceeds ceiling
  crossover at N tokens → computed from RECOMMENDATION §6
```

This falls out of the cost model naturally and is a better answer than the
question asked for: the reader knows their own usage, and now knows where the
answer flips.

**Data required:** subscription-plan entities with allowances · metered pricing
as `step` facts · cache terms · default usage profiles per persona · free-tier
caps and fallback behavior.

**Verdict:** ⚠ **Answerable with a caveat.** The caveat is a feature. Surfaced a
new first-class requirement — see §8.1.

---

## Q2 — "I am a UI/UX designer who barely codes."

```yaml
objective:  { kind: maximize, target: fit }
context:    { persona: per-designer-engineer }
scope:      { required_slots: [model, access, harness, surface] }
```

**Trace**

1. **Resolve** — persona supplies `task_mix.frontend ≈ 0.7`,
   `expertise: learning`, `autonomy_appetite: hands_off`.
2. **Eliminate** — capability constraints derived from expertise: tools
   requiring deep CLI or git fluency are eliminated via
   `forbids_capability: cap-requires-git-fluency`, not by naming products.
3. **Score** — and here the model hits a wall it *should* hit.

**The finding:** the highest-weighted dimensions for this persona are D1 and D3
on **frontend** work. The available measurements in this ecosystem are
overwhelmingly repository-patching benchmarks, which do not measure frontend
generation at all.

Using them anyway would be a construct-validity error — the most common failure
in AI tool comparison, and one this Atlas exists partly to correct. So the model
must be able to *refuse a metric*, not just a query.

That mechanism did not exist. It does now: objectives declare metric sets,
benchmarks declare constructs, and the engine rejects any metric whose construct
does not match the objective. See §8.2.

4. **Anti-recommendations** — this persona's most useful output is often what to
   avoid: high-autonomy agents that produce large unreviewable diffs are
   `unsuitable_for` a reader who cannot review them.

**Data required:** frontend-specific measurements (Class D — the *frontend
fidelity* experiment already in METHODOLOGY §7) · D7 scores from convergent
Class C evidence · capability declarations for CLI/git prerequisites ·
anti-recommendation edges.

**Verdict:** ⛔ **Refuses, informatively** today: `NO_MEASUREMENTS` naming
frontend fidelity. ✅ once that experiment runs. The refusal is the right
behavior — this is the exact question the ecosystem currently answers with
irrelevant benchmarks.

---

## Q3 — "I want maximum autonomous coding."

```yaml
objective:  { kind: maximize, target: D2 }
context:    { persona: null }
```

**Trace**

1. **Resolve** — single-dimension maximization.
2. **The trap** — maximizing autonomy alone selects for the tool that runs
   longest without stopping, which is not the same as the tool that produces the
   most completed work. An agent that runs four hours and produces an
   unmergeable diff maximizes D2 and is useless.

**The finding:** pure `maximize` on one dimension is almost always the wrong
reading of the question. The model needs **implied guards** — declared floors
that travel with an objective, disclosed to the reader and overridable:

```yaml
objective: maximize D2
implied_guards:
  - { dimension: D4, min: 3 }   # reliability
  - { dimension: D5, min: 3 }   # maintainability of output
disclosure: "Autonomy is ranked with reliability and maintainability floors.
             Remove them to rank on raw autonomy alone."
```

3. **Score** — D2 is **ordinal**, and this query only needs a *ranking*, not a
   ratio. Ordinal scores are valid here. No frontier computation required.
4. **Band** — near-ties reported as a band.

**Data required:** D2 scores grounded in intervention-rate-per-completed-work
(Class D `long-horizon autonomy` experiment) · D4/D5 scores · `via` harness
context on every score, since autonomy is a property of the model-in-harness,
never of the model.

**Verdict:** ✅ **Structurally answerable.** The cleanest of the six: ordinal
ranking, no ratio, no cost model. Surfaced §8.4.

---

## Q4 — "I prefer APIs over subscriptions."

```yaml
objective:    { kind: maximize, target: fit }
preferences:  [ { facet: billing_model, prefer: metered } ]
```

**Trace**

1. **The finding, immediately:** "prefer" is not a constraint. Treating it as a
   hard filter silently discards better options; ignoring it disrespects the
   input. Neither is right, and v1.0 of the engine had only constraints.

**Preferences are now a distinct input type** (§8.3) with three effects:

- Re-rank rather than eliminate
- Surface the preferred option even if it doesn't win
- **Price the preference** — state what it costs

2. **Cost** — the crossover machinery from Q1 answers the interesting part
   directly:

```
  Preferred (metered):   $X/month at your usage profile
  Best overall:          $Y/month
  Your preference costs: $(X−Y)/month, and buys: no lock-in, per-model routing,
                         usage transparency
```

That is the honest answer to a stated preference: *here is what it costs and
what it buys*, not silent compliance.

3. **Capabilities** — metered access typically implies `cap-byok`,
   `cap-model-routing`, `cap-usage-transparency`; subscriptions typically imply
   `cap-cost-predictability`. The preference is really about these, and the
   engine can say so.

**Data required:** billing-model facets · pricing facts on both shapes · usage
profiles · capability declarations.

**Verdict:** ✅ **Structurally answerable**, and better than asked. Surfaced
§8.3.

---

## Q5 — "I need the best frontend generation."

```yaml
objective: { kind: maximize, target: metric.frontend_fidelity }
```

**Trace**

1. **Resolve objective** — `frontend_generation` declares its metric set:
   visual fidelity to brief · responsive correctness · accessibility baseline ·
   framework-idiomatic output · iteration cost to acceptable.
2. **Admissibility gate** (§8.2) — general coding benchmarks are **rejected**:
   their declared construct is repository patching, not interface generation.
3. **Frontier** — computed only over admissible metrics.
4. **Refusal** — with no admissible measurements, the engine returns:

```
  REFUSAL: NO_MEASUREMENTS
  objective: frontend_generation
  missing:
    - visual fidelity to brief        (no admissible measurement)
    - responsive correctness          (no admissible measurement)
    - accessibility baseline          (no admissible measurement)
    - iteration cost to acceptable    (no admissible measurement)
  rejected_as_inadmissible:
    - repository-patching benchmarks  (construct mismatch)
  resolves_with: exp-frontend-fidelity-v1
```

That refusal is a **more accurate answer than any currently published ranking of
"best AI for frontend."** Everything in the wild answers this with general
coding benchmarks, which do not measure it.

**Data required:** the frontend fidelity experiment, with a rubric fixed before
outputs are seen · Class C convergent evidence on iteration friction.

**Verdict:** ⛔ **Refuses, informatively** — and the refusal is the product.
✅ once the experiment runs.

---

## Q6 — "The cheapest stack with at least 90% of frontier performance."

```yaml
objective:
  kind: minimize_subject_to
  target: cost
  subject_to: [ { ratio_to_frontier: { gte: 0.9 } } ]
```

**Trace**

1. **The ordinal trap** — "90%" cannot be computed from 1–5 rubric scores.
   `0.9 × 5` is not a value on an ordinal scale, and the gaps between points are
   not equal by construction. RECOMMENDATION §7 forbids it outright: ratios come
   only from continuous measurements.

2. **"Frontier performance" at *what*?** — unscoped. The frontier for
   repository patching, long-horizon autonomy, and frontend generation are
   different sets of entities.

   The engine does not guess. It computes the ratio **per declared objective**
   and returns the comparison — which is itself the most useful finding:

```
  objective              90%-of-frontier stack        cost/mo   ratio
  ─────────────────────────────────────────────────────────────────────
  repository patching    …                            $…        0.9x
  long-horizon autonomy  …                            $…        0.9x
  frontend generation    …                            (refused: no measurements)

  → the "90% stack" is not one stack. It differs by what you actually do.
```

3. **Pareto** — within an objective, return the frontier of (cost, ratio), not a
   single winner. Points inside the noise band are equal.
4. **Coverage gate** — entities measured on under the coverage threshold are
   `not_ratio_comparable` and excluded rather than extrapolated.

**Data required:** continuous measurements under compatible conditions ·
declared metric floors and directions · variance estimates for the noise band ·
pricing + usage profiles · a dated frontier per objective.

**Verdict:** ⚠ **Answerable with a caveat** — and the caveat ("there is no
single frontier") is the correct correction to a question that assumes there is.
Partial refusal per objective where measurements are missing.

---

## Q7 — "How do I spend my next $25 most effectively?"

*Added with the decision layer ([DECISION.md](DECISION.md)). This is the query
that separates a research site from a decision tool, and v1.0 of the engine could
not express it at all.*

> **Numbers below are illustrative placeholders demonstrating output shape.**
> No entity is named; no figure is a claim. The graph is empty.

```yaml
objective:
  kind: marginal_value            # not "what is best at $25"
  target: fit
context:
  persona: per-solo-founder
  usage_profile: use-solo-founder-typical
  horizon_months: 12
budget: { ceiling_usd_month: 25, shape: soft }
decision_criterion: auto          # → minimax_regret? no: persona risk_tolerance is high → p_best
```

**Trace**

1. **Stages 1–6** — candidates, constraints, compatibility, cost across the whole
   budget range, not just at $25. A marginal-value query needs the *curve*, so
   cost is evaluated at every feasible spend level.
2. **Stage 7** — scores become distributions. With an empty corpus these are
   maximally wide, which is why this query currently refuses (§9).
3. **Stage 8 — dominance, weight-free.** Prune anything worse on every axis.
   Whatever survives is defensible without any opinion entering.
4. **Stage 12 — the budget frontier.** The actual answer.

**Output shape**

```
  BUDGET FRONTIER                                        persona: solo founder
                                                         usage: assumed (low conf.)
    $0     baseline capability
    $20    ████████████████  large jump      ← KNEE, best value/$ in range
    $25    █████████████████ +marginal       ← your stated budget
    $45    ████████████████████████  step    ← KNEE
    $90+   ███████████████████████████ plateau

  ANSWER
  Spend $20. The $20→$25 step buys ~3% additional capability — inside the
  noise band, so treat it as buying nothing.

  Your $21–$44 range is DOMINATED: no stack in it beats the $20 stack by a
  margin we can distinguish. Hold the $5.

  If you can reach $45, that step is worth ~6× the $20→$25 move per dollar.

  WHY THIS WON                        (ranked by marginal effect on the outcome)
  • autonomy (D2)          largest single contributor at your weighting
  • maintainability (D5)   you have no reviewer; this is a delayed autonomy cost
  • cost                   below ceiling with headroom for usage variance

  WHAT WAS ASSUMED                                              [all editable]
  • monthly usage          use-solo-founder-typical · ASSUMED · low confidence
  • horizon                12 months
  • criterion              p_best (from risk_tolerance: high)
  • weights                per-solo-founder · opinion · dated 2026-08-03

  TRADEOFFS ACCEPTED
  • runner-up scored higher on developer experience (D7) by ~1 rank
  • runner-up has 2 more drop-in substitutes at the harness slot

  UNCERTAINTY
  • P(best choice for you): 0.41 — a lean, not a verdict
  • widest distributions: D2, D5 (thin evidence)
  • 3 of 6 component pairs are UNVERIFIED — untested combination
  • cost confidence: LOW (usage assumed, not measured)

  WHAT WOULD CHANGE IT                                    ← sensitivity margins
  • FRAGILE  actual usage ±35% from assumption flips the recommendation
  • FRAGILE  D2 one rank lower flips it
  • robust   any single weight moving ±0.2 does not change the outcome
  • robust   D10/D11 at any plausible value do not change the outcome

  WORTH KNOWING NEXT                                    ← value of information
  1. measured usage profile     DECISIVE — resolves the most fragile input
  2. intervention-rate data     HIGH — narrows D2, the second fragile input
  3. ecosystem maturity scores  NEGLIGIBLE — changes nothing at any value
```

**What this demonstrates**

- The answer to a budget question is **"spend $20 and hold the $5"**, not a
  product name. That is the leap.
- **Dominated spending ranges** are reportable. Telling someone their planned
  spend sits in a dead zone is not available anywhere else in this ecosystem.
- P(best) = 0.41 is presented as a lean, not a verdict — the honest shape when
  evidence is thin.
- The **fragile inputs are named**, so the reader knows the answer hinges on a
  usage assumption rather than on tool quality.
- The engine **tells the research team what to measure next**, and explicitly
  licenses skipping the low-value item.

**Data required:** usage profiles · pricing as temporal step facts across the
whole budget range · D2/D5 scores with belief distributions · compatibility
edges · substitute counts per slot.

**Verdict:** ⛔ **Refuses today** with `UNDER_DETERMINED` — no measured usage
profile, and an assumed one is disclosed as the dominant source of error rather
than quietly used to manufacture precision. ✅ once T-030 and T-031 land.

---

## 7. Extensibility test

The brief's real requirement: no redesign when the ecosystem changes. Three
scenarios run against the model.

**A new model version ships.**
One entity, `version_of` + `endpoint_of` edges, endpoints per provider,
measurements attached to endpoints. Prior versions keep their measurements and
validity intervals. Frontier recomputes at the next reference date; historical
ratios stay correct because they are dated.
→ Zero schema change. Zero engine change.

**A new category emerges that nobody anticipated.**
Add a `role` value and a facet schema by TAXONOMY amendment; declare which
`capability` entities it provides; add a slot if it is independently choosable.
Existing predicates apply because domains are role-scoped, not type-scoped.
Constraints already written against capabilities pick it up immediately.
→ One amendment, no redesign. The engine never learns the category exists,
because it never references categories by name (RECOMMENDATION §11.1).

**A provider invents a new pricing shape.**
New predicate with a declared `temporal_kind`; one new term in the cost
function. Existing pricing facts and their history are untouched.
→ Additive change only.

The invariant that makes all three hold: **no entity, vendor, or product name
appears in engine code.** It is grep-checkable, and it is the difference between
a model that absorbs the ecosystem and one that is rebuilt every year.

---

## 8. What the proofs changed

Four gaps, found by running the queries rather than by reasoning about the
schema. This is why the exercise happened before research.

### 8.1 Usage profiles are first-class *(new entity type)*

Q1 and Q4 are unanswerable without them, and they cannot be invented. Added to
the schema as `usage_profile` with `status: assumed | measured` and a confidence
that propagates into every cost figure.

**Consequence for research:** measuring real token consumption per working
pattern moves to the front of the queue. It gates every cost question, and cost
questions are most of what readers ask.

### 8.2 Objectives declare metric sets; benchmarks declare constructs

Q2 and Q5 showed the engine could otherwise answer a frontend question with a
repository-patching benchmark — fluently, and wrongly. Now:

- Each `objective` entity declares its admissible metric set
- Each `benchmark` entity declares its `construct`
- The engine **rejects** metrics whose construct does not match, and reports the
  rejection

This makes construct validity a machine-enforced property rather than an
editorial hope, and it is the mechanism by which the Atlas structurally cannot
reproduce the field's most common error.

### 8.3 Preferences are distinct from constraints

Q4. Constraints eliminate; preferences re-rank, stay visible, and **get priced**.
"This preference costs you $X/month and buys you Y" is the answer a stated
preference deserves.

### 8.4 Objectives carry implied guards

Q3. Single-dimension maximization is almost always an incomplete reading of the
question. Objectives now declare guard floors, disclosed and overridable —
visible paternalism rather than either silent paternalism or a literal-minded
wrong answer.

---

## 9. Verdict summary

| Query | Verdict | Blocked on |
|---|---|---|
| Q1 $20/month | ⚠ usage-parameterized | usage profiles, pricing facts |
| Q2 designer who barely codes | ⛔ → ✅ | frontend fidelity experiment |
| Q3 maximum autonomy | ✅ | D2 scores from intervention data |
| Q4 APIs over subscriptions | ✅ | pricing facts, usage profiles |
| Q5 best frontend generation | ⛔ → ✅ | frontend fidelity experiment |
| Q6 cheapest at ≥90% frontier | ⚠ per-objective | continuous measurements, variance |
| Q7 next $25 most effectively | ⛔ `UNDER_DETERMINED` | measured usage profiles, pricing curve |

**No query required a redesign of the graph or temporal model.** Four additive
extensions came out of Q1–Q6; **Q7 forced the decision layer**
([DECISION.md](DECISION.md)) — v1.0's weighted sum could not express marginal
value, opportunity cost, or dominated spending at all.

### The research agenda this implies

The query set — not intuition — now sets research priority:

1. **Usage profiles** — gates Q1, Q4, Q6, Q7. Nothing about cost works without
   them, and Q7's sensitivity analysis names them the single most fragile input
   in the system.
2. **Pricing facts as temporal step records** — gates Q1, Q4, Q6, Q7. Q7 needs
   the whole curve, not a point.
3. **Frontend fidelity experiment** — gates Q2, Q5, and is unanswerable from
   public evidence, so the Atlas must generate it.
4. **Intervention-rate measurement** — gates Q3 and every autonomy claim.
5. **Continuous measurements under controlled conditions** — gates Q6 and every
   ratio.

Note what is *absent*: comprehensive per-tool feature coverage. The questions
readers ask do not require it. Researching breadth first would have been the
obvious move and the wrong one.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-08-03 | Added Q7 (marginal spend). It could not be expressed by the v1.0 engine and forced the decision layer. |
| 1.0 | 2026-08-03 | Initial proofs. Six queries traced; four model extensions surfaced and applied. |
