# REPLICATION — R1

**Five minutes. One command. No setup. No account. No cost.**

You are being asked to help falsify a finding, not confirm it.

---

## What this is

The AI Engineering Atlas measured two numbers that turned out to be badly wrong
in its own cost model. The correction changed recommendations substantially.

**The problem: the measurement has a sample size of one.** One person, one
machine, one toolchain. We do not know whether the result describes the ecosystem
or describes that person's setup.

You can settle it in about two minutes.

## What it measures

Two ratios, from agent transcript files already sitting on your disk:

| Metric | What it is |
|---|---|
| **Cache hit rate** | Share of tokens sent to the model that were served from cache rather than charged at full input price |
| I/O ratio | Input tokens presented per output token generated |

**Only the cache hit rate is being tested.** The I/O ratio is already classified
as workload-specific — we *expect* yours to differ, and that difference carries
no evidential weight.

## Why it matters

Cached tokens bill at roughly **one tenth** of normal input price (one vendor
prices them at ~1/120th). So the cache hit rate, not the model's headline price,
dominates what agentic coding actually costs.

Our measurement put it at **0.9432**. Our previous assumption was 0.35–0.60.
Correcting it dropped every cost figure in the Atlas by **81–89%**, and changed
which models fit inside a $20/month budget.

If that rate is a property of the *harness*, it holds for everyone using it and
the correction is sound. If it is a property of *one person's habits*, the
correction is wrong and we need to retract it.

**Your number decides which.**

## Expected runtime

| Step | Time |
|---|---|
| Clone / download | ~1 min |
| Run the command | 30 s – 3 min (scales with transcript volume) |
| Copy 4 numbers into a reply | ~30 s |

## Privacy guarantees

The `--share` output contains **aggregate statistics only**. It is verified
adversarially, not asserted.

**Cannot be exposed — mechanically prevented:**

prompts · code · conversation content · file names · file paths · project names ·
repository identifiers · git branches · timestamps · dates · session IDs · URLs ·
email addresses · hashes · tool names

**How this is enforced:** the extractor reads a *fixed allowlist* of numeric
fields. It is not a content reader with a filter — there is no code path by which
text can reach the output.

**How it is verified:** `scripts/evidence/verify_share.py` runs the real command
against real transcripts, then (a) asserts an exact key allowlist, (b) asserts
every data leaf is numeric, (c) scans for path/timestamp/URL/email/hash patterns,
and (d) takes 78 distinctive strings out of your actual transcript files and
proves none appear in the output.

**Run the verifier yourself before sharing anything.** It exits non-zero if any
check fails.

## Exactly how to execute it

```bash
git clone <repo-url> && cd AI-Engineering-Atlas
python scripts/evidence/verify_share.py
python scripts/evidence/usage_profile.py --days 56 --share
```

Requires Python 3.9+. No dependencies for these two scripts. Reads only
`~/.claude/projects/**/*.jsonl` (or `%USERPROFILE%\.claude\projects\`). Writes
nothing to disk in `--share` mode.

If you use a different agent harness that emits token telemetry, say so — that is
**more** valuable than another run on the same one, because it tests the harness
hypothesis directly.

## Exactly what to share

The entire output. It is four numbers and a fixed literal block:

```json
{
  "replication_of": "RQ-18/19",
  "window_days": 56,
  "cache_hit_rate": 0.xxxx,
  "io_ratio": xxx.xx,
  "turns": xxxxx
}
```

Nothing else. Do not send transcripts, logs, or screenshots — they are not
wanted and will not be used.

## What your number will mean

Thresholds were **fixed in advance**, before any replication was collected. They
are not adjustable after seeing your result.

| Your cache hit rate | Verdict | Consequence |
|---|---|---|
| **≥ 0.85** | Replicates | Correction is harness-level. Atlas publishes cost figures scoped to this harness. |
| **0.70 – 0.85** | Partial | Direction holds, magnitude varies. Atlas publishes a **range**, never a point estimate. |
| **< 0.70** | **Falsified** | Our number is idiosyncratic. Atlas **reverts** the correction to operator-scoped and publishes a retraction. |

A payload with fewer than 200 turns is treated as **underpowered** and excluded
rather than counted — not a judgement on your usage, just insufficient signal.

## What happens next

Results are fed to:

```bash
python scripts/evidence/replication_check.py replications/*.json
```

which applies the thresholds mechanically, classifies the outcome, resolves or
maintains **RQ-28**, and states what the cost correction is licensed to claim.
No human judgement enters at that step.

**A falsifying result is as useful to us as a confirming one, and will be
published with equal prominence.** If you run this and our number does not hold
up, that is the outcome we most need.
