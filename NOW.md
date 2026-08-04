# NOW

**FROZEN at v0.1 Research Preview — 2026-08-04**

> **North star:** *"I'm a UI/UX designer with $25/month. What should I actually
> do tomorrow?"*
> The Atlas cannot answer this yet. It can now say precisely why not.

---

## Status

**Frozen. Not paused, not blocked — frozen deliberately.**

The limiting factor is no longer engineering effort or analysis. It is **new
evidence from outside this machine**, and no amount of further work here
produces it.

## What unfreezes this

**Independent replication data.** One or more `--share` payloads from other
operators. See [REPLICATION.md](REPLICATION.md).

```bash
python scripts/evidence/usage_profile.py --days 56 --share
```

## When replication data arrives — do exactly this, in order

```bash
# 1. drop the payloads in replications/ then:
python scripts/evidence/replication_check.py replications/*.json
```

The classifier is mechanical and the thresholds are preregistered. **Do not
adjust them after seeing results.** Its verdict determines the next action:

| Verdict | Next action |
|---|---|
| `REPLICATED` | Relabel cost figures **harness-scoped**. Resolve RQ-28. Resume Track A/B. |
| `PARTIAL` | Publish cache rate as a **range**, never a point. Resume with the range. |
| `FALSIFIED` | **Retract the cost correction.** Publish the retraction with equal prominence to the original finding. Relabel everything operator-scoped. |
| `AWAITING_REPLICATION` | Still frozen. |

## Current machine state

```
verdict: AWAITING_REPLICATION
usable independent replications: 0 (1 required)
cost correction licensed as: operator-scoped only
RQ-28: open — unresolved
```

## Do not, while frozen

- Analyse the originating transcripts further — ten cuts of one dataset still
  have n=1
- Add entities to raise a count
- Extend the architecture
- Soften any threshold to make a result fit

Each is available, none moves credibility, and each is a way of looking busy
while the actual constraint goes untouched.

## Decision needed from user

1. **Collect 3–5 independent `--share` payloads.** Do not tell replicators the
   expected value — it biases nothing mechanically, but it biases whether they
   bother to report an odd result.
2. **Reddit OAuth** — still deferred, still the largest Class C population gap.
3. **Remote push** — repo is versioned locally and tagged. Not pushed anywhere.
