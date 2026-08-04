# PREREGISTRATION — `exp-tokenizer-normalization-v1`

**Study:** RQ-01 Cross-Vendor Token Economics
**Preregistered:** 2026-08-03 · **Status:** FINALIZED — no changes after data collection begins
**Operator:** atlas-editorial

> **Preregistration integrity.** This document was written after a capability
> probe (`scripts/experiments/probe_capability.py`, which established *which
> tokenizers are reachable*) and **before any measurement on the study corpus**.
> The probe used a single throwaway string (`def hello():\n    return 1\n`) that
> is deliberately **not** part of the corpus. Hypotheses below are fixed.

---

## 1. Research question

By what factor do vendor tokenizers differ in tokens produced for identical
text, and what correction does that imply for published per-token prices?

## 2. Motivation

Every per-token price comparison in this ecosystem assumes a token is a common
unit across vendors. It is not, and vendors have never shared tokenizers.

Anthropic documents that its own models from Claude 4.7 onward produce
"approximately 30% more tokens for the same text" than earlier models
(`src-anthropic-pricing-2026-08-03` ex.5, verbatim Class A). If one vendor's own
generations differ by ~30%, cross-vendor comparison has no established basis.

The Atlas currently **cannot publish any cross-vendor price comparison** without
violating its own construct-validity rules. This study is the gate.

We could find no public measurement of this. Vendors have no incentive to publish
a figure that worsens their headline price.

## 3. Hypotheses

Fixed before data collection.

| ID | Hypothesis | Direction |
|---|---|---|
| **H1** | Cross-vendor spread (max/min tokens for identical text) on code strata **exceeds 20%** | one-tailed |
| **H2** | Spread is **larger on code than on prose** | directional |
| **H3** | Within-vendor generational spread is smaller than cross-vendor spread | directional |

H1 and H2 are carried forward verbatim from `RQ-01-tokenizer-normalization.md`
§5, written 2026-08-03 before any tokenizer was loaded. H3 is added here and is
new; it is marked as such so it cannot later be presented as long-held.

## 4. Success criteria

The study **succeeds** if it produces, for every reachable tokenizer, token
counts on all five corpus strata, plus a normalization table against a declared
reference — regardless of whether the hypotheses hold.

**Success is not contingent on the hypotheses being confirmed.** A result showing
spread below 20% would be a valuable negative finding: it would mean per-token
prices are more comparable than we claimed, and the Atlas would have to retract
the framing in `research/findings-2026-08-03.md` F1.

## 5. Failure criteria

The study **fails** (and publishes as failed) if:

- Fewer than three vendor tokenizer families are reachable
- Tokenizer versions cannot be pinned, making the result unreproducible
- The corpus cannot be published, making the result unverifiable

## 6. Threats to validity

| Threat | Severity | Mitigation |
|---|---|---|
| **Anthropic and Google are unmeasurable offline** — no public tokenizer; counts require an API key we do not have | **Severe** | They are excluded as `not_normalizable`, not estimated. This is a coverage hole in exactly the vendors our pricing corpus covers best, and the report leads with it. |
| Tokenizer ≠ model. A repo's tokenizer may not be the one used in the served endpoint | High | Report measures *published tokenizers*, not endpoints. Scope stated explicitly. |
| Corpus non-representativeness — five strata are not "all code" | High | Strata reported separately, never averaged into a single headline number. |
| Chat templates and special tokens inflate counts differently per vendor | Medium | Raw text only, no chat template applied. Recorded as a scope limit. |
| Llama gated (401) — a major open-weight family excluded | Medium | Reported as a gap; not substituted with a proxy. |
| Version drift — tokenizers change | Medium | Repo revision hashes recorded where available. |
| Corpus authored by the operator may unconsciously favour a tokenizer | Low–Medium | Corpus is mechanical/idiomatic, written before any counts were seen, and published in full. |

## 7. Variables

- **Independent:** tokenizer (vendor × version); corpus stratum
- **Dependent:** token count for a fixed byte sequence
- **Derived:** normalization ratio vs reference; price per normalized token
- **Controlled:** byte-identical input; no preprocessing; no chat template
- **Uncontrolled:** tokenizer training corpus; vendor tokenization strategy

## 8. Assumptions

1. The tokenizer published in a vendor's public repo is the tokenizer used for
   billing that vendor's models. **Unverified** — a stated assumption, not a fact.
2. Token counts are deterministic for a given tokenizer and input.
3. Whitespace handling is a real difference and must not be normalized away.
4. `o200k_base` is the appropriate encoding for current OpenAI models.
   **Assumption**, based on it being the newest general encoding shipped; not
   confirmed against per-model documentation.

## 9. Methodology

**Corpus.** Five strata, ~1–3 KB each, version-pinned and published in full at
`research/experiments/corpus/`:

| Stratum | Content |
|---|---|
| `code_python` | Idiomatic Python: classes, type hints, docstrings, comprehensions |
| `code_typescript` | Idiomatic TS: interfaces, generics, async, JSX-free |
| `prose_documentation` | Technical prose, no code blocks |
| `structured_json` | Nested JSON config with realistic key names |
| `mixed_repo_context` | Realistic agent context: file tree + two files + a unified diff |

**Procedure.**
1. Load each reachable tokenizer, pinned by version/revision.
2. Encode each stratum. Record token count and byte length.
3. Compute tokens-per-1000-bytes per (tokenizer, stratum).
4. Compute ratio against the declared reference tokenizer.
5. Apply ratios to captured pricing to produce price-per-normalized-token.

**Reference tokenizer:** `cl100k_base`. Chosen because it is the most widely
deployed historical encoding and is not the newest from any vendor, so it does
not privilege a current model. **Declared before running.** The choice of
reference affects only presentation; all pairwise ratios are reference-invariant.

## 10. Planned analysis

- Token counts per (tokenizer, stratum) — full matrix, no aggregation
- Spread = max/min per stratum → **tests H1** (threshold 1.20)
- Compare code-stratum spread vs prose-stratum spread → **tests H2**
- Compare within-vendor vs cross-vendor spread → **tests H3**
- Price correction applied only to vendors with both a reachable tokenizer *and*
  captured pricing

**No aggregation across strata into a single "spread" figure.** The vendor
states the effect is content-dependent; averaging would destroy the finding.

## 11. Stopping conditions

- **Stop and publish** once all reachable tokenizers have been run on all strata.
  Single deterministic pass; no replication needed (no stochasticity).
- **Stop and publish as failed** if fewer than three vendor families load.
- **Do not** add tokenizers after seeing results to change a conclusion. The
  candidate list is fixed at: OpenAI (tiktoken), Qwen, DeepSeek, Mistral, Llama.

## 12. Replication instructions

```bash
python scripts/experiments/probe_capability.py
python scripts/experiments/exp_tokenizer_normalization.py
```

Outputs `research/experiments/results/tokenizer-normalization-v1.json`.
Corpus is in-repo. Requires network on first run for HuggingFace tokenizers;
tiktoken encodings may also fetch on first use.

**Recorded for reproducibility:** Python version · package versions · tokenizer
repo IDs and revisions · corpus SHA-256 · run date. No random seeds — the
procedure is deterministic.

## 13. Expected Recommendation Impact

| Component | Estimate |
|---|---|
| breadth | 1.0 — every cost-bearing query |
| flip_probability | 0.7 |
| magnitude | 4/5 |

**ERI: Decisive.** Gates all cross-vendor cost claims.

## 14. Required tooling

Python 3.11.9 · `tiktoken` 0.12.0 · `tokenizers` 0.22.2 · `transformers` 5.1.0 ·
network for tokenizer download. **No model API access. No inference.**

## 15. Estimated cost

**$0.00.** No inference. Compute is negligible. This is why the study carries
JUMP QUEUE.

## 16. Ethical considerations

Tokenizers are downloaded under their published licences and used for
measurement only; no weights are used and no model is run. The corpus is
operator-authored, avoiding any third-party licensing question. No personal data.
