# Cross-Vendor Token Economics

**Technical report · `exp-tokenizer-normalization-v1`**
**Study:** RQ-01 · **Run:** 2026-08-04 · **Preregistered:** 2026-08-03
**Status:** complete, with a material coverage limitation
**Cost:** $0.00 · **Reproducible:** yes

> ## ⚠️ CORRECTION — 2026-08-04, issued by RQ-01a
>
> **§10's generalization was too broad and is corrected here.**
>
> This report concluded that cross-vendor per-token prices are "not comparable
> without normalization", citing a 1.33× spread. That spread was **driven by
> `Mistral-7B-Instruct-v0.3`, an older tokenizer generation that is not the
> tokenizer of any currently-priced model.**
>
> A follow-up study (`exp-normalized-cost-v1`) measured only models with captured
> pricing and exact tokenizer matches. Among those, the spread is **1.03–1.11×**,
> and **normalization changed no cost ranking in any of the five strata**, because
> posted prices span 263× while token counts span 11%.
>
> **Corrected conclusion:** normalization changes a ranking only when posted
> prices differ by **less than ~11%**. Above that, it refines magnitude without
> altering the decision.
>
> **The measurements in this report stand unchanged.** Only the interpretation in
> §7 and §10 is narrowed. See `M4.1-BLOCKER-RESOLUTION.md` Blocker 4.

---

## 1. Executive summary

We measured how many tokens six vendor tokenizers produce for byte-identical
text across five content strata. All three preregistered hypotheses were
supported.

**Headline result: a 33% cross-vendor spread on code.** Identical Python source
costs 503 tokens under OpenAI's `cl100k_base` and 670 tokens under Mistral's
tokenizer — a **1.33× difference in billable units for the same work**. On
structured JSON the spread reaches 1.34×.

**Second, unpredicted result — and the more consequential one:** *within-vendor*
generational drift is nearly as large as cross-vendor difference. OpenAI's own
`p50k_base` → `cl100k_base` transition changed code token counts by up to
**1.27×**. This means Anthropic's documented "~30% more tokens" for its newer
tokenizer is **not unusual** — it is typical of tokenizer generational shifts.
The implication is broader than one vendor: **any vendor may have changed
tokenizers between model generations without documenting it**, and comparisons
across a vendor's own product line may be as unsound as comparisons across
vendors.

**Material limitation, stated up front:** we could not complete the price
correction the study was designed to produce. The vendors whose pricing we have
captured (Anthropic, Google) publish **no offline tokenizer**, and the vendors
whose tokenizers we can reach (Qwen, DeepSeek, Mistral) have no pricing captured.
**The two sets do not intersect.** The measurement stands; the price correction
does not yet exist for any vendor pair.

---

## 2. Background

The Atlas captured Anthropic pricing documentation on 2026-08-03 which states,
verbatim:

> "This tokenizer produces approximately 30% more tokens for the same text. The
> exact increase depends on the content and workload shape."
> — `src-anthropic-pricing-2026-08-03` ex.5, Class A, verbatim

That disclosure implies per-token prices are not comparable even within one
vendor's product line. Whether the same holds across vendors was unknown, and we
could find no public measurement. Vendors have no incentive to publish a figure
that worsens their headline price.

Under the Atlas's construct-validity rules this blocked all cross-vendor cost
publication (`obj-cost-efficiency`, `met-effective-token-multiplier`).

## 3. Research question

By what factor do vendor tokenizers differ in tokens produced for identical
text, and what correction does that imply for published per-token prices?

## 4. Why this matters

A model priced 10% below a competitor can be **more expensive per unit of actual
work** if its tokenizer is 20% less efficient on your content type. Every price
table, budget recommendation, and "best value" claim depends on this.

The finding also affects the Atlas's own budget frontier: knee positions
(DECISION §5) shift when effective prices shift, and a knee moving past a
reader's stated budget changes the recommendation entirely.

## 5. Methodology

Full protocol: [`PREREG-exp-tokenizer-normalization-v1.md`](PREREG-exp-tokenizer-normalization-v1.md).
Finalized before any measurement on the study corpus.

**Corpus.** Five operator-authored strata, published in full at
`research/experiments/corpus/`, SHA-256 recorded per file. Operator-authored to
avoid third-party licensing questions and written before any counts were seen.

| Stratum | Bytes | SHA-256 (first 12) |
|---|---|---|
| `code_python` | 1,920 | `be98433f30f6` |
| `code_typescript` | 1,773 | `9808cf7a4ec9` |
| `prose_documentation` | 2,043 | `ce512190f699` |
| `structured_json` | 1,849 | `4df57eb0dc7b` |
| `mixed_repo_context` | 2,302 | `05275654646d` |

**Procedure.** Each tokenizer encodes each stratum. Raw text only — no chat
template, no special tokens (`add_special_tokens=False`). Counts, tokens per
1000 bytes, and ratios against the declared reference (`cl100k_base`, chosen in
the preregistration precisely because it is nobody's newest encoding).

**Deterministic.** No sampling, no seeds, no inference, no API calls.

## 6. Results

### 6.1 Raw token counts

| Tokenizer | py | ts | prose | json | mixed |
|---|---|---|---|---|---|
| openai/`o200k_base` | 507 | 448 | **407** | **571** | **678** |
| openai/`cl100k_base` | **503** | **446** | 409 | 572 | **678** |
| openai/`p50k_base` | 626 | 568 | 427 | 704 | 830 |
| qwen/Qwen2.5-Coder-7B | 523 | 446 | 409 | 611 | 729 |
| deepseek/DeepSeek-V3 | 541 | 465 | 410 | 606 | 702 |
| mistral/Mistral-7B-v0.3 | 670 | 581 | 449 | 766 | 893 |

Bold = minimum for that stratum.

### 6.2 Cross-vendor spread (max ÷ min)

| Stratum | Spread | Cheapest | Most expensive |
|---|---|---|---|
| `structured_json` | **1.342** | openai/o200k | mistral |
| `code_python` | **1.332** | openai/cl100k | mistral |
| `mixed_repo_context` | **1.317** | openai/o200k | mistral |
| `code_typescript` | **1.303** | openai/cl100k | mistral |
| `prose_documentation` | 1.103 | openai/o200k | mistral |

### 6.3 Within-vendor spread (OpenAI generations only)

| Stratum | Spread |
|---|---|
| `code_typescript` | 1.274 |
| `code_python` | 1.245 |
| `structured_json` | 1.233 |
| `mixed_repo_context` | 1.224 |
| `prose_documentation` | 1.049 |

### 6.4 Preregistered hypothesis outcomes

| ID | Hypothesis | Threshold | Observed | Result |
|---|---|---|---|---|
| H1 | Cross-vendor code spread > 1.20 | 1.20 | **1.332** | ✅ supported |
| H2 | Code spread > prose spread | — | 1.332 vs 1.103 | ✅ supported |
| H3 | Within-vendor spread < cross-vendor spread | — | 1.274 vs 1.342 | ✅ supported, **narrowly** |

## 7. Analysis

**H1 — confirmed, and the magnitude matters.** A 1.33× spread on code exceeds
the price gap between many adjacent model tiers. Comparing two vendors on posted
per-token price, without normalization, can invert the true ranking.

**H2 — confirmed, with a large margin.** Code spread (1.33) is triple prose
spread (1.10) in excess-over-parity terms. Tokenizers differ most on exactly the
content this domain cares about. **A general-purpose "tokens are roughly
comparable" heuristic derived from prose is actively misleading for code.**

**H3 — supported, but the near-miss is the finding.** We predicted within-vendor
drift would be clearly smaller. It is smaller by only 0.068 (1.274 vs 1.342).
OpenAI's own generational transition moved code counts ~24–27%, which is
statistically indistinguishable in practical terms from Anthropic's documented
~30%.

Three consequences follow:

1. **Anthropic's ~30% disclosure is unremarkable, not exceptional.** It is
   consistent with a generational tokenizer change at another vendor. We should
   stop treating it as an Anthropic-specific quirk.
2. **The disclosure itself is the outlier, not the effect.** Anthropic documented
   the change. We have no evidence other vendors document theirs — and OpenAI's
   `p50k`→`cl100k` shift is visible only because both encodings remain publicly
   loadable. **Undocumented tokenizer changes are plausibly widespread and
   currently undetectable from documentation alone.**
3. **Longitudinal price comparisons within one vendor are unsound** unless the
   tokenizer generation is held constant.

**An unexpected null:** OpenAI's newest encoding (`o200k_base`) is **not more
efficient than `cl100k_base` on code** — 507 vs 503 on Python, 448 vs 446 on
TypeScript. It is marginally better on prose and JSON. Newer does not mean
cheaper per unit of text.

**A coincidence worth flagging, not over-reading:** Qwen matches `cl100k_base`
exactly on TypeScript (446) and prose (409). With n=1 per stratum this is
plausibly coincidence between similarly-trained BPE vocabularies. We do not claim
shared lineage.

## 8. Threats to validity

| Threat | Severity | Status |
|---|---|---|
| **Anthropic and Google unmeasurable** — no offline tokenizer | **Severe** | Realized. §9. |
| **Tokenizer ≠ served endpoint** — repo tokenizer may differ from billing tokenizer | High | Unresolved. We measured published tokenizers; the assumption that they are the billing tokenizers is stated and unverified. |
| **Corpus is n=1 per stratum** | High | Realized. Single sample per content type. Spread magnitudes should be treated as indicative, not precise. |
| **Operator-authored corpus** | Medium | Written before counts were seen; published in full for independent re-tokenization with different corpora. |
| **`o200k_base` assumed current for OpenAI** | Medium | Unverified against per-model docs. |
| **Llama excluded (gated, HTTP 401)** | Medium | Realized. Major open-weight family missing. Not substituted. |
| **No chat templates applied** | Low–Medium | Real deployments add template tokens; these differ per vendor and would likely *increase* spread. |

## 9. Limitations

**The primary deliverable was not achieved.** The study was designed to produce
corrected price-per-normalized-token figures. It cannot, because:

| Vendor | Pricing captured | Tokenizer reachable | Correctable? |
|---|---|---|---|
| Anthropic | ✅ verbatim | ❌ none published | **No** |
| Google | ⚠️ tool_extracted | ❌ none published | **No** |
| OpenAI | ⚠️ tool_extracted | ✅ tiktoken | Partly |
| Qwen | ❌ | ✅ | No |
| DeepSeek | ❌ | ✅ | No |
| Mistral | ❌ | ✅ | No |

**No vendor pair has both.** This is not a scheduling failure — it is a
structural asymmetry in the ecosystem: closed-weight vendors publish prices and
withhold tokenizers; open-weight vendors publish tokenizers and are priced by
third-party hosts we have not yet captured.

Further limitations: n=1 per stratum; five strata do not span all real content;
output-side tokenization unmeasured (and output is the expensive side).

## 10. Discussion

The measurement is solid and the correction is blocked. That combination is worth
stating plainly rather than dressing up.

What we can now assert with evidence:
- Cross-vendor per-token prices are **not comparable without normalization**, and
  the error is ~33% on code — larger than most inter-tier price gaps.
- Normalization must be **content-type specific**. One global multiplier per
  vendor would be wrong by up to 23 percentage points between prose and JSON.
- Within-vendor generational comparisons are **also** unsound.

What we cannot assert: any corrected cross-vendor price. The Atlas's block on
cross-vendor cost publication **remains in force**, now for a documented reason
rather than a suspected one.

A note on incentives, offered as interpretation rather than finding: the vendors
that publish tokenizers are the ones whose weights are open. For closed vendors,
the tokenizer is the one component that would let an outsider verify billing
independently, and it is precisely the component not published. We do not
attribute motive; we note the pattern is consistent and that it makes independent
verification of token billing impossible.

## 11. Recommendation impact

**Realized impact this study delivers now:**

1. Cross-vendor cost claims stay blocked — now evidenced, not precautionary.
2. `met-effective-token-multiplier` gains real values for six tokenizers across
   five content types.
3. **Usage profiles need a content-mix field.** Effective cost depends on whether
   a workload is code-heavy or prose-heavy by up to 23 points of spread. Profiles
   currently have no content-mix dimension. *(New schema requirement — §12.)*
4. **Longitudinal price comparison requires a tokenizer-generation guard**, or
   the Atlas will publish invalid within-vendor trends over time.

**Impact deferred:** the price correction itself, pending either API access or
capture of pricing for open-weight hosts.

**ERI reassessment.** Preregistered as Decisive (breadth 1.0 × flip 0.7 ×
magnitude 4/5). Realized breadth is lower — the correction cannot be applied — but
the *blocking* function is fully realized, and the within-vendor finding was
unanticipated and broadens applicability. **Revised: High, pending unblock.**

## 12. Future research

| ID | Work | Priority |
|---|---|---|
| **RQ-01a** | Capture pricing for open-weight hosts (Together, Fireworks, DeepInfra, OpenRouter) so a vendor pair with both pricing *and* tokenizer exists | **Highest — unblocks the correction** |
| **RQ-01b** | Obtain API access for Anthropic/Google `count_tokens` endpoints; measure the two largest pricing sources | High |
| **RQ-01c** | Expand corpus to n≥5 per stratum with independently-sourced code | High |
| **RQ-01d** | Output-side tokenization — output is billed 3–5× input | High |
| **RQ-01e** | Chat-template overhead per vendor | Medium |
| **RQ-01f** | Audit whether other vendors changed tokenizers between generations without disclosure | Medium — implied by §7 |
| — | HuggingFace token for Llama access | Low, mechanical |

## 13. Complete source list

**Primary evidence generated by this study**
- `research/experiments/results/tokenizer-normalization-v1.json` — full result set
- `research/experiments/corpus/*.txt` — corpus, SHA-256 in results
- `scripts/experiments/exp_tokenizer_normalization.py` — instrument
- `scripts/experiments/probe_capability.py` — capability probe

**Class A sources cited**
- `src-anthropic-pricing-2026-08-03` ex.5 — tokenizer disclosure (verbatim)
- `src-anthropic-models-overview-2026-08-03` ex.3 — same, model-specific (verbatim)

**Software**
Python 3.11.9 · Windows-10-10.0.26200-SP0 · tiktoken 0.12.0 · tokenizers 0.22.2
· transformers 5.1.0

**Tokenizers measured**
`o200k_base`, `cl100k_base`, `p50k_base` (tiktoken) ·
`Qwen/Qwen2.5-Coder-7B-Instruct`, `deepseek-ai/DeepSeek-V3`,
`mistralai/Mistral-7B-Instruct-v0.3` (HuggingFace)

**Failed:** `meta-llama/Llama-3.1-8B-Instruct` — GatedRepoError, HTTP 401

## 14. Replication guide

```bash
pip install tiktoken tokenizers transformers
python scripts/experiments/probe_capability.py
python scripts/experiments/exp_tokenizer_normalization.py
```

Writes `research/experiments/results/tokenizer-normalization-v1.json`.

**Expected differences on replication.** Tokenizer repos are not revision-pinned
in this run — a known reproducibility weakness. If a vendor updates a tokenizer,
counts may change. Corpus SHA-256 values are recorded, so any input drift is
detectable. No seeds; the procedure is deterministic. Network required on first
run. Runtime under two minutes.

**To falsify:** substitute your own corpus. If cross-vendor spread on code falls
below 1.20 on a larger, independently-sourced corpus, H1 does not generalize and
this report should be corrected.
