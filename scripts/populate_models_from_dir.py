#!/usr/bin/env python3
"""
Utility script to populate the `models` section of config.yml using
all immediate subdirectories found under a given root directory.

Usage:
  python scripts/populate_models_from_dir.py --root "/scratch/shared_dir/oduran6/" \
      --config "/nethome/oduran6/unified-llm-eval/config.yml" \
      --model-name-prefix "deepseek-coder-instruct" \
      --type "instruct"

Notes:
  - This script preserves the rest of the YAML file unmodified and
    only replaces the `models` list.
  - `model_name` is derived from the prefix plus the leaf directory name
    (e.g., prefix=deepseek-coder-instruct, leaf=my_model -> deepseek-coder-instruct-my_model).
  - Default model type is "instruct" if not specified.
"""

import argparse
from pathlib import Path
import sys
from typing import List

import yaml


def find_immediate_subdirs(root_dir: Path) -> List[Path]:
    if not root_dir.exists() or not root_dir.is_dir():
        raise FileNotFoundError(f"Root directory not found or not a directory: {root_dir}")
    # Only immediate subdirectories (not recursive)
    return sorted([p for p in root_dir.iterdir() if p.is_dir()])


def load_yaml_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r") as f:
        return yaml.safe_load(f)


def write_yaml_config(config_path: Path, data: dict) -> None:
    # Preserve indentation style (2 spaces) consistent with repository's config.yml
    with config_path.open("w") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            indent=2,
            default_flow_style=False,
            width=120,
        )


def build_models_list(
    subdirs: List[Path], model_name_prefix: str, model_type: str, description: str
) -> List[dict]:
    models = []
    for d in subdirs:
        leaf = d.name
        model_name = f"{model_name_prefix}-{leaf}" if model_name_prefix else leaf
        models.append(
            {
                "model_name": model_name,
                "path": str(d.resolve()),
                "type": model_type,
                "description": description,
            }
        )
    return models


def main() -> int:
    parser = argparse.ArgumentParser(description="Populate models list in config.yml from a root directory of subfolders")
    parser.add_argument("--root", required=True, help="Root directory containing model subdirectories")
    parser.add_argument("--config", default="config.yml", help="Path to config.yml to update")
    parser.add_argument(
        "--model-name-prefix",
        default="deepseek-coder-instruct",
        help="Prefix for model_name; final name is prefix-<leaf-dir>",
    )
    parser.add_argument("--type", default="instruct", help="Model type to set for all entries")
    parser.add_argument(
        "--description",
        default="Auto-populated model",
        help="Description to set for each model entry",
    )
    args = parser.parse_args()

    root_dir = Path(args.root)
    config_path = Path(args.config)

    subdirs = find_immediate_subdirs(root_dir)
    if not subdirs:
        print(f"No subdirectories found under {root_dir}. Nothing to populate.")
        return 0

    config_data = load_yaml_config(config_path)

    # Build new models list
    new_models = build_models_list(
        subdirs=subdirs,
        model_name_prefix=args.model_name_prefix,
        model_type=args.type,
        description=args.description,
    )

    # Replace the models section
    config_data["models"] = new_models

    write_yaml_config(config_path, config_data)

    print(f"Updated {config_path} with {len(new_models)} models from {root_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


