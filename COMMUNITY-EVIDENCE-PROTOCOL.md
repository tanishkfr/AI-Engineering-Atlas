# COMMUNITY EVIDENCE PROTOCOL

**Status:** v1.0 · **2026-08-04** · Extends [METHODOLOGY.md](METHODOLOGY.md) §4
**Governs:** all Class C collection · **Primary consumers:** D4, D7, D9, D10, D12

---

## 1. Why this needs its own protocol

Class C is the **authoritative** class for experience claims (SOURCES §3). It is
also the easiest evidence in the world to fake yourself into. Read enough
threads and you will find support for any conclusion you brought with you.

The protocol exists to make a Class C sample reproducible by a stranger who
disagrees with us.

## 2. Thresholds

| Requirement | Threshold |
|---|---|
| Minimum independent threads | **5** |
| Minimum distinct participants | **50** |
| **Max share of participants from any single thread** | **40%** |
| Maximum source age | **6 months** |
| Minimum independent reports per specific behaviour | **3** |

### The 40% rule — an addition to the proposed thresholds

A 50-participant minimum can be satisfied by one viral thread. One thread is one
context, one moment, and frequently one framing that everyone downstream is
reacting to.

**Capping any single thread at 40% of the participant count forces genuine
independence.** Convergence across five separate contexts is evidence.
Fifty people agreeing inside one thread is one data point with fifty
signatures.

## 3. Platforms

| Platform | Strength | Known bias |
|---|---|---|
| Reddit | Volume; sustained-use reports | Recency; vocal minority; subreddit culture |
| GitHub Discussions | Specific, versioned, reproducible | Skews to bugs over workflow friction |
| Hacker News | Senior practitioners | Strong contrarian and novelty bias |
| Discord summaries | Real-time friction | Ephemeral; hard to cite; unrepresentative sampling |
| Maintainer discussions | Authoritative on intent | Not independent of the project |
| Engineering blogs | Long-form, sustained use | Survivorship — people write when it worked |

**Minimum two platforms per finding.** A behaviour found only on one platform is
recorded as platform-specific until shown otherwise.

### 3.1 Retrieval methods — evaluated empirically 2026-08-04

Probed by `scripts/evidence/probe_platforms.py`. **Findings, not assumptions.**

| Platform | Method | Auth | Status | Suitable? |
|---|---|---|---|---|
| **Hacker News** | Algolia API `hn.algolia.com/api/v1/search_by_date` | none | ✅ 200 | **Yes** — stories *and* comments, date-filterable |
| **GitHub** | `gh api graphql`, DISCUSSION + ISSUE search | gh auth | ✅ works | **Yes** — searches bodies, not just titles |
| **Stack Exchange** | API v2.3 `/search/advanced` | none, quota | ✅ 200 | **Yes, low priority** — Q&A format rarely carries migration narratives |
| **Reddit** | `.json` endpoints (www and old) | none | ❌ **403 Blocked** | **No** — see §3.2 |
| **Lobsters** | `search.json` | none | ❌ 400 | Deferred — low volume, not worth debugging |

**Operational retriever:** `scripts/evidence/harvest.py`. Records the executed
query verbatim, applies a 1s inter-request delay, caps body extraction, and
writes raw records to `research/evidence/raw/` for independent re-analysis.

**Demonstrated clearing thresholds** (2026-08-04, query `"switched from claude
code"`, window from 2026-02-01): 104 threads · 101 distinct authors · 2
platforms · 0 errors. Thresholds are 5 / 50 / 2.

### 3.2 Reddit — blocked, and not worked around

Both `www.reddit.com` and `old.reddit.com` `.json` endpoints return **HTTP 403**
without authentication.

**We are not circumventing this.** Evading an access control the platform has
deliberately applied is not an acceptable research method, regardless of whether
a workaround exists. Scraping HTML behind a blocked JSON endpoint, rotating user
agents, or routing through third-party mirrors are all excluded.

**The compliant path** is Reddit's OAuth API, which requires a registered
application and credentials the project does not hold. That is a **user action**,
not something the pipeline can resolve.

**Consequence, stated plainly:** the highest-volume source of sustained-use and
migration reports is unavailable. Findings produced from HN and GitHub alone
carry a **known population bias** — HN skews senior and contrarian, GitHub skews
toward bug reports over workflow friction. Neither represents the practitioner
mainstream that Reddit reaches.

**Every Class C claim collected without Reddit must record**
`population_gap: reddit_unavailable`. This is not a formality: it is the
difference between "practitioners report X" and "senior HN commenters and GitHub
issue filers report X."

## 4. Synthesis: by theme, never by votes

**Votes measure agreement with a framing. Themes measure recurrence of an
experience.** These come apart constantly — the most-upvoted comment is often the
best-written one, not the most common experience.

Procedure:

1. Extract every **specific behavioural claim** from each thread. "It's slow" is
   not specific. "It re-reads the whole file after every edit" is.
2. Cluster by behaviour, not by sentiment.
3. Count **independent threads** per cluster, not upvotes, not comments.
4. A cluster reaching 3 independent threads across ≥2 platforms becomes an
   X-type claim.
5. Record dissent inside the cluster. If 3 threads report a behaviour and 2
   report the opposite, that is `contested`, not a finding.

**Explicitly forbidden:** ranking findings by engagement; quoting the top comment
as representative; treating thread volume as a measure of severity.

## 5. Mandatory tagging

Every Class C source records: platform · query executed **verbatim** · time
window · thread URL · participant count · `usage_duration`
(first-impression / weeks / months / sustained / unknown) · `sample_type`
(single-report / recurring-theme / consensus).

**`usage_duration` carries the most weight.** A sustained-use report outweighs
launch-week reaction by a wide margin, and the two are systematically confused
because they use the same words.

## 6. Migration stories — a first-class evidence type

> "Cursor is good" is an opinion.
> "I switched from Cursor to OpenCode because I kept hitting quota mid-session"
> is evidence.

Migration reports are the strongest adoption signal available, because they carry
a **stated cost**: the person paid switching costs and can say why. They also
point opposite to marketing, which is precisely what makes them valuable.

### Migration record schema

```yaml
migration:
  from: ent-…
  to: ent-…
  stated_reason: "…"                  # verbatim, the person's own words
  reason_category: cost | rate_limits | quality | autonomy | lock_in |
                   workflow_friction | reliability | ecosystem | other
  usage_duration_before_switch: weeks | months | sustained
  switched_back: true | false | unknown
  partial: true | false               # kept both tools?
  platform: …
  thread_url: …
  date: …
```

### Two rules that prevent over-reading

**`switched_back` must be sought, not assumed.** Migration threads are written at
the moment of switching, when enthusiasm is highest. A migration that reversed
three weeks later is a different finding and is rarely posted about.

**`partial` matters more than it looks.** "I switched" and "I added" are
different claims. Early signals suggest many practitioners run multiple tools
concurrently rather than replacing one with another — if that holds, migration
counts systematically overstate displacement.

### Target migration pairs

Prioritized because each isolates a different decision axis:

| Pair | Isolates |
|---|---|
| Cursor ↔ Claude Code | editor-resident vs terminal-resident workflow |
| Claude Code ↔ OpenCode | vendor-locked vs model-agnostic |
| Claude Code ↔ Codex CLI | vendor-to-vendor at equivalent position |
| Frontier ↔ open-weight | cost vs capability |
| OpenRouter ↔ first-party | routing convenience vs directness |
| Cloud ↔ local | privacy/cost vs capability |

## 7. What is NOT Class C

The commonest failure, and the one that produced a discarded sample today:

| Artifact | Actual class |
|---|---|
| A blog post summarizing Reddit threads | **Class E** — pointer only |
| "What 500 developers on Reddit think" articles | **Class E** |
| A vendor's own community forum, on their own product | Class A |
| An aggregator's sentiment analysis | **Class E** |
| The Reddit threads themselves | **Class C** ✅ |

**Secondary summaries of community sentiment are Class E regardless of how many
people they claim to represent.** A number in a headline is not a sample. Using
them as citations would let one writer's reading of a forum enter the corpus as
if fifty practitioners had been sampled.

They are legitimate for **finding** threads. Then the threads get read.

## 7.5 The relevance gate

*Added 2026-08-04 after Synthesis 001.*

The §2 thresholds measure **independence**. They do not measure **relevance**,
and a corpus can pass all of them while containing none of the evidence sought.

Synthesis 001 produced a sample of 157 distinct participants across 162 threads
with a largest-thread share of 0.6% — sixty-six times better than the ceiling —
and **one** matching behaviour report. The queries were entity-targeted
(`"claude code"`), so they returned discussion *about* the tool rather than
friction *with* it.

**Gate: probe hit rate ≥ 5%.** Before synthesis, at least 5% of harvested
records must match at least one specific behaviour probe. Below that the harvest
is **off-target** and is re-run with different queries rather than analysed.
Analysing an off-target corpus produces a null result that looks like an absence
of evidence and is actually an absence of sampling.

**Query design rule: harvest on symptoms, not subjects.** Query the behaviour
being investigated, then filter by entity — never the reverse. Product names
select for announcements and comparisons; symptom language selects for
experience.

## 8. Failure conditions

Publish as insufficient — do not extend the sample — when:

- Fewer than 5 independent threads within the window
- A single thread exceeds 40% of participants
- Fewer than 3 independent reports for any behaviour
- Only one platform is represented

**A null harvest is a valid, publishable outcome.** The dimension stays
`not_scored`.
