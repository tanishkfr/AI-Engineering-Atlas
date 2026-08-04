# NOW

**Updated:** 2026-08-04 · The only file you need open. No history, no philosophy.

> **North star:** *"I'm a UI/UX designer with $25/month. What should I actually
> do tomorrow?"*
> Everything in this repo either serves that sentence or is overhead.
> Today the Atlas cannot answer it. That is the whole problem.

---

## Current Priority

**Synthesize Harvest 003.** ~300KB of primary community records sit in
`research/evidence/raw/` un-analysed. Clustering them into convergent behaviours
is the first real chance to move a dimension out of `not_scored`.

## Current Blocker

**Nothing is enforced.** ~25 validation rules in SCHEMA §11 are specified as
"the build fails" and there is no build. No validator has run. Confidence and
freshness are specified as computed and have never been computed.

## Current Milestone

Track A + Track B autonomous operation. No milestone prompt pending.

## Current Active RQ

**RQ-05 — Harness Effect Study.** Status: ⏸ **planned, gate shut.**
Gate opens on two consecutive *clean* harvests yielding little. The two nulls so
far were a protocol error and a tooling gap — broken instrument, not diminishing
returns.

## Current Coverage

```
Decision Coverage     8 / 50
Reference Coverage    26 entities · 3 gold-standard
Evidence Coverage     1 Class B · 0 Class C admitted · 0 / 13 dimensions scored
```

## Next Three Actions

1. **Synthesize the harvest** — cluster by behaviour, apply the ≥3-independent
   bar, record `population_gap: reddit_unavailable` on everything.
2. **Build the validator** — turn SCHEMA §11 from prose into a script that fails.
   Highest-leverage engineering task in the repo.
3. **Resolve RQ-17** — is vendor top-model access restricted through third-party
   harnesses? Class A, cheap, and a live delta for the lock-in question.

## Known Risks

- **Self-grading.** Every gate in the framework is administered by the same
  operator who wrote it. Inter-rater reliability is specified everywhere and has
  never once been run.
- **Vendor skew.** The corpus over-represents whoever documents most thoroughly,
  not whoever is best.
- **Decaying sources.** No hashes, no archives. Cited pages can change silently
  and we would not know.
- **Untested machinery.** The decision engine has never produced a single output.

## Decision Needed From User

1. **Reddit OAuth credentials** — blocks the highest-volume Class C source.
   Requires registering an application; cannot be resolved from inside the
   pipeline.
2. **Is `git init` wanted?** Still not a repository. Versioned corrections and
   public changelogs are load-bearing in the constitution and currently
   unenforceable without it.
