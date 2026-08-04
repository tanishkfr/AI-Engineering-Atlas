# COVERAGE BENCHMARK — 50 decision questions

**Defined:** 2026-08-04, **before** the M5.1 population pass
**Status:** FROZEN — questions are not edited to match findings

---

## Why this is frozen

A coverage metric defined *after* seeing what you found measures nothing. It
selects for questions you happen to be able to answer.

These 50 questions were written before the M5.1 research pass, from the personas
and primary questions established in M1–M2. **Questions are never removed or
reworded because they turned out to be hard.** If a question is unanswerable for
a year, it stays on the list scoring zero, and that is the point.

Adding questions is permitted; the count moves and the denominator moves with it.
Removing one requires a recorded reason.

## Scoring criteria

| State | Requirement |
|---|---|
| **Fully answerable** | Engine returns a recommendation or an *informative* refusal, backed by admissible evidence, traceable to sources, scoped to a persona |
| **Partially answerable** | Some components evidenced; at least one required input missing, so the answer is incomplete but not empty |
| **Unanswerable** | No admissible evidence for the core of the question |

**An informative refusal counts as fully answerable** when the refusal is itself
the correct answer and names what would resolve it — e.g. Q7 below, where "this
is not publicly computable, and here is why" is the true answer.

---

## A. Budget and cost (Q1–Q8)

1. I have $20/month — what stack should I use?
2. I have $100/month — what changes?
3. What does a month of real agentic development actually cost?
4. Subscription or metered API for my usage?
5. What does my next $25 buy me?
6. Which is cheaper per unit of completed work, not per token?
7. Can I compare two vendors' prices directly?
8. What are the hidden per-request costs?

## B. Model choice (Q9–Q16)

9. Which model for agentic coding?
10. Which model for frontend generation?
11. Which model for large-repo comprehension?
12. When is an open-weight model good enough?
13. Does the model matter more than the harness?
14. Which model has the largest usable context?
15. Which model has the most current knowledge?
16. Should I route different tasks to different models?

## C. Harness and workflow (Q17–Q25)

17. Which coding harness should I use?
18. CLI agent or IDE-resident agent?
19. Do I need a harness that supports multiple models?
20. Which harness works headless / in CI?
21. Which harness handles long-horizon tasks best?
22. How much human intervention will I actually need?
23. Does the harness support subagents or parallel work?
24. How does a harness manage context as sessions grow?
25. How does a harness recover from its own errors?

## D. Provider and access (Q26–Q32)

26. First-party API or aggregator?
27. Which provider is fastest?
28. Will rate limits bind before price does?
29. Can I control which provider serves my request?
30. Can I avoid quantized endpoints?
31. What happens to my code — is it trained on?
32. Can I keep inference in a specific geography?

## E. Editors and surfaces (Q33–Q37)

33. Which editor for AI-assisted work?
34. Do I need an AI-first editor, or is an extension enough?
35. How does editor choice change the AI workflow?
36. Can I use the same agent across editor and terminal?
37. What if I barely code — what's the lowest-friction surface?

## F. Context engineering (Q38–Q42)

38. What belongs in a repo instruction file?
39. Index-first or agentic search for a large repo?
40. Does a memory layer earn its complexity?
41. How much does prompt caching actually save?
42. Is there a cross-vendor standard for agent instructions?

## G. Interop and ecosystem (Q43–Q46)

43. Which protocols are safe to build on?
44. Does supporting MCP make a tool secure?
45. Which MCP servers are worth installing?
46. What's the security exposure of third-party extensions?

## H. Evidence and trust (Q47–Q50)

47. What does SWE-bench actually measure?
48. Why do benchmark scores for the same model disagree?
49. When should I ignore benchmark rankings entirely?
50. Does AI-assisted development actually make teams faster?

---

## Baseline — scored at M5 close, before M5.1 population

| State | Count |
|---|---|
| Fully answerable | **3** / 50 |
| Partially answerable | **9** / 50 |
| Unanswerable | **38** / 50 |

**Fully answerable at baseline:** Q7 (no — normalization rule established),
Q4 and Q1 (informative refusal: not publicly computable, with the reason).

That baseline is deliberately unflattering. It is the honest starting point.

---

## Scored — M5.1 close, 2026-08-04

| State | Count | Δ from baseline |
|---|---|---|
| **Fully answerable** | **7** / 50 | +4 |
| **Partially answerable** | **14** / 50 | +5 |
| **Unanswerable** | **29** / 50 | −9 |

### Fully answerable (7)

| Q | Question | Why it qualifies |
|---|---|---|
| Q1 | $20/month stack | Informative refusal: `NOT_PUBLICLY_COMPUTABLE`, with the reason (session-based meter) |
| Q4 | Subscription or metered | Same — the comparison is not computable, and we can say why |
| Q7 | Compare two vendors' prices directly | Yes, with the ~11% rule from `exp-normalized-cost-v1` |
| Q42 | Cross-vendor instruction standard | AGENTS.md, 23 products, foundation-stewarded — with the interop caveat stated |
| Q44 | Does MCP support make a tool secure | **No** — the spec says it cannot enforce security at protocol level |
| Q47 | What SWE-bench measures | Full construct-validity record: measures, does not measure, misuse |
| Q49 | When to ignore benchmark rankings | Derived from Q47 + harness-dependency + solvability-filter bias |

### Partially answerable (14)

Q2, Q3, Q8 (cost shape known, absolute figures blocked on usage profiles) ·
Q14, Q15 (context and knowledge cutoffs captured for one vendor family) ·
Q17, Q19, Q20, Q23 (harness capabilities captured; no scores) ·
Q28 (rate-limit tables captured for one provider) ·
Q29 (routing controls captured, draft) · Q32 (geography controls captured) ·
Q38 (placement/resolution known, content structure not) ·
Q43 (MCP + AGENTS.md governance known; adoption durability not)

### Still unanswerable (29)

All quality, autonomy, and comparative questions — Q9–Q13, Q16, Q18, Q21, Q22,
Q24, Q25 — because **zero dimensions are scored**.
All editor questions Q33–Q37 — **no L4 editor entity exists**.
Q5, Q6 (need measured usage profiles) · Q26, Q27, Q30, Q31 (provider coverage
too thin; no speed or data-policy evidence) · Q39, Q40, Q41 (context-engineering
practices unresearched) · Q45, Q46 (no MCP server entities) · Q48, Q50 (need
Class B evidence).

### The binding constraint, stated plainly

**29 of 50 are unanswerable, and 20 of those 29 fail for one of two reasons:**

1. **No dimension is scored anywhere** (zero Class B, zero Class C evidence) —
   blocks every quality, autonomy, and "which should I use" question.
2. **Entire workstreams have no entities** — editors (0), MCP servers (0),
   agent frameworks (0), context-engineering practices (0).

Adding more model or provider entities will move this number **very little**.
The next meaningful jump requires Class B/C evidence so that scoring can begin,
not more Class A specification capture.
