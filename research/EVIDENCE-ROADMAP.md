# EVIDENCE ROADMAP

**Opened:** 2026-08-04 · **Ranks:** every missing evidence stream by Expected
Recommendation Impact · **Governs:** Track A sequencing

---

## The ranking

ERI here is measured in **benchmark questions unblocked** (of the frozen 50),
not in novelty. Effort is shown but does not reorder.

| # | Evidence stream | Unblocks | Dimensions | Effort | Experiment needed? |
|---|---|---|---|---|---|
| **1** | **Class C sampling programme** | Q17–Q25, Q33–Q37 partial | D4, D7, D9, D10, D12 | **Low** ⚡ | **No** |
| **2** | **Measured usage profiles** | Q2, Q3, Q5, Q6, Q8 | D6 | **Low–Med** ⚡ | Yes (instrumentation) |
| **3** | **Harness effect size** | Q13, Q17, Q18, Q21 + reframes all quality Qs | D1, D2, D3 | High | Yes |
| **4** | **Intervention rate** | Q21, Q22, Q25 | D2 | High | Yes |
| **5** | **Class B security capture** | Q46, Q44 depth | D13 | **Low** ⚡ | **No** |
| **6** | **Class B latency capture** | Q27 | D8 | **Low** ⚡ | **No** |
| **7** | **Frontend quality instrument** | Q10, Q37 | D1, D3 | High | Yes |
| **8** | **Continuity/governance capture** | Q43 depth | D12 | Low | **No** |
| **9** | **Context strategy comparison** | Q39, Q40, Q41 | D1, D6 | Medium | Yes |
| **10** | **Longitudinal maintainability** | Q50 partial | D5 | **Very High** | Yes — start now |
| **11** | **Canary suite** | none directly | D4, integrity | Low | Yes (automatable) |
| **12** | **Ecosystem maturity signals** | — | D10 | Low | **No** — but VOI says *negligible*; collect only if free |

---

## The finding that should change the plan

**Four of the top six streams require no experiment at all.**

Streams 1, 5, 6, and 8 are *collection discipline applied to evidence that
already exists*. They unblock five dimensions and a large share of the
harness-and-provider questions, at low effort, with no human raters and no model
spend.

Milestone 5.1 concluded the bottleneck was "no Class B/C evidence" and implied
that meant running experiments. That was half right. **The larger and cheaper
half is that we have not yet gone and collected the independent and field
evidence that is sitting in public.**

Stream 1 in particular — disciplined Class C sampling under METHODOLOGY §4 — is
the single highest-leverage action available: lowest effort in the table, and it
is the *authoritative* evidence class for D7 and D9 under the authority matrix,
not a fallback.

---

## Sequencing

**Phase 1 — harvest (no experiments)**
Streams 1, 5, 6, 8. Target: D4, D7, D9, D12, D13 leave `not_scored`.
This is the fastest path from 7/50 to a materially higher number.

**Phase 2 — instrument (cheap experiments)**
Streams 2, 11. Measured usage profiles unblock every absolute cost figure; the
canary suite protects everything else from silent endpoint drift.

**Phase 3 — flagship measurement**
Streams 3, 4, 9. The expensive factorial work, sharing one instrumentation base.

**Phase 4 — long horizon**
Streams 7, 10. Frontend instrument construction, and the maintainability study
that must start early because it is gated on elapsed time rather than effort.

**Stream 10 starts in Phase 1 despite ranking 10th.** It takes months to yield
anything; delaying it delays the answer by exactly as long as you delay the
start.

---

## Track A / Track B

Track A is this roadmap. Track B runs in parallel and is not subordinate to it.

| | Track A — Evidence | Track B — Reference |
|---|---|---|
| **Goal** | Make scoring possible | Make the Atlas useful to read today |
| **Measured by** | Coverage (x/50) | Canonical entity pages for things people search for |
| **Next up** | Phase 1 harvest | Qwen, Kimi K3, DeepSeek, OpenCode, Hermes, Cursor |
| **Quality bar** | Evidence thresholds (EVIDENCE §4) | The 17-section standard; `not_scored` stated honestly |

**Why Track B is not a distraction.** An entity page that cannot yet be scored is
still the best available reference on what a thing is, what it costs, what it
does not do, and what nobody has established about it. That has standalone value
for a reader, and it is what makes the Atlas worth visiting before the
recommendation engine is trustworthy.

**The correction being recorded:** M5.1 argued against populating more entities
because it would not move the coverage score. That was correct about the metric
and wrong about the product. Coverage measures decision quality; it does not
measure reference value, and optimizing only for it would produce a research
instrument nobody reads.

---

## Milestone reporting format

Every milestone now opens with coverage, not output:

```
Coverage
7 / 50
  ↓
Goal
12 / 50
```

Followed by the Track A and Track B objectives that are expected to get there.
Entity counts are reported only as a footnote.
