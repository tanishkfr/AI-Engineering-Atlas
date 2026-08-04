# RQ-01 — Tokenizer normalization

**Status:** accepted · **ERI:** Decisive · **Effort:** Low ⚡ **JUMP QUEUE**
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**By what factor do vendor tokenizers differ in tokens produced for identical
text, and what is the resulting correction to published per-token prices?**

Falsifiable, deterministic, and answerable without any model inference.

## 2. Why it matters

Every price comparison in this ecosystem — ours included — implicitly assumes a
token is a common unit. It is not.

Anthropic documents that models from Claude 4.7 onward use a tokenizer producing
**~30% more tokens for the same text** than earlier models. If a single vendor's
own generations differ by 30%, cross-vendor comparison has no defensible basis at
all. Vendors have never shared tokenizers.

The correction is not cosmetic. A model priced 10% below a competitor can be
**more expensive per unit of actual work**. Every cost table, every budget
recommendation, and every "best value" claim the Atlas will ever publish depends
on getting this right first.

It is also, as far as we can find, **unpublished**. Vendors have no incentive to
publish a number that makes their headline price look worse, and comparison sites
do not appear to have noticed the problem exists.

**Recommendation surface affected:** all cost outputs, the budget frontier
(DECISION §5), `obj-cost-efficiency`, and `met-effective-token-multiplier`, which
was created as a design precaution and is now a measured requirement.

## 3. Current evidence

| Evidence | Source | Class | Fidelity |
|---|---|---|---|
| "~30% more tokens for the same text" for Claude 4.7+ | `src-anthropic-pricing-2026-08-03` ex.5 | A | verbatim |
| Same, attached to Fable 5 | `src-anthropic-models-overview-2026-08-03` ex.3 | A | verbatim |
| `clm-claude-fable-5-004` | — | — | published |

That is the entire evidence base: **one vendor, describing itself, qualitatively,
with "approximately".** Nothing cross-vendor. Nothing measured.

## 4. Missing evidence

- Token counts for a fixed corpus under each vendor's tokenizer
- Content-type sensitivity — the vendor says "depends on the content", and code
  vs prose vs structured data plausibly differ substantially. Code is the
  workload we care about, and it is the one least likely to match a general
  estimate.
- Whether the ~30% figure holds for code specifically
- Per-model tokenizer identity where vendors do not state it (see RQ-07)
- Whether tokenizer changes correlate with output-length changes — a model
  emitting more tokens per answer compounds the input-side effect on the
  expensive side of the bill

## 5. Proposed experiments

### `exp-tokenizer-normalization-v1`

**Design.** Deterministic, no inference, no API cost.

1. **Fixed corpus**, version-pinned and published, in five strata:
   `code/python` · `code/typescript` · `prose/documentation` · `structured/json`
   · `mixed/repository-context` (realistic agent context: file tree + several
   files + a diff).
2. **Tokenize** each stratum with every available vendor tokenizer, pinned by
   version.
3. **Report** tokens per stratum, per tokenizer, plus a normalized ratio against
   a declared reference tokenizer.
4. **Derive** `met-effective-token-multiplier` per model, and a corrected
   price-per-normalized-token for every pricing claim in the graph.

**Controls.** Identical byte-for-byte corpus. Tokenizer versions pinned and
recorded. No preprocessing, no normalization of whitespace — whitespace handling
is exactly where tokenizers differ and normalizing it away would destroy the
measurement.

**Preregistered prediction.** Cross-vendor spread on the code strata exceeds
20%, and is *larger* on code than on prose. Recorded before running so the
result cannot be narrated after the fact.

**Failure mode to guard against.** Some vendors do not publish a tokenizer.
Where a tokenizer is unavailable, the model is recorded as
`not_normalizable` and **excluded from cross-vendor price claims entirely**
rather than estimated. An estimated multiplier would silently reintroduce the
error this experiment exists to remove.

### `exp-tokenizer-normalization-v2` *(follow-on)*

Output-side measurement: same prompts, same task, count output tokens per vendor.
Requires inference and therefore cost; deferred until v1 establishes whether the
input-side effect is large enough to justify it.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **1.0** | Every cost-bearing query: Q1, Q4, Q6, Q7 directly; Q2/Q3/Q5 via stack cost |
| flip_probability | **0.7** | A ≥20% correction is larger than the gap between many adjacent options |
| magnitude | **4/5** | Reorders "cheapest" rankings; does not change feasibility |

**ERI: Decisive.**

Concretely: today the Atlas *cannot publish a cross-vendor price comparison at
all* without violating its own construct-validity rules. This experiment is the
gate. Until it runs, cost claims are single-vendor only.

## 7. Estimated effort

**Low.** Days, not weeks.

| Component | Effort |
|---|---|
| Corpus construction | ~0.5 day |
| Tokenizer acquisition and pinning | ~1 day, **binding constraint** |
| Measurement and reporting | ~0.5 day |
| Integration into the cost model | ~1 day |

**Binding constraint:** tokenizer *availability*, not compute. Where a vendor
ships a public tokenizer this is trivial; where they do not, the model is
excluded. No model access, no inference spend, no human judgment in scoring.

This is the best effort-to-impact ratio in the portfolio by a wide margin, which
is why it carries JUMP QUEUE.

## 8. Current confidence

**In the answer: low.** We are confident the effect is real and non-zero — one
vendor documents it — and we have **no basis whatsoever** for its cross-vendor
magnitude. The 20% preregistered prediction is a stated prior, not a finding, and
we would not be surprised to be wrong in either direction.

**In the question: high.** The problem is real, unambiguous, and blocks
downstream work.
