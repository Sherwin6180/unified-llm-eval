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
        url = f"https://huggingface.co/{hf_repo}/raw/main/config.json"
        # Prefer requests if available; fallback to urllib
        try:
            import requests  # type: ignore
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception:
            try:
                import json as _json
                from urllib.request import urlopen
                with urlopen(url, timeout=15) as resp:
                    return _json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                raise FileNotFoundError(f"Failed to fetch config.json from {url}: {e}")
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


def is_per_layer_component(name: str) -> bool:
    return name not in {"embed_tokens", "lm_head", "final_norm"}


def bytes_per_param(dtype: str) -> float:
    d = dtype.lower()
    if d in ("bf16", "bfloat16", "fp16", "float16"):  # 16-bit
        return 2.0
    if d in ("fp32", "float32"):  # 32-bit
        return 4.0
    if d in ("fp8", "e4m3", "int8", "uint8"):  # 8-bit
        return 1.0
    if d in ("nf4", "q4", "int4", "fp4"):  # 4-bit
        return 0.5
    # Default to bf16
    return 2.0


def human_bytes(num_bytes: float) -> str:
    gb = num_bytes / (1024 ** 3)
    if gb >= 1.0:
        return f"{gb:.2f} GiB"
    mb = num_bytes / (1024 ** 2)
    return f"{mb:.2f} MiB"


def per_layer_param_count(component: str, counts: dict) -> int:
    L = int(counts["_dims"]["L"]) if "_dims" in counts else 1
    total = counts[component]
    return total // L if L > 0 and is_per_layer_component(component) else total


PRESETS = {
    # All per-layer components (attention + MLP + both LNs). No non-layer by default.
    "full": [
        "self_attn.q_proj",
        "self_attn.k_proj",
        "self_attn.v_proj",
        "self_attn.o_proj",
        "mlp.gate_proj",
        "mlp.up_proj",
        "mlp.down_proj",
        "input_layernorm",
        "post_attention_layernorm",
    ],
    # Attention only (q, k, v, o)
    "attn_only": [
        "self_attn.q_proj",
        "self_attn.k_proj",
        "self_attn.v_proj",
        "self_attn.o_proj",
    ],
    # Attention + MLP (common selective merge)
    "attn_mlp": [
        "self_attn.q_proj",
        "self_attn.k_proj",
        "self_attn.v_proj",
        "self_attn.o_proj",
        "mlp.gate_proj",
        "mlp.up_proj",
        "mlp.down_proj",
    ],
    # Alias for your preferred/best setting; maps to attn_mlp by default
    "best_setting": [
        "self_attn.q_proj",
        "self_attn.k_proj",
        "self_attn.v_proj",
        "self_attn.o_proj",
        "mlp.gate_proj",
        "mlp.up_proj",
        "mlp.down_proj",
    ],
}


PRESET_ORDER = ["full", "attn_only", "attn_mlp", "best_setting"]


def resolve_selected_components(preset: str | None, component_ids: list[int] | None) -> list[str]:
    if preset:
        return PRESETS[preset]
    if component_ids:
        selected = []
        for idx in component_ids:
            if 0 <= idx < len(COMPONENTS):
                selected.append(COMPONENTS[idx])
        return selected
    # Default to full per-layer set if nothing provided
    return PRESETS["full"]


def compute_delta_params(counts: dict, layers_to_merge: int, selected_components: list[str], include_non_layer: list[str]) -> int:
    L = int(counts["_dims"]["L"]) if "_dims" in counts else 1
    layers = max(0, min(int(layers_to_merge), L))

    delta = 0
    # Per-layer components
    for name in selected_components:
        if is_per_layer_component(name):
            delta += per_layer_param_count(name, counts) * layers
    # Non-layer components (merged once when included)
    for name in include_non_layer:
        if name in {"embed_tokens", "lm_head", "final_norm"}:
            delta += counts[name]
    return int(delta)


def main():
    parser = argparse.ArgumentParser(description="Print parameter counts and memory savings for selective merges (LLaMA-like models).")
    parser.add_argument("--model_dir", type=str, default=None, help="Local model directory containing config.json (preferred).")
    parser.add_argument("--hf_repo", type=str, default="deepseek-ai/deepseek-coder-7b-instruct-v1.5", help="HF repo id to fetch config.json if local config is not available.")
    # Savings options
    parser.add_argument("--dtype", type=str, default="bf16", choices=[
        "bf16", "bfloat16", "fp16", "float16", "fp32", "float32", "fp8", "int8", "nf4", "q4", "int4", "fp4"
    ], help="Precision to use when estimating bytes per parameter.")
    parser.add_argument("--merge_layers", type=int, nargs="+", default=None, help="Layer counts to merge (e.g., 10 15 20). Uses min(L, value).")
    parser.add_argument("--preset", type=str, choices=(list(PRESETS.keys()) + ["all"]), default=None, help="Preset component selection for per-layer merges. Use 'all' to print all presets.")
    parser.add_argument("--component_ids", type=int, nargs="+", default=None, help="Explicit component indices to include (overrides --preset).")
    parser.add_argument("--non_layer", type=str, nargs="*", default=None, choices=["embed_tokens", "lm_head", "final_norm", "all", "none"], help="Non-layer components to include once globally.")
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

    # If user asked for savings, compute and print
    if args.merge_layers:
        # Resolve non-layer includes (applies to all presets equally)
        non_layer_selection: list[str] = []
        if args.non_layer:
            if "all" in args.non_layer:
                non_layer_selection = ["embed_tokens", "lm_head", "final_norm"]
            elif "none" in args.non_layer:
                non_layer_selection = []
            else:
                non_layer_selection = [x for x in args.non_layer if x in {"embed_tokens", "lm_head", "final_norm"}]

        bpp = bytes_per_param(args.dtype)
        total_bytes = total * bpp

        # Decide which presets to print
        if args.preset == "all" and not args.component_ids:
            print("\nSavings vs storing a full second model (same dtype) — all presets:")
            hdr = f"{'Preset':<15} {'Layers':>8}  {'Delta Params':>15}  {'Delta Size':>12}  {'Full Size':>12}  {'Savings':>9}"
            print(hdr)
            print("-" * len(hdr))
            for preset_name in PRESET_ORDER:
                selected_components = PRESETS[preset_name]
                for layers in args.merge_layers:
                    delta_params = compute_delta_params(counts, layers, selected_components, non_layer_selection)
                    delta_bytes = delta_params * bpp
                    savings = (delta_bytes / (2.0 * total_bytes)) if total_bytes > 0 else 0.0
                    print(f"{preset_name:<15} {int(layers):>8}  {delta_params:>15,}  {human_bytes(delta_bytes):>12}  {human_bytes(total_bytes):>12}  {savings*100:>8.2f}%")
        else:
            # Single preset or explicit component_ids
            selected_components = resolve_selected_components(args.preset, args.component_ids)
            print("\nSavings vs storing a full second model (same dtype):")
            hdr = f"{'Layers':>8}  {'Delta Params':>15}  {'Delta Size':>12}  {'Full Size':>12}  {'Savings':>9}"
            print(hdr)
            print("-" * len(hdr))
            for layers in args.merge_layers:
                delta_params = compute_delta_params(counts, layers, selected_components, non_layer_selection)
                delta_bytes = delta_params * bpp
                savings = (delta_bytes / (2.0 * total_bytes)) if total_bytes > 0 else 0.0
                print(f"{int(layers):>8}  {delta_params:>15,}  {human_bytes(delta_bytes):>12}  {human_bytes(total_bytes):>12}  {savings*100:>8.2f}%")


if __name__ == "__main__":
    main()
