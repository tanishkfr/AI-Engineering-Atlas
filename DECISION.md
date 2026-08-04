# DECISION FRAMEWORK

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Consumed by:**
[RECOMMENDATION.md](RECOMMENDATION.md) · **Depends on:**
[EVALUATION.md](EVALUATION.md), [TEMPORAL.md](TEMPORAL.md)

The decision science under the engine. This document exists because the engine's
first design was a weighted sum, and a weighted sum is not a decision procedure —
it is a ranking with the uncertainty thrown away at the last step.

---

## 0. What was wrong with v1.0

The v1.0 pipeline filtered candidates, computed `Σ w·score`, and banded the
result. Every comparison site does approximately this. Three specific failures:

1. **Uncertainty was a label, not an input.** Confidence was computed, attached
   to the answer, and then had no effect on *which answer came out*. In a domain
   where most evidence is thin and three months old, uncertainty should change
   the recommendation, not annotate it.
2. **No opportunity cost.** The engine could say "this is best at $20." It could
   not say "the 21st dollar buys nothing, and the next real step up is $45" —
   which is the actual question people are asking when they mention a budget.
3. **It treated a choice as terminal.** A stack is a *position*, not a purchase.
   Two stacks equal on today's evidence are not equal if one can be partially
   swapped next quarter and the other cannot. In an ecosystem that reprices and
   deprecates on a scale of months, that difference is often larger than the
   difference in measured quality.

What follows fixes those. Everything here is standard decision analysis; the
novelty is not the math, it is that nobody applies it to this domain.

---

## 1. Uncertainty is a distribution, not a label

A dimension score is not `4`. It is a **belief distribution over {1..5}**, whose
shape is determined by the evidence behind it.

```
  strong, corroborated, fresh        thin, single-source, aging
  ┌─────────────────────┐            ┌─────────────────────┐
  │        ▁▃█▃▁        │            │      ▂▄▅▆▅▄▂        │
  │      1 2 3 4 5      │            │    1 2 3 4 5        │
  │   mode 4, tight     │            │  mode 4, wide       │
  └─────────────────────┘            └─────────────────────┘
        both "score 4" — and they should not behave the same
```

The distribution is derived, never authored, from: number of independent
sources · source class admissibility · convergence for X/T claims · conflict
presence and severity · flag load · **age relative to the claim's decay
window**.

Decay matters more here than anywhere. As a score ages, its distribution does not
shift — it **widens**. We do not become wrong about a six-month-old score; we
become *less sure*. That is a materially different thing and the model should say
so.

### The ordinal guardrail

Distributions over ordinal categories are legitimate. Treating them as interval
quantities is not.

| Permitted | Forbidden |
|---|---|
| P(score ≥ 4) | "expected score 3.7" as a reportable quantity |
| P(A ranks above B) | "A is 18% better than B" |
| Regret expressed in ranks or probabilities | Regret expressed in utility points on an ordinal scale |
| Ratios on **continuous metrics and cost** (pass rate, dollars, latency) | Ratios on rubric dimensions |

Internal expectations may be computed for sorting. They are never displayed as
findings, and they never produce a percentage. This is the same rule that
governs frontier ratios (RECOMMENDATION §7), applied consistently.

---

## 2. Dominance before weighting

Weights are opinion (CONSTITUTION §3). So the engine establishes what is true
*without* them first.

**Stage A — dominance pruning, weight-free.**
Stack A dominates B if A is at least as good on every dimension and cost, and
strictly better on one. Dominated stacks are eliminated. **No weights are used
and no opinion enters.**

**Stage B — the Pareto set.** What survives is the set of defensible choices.
This is the objective part of the answer.

**Stage C — weights choose within the Pareto set.** Only now does persona
opinion enter, and it can only reorder options that were already defensible.

The epistemic payoff: the interface can show *"these six stacks are all
defensible; here is the one your priorities point to, and here is what changes if
your priorities differ."* Dominance is a fact about the evidence. Ranking is a
judgment about you. Keeping them in separate stages keeps them separable in the
output.

**Probabilistic dominance.** With distributions, dominance is also probabilistic:
A dominates B with probability p. Elimination requires p above a threshold
(default 0.9), so we do not discard a candidate on noise.

---

## 3. Probability of being the right choice

Rankings are the wrong output shape when evidence is thin.

By sampling the belief distributions (Monte Carlo over scores, costs, and
measurements), the engine computes:

```
  P(stack is the best choice for this persona)     ← the headline number
  P(stack is in the top band)
  P(stack ≻ specific alternative)
```

So the answer becomes:

```
  Stack A   62% likely to be the best choice for you
  Stack B   28%
  Stack C   10%
  → A is the better bet, not the proven winner. Section §7 says what would settle it.
```

That is a **materially more honest output than a ranked list**, and it is the
correct shape for the actual epistemic state of this ecosystem. A 34-point gap in
probability means something a "4.2 vs 3.9" does not.

When the top probability is low and diffuse — say nothing above 40% across four
candidates — the honest output is `INDISTINGUISHABLE`, and the engine says so
rather than reporting a winner produced by rounding.

---

## 4. Regret, and why it often outranks expected value

Maximizing expected fit is the right criterion when you know the distributions
well. We do not. The robust criterion for decisions under deep uncertainty is
**minimax regret**: choose the option whose worst-case shortfall, across
plausible states of the world, is smallest.

```
  regret(stack, state) = value(best stack in that state) − value(stack in that state)
  minimax choice        = argmin over stacks of max over states of regret
```

Where "states of the world" are draws from the belief distributions, plus
scenario states (§5).

Why this matters for this project specifically: a stack that is *never terrible*
under any plausible reading of thin evidence is frequently the right
recommendation, even when it never wins on expected value. That is precisely the
advice a good consultant gives and a leaderboard cannot.

**Regret units, per the §1 guardrail:**
- Cost regret → **dollars**. Real and reportable.
- Continuous-metric regret → **natural units** (percentage points of pass rate).
- Ordinal-dimension regret → **probability of being worse, and by how many
  ranks**. Never a synthetic utility gap.

**Which criterion runs is set by persona risk posture** — and this is where
`risk_tolerance` finally does real work instead of sitting decoratively in the
schema:

| Risk posture | Criterion |
|---|---|
| `high` | Maximize P(best) — chase the upside, tolerate variance |
| `medium` | Balanced: expected value with a regret cap |
| `low` | Minimax regret — never be badly wrong |

An enterprise team and a solo founder now receive genuinely different
recommendations from identical evidence, for a defensible reason, rather than
because someone nudged a weight.

---

## 5. Opportunity cost and the budget frontier

The user question is almost never "what is best at $X." It is **"what does my
next dollar buy?"**

The engine computes the **efficient frontier** of budget against capability, and
reports its **knees** — the points where marginal return changes sharply.

```
  capability
     ▲
     │                                    ╭──────────  ← plateau: more money buys nothing
     │                           ╭────────╯
     │                  ╭────────╯   ← knee 2
     │        ╭─────────╯
     │   ╭────╯  ← knee 1
     │  ╱
     └──┴────┴─────────┴──────────┴──────────────▶  $/month
        0   20        45         90
```

Output shape:

```
  $0     baseline capability
  $20    large jump — KNEE. Best value per dollar in the whole range.
  $25    +marginal. The extra $5 buys ~nothing.
  $45    next meaningful step — KNEE
  $90+   plateau; additional spend buys variance, not capability
```

So the answer to *"how should I spend my next $25?"* is not a product name. It is:

> **"Spend $20. The next $5 buys nothing measurable — hold it. If you can reach
> $45, that step is worth more than the $20→$25 move by a wide margin."**

Three derived quantities, all reportable:

- **Marginal capability per dollar** at the current spend level
- **Cost of the road not taken** — what a rejected stack would have given you, in
  the dimensions you deprioritized
- **Dominated spending** — budget ranges where *no* stack beats a cheaper one.
  Telling someone their planned spend sits in a dead zone is among the most
  valuable outputs available, and nothing in this ecosystem currently does it.

---

## 6. Option value: a stack is a position, not a purchase

Two stacks with identical present fit are not equal if one is replaceable and one
is a bet. In an ecosystem that reprices and deprecates on a scale of months, the
ability to swap a layer later has real value.

```
  position_value(stack) =
        present_fit
      − expected_decay(over horizon)          ← D12 continuity risk + release velocity
      − switching_cost(if forced to move)     ← lock-in, data portability, retraining
      + option_value(substitutability)        ← how many compatible alternatives exist
```

The inputs already exist in the graph:

- **Expected decay** — continuity risk (D12) plus observed release/deprecation
  velocity from the temporal record.
- **Switching cost** — how many slots move together if one is replaced, derived
  from `depends_on` and `bundles` edges. A stack whose harness, surface, and
  model are one product has a switching cost of "all of it."
- **Option value** — count and quality of `alternative_to` candidates that are
  compatible with the *rest* of the stack. A slot with four viable substitutes is
  cheap to be wrong about; a slot with none is a bet.

The output that follows is one the domain badly needs:

> *"These two stacks are equal today. The first has three drop-in substitutes for
> every layer. The second is a single vendor across four layers with one
> alternative. If you expect to still be running this in a year, they are not the
> same decision."*

Horizon is a query parameter. Someone shipping in six weeks should weight option
value near zero, and the engine should let them.

---

## 7. Sensitivity: what would change this?

Required by the explanation contract (§9). Computed, not narrated.

For every input — weight, score, price, usage assumption, measurement — compute
**how far it must move before the recommendation changes**, then report the
inputs with the smallest margins.

```
  FRAGILE INPUTS
  • assumed monthly token volume — recommendation flips if actual usage is
    ±35% from assumption                                    ← most fragile
  • D2 autonomy score for the leading stack — flips if it is 1 rank lower
  • price of the access layer — flips at +$8/month

  ROBUST TO
  • all D10/D11 scores (no plausible movement changes the outcome)
  • persona weight changes within ±0.2 on any single dimension
```

Two consequences worth stating:

1. **A fragile recommendation is disclosed as fragile.** "This answer hinges
   almost entirely on a usage assumption we have not measured" is more useful
   than a confident ranking.
2. **Robustness is itself a finding.** "This holds across every reasonable
   weighting and any usage in this range" is a strong result and currently
   unreportable anywhere else.

---

## 8. Value of information: the engine writes the research agenda

The closing loop, and the piece that makes this system self-directing.

For each *unknown* — an unscored dimension, an unmeasured metric, an assumed
usage profile — estimate how much resolving it would change recommendations:

```
  VOI(unknown) = E[ change in chosen stack across the query population
                    if this unknown were resolved ]
```

Rank the unknowns. Publish the ranking. **That ranking is the research
priority.**

```
  HIGHEST VALUE RESEARCH (computed 2026-08-03)
  1. measured usage profiles              affects 5 of 7 standard queries
  2. frontend fidelity measurement        affects 2, currently unanswerable
  3. intervention rate per completed work affects 1, plus every autonomy claim
  …
  LOW VALUE
  •  ecosystem maturity scores            changes no recommendation at any
                                          plausible value
```

M2 reached this conclusion by hand (QUERIES §9). §8 makes it **continuous and
quantitative**: as the corpus grows and the query log accumulates, the engine
keeps recomputing what is worth knowing next.

It also licenses *not* researching things. "Ecosystem maturity scores change no
recommendation" is permission to stop — and CONSTITUTION §14 caps coverage at
maintenance capacity, so knowing what to skip is as valuable as knowing what to
chase.

---

## 9. The explanation contract

Every recommendation carries six components. All generated from the computation,
none written by hand. A recommendation missing any of them does not render.

| # | Component | Source |
|---|---|---|
| 1 | **Why this won** | Dimension contributions ranked by marginal effect on the outcome — not a score dump |
| 2 | **What was assumed** | Usage profile, weights, horizon, reference date, defaults the reader never chose |
| 3 | **What tradeoffs were accepted** | What the runner-up was better at, in what units |
| 4 | **What evidence supports it** | Claim → source → excerpt chain, with class and freshness per link |
| 5 | **What uncertainty remains** | P(best), distribution widths, unverified compatibility pairs, gaps |
| 6 | **What would change it** | Sensitivity margins from §7 |

Component 3 is the one most systems omit and the one a reader most needs: **the
runner-up was better at something, and you should know what you gave up.**

Component 2 deserves emphasis too. Most of what determines a recommendation is
assumptions the reader never made — how much they use it, how long they'll keep
it, how much they care about cost. Surfacing those *as editable* turns a verdict
into a model the reader can argue with, which is the correct relationship between
a research tool and a person making a decision.

---

## 10. Stacks, not products

**The unit of recommendation is a stack.** Single-tool queries are a degenerate
case — a stack with one slot open and the rest held fixed or marked unspecified.
One code path, no special casing.

Why this is enforced rather than preferred: "which model is best" is close to
unanswerable and reliably misleading, because observed quality is produced by a
model *inside* a harness, reached through an access path, with some context
layer. Recommending a component in isolation smuggles in unstated assumptions
about everything around it. Recommending a stack makes those assumptions
explicit — they become slots with named occupants.

When a reader asks about one tool, the honest answer is: *here is what it is good
at, and here is the stack it belongs in for your situation.*

Formally this makes the engine a **constrained combinatorial optimization**:
assign entities to slots, subject to compatibility edges, capability
requirements, and a budget — maximizing a risk-adjusted objective. Not a sort.

---

## 11. Portfolio allocation

You do not have to pick one. Routing cheap work to a cheap component and hard
work to an expensive one is a real strategy and often dominates any single
choice.

The optimizer may therefore return a **mix**:

```
  70% of tasks →  slot occupant A
  30% of tasks →  slot occupant B    (the long-horizon and frontend work)

  vs. best single choice: −34% monthly cost, −3% capability on the mixed workload
```

Requirements before this is trustworthy: a task-mix decomposition in the persona
(present), per-task-class measurements (missing — a Class D dependency), and
honest accounting of the **switching friction** of running two things, which is
not zero and must be a term, not an omission.

Until per-task-class measurements exist, portfolio output is marked
`unvalidated` and shown as an option to consider, never as a recommendation.

---

## 12. Honest limits

Stated plainly, because a decision framework that hides its own fragility is
worse than a weighted sum that admits to being one.

- **Belief distributions are constructed, not observed.** Their shapes come from
  our heuristics about evidence strength. Reasonable people would construct them
  differently, and the outputs would move. The heuristics are published and
  versioned; that is mitigation, not a solution.
- **Monte Carlo over ordinal beliefs is a modelling convenience.** It assumes
  independence between dimension scores that does not hold — cost and autonomy
  interact, speed trades against quality. Correlation structure is currently
  unmodelled and is a known source of over-confidence in P(best).
- **Minimax regret can be too conservative.** It optimizes against a worst case
  that may be implausible. Which criterion applies is set by persona and is
  always disclosed.
- **VOI depends on a query population** we do not yet have. Early estimates use
  the seed question index and are labeled as such. It gets better with usage and
  is worth little at launch.
- **Option value uses estimated horizons.** Nobody knows how long a tool remains
  viable. D12 is a scored judgment, not a measurement, and the decay term
  inherits that softness.
- **Everything above degrades to the v1.0 weighted sum when evidence is absent.**
  With one thin source per dimension, distributions are wide, dominance prunes
  nothing, and P(best) is flat. The sophistication earns its place only as the
  corpus fills. Early outputs will be mostly refusals and wide bands — and
  showing that honestly is the correct behavior, not a deficiency to engineer
  around.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial framework. Replaces the v1.0 weighted-sum ranking with dominance-first, uncertainty-propagating, regret-aware optimization; adds opportunity cost, option value, sensitivity, and value of information. |
