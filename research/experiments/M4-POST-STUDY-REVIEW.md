# M4 POST-STUDY REVIEW

**Date:** 2026-08-04 · **Studies reviewed:** RQ-01, RQ-07, RQ-08
**Required before broad evidence population resumes**

---

## 0. Outcome summary

| Study | Outcome | Data produced |
|---|---|---|
| **RQ-01** Cross-vendor token economics | ✅ Complete, 3/3 hypotheses supported, primary deliverable blocked | Original measurement, 6 tokenizers × 5 strata |
| **RQ-07** Sonnet 5 tokenizer | ⛔ Blocked — no API credential | None |
| **RQ-08** Subscription crossover | ⚠️ Negative result — not publicly computable | Subscription terms captured |

**One of three studies produced its intended deliverable. All three produced
publishable findings.** That ratio is worth stating plainly: the program's value
came as much from the two that failed as from the one that worked.

---

## 1. Lessons learned

### L1 — The blockers clustered, and the cluster is the finding

Three independent studies hit the same wall from different directions:

- RQ-01: Anthropic and Google publish no offline tokenizer
- RQ-07: verification requires a paid API credential
- RQ-08: subscription allowances are published only as relative multipliers

Separately these look like access problems. Together they describe a market where
**the information required to verify what you are paying for is systematically
unavailable for closed-weight vendors**. Prices are published to five significant
figures; the units those prices are denominated in are not.

This was not a hypothesis going in. It emerged from three failures pointing the
same way, and it is the most important thing M4 produced.

### L2 — Capability probing must precede protocol design

The RQ-01 probe took minutes and prevented a preregistration committing to
measurements we could not make. Had we preregistered "measure all major vendors"
we would have had to amend the protocol after seeing partial results — the exact
integrity failure preregistration exists to prevent.

**Adopted:** capability probe is a required first step for every experiment,
using throwaway inputs that are never part of the study corpus.

### L3 — Preregistered failure criteria did real work

RQ-08's negative result was **pre-committed** in M3.1. Without that, the honest
move (publish "not computable") would have competed against the tempting one
(estimate the allowance and publish a crossover). The pre-commitment removed the
temptation before the data arrived.

### L4 — We deviated from process, and the deviation is instructive

RQ-08's standalone PREREG document did not exist before the first capture; the
protocol lived in the RQ file. The substantive protection was in place, but
"the protection that mattered was in place" is precisely the post-hoc reasoning
preregistration guards against.

**Corrective action, effective immediately:** no data-collection call for any
study before a PREREG file exists. Enforced as a checklist item, not a norm.

### L5 — Hypotheses can pass and still mislead

All three RQ-01 hypotheses were supported. The most consequential result was the
one we did not predict: within-vendor generational drift (1.27×) is nearly as
large as cross-vendor difference (1.34×). H3 "passed" while nearly failing, and
the near-miss carried more information than the pass.

**Adopted:** report margin, not just direction, on every hypothesis outcome.

### L6 — n=1 corpora produce indicative, not precise, magnitudes

One sample per stratum. The 1.33× figure is directionally solid and numerically
soft. We reported it as such; the temptation to quote it as precise will grow as
it gets cited.

---

## 2. Schema changes required

| # | Change | Driver | Status |
|---|---|---|---|
| **S1** | `usage_profile` gains a **content mix** field (code / prose / structured shares) | RQ-01: effective cost varies by up to 23 points of spread across content types | **Required** |
| **S2** | `model_version` gains `tokenizer_generation` and `tokenizer_verified` (bool) | RQ-01 §7: undocumented tokenizer changes are plausibly widespread | **Required** |
| **S3** | `subscription_plan` must permit `allowance: not_publicly_disclosed` as a first-class value distinct from `unknown` | RQ-08: the vendor has not published it, versus we have not found it | **Required** |
| **S4** | `metric` records gain `corpus_n` so indicative magnitudes are distinguishable from precise ones | L6 | Recommended |
| **S5** | Tokenizer repo **revision pinning** in experiment records | RQ-01 replication weakness | Recommended |

None of these is a redesign. All are additive fields with safe defaults — the
behaviour the schema was built for.

## 3. Recommendation engine changes triggered

| # | Change | Driver |
|---|---|---|
| **E1** | New refusal code **`NOT_PUBLICLY_COMPUTABLE`**, distinct from `UNDER_DETERMINED` | RQ-08. The former means the input does not exist publicly; the latter means we lack it. Conflating them implies the gap is ours to close. |
| **E2** | Cross-vendor cost comparison remains **blocked**, now with cited evidence rather than precaution | RQ-01 |
| **E3** | Cost model must apply a **content-type-specific** token multiplier, never a single per-vendor constant | RQ-01 §7 |
| **E4** | **Longitudinal price comparisons within one vendor require a tokenizer-generation guard** | RQ-01 H3 |
| **E5** | Subscription and API offerings may not appear in the same price column until the 200k-vs-1M context discrepancy resolves | RQ-08 §7 |
| **E6** | Q1 (`$20/month`) answer changes from a refusal-for-lack-of-data to a **substantive negative answer** | RQ-08 |

E6 is the one that changes what a reader sees. The Atlas can now tell someone
asking about a $20 budget something true: *this comparison is not publicly
computable, and any source giving you a confident answer has silently estimated
the missing number.*

## 4. New research questions generated

| ID | Question | ERI | Effort |
|---|---|---|---|
| **RQ-08a** | Are absolute subscription allowances published anywhere outside the pricing page? | **High** | **Trivial** ⚡ |
| **RQ-08b** | Do subscription tiers really cap context at 200k while the API offers 1M? | **High** | **Low** ⚡ |
| **RQ-01a** | Capture pricing for open-weight hosts, creating a vendor pair with both pricing *and* tokenizer | **Decisive** | Low ⚡ |
| **RQ-11** | Have vendors changed tokenizers between generations without disclosure? | High | Medium |
| **RQ-12** | Is token billing independently verifiable for any closed-weight vendor? | High | Medium |
| RQ-01c | Expand corpus to n≥5 per stratum, independently sourced | High | Low |
| RQ-01d | Output-side tokenization (output bills 3–5× input) | High | Medium |
| RQ-07a | Obtain API credential; execute RQ-07 unchanged | Moderate | Trivial once unblocked |
| RQ-08c | Does any vendor publish absolute allowances? | High | Low |

**RQ-01a is the new highest-value item.** It is the shortest path to unblocking
the price correction that RQ-01 could not complete: capture pricing for hosts
serving open-weight models whose tokenizers we already have.

**RQ-12 is the emergent flagship candidate.** L1's convergent finding deserves to
be a question in its own right rather than an observation scattered across three
reports.

## 5. Should the methodology be revised?

**Largely no.** The framework did what it was built to do:

- Preregistered failure criteria produced an honest negative (RQ-08)
- Construct-validity rules correctly blocked a comparison we lacked evidence for
- `not_normalizable` exclusion, specified in M3.1, was applied exactly as written
- The bitemporal and evidence-class machinery absorbed all findings without change

**Three revisions adopted:**

| # | Revision | Driver |
|---|---|---|
| **M1** | Capability probe required before protocol design; probe inputs must not enter the study corpus | L2 |
| **M2** | PREREG file must exist before the first data-collection call. No exceptions. | L4 |
| **M3** | Hypothesis outcomes report **margin**, not just supported/unsupported | L5 |

**One thing to watch, not yet a revision.** All three studies were run and scored
by the same operator with no blinding. For deterministic tokenizer counting that
is harmless. For RQ-04 (intervention rate) and RQ-10 (frontend fidelity) it will
not be, and the inter-rater gates already specified in those RQ files are now
demonstrably load-bearing rather than precautionary.

## 6. Should broad population resume?

**Not immediately.** Four items should land first, and all four are cheap:

1. **RQ-08a** — could invert the RQ-08 negative result outright (trivial)
2. **RQ-08b** — could reframe the entire subscription question (low)
3. **RQ-01a** — unblocks the cross-vendor price correction (low)
4. **Schema changes S1–S3** — populating entities before these lands means
   re-writing usage profiles and subscription entities afterwards

Populating entities now would mean writing cost figures that S1–S3 force us to
revise, and possibly publishing a negative result (RQ-08) that RQ-08a overturns
within an hour of work.

**Recommended sequence:** RQ-08a → RQ-08b → S1–S3 → RQ-01a → resume population.

## 7. Honest assessment

The program worked, and it worked partly by failing.

What we produced that did not previously exist: a measured cross-vendor tokenizer
comparison, evidence that within-vendor drift rivals cross-vendor difference, and
a documented demonstration that the most-asked cost question in this domain is
not answerable from published information.

What we did not produce: the price correction RQ-01 was designed to deliver, and
any resolution of the Sonnet 5 ambiguity.

The uncomfortable part is that **two of three studies were blocked by information
vendors choose not to publish**, and no amount of methodological rigour on our
side changes that. The Atlas's ability to verify closed-weight vendors is
structurally limited, and that limitation should be stated in METHODOLOGY §9
alongside the biases already listed there — not buried in three separate reports.
