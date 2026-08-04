# RQ-07 — Does Claude Sonnet 5 use the newer tokenizer?

**Status:** accepted · **ERI:** Moderate · **Effort:** Trivial ⚡
**Flagship track:** no · **Opened:** 2026-08-03 · **Tracked as:** RG-001

---

## 1. Research question

**Does Claude Sonnet 5 use the tokenizer introduced with Claude Opus 4.7 (~30%
more tokens for identical text), or the previous one?**

## 2. Why it matters

Sonnet 5 is the mid-tier model most readers on a budget would land on, and its
effective cost depends on this by up to ~30% — **larger than the entire
introductory discount** currently in effect.

It is also a clean instance of a category the Atlas should handle well: **two
Class A sources from the same vendor that do not obviously agree.** How this is
resolved sets the pattern for every future documentation conflict, which is worth
more than the specific answer.

**Recommendation surface affected:** all Sonnet 5 cost claims; any comparison
between Sonnet 5 and pre-4.7-tokenizer models.

## 3. Current evidence

Two verbatim Class A sources, from one vendor, that cannot both be
straightforwardly true of Sonnet 5:

| Position | Source | Quote |
|---|---|---|
| Newer tokenizer applies broadly | `src-anthropic-pricing-2026-08-03` ex.5 | "Claude 4.7 and later models … use a newer tokenizer … approximately 30% more tokens … Claude Sonnet 4.6 and earlier models use the previous tokenizer." |
| Attribution is model-specific | `src-anthropic-models-overview-2026-08-03` ex.3 | Tooltip attached to **Claude Fable 5**: "uses the tokenizer introduced with Claude Opus 4.7" |

"Claude 4.7 and later" reads as a generation boundary that would include Sonnet 5.
But the overview attaches the tooltip only to Fable 5 and does not mark Sonnet 5's
context tooltip the same way. Sonnet 5 is named in neither list explicitly.

Recorded as `clm-claude-sonnet-5-090`, value `unknown`, with a `conflicts` block
and `likely_cause: unexplained`. **Not resolved by inference** — the inference is
plausible and the Constitution forbids manufacturing certainty from plausible.

## 4. Missing evidence

- A direct statement covering Sonnet 5
- An empirical token count for Sonnet 5 on a fixed corpus
- Whether the tokenizer maps to the *generation* or is chosen per model

## 5. Proposed experiments

### `exp-sonnet-5-tokenizer-identity-v1`

Resolvable in minutes, empirically, without waiting for documentation to improve.

1. Take a fixed text sample.
2. Submit it to Sonnet 5 and to a known pre-4.7-tokenizer model via the token
   counting endpoint (or read `input_tokens` from a minimal request).
3. Compare counts. A ~30% divergence settles it.

**Controls.** Identical text. Minimal system prompt, subtracted out. Repeat
across content types, since the vendor states the increase is content-dependent.

**Why this generalizes:** the same method resolves tokenizer identity for *any*
model whose documentation is silent, and folds directly into RQ-01's corpus. This
question is effectively RQ-01's smallest instance and a useful pilot for it.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.4** | Cost queries touching Sonnet 5 specifically |
| flip_probability | **0.35** | A 30% correction can flip which mid-tier model is cheapest |
| magnitude | **3/5** | Single-model correction, though a large one |

**ERI: Moderate**, ⚡ JUMP QUEUE on effort grounds alone. Lower breadth than RQ-01
because it concerns one model; near-zero cost to resolve.

## 7. Estimated effort

**Trivial.** Under an hour, plus negligible API spend.

**Binding constraint:** API access to both models. Nothing else.

## 8. Current confidence

**In the answer: low, leaning toward "yes, newer tokenizer"** on the plain
reading of "Claude 4.7 and later models". That lean is explicitly **not** encoded
in the graph — the claim sits at `unknown`, and the lean is recorded here as an
analyst's prior so that confirming it later cannot be mistaken for having known
it all along.

**In the question: high.** Cheap, unambiguous, and materially affects a
frequently-recommended model.
