# Sonnet 5 Tokenizer Verification — BLOCKED STUDY

**Technical report · `exp-sonnet-5-tokenizer-identity-v1`**
**Study:** RQ-07 · **Attempted:** 2026-08-04 · **Status:** ⛔ **BLOCKED — not executable**
**Cost:** $0.00 · **Reproducible:** the blocking condition is reproducible

---

## 1. Executive summary

**This study could not be run.** It requires API access to Anthropic's
`count_tokens` endpoint, and no API credential is available in this environment.

The question — *does Claude Sonnet 5 use the newer (~30% more tokens) tokenizer?*
— remains **unresolved**, and `clm-claude-sonnet-5-090` remains `unknown`.

Publishing a blocked study rather than silently dropping it is deliberate. The
blocker is not incidental: **Anthropic publishes no offline tokenizer**, so this
question is unanswerable by anyone without a funded API account. That is a
finding about the ecosystem's verifiability, not just about our access.

---

## 2. Background and research question

Two verbatim Class A sources from the same vendor do not obviously agree about
Sonnet 5:

| Position | Source | Text |
|---|---|---|
| Newer tokenizer applies from 4.7 onward | `src-anthropic-pricing-2026-08-03` ex.5 | "Claude 4.7 and later models … use a newer tokenizer … Claude Sonnet 4.6 and earlier models use the previous tokenizer." |
| Attribution is model-specific | `src-anthropic-models-overview-2026-08-03` ex.3 | Tooltip attached to **Claude Fable 5** only |

Sonnet 5 is named in neither list. The plain reading of "4.7 and later" includes
it; the overview's model-specific attribution does not confirm it.

**Research question:** Does Claude Sonnet 5 use the tokenizer introduced with
Claude Opus 4.7?

## 3. Why this matters

Sonnet 5 is the mid-tier model most budget-constrained readers would land on.
A ~30% token inflation is **larger than its entire introductory discount**
(which itself expires 2026-08-31). Getting this wrong misprices the most
commonly-recommended model.

## 4. Methodology (as preregistered, unexecuted)

Preregistered in `research/questions/RQ-07-sonnet-5-tokenizer.md` §5 on
2026-08-03.

1. Take a fixed text sample.
2. Submit to Sonnet 5 and to a known pre-4.7-tokenizer model via `count_tokens`.
3. Compare. A ~30% divergence settles it.

Controls: identical text; minimal system prompt subtracted; repeated across
content types, since the vendor states the increase is content-dependent.

## 5. Blocking condition

| Requirement | Status |
|---|---|
| Anthropic offline tokenizer | ❌ **Does not exist publicly** |
| `count_tokens` API endpoint | ✅ exists |
| API credential | ❌ **not available** |
| `anthropic` Python SDK | ✅ 0.79.0 installed |
| `ANTHROPIC_BASE_URL` env var | ✅ present |
| `ANTHROPIC_API_KEY` | ❌ **absent** |

Verified by `scripts/experiments/probe_capability.py`. The environment scan found
no API key for any vendor.

**We did not attempt to call the endpoint without a credential.** Doing so would
generate a failed request against infrastructure we are not authorized to use.

## 6. Results

**None.** No data collected.

## 7. Analysis

The blocker generalizes further than this study.

RQ-01 established that Anthropic and Google publish **no offline tokenizer**,
while OpenAI, Qwen, DeepSeek, and Mistral do. Combined with this study's blocker:

> **Token billing for the two vendors whose pricing the Atlas has captured most
> thoroughly cannot be independently verified by anyone without a paid account.**

The tokenizer is the single component that would let an outsider check that
billed token counts match the text submitted. For closed-weight vendors it is
consistently the component not published.

We do not attribute motive — there are legitimate reasons not to publish a
tokenizer, including it being an implementation detail vendors wish to change
freely. We report the consequence: **independent verification of token billing is
impossible for these vendors**, and that is a structural property of the market,
not an oversight.

## 8. Threats to validity

Not applicable — no data. One threat applies to the *blocking claim* itself: we
searched for a public Anthropic tokenizer and found none. **Absence of evidence
here is weak evidence of absence**; a tokenizer could exist in a form we did not
locate. Confidence that none is published: moderate, not high.

## 9. Limitations

The study is unexecuted. Nothing about Sonnet 5's tokenizer is established.

## 10. Discussion

The correct action was to publish the blocker rather than resolve the ambiguity
by inference. The plain reading of "Claude 4.7 and later models" probably
includes Sonnet 5 — and "probably" is not a basis for a published claim under
CONSTITUTION §7.

`clm-claude-sonnet-5-090` stays `unknown` with its `conflicts` block intact. The
analyst's lean is recorded in the RQ file so that confirming it later cannot be
mistaken for having known it.

## 11. Recommendation impact

**Zero realized impact.** The claim remains `unknown`; Sonnet 5 cost figures
carry the unresolved multiplier.

**One indirect impact:** combined with RQ-01, this establishes that the Atlas's
verification capability is **structurally limited for closed-weight vendors**.
That belongs in the methodology's stated limitations, not only in this report.

## 12. Future research

| ID | Work | Priority |
|---|---|---|
| **RQ-07a** | Obtain an Anthropic API credential; execute the preregistered protocol unchanged | High — trivial once unblocked |
| **RQ-07b** | Ask the vendor directly to clarify which models use which tokenizer; publish the answer and its provenance | Medium — cheap, and documentation ambiguity is itself worth reporting |
| **RQ-07c** | Infer tokenizer generation from `usage.input_tokens` on ordinary API calls rather than `count_tokens` — same credential requirement, no extra cost | Medium |

## 13. Complete source list

- `src-anthropic-pricing-2026-08-03` ex.5 — Class A, verbatim
- `src-anthropic-models-overview-2026-08-03` ex.3 — Class A, verbatim
- `scripts/experiments/probe_capability.py` — blocker verification
- `research/questions/RQ-07-sonnet-5-tokenizer.md` — preregistered protocol

## 14. Replication guide

To reproduce the **blocking condition**:

```bash
python scripts/experiments/probe_capability.py
```

Confirms no Anthropic offline tokenizer and reports environment credentials.

To reproduce the **study**, set `ANTHROPIC_API_KEY` and execute the §4 protocol
unchanged. Estimated cost: under $0.01. Runtime: minutes.
