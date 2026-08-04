# CONSTITUTION

**Status:** ratified v1.0 · **Last reviewed:** 2026-08-03 · **Amendment process:** §15

This document defines the non-negotiable principles of the AI Engineering Atlas.
It outranks every other document in this repository. Where METHODOLOGY.md,
EVALUATION.md, SCHEMA.md, or any page contradicts this file, this file wins and
the other document is the bug.

These are constraints, not aspirations. A page that violates a principle here is
not "a page that needs improvement" — it is a page that must not ship.

---

## 1. The Atlas answers decisions, not topics

Every page exists to help someone choose. If a page does not change what a
reader does on Monday morning, it does not belong in the Atlas.

- Pages are titled as questions, because pages answer questions.
- A page with no decision behind it is an encyclopedia entry. We are not an
  encyclopedia. Wikipedia is better at that than we will ever be.
- The test: *what decision does a reader make differently after reading this?*
  If the answer is "none", delete the page.

## 2. Every claim is traceable

No fact enters the Atlas without a source, an evidence level, and a date.

- A claim with no source is not a weak claim. It is not a claim at all, and it
  does not render.
- "Everyone knows" is not a source. Neither is a previous version of this Atlas
  citing itself, nor a model's training data.
- Sources are archived at capture time (§SOURCES.md). The web rots. A citation
  that 404s in eighteen months is a citation we no longer have.
- Traceability is enforced mechanically, not socially. The build fails on an
  unsourced claim.

## 3. Facts, interpretations, and opinions are structurally separated

Three different things wear the same clothes in most AI writing. Here they do
not.

- **Fact** — verifiable against a primary source. "Model X costs $Y per million
  input tokens." Has a source and a verified date.
- **Interpretation** — a reading of evidence that a reasonable analyst could
  dispute. "The pricing change suggests they are optimizing for agentic
  workloads." Has evidence behind it and is labeled as inference.
- **Opinion** — the Atlas's editorial judgment. "We would not build a production
  agent on this." Labeled, attributed, dated, and never dressed as a finding.

The reader must never have to guess which of the three they are reading. This is
a rendering requirement, not a writing-style suggestion: the three types have
distinct visual treatments in the interface.

## 4. Benchmarks are evidence, never verdicts

A benchmark score is a measurement of a benchmark, not of usefulness.

- No page ranks anything by benchmark score alone.
- Every benchmark reference states what the benchmark actually measures, its
  known failure modes, contamination risk, and who ran it.
- Self-reported scores are labeled as self-reported, always, without exception,
  including when the reporter is a company we like.
- When a benchmark and sustained real-world usage disagree, we report the
  disagreement. We do not silently pick the flattering one.
- Leaderboard position is not a finding. *Why* a model is positioned there, and
  whether that generalizes to the reader's work, is the finding.

## 5. Real-world usefulness outranks measured performance

The Atlas optimizes for the question "will this work for me, in my codebase, at
my budget, on Tuesday". Weighted always: quality, autonomy, engineering output,
reliability, maintainability, cost, developer experience, speed, flexibility,
ecosystem maturity. No single axis is permitted to dominate a recommendation.

## 6. There is no universal "best"

Every recommendation is conditional. Conditions are stated explicitly.

- Recommendations are scoped to a persona, a budget, a task class, and a date.
- "Best coding model" is a question the Atlas refuses to answer in that form,
  and explains why refusing is the honest response.
- Where the honest answer is "it depends", the Atlas states *what* it depends
  on and how to tell which case you are in. "It depends" without decomposition
  is a failure, not humility.

## 7. Uncertainty is stated, never manufactured

- When evidence is thin, the page says the evidence is thin.
- When sources conflict, the page shows the conflict and explains the likely
  cause. It does not average them into a false consensus.
- When nobody knows, the page says nobody knows. This is a valid and valuable
  page state.
- Confidence ratings are honest. A "high confidence" label on a
  single-community-anecdote claim corrupts every other confidence label in the
  Atlas.
- We never round uncertainty toward whichever answer makes a better page.

## 8. Freshness is a property of every fact, not a footer on every page

This ecosystem invalidates itself on a scale of weeks. An atlas that does not
model decay is a fossil that thinks it is alive.

- Every fact carries `last_verified` and a `review_cadence`.
- Every fact has a computed freshness state: **fresh · aging · stale ·
  expired**.
- Stale and expired facts are visibly marked *in the interface*, at the point of
  use, not hidden in metadata.
- An expired fact is never presented as current. It degrades to "as of
  [date]" or is withheld.
- We would rather show a gap than a confident lie about last quarter.

## 9. Single source of truth

Every fact exists exactly once, in structured data under `/data`.

- Narrative references facts by ID. Narrative never restates them.
- If a number appears in prose, it was interpolated from the graph at build
  time, or it is a bug.
- Comparison tables, pricing tables, capability matrices, and timelines are
  generated, never authored.
- Corollary: fixing a fact in one place fixes it everywhere, and this is the
  only reason the Atlas is maintainable at all.

## 10. The database is the product; the website is a view

Layer order, permanently: **data → research engine → recommendation engine →
interface**. Each layer may depend only on layers above it.

- No knowledge lives only in the UI.
- No presentation concern is allowed to shape the schema.
- If the website were deleted, the Atlas would still exist and still be
  valuable. If `/data` were deleted, nothing would remain.

## 11. Corrections are public and versioned

- Facts are versioned. Changes append to a changelog with a reason.
- Corrections are surfaced, not silently patched. A reader who acted on an old
  claim deserves to know it changed.
- Being wrong is acceptable and expected. Hiding that we were wrong is not.
- Retracted claims stay in the graph as retracted, with the retraction reason.

## 12. Independence

- No affiliate links, no sponsored placement, no paid inclusion, ever.
- Vendor relationships, if any ever exist, are disclosed on every affected page.
- We do not soften findings for access.
- Free credits, early access, and preview programs are disclosed as potential
  bias on any claim they touch.

## 13. First-party experiments must be reproducible

- Every experiment ships its prompts, harness config, model versions, seeds,
  timestamps, raw outputs, and cost accounting.
- An experiment that cannot be re-run by a stranger is an anecdote. Anecdotes
  are Level C evidence at best, and are labeled as such.
- Negative and inconclusive results are published. Suppressing them makes the
  dataset a marketing document.
- Experiments are versioned so re-runs against future models are comparable.

## 14. Maintainability is a hard constraint on scope

- We do not add a fact we have no plan to re-verify.
- We do not add a page we have no plan to review.
- Coverage that cannot be sustained is worse than an acknowledged gap, because
  it decays silently into misinformation while looking authoritative.
- Known gaps are documented in `RESEARCH.md` as first-class content. A visible
  gap is honest; an invisible one is a trap.

## 15. Amendment

This document changes by explicit amendment only.

1. Proposed change is written as a diff with a rationale.
2. The rationale states which existing pages or data the change invalidates.
3. On acceptance, the version increments and the change is logged below.
4. Downstream documents are reconciled in the same change. A constitution
   amendment that leaves METHODOLOGY.md contradicting it is incomplete.

Principles may be added, sharpened, or retired. They may not be quietly
loosened to accommodate work that already violates them — that is the one edit
this process exists to prevent.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial ratification. |
