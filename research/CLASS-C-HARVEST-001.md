# CLASS C HARVEST 001 — D7 / D9

**Date:** 2026-08-04 · **Declaration:** `CLASS-B-AUDIT-2026-08-04.md` Part 2
**Outcome:** ⚠️ **Protocol violation on one sample; one usable finding from another source**

---

## 1. Protocol violation — recorded, not corrected away

**The declared query** (Part 2) specified negative-case terms as *mandatory*:
`problems · limitations · migrated away · issues`.

**The query actually executed** was:
```
github.com/Aider-AI/aider/issues?q=is:issue+label:enhancement+sort:comments-desc
```

`label:enhancement sort:comments-desc` selects for **popular feature requests**.
It is close to the opposite of a negative-case filter — it surfaces what people
want added, not what frustrates them. Predictably, the results were almost
entirely feature requests ("Add GitHub Copilot as model provider", "Feature
request: vscode extension", "Python 3.13 support").

**This sample is discarded.** It does not match the declaration and cannot be
used, including for the parts that looked interesting.

**Why this is recorded rather than quietly re-run:** the whole purpose of
declaring a query in advance is that the executed query can be checked against
it. A researcher who silently swaps the query and reports the results has
converted a preregistered sample into an exploratory one without telling anyone.
The violation is more instructive than the sample would have been.

**Corrective action:** the declaration now requires the **executed URL or query
string** to be recorded verbatim alongside the declared query, so mismatch is
visible at review rather than discoverable only by re-reading both.

**Not re-run in this pass.** Pre-committed stopping rules forbid extending a
sample to reach a conclusion, and re-running immediately after seeing a null
result sits uncomfortably close to that. It goes to the next harvest with the
declared query executed as written.

---

## 2. One usable finding — from an unexpected source class

The second retrieval was Aider's own troubleshooting documentation. That is
**Class A, not Class C** — it is the project documenting itself.

It is an unusually candid Class A source, because it documents a failure mode the
publisher has no incentive to publicise:

> "Weaker models are more prone to disobeying the system prompt instructions.
> **Most local models are just barely capable of working with aider, so editing
> errors are probably unavoidable.**"

> "Sometimes the LLM will reply with some code changes that don't get applied to
> your local files… this usually happens because the LLM is disobeying the system
> prompts and trying to make edits in a format that aider doesn't expect."

Documented mitigations: keep context under ~25k tokens, use `/drop` and
`/clear`, switch to a more capable model, `--edit-format whole`, `--architect`
mode.

### Why this matters more than it first appears

In M5 I asserted `cap-offline-operation` for Aider from documented local-runtime
support (LM Studio, Ollama) and **flagged it in the entity's own open questions
as below bar** — the capability's `evidence_requirement` is `demonstrated`, and
I had only `documented`.

This source resolves that flag in a direction I did not anticipate. The vendor
documents that local models work **marginally**, with edit failures described as
"probably unavoidable". So the capability is not simply unverified — it is
**verified as degraded**.

`cap-offline-operation` for Aider should therefore be recorded with a
qualification, not removed and not confirmed. A reader choosing Aider for
offline work needs to know the vendor's own position is "this barely works."

---

## 3. Outcome against the threshold

| Dimension | Convergent specific behaviours found | Threshold (EVIDENCE §4) | Result |
|---|---|---|---|
| **D7** — Developer experience | 0 | ≥3 independent Class C | **remains `not_scored`** |
| **D9** — Flexibility | 0 Class C (1 Class A limitation) | ≥3 independent Class C | **remains `not_scored`** |

**Publishing as insufficient**, exactly as the declaration pre-committed. Zero
convergent Class C behaviours were obtained because the one Class C sample was
invalid and the other retrieval was a different source class.

**This is a null harvest, and it is being reported as one.** The temptation to
count the Aider documentation toward D9 and declare partial progress is precisely
what the authority matrix exists to prevent: Class A is inadmissible for X-type
experience claims no matter how candid it is.

---

## 4. What the next harvest changes

1. Execute the declared query verbatim; record the executed string.
2. Search **issue bodies and comments**, not titles — friction reports live in
   comment threads, and title-level search systematically misses them.
3. Do not filter by label. Labels encode the maintainer's taxonomy, not the
   user's experience, and `enhancement` in particular routes complaints away from
   view.
4. Add long-form practitioner posts as a second platform; issue trackers
   over-represent bugs and under-represent workflow friction, which is most of
   D7.

**Estimated effort of the corrected pass:** low. This failure cost one retrieval
and produced a better protocol.
