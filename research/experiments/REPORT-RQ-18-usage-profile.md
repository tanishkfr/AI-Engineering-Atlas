# RQ-18/19/20 — Usage Profile Measurement

**Technical report** · **Executed:** 2026-08-04 · **Preregistered:** same day, frozen before run
**Method:** retrospective metadata extraction · **Cost:** $0.00 · **Reproducible:** yes

---

## 1. Executive summary

Two assumptions that underpinned every cost figure in the Atlas were measured and
**both were wrong by roughly an order of magnitude**, in the same direction.

| Parameter | Assumed | **Measured (56d)** | Error |
|---|---|---|---|
| Cache hit rate | 0.35 – 0.60 | **0.9432** | ~1.9× the top of range |
| Input : output ratio | 4:1 – 20:1 | **197.7 : 1** | ~10× the top of range |

**Consequence: every cost figure the Atlas has ever produced was overstated by
~81–89%.**

The recommendation impact is concrete. Under the assumed profile, a $20/month
ceiling excluded **every** Claude model. Under measurement it admits three of
them, including Claude Sonnet 5 at **$13.23/month**.

**Scale:** 2,132 transcripts · 2,123 sessions · 18,604 assistant turns ·
**4.51 billion tokens presented to a model.** Zero friction, zero behaviour
change, zero cost.

---

## 2. Method

Retrospective extraction from agent transcripts already written to disk. No
prospective logger; no change to how work was done.

**Metadata only by construction.** A fixed allowlist of numeric and enum fields —
token counts, timestamps, model IDs, tool *names*, error counts. No code path
exists by which message content, file contents, paths, prompts, code, or branch
names could reach the output. Project identity is one-way hashed.

**Primary window: 56 days.** The 7-day window is a freshness comparison only,
per the frozen preregistration §0.

## 3. Results

### 3.1 Primary — 56 days

| | |
|---|---|
| Files scanned | 2,132 |
| Sessions | 2,123 |
| Assistant turns | 18,604 |
| Uncached input | 1,566,443 |
| Cache write | 254,623,681 |
| Cache read | 4,252,826,897 |
| Output | 22,808,033 |
| **Total presented** | **4,509,017,021** |
| **Cache hit rate** | **0.9432** |
| **I/O ratio** | **197.69 : 1** |
| Distinct models | 7 |
| Error records | 11,666 |

### 3.2 Freshness comparison — 7 days

| Metric | 56d | 7d | Relative divergence |
|---|---|---|---|
| Cache hit rate | 0.9432 | 0.9511 | **0.8%** |
| I/O ratio | 197.69 | 241.12 | **22.0%** |

Both fall under the preregistered 25% divergence threshold, so **no
workload-variability finding is triggered**. The 56-day figure stands as primary,
as declared in advance.

The I/O divergence at 22% is close to the line and directionally consistent with
recent work being unusually read-heavy. Worth watching, not worth acting on.

## 4. Cost recomputation

Presented-input volume held constant at 25M/month so the comparison isolates the
two measured parameters. Prices are captured Class A facts.

| Model | Assumed $/mo | **Measured $/mo** | Δ |
|---|---|---|---|
| Claude Fable 5 | 237.50 | **44.10** | −81.4% |
| Claude Opus 5 | 118.75 | **22.05** | −81.4% |
| Claude Sonnet 5 (from 2026-09-01) | 71.25 | **13.23** | −81.4% |
| Claude Sonnet 5 (introductory) | 47.50 | **8.82** | −81.4% |
| Claude Haiku 4.5 | 23.75 | **4.41** | −81.4% |
| DeepSeek V4 Pro | 7.22 | **0.81** | −88.7% |
| DeepSeek V4 Flash | 2.35 | **0.30** | −87.2% |

**Mean delta: −83.3%.**

**The identical −81.4% across all Claude models is structural, not coincidental.**
That vendor prices cache reads at exactly 0.1× input for every model, so the
cache-rate correction scales all of them by the same factor. DeepSeek's larger
delta follows from its far more aggressive cache discount (~1/120th of a miss).

**Ranking did not change.** Every model moved by a similar proportion, so relative
order is preserved. The decision that changes is *affordability*, not *ordering*.

## 5. Recommendation delta

| | Assumed | Measured |
|---|---|---|
| Models fitting **$20/month** | DeepSeek V4 Pro, DeepSeek V4 Flash | + **Claude Haiku 4.5**, **Claude Sonnet 5** (both pricing periods) |

Under the old assumption, a reader with $20/month was steered exclusively toward
open-weight models. Under measurement, a frontier mid-tier model fits inside that
budget with headroom.

**This is the single largest recommendation change in the project's history**, and
it was caused by correcting our own guess — not by any change in the market.

## 6. Assumptions eliminated

| RQ | Status | Basis |
|---|---|---|
| **RQ-18** token volume, I/O ratio, sessions | ✅ **RESOLVED** | 18,604 turns over 56 days |
| **RQ-19** cache hit rate | ✅ **RESOLVED** | 4.25B cache-read tokens measured directly |
| **RQ-20** retry / rework rate | ⚠️ **PROXY ONLY** | 11,666 error records counted; "rework" has no transcript ground truth |
| **RQ-21** content mix | ❌ **OPEN** | Requires content classification, which the privacy design forbids |

**Two resolved outright. Not four.** RQ-20's error count is a countable proxy and
is not the same quantity; RQ-21 is untouched.

## 7. Threats to validity — and one realized

| Threat | Status |
|---|---|
| **Single operator, single toolchain** | **Realized and severe.** This profile describes one person's work. Every derived cost figure must say so. It is not a population estimate. |
| **`sessionId` ≠ human work session** | **Realized.** Median session is 2 turns / 0.3 min across 2,123 sessions — most are trivial or aborted. Per-session medians are therefore **not** meaningful and are excluded from conclusions. Aggregate token ratios are unaffected. |
| Harness-specific cache behaviour | Standing. The 0.9432 rate is a property of this harness. Not transferable. |
| Workload atypicality | Partially mitigated by the 56-day window; 7d/56d divergence of 22% on I/O suggests residual recency effect. |

## 8. New research questions generated

| RQ | Question | Why it matters |
|---|---|---|
| **RQ-28** | Is a ~0.94 cache hit rate typical, or an artifact of this harness and workload? | The entire cost correction rests on it. If harness-specific, cost answers must be **per-harness**, not per-model. |
| **RQ-29** | Does I/O ratio vary systematically by task class? | 197:1 aggregate may hide code-generation work at 10:1. Would change per-persona profiles. |
| **RQ-30** | What is the correct unit of "session"? | The 2-turn median shows `sessionId` is the wrong grain. Blocks all per-session cost reporting. |
| **RQ-31** | What fraction of the 11,666 error records represent real rework? | Determines whether RQ-20 can close from this data. |

## 9. Should retrospective telemetry become a permanent pipeline?

**Yes — formally adopted, with two stated limits.**

**The case for:**

| | Retrospective | Prospective |
|---|---|---|
| Friction | Zero | Requires setup and discipline |
| Observer effect | **None** — data predates the question | Instrumentation can change behaviour |
| History available | 56 days immediately | Starts at zero |
| Cost | $0.00 | Operator time |
| Reproducibility | Exact — same files, same result | Cannot re-run a past week |

The observer-effect point is the decisive one and it is a **validity advantage**,
not merely convenience. Data written before the question was asked cannot have
been shaped by it.

**The limits, which prevent it replacing prospective work entirely:**

1. **It can only answer questions the telemetry already records.** RQ-21 is
   unanswerable retrospectively at any sample size. Prospective instrumentation
   remains necessary where the needed field does not exist.
2. **It inherits whatever population wrote the logs.** Here: n=1. Retrospective
   telemetry scales in *depth*, never in *breadth*.

**Adopted as EVIDENCE.md Pipeline G, with the standing rule:**

> Before designing any prospective instrument, check whether the measurement
> already exists in telemetry. Prefer retrospective extraction where the field is
> present; use prospective instrumentation only for fields that are not.

Applying that rule to RQ-18 turned a one-week prospective study into an
eight-week retrospective one, executed the same day, at no cost, with a stronger
validity argument.

## 10. Replication

```bash
python scripts/evidence/probe_transcripts.py
python scripts/evidence/usage_profile.py --days 56
python scripts/atlas/cost_delta.py
```

Deterministic. Outputs to `research/evidence/usage/`.

**To falsify:** run against a different operator's transcripts. A cache hit rate
materially below 0.9432, or an I/O ratio near the originally assumed 4:1–20:1,
would show this profile is idiosyncratic and that the cost correction should not
generalize. **We expect that test to weaken the result and want it run.**
