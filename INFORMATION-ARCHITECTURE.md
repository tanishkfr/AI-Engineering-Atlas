# INFORMATION ARCHITECTURE

**Status:** v1.0 · **Last reviewed:** 2026-08-03 · **Implements:**
[CONSTITUTION.md](CONSTITUTION.md) §1, §3, §8

How the Atlas is organized for a reader. Structure follows decisions, not
categories — the taxonomy organizes the *data*, and it is the wrong shape for
navigation.

---

## 1. The organizing principle

A reader arrives with a question, not a category. Three entry paths, and no
hierarchy above them:

```
   ASK              BROWSE            BUILD
   question index   by stack layer    stack builder
   "what should     "what exists      "given my
    I do about…"     in L3?"           situation…"
```

Nobody arrives wanting to browse a taxonomy. Browse exists for the reader who
already knows the shape of the problem; **Ask is the front door**, and the
question index is the most important page on the site.

---

## 2. Page types

Nine. Anything that doesn't fit one is probably filler (CONSTITUTION §1).

### 2.1 Decision page — *the primary unit*

Titled as the question. `atlas/decisions/<slug>.mdx`

Fixed structure, because a consistent shape is what makes the Atlas scannable
across hundreds of pages:

```
  THE QUESTION            stated precisely, with what it depends on
  THE SHORT ANSWER        conditional, per-persona, ≤ 5 lines
  WHY                     evidence, with confidence and dates inline
  WHEN THIS IS WRONG      the conditions under which the answer flips
  THE STRONGEST COUNTER   steelman of the alternative
  WHAT WE DON'T KNOW      gaps, explicitly
  HOW WE'D CHECK          what evidence would change this
  SOURCES                 every source, with excerpts
```

`WHEN THIS IS WRONG` and `WHAT WE DON'T KNOW` are **mandatory sections**. A
decision page without them is a recommendation pretending to be an analysis.

### 2.2 Entity page

*"When should I use X?"* — never *"X"*. `atlas/entities/<layer>/<slug>.mdx`

Header block generated from the graph: what it is, layer/roles, who makes it,
status, last verified, freshness state. Then: what problem it solves · what it
replaces · dimension scores with confidence · costs · known failure modes ·
relationships · the decision pages it appears in · open questions.

The failure-modes section is generated from X-type claims, which is why Class C
evidence is worth the methodological trouble — no other source produces it.

### 2.3 Comparison page

Generated table + authored narrative. The table is never hand-written.

Hard rule: **incomparable numbers are never placed in the same column.**
Different-harness benchmark results render in separate columns with an explicit
warning, or not at all. The scan found six mutually incomparable SWE-bench
figures circulating as if they were one ranking; refusing to reproduce that is a
core function of this site.

### 2.4 Stack page

A complete working setup for a situation, with total cost, tradeoffs, what it
optimizes for, what it sacrifices, and — required — a **switching-cost note**:
what it costs to leave.

Rendered from the engine's output object, which means every stack page carries
the six explanation components, its P(best) or regret bound, its assumed usage
profile, and its sensitivity margins. **The recommendation is the unit; the page
is its presentation.** A stack page that cannot show what would change its mind
is not rendering an incomplete recommendation — it is rendering an invalid one.

### 2.4b Budget page

Answers *"what does my next dollar buy?"* rather than *"what's best at $X."*
Renders the budget frontier with its knees and **dominated spending ranges**
marked. The headline is an instruction — *spend $20, hold the $5, the next real
step is $45* — not a product.

### 2.5 Concept / practice page

*"What is context engineering, and does it change what I should do?"* Practices
and anti-patterns are entities and get real pages with real evidence.

### 2.6 Evidence page

*"What does SWE-bench actually measure?"* One per benchmark, survey, or dataset.
Mandatory sections: what it measures · **what it is routinely misread as
measuring** · harness dependency · contamination risk · saturation state · who
publishes results and with what interest.

These pages exist so that every score elsewhere on the site can link to an honest
account of its own instrument.

### 2.7 Economics page

Cost per unit of work, subscription vs API, cache economics, budget-tier stacks,
hidden costs (review time, retries, failed runs). Every figure carries its
pricing snapshot date.

### 2.8 Register pages — *the meta layer*

Generated, and unusual enough to be the site's signature:

| Register | Shows |
|---|---|
| **Conflict register** | Every place our sources disagree, and why |
| **Gap register** | Every `unknown` claim and `not_scored` dimension |
| **Freshness dashboard** | What is current, what is decaying, what expired |
| **Changelog** | What changed each month, what it invalidated, what we got wrong |
| **Corrections** | Retracted claims, with reasons |
| **Research agenda** | Unknowns ranked by value of information — what we're researching next and why, including what we've decided *not* to research |

Most research sites hide these. Publishing them is the clearest available signal
that the methodology is real, and they are genuinely useful: the gap register is
a research agenda, and the conflict register is often where the interesting
questions are.

### 2.9 Experiment page

One per Class D experiment: preregistration, method, raw results, cost
accounting, failures, and what it did *not* establish.

---

## 3. The question index

The front door. A searchable, filterable list of every question the Atlas
answers, each with its current answer state:

`answered` · `contested` · `unknown` · `stale`

A question with no good answer is still listed. **The list of questions we
cannot answer is part of the map** — arguably the most honest part.

Seed questions, drawn from the landscape scan and grouped by decision. These
drive Milestone 2 research priority:

**Getting started**
- What should I use if I'm starting from zero today?
- Subscription or API credits — which for my usage?
- Do I need an AI editor, or is a terminal agent enough?

**Model choice**
- Which model for which kind of task?
- When is an open-weight model actually good enough?
- Does the model matter as much as the harness?

**Cost**
- What does a month of real agentic development actually cost?
- Where does caching change the answer?
- What is the cheapest setup that still does autonomous work?
- What is the *hidden* cost — review time, retries, rework?

**Autonomy**
- How far can an agent get unsupervised on real work?
- What actually breaks on long-horizon tasks?
- Is parallel multi-agent work worth its coordination cost?

**Quality and risk**
- Does AI-assisted code hold up over six months?
- If review time now exceeds writing time, what reduces it?
- What is the realistic security exposure of an agent with system access?
- Which third-party extensions can be trusted, and how would you know?

**Context**
- Index-first or agentic search for a large repository?
- Does a memory layer earn its complexity?
- What belongs in a repo instruction file?

**Ecosystem bets**
- Which protocols and standards are safe to build on?
- Which tools are at risk of disappearing or being absorbed?
- What is hype and what is durable adoption?

**Meta**
- Does any of this actually make teams faster?
  *(Answer state: `contested`. Adoption is near-universal; measured productivity
  effects and self-reported trust point in different directions. This may be the
  most important page on the site, and it will not have a clean answer.)*

---

## 4. Evidence rendering

The visual system carries the epistemics. Getting this wrong makes every
principle in the Constitution decorative.

**Three assertion types, three treatments.** Fact, interpretation, opinion must
be distinguishable at a glance and without reading the label. Opinion is
attributed and dated in the flow of text, not in a footer.

**Confidence is visible on the claim.** Not a page-level badge — page-level
confidence is meaningless when a page contains fifty claims of varying strength.

**Freshness at the point of use.** An aging number shows its date. A stale one
shows an explicit "as of" treatment. An expired one does not render as current;
the page shows a gap and says what is missing.

**Every number is a link** to its source and excerpt. One click, no exceptions.

**Self-reported measurements are marked persistently** — the marker travels with
the number into every table and chart it appears in.

**Weights next to rankings, always.**

The design failure to avoid: an interface so clean that a `low`-confidence,
six-month-old, self-reported number looks exactly like a fresh, corroborated,
independently-measured one. Visual polish that flattens epistemic difference is
worse than no polish.

---

## 5. Search and filter

**Search-first.** Keyboard-driven, immediate, over entities, aliases, claims,
questions, and narrative. Aliases matter: readers will search the old name.

**Filter-first for browse.** Facets from the taxonomy — layer, role, openness,
delivery, price band, self-hostable, licence, data policy — plus filters no
comparison site offers: **evidence strength**, **freshness**, and
**confidence**. "Show me only what we're confident about and verified this
month" is a legitimate and useful query.

**Compare from anywhere.** Any two entities of compatible role, side by side,
generated.

---

## 6. Navigation

Flat and shallow. Two levels maximum before content.

```
  /                     Ask — question index, search
  /decisions/…          decision pages
  /entities/<layer>/…   browse by stack layer
  /stacks/…             complete setups
  /personas/…           by situation
  /economics/…          cost analysis
  /evidence/…           benchmarks, surveys, experiments
  /registers/…          conflicts, gaps, freshness, changelog, corrections
  /method/…             constitution, methodology, sources, evaluation, taxonomy
```

`/method/` is public and prominent. The methodology is not back-matter — it is
the reason to believe anything else on the site, and it should be reachable from
every page that makes a claim.

---

## 7. What this site will not have

- A "best AI coding tool" ranking
- A single overall score per tool
- Undated recommendations
- A tool list without decisions attached
- Pages that exist for search coverage
- Any claim you cannot click through to a source

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-08-03 | Initial IA. Question index as front door; registers as first-class pages. |
