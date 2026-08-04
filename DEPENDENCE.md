# DEPENDENCE

**What holds a conclusion up, and what happens when you take it away.**

> *What evidence could disappear before this conclusion should disappear?*

This is the thesis. Everything else in the repository is either the corpus that
makes it demonstrable or the machinery that makes it computable.

Deliberately short. The project's previous failure mode was 47,000 words of
framework governing 50 claims; a document that restates the thesis five times is
the same mistake in a new costume.

---

## 1. Two questions that look alike and are not

| | Question | Operation |
|---|---|---|
| **Sensitivity** | What if the world were different? | change an **input** |
| **Dependence** | What if we stopped being entitled to this? | withdraw **evidence** |

Sensitivity is a property of a function. Dependence is a property of knowledge.

The instrument's dials express the first. Withdrawal expresses the second. A
recommendation that survives every dial can still be resting on one measurement
taken once, and only the second operation reveals it.

---

## 2. Support is not a count

A conclusion is computed from claims; claims are supported by sources; sources
are published by institutions. Counting any of those layers produces a number
that looks like strength and is not.

Three distinct situations, currently indistinguishable in the data:

| | Situation | Reading |
|---|---|---|
| **Corroboration** | two sources with independent causal access to the fact | genuine |
| **Duplication** | two sources, one publisher — a pricing page and an overview | **not** strength |
| **Derivation** | two publishers, one upstream of the other — a reseller quoting a vendor | **not** strength |

Duplication and derivation both *look* like corroboration in a source list.
Derivation is the more dangerous of the two, because the publisher names differ.

**Rule.** Support counts only where a source has a causal path to the fact that
does not pass through another counted source.

---

## 3. Not every claim can be corroborated, and that is not a defect

Corroboration is only meaningful where an external fact exists for two parties
to observe independently. For much of this corpus, it does not.

Mapped onto the claim types already defined in [SOURCES.md](SOURCES.md) §2:

| Type | Authority model | Can be independently corroborated? |
|---|---|---|
| **S** Specification | **Constitutive** — the vendor does not report the price, it *constitutes* it | **No.** A second source verifies transcription, not truth |
| **M** Measurement | **Observational** — an external fact exists | **Yes**, by replication. This is where fragility is real |
| **X** Experience | Observational, convergent | Yes, across independent practitioners |
| **T** Trend | Observational, convergent | Yes |
| **C** Comparative | **Interpretive** — synthesised, never observed | No. Attributed, not corroborated |
| **F** Forecast | Interpretive | Never published as fact |

The consequence for the interface is a distinction it must draw and currently
cannot:

- **Sole authority** — one source because only one can exist. Correct. Not fragile.
- **Under-corroborated** — one source because nobody else has looked. Fragile.

Rendering these identically would raise a false alarm on every price in the
corpus and drown the one signal that matters.

---

## 4. Corroboration does not protect against invalidity

A stable, replicable measurement of the wrong thing replicates perfectly.

The corpus already contains two instances, both found before this model was
written:

- **TTFT** measured as request-sent-to-first-token includes the entire reasoning
  phase for a reasoning model. Two labs measuring identically get identically
  incomparable numbers.
- **SWE-bench Verified** filters instances for solvability, so the score
  measures performance on a set selected partly by the thing being measured.

So a third axis, orthogonal to authority and to support:

**`construct_stable`** — is the thing being measured well defined for the
subjects being compared?

Where it is false, a replication counter is actively misleading. The honest
state is not `1 / 2 replications`. It is **replication will not fix this**.

---

## 5. Load, and what to research next

**Load** = how many published conclusions cease to be computable if this claim
is withdrawn. A graph property, computed, never asserted.

The research principle that follows:

> **Corroborate in proportion to load.**

Not "collect more evidence." A claim carrying eleven conclusions earns an
independent observation. A claim carrying none does not need corroborating — it
needs deleting.

This is [DECISION.md's](https://github.com/tanishkfr/AI-Engineering-Atlas) value
of information, rescued from a document that specified it and never ran it, and
made computable: **VOI is load, weighted by whether corroboration is even
possible for that claim's authority model.**

It licenses *not* researching things, which matters more than it sounds —
CONSTITUTION §14 caps coverage at maintenance capacity, so knowing what to skip
is worth as much as knowing what to chase.

### The pending-experiment rule

A projected impact must show **both branches**. "If replicated, eleven
conclusions strengthen" is half of the truth; the other half is "if it fails to
replicate, eleven conclusions retract." Showing only the favourable arm of a
pending experiment is precisely the overclaiming this project exists to refuse.

And replication widens scope, it does not remove it. Two operators is two
operators, not "operator-independent."

---

## 6. Withdrawal is discrete

Epistemic support does not degrade continuously. Nobody 60%-knows a price.

Withdrawing a redundant source must visibly do **nothing** — and that "nothing"
is the finding, because it means the conclusion was over-determined. Withdrawing
a load-bearing one must fail **at once**, with no easing and no elastic decay.
Anything that fades or stretches is an authored animation asserting a continuity
the epistemics do not have.

What does vary continuously is the **margin** — how much independent support
remains before failure. That is the honest analogue of confidence draining.

**Refusal is the terminal state of withdrawal.** Remove enough support and the
system does not produce a worse answer; it produces no answer. That state is
already built, already styled, already driven from `elicit.default: null`.
Withdrawal is the mechanism; refusal is where it ends.

---

## 7. What a conclusion must disclose

Carried over from the deleted recommendation spec, reduced to what the
dependency model actually obligates. Generated from the computation, never
written by hand. A conclusion missing any of these does not render.

| # | Component |
|---|---|
| 1 | **What it rests on** — the claim → source → excerpt chain, with class per link |
| 2 | **What was assumed** — defaults the reader never chose |
| 3 | **How independent that support is** — corroborated, duplicated, or derived |
| 4 | **What is load-bearing** — which single withdrawal ends it |
| 5 | **What remains unknown** — gaps stated as gaps, not omitted |
| 6 | **What would change it** — sensitivity margins *and* withdrawal thresholds |

---

## 8. The state of this corpus, measured

Run against the twelve claims the interface depends on, 2026-08-05:

```
every load-bearing claim:     exactly 1 publisher
independent corroboration:    0 of 12
withdraw Anthropic:           11 of 12 claims die
withdraw the cache measurement: every figure becomes uncomputable
```

Eleven of those are type **S** — constitutively single-sourced, correctly so.
One is type **M**: `clm-usage-cache-hit-001`, measured once, on one machine, over
56 days, and load-bearing for everything.

The instrument, built honestly, resolves to a single instruction: **one other
person needs to run that measurement.**

---

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-05 | Written on the subtraction branch. Absorbs value of information and the explanation contract from DECISION.md and RECOMMENDATION.md, both deleted. |
