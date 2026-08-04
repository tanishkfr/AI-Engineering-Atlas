# REPLICATION AUDIT — RQ-18/19

**Date:** 2026-08-04 · **Subject:** `REPORT-RQ-18-usage-profile.md` (frozen)
**Objective:** determine what generalizes — **not** to strengthen the result

> **RQ-18 is closed.** No further analysis of the originating dataset is
> permitted. Additional passes over the same transcripts cannot distinguish a
> true effect from an operator artifact, however sophisticated they get.
> **One replication is worth more than ten reanalyses.**

---

## 1. The core distinction

> **The parameter values are local. The sensitivity structure is general.**

Everything below follows from that. We measured *one operator on one harness*, so
the numbers describe that pair. But *why* those numbers matter — the arithmetic
by which a cache rate dominates a cost model — is vendor-published and holds for
anyone.

---

## 2. Operator-specific — do NOT generalize

These describe one person's working intensity and subject matter. They should
never be quoted as ecosystem facts.

| Conclusion | Why it is operator-bound |
|---|---|
| 4.51B tokens / 56 days | Pure intensity. Says nothing about anyone else. |
| 2,123 sessions · 18,604 turns | Same. |
| **I/O ratio 197.69 : 1** | Determined by *what work was done*. The measured window was document-heavy Atlas research — read a lot, write prose. A code-generation-heavy operator would plausibly land an order of magnitude lower. |
| Tool-call distribution | Reflects this operator's toolchain and habits. |
| 11,666 error records | Intensity-scaled; no denominator. |

**Consequence:** the `use-*` profiles updated from this study must be labelled
**operator-derived**, not "measured" in a way that implies population validity.
A cost figure computed from them is *"what this would cost someone working like
our operator"* — which is a legitimate and clearly-scoped claim, and not the same
as *"what this costs."*

## 3. Harness-specific — likely generalizes across operators, NOT across harnesses

| Conclusion | Why it is harness-bound |
|---|---|
| **Cache hit rate 0.9432** | This is the *harness's caching strategy*, not the operator's behaviour. The operator does not choose what gets cached; the scaffold does. A harness that caches only the system prompt — or not at all — would produce a radically different figure from identical work. |
| Cache reads = 94% of all presented tokens | Same cause. |
| `sessionId` ≈ 2-turn median | An artifact of how this harness writes transcripts, not of how humans work. |
| Availability of the telemetry at all | Other harnesses may not emit usage blocks. |

**This is the load-bearing one.** The entire 83% cost correction rests on the
cache hit rate. If it is harness-determined — and the mechanism says it is — then
**cost answers must be published per-harness, not per-model.** That is a
structural change to how the Atlas reports cost, and it is currently unproven.

Registered as **RQ-28**, now the highest-priority open question in the program.

## 4. Should generalize — structural, not empirical

These follow from vendor-published pricing arithmetic and hold for any operator
and any harness.

| Conclusion | Why it holds generally |
|---|---|
| **Cache hit rate dominates effective input cost** | Cache reads bill at 0.1× input for one major vendor and ~1/120× for another. At any high hit rate the effective input price collapses toward the cache rate, regardless of headline price. Arithmetic, not observation. |
| **Cost is more sensitive to cache rate than to model choice within a tier** | Follows directly. A 2× headline price difference is swamped by a 0.5→0.95 hit-rate difference. |
| **A uniform per-vendor delta implies a uniform cache multiplier** | The identical −81.4% across five Claude models reflects that vendor applying 0.1× uniformly. Reproducible from the pricing table alone. |
| **Assumed cache rates of 0.3–0.6 are probably too low for caching agentic harnesses** | Such harnesses re-send a stable system prompt and repo context every turn *by design*. High reuse is the intended behaviour, not an accident. |
| **Retrospective telemetry has zero observer effect** | Methodological, not empirical. Data written before the question was posed cannot have been shaped by it. |

**Practical upshot:** even if the 0.9432 figure fails to replicate entirely, the
*finding that the Atlas was measuring the wrong variable* survives. We were
tuning model selection while cache behaviour moved cost by an order of magnitude
more.

---

## 5. Minimum falsification design

The smallest experiment that could overturn the result — not the most thorough.

### R1 — Same harness, different operator ⚡ **run this first**

**Cost: ~2 minutes, $0, no setup.** A second person runs:

```bash
python scripts/evidence/usage_profile.py --days 56 --share
```

`--share` emits **aggregate ratios only** — no project hashes, no session counts,
no tool names, no timestamps. Safe to send as a single line.

**Isolates:** operator. Holds harness constant.

**Preregistered falsification thresholds:**

| Observed cache hit rate | Verdict |
|---|---|
| ≥ 0.85 | **Replicates.** Correction is harness-level; apply broadly for this harness. |
| 0.70 – 0.85 | **Partial.** Direction holds, magnitude is operator-sensitive. Report a range, not a point. |
| **< 0.70** | **FALSIFIED as a general figure.** The 0.9432 is idiosyncratic; every cost correction reverts to operator-scoped and must be relabelled. |

I/O ratio is **expected** to diverge widely and is *not* a falsification target —
§2 already classifies it as operator-bound. Predicting it will differ is not a
prediction that costs anything.

### R2 — Different harness, same operator

Run any second harness that emits token telemetry over comparable work.
**Isolates:** harness. This is the direct test of RQ-28.

Blocked on a harness that exposes `cache_read` counts. Where one does not, that
absence is itself reportable: *this harness makes its own cost unauditable.*

### R3 — Different harness, different operator

The real generalization test. Only meaningful **after** R1 and R2 have separated
the two factors — running it first would confound them and waste the strongest
evidence available.

### What a successful R1 does and does not license

| Licensed | **Not** licensed |
|---|---|
| Treating the correction as **harness-level** | Treating it as universal |
| Publishing cost figures scoped to that harness | Publishing unscoped cost figures |
| Retiring the "operator-specific" caveat on cache rate | Retiring it on I/O ratio or volume |

---

## 6. What we will not do

- ❌ Re-analyse the originating transcripts at finer grain
- ❌ Segment by project, week, or task type to "check robustness" — segmenting one
  operator's data produces correlated sub-samples that *look* like independent
  confirmation and are not
- ❌ Extend the window past 56 days
- ❌ Publish an unscoped cost figure before R1 returns

**The most tempting error here is a robustness check that feels rigorous and
adds no information.** Ten cuts of one operator's data still have n=1.

---

## 7. Status changes

| Item | Change |
|---|---|
| RQ-18 | **CLOSED** — frozen, no further analysis |
| RQ-19 | **CLOSED**, scoped harness-level pending R1 |
| **RQ-28** | **Promoted to highest-priority open question** — is 0.9432 harness-determined? |
| `use-*` profiles | Relabelled **operator-derived**; cost outputs must carry the scope |
| Retrospective telemetry | Adopted as Pipeline G; **breadth still requires other operators** |
