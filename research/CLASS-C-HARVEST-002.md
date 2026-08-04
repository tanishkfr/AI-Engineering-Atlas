# CLASS C HARVEST 002 — migration signals

**Date:** 2026-08-04 · **Protocol:** COMMUNITY-EVIDENCE-PROTOCOL v1.0
**Outcome:** ⚠️ **Class E pointers only — no Class C admitted**

---

## 1. What was executed

**Declared queries, recorded verbatim** (corrective action from Harvest 001):

```
"switched from Cursor to" OR "moved from Cursor to" Claude Code OpenCode reddit 2026 why
reddit developers "switched from Claude Code" OR "left Claude Code" 2026 reasons friction
```

Both included negative-case terms as the declaration requires. The queries
matched the declaration this time.

## 2. Why nothing was admitted

Every result was a **secondary summary of community sentiment** — blog posts,
Medium and Substack articles, and dev.to pieces *about* Reddit threads. One was
titled "What 500+ Reddit Developers Really Think".

Under COMMUNITY-EVIDENCE-PROTOCOL §7 these are **Class E, pointer only**,
regardless of how many practitioners they claim to represent.

**This is the exact laundering the protocol was written to prevent.** Citing
"500+ Reddit developers" from an article would put one writer's reading of a
forum into the corpus as though we had sampled five hundred people. We sampled
zero.

**Zero threads retrieved. Zero participants counted. Thresholds not approached:**
5 independent threads (0), 50 participants (0), 2 platforms (0).

## 3. What the pointers are legitimately good for

Directing the next harvest. Recorded as **investigation targets, not findings** —
no claim is created from any of them.

### Migration themes to investigate

| Theme | Direction | Would inform | Status |
|---|---|---|---|
| Usage limits hit mid-session, breaking flow | away from vendor-locked | D4, D7, RQ-02 | **unverified** |
| Token burn from aggressive context management | away | D6, RQ-03 | **unverified** |
| Over-asking clarifying questions before acting | away | D7, D2 | **unverified** |
| Perceived quality change over time | away | D4 | **unverified** |
| Running multiple tools rather than switching | neither | adoption modelling | **unverified** |

That last one matters most methodologically: if practitioners commonly *add*
rather than *replace*, migration counts overstate displacement, and the protocol's
`partial` field is load-bearing rather than a nicety.

### One pointer that is checkable against Class A — and would be a delta

Several secondary sources assert that access to a vendor's top model **through
third-party tools** was restricted, such that subscription holders could not use
it inside external harnesses.

If true, this **directly qualifies `clm-harness-claude-code-004`**, which records
third-party provider support on the Terminal CLI and VS Code. Support for
third-party *providers into* the harness is a different axis from access to the
vendor's *own model from* third-party harnesses — and a reader asking "can I
avoid lock-in?" needs both.

**Not asserted.** Flagged as **RQ-17**, resolvable from first-party
documentation, and a genuine candidate recommendation delta for Q19 and Q31.

## 4. Outcome against thresholds

| Dimension | Convergent Class C behaviours | Threshold | Result |
|---|---|---|---|
| D7 | 0 | ≥3 across ≥2 platforms | **remains `not_scored`** |
| D9 | 0 | ≥3 across ≥2 platforms | **remains `not_scored`** |

**Second consecutive null harvest.** Published as insufficient, per the
pre-committed failure conditions.

## 5. The finding about our own method

Two harvests, two different failure modes:

| | Harvest 001 | Harvest 002 |
|---|---|---|
| Failure | Executed query ≠ declared query | Queries correct; results were the wrong source class |
| Cause | Protocol discipline | **Tooling** — general web search surfaces commentary, not primary threads |

Harvest 001's fix was procedural and worked. Harvest 002's failure is **not
fixable by better queries**, because general web search is optimized to return
articles, and articles about forums outrank forums.

**Corrective action for Harvest 003:** retrieve threads directly at platform URLs
(subreddit search endpoints, GitHub Discussions, HN Algolia) rather than
discovering them through general search. Class E pointers may name the platforms
and topics; the threads themselves must be fetched from the platform.

This is a **tooling requirement, now blocking Track B's largest evidence stream**
— and it is the single biggest obstacle to leaving `not_scored` on five
dimensions.

## 6. Honest note on the gate

The EVIDENCE-ROADMAP gate for executing RQ-05 is "two consecutive harvest passes
each moving fewer than two dimensions out of `not_scored`."

Two consecutive passes have now moved **zero**.

**The gate is not treated as open.** It was written to detect *diminishing
returns from a working process* — the point at which public evidence is genuinely
exhausted. What has happened instead is that the process has not worked yet: one
procedural error and one tooling limitation. Diminishing returns and a broken
instrument produce the same number and mean opposite things.

Treating this as the gate opening would use our own failures as justification for
skipping to the expensive experiment we already wanted to run. **Gate stays
shut** until a harvest executes cleanly and *then* yields little.
