#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path

# Component mapping (indices are not required here, but types match merge_pipeline)
COMPONENTS = [
    "self_attn.q_proj",  # 0
    "self_attn.k_proj",  # 1
    "self_attn.v_proj",  # 2
    "self_attn.o_proj",  # 3
    "mlp.gate_proj",     # 4
    "mlp.up_proj",       # 5
    "mlp.down_proj",     # 6
    "input_layernorm",   # 7
    "post_attention_layernorm",  # 8
    "embed_tokens",      # 9 (non-layer)
    "lm_head",           # 10 (non-layer)
    "final_norm",        # 11 (non-layer)
]


def load_config(model_dir: str | None, hf_repo: str | None) -> dict:
    # Try local first if provided
    if model_dir:
        cfg_path = Path(model_dir) / "config.json"
        if cfg_path.exists():
            with open(cfg_path, "r") as f:
                return json.load(f)
    # Fallback to HF raw config if repo provided
    if hf_repo:
        import requests
        url = f"https://huggingface.co/{hf_repo}/raw/main/config.json"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    raise FileNotFoundError("Could not locate config.json locally and no HF repo provided.")


def pick(cfg: dict, *keys, default=None):
    for k in keys:
        if k in cfg:
            return cfg[k]
    return default


def compute_counts(cfg: dict) -> dict:
    # Extract core dims (robust to different key names)
    L = int(pick(cfg, 'num_hidden_layers', 'n_layer'))
    H = int(pick(cfg, 'hidden_size', 'n_embd', 'hidden_dim'))
    I = int(pick(cfg, 'intermediate_size', 'ffn_dim'))
    V = int(pick(cfg, 'vocab_size'))

    # Attention linear projections: (H, H) per layer
    def attn_lin():
        return L * H * H

    # MLP: gate/up are (I, H); down is (H, I) per layer
    def gate_up():
        return L * I * H

    def down():
        return L * H * I

    # LayerNorms: (H,) per layer
    def ln():
        return L * H

    # Non-layer components
    embed_tokens = V * H
    lm_head = V * H
    final_norm = H

    return {
        'self_attn.q_proj': attn_lin(),
        'self_attn.k_proj': attn_lin(),
        'self_attn.v_proj': attn_lin(),
        'self_attn.o_proj': attn_lin(),
        'mlp.gate_proj': gate_up(),
        'mlp.up_proj': gate_up(),
        'mlp.down_proj': down(),
        'input_layernorm': ln(),
        'post_attention_layernorm': ln(),
        'embed_tokens': embed_tokens,
        'lm_head': lm_head,
        'final_norm': final_norm,
        '_dims': {'L': L, 'H': H, 'I': I, 'V': V},
    }


def main():
    parser = argparse.ArgumentParser(description="Print parameter counts per component type for DeepSeek Coder 7B (or any LLaMA-like model).")
    parser.add_argument("--model_dir", type=str, default=None, help="Local model directory containing config.json (preferred).")
    parser.add_argument("--hf_repo", type=str, default="deepseek-ai/deepseek-coder-7b-instruct-v1.5", help="HF repo id to fetch config.json if local config is not available.")
    args = parser.parse_args()

    cfg = load_config(args.model_dir, args.hf_repo)
    counts = compute_counts(cfg)

    L, H, I, V = counts['_dims']['L'], counts['_dims']['H'], counts['_dims']['I'], counts['_dims']['V']
    print(f"Model dims: L={L} H={H} I={I} V={V}")

    # Pretty print
    order = COMPONENTS
    width = max(len(k) for k in order) + 2
    total = 0
    for k in order:
        n = counts[k]
        total += n
        print(f"{k.ljust(width)} {n:,}")
    print(f"{'TOTAL (components listed)':<{width}} {total:,}")


if __name__ == "__main__":
    main()
