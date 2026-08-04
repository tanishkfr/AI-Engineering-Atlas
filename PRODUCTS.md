# TWO PRODUCTS, ONE GRAPH

**Status:** v1.0 · **2026-08-04**

The project ships two products. Neither is subordinate. They share one evidence
graph, and that shared graph is the entire reason both are worth building.

---

## Product A — AI Engineering Atlas

**A canonical reference for the modern AI engineering ecosystem.**

Answers questions about individual models, harnesses, providers, editors,
benchmarks, protocols, and workflows.

- **Success measured by:** reference quality — is this the best available account
  of what this thing is, what it costs, what it does not do, and what nobody has
  established about it?
- **Cadence:** continuous. **The default state of the project is reference
  growth.**
- **Reader:** someone searching for a specific tool who wants a straight answer.

## Product B — AI Engineering Observatory

**An original research program investigating questions that change engineering
decisions.**

Produces findings that cannot be copied from vendor documentation, because
nobody has measured them.

- **Success measured by:** recommendation impact — did this change what we tell
  people?
- **Cadence:** irregular. **Publishes only when evidence meets the standard**
  (EVIDENCE §4). Never on a schedule.
- **Reader:** someone who wants their assumptions tested.

---

## The relationship

```
        Atlas population  ──────────────▶  new research questions
              ▲                                     │
              │                                     ▼
     improved recommendations  ◀────────  Observatory findings
              ▲                                     │
              └──────────  shared evidence graph  ◀─┘
```

This has already happened repeatedly and is not aspirational:

| Atlas population found… | …which became Observatory research |
|---|---|
| A vendor's ~30% tokenizer note | RQ-01 → measured cross-vendor spread |
| Rate-limit tables | RQ-02 throughput-constrained autonomy |
| Cache multipliers + ITPM exclusion | RQ-03 cache economics |
| Three incompatible pricing shapes | RQ-09, RQ-14 cost-model extensions |

And in reverse:

| Observatory finding | …which changed the Atlas |
|---|---|
| Normalization rarely flips rankings | Corrected an over-broad Atlas claim (D-001) |
| Subscription meter isn't token-denominated | Turned a gap into an answer (D-003) |
| MCP cannot enforce its own security | D13 must be scored on hosts (D-004) |

---

## Operating rules

1. **Continuous reference growth is the default.** Atlas population does not pause
   for research.
2. **Only one flagship experiment executes at a time.** Currently RQ-05, gated.
3. **The Observatory publishes on evidence, never on schedule.** A quarter with
   no publishable finding is a correct outcome, not a failure.
4. **Interrupt population only for:** methodology failures threatening research
   integrity · Decisive-ERI research questions · recommendation-changing evidence.
5. **Neither product's metric may be used to argue against the other's work.**
   Coverage does not measure reference value; reference count does not measure
   decision quality.

Rule 5 exists because I violated it in M5.1 — arguing against populating entities
because they would not move the coverage score. Correct about the metric, wrong
about the product.

---

## Milestone reporting

```
Decision Coverage        x / 50
Reference Coverage       entities, gold-standard count
Evidence Coverage        Class B / Class C / dimensions scored
Recommendation Deltas
Original Findings
Methodology Changes
Biggest Remaining Unknowns
```

Entity counts are a footnote, never a headline.
