# RQ-05 — Harness effect size

**Status:** accepted · **ERI:** Decisive · **Effort:** High
**Flagship track:** yes · **Opened:** 2026-08-03

---

## 1. Research question

**What share of observed variance in agentic coding outcomes is attributable to
the harness rather than the model?**

## 2. Why it matters

This is arguably the central unanswered question of the field, and answering it
determines what kind of resource the Atlas should be.

Every observable outcome in agentic coding is produced by a model *inside* a
harness: the scaffold decides what gets read, what gets edited, when a command
runs, when to stop, how context is compacted, whether work is cached. Public
discourse attributes the result almost entirely to the model. Benchmarks report
model names. Leaderboards rank model names.

If harness variance is large — and the M1 scan's six mutually incomparable
figures for one nominal benchmark suggests it is — then:

- **Model-level recommendations are close to meaningless**, and the Atlas is
  right to recommend stacks rather than products (DECISION §10). That decision
  is currently a principled assertion; this experiment makes it an empirical one.
- Benchmark scores attributed to models are **systematically miscredited**.
- The cheapest route to better output may be changing scaffold, not model — a
  recommendation nobody currently makes because nobody has the number.

If harness variance is *small*, the opposite follows and we should say so
plainly, including where it contradicts our own architecture.

**Recommendation surface affected:** every D1/D2/D3 score (all of which are
already required to record a `via` harness), the stack-vs-product framing, and
the interpretation of every external benchmark the Atlas cites.

## 3. Current evidence

| Evidence | Source | Class |
|---|---|---|
| Six divergent SWE-bench figures in circulation for nominally comparable subjects | `research/scan-2026-08-03.md` F4 | E — **pointer only** |
| Per-model tool-use system prompt overhead varies 286–804 tokens | `src-anthropic-pricing-2026-08-03` ex.10 | A, verbatim |
| EVALUATION §3 already forbids scoring a model without harness context | internal | — |

**Effectively nothing.** The strongest signal is a Class E observation that
published numbers disagree — which establishes that *something* varies, not what.

## 4. Missing evidence

- Any controlled factorial run: same task suite, same prompts, N models × M
  harnesses
- Variance decomposition attributing outcome differences to model, harness, and
  interaction
- Whether the interaction term is large (i.e. some models suit some harnesses),
  which would make even stack-level generalization fragile
- Whether harness effect differs by task class — plausibly large for long-horizon
  work and small for single-file edits

## 5. Proposed experiments

### `exp-harness-effect-size-v1`

**Design.** Factorial, fully crossed where feasible.

- **Factors:** model (N ≥ 3, spanning capability tiers) × harness (M ≥ 3,
  spanning at least one model-agnostic CLI, one IDE-resident agent, and one
  minimal baseline scaffold)
- **Task suite:** the standing suite (METHODOLOGY §7), stratified by task class
  so per-class effects are separable
- **Replication:** ≥3 runs per cell — nondeterminism is the whole reason a single
  run cannot answer this
- **Held constant:** task definitions, repository state, time window, and the
  *user-level* prompt. Harness system prompts are **not** held constant, because
  the system prompt is part of the harness and normalizing it would define the
  effect away.

**Analysis.** Two-way ANOVA / variance decomposition on each metric:
task success, intervention count, cost per completed task, output quality
against a rubric fixed before outputs are seen.

**Preregistered prediction.** Harness accounts for ≥30% of outcome variance on
long-horizon tasks, and <15% on single-file edits. Recorded in advance.

**The minimal baseline scaffold matters more than it looks.** A deliberately
thin harness — read, edit, run, loop — is the control that makes "what does the
sophisticated harness actually add?" answerable. Without it, we would only be
comparing products to each other.

### Honest design limitations

- **Combinatorial cost.** N×M×tasks×replications grows fast; reduced coverage
  (fractional factorial) weakens the interaction term specifically, which is one
  of the more interesting outputs.
- **Harness versions move under us.** Every cell must record harness version;
  results are valid for a version pair, and the dataset is longitudinal by
  necessity rather than by ambition.
- **Rubric scoring is the soft joint.** Quality scoring is human judgment. Fix
  the rubric first, score blind to condition where possible, and publish the
  rubric.

## 6. Expected impact on recommendations

| Component | Estimate | Basis |
|---|---|---|
| breadth | **0.9** | Every quality, autonomy, and stack query |
| flip_probability | **0.6** | If harness dominates, recommended stacks change composition, not just ranking |
| magnitude | **5/5** | Changes what the Atlas recommends *at all* — products vs stacks |

**ERI: Decisive.** The highest-magnitude question in the portfolio. It is ranked
below RQ-01 only because RQ-01 is decisive *and* nearly free.

## 7. Estimated effort

**High.** Weeks, and ongoing as a flagship track.

| Component | Effort |
|---|---|
| Task suite implementation and instrumentation | ~1 week |
| Harness integration (M harnesses, headless operation) | ~1 week, **binding constraint** |
| Runs | compute + API spend, scaling with N×M×replications |
| Blind rubric scoring | substantial human time |

**Binding constraint:** getting M harnesses to run the same task
non-interactively and comparably. Several are not designed for headless
operation, and forcing them into it risks measuring our integration rather than
the harness.

## 8. Current confidence

**In the answer: very low.** We have a directional belief that harness effects
are large, sourced from a Class E observation that numbers disagree. That is
close to no evidence. The preregistered 30%/15% split is a stated prior we fully
expect to be wrong about in at least one direction.

**In the question: high.** Whatever the answer, it changes how this Atlas —
and arguably the whole field — should present its results.
