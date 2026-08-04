# ASSUMPTION REGISTER

**Status:** v1.0 · **2026-08-04** · **Rule adopted:** every assumption becomes a
research question

---

## The rule

> **No assumption may exist in the Atlas without a research question attached to
> it.**

An assumption without an RQ is a permanent guess wearing a temporary label.
Attaching an RQ converts it into a *scheduled measurement* — something with an
owner, an effort estimate, and a path to being eliminated.

This is enforced, not encouraged. Any record carrying `status: assumed` must
carry an `rq:` field naming the research question that would replace it.
`scripts/atlas/validate.py` rule **ASSUM-1** fails the build otherwise.

**Corollary — the question to ask on discovering any assumption:**
*"Can this be measured instead?"* If yes, it becomes an RQ. If no, it must be
documented as **irreducibly uncertain** with the reason, which is a different and
more honest status than "assumed."

---

## Register

| RQ | Assumption | Where | Impact if wrong | Measurable? | Effort |
|---|---|---|---|---|---|
| **RQ-18** | Monthly token volume per working pattern | all 4 usage profiles | **Every dollar figure the Atlas produces** | ✅ instrument a week of real work | Low |
| **RQ-19** | Cache hit rate (0.35–0.60 assumed) | all 4 usage profiles | Cost *and* feasibility — cache reads are excluded from ITPM | ✅ log `cache_read_input_tokens` | Low |
| **RQ-20** | Retry/rework rate (0.15–0.45 assumed) | all 4 usage profiles | Cost per completed unit of work | ✅ count re-runs against completions | Low |
| **RQ-21** | Content mix (code/prose/structured shares) | usage profiles, added M4.1 | Effective token multiplier varies up to 23 points by content type | ✅ classify real session inputs | Low |
| **RQ-22** | `o200k_base` is the encoding for current OpenAI models | `exp-normalized-cost-v1` | All OpenAI rows in the normalized cost table | ⚠️ needs vendor documentation | Trivial |
| **RQ-23** | A vendor's published tokenizer is its *billing* tokenizer | `exp-tokenizer-normalization-v1` §8 | The entire normalization result | ⚠️ requires API token counts to cross-check | Low |
| **RQ-24** | Belief-distribution heuristics (evidence → distribution shape) | `compute.py` | Every confidence value and every P(best) | ⚠️ partially — sensitivity to the heuristic is measurable | Medium |
| **RQ-25** | ERI components: flip_probability and magnitude | research program ranking | Which research gets done first | ❌ **irreducible until a query log exists** | — |
| **RQ-26** | Kimi K3 is open-weight | `ent-model-kimi-k3` | Self-hosting and licence answers | ✅ read the licence | Trivial |
| **RQ-27** | DeepSeek V4 is self-hostable | `ent-model-deepseek-v4-pro` | Same | ✅ read the licence | Trivial |

### Irreducibly uncertain — not assumptions, and not measurable

| Item | Why it cannot be measured |
|---|---|
| **Persona weight vectors** | These are *editorial opinion* about whose problem matters, not facts about the world. Already labelled `weights_status: opinion`. Measuring them is a category error — they can be argued with, not verified. |
| **RQ-25 ERI components** | Requires a query log from real users. Until the Atlas has readers, flip_probability is a prior. Documented as such rather than pretending otherwise. |

---

## What this changes about prioritisation

Six of ten register entries are **Low or Trivial effort and directly
measurable**. Four of those (RQ-18/19/20/21) are satisfied by the *same*
instrumentation run — a single week of logged agentic work eliminates four
assumptions at once.

That makes the usage-profile measurement the highest-leverage action in the
project by a wide margin, which the register makes visible in a way the prose
did not.

RQ-22, RQ-26, RQ-27 are each a single documentation lookup. They are trivial and
have been sitting unresolved because nothing forced them to be listed.

**That is the register's real function:** it converts scattered caveats into a
ranked, finite, shrinking list.

---

## Status discipline

| Status | Meaning | Requires |
|---|---|---|
| `assumed` | A guess, with a path to measurement | **`rq:` field, mandatory** |
| `measured` | Derived from a Class D experiment | `derived_from:` experiment id |
| `irreducible` | Cannot be measured; documented reason | `reason:` field |

`assumed` without an `rq` is a validation failure. The build does not pass.
