import yaml
import os
import argparse
import subprocess
import tempfile
import json
import random
import textwrap
from transformers import AutoConfig
import torch
from mergekit.config import MergeConfiguration
from mergekit.merge import MergeOptions, run_merge

COMPONENT_MAPPING = {
    # Attention components (per-layer)
    "self_attn.q_proj": 0, "self_attn.k_proj": 1, "self_attn.v_proj": 2, "self_attn.o_proj": 3,
    # MLP components (per-layer)
    "mlp.gate_proj": 4, "mlp.up_proj": 5, "mlp.down_proj": 6,
    # Layer norms (per-layer)
    "input_layernorm": 7, "post_attention_layernorm": 8,
    # Non-layer components
    "embed_tokens": 9, "lm_head": 10, "final_norm": 11,
}

# Components that are not tied to per-layer modules
NON_LAYER_COMPONENT_NAMES = {"embed_tokens", "lm_head", "final_norm"}

def normalize_merge_method(method_str):
    """Normalize user-provided merge method aliases to canonical values.

    Supported canonical values: 'slerp', 'nuslerp', 'della', 'dare_ties'.
    Accepted aliases (case-insensitive): 'NuSLERP' -> 'nuslerp',
    'DELLA' -> 'della', 'DARE+TIES'/'DARE TIES'/'dareties' -> 'dare_ties'.
    """
    if method_str is None:
        return 'slerp'
    s = str(method_str).strip()
    s_lower = s.lower().replace('+', '_').replace('-', '_').replace(' ', '_')
    # Compact form for fuzzy matching like dareties
    compact = s_lower.replace('_', '')

    if s_lower in ('slerp',):
        return 'slerp'
    if s_lower in ('nuslerp', 'nu_slerp'):
        return 'nuslerp'
    if s_lower in ('della',):
        return 'della'
    if s_lower in ('dare_ties',) or compact == 'dareties':
        return 'dare_ties'
    if s_lower in ('model_stock',):
        return 'model_stock'

    raise ValueError(f"Unsupported merge method '{method_str}'. Supported: slerp, NuSLERP, DELLA, DARE+TIES, model_stock")

def get_num_layers(model_identifier):
    """Fetches the number of layers for a model from a local path or Hugging Face Hub."""
    try:
        config = AutoConfig.from_pretrained(model_identifier)
        if hasattr(config, 'num_hidden_layers'):
            return config.num_hidden_layers
        else:
            raise ValueError(f"Could not find 'num_hidden_layers' in the config for '{model_identifier}'.")
    except Exception as e:
        print(f"Could not load model config from '{model_identifier}': {e}")
        return None

def show_model_properties(model_identifier):
    """
    Loads and prints the configuration of a local or Hub model.
    """
    print(f"Attempting to load configuration from: {model_identifier}")
    try:
        config = AutoConfig.from_pretrained(model_identifier)
        config_dict = config.to_dict()
        
        print("\n--- Model Properties ---")
        print(json.dumps(config_dict, indent=2))
        print("--- End of Properties ---")

    except Exception as e:
        print(f"--> Error: An exception occurred while trying to load the configuration: {e}")

def create_single_layer_swap_config(
    layer_num,
    base_model,
    model_to_merge,
    num_layers,
    t_value=0.5,
    merge_method='slerp',
    tokenizer_source='union',
    chat_template='auto',
    normalize=True,
):
    """
    Creates a YAML config to swap a single layer from model_to_merge into base_model.
    """
    if merge_method not in ('slerp', 'nuslerp'):
        raise ValueError("Single-layer swap supports only SLERP/NuSLERP. Use --merge_method slerp or nuslerp.")
    method_for_config = 'slerp' if merge_method in ('slerp', 'nuslerp') else merge_method
    method_for_config = 'nuslerp' if merge_method == 'nuslerp' else 'slerp'
    cfg = {
        'merge_method': method_for_config,
        'base_model': base_model,
        'dtype': 'bfloat16',
        'tokenizer_source': tokenizer_source,
        'chat_template': chat_template,
        'slices': [
            {
                'sources': [
                    {'model': base_model, 'layer_range': [0, layer_num]},
                    {'model': model_to_merge, 'layer_range': [0, layer_num]}
                ],
                'parameters': {'t': [{'value': 0}]}
            },
            {
                'sources': [
                    {'model': base_model, 'layer_range': [layer_num, layer_num + 1]},
                    {'model': model_to_merge, 'layer_range': [layer_num, layer_num + 1]}
                ],
                'parameters': {'t': [{'value': t_value}]}
            },
            {
                'sources': [
                    {'model': base_model, 'layer_range': [layer_num + 1, num_layers]},
                    {'model': model_to_merge, 'layer_range': [layer_num + 1, num_layers]}
                ],
                'parameters': {'t': [{'value': 0}]}
            }
        ]
    }
    # Ensure normalize top-level parameter is present for all configs
    if method_for_config == 'nuslerp':
        cfg['parameters'] = {'normalize': bool(normalize)}
    else:
        cfg['parameters'] = {'normalize': bool(normalize)}
    return cfg

def create_windowed_merge_config(
    start_layer,
    window_size,
    base_model,
    model_to_merge,
    num_layers,
    t_value=0.5,
    merge_method='slerp',
    tokenizer_source='union',
    chat_template='auto',
    normalize=True,
):
    """
    Creates a YAML config to merge a 'window' of layers from model_to_merge into base_model.
    """
    end_layer = min(start_layer + window_size, num_layers)

    if merge_method not in ('slerp', 'nuslerp'):
        raise ValueError("Windowed sweep supports only SLERP/NuSLERP. Use --merge_method slerp or nuslerp.")
    method_for_config = 'slerp' if merge_method in ('slerp', 'nuslerp') else merge_method

    method_for_config = 'nuslerp' if merge_method == 'nuslerp' else 'slerp'
    cfg = {
        'merge_method': method_for_config,
        'base_model': base_model,
        'dtype': 'bfloat16',
        'tokenizer_source': tokenizer_source,
        'chat_template': chat_template,
        'slices': [
            {
                'sources': [
                    {'model': base_model, 'layer_range': [0, start_layer]},
                    {'model': model_to_merge, 'layer_range': [0, start_layer]}
                ],
                'parameters': {'t': [{'value': 0}]}
            },
            {
                'sources': [
                    {'model': base_model, 'layer_range': [start_layer, end_layer]},
                    {'model': model_to_merge, 'layer_range': [start_layer, end_layer]}
                ],
                'parameters': {'t': [{'value': t_value}]}
            },
            {
                'sources': [
                    {'model': base_model, 'layer_range': [end_layer, num_layers]},
                    {'model': model_to_merge, 'layer_range': [end_layer, num_layers]}
                ],
                'parameters': {'t': [{'value': 0}]}
            }
        ]
    }
    # Ensure normalize top-level parameter is present for all configs
    cfg['parameters'] = {'normalize': bool(normalize)}
    return cfg

def create_full_merge_config(
    base_model,
    model_to_merge,
    num_layers,
    t_value=0.5,
    merge_method='slerp',
    density=0.5,
    model_a=None,
    model_b=None,
    model_weights=None,
    tokenizer_source='union',
    chat_template='auto',
    normalize=True,
    model_stock_filter_wise=False,
):
    """
    Creates a YAML config for a full merge of all layers.
    """
    if merge_method in ('slerp', 'nuslerp'):
        # For NuSLERP, prefer models-style config when two explicit models are provided
        if merge_method == 'nuslerp' and model_a and model_b:
            weights = model_weights if model_weights is not None else [0.5, 0.5]
            return {
                'merge_method': 'nuslerp',
                'base_model': base_model,
                'dtype': 'bfloat16',
                'tokenizer_source': tokenizer_source,
                'chat_template': chat_template,
                'models': [
                    {'model': model_a, 'parameters': {'weight': float(weights[0])}},
                    {'model': model_b, 'parameters': {'weight': float(weights[1])}},
                ],
                'parameters': {'normalize': bool(normalize)},
            }
        # Fallback to slice-based two-model interpolation using t_value
        method_for_config = 'slerp'
        cfg = {
            'merge_method': method_for_config,
            'base_model': base_model,
            'dtype': 'bfloat16',
            'tokenizer_source': tokenizer_source,
            'chat_template': chat_template,
            'slices': [
                {
                    'sources': [
                        {'model': base_model, 'layer_range': [0, num_layers]},
                        {'model': model_to_merge, 'layer_range': [0, num_layers]}
                    ],
                    'parameters': {'t': [{'value': t_value}]}
                }
            ]
        }
        # Ensure normalize top-level parameter is present for all configs
        cfg['parameters'] = {'normalize': bool(normalize)}
        return cfg
    elif merge_method in ('della', 'dare_ties'):
        # For task arithmetic methods, require two source models; base_model stays separate
        if not (model_a and model_b):
            raise ValueError("For 'della' and 'dare_ties', you must provide --model_a and --model_b.")
        weights = model_weights if model_weights is not None else [0.5, 0.5]
        return {
            'models': [
                {
                    'model': model_a,
                    'parameters': {
                        'weight': float(weights[0]),
                        'density': float(density),
                    },
                },
                {
                    'model': model_b,
                    'parameters': {
                        'weight': float(weights[1]),
                        'density': float(density),
                    },
                },
            ],
            'merge_method': merge_method,
            'base_model': base_model,
            'dtype': 'bfloat16',
            'tokenizer_source': tokenizer_source,
            'chat_template': chat_template,
        }
    elif merge_method == 'model_stock':
        # Model Stock requires a base model and at least two other models
        if not (model_a and model_b):
            raise ValueError("For 'model_stock', you must provide --model_a and --model_b.")
        return {
            'base_model': base_model,
            'merge_method': 'model_stock',
            'models': [
                # For model_stock, models are specified without parameters like weight/density
                {'model': model_a},
                {'model': model_b},
            ],
            'dtype': 'bfloat16',
            'tokenizer_source': tokenizer_source,
            'chat_template': chat_template,
            'parameters': {'filter_wise': bool(model_stock_filter_wise)},
        }
    else:
        raise ValueError(f"Unsupported merge method: {merge_method}")

def create_random_layers_merge_config(
    layers_to_merge,
    base_model,
    model_to_merge,
    num_layers,
    t_value=0.5,
    merge_method='slerp',
    tokenizer_source='union',
    chat_template='auto',
    normalize=True,
):
    """
    Creates a YAML config to merge a specific set of layers from model_to_merge into base_model.
    """
    if merge_method not in ('slerp', 'nuslerp'):
        raise ValueError("Random layer merge supports only SLERP/NuSLERP. Use --merge_method slerp or nuslerp.")
    method_for_config = 'slerp' if merge_method in ('slerp', 'nuslerp') else merge_method

    layers_to_merge = sorted(list(set(layers_to_merge)))
    
    slices = []
    current_layer = 0
    
    for layer in layers_to_merge:
        # Part with base model layers
        if layer > current_layer:
            slices.append({
                'sources': [
                    {'model': base_model, 'layer_range': [current_layer, layer]},
                    {'model': model_to_merge, 'layer_range': [current_layer, layer]}
                ],
                'parameters': {'t': [{'value': 0}]}
            })
        
        # The layer to merge
        slices.append({
            'sources': [
                {'model': base_model, 'layer_range': [layer, layer + 1]},
                {'model': model_to_merge, 'layer_range': [layer, layer + 1]}
            ],
            'parameters': {'t': [{'value': t_value}]}
        })
        current_layer = layer + 1
        
    # Remaining layers from base model
    if current_layer < num_layers:
        slices.append({
            'sources': [
                {'model': base_model, 'layer_range': [current_layer, num_layers]},
                {'model': model_to_merge, 'layer_range': [current_layer, num_layers]}
            ],
            'parameters': {'t': [{'value': 0}]}
        })

    method_for_config = 'nuslerp' if merge_method == 'nuslerp' else 'slerp'
    cfg = {
        'merge_method': method_for_config,
        'base_model': base_model,
        'dtype': 'bfloat16',
        'tokenizer_source': tokenizer_source,
        'chat_template': chat_template,
        'slices': slices
    }
    # Ensure normalize top-level parameter is present for all configs
    cfg['parameters'] = {'normalize': bool(normalize)}
    return cfg

def create_selective_merge_config(
    base_model,
    model_to_merge,
    component_names,
    num_layers,
    t_value=0.5,
    merge_method='slerp',
    density=0.5,
    tokenizer_source='union',
    chat_template='auto',
    normalize=True,
    model_a=None,
    model_b=None,
    model_weights=None,
    unfiltered_source='base',
):
    """
    Selectively merge specific components across *all layers*.
    This function creates different config structures based on the merge method.
    """
    # Build the list of filters MergeKit will apply
    filters = []
    for comp in component_names:
        if comp == "embed_tokens":
            # Fully-qualified path expected by mergekit filter matching
            filters.append("model.embed_tokens.weight")
        elif comp == "lm_head":
            filters.append("lm_head.weight")
        elif comp == "final_norm":
            filters.append("model.norm.weight")
        else:
            # Target the weight tensor of the specified module across layers
            filters.append(f"{comp}.weight")

    if merge_method in ['slerp', 'nuslerp']:
        # NuSLERP supports a models-style config with per-model weights. If two explicit
        # models are provided, prefer that form and apply weights only to filtered tensors.
        if merge_method == 'nuslerp' and model_a and model_b:
            weights = model_weights if model_weights is not None else [0.5, 0.5]
            # Determine default (unfiltered) weight behavior. For a two-source merge without
            # a base, 'base' is ambiguous. Default to 'model_a' as the safer option.
            if unfiltered_source == 'base':
                print("--- WARNING: `unfiltered_source: base` is ambiguous for a two-source NuSLERP merge. Defaulting to 'model_a' for unfiltered components. ---")
                unfiltered_source = 'model_a'
            
            default_weight_a = 1.0 if unfiltered_source == 'model_a' else 0.0
            default_weight_b = 1.0 if unfiltered_source == 'model_b' else 0.0
            return {
                "merge_method": "nuslerp",
                "base_model": base_model,
                "dtype": "bfloat16",
                "tokenizer_source": tokenizer_source,
                "chat_template": chat_template,
                "models": [
                    {
                        "model": model_a,
                        "parameters": {
                            # Apply weight only on selected components; default 0 elsewhere
                            "weight": ([{"filter": f, "value": float(weights[0])} for f in filters] + [{"value": float(default_weight_a)}])
                        },
                    },
                    {
                        "model": model_b,
                        "parameters": {
                            "weight": ([{"filter": f, "value": float(weights[1])} for f in filters] + [{"value": float(default_weight_b)}])
                        },
                    },
                ],
                "parameters": {"normalize": bool(normalize)},
            }
        # Otherwise, fall back to a slice-based interpolation where only filtered tensors
        # receive non-zero t and everything else remains from the base (t=0 default).
        method_for_config = 'slerp'
        # Default t for unfiltered tensors
        default_t = 0.0
        if unfiltered_source == 'model_to_merge':
            default_t = 1.0
        elif unfiltered_source == 'base':
            default_t = 0.0
        elif unfiltered_source in ('model_a', 'model_b'):
            print(f"--- WARNING: unfiltered_source '{unfiltered_source}' is invalid for a slice-based merge which uses 'base' or 'model_to_merge'. Using 'base' for unfiltered tensors. ---")
            default_t = 0.0
        cfg = {
            "merge_method": method_for_config,
            "base_model": base_model,
            "dtype": "bfloat16",
            "tokenizer_source": tokenizer_source,
            "chat_template": chat_template,
            "slices": [{
                "sources": [
                    {"model": base_model, "layer_range": [0, num_layers]},
                    {"model": model_to_merge, "layer_range": [0, num_layers]},
                ],
                "parameters": {
                    "t": (
                        [{"filter": f, "value": float(t_value)} for f in filters]
                        + [{"value": float(default_t)}]
                    )
                }
            }],
        }
        cfg["parameters"] = {"normalize": bool(normalize)}
        return cfg
    elif merge_method in ['della', 'dare_ties']:
        # Component-selective task arithmetic: restrict tensors via filters and merge two source models.
        weights = model_weights if model_weights is not None else [0.5, 0.5]
        if not (model_a and model_b):
            raise ValueError("Selective DELLA/DARE+TIES requires --model_a and --model_b.")
        # Determine default fallback for unfiltered tensors
        default_weight_a = 1.0 if unfiltered_source == 'model_a' else 0.0
        default_weight_b = 1.0 if unfiltered_source == 'model_b' else 0.0
        return {
            "models": [
                {
                    "model": model_a,
                    "parameters": {
                        # Only selected components contribute; default weight 0 elsewhere
                        "weight": ([{"filter": f, "value": float(weights[0])} for f in filters] + [{"value": float(default_weight_a)}]),
                        # Apply density only on selected components for this model
                        "density": [{"filter": f, "value": float(density)} for f in filters],
                    },
                },
                {
                    "model": model_b,
                    "parameters": {
                        "weight": ([{"filter": f, "value": float(weights[1])} for f in filters] + [{"value": float(default_weight_b)}]),
                        "density": [{"filter": f, "value": float(density)} for f in filters],
                    },
                },
            ],
            "merge_method": merge_method,
            "base_model": base_model,
            "dtype": "bfloat16",
            "tokenizer_source": tokenizer_source,
            "chat_template": chat_template,
        }
    else:
        raise ValueError(f"Unsupported merge method: {merge_method}")


def create_layer_component_slerp_config(
    base_model,
    model_to_merge,
    num_layers,
    layers_to_merge,
    component_names,
    t_value=0.5,
    unfiltered_source='model_to_merge',
    normalize=True,
):
    """
    Build a SLERP config that merges ONLY selected components on a SELECTED set of layers.

    - On layers listed in 'layers_to_merge', only the provided component_names are merged with t=t_value.
    - All other components fall back to 'unfiltered_source' (base or model_to_merge).
    - On layers NOT in layers_to_merge, ALL components come from 'unfiltered_source'.
    - Non-layer components (embed_tokens, lm_head, final_norm) are merged once globally with t=t_value.
    """
    if unfiltered_source not in ('base', 'model_to_merge'):
        raise ValueError("unfiltered_source must be 'base' or 'model_to_merge' for SLERP")

    default_t = 1.0 if unfiltered_source == 'model_to_merge' else 0.0

    # Split components into per-layer vs non-layer
    per_layer_components = [c for c in component_names if c not in NON_LAYER_COMPONENT_NAMES]
    non_layer_components = [c for c in component_names if c in NON_LAYER_COMPONENT_NAMES]

    # Helper to map component name to filter string
    def comp_to_filter(name: str) -> str:
        if name == 'embed_tokens':
            return 'model.embed_tokens.weight'
        if name == 'lm_head':
            return 'lm_head.weight'
        if name == 'final_norm':
            return 'model.norm.weight'
        return f"{name}.weight"

    per_layer_filters = [comp_to_filter(c) for c in per_layer_components]
    non_layer_filters = [comp_to_filter(c) for c in non_layer_components]

    # Build slice list
    slices = []

    # For each layer, set defaults and optional component merges
    layers_to_merge_set = set(int(x) for x in layers_to_merge)
    for layer_idx in range(int(num_layers)):
        t_entries = []
        if layer_idx in layers_to_merge_set and per_layer_filters:
            # Merge only the selected per-layer components on this layer
            for f in per_layer_filters:
                t_entries.append({"filter": f, "value": float(t_value)})
        # Default fallback for everything else on this layer
        t_entries.append({"value": float(default_t)})
        slices.append({
            'sources': [
                {'model': base_model, 'layer_range': [layer_idx, layer_idx + 1]},
                {'model': model_to_merge, 'layer_range': [layer_idx, layer_idx + 1]},
            ],
            'parameters': {'t': t_entries},
        })

    # Add a single global slice to handle non-layer components
    if non_layer_filters:
        t_entries = [{"filter": f, "value": float(t_value)} for f in non_layer_filters]
        t_entries.append({"value": float(default_t)})
        slices.append({
            'sources': [
                {'model': base_model, 'layer_range': [0, int(num_layers)]},
                {'model': model_to_merge, 'layer_range': [0, int(num_layers)]},
            ],
            'parameters': {'t': t_entries},
        })

    cfg = {
        'merge_method': 'slerp',
        'base_model': base_model,
        'dtype': 'bfloat16',
        'tokenizer_source': 'union',  # default; will be overwritten by args if provided
        'chat_template': 'auto',      # default; will be overwritten by args if provided
        'slices': slices,
    }
    cfg['parameters'] = {'normalize': bool(normalize)}
    return cfg


def run_mergekit(config, output_path, args):
    """Runs mergekit with a given config and output path using the Python API."""
    # Set CUDA devices if specified. This must be done BEFORE any torch calls.
    if args.cuda_devices:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.cuda_devices
        print(f"--> Setting CUDA_VISIBLE_DEVICES to: {args.cuda_devices}")

    try:
        # Ensure tokenizer is present before validation/merge
        try:
            if not isinstance(config, dict):
                raise TypeError("config must be a dict")
            # If 'tokenizer_source' is not set, default it to 'union'
            if 'tokenizer_source' not in config:
                config['tokenizer_source'] = getattr(args, 'tokenizer_source', None) or 'union'

            # Persist the effective config we are about to validate/merge
            try:
                os.makedirs(output_path, exist_ok=True)
                with open(os.path.join(output_path, 'effective_config.yml'), 'w') as f:
                    yaml.safe_dump(config, f, sort_keys=False)
                print(f"Saved effective config to {os.path.join(output_path, 'effective_config.yml')}")
            except Exception as _persist_e:
                print(f"--- WARNING: Could not save effective_config.yml: {_persist_e} ---")
        except Exception as _e:
            print(f"--- WARNING: Could not ensure tokenizer_source default; proceeding: {_e} ---")

        # Validate the config dictionary
        merge_config = MergeConfiguration.model_validate(config)
        
        # Set merge options
        merge_options = MergeOptions(
            lora_merge_cache=None,  # Not using LoRA
            cuda=torch.cuda.is_available(),
            # Let planner/build step create tokenizers per config; only copy if explicitly requested
            copy_tokenizer=False,
            lazy_unpickle=False,
            low_cpu_memory=False,
        )

        if not merge_options.cuda:
            print("--- WARNING: CUDA not available, merging on CPU. This will be slow. ---")

        print(f"Starting merge process for output path: {output_path}")
        run_merge(
            merge_config,
            out_path=output_path,
            options=merge_options,
        )
        print(f"Successfully merged model at {output_path}")

    except Exception as e:
        print(f"Error during mergekit execution: {e}")

def run_sweep(args):
    """Generates YAMLs and runs mergekit for each layer to be swapped."""
    os.makedirs(args.output_dir, exist_ok=True)
    window_size = args.sweep_window_size

    if window_size > 1:
        # New logic for windowed sweep that only processes full windows
        print(f"--- Starting sweep with window size: {window_size} ---")
        
        # Check if there will be unmerged layers at the end and notify the user
        if args.num_layers % window_size != 0:
            unmerged_count = args.num_layers % window_size
            print(f"--- NOTE: The last {unmerged_count} layer(s) will not be merged as they do not form a full window of size {window_size}. ---")

        # Only iterate up to the last possible start layer for a full window
        for start_layer in range(0, args.num_layers - window_size + 1, 1):
            end_layer = start_layer + window_size
            
            print(f"--- Processing Layer Window [{start_layer}, {end_layer}) ---")
            try:
                if args.merge_method in ('della', 'dare_ties'):
                    print("Error: --sweep is not supported for DELLA/DARE+TIES.")
                    return
                config = create_windowed_merge_config(
                    start_layer,
                    window_size,
                    args.base_model,
                    args.model_to_merge,
                    args.num_layers,
                    args.t_value,
                    args.merge_method,
                    tokenizer_source=args.tokenizer_source,
                    chat_template=args.chat_template,
                    normalize=args.normalize,
                )
            except ValueError as e:
                print(f"Error: {e}")
                return
            merge_output_path = os.path.join(args.output_dir, f'merged_model_layers_{start_layer}-{end_layer}')
            run_mergekit(config, merge_output_path, args)
    else:
        # Original logic for single-layer sweep
        print("--- Starting single-layer sweep ---")
        for layer in range(args.num_layers):
            print(f"--- Processing Layer {layer}/{args.num_layers - 1} ---")
            try:
                if args.merge_method in ('della', 'dare_ties'):
                    print("Error: Single-layer merges are not supported for DELLA/DARE+TIES.")
                    return
                config = create_single_layer_swap_config(
                    layer,
                    args.base_model,
                    args.model_to_merge,
                    args.num_layers,
                    args.t_value,
                    args.merge_method,
                    tokenizer_source=args.tokenizer_source,
                    chat_template=args.chat_template,
                )
            except ValueError as e:
                print(f"Error: {e}")
                return
            merge_output_path = os.path.join(args.output_dir, f'merged_model_layer_{layer}')
            run_mergekit(config, merge_output_path, args)

def run_single_layer_merge(args):
    """Generates a YAML and runs mergekit for a single specified layer."""
    os.makedirs(args.output_dir, exist_ok=True)
    if not (0 <= args.layer < args.num_layers):
        print(f"Error: --layer must be between 0 and {args.num_layers - 1}")
        return
        
    try:
        if args.merge_method in ('della', 'dare_ties'):
            print("Error: Single-layer merges are not supported for DELLA/DARE+TIES.")
            return
        config = create_single_layer_swap_config(
            args.layer,
            args.base_model,
            args.model_to_merge,
            args.num_layers,
            args.t_value,
            args.merge_method,
            tokenizer_source=args.tokenizer_source,
            chat_template=args.chat_template,
            normalize=args.normalize,
        )
    except ValueError as e:
        print(f"Error: {e}")
        return
    merge_output_path = os.path.join(args.output_dir, f'merged_model_layer_{args.layer}')
    run_mergekit(config, merge_output_path, args)

def run_full_merge(args):
    """Generates a YAML and runs mergekit for a full model merge."""
    os.makedirs(args.output_dir, exist_ok=True)
    # Build full-merge config depending on method
    model_weights = None
    if args.model_weights is not None:
        if len(args.model_weights) != 2:
            print("Error: --model_weights must provide exactly two floats (w1 w2).")
            return
        model_weights = args.model_weights

    try:
        config = create_full_merge_config(
            args.base_model,
            args.model_to_merge,
            args.num_layers,
            args.t_value,
            args.merge_method,
            args.density,
            model_a=args.model_a,
            model_b=args.model_b,
            model_weights=model_weights,
            tokenizer_source=args.tokenizer_source,
            chat_template=args.chat_template,
            normalize=args.normalize,
            model_stock_filter_wise=args.model_stock_filter_wise,
        )
    except ValueError as e:
        print(f"Error: {e}")
        return
    merge_output_path = os.path.join(args.output_dir, 'merged_model_full')
    run_mergekit(config, merge_output_path, args)

def run_random_merge(args):
    """
    Generates YAMLs and runs mergekit for N randomly selected layers, for a number of iterations.
    """
    os.makedirs(args.output_dir, exist_ok=True)
    
    if not (0 < args.random_merge <= args.num_layers):
        print(f"Error: --random_merge must be between 1 and {args.num_layers}")
        return

    num_iterations = args.num_iterations
    
    for i in range(num_iterations):
        print(f"--- Starting Random Merge Iteration {i+1}/{num_iterations} ---")
        
        all_layers = list(range(args.num_layers))
        layers_to_merge = random.sample(all_layers, args.random_merge)
        sorted_layers = sorted(layers_to_merge)
        
        print(f"--- Randomly selected layers for merging: {sorted_layers} ---")
        
        try:
            if args.merge_method in ('della', 'dare_ties'):
                print("Error: Random layer merges are not supported for DELLA/DARE+TIES.")
                return
            config = create_random_layers_merge_config(
                layers_to_merge,
                args.base_model,
                args.model_to_merge,
                args.num_layers,
                args.t_value,
                args.merge_method,
                tokenizer_source=args.tokenizer_source,
                chat_template=args.chat_template,
                normalize=args.normalize,
            )
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        layer_ids_str = '-'.join(map(str, sorted_layers))
        merge_output_path = os.path.join(args.output_dir, f'merged_model_random_layers_{layer_ids_str}')

        if os.path.exists(merge_output_path):
            print(f"--- Output path {merge_output_path} already exists, skipping iteration. ---")
            continue
        
        run_mergekit(config, merge_output_path, args)
        
        try:
            with open(os.path.join(merge_output_path, 'merged_layers.json'), 'w') as f:
                json.dump(sorted_layers, f, indent=2)
            print(f"--- Saved merged layer list to {os.path.join(merge_output_path, 'merged_layers.json')} ---")
        except Exception as e:
            print(f"--- WARNING: Could not save the list of merged layers: {e} ---")

def run_selective_merge(args):
    """
    Generates a YAML and runs mergekit for a selective merge of components.
    """
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Get component names from indices
    rev_mapping = {v: k for k, v in COMPONENT_MAPPING.items()}
    component_names = []
    for idx in args.selective_merge:
        if idx in rev_mapping:
            component_names.append(rev_mapping[idx])
        else:
            print(f"Warning: a component index '{idx}' is not valid. Skipping.")
    
    if not component_names:
        print("Error: No valid component indices provided for selective merge.")
        return

    # Determine the effective number of layers by taking the minimum across sources
    if args.merge_method in ('della', 'dare_ties') and args.model_a and args.model_b:
        print(f"Probing sources for number of layers: '{args.model_a}' and '{args.model_b}' ...")
        layers_a = get_num_layers(args.model_a)
        layers_b = get_num_layers(args.model_b)
        if layers_a is None or layers_b is None:
            print("Could not determine number of layers for one of the source models. Aborting.")
            return
        merge_model_layers = min(layers_a, layers_b)
    else:
        print(f"Probing '{args.model_to_merge}' for number of layers...")
        merge_model_layers = get_num_layers(args.model_to_merge)
    if merge_model_layers is None:
        print(f"Could not determine number of layers for {args.model_to_merge}. Aborting.")
        return
    
    effective_num_layers = min(args.num_layers, merge_model_layers)
    if effective_num_layers < args.num_layers or effective_num_layers < merge_model_layers:
        print(f"--- WARNING: Models have different layer counts ({args.num_layers} vs {merge_model_layers}). Using the minimum: {effective_num_layers} layers. ---")

    print(f"--- Starting selective merge for components: {', '.join(component_names)} ---")

    model_weights = None
    if args.model_weights is not None:
        if len(args.model_weights) != 2:
            print("Error: --model_weights must provide exactly two floats (w1 w2).")
            return
        model_weights = args.model_weights

    config = create_selective_merge_config(
        args.base_model,
        args.model_to_merge,
        component_names,
        effective_num_layers,
        args.t_value,
        merge_method=args.merge_method,
        density=args.density,
        tokenizer_source=args.tokenizer_source,
        chat_template=args.chat_template,
        normalize=args.normalize,
        model_a=args.model_a,
        model_b=args.model_b,
        model_weights=model_weights,
        unfiltered_source=args.unfiltered_source,
    )
    
    component_ids_str = '-'.join(map(str, sorted(args.selective_merge)))
    merge_output_path = os.path.join(args.output_dir, f'merged_model_selective_{component_ids_str}')

    if os.path.exists(merge_output_path):
        print(f"--- Output path {merge_output_path} already exists, skipping. ---")
        return

    run_mergekit(config, merge_output_path, args)


def run_layer_component_selective_merge(args):
    """Run SLERP merging only certain components and only on selected layers."""
    if args.merge_method not in ('slerp', 'nuslerp'):
        print("Error: --layer_component_selective currently supports only SLERP/NuSLERP style interpolation.")
        return

    # Determine number of layers
    if args.num_layers is None:
        print(f"Probing '{args.base_model}' for number of layers...")
        args.num_layers = get_num_layers(args.base_model)
        if args.num_layers is None:
            print("Could not determine number of layers. Please specify with --num_layers.")
            return
        else:
            print(f"--> Detected {args.num_layers} layers.")

    # Validate inputs
    if not args.layers_to_merge or not isinstance(args.layers_to_merge, list):
        print("Error: --layers_to_merge must be provided for --layer_component_selective.")
        return
    if not args.component_ids or not isinstance(args.component_ids, list):
        print("Error: --component_ids must provide component indices to merge.")
        return

    # Map indices to names
    rev_mapping = {v: k for k, v in COMPONENT_MAPPING.items()}
    component_names = []
    for idx in args.component_ids:
        if idx in rev_mapping:
            component_names.append(rev_mapping[idx])
        else:
            print(f"Warning: component index '{idx}' is invalid. Skipping.")
    if not component_names:
        print("Error: No valid components resolved from --component_ids.")
        return

    # Build config
    try:
        cfg = create_layer_component_slerp_config(
            base_model=args.base_model,
            model_to_merge=args.model_to_merge,
            num_layers=args.num_layers,
            layers_to_merge=args.layers_to_merge,
            component_names=component_names,
            t_value=args.t_value,
            unfiltered_source=('model_to_merge' if args.unfiltered_source in (None, 'model_to_merge') else 'base'),
            normalize=args.normalize,
        )
        # Allow overrides for tokenizer/chat Template from args
        if hasattr(args, 'tokenizer_source') and args.tokenizer_source:
            cfg['tokenizer_source'] = args.tokenizer_source
        if hasattr(args, 'chat_template') and args.chat_template:
            cfg['chat_template'] = args.chat_template
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Output path naming
    layer_ids_str = '-'.join(map(str, sorted(set(args.layers_to_merge))))
    comp_ids_str = '-'.join(map(str, sorted(set(args.component_ids))))
    merge_output_path = os.path.join(
        args.output_dir,
        f'merged_model_layercomp_L{layer_ids_str}_C{comp_ids_str}',
    )

    if os.path.exists(merge_output_path):
        print(f"--- Output path {merge_output_path} already exists, skipping. ---")
        return

    run_mergekit(cfg, merge_output_path, args)

def main():
    parser = argparse.ArgumentParser(
        description='A comprehensive tool for merging, inspecting, and managing language models with mergekit.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # --- Argument Groups ---
    # Group for primary merge operations
    merge_group = parser.add_argument_group(
        'Merge Operations', 
        'Arguments for performing a model merge. Requires --output_dir.'
    )
    merge_group.add_argument('--output_dir', help='Directory where merged models will be saved.')
    merge_group.add_argument('--base_model', default='deepseek-ai/deepseek-math-7b-instruct', help='The base model (Hugging Face repo or local path).')
    merge_group.add_argument('--model_to_merge', default='deepseek-ai/deepseek-coder-6.7b-instruct', help='The model to merge layers from (Hugging Face repo or local path).')
    merge_group.add_argument('--num_layers', type=int, default=None, help='Number of layers in the models. If not provided, it will be fetched from the base_model config.')
    merge_group.add_argument('--t_value', type=float, default=0.5, help='Parameter t for SLERP merge, or ignored if --model_weights provided for models/NuSLERP.')
    merge_group.add_argument('--cuda_devices', type=str, default=None, help='Comma-separated list of GPU IDs to use (e.g., "0,1,2,3"). Sets CUDA_VISIBLE_DEVICES.')
    merge_group.add_argument('--num_iterations', type=int, default=25, help='Number of iterations for random merge.')
    merge_group.add_argument('--merge_method', type=str, default='slerp', help='Merge method: slerp | NuSLERP | DELLA | DARE+TIES | model_stock')
    merge_group.add_argument('--density', type=float, default=0.5, help='The density parameter for methods like dare_ties and della.')
    # Two-model merge inputs
    merge_group.add_argument('--model_a', type=str, default=None, help='First source model for NuSLERP/DELLA/DARE+TIES/model_stock.')
    merge_group.add_argument('--model_b', type=str, default=None, help='Second source model for NuSLERP/DELLA/DARE+TIES/model_stock.')
    merge_group.add_argument('--model_weights', type=float, nargs=2, default=None, metavar=('W1','W2'), help='Weights for model_a and model_b (two floats).')
    merge_group.add_argument('--unfiltered_source', type=str, default='base', choices=['base', 'model_a', 'model_b', 'model_to_merge'], help='For selective merges, the source for components not explicitly merged.')
    # Tokenizer/chat/normalize
    merge_group.add_argument('--tokenizer_source', type=str, default='union', choices=['union','base'], help='Tokenizer source for output model (union or base).')
    merge_group.add_argument('--chat_template', type=str, default='auto', help='Chat template to set on output repo.')
    # By default, enable normalization for NuSLERP to match best practices
    merge_group.add_argument('--normalize', action='store_true', default=True, help='Enable normalization (for NuSLERP). Use --no-normalize to disable.')
    merge_group.add_argument('--no-normalize', dest='normalize', action='store_false')
    # model_stock specific
    merge_group.add_argument('--model_stock_filter_wise', action='store_true', help='Enable filter-wise operation for model_stock merge. Default is False.')

    # Group for merge modes (mutually exclusive)
    mode_group = merge_group.add_mutually_exclusive_group()
    mode_group.add_argument('--sweep', action='store_true', help='Run a sweep, merging each layer one by one.')
    mode_group.add_argument('--layer', type=int, help='Merge only a single specified layer.')
    mode_group.add_argument('--random_merge', type=int, metavar='N', help='Merge N randomly selected layers, for a number of iterations.')
    # New mode: layer+component selective SLERP
    mode_group.add_argument('--layer_component_selective', action='store_true', help='Merge only selected components on a selected set of layers (SLERP).')
    
    component_map_str = "\n".join([f"  {v}: {k}" for k, v in COMPONENT_MAPPING.items()])
    selective_merge_help = f"""Merge only specific components (e.g., attention projections) across all layers.
Provide a space-separated list of component indices.

Available components:
{component_map_str}
"""
    mode_group.add_argument(
        '--selective_merge', 
        type=int, 
        nargs='+', 
        metavar='ID',
        help=textwrap.dedent(selective_merge_help)
    )
    
    # Add sweep window size argument here, tied to the a merge group
    merge_group.add_argument('--sweep_window_size', type=int, default=1, help='The size of the layer window for merging during a sweep. Only used with --sweep.')
    # (Removed) use_output_dir_as_leaf behavior to avoid empty tag directories
    # Arguments for layer+component selective SLERP
    merge_group.add_argument('--layers_to_merge', type=int, nargs='+', help='List of layer indices to apply component merges to (used with --layer_component_selective).')
    merge_group.add_argument('--component_ids', type=int, nargs='+', help='Component IDs to merge (used with --layer_component_selective).')

    # Group for standalone utility functions
    utility_group = parser.add_argument_group(
        'Utility Functions', 
        'Standalone tools for inspecting models. These commands run and exit immediately.'
    )
    utility_group.add_argument('--get-layers', type=str, metavar='MODEL_ID', help='Print the number of layers for a model and exit.')
    utility_group.add_argument('--show-properties', type=str, metavar='MODEL_ID', help='Print the full configuration for a model and exit.')
    
    args = parser.parse_args()

    # Normalize/validate merge method early
    try:
        args.merge_method = normalize_merge_method(args.merge_method)
    except ValueError as e:
        parser.error(str(e))

    # --- Execute Utility Functions ---
    # If a utility flag is used, perform the action and exit.
    if args.get_layers:
        print(f"Probing '{args.get_layers}' for number of layers...")
        num_layers = get_num_layers(args.get_layers)
        if num_layers is not None:
            print(f"--> The model '{args.get_layers}' has {num_layers} layers.")
        return

    if args.show_properties:
        show_model_properties(args.show_properties)
        return

    # --- Execute Merge Operation ---
    # If no utility was called, proceed with merge logic.
    # First, ensure output_dir is specified for merging.
    if not args.output_dir:
        parser.error("The --output_dir argument is required for all merge operations.")
        return

    # If num_layers is not provided, try to fetch it
    if args.num_layers is None:
        print(f"Probing '{args.base_model}' for number of layers...")
        args.num_layers = get_num_layers(args.base_model)
        if args.num_layers is None:
            print("Could not determine number of layers. Please specify with --num_layers.")
            return
        else:
            print(f"--> Detected {args.num_layers} layers.")

    # Method-specific validations
    if args.merge_method in ('della', 'dare_ties', 'model_stock'):
        if not (args.model_a and args.model_b):
            print(f"Error: {args.merge_method.upper()} requires --model_a and --model_b.")
            return
    if args.merge_method == 'nuslerp':
        # Allow either the legacy two-source slice mode or explicit --model_a/--model_b
        if args.model_a and args.model_b and args.model_weights is None:
            # If weights not given, derive from t_value as equal weights by default
            pass

    # Execute the selected mode
    if args.sweep:
        print("Starting layer sweep...")
        run_sweep(args)
    elif args.layer is not None:
        print(f"Starting single-layer merge for layer {args.layer}...")
        run_single_layer_merge(args)
    elif args.random_merge is not None:
        print(f"Starting random merge of {args.random_merge} layers for {args.num_iterations} iterations...")
        run_random_merge(args)
    elif args.layer_component_selective:
        print("Starting layer+component selective SLERP merge...")
        run_layer_component_selective_merge(args)
    elif args.selective_merge is not None:
        print(f"Starting selective merge for components {args.selective_merge}...")
        run_selective_merge(args)
    else:
        print("Starting full model merge...")
        run_full_merge(args)
    
    print("Pipeline finished.")

if __name__ == '__main__':
    main()
