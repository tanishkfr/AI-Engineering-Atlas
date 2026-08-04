# RECOMMENDATION DELTAS

**Living document · opened 2026-08-04**

Where new evidence changes what the Atlas would tell a reader, the change is
published here rather than silently applied. A reader who acted on an earlier
version deserves to know it moved (CONSTITUTION §11).

Each delta records: what changed, what caused it, who is affected, and whether
the prior position was *wrong* or merely *narrower than stated*.

---

## D-001 — Cross-vendor token normalization matters less than we said

**Date:** 2026-08-04 · **Cause:** `exp-normalized-cost-v1` (RQ-01a)
**Severity:** correction of an over-broad claim

| | |
|---|---|
| **Previously** | "Cross-vendor per-token prices are not comparable without normalization" — cited spread 1.33× |
| **Now** | Among currently-priced models, spread is **1.03–1.11×**. Normalization changes a ranking only when posted prices differ by **less than ~11%** |
| **Why it moved** | The 1.33× figure was driven by `Mistral-7B-Instruct-v0.3`, an older tokenizer generation belonging to no currently-priced model. Measuring only exact model↔tokenizer matches cut the effect by two-thirds |
| **Affects** | Anyone comparing models on price. In practice: almost nobody's decision changes, because price gaps between tiers are 10–260× |
| **Status of prior claim** | **Measurement valid, interpretation too broad.** Not retracted — narrowed |

**Practical effect on advice:** we previously implied readers should distrust
posted price comparisons. They mostly should not. The exception is real and
narrow: closely-priced models within ~11% of each other.

---

## D-002 — Subscription tiers are NOT context-degraded

**Date:** 2026-08-04 · **Cause:** RQ-08b · **Severity:** retraction of an unverified lead

| | |
|---|---|
| **Previously** | Flagged (as an explicitly unverified lead) that subscription plans might cap context at 200k vs 1M on the API |
| **Now** | **False.** "Claude Opus 5 and Sonnet 5 support a 1M token context window on all paid plans when chatting with Claude." The 200K figure applies to *other* models |
| **Why it moved** | Our M4 capture was `tool_extracted` and the extraction attached a figure to the wrong model list |
| **Affects** | Nobody — it was never published as a claim |
| **Status of prior claim** | **Retracted.** The error was ours |

**Why this delta exists even though nothing was published:** the guard that
caught it (`excerpt_fidelity` + "unverified lead, not a claim") is worth
recording as having worked. It cost one extra fetch and prevented a public
correction.

**Engine change:** rule E5 ("subscription and API may not share a price column")
is **withdrawn** — its premise was false.

---

## D-003 — The $20/month question now has a substantive answer

**Date:** 2026-08-04 · **Cause:** RQ-08 + RQ-08a · **Severity:** gap → answer

| | |
|---|---|
| **Previously** | `UNDER_DETERMINED` — "we lack a usage profile" |
| **Now** | `NOT_PUBLICLY_COMPUTABLE` — the subscription meter is denominated in **five-hour sessions and weekly limits**, not tokens. A crossover cannot exist in closed form |
| **Why it moved** | Following the documentation chain two levels deeper revealed *why* allowances are unpublished: there is no token allowance to publish |
| **Affects** | Every reader asking about a fixed monthly budget — the single most common question |
| **Status of prior claim** | **Valid and strengthened** |

**Practical effect:** the Atlas can now say something true and useful where it
previously said nothing: *any source giving you a confident subscription-vs-API
crossover has silently estimated a number the vendor does not publish, in a unit
the vendor does not meter.*

---

## D-004 — MCP's security guarantees are the implementor's, not the protocol's

**Date:** 2026-08-04 · **Cause:** M5 population, MCP specification capture
**Severity:** new decision-relevant finding

| | |
|---|---|
| **Previously** | No position — MCP was an unpopulated entity |
| **Now** | The specification states it **cannot enforce** its security principles at the protocol level, and that tool annotations "should be considered untrusted, unless obtained from a trusted server" |
| **Affects** | Anyone evaluating "is this standard safe to build on", and every D13 security-posture score for an MCP client |
| **Status of prior claim** | New |

**Practical effect:** "supports MCP" is **not** a security property. Two hosts
implementing the same protocol can have completely different safety postures,
and the protocol says so itself. D13 must be scored on the *host*, never inferred
from protocol support — which is the same reasoning that made GRAPH §6 forbid
deriving `works_with` from shared protocol support.

---

## D-005 — "Model-agnostic" needs a surface qualifier

**Date:** 2026-08-04 · **Cause:** M5 population, Claude Code capture
**Severity:** refinement of a capability definition

| | |
|---|---|
| **Previously** | `cap-model-agnostic` treated as a whole-product property |
| **Now** | Third-party providers are documented on **2 of 6** Claude Code surfaces (Terminal CLI, VS Code). The capability is **surface-dependent** |
| **Affects** | The "I don't want vendor lock-in" question. A reader choosing the desktop or web surface has different lock-in exposure than one choosing the terminal — same product name |
| **Status of prior claim** | Refined |

**Schema consequence:** capability edges need a `surface` qualifier where a
capability varies by surface. Applied to Claude Code's
`cap-requires-cli-fluency` edge. **No schema change needed** — relationship
`qualifiers` already accommodates it, which is a small validation of the graph
design.

---

## D-006 — Price is not one number per model: time-of-day variation exists

**Date:** 2026-08-04 · **Cause:** M5.1 population, DeepSeek pricing capture
**Severity:** new pricing shape the cost model cannot express

| | |
|---|---|
| **Previously** | Cost model treats a model's price as a `step` fact — constant until superseded |
| **Now** | At least one vendor documents **2× pricing during peak hours** (09:00–12:00 and 14:00–18:00 UTC+8 daily) |
| **Affects** | Any cost figure for a vendor with time-of-day pricing; anyone whose working hours overlap a peak window |
| **Status of prior claim** | Incomplete, not wrong |

**Why this is structurally new.** RQ-09 found Google bills cache *storage by
elapsed time*. This is different again: the **unit price itself varies by clock
time**. A cost model with a single price per model per period cannot express it,
and a user in one timezone pays systematically more than a user in another for
identical work.

**Cost model consequence:** the price term needs an optional **time-of-day
schedule**, defaulting to flat. Additive, like RQ-09's storage term. Logged as
**RQ-14** — deliberately *not* interrupting population, since it affects one
captured vendor and the flat default is correct for the rest.

**Not yet in force:** the vendor states the effective date is "subject to the
official announcement", so whether this currently applies is unknown. Recorded
as `in_force: unknown` rather than assumed active.

---

## D-007 — There IS a cross-vendor standard for agent instructions

**Date:** 2026-08-04 · **Cause:** M5.1 population, AGENTS.md capture
**Severity:** gap → partial answer

| | |
|---|---|
| **Previously** | Q42 ("is there a cross-vendor standard for agent instructions?") unanswerable |
| **Now** | AGENTS.md is documented as supported by 23 named products across competing vendors, stewarded by the Agentic AI Foundation under the Linux Foundation |
| **Affects** | Anyone deciding what to write in a repo instruction file, and anyone worried about lock-in at the context layer |
| **Status of prior claim** | New |

**Caveat carried with the answer, and it matters.** The adopter list is published
**by the standard's own site**. That establishes these products *claim* support —
not that a file written for one works unmodified in another. Recorded as a
`conflicts` block with `likely_cause: incentive`, and raised as **RQ-15**.

**Practical effect:** the honest advice is *"write AGENTS.md, because the
downside if interop is weaker than claimed is small, and the upside if it holds
is portability across 23 tools."* That is a decision under uncertainty, stated as
one.

---

## D-008 — Aider's offline capability is verified as *degraded*, not simply unverified

**Date:** 2026-08-04 · **Cause:** M6.1.1 Class C harvest (from a Class A source)
**Severity:** capability qualification

| | |
|---|---|
| **Previously** | `cap-offline-operation` asserted for Aider from documented local-runtime support, flagged in the entity's own open questions as below evidence bar |
| **Now** | The vendor's own troubleshooting documentation states: "**Most local models are just barely capable of working with aider, so editing errors are probably unavoidable.**" |
| **Affects** | Anyone choosing Aider specifically to run offline or against local models — a real persona (privacy-constrained, air-gapped, cost-floor) |
| **Status of prior claim** | **Qualified, not retracted.** The capability exists and is documented as marginal |

**Why the direction is surprising.** The open question expected to resolve as
either *confirmed* or *withdrawn*. It resolved as neither: the capability is real
and the vendor documents it as barely functional. "Supports local models" and
"works well with local models" are different claims, and only the first is true.

**Practical effect on advice:** for a reader whose *reason* for choosing Aider is
offline operation, the honest answer is now that the tool's own documentation
describes that path as error-prone, with specific mitigations (`--edit-format
whole`, `--architect` mode, sub-25k context). That is more useful than either a
bare capability tick or a removed one.

---

## Open deltas — evidence pending

| ID | Would change | Blocked on |
|---|---|---|
| D-006? | Whether context is **surface**-specific as well as model-specific (Fable 5 appears in the Claude Code 1M list but not the chat list) | RQ-08g |
| D-007? | Whether the MCP revision we cite is current | RQ-13 |
| D-008? | Every absolute cost figure | Measured usage profiles (RQ-03) |
