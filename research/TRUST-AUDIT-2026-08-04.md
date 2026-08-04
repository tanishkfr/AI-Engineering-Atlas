# TRUST AUDIT — why an expert would not trust the Atlas today

> **STATUS UPDATE 2026-08-04 (post vertical slice + provenance backfill)**
>
> | # | Item | Status |
> |---|---|---|
> | 1 | Engine never produced a recommendation | ⚠️ **Partial** — runs end-to-end, emits full explanation, but correctly *refuses* at 1/13 coverage |
> | 2 | "Build fails" rules are fiction | ✅ **Substantially resolved** — validator runs, exits non-zero, found 6 real errors; ~14 of ~25 rules implemented |
> | 3 | Every gate self-administered | ❌ **Unchanged** |
> | 4 | Sources unhashed and unarchived | ✅ **RESOLVED** — 15/15 sources carry a real SHA-256 of the raw body and a Wayback URL; `reverification: hash_triggered` |
> | 5 | Corpus tiny and vendor-skewed | ❌ **Unchanged** |
>
> Two resolved, one partial, two untouched. Detail in
> `research/VERTICAL-SLICE-REPORT.md`.

---


**Date:** 2026-08-04 · **Framing:** if this launched publicly tomorrow, what
would a hostile, competent reviewer attack first?

Ranked by severity. Severity = how much it undermines the project's *central
claim* — that its recommendations are trustworthy — not how hard it is to fix.

---

## 1. The recommendation engine has never produced a recommendation

**Severity: critical.**

The Atlas presents itself as a decision system. Thirteen dimensions, belief
distributions, dominance pruning, minimax regret, persona weight vectors,
budget-frontier knees, a mandatory six-part explanation object, twelve enforced
invariants.

**None of it has ever run.** Zero dimensions are scored, so no composite has ever
been computed, so no stack has ever been ranked, so no explanation has ever been
generated. The seven query proofs in QUERIES.md are traced *by hand* against an
empty graph.

A reviewer's line: *"You have specified a decision engine in extraordinary
detail and never once demonstrated it produces a defensible answer. Untested
machinery is broken machinery. How do you know minimax regret over ordinal
beliefs even produces sensible output?"*

We do not know. The honest answer is that the engine is a design, not a system.

**Fix:** score one dimension on one entity family end-to-end, even provisionally,
and publish the full output including the explanation object. One worked example
would convert this from "unproven" to "demonstrated at small scale."

---

## 2. Every "the build fails" rule is currently fiction

**Severity: critical.**

SCHEMA §11 lists roughly twenty-five validation rules as hard errors: no
Class-E-only claims, no authored confidence, comparative claims need two
independent sources, no orphan numbers in prose, domain/range conformance,
acyclicity, no vendor names in engine code.

**There is no build. No validator has ever run.** Claims are marked `published`
by hand. `confidence` and `freshness` are specified as computed and have never
been computed — every confidence value in the corpus was, in practice, decided
by a human despite a rule forbidding exactly that.

A reviewer's line: *"Your integrity guarantees are prose. Show me the CI run."*

This is more damaging than a missing feature, because the documents assert
enforcement in the present tense. That is closer to a false statement about the
system than a gap in it.

**Fix:** build the validator before adding one more entity. It is the
highest-leverage engineering task in the repository and it is not large.

---

## 3. Every gate is self-administered by the person who wrote it

**Severity: high.**

The framework specifies inter-rater reliability gates for intervention
classification and rubric scoring, second-pass independent re-scoring with a
divergence threshold, blind evaluation, and preregistration.

**Inter-rater reliability has never been run. Not once.** Every evidence-class
assignment, ERI estimate, belief-distribution heuristic, persona weight, and
convergence judgement comes from a single operator who also authored the rules
those judgements are graded against.

The self-catches are real and documented — a discarded sample, a demoted flagship,
a corrected over-broad claim, a refused gate opening. But a reviewer will
correctly note that **self-catching is not independent verification**, and that
the cases we caught are by definition the ones we were capable of seeing.

A reviewer's line: *"Every check in this system is graded by its author. What
would a check that you are systematically blind to look like?"*

**Fix:** cannot be fully resolved alone. Partial mitigations: publish the
belief-distribution heuristics and rubrics for external attack; recruit one
second rater for a single sample; make the corpus contributable.

---

## 4. No source is hashed or archived — the evidence base is unverifiable and decaying

**Severity: high.**

Every claim cites a live URL. `content_hash` is `null` across the entire corpus.
No source is archived.

Consequences: a reader cannot verify that our quoted excerpt matches what the
page said. We cannot detect silent vendor edits — and vendor pricing pages are
edited in place without notice, which is precisely the failure the hash rule was
written to catch. Every pricing claim in the corpus is one silent edit away from
being wrong with no signal.

A reviewer's line: *"Your entire proposition is traceability. Your citations
point at mutable pages you did not preserve."*

Sharpened by the fact that we **documented** this gap honestly in M3 and then
kept collecting for four more milestones without closing it.

**Fix:** raw-body fetch, SHA-256, archive snapshot. Specified as T-002 since M3.
Not hard. Not done.

---

## 5. The corpus is tiny and systematically vendor-skewed

**Severity: moderate–high.**

26 entities, ~64 claims. A large majority of published claims trace to **one
vendor's documentation**, because that vendor documents most thoroughly and its
pages extract cleanly.

That is a selection effect masquerading as coverage. The Atlas's picture of the
ecosystem is shaped by whose documentation is easiest to read, not by who matters
or who is good. OpenAI and Google claims sit at `draft` because their pages
resisted verbatim capture — so the corpus is *most confident about the vendor
that writes the best docs.*

A reviewer's line: *"Your evidence density correlates with documentation quality,
not with importance. That is a bias, and you have a framework that claims to
correct for bias."*

**Fix:** deliberately quota capture across vendors rather than following the path
of least resistance, and report per-vendor claim counts as a standing bias
metric.

---

## Did not make the top five, and would still land

- **n=1 corpora.** The tokenizer study's 1.33× headline rests on one sample per
  content stratum. Already corrected once; still thin.
- **ERI numbers look quantitative and are guesses.** breadth × flip × magnitude
  is stated as computed; two of three terms are judgement.
- **The 50-question benchmark is self-authored.** We chose the exam.
- **No external contribution has ever been tested.** The contribution process is
  designed and unexercised.
- **`git init` has never been run.** Versioned corrections and public changelogs
  are constitutionally load-bearing and currently impossible.

---

## The pattern underneath

Four of the top five are the same failure in different clothes: **the Atlas has
specified far more than it has built or verified.**

The frameworks are, I think, genuinely good. But the ratio of specification to
demonstration is roughly ten to one, and an expert reviewer will find that ratio
much faster than they will find any individual error — because the documents are
written in the present tense about things that do not yet happen.

**The single most credibility-restoring action is not more research.** It is
making a small part of the system actually run end-to-end: validator, one scored
dimension, one generated recommendation, one hashed source. Small, unglamorous,
and it converts the project from a design document into a system.
