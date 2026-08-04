"""Atlas recommendation engine — minimal executable slice.

Implements the RECOMMENDATION.md pipeline narrowly but genuinely:
  graph_at(date) -> candidates -> constraints -> cost -> compute D6 ->
  confidence -> band -> explanation | refusal

Deliberately NOT implemented in this slice: belief distributions, Monte Carlo
P(best), minimax regret, dominance pruning, option value, budget frontier.
Those need >1 scored dimension to mean anything.

Run:
  python scripts/atlas/engine.py --persona per-solo-founder --date 2026-08-15
  python scripts/atlas/engine.py --persona per-solo-founder --date 2026-09-15
  python scripts/atlas/engine.py --delta 2026-08-15 2026-09-15
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


class StrDateLoader(yaml.SafeLoader):
    pass


StrDateLoader.add_constructor(
    "tag:yaml.org,2002:timestamp", lambda l, n: l.construct_scalar(n)
)


def _load(p: Path):
    return yaml.load(p.read_text(encoding="utf-8"), Loader=StrDateLoader)


# ---------------------------------------------------------------- graph_at()
def load_graph(ref: str) -> dict:
    """TEMPORAL.md §4: the subgraph valid AND asserted at `ref`."""
    entities: dict[str, dict] = {}
    sources: dict[str, dict] = {}

    for p in sorted(DATA.rglob("*.yaml")):
        if "schema" in p.parts:
            continue
        doc = _load(p)
        if not isinstance(doc, dict):
            continue
        for e in doc.get("entities") or ([doc] if str(doc.get("id", "")).startswith("ent-") else []):
            if isinstance(e, dict) and e.get("id"):
                entities[e["id"]] = e
        for s in doc.get("sources") or []:
            if isinstance(s, dict) and s.get("id"):
                sources[s["id"]] = s
    return {"entities": entities, "sources": sources, "reference_date": ref}


def _in_window(t: dict, ref: str) -> bool:
    vf, vt = t.get("valid_from"), t.get("valid_to")
    af, at = t.get("asserted_from"), t.get("asserted_to")
    if af and str(af) > ref:
        return False
    if at and str(at) <= ref:
        return False
    if vf and vf != "unknown" and str(vf) > ref:
        return False
    if vt and vt not in (None, "unknown") and str(vt) < ref:
        return False
    return True


def current_claims(ent: dict, predicate: str, ref: str) -> list[dict]:
    out = []
    for c in ent.get("claims") or []:
        if c.get("predicate") != predicate:
            continue
        if c.get("status") != "published":
            continue
        if _in_window(c.get("temporal") or {}, ref):
            out.append(c)
    return out


# ------------------------------------------------------- computed confidence
def compute_confidence(claim: dict, sources: dict) -> str:
    """SOURCES §5. Computed, never authored."""
    ev = claim.get("evidence") or []
    if not ev:
        return "unknown"
    classes = [sources.get(e.get("source"), {}).get("class", "?") for e in ev]
    distinct = len({e.get("source") for e in ev})
    ctype = claim.get("type")

    authoritative = ("A" in classes) if ctype == "S" else ("B" in classes or "D" in classes)
    if not authoritative:
        return "low"
    if claim.get("conflicts"):
        return "contested"
    flagged = sum(
        1 for e in ev
        if "self_interested" in (sources.get(e.get("source"), {}).get("flags") or [])
    )
    if distinct >= 2 and flagged < len(ev):
        return "high"
    if distinct >= 2:
        return "moderate"
    return "moderate" if flagged == 0 else "low"


def compute_freshness(claim: dict, ref: str) -> str:
    """TEMPORAL.md §6 — kind-aware."""
    kind = claim.get("temporal_kind")
    if kind in ("static", "point"):
        return "not_applicable"
    if kind in ("measurement", "series"):
        return "never_current"
    observed = str((claim.get("temporal") or {}).get("observed_at", ""))
    cadence = int(claim.get("cadence_days") or 90)
    try:
        age = (date.fromisoformat(ref) - date.fromisoformat(observed)).days
    except ValueError:
        return "fresh"
    r = age / cadence if cadence else 0
    return "fresh" if r <= 1 else "aging" if r <= 1.5 else "stale" if r <= 3 else "expired"


# ------------------------------------------------------------------ cost (D6)
D6_ANCHORS = [
    (0.00, 5, "dramatically cheaper than alternatives for equivalent work"),
    (25.00, 4, "good value; cost is not a factor in choosing it"),
    (75.00, 3, "fair; cost management required at volume"),
    (200.00, 2, "expensive enough to change how you work"),
    (500.00, 1, "cost is the reason not to use it"),
]


def score_d6(monthly_usd: float) -> tuple[int, str]:
    value, rationale = 1, D6_ANCHORS[-1][2]
    for threshold, v, r in D6_ANCHORS:
        if monthly_usd >= threshold:
            value, rationale = v, r
    return value, rationale


def monthly_cost(model: dict, profile: dict, ref: str, sources: dict) -> dict | None:
    ins = current_claims(model, "pricing.input_per_mtok", ref)
    outs = current_claims(model, "pricing.output_per_mtok", ref)
    if not ins or not outs:
        # some models carry a combined pricing.per_mtok claim
        combo = current_claims(model, "pricing.per_mtok", ref)
        # `value: unknown` is a legal published value (a known negative). It is
        # not a price, and the entity is correctly excluded from cost ranking.
        combo = [c for c in combo if isinstance(c.get("value"), dict)]
        if not combo:
            return None
        v = combo[0]["value"]
        p_in = v.get("input") or v.get("input_miss")
        p_out = v.get("output")
        claims = combo
    else:
        vi = ins[0].get("value")
        vo = outs[0].get("value")
        if not isinstance(vi, dict) or not isinstance(vo, dict):
            return None
        p_in = vi.get("amount")
        p_out = vo.get("amount")
        claims = ins + outs
    if p_in is None or p_out is None:
        return None

    cache_claims = current_claims(model, "pricing.cache_read_per_mtok", ref)
    p_cache = (cache_claims[0].get("value") or {}).get("amount") if cache_claims else p_in * 0.1

    hit = float(profile["cache_hit_rate"])
    tin = float(profile["tokens_in_month"])
    tout = float(profile["tokens_out_month"])
    retry = float(profile.get("retry_rate", 0.0))

    cost = (
        tin * (1 - hit) * p_in + tin * hit * p_cache + tout * p_out
    ) / 1_000_000 * (1 + retry)

    conf = [compute_confidence(c, sources) for c in claims]
    order = ["unknown", "low", "contested", "moderate", "high"]
    floor = min(conf, key=lambda c: order.index(c)) if conf else "unknown"

    return {
        "monthly_usd": round(cost, 2),
        "price_in": p_in,
        "price_out": p_out,
        "price_cache_read": p_cache,
        "pricing_confidence": floor,
        "evidence": [c["id"] for c in claims],
    }


# ------------------------------------------------------------------- engine
def recommend(ref: str, persona_id: str, budget: float | None) -> dict:
    graph = load_graph(ref)
    ents, sources = graph["entities"], graph["sources"]

    persona = _load(DATA / "personas" / f"{persona_id}.yaml")
    profiles = _load(DATA / "usage" / "usage-profiles.yaml")["profiles"]
    profile = next((p for p in profiles if p.get("persona") == persona_id), profiles[0])

    candidates, no_pricing = [], []
    for eid, e in ents.items():
        if "model" not in (e.get("slots") or []):
            continue
        c = monthly_cost(e, profile, ref, sources)
        if c is None:
            no_pricing.append(eid)
            continue
        d6, rationale = score_d6(c["monthly_usd"])
        candidates.append({
            "entity": eid, "name": e.get("name"), "cost": c,
            "scores": {"D6": {"value": d6, "rationale": rationale,
                              "confidence": c["pricing_confidence"],
                              "evidence": c["evidence"]}},
        })

    eliminated = []
    if budget is not None:
        before = len(candidates)
        candidates = [c for c in candidates if c["cost"]["monthly_usd"] <= budget]
        if before - len(candidates):
            eliminated.append({"constraint": f"budget_ceiling<={budget}",
                               "removed": before - len(candidates)})

    weights = persona["weights"]
    scored_dims = ["D6"]
    coverage = f"{len(scored_dims)}/{len(weights)} dimensions"

    for c in candidates:
        c["fit"] = round(
            sum(c["scores"][d]["value"] * weights[d] for d in scored_dims)
            / sum(weights[d] for d in scored_dims), 3
        )
    candidates.sort(key=lambda c: (-c["fit"], c["cost"]["monthly_usd"]))

    # band near-ties (ordinal scale: equal D6 == equal band)
    band = 0
    prev = None
    for c in candidates:
        if prev is None or c["fit"] != prev:
            band += 1
        c["rank_band"] = band
        prev = c["fit"]

    conf_floor = "unknown"
    order = ["unknown", "low", "contested", "moderate", "high"]
    if candidates:
        conf_floor = min(
            (c["scores"]["D6"]["confidence"] for c in candidates),
            key=lambda x: order.index(x),
        )
        # a cost answer can never exceed the confidence of its usage profile
        if profile.get("status") == "assumed":
            conf_floor = "low"

    result = {
        "reference_date": ref,
        "persona": persona_id,
        "usage_profile": {"id": profile["id"], "status": profile["status"],
                          "assumptions": profile["assumptions"][:2]},
        "coverage": coverage,
        "confidence": conf_floor,
        "eliminated": eliminated,
        "candidates_without_pricing": no_pricing,
        "result": "refusal" if len(scored_dims) < 6 else "recommendation",
        "refusal": None,
        "stacks": candidates,
    }

    if result["result"] == "refusal":
        result["refusal"] = {
            "code": "INSUFFICIENT_COVERAGE",
            "detail": (
                f"Ranked on {coverage}. RECOMMENDATION §10 requires >=6 of 13 "
                "scored dimensions before a stack recommendation may be issued."
            ),
            "resolves_with": [
                "Class B/C evidence for D1, D2, D4, D7 (EVIDENCE-ROADMAP streams 1-4)",
                "Measured usage profile (currently assumed) to raise cost confidence",
            ],
        }

    if candidates:
        top, runner = candidates[0], (candidates[1] if len(candidates) > 1 else None)
        result["explanation"] = {
            "why_won": [{
                "factor": "cost (D6)",
                "contribution": f"${top['cost']['monthly_usd']}/mo at the assumed profile",
                "marginal_effect": top["fit"],
            }],
            "assumptions": [
                {"assumption": "monthly token volume", "value":
                 f"{profile['tokens_in_month']:,} in / {profile['tokens_out_month']:,} out",
                 "source": "usage_profile", "editable": True},
                {"assumption": "cache hit rate", "value": profile["cache_hit_rate"],
                 "source": "usage_profile", "editable": True},
                {"assumption": "reference date", "value": ref,
                 "source": "query", "editable": True},
            ],
            "tradeoffs_accepted": (
                [{"gave_up": "unmeasured quality, autonomy and reliability",
                  "versus": runner["name"],
                  "magnitude": f"${abs(top['cost']['monthly_usd'] - runner['cost']['monthly_usd']):.2f}/mo cheaper, "
                               "but nothing else about it has been scored"}]
                if runner else []),
            "evidence": top["scores"]["D6"]["evidence"],
            "uncertainty": {
                "summary": "Ranked on cost alone, from an assumed usage profile. "
                           "Not a quality judgement.",
                "widest_distributions": ["all unscored dimensions"],
                "gaps": ["12 of 13 dimensions unscored", "usage profile assumed, not measured"],
            },
            "what_would_change_it": [
                {"input": "usage profile token volume", "threshold":
                 "any change scales all costs proportionally; ranking is volume-invariant",
                 "fragility": "robust"},
                {"input": "reference date", "threshold":
                 "prices with dated validity intervals change the ranking",
                 "fragility": "fragile"},
            ],
        }
    return result


def make_delta(a: dict, b: dict) -> dict:
    ra = {c["entity"]: c for c in a["stacks"]}
    rb = {c["entity"]: c for c in b["stacks"]}
    changes = []
    for eid in sorted(set(ra) | set(rb)):
        ca, cb = ra.get(eid), rb.get(eid)
        if ca and cb:
            if ca["cost"]["monthly_usd"] != cb["cost"]["monthly_usd"]:
                before, after = ca["cost"]["monthly_usd"], cb["cost"]["monthly_usd"]
                changes.append({
                    "entity": eid, "name": ca["name"], "change": "cost_changed",
                    "before_usd": before, "after_usd": after,
                    "pct": round((after - before) / before * 100, 1) if before else None,
                    "band_before": ca["rank_band"], "band_after": cb["rank_band"],
                    "d6_before": ca["scores"]["D6"]["value"],
                    "d6_after": cb["scores"]["D6"]["value"],
                })
        elif ca:
            changes.append({"entity": eid, "change": "dropped_out"})
        else:
            changes.append({"entity": eid, "change": "entered"})
    return {
        "delta_type": "reference_date",
        "from_date": a["reference_date"], "to_date": b["reference_date"],
        "order_before": [c["entity"] for c in a["stacks"]],
        "order_after": [c["entity"] for c in b["stacks"]],
        "order_changed": [c["entity"] for c in a["stacks"]] != [c["entity"] for c in b["stacks"]],
        "changes": [c for c in changes if c.get("change") != "cost_changed" or c["before_usd"] != c["after_usd"]],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", default="per-solo-founder")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--budget", type=float, default=None)
    ap.add_argument("--delta", nargs=2, metavar=("FROM", "TO"))
    a = ap.parse_args()

    if a.delta:
        r1 = recommend(a.delta[0], a.persona, a.budget)
        r2 = recommend(a.delta[1], a.persona, a.budget)
        print(json.dumps(make_delta(r1, r2), indent=2))
        return 0

    print(json.dumps(recommend(a.date, a.persona, a.budget), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
