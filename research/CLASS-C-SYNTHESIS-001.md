# CLASS C SYNTHESIS 001 — D7

**Date:** 2026-08-04 · **Tool:** `scripts/evidence/synthesize.py`
**Verdict:** ⚠️ **NOT_SCOREABLE** — D7 remains `not_scored`

---

## Result

164 records analysed from two primary-source harvests.

**All four corpus gates PASS:**

| Gate | Value | Threshold | |
|---|---|---|---|
| Independent threads | 162 | ≥5 | ✅ |
| Distinct participants | 157 | ≥50 | ✅ |
| Platforms | github, hacker_news | ≥2 | ✅ |
| Max single-thread share | **0.6%** | ≤40% | ✅ |

**Behaviour convergence FAILS:**

| Behaviour probe | Threads | Platforms | Qualifies |
|---|---|---|---|
| `unexpected_cost_spike` | 1 | 1 | ❌ <3 threads |
| `rate_limit_interrupts_session` | 0 | — | ❌ |
| `context_exhaustion_forces_restart` | 0 | — | ❌ |
| `over_asks_before_acting` | 0 | — | ❌ |
| `edits_not_applied` | 0 | — | ❌ |

**0 of 5 behaviours reached the ≥3-independent-threads / ≥2-platforms bar.**

---

## The finding: corpus gates measure independence, not relevance

This is the important part, and it is a gap in our own protocol.

The sample is **large, independent, and recent** — 157 distinct participants
across 162 threads, with the largest single thread contributing 0.6% of
participants, sixty-six times better than the 40% ceiling. By every structural
measure this is an excellent Class C corpus.

It contains almost no friction reports.

The harvest queries were `"claude code"` and `"switched from claude code"` —
**entity-targeted**, not **friction-targeted**. They returned discussion *about*
the tool: announcements, comparisons, general commentary. The behaviour probes
are deliberately specific, as COMMUNITY-EVIDENCE-PROTOCOL §4 requires ("It's
slow" must not match). Specific friction language is simply not present in a
sample selected by product name.

> **A corpus can pass every independence gate and still be the wrong corpus.**
> Volume and independence are necessary and not sufficient. The protocol
> currently has no relevance gate.

The 40% rule added in M6.3 to force independence worked exactly as intended —
and independence turns out to be the easy half.

## Methodology change adopted

**COMMUNITY-EVIDENCE-PROTOCOL gains a relevance gate.** Before a harvest is
synthesized, it must clear:

- **Probe hit rate ≥ 5%** of records matching at least one behaviour probe.
  Below that the harvest is *off-target* and is re-run with different queries
  rather than analysed.

Today's hit rate: **1/164 = 0.6%.** The harvest should have been rejected before
synthesis, not after.

**Query design rule:** harvest on *symptoms*, not on *subjects*. Query the
behaviour you are looking for, then filter by entity — not the reverse.

Corrected query set for Harvest 004:

```
"rate limit" mid-session agent coding
"context window" ran out restart agent
coding agent "kept asking" clarifying questions
"edits were not applied" OR "diff failed" coding agent
"switched to" coding agent because slow OR expensive OR unreliable
```

## Outcome

| Dimension | Verdict | Reason |
|---|---|---|
| D7 | **NOT_SCOREABLE** | 0 convergent behaviours |

Published as insufficient, per the pre-committed failure conditions. This is the
third consecutive null Class C result — and the first where the *instrument*
worked and the *sampling strategy* was wrong. That is progress: the previous two
failed on protocol discipline and tooling.

## Note on the RQ-05 gate

Still shut. Three nulls now, but none is diminishing returns from a working
process: protocol error (001), tooling gap (002), off-target sampling (003).
The gate opens on a *clean, on-target* harvest that then yields little.
