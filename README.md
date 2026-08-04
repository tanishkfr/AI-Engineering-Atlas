# AI Engineering Atlas

A research atlas for AI software engineering. Not a blog, not a benchmark
leaderboard, not a comparison article.

It exists to answer one question well:

> **What is the best AI software engineering stack for my specific situation?**

Every claim is sourced, dated, and graded. Every recommendation is scoped to who
it is for. Every gap is published rather than hidden.

---

## Status

**Milestones 1–2.5 complete — foundations, formalization, decision layer. Zero
published claims, by design.**

M1 built the research system: how evidence is graded, how claims are structured,
how the ecosystem is divided, how things are scored, how it stays current.

M2 formalized the knowledge graph and the engine, then **proved the data model
against real questions before researching anything**. No query required a
redesign of the graph; four additive extensions were surfaced by the queries and
applied.

M2.5 rebuilt the engine as a **constraint solver under uncertainty** after a
seventh query — *"how do I spend my next $25 most effectively?"* — turned out to
be inexpressible by a weighted sum.

Finding those gaps against seven questions cost a day. Finding them against five
hundred facts would have cost a migration.

See [DEPENDENCE.md](DEPENDENCE.md) for the thesis,
[QUERIES.md](QUERIES.md) for the proofs, and
[RESEARCH.md](RESEARCH.md) for the state of the corpus.

---

## What makes this different

**Source class is separated from claim type.** Vendor documentation is
authoritative about pricing and inadmissible for comparative judgment. A Reddit
thread is weak evidence for a context window and the strongest available evidence
for a silent truncation bug. Authority is the intersection of what a source *is*
and what is being *claimed* — see the matrix in [SOURCES.md](SOURCES.md) §3.

**There is no overall score.** No "87/100". A composite requires a weighting, and
a weighting encodes whose problem you are solving. Scores are stored per
dimension; composites are computed against an explicit persona weight vector,
with the weights always visible.

**Freshness is modelled, not footnoted.** Every fact carries a verification date
and a decay window. Stale facts look stale at the point of use. Expired facts do
not render as current — the page shows a gap instead.

**One fact, one place.** All facts live in structured data under `/data`. Prose
references them by ID. Tables, charts, and matrices are generated. Fixing a
number fixes it everywhere.

**Nothing is overwritten.** Facts are immutable and bitemporal: they record both
when something was true in the world and when the Atlas believed it. That makes
a price change and a correction structurally different — so the Atlas can publish
its own error rate, and can replay a past recommendation against past evidence to
check whether it held up.

**Compatibility is three-valued.** Compatible, incompatible, or *unverified*.
The absence of evidence that two tools work together is never treated as evidence
that they do.

**It's a constraint solver, not a ranker.** Recommendations come from
optimization over budgets, objectives, constraints, preferences, evidence
quality, freshness, uncertainty, opportunity cost, and compatibility. Uncertainty
propagates as belief distributions rather than being thrown away at the last
step; dominance prunes before any weight is applied, so *defensible* and
*recommended* stay separable; and the decision criterion follows the reader's risk
posture, so an enterprise team and a solo founder get different answers from
identical evidence, for a stated reason.

**It answers "what does my next dollar buy?"** — not just "what's best at $X."
The engine reports the budget frontier, its knees, and **dominated spending
ranges**. The answer to *"how should I spend my next $25?"* is
"spend $20 and hold the $5 — the $21–$44 range is dominated", not a product name.

**Every recommendation explains itself, or does not render.** Six mandatory
machine-generated components: why this won · what was assumed · what tradeoffs
were accepted · what evidence supports it · what uncertainty remains · what would
change it.

**The engine writes the research agenda.** Value-of-information ranks every
unknown by how much resolving it would change recommendations — and licenses
*not* researching the ones that change nothing.

**It runs its own research program.** Findings that generate original questions
become ranked entries in [`research/questions/`](research/questions/README.md),
scored by Expected Recommendation Impact rather than novelty. Seven of the ten
open questions **cannot be answered from any public source** — they are gaps in
the field, not gaps in our reading. Six flagship tracks produce longitudinal
first-party datasets: tokenizer normalization, throughput-constrained autonomy,
cache economics, intervention rate, harness effect size, and real-world feature
cost.

**The registers are published.** Conflicts between sources, gaps in coverage,
and corrections are generated pages, not hidden metadata.

---

## Structure

| Document | Responsibility |
|---|---|
| [CONSTITUTION.md](CONSTITUTION.md) | Non-negotiable principles. Outranks everything else. |
| [SOURCES.md](SOURCES.md) | Source quality framework and the authority matrix |
| [METHODOLOGY.md](METHODOLOGY.md) | How research is gathered, weighted, reviewed, and re-verified |
| [EVALUATION.md](EVALUATION.md) | The 13-dimension scoring rubric |
| [TAXONOMY.md](TAXONOMY.md) | How the ecosystem is divided — 9 layers, 2 meta-classes |
| [DEPENDENCE.md](DEPENDENCE.md) | **The thesis** — what holds a conclusion up, and what happens when you withdraw it |
| [GRAPH.md](GRAPH.md) | Typed relationship ontology — domains, ranges, inference rules |
| [TEMPORAL.md](TEMPORAL.md) | Bitemporal fact model — how the past is kept |
| [SCHEMA.md](SCHEMA.md) | The knowledge graph data model |
| [QUERIES.md](QUERIES.md) | Seven queries traced end to end — the model's acceptance tests |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System layers: data → research → recommendation → interface → pipeline |
| [INFORMATION-ARCHITECTURE.md](INFORMATION-ARCHITECTURE.md) | Site structure and evidence rendering |
| [RESEARCH.md](RESEARCH.md) | Live inventory, gaps, and open questions |
| [CLAUDE.md](CLAUDE.md) | How agents work in this repository |

```
data/       the source of truth — entities, claims, sources, personas
atlas/      MDX narrative that references the data
research/   working notes and scans (never citable)
scripts/    validation, computation, reports, pipeline
```

---

## The rules that constrain everything

1. Every page answers a decision, not a topic.
2. Every claim is traceable to a captured primary source.
3. Fact, interpretation, and opinion are structurally separated.
4. Benchmarks are evidence, never verdicts.
5. There is no universal "best".
6. Uncertainty is stated, never manufactured.
7. Every fact has a verification date and a decay state.
8. Every fact exists exactly once.
9. Corrections are public and versioned.
10. Coverage never exceeds the capacity to keep it true.

Full text in [CONSTITUTION.md](CONSTITUTION.md).

---

## What this will never publish

A "best AI coding tool" ranking · a single overall score · an undated
recommendation · a claim you cannot click through to a source · a comparison
table placing incomparable numbers in the same column.
