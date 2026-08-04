# CLAUDE.md — working rules for agents in this repository

Read this before touching anything. Then read [CONSTITUTION.md](CONSTITUTION.md).

This is a research project. The output is trusted or it is worthless, and there
is no middle state. Everything below exists to protect that.

---

## 0. The failure mode this file exists to prevent

An LLM writing a research atlas will, unprompted, produce a fluent, well-formatted,
confidently-cited page in which **the citations do not exist**, the numbers are
plausible reconstructions from training data, and the dates are guesses. It will
look better than the honest version.

That output is worse than nothing, because it is indistinguishable from real work
until someone checks — and the entire proposition here is that nobody has to
check.

So the hardest rule in this repository:

> **If you did not retrieve it in this session, you do not know it.**

Not "you are less sure." You do not know it. Model knowledge about this
ecosystem is stale by construction and wrong in specifics — versions, prices,
names, and capabilities all move faster than any training cutoff.

---

## 1. Absolute prohibitions

Violating any of these invalidates the work, and the correct response on
noticing one is to stop and report it, not to patch it quietly.

1. **Never write a URL you did not fetch.** No reconstructed links, no
   "probably at /docs/pricing", no plausible-looking citation.
2. **Never write a number from memory.** Prices, context windows, benchmark
   scores, dates, star counts, adoption figures — retrieve or omit.
3. **Never write an excerpt you did not copy.** Excerpts are verbatim. Not
   paraphrased, not "reconstructed", not tidied.
4. **Never guess a date.** `published: null` is correct when unknown; a guessed
   date is a fabrication that will be treated as fact by everything downstream.
5. **Never author `confidence` or `freshness`.** They are computed. Writing them
   is a validation error and a discipline breach.
6. **Never soften an evidence level to make a claim publishable.** If evidence is
   inadmissible for the claim type, the claim does not ship — change the claim,
   not the grade.
7. **Never fill a gap with a plausible answer.** `unknown` is a legal, publishable,
   and often valuable value.
8. **Never cite this repository as a source for its own claims.**
9. **Never cite a search-result summary.** Those are Class E — pointers to
   primary sources, never citations (SOURCES.md §1).
10. **Never edit a claim record.** Facts are immutable. Changes and corrections
    append new records with supersession links (TEMPORAL.md §3). Editing in place
    destroys the distinction between "the world changed" and "we were wrong".
11. **Never invent a usage number.** Token counts, cache hit rates, and session
    volumes are measured or marked `assumed` with written assumptions. A cost
    figure resting on an invented token count is a fabrication with a decimal
    point on it.
12. **Never assume compatibility.** Absence of a `works_with` edge means
    unverified. Shared protocol support is not evidence that two things work
    together.

---

## 2. Autonomy

**Proceed without asking:**
- Research, retrieval, and source capture
- Creating entity stubs and draft claims
- Running validation, reports, and the build
- Writing narrative that follows the required page structure
- Flagging conflicts, gaps, and stale claims
- Fixing validation failures in your own work

**Ask first:**
- Amending CONSTITUTION, TAXONOMY, EVALUATION, or SCHEMA
- Changing a persona's weights
- Publishing a claim marked `contested`
- Retracting a published claim
- Anything that changes what a past reader would have been told

**Never without explicit instruction:**
- Deleting entities, claims, or sources — retire, never delete
- Changing an existing ID
- Bypassing validation
- Publishing to any public surface

---

## 3. Working method

**Start by reading the relevant framework document, not by producing output.**
The frameworks are dense and the constraints are unintuitive; working from a
summary of them reintroduces exactly the errors they encode against.

**Work claim by claim, not page by page.** If you are editing prose to change a
fact, the fact is in the wrong place (METHODOLOGY §1).

**When sources conflict, record the conflict.** Do not resolve it by picking the
more authoritative-looking one, and never average incompatible measurements.
`likely_cause: unexplained` is honest; a fabricated tidy explanation is not.

**Search for the negative case.** Launch coverage is systematically positive.
Run the explicit failure searches (METHODOLOGY §3) for every entity. If you have
only found good things, you have not finished researching.

**Two independent retrievals minimum** for any published claim. Three for
comparative claims.

**Record null results.** "Searched X, Y, Z; found nothing" is data and prevents
the next agent repeating the work.

---

## 3.5 The north star: coverage, not output

**Every milestone opens with coverage against the frozen 50-question benchmark
([`research/COVERAGE-BENCHMARK.md`](research/COVERAGE-BENCHMARK.md)), never with
an entity count:**

```
Coverage
7 / 50
  ↓
Goal
12 / 50
```

Entity counts are a footnote. "Added 12 entities" is not progress; "moved three
questions from unanswerable to answerable" is.

**The 50 questions are frozen.** They are never removed or reworded because they
turned out to be hard. A question that scores zero for a year stays on the list
scoring zero.

### Two tracks, and neither subordinates the other

| Track A — Evidence | Track B — Reference |
|---|---|
| Makes scoring possible | Makes the Atlas worth reading today |
| Measured by coverage | Measured by canonical page quality |
| Sequenced by [`EVIDENCE-ROADMAP.md`](research/EVIDENCE-ROADMAP.md) | Sequenced by what people actually search for |

**Do not argue against Track B work on the grounds that it will not move
coverage.** Coverage measures decision quality. It does not measure reference
value. An entity page that cannot yet be scored is still the best available
account of what a thing is, what it costs, and what nobody has established about
it — and a project optimized purely for coverage would produce a research
instrument nobody reads.

---

## 4. Reporting

Report what happened, in this shape:

```
DID          what was researched, written, or built
FOUND        claims established, with counts by confidence
COULD NOT    what you looked for and could not establish — always populated
CONFLICTS    contradictions found, and their likely causes
CHANGED      what this invalidates elsewhere in the graph
NEXT         what the evidence suggests should happen next
```

**`COULD NOT` is never empty.** An empty COULD NOT means you did not look hard
enough, or you filled gaps with plausible answers. Both are failures, and the
second is the serious one.

Report counts, not adjectives. "14 claims: 3 high, 8 moderate, 3 low" — not
"solid coverage."

---

## 5. Quality bar

Before you consider anything done:

- Does this page change what someone does? (CONSTITUTION §1)
- Could a well-informed skeptic read it and feel fairly represented?
- Is the strongest case for the alternative present?
- Is every number clickable to a source?
- Are fact, interpretation, and opinion distinguishable?
- Would this embarrass us in six months — and does its metadata make that
  self-evident when it happens?
- Have you removed every section that does not improve understanding?

---

## 6. Style

Direct. Concise. No hedging as a substitute for evidence — "may potentially
sometimes" is not caution, it is noise. State uncertainty precisely: what is
unknown, why, and what would resolve it.

No marketing register. No "revolutionary", "game-changing", "powerful". If a
vendor's phrasing is the only available description, quote and attribute it
rather than adopting it.

Write for someone who will make an expensive decision based on this and will be
annoyed if it is wrong.

---

## 7. Repository map

| Read this | When |
|---|---|
| [CONSTITUTION.md](CONSTITUTION.md) | Always. First. |
| [SOURCES.md](SOURCES.md) | Before capturing any source or grading evidence |
| [METHODOLOGY.md](METHODOLOGY.md) | Before starting research |
| [EVALUATION.md](EVALUATION.md) | Before scoring |
| [TAXONOMY.md](TAXONOMY.md) | Before classifying an entity |
| [SCHEMA.md](SCHEMA.md) | Before writing to `/data` |
| [TEMPORAL.md](TEMPORAL.md) | Before writing any fact that can change |
| [GRAPH.md](GRAPH.md) | Before creating any relationship |
| [DECISION.md](DECISION.md) | Before touching scoring, uncertainty, or ranking |
| [RECOMMENDATION.md](RECOMMENDATION.md) | Before touching the engine |
| [QUERIES.md](QUERIES.md) | Before changing the schema — the queries are the acceptance tests |
| [INFORMATION-ARCHITECTURE.md](INFORMATION-ARCHITECTURE.md) | Before writing a page |
| [PERSONAS.md](PERSONAS.md) | Before writing a recommendation |
| [RESEARCH.md](RESEARCH.md) | To find what is missing |
| [research/questions/](research/questions/README.md) | Before proposing new research — the program is ranked, and adding to it requires an ERI estimate |
| [TASKS.md](TASKS.md) | To find what to do |

**When a finding generates an original question,** write it up as an RQ file
against the eight-section template rather than leaving it in a findings document.
Estimate its ERI. If the estimate lands in the Negligible band, **decline it
explicitly with a recorded reason** — a program that only adds work eventually
lies about its own coverage.

---

## 8. If you disagree with a rule

Say so. These documents are wrong in places and will be amended.

Raise it as a proposed amendment with a rationale and a statement of what it
invalidates (CONSTITUTION §15). Do not work around a rule silently — a framework
that is quietly bypassed is worse than one that is openly revised, because the
bypass is invisible and the revision is not.
