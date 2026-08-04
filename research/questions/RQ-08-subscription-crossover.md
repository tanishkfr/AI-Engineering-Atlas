# RQ-08 — Subscription vs metered crossover

**Status:** accepted · **ERI:** High · **Effort:** Low ⚡
**Flagship track:** no · **Opened:** 2026-08-03

---

## 1. Research question

**At what usage level does a subscription plan become cheaper than metered API
access, and how does that crossover move with cache hit rate and model choice?**

## 2. Why it matters

*"I have $20/month"* is the first of the Atlas's primary questions and is
currently **completely unanswerable**. No subscription-plan entity exists in the
corpus.

The right output is not a product name but a **crossover point** — the usage at
which the cheaper option flips (RECOMMENDATION §6). The reader knows their own
usage far better than we do; give them the threshold and they can place
themselves on it.

This also determines the honest answer to *"I prefer APIs"* (Q4). A stated
preference deserves to be **priced**: *this preference costs you $X/month at your
usage, and buys you no lock-in, per-model routing, and usage transparency.*
Without subscription data we can state the benefits and not the cost.

**Recommendation surface affected:** Q1, Q4, Q7 — three of seven standard
queries, and the entire budget frontier below roughly $100/month.

## 3. Current evidence

| Evidence | Source | Class |
|---|---|---|
| Full metered API pricing for one vendor | `src-anthropic-pricing-2026-08-03` | A, verbatim |
| Spend caps by tier (Start $500 / Build $1,000 / Scale $200,000) | `src-anthropic-rate-limits-2026-08-03` ex.0 | A, verbatim |
| Four usage profiles | `data/usage/usage-profiles.yaml` | **all `assumed`** |

**Zero subscription-plan evidence.** The metered half of the comparison is
well-sourced; the subscription half does not exist in the corpus at all.

## 4. Missing evidence

- Subscription plan entities: price, included allowance, overage behaviour, model
  access, rate limits
- Whether subscription plans expose the same models as the API — if a plan gates
  the frontier model, the comparison is not like-for-like
- Whether subscription usage is measured in tokens at all, or in opaque units
  that make the crossover *incomputable in principle* rather than merely unknown
- Fair-use and throttling policy under sustained load
- Measured usage profiles (RQ-03 dependency) — without them, the crossover is a
  function whose input is a guess

## 5. Proposed experiments

### `exp-subscription-crossover-v1`

Not an experiment so much as a **modelling exercise on captured pricing**, which
is why effort is low.

1. Capture subscription plan terms as temporal `step` facts, same discipline as
   API pricing.
2. For each usage profile, compute monthly cost under (a) subscription, (b)
   metered, (c) mixed.
3. Solve for the crossover token volume; report as a **surface** across cache hit
   rate and model tier, not a single number — the crossover moves substantially
   with caching, since caching only benefits the metered side.
4. Identify **dominated ranges** (DECISION §5): usage bands where one option is
   never right.

**Preregistered prediction.** The crossover is *lower* than commonly assumed —
metered access beats subscriptions at surprisingly modest usage once caching is
active — because cache reads at 0.1× base input are not reflected in
subscription pricing.

### Honest limitation

If subscription plans do not disclose token allowances, the crossover cannot be
computed from published terms and would require measured consumption under a
subscription. In that case the finding becomes *"this comparison is not publicly
computable"* — which is a legitimate and useful published result, not a failure.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.45** | Q1, Q4, Q7 |
| flip_probability | **0.8** | The question is currently unanswerable; almost any answer changes the output |
| magnitude | **4/5** | Determines the entire recommendation below ~$100/month, where most readers sit |

**ERI: High**, with ⚡ JUMP QUEUE — it is mostly capture and arithmetic.

## 7. Estimated effort

**Low.** Days.

| Component | Effort |
|---|---|
| Subscription plan capture | ~1 day |
| Crossover modelling | ~1 day |
| Surface generation and integration | ~1 day |

**Binding constraint:** whether plan terms are published in computable form. If
allowances are opaque, effort rises sharply and the deliverable changes shape.

## 8. Current confidence

**In the answer: very low** — we have not captured a single subscription plan.

**In the question: very high.** It is the single most-asked question this project
exists to answer, and it is the largest hole in the corpus.
