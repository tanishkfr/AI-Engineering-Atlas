"""Class C synthesis — cluster harvested records into convergent behaviours.

Exercises COMMUNITY-EVIDENCE-PROTOCOL §4: cluster by BEHAVIOUR, never by votes.
Applies the thresholds mechanically so the outcome is not a judgement call:
  >= 5 independent threads, >= 50 distinct participants, >= 2 platforms,
  no single thread > 40% of participants, >= 3 independent reports per behaviour.

Run: python scripts/evidence/synthesize.py --dimension D7
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "research" / "evidence" / "raw"

# Behaviour probes. Deliberately SPECIFIC — the protocol requires clustering on
# concrete described behaviour, not sentiment. "It's slow" must not match.
PROBES = {
    "D7": {
        "rate_limit_interrupts_session": [
            r"\b(hit|hitting|ran into|reached)\b.{0,40}\b(rate ?limit|usage limit|quota|cap)\b",
            r"\blimit\b.{0,30}\bmid[- ]?(session|task|flow)\b",
        ],
        "context_exhaustion_forces_restart": [
            r"\b(context|window)\b.{0,40}\b(ran out|exhaust|full|overflow|compact)\b",
            r"\b(had to|forced to)\b.{0,30}\brestart\b",
        ],
        "over_asks_before_acting": [
            r"\b(too many|keeps? asking|constantly asks?)\b.{0,40}\b(question|clarif|confirm)\b",
            r"\basks?\b.{0,30}\bbefore (doing|writing|starting)\b",
        ],
        "edits_not_applied": [
            r"\bedit(s)?\b.{0,40}\b(not applied|failed|didn'?t apply|silently)\b",
            r"\b(diff|patch)\b.{0,30}\b(fail|reject|malformed)\b",
        ],
        "unexpected_cost_spike": [
            r"\b(burn|burned|blew|spent)\b.{0,30}\b(\$|credit|token)",
            r"\bbill\b.{0,30}\b(shock|surprise|unexpected)\b",
        ],
    },
    "D9": {
        "workaround_required_for_nonstandard": [
            r"\bworkaround\b", r"\bhack(ed|y)?\b.{0,30}\b(around|together)\b",
        ],
        "cannot_change_system_prompt": [
            r"\b(can'?t|cannot|no way to)\b.{0,30}\b(system prompt|override|customi[sz]e)\b",
        ],
    },
}


def load_records() -> list[dict]:
    recs = []
    for p in sorted(RAW.glob("harvest-*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for r in d.get("records", []):
            r["_file"] = p.name
            recs.append(r)
    return recs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dimension", default="D7")
    a = ap.parse_args()

    probes = PROBES[a.dimension]
    recs = load_records()

    clusters: dict[str, list[dict]] = defaultdict(list)
    for r in recs:
        blob = f"{r.get('title') or ''}\n{r.get('text') or ''}".lower()
        for behaviour, patterns in probes.items():
            if any(re.search(p, blob, re.I) for p in patterns):
                clusters[behaviour].append(r)

    # Threshold evaluation, mechanical
    total_authors = {r.get("author") for r in recs if r.get("author")}
    platforms = {r.get("platform") for r in recs}
    per_thread = defaultdict(set)
    for r in recs:
        per_thread[r.get("url")].add(r.get("author"))
    max_share = (max((len(v) for v in per_thread.values()), default=0)
                 / max(len(total_authors), 1))

    corpus_gates = {
        "independent_threads": {"value": len(per_thread), "min": 5,
                                "pass": len(per_thread) >= 5},
        "distinct_participants": {"value": len(total_authors), "min": 50,
                                  "pass": len(total_authors) >= 50},
        "platforms": {"value": sorted(p for p in platforms if p), "min": 2,
                      "pass": len(platforms) >= 2},
        "max_single_thread_share": {"value": round(max_share, 3), "max": 0.40,
                                    "pass": max_share <= 0.40},
    }

    findings = []
    for behaviour, hits in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
        threads = {h.get("url") for h in hits}
        plats = {h.get("platform") for h in hits}
        authors = {h.get("author") for h in hits if h.get("author")}
        qualifies = len(threads) >= 3 and len(plats) >= 2
        findings.append({
            "behaviour": behaviour,
            "independent_threads": len(threads),
            "distinct_authors": len(authors),
            "platforms": sorted(p for p in plats if p),
            "qualifies_as_claim": qualifies,
            "reason": None if qualifies else
                      ("<3 independent threads" if len(threads) < 3 else "<2 platforms"),
            "sample_urls": sorted(t for t in threads if t)[:3],
        })

    qualifying = [f for f in findings if f["qualifies_as_claim"]]
    scoreable = all(g["pass"] for g in corpus_gates.values()) and len(qualifying) >= 3

    out = {
        "dimension": a.dimension,
        "protocol": "COMMUNITY-EVIDENCE-PROTOCOL v1.0",
        "records_analysed": len(recs),
        "population_gap": "reddit_unavailable",
        "corpus_gates": corpus_gates,
        "behaviour_clusters": findings,
        "qualifying_behaviours": len(qualifying),
        "threshold_for_scoring": ">=3 convergent behaviours across >=2 platforms",
        "verdict": "SCOREABLE" if scoreable else "NOT_SCOREABLE",
        "verdict_reason": (
            "all corpus gates pass and >=3 behaviours converge"
            if scoreable else
            "corpus gates failed" if not all(g["pass"] for g in corpus_gates.values())
            else f"only {len(qualifying)} behaviour(s) reached >=3 threads on >=2 platforms"
        ),
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
