# SOURCE CAPTURE LIMITATIONS — 2026-08-03

**Status:** blocking methodological finding, raised at the start of M3
**Affects:** every source record captured before T-002 ships

SOURCES.md §7 and §9 require every source to carry a **content hash**, an
**archive URL**, and a **verbatim excerpt**. The capture tooling available today
cannot fully deliver two of those three. Recording it here rather than quietly
lowering the standard.

---

## 1. Content hashes are not available

The fetch tool returns a *processed rendering* of a page, not the raw response
body. Hashing that rendering would produce a value that changes when the tool
changes, not when the page changes — which defeats the entire purpose of the
hash (detecting silent vendor edits, SOURCES.md §7).

**Decision:** `content_hash` is recorded as `null` with
`hash_status: unavailable_pending_tooling`. It is **not** fabricated, and the
validator's hash requirement is recorded as a known-failing rule rather than
relaxed.

**Consequence:** the automatic re-verification trigger (a changed hash marks
dependent claims `needs_review`) does not work yet. Until T-002 ships,
re-verification is calendar-driven only. Every claim captured in this window
carries `reverification: calendar_only`.

## 2. Excerpt fidelity varies by source, and it is not always verbatim

The tool answers a prompt against a page using a small model. Sometimes it
returns near-raw document text; sometimes it returns a restructured summary.
Those are very different evidentiary artifacts and must not be recorded
identically.

A new required field, `excerpt_fidelity`:

| Value | Meaning | Admissible for |
|---|---|---|
| `verbatim` | Returned text is the page's own text — tables, sentences, and numbers reproduced structurally intact | Any claim type |
| `tool_extracted` | Numbers and IDs appear reproduced, but prose is restructured by the extraction model | S-type claims only, flagged |
| `tool_summarized` | Content is paraphrased | **Nothing.** Pointer only, like Class E |

**Observed today:**

| Source | Fidelity | Basis |
|---|---|---|
| Anthropic models overview | `verbatim` | Full markdown tables, footnotes, and inline components returned intact |
| Anthropic pricing | `verbatim` | Same |
| OpenAI pricing | `tool_extracted` | Opens "Based on the pricing page, here are…" — restructured, though IDs and figures appear reproduced |
| Google Gemini pricing | `tool_extracted` | Individual figures quoted, surrounding structure rebuilt |

**Consequence:** the Anthropic figures below can support published claims. The
OpenAI and Google figures are recorded as `draft` claims requiring a
verbatim re-capture before publication. They are *not* published on the strength
of a restructured extraction — that would be exactly the Class E laundering
SOURCES.md §1 exists to prevent.

## 3. Archive URLs are not being created

Creating an archive snapshot requires a write request to an archiving service.
Not attempted. `archive_url: null`, `archive_status: pending`.

**Consequence:** these sources are vulnerable to the exact failure the archival
policy exists to prevent — a vendor edits a pricing page in place and our
citation now points at different content with no record of what it said. For
pages known to change silently (all four captured today), this is a real risk and
the reason T-002 is the top tooling task.

---

## 4. What this changes

1. `source.schema.json` gains `excerpt_fidelity`, `hash_status`, and
   `archive_status`. Required fields become conditionally required.
2. Claims sourced only to `tool_extracted` evidence cannot reach
   `status: published`. They sit at `draft`.
3. **The corpus starts with a known, documented integrity gap** rather than a
   hidden one. Everything captured in this window is re-captured when T-002
   ships, and the re-capture is a scheduled task, not an aspiration.

The alternative — writing plausible hashes, calling restructured text verbatim,
and moving on — would have produced a corpus that looks compliant and is not.
CONSTITUTION §2 and §7 make that the one thing this project cannot do.

---

## 5. Tasks created

| ID | Task |
|---|---|
| T-002a | Raw-body fetch + SHA-256 hashing, independent of any extraction model |
| T-002b | Archive snapshot creation on capture |
| T-002c | Verbatim excerpt extraction with fidelity classification |
| T-090 | Re-capture every source recorded in this window once T-002 ships |
