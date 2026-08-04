# PERSONAS

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Machine form:**
`data/personas/*.yaml` · **Schema:** `data/schema/persona.schema.json`

Personas here are **decision contexts**, not marketing profiles. No photos, no
names, no invented biographies. A persona is a set of constraints and priorities
precise enough that a machine can rank options with it.

---

## 1. The rule that keeps this honest

**A persona that never changes a recommendation gets deleted.**

This is enforced, not aspirational. The build computes, for every pair of
personas, whether they ever produce different rankings on any decision. Pairs
that never diverge are flagged, and one of them is merged away.

The reason: persona sections in most comparison content are decorative. Five
profiles, five headshots, and the same three tools recommended to all of them.
That is worse than having no personas, because it implies a specificity the
analysis doesn't have. If "student" and "startup CTO" always get the same answer,
then the honest page says "this answer doesn't depend on who you are" — which is
useful information, and the personas were noise.

---

## 2. What defines a persona

Four things, all of which change answers. Everything else is decoration.

| Axis | Why it changes the answer |
|---|---|
| **Hard constraints** | Eliminate candidates outright — data residency, no-training guarantees, offline operation, licence compatibility, procurement. Constraints are not preferences and never trade off against quality. |
| **Budget shape** | Not just amount. A hard ceiling behaves completely differently from a variable budget: the former favors subscriptions and local inference, the latter favors metered access with cache optimization. |
| **Task mix** | The strongest single predictor of which dimensions matter. Frontend-heavy work weights output quality and iteration speed; legacy maintenance weights context handling and output maintainability. These pull in different directions. |
| **Risk posture** | Tolerance for autonomous action, for rework, for a tool disappearing. Drives D2, D12, D13 weighting more than budget does. |

Explicitly **not** persona axes: job title, seniority, company size, or industry
— except where they imply one of the four above. "Enterprise" matters because it
implies compliance constraints and procurement, not because of headcount.

---

## 3. The initial set

Nine personas. Each entry states the constraint that makes it distinct — if that
constraint were removed, the persona would collapse into another.

| ID | Context | Distinguishing constraint |
|---|---|---|
| `per-solo-founder` | Shipping a product alone, speed over process | Wide task mix, no review partner — output must be trustworthy *unreviewed*, which weights maintainability far above where most would put it |
| `per-startup-cto` | Small team, setting standards others inherit | Optimizing for a *team's* consistency and onboarding, not personal preference; switching cost is multiplied by headcount |
| `per-student` | Learning, hard budget ceiling | Hard ceiling near zero; **learning value is a genuine objective** — a tool that produces good code while teaching nothing scores differently here than anywhere else |
| `per-designer-engineer` | Design-to-code, UI-heavy | Task mix is overwhelmingly frontend; visual fidelity and iteration speed dominate, and general coding benchmarks are near-useless as evidence |
| `per-backend-engineer` | Services, data, mature codebase | Large existing codebase — context handling and cross-file reasoning are the binding constraint, not generation quality |
| `per-legacy-maintainer` | Old, large, poorly documented systems | Comprehension over generation; low autonomy appetite; the highest bar for output maintainability in the set |
| `per-ai-researcher` | Building on models, needs control | Needs raw API access, reproducibility, and flexibility; hosted abstractions are a cost, not a benefit |
| `per-enterprise-team` | Compliance, procurement, scale | Hard constraints dominate everything — most of the candidate set is eliminated before any scoring happens |
| `per-agency` | Many client codebases, fixed-price work | Cost predictability and fast context-switching across unrelated repos; per-project isolation is a hard requirement |

Two absences are deliberate:

- **No "hobbyist" separate from student.** Their constraint profile is
  near-identical; keeping both would violate §1. Merged into `per-student` with
  the learning-value weight noted as optional.
- **No "beginner vs expert" split.** Expertise changes *how* you use a tool far
  more than *which* tool you should pick. Where it genuinely changes the answer,
  it appears as the `expertise` context field rather than as separate personas.

---

## 4. How personas are used

**In recommendations** — hard constraints eliminate, then weights rank
(EVALUATION.md §4, ARCHITECTURE.md layer 3).

**In decision pages** — the short answer is stated per-persona wherever the
answer actually differs, and stated once where it doesn't.

**In the Stack Builder** — the reader either picks a persona or answers a short
series of questions that construct one. The constructed persona is shown back to
them, editable, so they can see and change what the recommendation is assuming.

**As an audit** — a recommendation that cannot be traced to a persona's weights
is unscoped, and unscoped recommendations violate CONSTITUTION §6.

---

## 5. Honesty constraints

- **Weights are opinion**, labeled `weights_status: opinion` in the data itself,
  with a written rationale and a date. The scores are evidence; the weights are
  a point of view about whose problem matters, and the interface must never blur
  the two.
- **Personas are not evidence.** They do not make a claim stronger. A weak claim
  weighted heavily is still a weak claim, and the composite's confidence is the
  floor of its inputs.
- **Readers are not personas.** Every persona-scoped answer offers "adjust
  these assumptions." The persona is a starting point, not a diagnosis.
- **Anti-recommendations are required** where they exist. What a persona should
  *avoid* is frequently more actionable than what it should pick, and it is the
  part nobody publishes.

---

## 6. Open questions

- Should personas compose (e.g. solo founder **with** enterprise compliance)?
  Composition is more truthful and combinatorially expensive to validate.
  Deferred until real usage shows whether the fixed set is too coarse.
- How should a persona's weights be re-derived as the ecosystem changes? Weights
  set in 2026 encode 2026 tradeoffs. Annual review is scheduled; the mechanism
  for revising them without invalidating historical recommendations is unsolved.
- Does `per-student`'s learning-value objective belong in the rubric as a
  dimension rather than a weight? It is currently the only persona-specific
  objective in the set, which is a smell.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial set of nine. Added the divergence rule; merged hobbyist into student; rejected a beginner/expert split. |
