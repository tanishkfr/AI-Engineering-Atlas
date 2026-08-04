"""exp-normalized-cost-v1  (RQ-01a)

NEW STUDY, not an amendment to exp-tokenizer-normalization-v1.

v1 measured tokenizers chosen for coverage. This study measures tokenizers for
the models we have CAPTURED PRICING FOR, so that price-per-normalized-token can
be computed. The candidate list is therefore different by design and is fixed by
the priced-model list, not chosen after seeing v1's results.

RQ-01 H3 established that within-vendor generational tokenizer drift can reach
~1.27x. Therefore a tokenizer from one model generation may NOT be substituted
for another generation of the same vendor. Only exact model matches count.

Run: python scripts/experiments/exp_normalized_cost.py
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = ROOT / "research" / "experiments" / "corpus"
OUT_DIR = ROOT / "research" / "experiments" / "results"

STRATA = [
    "code_python",
    "code_typescript",
    "prose_documentation",
    "structured_json",
    "mixed_repo_context",
]

# Models with pricing captured 2026-08-04 from DeepInfra (Class A, tool_extracted).
# tokenizer_repo is the EXACT repo for the priced model, or None if unavailable.
PRICED_MODELS = {
    "deepseek/DeepSeek-V3": {
        "tokenizer_repo": "deepseek-ai/DeepSeek-V3",
        "price_in": 0.32,
        "price_out": 0.89,
        "provider": "deepinfra",
        "match": "exact",
    },
    "qwen/Qwen3-32B": {
        "tokenizer_repo": "Qwen/Qwen3-32B",
        "price_in": 0.08,
        "price_out": 0.28,
        "provider": "deepinfra",
        "match": "exact",
    },
    "mistral/Mistral-Small-3.2-24B-Instruct-2506": {
        "tokenizer_repo": "mistralai/Mistral-Small-3.2-24B-Instruct-2506",
        "price_in": 0.075,
        "price_out": 0.20,
        "provider": "deepinfra",
        "match": "exact",
    },
    "mistral/Mistral-Nemo-Instruct-2407": {
        "tokenizer_repo": "mistralai/Mistral-Nemo-Instruct-2407",
        "price_in": 0.019,
        "price_out": 0.03,
        "provider": "deepinfra",
        "match": "exact",
    },
}

# OpenAI: pricing captured but the encoding used by the priced model is an
# ASSUMPTION, not documented. Recorded separately and flagged.
OPENAI_ASSUMED = {
    "openai/gpt-5.6-terra": {
        "encoding": "o200k_base",
        "price_in": 2.00,
        "price_out": 12.00,
        "provider": "openai-first-party",
        "match": "assumed_encoding",
    },
    "openai/gpt-5.6-sol": {
        "encoding": "o200k_base",
        "price_in": 5.00,
        "price_out": 30.00,
        "provider": "openai-first-party",
        "match": "assumed_encoding",
    },
}

# Vendors that cannot enter a normalized comparison at all.
NOT_NORMALIZABLE = {
    "anthropic": "No public offline tokenizer; count_tokens requires an API key.",
    "google": "No public offline tokenizer; countTokens requires an API key.",
}


def load_corpus() -> dict[str, dict]:
    out = {}
    for name in STRATA:
        raw = (CORPUS_DIR / f"{name}.txt").read_bytes()
        out[name] = {
            "text": raw.decode("utf-8"),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    return out


def pkg_version(name: str) -> str:
    try:
        import importlib.metadata as md

        return md.version(name)
    except Exception:  # noqa: BLE001
        return "unknown"


def main() -> int:
    corpus = load_corpus()
    counts: dict[str, dict[str, int]] = {}
    meta: dict[str, dict] = {}
    failures: dict[str, str] = {}

    from tokenizers import Tokenizer

    for label, spec in PRICED_MODELS.items():
        repo = spec["tokenizer_repo"]
        try:
            tok = Tokenizer.from_pretrained(repo)
            counts[label] = {
                s: len(tok.encode(corpus[s]["text"], add_special_tokens=False).ids)
                for s in STRATA
            }
            meta[label] = {**spec, "tokenizer_loaded": True}
        except Exception as ex:  # noqa: BLE001
            failures[label] = f"{type(ex).__name__}: {str(ex)[:180]}"

    import tiktoken

    for label, spec in OPENAI_ASSUMED.items():
        try:
            enc = tiktoken.get_encoding(spec["encoding"])
            counts[label] = {s: len(enc.encode(corpus[s]["text"])) for s in STRATA}
            meta[label] = {**spec, "tokenizer_loaded": True}
        except Exception as ex:  # noqa: BLE001
            failures[label] = f"{type(ex).__name__}: {str(ex)[:180]}"

    # --- Normalized cost ---
    # Cost to process each stratum ONCE, in USD, using that model's own tokenizer.
    # This is the whole point: price x actual tokens for identical work.
    normalized_cost = {}
    for label in counts:
        spec = meta[label]
        normalized_cost[label] = {
            s: round(counts[label][s] * spec["price_in"] / 1_000_000, 8) for s in STRATA
        }

    # Naive comparison: what you'd conclude from posted price alone, assuming
    # every vendor's tokens are equivalent. Uses the cheapest model's token count
    # as a stand-in for "tokens" as a universal unit.
    naive_ranking = sorted(meta, key=lambda l: meta[l]["price_in"])
    normalized_ranking = {
        s: sorted(counts, key=lambda l: normalized_cost[l][s]) for s in STRATA
    }

    ranking_changed = {
        s: normalized_ranking[s] != naive_ranking for s in STRATA
    }

    # Effective token multiplier vs the most token-efficient priced model
    multipliers = {}
    for s in STRATA:
        best = min(counts, key=lambda l: counts[l][s])
        multipliers[s] = {
            l: round(counts[l][s] / counts[best][s], 4) for l in counts
        }

    result = {
        "experiment": "exp-normalized-cost-v1",
        "study": "RQ-01a",
        "note": (
            "New study. Candidate list fixed by which models we have captured "
            "pricing for, not chosen after seeing exp-tokenizer-normalization-v1 "
            "results. Only exact tokenizer/model matches admitted; RQ-01 H3 "
            "showed within-vendor generational drift up to 1.27x, so tokenizers "
            "are not substituted across generations."
        ),
        "run_date": date.today().isoformat(),
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "tiktoken": pkg_version("tiktoken"),
            "tokenizers": pkg_version("tokenizers"),
        },
        "pricing_source": "src-deepinfra-pricing-2026-08-04 (Class A, tool_extracted); "
                          "src-openai-pricing-2026-08-03 (Class A, tool_extracted)",
        "pricing_as_of": "2026-08-04",
        "corpus": {s: {"bytes": corpus[s]["bytes"], "sha256": corpus[s]["sha256"]} for s in STRATA},
        "models_measured": meta,
        "models_failed": failures,
        "not_normalizable": NOT_NORMALIZABLE,
        "token_counts": counts,
        "normalized_cost_usd_per_pass": normalized_cost,
        "effective_token_multiplier": multipliers,
        "naive_price_ranking": naive_ranking,
        "normalized_cost_ranking": normalized_ranking,
        "ranking_changed_by_normalization": ranking_changed,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "normalized-cost-v1.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
