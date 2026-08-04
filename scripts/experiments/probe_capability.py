"""Capability probe for RQ-01 / RQ-07.

Determines which vendor tokenizers are reachable in this environment BEFORE the
protocol is finalized. This is capability scoping, not data collection: it
records what CAN be measured, not what the measurements are.

Run: python scripts/experiments/probe_capability.py
"""
import json
import sys

result = {"python": sys.version.split()[0], "tiktoken": {}, "hf": {}, "notes": []}

# --- OpenAI: tiktoken ships encodings; may need network on first use ---
try:
    import tiktoken

    result["tiktoken"]["version"] = getattr(tiktoken, "__version__", "unknown")
    result["tiktoken"]["encodings_listed"] = tiktoken.list_encoding_names()
    for enc_name in ("o200k_base", "cl100k_base", "p50k_base"):
        try:
            enc = tiktoken.get_encoding(enc_name)
            n = len(enc.encode("def hello():\n    return 1\n"))
            result["tiktoken"][enc_name] = {"loadable": True, "sample_tokens": n}
        except Exception as ex:  # noqa: BLE001
            result["tiktoken"][enc_name] = {
                "loadable": False,
                "error": f"{type(ex).__name__}: {str(ex)[:200]}",
            }
except Exception as ex:  # noqa: BLE001
    result["tiktoken"]["error"] = f"{type(ex).__name__}: {str(ex)[:200]}"

# --- Open-weight vendors: HuggingFace tokenizers require network ---
HF_CANDIDATES = [
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "deepseek-ai/DeepSeek-V3",
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
]
try:
    from tokenizers import Tokenizer

    for repo in HF_CANDIDATES:
        try:
            tok = Tokenizer.from_pretrained(repo)
            n = len(tok.encode("def hello():\n    return 1\n").ids)
            result["hf"][repo] = {"loadable": True, "sample_tokens": n}
        except Exception as ex:  # noqa: BLE001
            result["hf"][repo] = {
                "loadable": False,
                "error": f"{type(ex).__name__}: {str(ex)[:200]}",
            }
except Exception as ex:  # noqa: BLE001
    result["hf"]["error"] = f"{type(ex).__name__}: {str(ex)[:200]}"

# --- Vendors with NO public tokenizer library ---
result["notes"].append(
    "Anthropic publishes no offline tokenizer. Token counts require the "
    "count_tokens API endpoint, which needs an API key."
)
result["notes"].append(
    "Google publishes no offline tokenizer for Gemini. Token counts require the "
    "countTokens API endpoint, which needs an API key."
)

print(json.dumps(result, indent=2))
