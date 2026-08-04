# Contributing

**The point of this file: disagreement should arrive as a pull request, not an
opinion.**

Every gate in this project is currently administered by the person who wrote it.
That is the deepest unresolved weakness in the Trust Audit, and it cannot be
fixed by trying harder — only by other people being able to push back
mechanically. This is the door.

---

## The one rule

**If you did not retrieve it, you do not know it.** No reconstructed URLs, no
numbers from memory, no paraphrased excerpts, no guessed dates. `unknown` is a
publishable, respected value.

---

## Add a claim in five steps

**1. Capture the source.**

```bash
python scripts/atlas/backfill_capture.py --dry-run
```

You need the URL, the retrieval date, a **verbatim excerpt**, and a SHA-256 of
the raw body. If you cannot hash it, set `content_hash: null` **and**
`hash_status: unavailable_pending_tooling`. Do not invent a hash — the validator
will not catch a plausible fake, and that is exactly why it matters.

**2. Grade the source honestly.**

Class A is the vendor about itself. Class B is independent work **with published
methodology** — assessed at the *deepest* page where methodology actually lives,
not the first one you land on ([SOURCES.md](SOURCES.md) §1.5). Class C is field
reporting. **Class E is a pointer and never a citation**, no matter how many
people a secondary summary claims to represent.

**3. Write the claim.**

Every claim needs a type (`S`/`M`/`X`/`C`/`T`/`F`), a `temporal_kind`, a full
bitemporal interval, and evidence. Never write `confidence` or `freshness` —
they are computed, and authoring them fails the build.

**4. Set `scope` — this is the one people forget.**

Who is this true for?

| scope | meaning |
|---|---|
| `universal` | holds regardless (arithmetic, definitions) |
| `vendor` | holds for this product |
| `harness` | determined by tooling, not by the person |
| `operator` | varies by individual |
| `workload` | varies by the kind of work |

**Anything not `universal` or `vendor` must carry an `elicit` block** — the
question that makes the claim applicable to a given reader. `elicit.default` is
locked to `null`; a default silently reintroduces the unasked assumption the
field exists to prevent.

**5. Run the gates.**

```bash
python scripts/atlas/validate.py      # must pass
python scripts/atlas/test_validate.py # 14/14 rules must fire
python scripts/atlas/bias_report.py   # check you are not deepening the skew
python scripts/engine/build_ui.py     # regenerate the interface
```

---

## Disagreeing with an existing claim

**Do not delete it.** Nothing is ever deleted.

- **We were wrong** → new claim with `supersession_kind: correction` and a
  `supersession_reason`. It appears in the corrections register.
- **The world changed** → `supersession_kind: change`. The old record stays true
  for its own interval, permanently.
- **Sources genuinely conflict** → add a `conflicts` block with a
  `likely_cause`. `unexplained` is permitted and preferred over invention.

## Disagreeing with the framework

Also welcome, and more valuable. Open an issue naming the document, the section,
and **what your change invalidates**. An amendment that leaves two documents
contradicting each other is incomplete
([CONSTITUTION.md](CONSTITUTION.md) §15).

## The most useful thing you can do

**Run the replication.** Two minutes, no setup, and it decides whether this
project's headline finding survives:

```bash
python scripts/evidence/usage_profile.py --days 56 --share
```

Output is four numbers and nothing else — verified adversarially against your
own transcripts ([REPLICATION.md](REPLICATION.md)). **A result that falsifies us
is worth more than one that agrees**, and will be published with equal
prominence.

## What gets rejected

Claims sourced only to Class E · authored confidence · guessed dates ·
paraphrase presented as excerpt · non-transferable claims without `elicit` ·
scores without a `via` harness context · anything that makes the corpus more
confident than its evidence.
