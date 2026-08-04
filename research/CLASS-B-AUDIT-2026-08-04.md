# CLASS B RETROACTIVE AUDIT + CLASS C SAMPLING DECLARATION

**Date:** 2026-08-04 · **Triggered by:** SOURCES.md v1.1 (Methodology Depth)

---

## Part 1 — Retroactive audit

Every Class B source in the corpus, re-checked against the §1.5 depth rule and
the §1.6 completeness checklist.

**Corpus size: 1 Class B source.** Small enough to audit exhaustively, which is
the only reason this rule change is cheap. Applying it later, across dozens of
sources, would have been expensive — and the sources admitted before the rule
existed would have been the least trustworthy in the corpus.

### `src-artificialanalysis-methodology-2026-08-04`

| Element | Found? | Where |
|---|---|---|
| Methodology disclosure | ✅ core | `/methodology/performance-benchmarking` |
| Measurement procedure | ✅ core | TTFT and output-speed definitions |
| Statistical treatment | ✅ core | Median P50 / 72h; 14-day for 100k |
| Sampling strategy | ✅ | 8×/day; 1k, 10k, 100k workloads |
| Update cadence | ✅ | approximately every 3 hours |
| Limitations | ✅ | TTFT location sensitivity acknowledged |
| Reproducibility | ❌ | No code, data, or harness released |

**Grade: B-full** (3/3 core + 4/4… minus reproducibility = 3 supporting, above
the ≥3 threshold).

**Verdict: STILL ADMISSIBLE.** Depth searched: 1 hop. Assessment page recorded.

### Audit summary

| Outcome | Count | Sources |
|---|---|---|
| Still admissible | **1** | `src-artificialanalysis-methodology-2026-08-04` (B-full) |
| Downgraded | 0 | — |
| Upgraded | 0 | — |
| Requires further investigation | 0 | — |

### What the audit found that the original assessment missed

Nothing about the verdict changed. **But the original record did not distinguish
between the page where the claim was found and the page where methodology
lives** — those happened to differ, and the record silently used the deeper one
without saying so.

Had a reviewer later re-checked from the capture page (`/methodology`), they
would have found insufficient disclosure and concluded the source was
misclassified. The audit trail was broken even though the answer was right.

`assessed_at_url` and `depth_searched` now exist precisely so that a future
reviewer can reproduce the *assessment*, not just the claim.

### Class E reclassification note

Two existing sources are recorded as Class A but were captured at index-page
depth and lack the detail their deeper pages hold
(`src-kimi-models-2026-08-04`, `src-swebench-repo-2026-08-04`). **The depth rule
does not apply to Class A** — vendor documentation is authoritative about the
vendor regardless of which page it sits on. Their gaps are coverage gaps, not
admissibility problems, and they are already recorded as such.

---

## Part 2 — Class C sampling declaration for D7 and D9

**Declared before any source is read**, per METHODOLOGY §4. Recording the plan
first is what makes the sample reproducible rather than a search for confirmation.

### Target dimensions

| Dimension | Why Class C is the *authoritative* class here |
|---|---|
| **D7 — Developer experience** | Friction between intent and result is not measurable from documentation and not captured by any benchmark. The authority matrix (SOURCES §3) makes field reporting authoritative for X-type claims. |
| **D9 — Flexibility** | How far a tool bends before breaking is only visible when people push it past intended use. |

### Population, declared

| | |
|---|---|
| **Platforms** | GitHub issues and discussions on the repositories of harnesses already in the corpus; practitioner long-form posts |
| **Entities in scope** | `ent-harness-claude-code`, `ent-harness-aider` — the only L3 entities populated |
| **Query terms** | friction · confusing · workaround · gave up · switched to · unexpected behaviour · limitation |
| **Negative-case terms (mandatory)** | problems · limitations · migrated away · issues |
| **Time window** | 2026-02-01 → 2026-08-04 (6 months) |
| **Sample rule** | Top-N by engagement **and** most-recent N. Hype lives in the first, reality in the second |
| **Convergence bar** | ≥3 independent reports of the **same specific behaviour** before an X-type claim is created. Sentiment volume is not convergence |

### Pre-committed stopping and failure conditions

- **Stop** when the declared queries are exhausted or convergence is reached on
  ≥3 specific behaviours per entity.
- **Publish as insufficient** if fewer than 3 convergent behaviours emerge — D7
  and D9 stay `not_scored`, and that is a valid outcome.
- **Do not** extend the window or add platforms to reach a conclusion. Extending
  the sample after seeing results is the exact failure Pipeline E's gate exists
  to prevent.

### Threshold to leave `not_scored`

Per EVIDENCE §4: D7 and D9 each require **≥3 independent Class C reports
converging on specific behaviours**, sampled under this declaration.

---

## Part 3 — Is the Class B framework stable enough to scale?

**Yes, with one caveat.**

**Stable:** the depth rule and completeness checklist are mechanical, produce a
recorded grade, and are auditable after the fact. The schema enforces recording
of `assessed_at_url`, `depth_searched`, and `completeness`. A reviewer can
reproduce any assessment.

**The caveat:** the checklist has been exercised against exactly **one** source,
which passed comfortably. It has never been tested against a borderline case —
a source with a methodology page that is mostly marketing, or one where
methodology is split across a paper and a website with the two disagreeing.

**Prediction, recorded now so it can be checked:** the first genuine
disagreement will be over element 2 (measurement procedure) — the boundary
between "we measure latency" and "here is exactly what we timed" is where
promotional benchmarks are most likely to look sufficient without being so.

**Not blocking the harvest.** The rule is strictly better than what preceded it
(which was implicit and unrecorded), and refusing to scale until the checklist is
battle-tested would be a different kind of over-caution. Borderline cases get
logged for review rather than resolved silently.
