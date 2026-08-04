"""exp-tokenizer-normalization-v1

Executes the preregistered protocol in
research/experiments/PREREG-exp-tokenizer-normalization-v1.md

Deterministic. No inference. No API keys. No random seeds.

Run: python scripts/experiments/exp_tokenizer_normalization.py
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

# Fixed candidate list — preregistered, not extended after seeing results.
TIKTOKEN_ENCODINGS = {
    "openai/o200k_base": "o200k_base",
    "openai/cl100k_base": "cl100k_base",
    "openai/p50k_base": "p50k_base",
}
HF_TOKENIZERS = {
    "qwen/Qwen2.5-Coder-7B-Instruct": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "deepseek/DeepSeek-V3": "deepseek-ai/DeepSeek-V3",
    "mistral/Mistral-7B-Instruct-v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
    "meta/Llama-3.1-8B-Instruct": "meta-llama/Llama-3.1-8B-Instruct",
}

REFERENCE = "openai/cl100k_base"  # declared in prereg §9, before running

# Vendors with no offline tokenizer — excluded, NOT estimated (prereg §6).
NOT_NORMALIZABLE = {
    "anthropic": "No public offline tokenizer. Counts require the count_tokens "
                 "API endpoint, which requires an API key.",
    "google": "No public offline tokenizer for Gemini. Counts require the "
              "countTokens API endpoint, which requires an API key.",
}


def load_corpus() -> dict[str, dict]:
    corpus = {}
    for name in STRATA:
        path = CORPUS_DIR / f"{name}.txt"
        raw = path.read_bytes()
        corpus[name] = {
            "text": raw.decode("utf-8"),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    return corpus


def pkg_version(name: str) -> str:
    try:
        import importlib.metadata as md

        return md.version(name)
    except Exception:  # noqa: BLE001
        return "unknown"


def main() -> int:
    corpus = load_corpus()
    counts: dict[str, dict[str, int]] = {}
    tokenizer_meta: dict[str, dict] = {}
    failures: dict[str, str] = {}

    # --- OpenAI via tiktoken ---
    import tiktoken

    for label, enc_name in TIKTOKEN_ENCODINGS.items():
        try:
            enc = tiktoken.get_encoding(enc_name)
            counts[label] = {s: len(enc.encode(corpus[s]["text"])) for s in STRATA}
            tokenizer_meta[label] = {"backend": "tiktoken", "encoding": enc_name}
        except Exception as ex:  # noqa: BLE001
            failures[label] = f"{type(ex).__name__}: {str(ex)[:200]}"

    # --- Open-weight vendors via HuggingFace ---
    from tokenizers import Tokenizer

    for label, repo in HF_TOKENIZERS.items():
        try:
            tok = Tokenizer.from_pretrained(repo)
            counts[label] = {
                s: len(tok.encode(corpus[s]["text"], add_special_tokens=False).ids)
                for s in STRATA
            }
            tokenizer_meta[label] = {"backend": "tokenizers", "repo": repo}
        except Exception as ex:  # noqa: BLE001
            failures[label] = f"{type(ex).__name__}: {str(ex)[:200]}"

    # --- Derived measures ---
    tokens_per_kb = {
        label: {s: round(counts[label][s] / (corpus[s]["bytes"] / 1000), 2) for s in STRATA}
        for label in counts
    }

    ratios = {}
    if REFERENCE in counts:
        ratios = {
            label: {s: round(counts[label][s] / counts[REFERENCE][s], 4) for s in STRATA}
            for label in counts
        }

    spread = {}
    for s in STRATA:
        vals = [counts[label][s] for label in counts]
        if vals:
            spread[s] = {
                "min": min(vals),
                "max": max(vals),
                "ratio": round(max(vals) / min(vals), 4),
                "argmin": min(counts, key=lambda l: counts[l][s]),
                "argmax": max(counts, key=lambda l: counts[l][s]),
            }

    # --- Preregistered hypothesis tests ---
    code_strata = ["code_python", "code_typescript"]
    prose_strata = ["prose_documentation"]
    code_spread = max(spread[s]["ratio"] for s in code_strata) if spread else None
    prose_spread = max(spread[s]["ratio"] for s in prose_strata) if spread else None

    # H3: within-vendor (OpenAI generations) vs cross-vendor
    openai_labels = [l for l in counts if l.startswith("openai/")]
    within_vendor = {}
    for s in STRATA:
        vals = [counts[l][s] for l in openai_labels]
        if len(vals) > 1:
            within_vendor[s] = round(max(vals) / min(vals), 4)

    hypotheses = {
        "H1_code_spread_exceeds_1.20": {
            "threshold": 1.20,
            "observed_max_code_spread": code_spread,
            "supported": bool(code_spread and code_spread > 1.20),
        },
        "H2_code_spread_greater_than_prose": {
            "observed_code": code_spread,
            "observed_prose": prose_spread,
            "supported": bool(code_spread and prose_spread and code_spread > prose_spread),
        },
        "H3_within_vendor_less_than_cross_vendor": {
            "within_vendor_max": max(within_vendor.values()) if within_vendor else None,
            "cross_vendor_max": max(v["ratio"] for v in spread.values()) if spread else None,
            "supported": bool(
                within_vendor
                and spread
                and max(within_vendor.values()) < max(v["ratio"] for v in spread.values())
            ),
        },
    }

    result = {
        "experiment": "exp-tokenizer-normalization-v1",
        "preregistration": "research/experiments/PREREG-exp-tokenizer-normalization-v1.md",
        "run_date": date.today().isoformat(),
        "reference_tokenizer": REFERENCE,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "tiktoken": pkg_version("tiktoken"),
            "tokenizers": pkg_version("tokenizers"),
            "transformers": pkg_version("transformers"),
        },
        "corpus": {s: {"bytes": corpus[s]["bytes"], "sha256": corpus[s]["sha256"]} for s in STRATA},
        "tokenizers_measured": tokenizer_meta,
        "tokenizers_failed": failures,
        "not_normalizable": NOT_NORMALIZABLE,
        "token_counts": counts,
        "tokens_per_1000_bytes": tokens_per_kb,
        "ratio_vs_reference": ratios,
        "cross_vendor_spread": spread,
        "within_vendor_spread_openai": within_vendor,
        "hypotheses": hypotheses,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "tokenizer-normalization-v1.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"\nWritten to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
