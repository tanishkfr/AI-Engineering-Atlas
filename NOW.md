# NOW

**Updated:** 2026-08-04 · The only file you need open. No history, no philosophy.

> **North star:** *"I'm a UI/UX designer with $25/month. What should I actually
> do tomorrow?"*
> Everything in this repo either serves that sentence or is overhead.
> Today the Atlas cannot answer it. That is the whole problem.

---

## Current Priority

**Two tracks, in parallel. Neither waits for the other.**

| Track A — Reference | Track B — Evidence |
|---|---|
| Qwen 3.8, Kimi K3, DeepSeek, Cursor, OpenCode, Hermes | 1. Measure one real usage profile |
| Canonical pages, 17-section standard | 2. Score D7 from harvested community records |
| Ships value before the engine matures | 3. Score a third evidence-backed dimension |
|  | 4. Resolve RQ-17 |

**Decision pages are gated on ≥3 genuinely scored dimensions.** No public launch
date. Optimize for the first release being something an expert respects.

## Current Blocker

**Every dollar figure rests on an invented usage profile.** The engine computes
$57.00/mo for Sonnet 5 from a token count with no measurement behind it. It is
labelled `assumed` and floors confidence to `low` — but labelling a fabrication
does not make it a measurement.

## Current Milestone

Track A + Track B autonomous operation. No milestone prompt pending.

## Current Active RQ

**RQ-05 — Harness Effect Study.** Status: ⏸ **planned, gate shut.**
Gate opens on two consecutive *clean* harvests yielding little. The two nulls so
far were a protocol error and a tooling gap — broken instrument, not diminishing
returns.

## Current Coverage

```
Decision Coverage     8 / 50   (engine executable; refuses at 1/13 dims)
Reference Coverage    26 entities · 3 gold-standard
Evidence Coverage     1 Class B · 0 Class C admitted · 1 / 13 dimensions scored
Executable            validator ✅ · capture ✅ · engine ✅ · delta ✅
```

## Next Three Actions

1. **Backfill capture** — run `scripts/atlas/capture.py` over the other 14
   sources. The tool works; the chore is unfinished.
2. **Synthesize the harvest** — cluster by behaviour, apply the ≥3-independent
   bar, record `population_gap: reddit_unavailable` on everything.
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
- **Untested machinery above one dimension.** The engine runs, but belief
  distributions, dominance pruning, regret, and the budget frontier are
  unexercised — they need ≥4 scored dimensions to mean anything.
- **Never edit UTF-8 data files with PowerShell 5.1 text cmdlets.** They decode
  as ANSI and write BOMs. Corrupted four schemas today. Use Python or the
  editor tooling.

## Decision Needed From User

1. **Reddit OAuth credentials** — blocks the highest-volume Class C source.
   Requires registering an application; cannot be resolved from inside the
   pipeline.
2. ~~git init~~ — **done.** Four commits; methodology, schema, and engine
   changes versioned independently.
