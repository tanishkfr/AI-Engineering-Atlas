# PROTOCOL — The Harness Effect Study

**`exp-harness-effect-size-v1`** · **RQ-05** · Lane 3 flagship
**Status:** ⏸ **PLANNED — execution gated on evidence-harvest diminishing returns**
**Drafted:** 2026-08-04 · **Not yet preregistered** — see §0

---

## 0. Status and gating

This is a **protocol draft**, not a preregistration. It becomes a preregistration
when the harvest gate opens and the document is frozen with hypotheses fixed.

**Execution gate:** Track A Phase 1 (Class B/C harvest) must reach diminishing
returns first. Concretely — the gate opens when **two consecutive harvest passes
each move fewer than two dimensions out of `not_scored`**.

Rationale: EVIDENCE-ROADMAP found eight of thirteen dimensions unblockable
without any experiment. Running the most expensive study in the portfolio while
cheap public evidence sits uncollected would be a poor allocation, and Class D is
not automatically superior to Class B (SOURCES §1).

**Only one flagship experiment may be active.** This is it. RQ-02, RQ-03, RQ-04,
RQ-06 remain flagship *tracks* but are not in execution.

---

## 1. Research question

**What share of variance in agentic coding outcomes is attributable to the
harness rather than the model?**

Secondary: is there a significant model × harness **interaction** — i.e. do
particular models suit particular harnesses?

## 2. Why this is the centerpiece

Every observable outcome in agentic coding is produced by a model *inside* a
harness. Public discourse, benchmarks, and leaderboards attribute results almost
entirely to models.

If harness variance is large, then model-level recommendations are close to
meaningless, benchmark scores attributed to models are systematically
miscredited, and the cheapest route to better output may be changing scaffold
rather than model — a recommendation nobody currently makes because nobody has
the number.

If harness variance is small, the Atlas's stack-first architecture is
over-engineered and we should say so plainly.

**Either answer changes what the Atlas is.** No other single experiment has that
property, and no party in the ecosystem has an incentive to run it: vendors
benefit from attribution to models, harness authors from the reverse, benchmark
maintainers measure one configuration.

---

## 3. Design

### 3.1 Factorial structure

Fully crossed **M models × H harnesses × T tasks × R replications**.

| Factor | Levels | Selection rule |
|---|---|---|
| **Model** | M ≥ 3 | Span capability tiers; ≥1 open-weight; all with `tokenizer_verified` where possible |
| **Harness** | H ≥ 4 | ≥1 vendor-first CLI, ≥1 model-agnostic CLI, ≥1 IDE-resident, **+1 minimal baseline** |
| **Task** | T ≥ 8 | Stratified by class (§3.3) |
| **Replication** | R ≥ 3 | Nondeterminism is the reason a single run cannot answer this |

Minimum cells: 3 × 4 × 8 × 3 = **288 runs**.

### 3.2 The minimal baseline harness — the control that makes this work

A deliberately thin scaffold: read file, write file, run command, loop, stop on
success or budget exhaustion. No retrieval strategy, no planning phase, no
context compaction, no subagents.

**Without it the study only compares products to each other.** With it, the
question becomes answerable in the form that matters: *what does a sophisticated
harness actually add over the minimum viable loop?* We build and publish it.

### 3.3 Task suite

Eight tasks minimum, stratified — because the preregistered expectation is that
harness effect **varies by task class**, and pooling would hide it.

| Class | n | Character |
|---|---|---|
| Single-file edit | 2 | Localized change, tests exist |
| Cross-file refactor | 2 | Touches ≥4 files, must not break tests |
| Debug unfamiliar break | 2 | Planted defect, no pointer to location |
| Long-horizon feature | 2 | Multi-step, ≥30 min expected, spec provided |

All tasks run against **operator-authored repositories**, not public ones.
Public repos risk contamination — a model may have seen the fix. Authored repos
are published with the study.

### 3.4 Held constant vs deliberately varied

**Held constant:** task definitions · repository state (fresh clone per run) ·
user-level prompt · time window · model version and endpoint · temperature and
sampling settings where exposed.

**Deliberately NOT held constant:** harness system prompts, context strategies,
retry logic, tool definitions. **These are the harness.** Normalizing them would
define the effect away — the most likely way to get a confidently wrong answer.

---

## 4. Instrumentation

Per run, logged automatically:

| Signal | Feeds |
|---|---|
| Task success (test suite pass/fail) | primary outcome |
| Wall-clock duration | D8, cost |
| Input / output / cache-read / cache-write tokens | D6, RQ-03, RQ-06 |
| Retry and error counts | D4 |
| Human interventions, typed | D2, RQ-04 |
| Files touched, diff size | D5 proxy |
| Peak per-minute token rate | RQ-02 |
| Full transcript | blind scoring, audit |

**This instrumentation is shared with RQ-02, RQ-03, RQ-04 and RQ-06.** Building
it once for this study is the reason the flagship is worth its cost — four other
tracks ride on it.

---

## 5. Statistical design

### 5.1 Model

Two-way ANOVA with interaction, per task class and per outcome:

```
Y_ijkr = μ + Model_i + Harness_j + (Model×Harness)_ij + Task_k + ε_ijkr
```

Variance decomposition reports η² (proportion of variance explained) for each
term. **η² for the Harness term is the headline result.**

For binary outcomes (task success), mixed-effects logistic regression with task
as a random effect.

### 5.2 Power and the honest limitation

At R=3 per cell, power to detect a *large* main effect is adequate; power to
detect a **moderate interaction is poor**. This is stated up front because the
interaction is the most interesting term and we are least able to resolve it.

**Preregistered handling:** if the interaction term is non-significant, we report
it as *underpowered*, **not** as evidence of absence. Reporting "no interaction"
from an underpowered design would be the single most misleading thing this study
could produce.

### 5.3 Multiple comparisons

Outcomes × task classes generates many tests. Benjamini–Hochberg FDR control at
q = 0.05, applied within outcome family. Declared before analysis.

### 5.4 Preregistered predictions

| ID | Prediction |
|---|---|
| H1 | Harness η² ≥ 0.30 on long-horizon tasks |
| H2 | Harness η² < 0.15 on single-file edits |
| H3 | Harness η² exceeds Model η² on at least one task class |
| H4 | The minimal baseline is within 20% of the best harness on single-file edits, and far behind on long-horizon |

H4 is the one we most expect to be wrong, and it is the most informative if right.

---

## 6. Blind rubric scoring

Quality outcomes (D1, D3, D5) are human-rated.

1. Rubric fixed and published **before** any output is generated.
2. Outputs stripped of harness/model identifiers before rating.
3. ≥2 independent raters on an overlapping sample.
4. **Inter-rater agreement gate** (Krippendorff's α ≥ 0.67 preregistered). Below
   threshold → rubric revised and re-rated; results do not publish.
5. Disagreements adjudicated and logged, not averaged silently.

---

## 7. Threats to validity

| Threat | Severity | Mitigation |
|---|---|---|
| **Our harness integration becomes the thing measured** | **Severe** | Several harnesses are not built for headless operation. Integration code published; any harness requiring non-trivial adaptation is flagged and analysed separately |
| Underpowered interaction term | High | Declared in advance; reported as underpowered, never as null |
| Harness versions drift mid-study | High | Versions pinned and recorded per cell; runs completed within one window |
| Operator not blind during runs | High | Unavoidable. Scoring is blind; run-time interventions follow a fixed published policy |
| Task suite favours a harness's design | Medium | Stratified classes; suite published for others to contest |
| Provider-side model changes mid-study | Medium | `suite-canary` runs alongside to detect endpoint drift |
| Single operator | Medium | Documented; the bias METHODOLOGY §9 already names |
| Cost forces reduced coverage | Medium | Fractional factorial degrades the interaction first — stated as the known cost |

---

## 8. Stopping conditions

- **Stop and publish** when all cells complete at R=3.
- **Stop and publish as partial** if budget exhausts — report which cells
  completed and which terms became unidentifiable. Partial results publish.
- **Halt** if `suite-canary` detects a model endpoint change mid-study; affected
  cells re-run or excluded with reason.
- **Do not** add or drop a harness after seeing results. The roster is frozen at
  preregistration.

---

## 9. Replication plan

Published with the study: task repositories · all prompts · harness
configurations and versions · the minimal baseline harness source ·
instrumentation code · every raw transcript · the rubric · rater instructions ·
per-cell results · analysis scripts.

**Falsification target stated in advance:** an independent group running this
suite and finding harness η² below 0.15 on long-horizon tasks would contradict
H1, and we would report that prominently.

---

## 10. Expected recommendation impact

| Component | Estimate |
|---|---|
| breadth | 0.9 — every quality, autonomy, and stack question |
| flip_probability | 0.6 |
| magnitude | 5/5 — changes what the Atlas recommends *at all* |

**ERI: Decisive.**

Secondary yield, which is most of why it is sequenced first among experiments:
the instrumentation and task suite unblock **RQ-02, RQ-03, RQ-04 and RQ-06**
as byproducts.

## 11. Estimated cost

| Item | Estimate |
|---|---|
| Task suite + repositories | ~1 week |
| Minimal baseline harness | ~3 days |
| Instrumentation | ~1 week (shared with 4 tracks) |
| Harness integration | ~1 week — **binding constraint** |
| 288+ runs | inference spend + wall-clock |
| Blind rating | substantial human time, ≥2 raters |
| Analysis | ~3 days |

## 12. Ethical considerations

Runs execute against operator-owned repositories only. No third-party code is
modified. Harnesses are used within their terms; rate limits respected and not
deliberately exceeded (that is RQ-02's separate, scoped test). Raters are
informed the study is for publication. Failures and unflattering results publish
unchanged.
