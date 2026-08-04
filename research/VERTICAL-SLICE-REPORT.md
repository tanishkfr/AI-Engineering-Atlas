# VERTICAL SLICE REPORT

**Date:** 2026-08-04 · **Commits:** `bdafa62` → `06ffdff` → `d5a0a81`
**Objective:** prove the architecture runs. Not that it recommends well.

---

## 1. What actually worked

**All six required components execute.**

| Component | Status | Evidence |
|---|---|---|
| Working validator | ✅ | `scripts/atlas/validate.py` — 19 docs, 26 entities, 64 claims, 15 sources, **0 errors** |
| One computed dimension | ✅ | D6 cost, computed from real pricing claims × usage profile |
| One hashed + archived source | ✅ | `sha256:f067cfe0…70f1`, Wayback `20260804053539` |
| One generated recommendation | ✅ | ranked candidates with fit, bands, coverage |
| One generated explanation | ✅ | all six mandatory components emitted |
| One recommendation delta | ✅ | reference-date change → +50.0% cost, D6 4→3 |

### The validator found six real errors on first run

Not a smoke test. Against a corpus I had hand-checked for six milestones:

- 3 **schema gaps** — `$schema` key rejected; relationships couldn't point at
  objectives (`measures` had nowhere to go); `sample_size` not nullable.
- 1 **data error** — SWE-bench construct-validity claims were `temporal_kind:
  static`, which asserts *true forever* and forces cadence ≥3650. They are
  `step` facts: true until the benchmark changes. **My own schema caught my own
  category error.**
- 2 duplicates of the above.

### The delta is the strongest result

```
2026-08-15  Claude Sonnet 5   $57.00/mo   D6=4   band 1
2026-09-15  Claude Sonnet 5   $85.50/mo   D6=3   band 1
                              +50.0%
```

Nothing was edited between runs. The engine resolved `graph_at(date)`, found
the introductory-pricing claim's validity interval closing 2026-08-31, selected
the superseding claim, recomputed cost, and re-scored across an anchor boundary.

**The bitemporal model — the most speculative part of the architecture — does
real work.** This is the single clearest demonstration that the design was worth
its complexity.

### The engine correctly refuses

`INSUFFICIENT_COVERAGE` at 1/13 dimensions, with `resolves_with` naming the
missing evidence streams. It ranks *and* refuses simultaneously: the ranking is
shown, marked as insufficient. That is the designed behaviour, and it fired
without being special-cased.

---

## 2. What architecture proved unnecessary

**In this slice — noting the sample is one dimension, which limits how much
this generalizes.**

- **Belief distributions, Monte Carlo P(best), minimax regret.** Meaningless at
  one dimension. A distribution over a single ordinal score adds nothing a
  confidence label doesn't already carry. **They earn their place only above ~4
  scored dimensions.** Until then they are dead weight, and I built the slice
  without them at no cost.
- **Dominance pruning.** Requires ≥2 dimensions to be anything but a sort.
- **Option value, switching cost, budget frontier.** All need multi-dimension
  input.
- **The `provides` convenience index** on entities — never read. Relationships
  were sufficient.
- **`slug_frozen_at`** — never read by anything.

**Not judged unnecessary, just untested:** the capability system, the objective
metric-sets, and the persona hard-constraint eliminator. The slice used exactly
one persona and no capability constraints.

---

## 3. What assumptions failed

**A1 — "The corpus is clean because I checked it carefully."**
Wrong. Six errors, including a conceptual one about temporal kinds. Careful
manual review across six milestones missed all of them.

**A2 — "Schemas written alongside data will match the data."**
Wrong in three places. Every schema gap was a case where I wrote data one way
and schema another and never executed the comparison.

**A3 — "Dates are unambiguous."**
YAML 1.1 auto-casts unquoted ISO dates to `datetime.date`. JSON Schema has no
date type. 343 spurious errors from a serialization mismatch that no amount of
document review would have surfaced.

**A4 — "Editing files is safe."**
PowerShell 5.1 `Get-Content -Raw` decodes UTF-8 as ANSI and `Set-Content
-Encoding utf8` writes a BOM. My own edits corrupted four schema files —
mojibake in descriptions and BOMs that broke `json.loads`. Recorded as a
standing rule: **never edit UTF-8 data files through PS5.1 text cmdlets.**

**A5 — "`value: unknown` is harmless."**
It is a legal, deliberately-published value, and it crashed the cost function
because the code assumed `value` was always a mapping. The *honesty* feature
broke the *engine*. Guarded now — a `value: unknown` price correctly excludes
an entity from cost ranking rather than erroring.

**A6 — most importantly: "the specification is the hard part."**
The specification was ~7,000 lines. The working slice is ~700. The specification
was not wrong, but it was **an order of magnitude larger than what was needed to
prove the ideas**, and building the slice first would have caught A1–A5 six
milestones earlier.

---

## 4. Trust Audit items now resolved

| # | Item | Status |
|---|---|---|
| **1** | Engine never produced a recommendation | ⚠️ **Partially resolved.** It now runs end-to-end and emits a full explanation object — but it *refuses*, correctly, at 1/13 coverage. The pipeline is demonstrated; a *positive* recommendation still is not. |
| **2** | Every "build fails" rule is fiction | ✅ **Resolved.** The validator exists, runs, exits non-zero, and found six real errors. Not all ~25 rules are implemented — ~14 are — but enforcement is now real rather than asserted. |
| **4** | No source hashed or archived | ⚠️ **Partially resolved.** One source of fifteen now has a real SHA-256 and Wayback URL. The tool works; the backfill has not run. |

**Unchanged:** #3 (self-administered gates — no external rater has looked at
anything) and #5 (vendor-skewed corpus — unchanged at 26 entities).

**Net: two items partially resolved, one substantially resolved, two untouched.**

---

## 5. What still prevents an expert from trusting the Atlas

Ranked, post-slice.

**1. No dimension other than cost has ever been scored.** *Critical.*
The engine refuses on everything real. D6 is computable only because pricing is
Class A specification data; the twelve dimensions that require judgement or
independent evidence remain at zero. An expert would say the system currently
answers "which is cheapest under assumptions we invented" and nothing else.

**2. The usage profile is invented.** *Critical.*
Every dollar figure above — $57.00, $85.50, $285.00 — derives from a token count
with no measurement behind it. The engine labels this correctly (`status:
assumed`, confidence floored to `low`, assumptions surfaced in the explanation),
but labelling a fabrication does not make it a measurement.

**3. Nobody but me has checked anything.** *High.* Unchanged from the audit.
Inter-rater reliability is still specified in four places and run zero times.

**4. Fourteen of fifteen sources are still unhashed and unarchived.** *High.*
The tool now exists, which converts this from an architectural gap into an
unfinished chore — but the chore is unfinished.

**5. The corpus is 26 entities and vendor-skewed.** *Moderate–high.* Unchanged.

### The honest summary

The slice proved the machine turns over. It did not prove the machine produces
anything worth acting on — and it wasn't supposed to.

What changed today: the Atlas moved from *asserting* enforcement, computation,
provenance, and temporal reasoning to *demonstrating* them, at small scale, with
commits anyone can check. What did not change: it still cannot tell a UI/UX
designer with $25/month what to do tomorrow, and the reason is evidence, not
architecture.

**That is now the only thing standing in the way, which is a better place to be
than yesterday.**
