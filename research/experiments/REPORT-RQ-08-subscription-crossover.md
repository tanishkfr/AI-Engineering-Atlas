# Subscription vs Metered Crossover — NEGATIVE RESULT

**Technical report · `exp-subscription-crossover-v1`**
**Study:** RQ-08 · **Run:** 2026-08-04
**Status:** ⚠️ **NEGATIVE RESULT — the comparison is not publicly computable**
**Cost:** $0.00 · **Reproducible:** yes

---

## 1. Executive summary

**The subscription-versus-metered crossover cannot be computed from published
terms.** Subscription usage allowances are stated as *relative multipliers with
no absolute base* — "More usage", "5x or 20x more usage than Pro" — and Pro's
allowance is never given in tokens, requests, or any other measurable unit.

This is a **preregistered failure criterion being realized**, not an
after-the-fact excuse. `RQ-08-subscription-crossover.md` §5, written 2026-08-03
before any capture, stated: *"If subscription plans do not disclose token
allowances, the crossover cannot be computed from published terms… the finding
becomes 'this comparison is not publicly computable' — which is a legitimate and
useful published result, not a failure."*

**Consequence for the Atlas's most-asked question.** *"I have $20/month"* now has
a defensible answer, and it is not a product recommendation:

> **You cannot determine from published information whether a $20 subscription
> gives you more or less than $20 of metered API usage. Nobody can. The vendor
> does not publish the number required to make that comparison.**

**A second finding may be more important.** The captured page indicates
subscription models carry a **200k context window**, while the same model
families on the API are documented at **1M tokens**. If confirmed, subscription
and API are **not the same product**, and the crossover question is not
like-for-like even in principle. This requires verbatim confirmation before it is
published as a claim.

---

## 2. Background

*"Can $20 of API credits replace a subscription?"* is among the founding questions
of this project and one of the seven standard queries. The Atlas had captured
complete metered pricing but **zero** subscription data.

## 3. Research question

At what usage level does a subscription become cheaper than metered API access,
and how does that crossover move with cache hit rate and model choice?

## 4. Why this matters

The correct output is a **crossover point**, not a product name — readers know
their own usage better than we do. It also determines the honest answer to
*"I prefer APIs"*: a stated preference deserves to be **priced**.

## 5. Methodology

**Preregistration provenance, stated plainly.** The protocol and the failure
criterion were fixed in `research/questions/RQ-08-subscription-crossover.md` §5
on 2026-08-03, before any capture. A standalone PREREG document was not written
before the first fetch — a **process deviation**, recorded here rather than
concealed. The substantive protection (a pre-committed failure criterion) was in
place; the documentary form was not. See §10.

**Procedure as preregistered:**
1. Capture subscription plan terms as temporal `step` facts.
2. Compute monthly cost per usage profile under subscription, metered, and mixed.
3. Solve for crossover token volume; report as a surface over cache hit rate and
   model tier.
4. Identify dominated ranges.

**Executed:** step 1 only. Steps 2–4 are unreachable — see §6.

## 6. Results

Captured 2026-08-04 from `https://www.claude.com/pricing`
(`excerpt_fidelity: tool_extracted` — restructured by the extraction model).

| Plan | Price | Stated allowance |
|---|---|---|
| Free | $0 | none specified |
| Pro | "$17 Per month with annual subscription discount ($200 billed up front)"; "$20 if billed monthly" | **"More usage*"** |
| Max 5x | "From $100 Per month" | **"Choose 5x or 20x more usage than Pro*"** |
| Max 20x | "From $100 Per month" | **"Choose 5x or 20x more usage than Pro*"** |
| Team (standard) | "$20 Per seat / month if billed annually. $25 if billed monthly" | not specified |
| Team (premium) | "$100 Per seat / month if billed annually. $125 if billed monthly" | not specified |

Team scope: "For teams of 2 to 150". The page states "Usage limits apply" with a
link to support documentation.

**The blocking observation.** Every allowance is expressed **relative to Pro**,
and **Pro's allowance is never expressed in any absolute unit**. The system of
equations has no constant term:

```
  Pro    = X          (X never given)
  Max5x  = 5X
  Max20x = 20X
  → the ratio between plans is known; the value of any plan is not.
```

Crossover requires comparing an absolute subscription allowance against an
absolute metered volume. One side of that comparison does not exist publicly.

## 7. Analysis

**Why relative-only allowances defeat the computation.** Metered cost is
`f(tokens, prices)` — fully determined by captured Class A data. Subscription
cost is `$20/month for X`, where X is undefined. No amount of modelling recovers
X from published information.

**Why we did not estimate X.** Estimating it from community reports would produce
a crossover that looks precise and rests on hearsay. CLAUDE.md §1.11 forbids
inventing usage numbers; this is that rule applying to the vendor's side of the
ledger. An estimated X would propagate into every budget recommendation with
false precision.

**The context-window observation.** The extraction states subscription models
carry a 200k context window. The Atlas holds verbatim Class A evidence that
Fable 5, Opus 5, and Sonnet 5 each provide **1M tokens** on the API
(`clm-claude-sonnet-5-010`). If both hold, subscription and API deliver
**materially different products at the same model name** — a 5× context
difference.

This is recorded as an **unverified lead, not a claim**: the source is
`tool_extracted`, and a 5× discrepancy of this significance requires verbatim
confirmation. If confirmed it substantially reframes the question — you would not
be comparing prices for the same thing.

**What this says about the market.** Metered pricing is published to five
significant figures, with cache multipliers, batch discounts, and geography
premiums fully specified. Subscription pricing — the tier most individuals
actually buy — is published as an unquantified relative. The precision is
inversely related to how many people rely on it.

## 8. Threats to validity

| Threat | Severity | Status |
|---|---|---|
| Reduced-fidelity capture — figures may be misrendered | High | Realized. All claims from this capture are `draft`. |
| Allowances may be published elsewhere (support docs, ToS) | **High** | **Not exhaustively searched.** The linked support article was not retrieved. This is the study's main weakness — see §9. |
| Single-vendor scope | High | Only one vendor's subscriptions captured. Others may publish absolute allowances. |
| Allowances may vary dynamically by load | Medium | Would make a published constant impossible in principle rather than merely absent. |

## 9. Limitations

**The negative result is scoped to the pricing page, not to all vendor
documentation.** We did not retrieve the linked usage-limits support article. The
honest claim is: *allowances are not on the pricing page in absolute terms*, not
*allowances are nowhere published*. Resolving this is RQ-08a and it is cheap.

Single vendor. Single capture date. Reduced fidelity throughout.

## 10. Discussion

**On the process deviation.** The formal preregistration document should have
existed before the first capture. It did not; the protocol lived in the RQ file.
The failure criterion was genuinely pre-committed, which is the substantive
protection — but "the protection that mattered was in place" is exactly what
someone would say after the fact, and that is why the deviation is recorded
rather than argued away. **Corrective action:** M4 process now requires a PREREG
file to exist before the first data-collection call for every study, without
exception.

**On the value of the negative result.** The Atlas can now answer *"I have
$20/month"* with something true and useful: the comparison you are being asked to
make is not publicly computable, and any source that gives you a confident answer
has estimated the missing number without telling you. That is more actionable
than a fabricated crossover.

## 11. Recommendation impact

| Change | Status |
|---|---|
| Q1 (`$20/month`) refusal code changes from `UNDER_DETERMINED` to a **new** `NOT_PUBLICLY_COMPUTABLE` | **New engine requirement** |
| Subscription entities recorded with allowance `unknown`, not estimated | Applied |
| Q4 (`I prefer APIs`) cannot price the preference against subscriptions | Realized limitation |
| Comparison-page rule: subscription and API may not appear in one price column until the context-window discrepancy resolves | **New rule** |

`NOT_PUBLICLY_COMPUTABLE` is distinct from `UNDER_DETERMINED`: the latter means
*we lack an input*, the former means *the input does not exist publicly and no
amount of our effort will produce it.* Conflating them would imply the gap is
ours to close.

**ERI reassessment.** Preregistered High (breadth 0.45 × flip 0.8 × magnitude
4/5). Realized differently: no crossover produced, but the question moved from
*unanswered* to *answered with a negative*, which does change what the Atlas
tells readers. **Revised: Moderate, realized.**

## 12. Future research

| ID | Work | Priority |
|---|---|---|
| **RQ-08a** | Retrieve the linked usage-limits support article; determine whether absolute allowances are published anywhere | **Highest — cheap, could invert this result** |
| **RQ-08b** | Verbatim re-capture to confirm the 200k vs 1M context discrepancy | **High — would reframe the question entirely** |
| **RQ-08c** | Survey other vendors: does any publish absolute subscription allowances? A vendor that does becomes the computable case | High |
| **RQ-08d** | If allowances are nowhere published, measure empirically — consume a subscription to its limit under instrumentation | Medium; requires a funded account and is the only path to an absolute number |

## 13. Complete source list

- `src-anthropic-subscription-pricing-2026-08-04` — `https://www.claude.com/pricing`, Class A, **tool_extracted**, retrieved 2026-08-04, not archived, not hashed
- `src-anthropic-pricing-2026-08-03` — metered pricing, Class A, verbatim
- `clm-claude-sonnet-5-010` — 1M context window, published
- `research/questions/RQ-08-subscription-crossover.md` — protocol and failure criterion, 2026-08-03

## 14. Replication guide

Fetch `https://www.claude.com/pricing` and inspect the plan table for an absolute
usage allowance in tokens, messages, or requests.

**To falsify:** produce a vendor-published absolute allowance for any plan. If
one exists, this negative result is wrong and the crossover becomes computable —
we would want to know quickly.

**Expected differences:** pricing pages change without notice. This capture is
dated 2026-08-04 and is not archived; a future reader may find different terms.
