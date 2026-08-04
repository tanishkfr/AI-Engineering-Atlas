# RQ-06 — Real-world feature cost

**Status:** accepted · **ERI:** Moderate–High · **Effort:** Low ⚡
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**What fraction of a real agentic bill is consumed by overhead that no price
table shows — tool definitions, system prompts, retries, failed runs, and
rework?**

## 2. Why it matters

Published pricing describes the rate. It does not describe the meter.

The first evidence pass found several overhead components that are documented,
free to look up, and never included in any comparison:

- **Tool-use system prompt tax**, charged on *every* request that includes tools.
  It varies by model far more than one would expect: 286/406 tokens for Claude
  Opus 5 versus 675/804 for Opus 4.7 — a ~2.4× difference between two versions of
  the same product line. For a high-frequency agent with small payloads, this is
  a meaningful share of input cost.
- **Per-tool definition costs** on top of that (bash, text editor, computer use
  each add their own token count).
- **Retries and rework**, which appear in no price table and are currently a pure
  guess in our usage profiles (`retry_rate: 0.20`, stated as "This is a guess").
- **Server-side tool charges** billed outside token pricing entirely.

The framing that matters: **cost per unit of completed work**, not cost per
token. A model needing four attempts is not cheap. `obj-cost-efficiency` already
says this; RQ-06 supplies the numbers that make it operational.

**Recommendation surface affected:** every cost output; D6 for every stack; the
budget frontier's accuracy near knees, where small errors flip which side of a
knee a reader lands on.

## 3. Current evidence

| Evidence | Source | Class | Fidelity |
|---|---|---|---|
| Tool-use system prompt token counts per model | `src-anthropic-pricing-2026-08-03` ex.10 | A | verbatim |
| Bash tool +325 / +244 tokens by model generation | same page | A | verbatim |
| Text editor tool +700 tokens | same page | A | verbatim |
| Computer use +466–499 system, +735 per definition | same page | A | verbatim |
| Web search $10/1,000 searches, billed outside tokens | ex.11 | A | verbatim |
| Code execution 1,550 free hours/month then $0.05/hr | ex.12 | A | verbatim |
| Managed Agents session runtime $0.08/session-hour | ex.13 | A | verbatim |

Unusually strong for a research question: the **components are documented**.
What is missing is their **share of a real bill**.

## 4. Missing evidence

- Overhead as a percentage of total spend on real agentic sessions
- Actual retry and rework rates — the single largest unknown, and currently an
  admitted guess
- Cost of *abandoned* work: sessions that produced nothing usable still bill
- Equivalent overhead accounting for other vendors. Anthropic documents these
  costs in unusual detail; whether others charge similar overheads **and simply
  do not document them** is unknown, and would be a significant comparability
  finding either way.
- Whether overhead share differs systematically by harness (a harness sending
  more tools per request pays more per request)

## 5. Proposed experiments

### `exp-real-world-feature-cost-v1`

**Design.** Pure accounting over runs performed for other experiments — no new
runs required, which is why effort is Low.

1. For every instrumented session, decompose total spend into:
   `productive_input` · `tool_definition_overhead` · `system_prompt_overhead` ·
   `cache_write_overhead` · `retry_cost` · `abandoned_work_cost` · `output`
   · `server_side_tool_charges`.
2. Report overhead as a share of total, per stack and per task class.
3. Compute the **effective price multiplier**: what you actually pay per unit of
   completed work, divided by the headline per-token rate.
4. Publish a corrected price table alongside the published one.

**Preregistered prediction.** Overhead plus rework exceeds **25%** of total spend
on agentic sessions, and the gap between headline and effective price is larger
for cheaper models — because cheaper models retry more, which would mean the
price spread between tiers is narrower in practice than it appears.

That prediction, if confirmed, is the headline finding: **cheap models are less
cheap than they look, and the entire value ranking compresses.**

### `exp-real-world-feature-cost-v2`

Vendor-comparative overhead audit: identical agent, identical tools, across
vendors; measure per-request overhead directly from usage fields rather than
documentation. Needed because we cannot assume undocumented means absent.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.75** | Every cost query, and the budget frontier's knee positions |
| flip_probability | **0.45** | Compresses the value ranking rather than reordering it — but compression near a knee flips the answer |
| magnitude | **3/5** | Corrects headline prices by a projected 25%+ |

**ERI: Moderate–High.** Carries ⚡ JUMP QUEUE because the effort is near-zero:
it is analysis of data other experiments already produce.

## 7. Estimated effort

**Low.** Days.

| Component | Effort |
|---|---|
| Cost-decomposition analysis code | ~2 days |
| Integration into the cost model | ~1 day |
| Cross-vendor audit (v2) | ~3 days, **binding constraint** |

**Binding constraint:** v1 requires only that the RQ-03 instrumentation exists.
v2 needs comparable usage-field reporting across vendors, which may not be
available everywhere — and where it is not, that itself is reportable.

## 8. Current confidence

**In the answer: low-to-moderate** — the highest in the portfolio, because the
components are individually documented and verbatim-sourced. We are reasonably
confident overhead is non-trivial; we have no idea whether it is 10% or 40%,
and the retry rate that drives most of the uncertainty is currently an
acknowledged guess.

**In the question: high.** Cost per unit of completed work is the correct
framing, is already encoded in `obj-cost-efficiency`, and is currently
unpopulated.
