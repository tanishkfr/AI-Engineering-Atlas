# EVALUATION FRAMEWORK

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Depends on:**
[SOURCES.md](SOURCES.md), [METHODOLOGY.md](METHODOLOGY.md)

How entities are scored, how scores become recommendations, and — most
importantly — what this framework refuses to produce.

---

## 0. What this framework will not do

**There is no overall score.** No "Claude Sonnet 5: 87/100". No leaderboard.

A composite number requires a weighting, and a weighting encodes whose problem
you're solving. A student on a free tier and a platform team with a compliance
review are not solving the same problem, and averaging them produces a number
that is correct for nobody while looking authoritative to everybody.

So: **dimension scores are stored; composites are computed at query time against
an explicit persona weight vector, and the weights are always visible next to
the result.** Change the persona, the ranking changes, and the reader can see
exactly why. That transparency is the product.

The second refusal: **an unscored dimension stays unscored.** No imputation, no
"assume average". `not_scored` is a rendered state.

---

## 1. The scale

All dimensions use one 5-point ordinal scale. Ordinal, not interval — a 4 is
better than a 3; it is not "one unit" better, and the numbers are never averaged
across dimensions without weights.

| Score | Label | Generic anchor |
|---|---|---|
| 5 | Exceptional | Best-in-class; defines the current ceiling. Rare by construction. |
| 4 | Strong | Clearly good; no significant reservations for its intended use. |
| 3 | Adequate | Works. Real limitations that a user will hit and can work around. |
| 2 | Weak | Frequently a problem; needs active mitigation or tolerance. |
| 1 | Poor | Disqualifying for most uses in this dimension. |
| — | `not_scored` | Not enough admissible evidence, or dimension not applicable. |

Every score carries: `value`, `confidence` (from SOURCES.md §5), `evidence`
(claim IDs), `as_of`, and `rationale` (one sentence, mandatory).

**A score with no rationale fails the build.** The rationale is what makes the
score auditable; the number alone is an opinion wearing a uniform.

### Display rule

Score and confidence render together, always. A `5` at `low` confidence must
never look like a `5` at `high` confidence — that visual equivalence is how
evidence frameworks quietly become vibes.

---

## 2. Dimensions

Twelve dimensions. Ten come from the project brief; two —
**data & licensing posture** and **continuity risk** — are added because they
decide real adoptions and are absent from every comparison article in this
space.

Not every dimension applies to every entity class (§3).

| # | Dimension | The question it answers |
|---|---|---|
| D1 | **Output quality** | How good is the work product, judged by someone who has to maintain it? |
| D2 | **Autonomy** | How far does it get without a human? |
| D3 | **Engineering output** | Does it produce *shippable engineering* — not just code that runs? |
| D4 | **Reliability** | Does it behave the same way tomorrow? |
| D5 | **Maintainability of its output** | What does the code look like in six months? |
| D6 | **Cost** | What does real usage actually cost? |
| D7 | **Developer experience** | How much friction between intent and result? |
| D8 | **Speed** | Latency and throughput as *felt*, not as benchmarked. |
| D9 | **Flexibility** | How far can you bend it before it breaks? |
| D10 | **Ecosystem maturity** | Integrations, docs, community, longevity of knowledge. |
| D11 | **Data & licensing posture** | What happens to your code, and what are you allowed to do with the output? |
| D12 | **Continuity risk** | What is the chance this is gone, gutted, or repriced in 18 months? |
| D13 | **Security posture** | What can it do if it is wrong, compromised, or fed hostile input? |

### Anchors for the dimensions that get abused most

Generic anchors invite generic scoring. These four carry the most weight in real
decisions and get explicit anchors.

**D2 — Autonomy**

| | Anchor |
|---|---|
| 5 | Completes multi-hour, multi-file tasks; recovers from its own errors; asks only when genuinely ambiguous |
| 4 | Completes substantial tasks with occasional course-correction |
| 3 | Completes well-scoped single tasks; needs supervision across steps |
| 2 | Needs correction within most tasks; drifts on anything multi-step |
| 1 | Effectively per-turn assistance only |

Measured primarily by **intervention rate per unit of completed work** (Class D
experiments), corroborated by sustained-use reports. Not by benchmark pass rate —
benchmarks are scored on the final state, which hides how many times a human
would have had to step in.

**D5 — Maintainability of output**

| | Anchor |
|---|---|
| 5 | Output is indistinguishable from a careful senior engineer's; conventions matched, abstractions earned |
| 4 | Good structure; minor cleanup before merge |
| 3 | Works, reviewable, but shows characteristic tells: over-abstraction, defensive noise, duplicated helpers |
| 2 | Needs substantial rework before it's safe to own |
| 1 | Faster to rewrite |

This dimension is the Atlas's sharpest disagreement with benchmark culture.
Benchmarks score whether tests pass. Nobody benchmarks what the codebase looks
like after three months of accepting suggestions — which is the cost that
actually lands on teams.

**D6 — Cost**

Scored on **cost per unit of completed work**, not per token. A cheap model that
needs four attempts is not cheap. Requires: pricing snapshot date, cache
behavior, and observed token consumption from Class D runs.

| | Anchor |
|---|---|
| 5 | Dramatically cheaper than alternatives for equivalent completed work |
| 4 | Good value; cost is not a factor in choosing it |
| 3 | Fair; cost management required at volume |
| 2 | Expensive enough to change how you work |
| 1 | Cost is the reason not to use it |

Never scored without a `pricing_as_of` date. Prices in this ecosystem move fast
enough that an undated cost score is disinformation.

**D12 — Continuity risk**

Scored inverted (5 = *lowest* risk), and the inversion is stated in the UI.

Inputs: funding and business-model durability, whether the thing is a feature of
a larger product, licence and forkability, single-maintainer exposure,
deprecation and repricing track record, contractual stability.

| | Anchor |
|---|---|
| 5 | Durable: open licence with real community, or core product of a stable business |
| 4 | Likely durable; no current signals of risk |
| 3 | Uncertain; dependent on one company's continued strategic interest |
| 2 | Elevated: single maintainer, unclear funding, or history of abrupt change |
| 1 | High: known deprecation trajectory, pivot signals, or repeated breaking repricing |

**D13 — Security posture** *(added v1.1; see §8)*

Scored inverted (5 = safest). Inputs: blast radius of the agent's permissions,
sandboxing and isolation model, approval gates on destructive and outbound
actions, exposure to untrusted input (retrieved web content, third-party skills
and servers, inbound messages), supply-chain posture of its extension ecosystem,
credential handling, and audit history.

| | Anchor |
|---|---|
| 5 | Least privilege by default, strong isolation, explicit gates on irreversible and outbound actions, audited extension supply chain |
| 4 | Sound defaults; residual risk is understood and documented by the vendor |
| 3 | Safe if configured carefully; unsafe defaults exist and are reachable |
| 2 | Broad system access with weak gating, or an unvetted extension surface |
| 1 | Arbitrary execution with untrusted input reaching it and no meaningful containment |

The 2026 scan justified promoting this from a facet to a dimension: agent
runtimes with system-level access reached mainstream use, independent audits
found prompt injection across a large share of sampled third-party skills, and
messaging-surface agents put untrusted inbound text directly into a loop holding
shell access. That is a decision input, not a caveat.

---

## 3. Applicability by entity class

`●` scored · `○` scored where meaningful · `—` not applicable

| | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Model** | ● | ● | ● | ● | ● | ● | ○ | ● | ● | ○ | ● | ● | ○ |
| **Harness / agent CLI** | ○ | ● | ● | ● | ○ | ● | ● | ● | ● | ● | ● | ● | ● |
| **IDE integration** | ○ | ○ | ○ | ● | ○ | ● | ● | ● | ● | ● | ● | ● | ● |
| **Agent framework** | — | ○ | ● | ● | ● | ○ | ● | ○ | ● | ● | ○ | ● | ● |
| **Inference provider** | ○ | — | — | ● | — | ● | ● | ● | ● | ○ | ● | ● | ○ |
| **Local inference stack** | ○ | — | — | ● | — | ● | ● | ● | ● | ● | ● | ● | ○ |
| **Benchmark / eval suite** | — | — | — | ● | — | — | ○ | — | ● | ● | — | ● | — |
| **MCP server / skill / tool** | — | — | ○ | ● | — | ○ | ● | ○ | ● | ● | ● | ● | ● |
| **Orchestration / runner** | — | ○ | ● | ● | — | ○ | ● | ○ | ● | ● | ○ | ● | ● |
| **Assurance tool** | ● | — | ● | ● | — | ● | ● | ○ | ● | ● | ● | ● | ○ |
| **Context / memory layer** | ○ | — | ○ | ● | — | ● | ● | ● | ● | ● | ● | ● | ● |
| **Workflow / practice** | ○ | ○ | ● | ● | ● | ○ | ● | ○ | ● | — | — | — | ○ |

Two notes that prevent category errors:

- **Model vs. harness quality is confounded and we say so.** Almost every
  observable outcome is produced by a model *inside* a harness. D1/D2/D3 on a
  model are always scored `via` a named harness, recorded in the score object.
  A model score with no harness context is not admissible.
- **Providers are not scored on model quality.** A provider serving Model X is
  scored on how well it serves it — reliability, latency, price, fidelity to the
  reference implementation. Quantization or routing that degrades output is a
  *provider* finding, and one of the more useful things the Atlas can surface.

---

## 4. Composites (persona-weighted)

Computed at query time. Never stored as an entity property.

```
fit(entity, persona) = Σ (w_d × score_d) / Σ w_d   over dimensions where score exists
```

Rules:

1. **Weights are shown.** Any composite renders with its weight vector visible.
2. **Coverage is shown.** "Scored on 8 of 12 dimensions" travels with the number.
3. **Confidence propagates.** A composite's confidence is the *floor* of its
   inputs' confidence, not the average. One shaky input makes the composite
   shaky, because that's what it means.
4. **Hard constraints filter before they weight.** A persona with "no code leaves
   our network" doesn't get a low-scoring cloud provider — it gets no cloud
   providers. Constraints are eliminations, not penalties.
5. **Near-ties are reported as ties.** Differences within the noise of an ordinal
   5-point scale are not rankings. The UI shows a band, not a podium.
6. **Every composite is reversible to its inputs.** One click from ranking to the
   dimension scores to the claims to the sources. If that chain breaks anywhere,
   the composite doesn't render.

### Persona weight vectors

Live in `data/personas/*.yaml`, versioned, with a written rationale for each
weight. A weight vector is an editorial judgment and is labeled `opinion` per
Constitution §3 — the *scores* are evidence; the *weights* are a point of view
about whose problem matters.

---

## 5. Stack evaluation

The Atlas's real question is rarely about one entity. It's "what should my whole
setup be?" A **stack** is a composed entity: model + harness + provider +
IDE + workflow, evaluated as a unit.

Stacks are scored on the same dimensions, plus three that only exist at the
composition level:

- **Integration friction** — how much work to make the pieces cooperate
- **Failure locality** — when it breaks, can you tell which layer broke?
- **Substitutability** — can you swap one layer without rebuilding the others?
  (This is the dimension that separates a resilient setup from a bet.)

Stack scores are **not** the mean of component scores. Composition is where
things actually fail, and cross-layer effects are the finding. A stack score
requires at least one Class D run of the assembled stack; without it, the stack
is `not_scored` and rendered as untested.

---

## 6. Scoring procedure

1. Confirm evidence exists and is admissible for the claim type behind each
   dimension (SOURCES.md §3).
2. Assign the score against the anchor, in writing, before looking at any other
   entity's score. Anchoring to peers produces a ranking, not a measurement.
3. Write the one-sentence rationale.
4. Record confidence, evidence IDs, `as_of`, and any `via` (harness/config)
   context.
5. Independent check: a second pass — human or a separate agent — re-scores from
   the same evidence without seeing the first score. Divergence of ≥2 points
   triggers re-examination and is logged.
6. Log the score with a changelog entry. Score changes are versioned; the
   history of a score is itself informative.

### Re-scoring triggers

New model or harness version · pricing change · new Class D results · sustained
contradicting field reports · benchmark saturation or contamination finding ·
scheduled cadence expiry.

Scores never silently persist past their `as_of` freshness window. They degrade
exactly like claims (METHODOLOGY.md §6).

---

## 7. Known weaknesses of this framework


- **Ordinal scores invite false precision.** Readers will treat 4 vs 3 as
  meaningful even when confidence is low. Display treatment mitigates this; it
  doesn't eliminate it.
- **Dimension independence is assumed and is not real.** Cost and autonomy
  interact; speed and quality trade off. Composites paper over this.
- **Anchors drift as the ceiling rises.** A 5 in 2026 is not a 5 in 2028. Scores
  carry `as_of` and the anchor set is versioned, but longitudinal comparison of
  raw scores is invalid and the UI must not offer it.
- **Model/harness confounding is mitigated, not solved.** We hold harness
  constant where we can; we cannot always.
- **We are one team.** D7 (developer experience) especially reflects our working
  style. It is scored from convergent Class C evidence rather than our own taste
  wherever possible, and flagged where it isn't.

---

## 8. Amendments

**v1.1 — add D13 Security posture.**
*Forced by:* the 2026-08-03 landscape scan (TAXONOMY.md §0, Finding 3).
*Rationale:* security kept appearing as a facet across four separate layers —
data handling (L2), sandboxing (L3), untrusted extensions (L5), and messaging
exposure (L4). A property that recurs across the whole stack and independently
changes adoption decisions is a dimension, not a footnote.
*Invalidates:* nothing — no entity had been scored at the time of amendment.
Applicability matrix extended in the same change, per CONSTITUTION §15.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-08-03 | Added D13 Security posture. Extended applicability matrix with orchestration, assurance, and context/memory classes surfaced by the scan. |
| 1.0 | 2026-08-03 | Initial rubric. Added D11/D12 beyond the brief's ten. No stored composites. |
