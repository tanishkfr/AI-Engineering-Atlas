# PREREGISTRATION — RQ-18/19/20/21 usage profile

**Status:** 🔒 **FROZEN FOR EXECUTION** · **Amended:** 2026-08-04, before any run
**Designed:** 2026-08-04

---

## 0. Amendment — execution design (recorded BEFORE running)

| Run | Window | Role |
|---|---|---|
| **Primary** | **56 days** (full retrospective history) | **The measurement.** All assumption elimination, all cost recomputation, all deltas derive from this. |
| Secondary | 7 days | **Freshness comparison only.** Detects whether recent behaviour diverges from the 56-day baseline. Never the primary figure. |

**Why 56 days is primary:** a 7-day window on a single operator is dominated by
whatever that week happened to contain. The recent weeks are document-heavy Atlas
work — atypical by construction. The longer window dilutes that and is the more
defensible basis for a profile.

**Divergence rule, fixed in advance:** if the 7-day cache hit rate or I/O ratio
differs from the 56-day figure by **more than 25% relative**, that is reported as
a **finding about workload variability**, not as a reason to prefer either
window. The 56-day figure remains primary regardless of which looks better.

**Smoke-test values from §6 are excluded from all analysis, comparison, and
citation.** They informed hypothesis *direction* only, which §4 already discloses.

**Analysis plan, fixed:**
1. Compute 56-day profile → replaces `use-*` assumed values.
2. Recompute D6 cost for every scored candidate at captured pricing.
3. Emit a recommendation delta for every figure that moves materially.
4. Mark RQ-18/RQ-19 `resolved` only if the data actually supports it; RQ-20
   proxy-only; RQ-21 remains open.
5. Report medians and p90. **Never means alone** — the distribution is expected
   to be right-skewed and a mean would misrepresent a typical session.

---


---

## 1. The design changed after probing

The brief was a prospective logger running for a week. **A probe found that is
unnecessary.**

`scripts/evidence/probe_transcripts.py` established that local agent transcripts
already contain every field the study needs, in 40/40 sampled files:

| Field | Answers |
|---|---|
| `input_tokens` · `output_tokens` | RQ-18 token volume |
| `cache_read_input_tokens` | RQ-19 cache hit rate |
| `cache_creation_input_tokens` | RQ-19 cache write cost |
| timestamps · `sessionId` · `cwd` | sessions, duration, project grouping |

**2,137 transcripts spanning 2026-06-11 → 2026-08-04 already exist.** Verdict:
`RETROSPECTIVE_VIABLE`.

**Consequence: zero friction, zero behaviour change, and ~8 weeks of history
instead of 1.** Building a prospective logger would have collected worse data,
later, while changing the thing being measured.

This is the assumption register working as intended: asking *"can this be
measured instead?"* produced a better answer than the original plan.

## 2. What is and is not answerable retrospectively

| RQ | Assumption | Retrospective? |
|---|---|---|
| RQ-18 | Token volume, sessions, I/O ratio | ✅ fully |
| RQ-19 | Cache hit rate | ✅ fully |
| RQ-20 | Retry/rework rate | ⚠️ **proxy only** — error records are countable; "rework" has no ground truth in the transcript |
| RQ-21 | Content mix | ❌ **not answerable** — would require classifying message content, which the privacy design forbids |

**RQ-20 and RQ-21 do not close with this study.** RQ-20 gets a proxy with a
stated definition; RQ-21 stays open and needs a different method. Claiming four
assumptions eliminated when two are partial would be exactly the overreach the
register exists to prevent.

## 3. Privacy design — metadata only by construction

`scripts/evidence/usage_profile.py` extracts a **fixed allowlist** of numeric and
enum fields. It is not a content reader with a filter; there is no code path by
which content can reach the output.

**Never read or emitted:** message text · file contents · file paths · prompts ·
code · git branch names.
**Emitted:** token counts · timestamps · model IDs · tool *names* · error counts
· SHA-256-truncated project pseudonyms.

Project identity is one-way hashed so sessions can be grouped without naming
anything.

**This is the user's own working data. Deployment requires explicit approval,
and that is why the study is built but not run.**

## 4. Hypotheses — fixed before the full run

| ID | Hypothesis | Assumed value |
|---|---|---|
| **H1** | Realized cache hit rate **exceeds** the 0.35–0.60 assumed range | 0.35–0.60 |
| **H2** | Input:output ratio **exceeds** the 4:1–20:1 assumed range | 4:1 – 20:1 |
| **H3** | Session duration distribution is right-skewed; median well below mean | p90 = 1.8–3.0× |

H1 and H2 are directional and were fixed **after** a 15-file validation smoke
test (§6) and **before** the full run. That ordering is disclosed rather than
concealed — the smoke test informed the direction, so these are **not**
independent predictions and must not be reported as confirmed hypotheses. They
are recorded to make the assumed values falsifiable.

## 5. Procedure

```bash
python scripts/evidence/probe_transcripts.py                    # feasibility
python scripts/evidence/usage_profile.py --days 7  --dry-run    # inspect
python scripts/evidence/usage_profile.py --days 7               # 1-week profile
python scripts/evidence/usage_profile.py --days 56              # full history
```

Outputs to `research/evidence/usage/`. Deterministic; re-running on the same
transcripts reproduces the result exactly.

**Analysis:** compute per-session and per-day distributions; report medians and
p90, never means alone; recompute every `assumed` usage profile; regenerate the
cost model; emit a recommendation delta for every figure that moves.

## 6. Validation run — NOT the study

A 15-file smoke test confirmed the extractor runs and produces coherent output.

> ⚠️ **The numbers it produced are not findings and must not be cited.** The
> sample is 15 files from one operator's most recent sessions — document-heavy
> Atlas work, which is close to the least representative workload possible for a
> general coding profile. It is a functional test, not a measurement.

What it does establish: the pipeline works end to end, and **the assumed values
may be wrong by a large margin**, which is the reason to run the real study
rather than a reason to believe any particular number.

## 7. Stopping conditions

- Publish after the 7-day and full-history runs, whichever the operator approves.
- If fewer than 20 sessions fall in the window, report as **underpowered** and
  extend the window rather than the interpretation.
- **Do not** re-run with different windows to obtain a preferred number. Window
  choices are declared here: 7 days and full history.

## 8. Threats to validity

| Threat | Severity | Handling |
|---|---|---|
| **Single operator, single toolchain** | **Severe** | The resulting profile describes *this user*, not a population. Every derived cost figure must say so. |
| Workload atypicality — recent work is document-heavy | High | Report per-project breakdown; full-history run dilutes recency bias |
| Cache behaviour is harness-specific | High | Profile is valid for this harness; not transferable to others without re-measurement |
| `sessionId` may not equal a human work session | Medium | Report both session-grouped and day-grouped figures |
| RQ-20 proxy is not rework | Medium | Stated as a proxy; RQ-20 remains open |

## 9. Expected impact

Eliminates **RQ-18 and RQ-19 outright**, partially addresses RQ-20, leaves RQ-21
open. Unblocks every absolute cost figure in the Atlas and converts D6 from
`assumed`-derived to `measured`-derived — the first dimension in the corpus to
rest on first-party measurement.

## 10. Deployment decision required

Running this reads the user's own development transcripts. Built, validated, and
**not run**. One command away.
