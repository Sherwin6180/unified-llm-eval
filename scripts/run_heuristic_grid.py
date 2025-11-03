#!/usr/bin/env python3
import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
import yaml
from copy import deepcopy

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_CONFIG_PATH = REPO_ROOT / "algorithms" / "sandhi_config.yml"
OUTPUT_ROOT = REPO_ROOT / "algorithms" / "outputs" / "heuristic_runs"
PYTHON_EXE = sys.executable
HEURISTIC_MODULE = "algorithms.heuristic"

SCHEMES = [
    "attn_only",
    "attn_plus_mlp",
    "best_setting",
    "full",
]
BUDGETS = [10, 15, 20]
# GPU pairs (as absolute IDs). We will export CUDA_VISIBLE_DEVICES to restrict visibility
GPU_PAIRS = ["0,1", "2,3", "4,5", "6,7"]


def load_base_config() -> dict:
    with open(BASE_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def write_run_config(base_cfg: dict, budget: int, scheme: str, out_path: Path, gpu_pair_visible_ids: str) -> None:
    cfg = deepcopy(base_cfg)
    # Update heuristic settings
    cfg["algorithm_settings"]["heuristic_settings"]["layer_budget"] = int(budget)
    cfg["algorithm_settings"]["heuristic_settings"]["merge_scheme"] = str(scheme)
    # Make harness use the absolute GPU pair for this run (the evaluator resets CUDA_VISIBLE_DEVICES)
    cfg["evaluation_settings"]["gpu_ids"] = gpu_pair_visible_ids
    # Ensure output dir exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)


def start_run(budget: int, scheme: str, gpu_pair: str) -> subprocess.Popen:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    run_dir = OUTPUT_ROOT / f"budget_{budget}" / scheme
    run_dir.mkdir(parents=True, exist_ok=True)

    # Per-run config file (point heuristic via env var)
    run_config_path = run_dir / "sandhi_config.yml"
    base_cfg = load_base_config()
    write_run_config(base_cfg, budget, scheme, run_config_path, gpu_pair)

    # Log file
    log_path = run_dir / f"run_{timestamp}.log"
    log_f = open(log_path, "w")

    # Environment for the subprocess
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = gpu_pair
    env["SANDHI_CONFIG_PATH"] = str(run_config_path)
    env["PYTHONUNBUFFERED"] = "1"
    # Ensure package imports (e.g., utils.env_manager) resolve
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{str(REPO_ROOT)}:{existing_pp}" if existing_pp else str(REPO_ROOT)

    # Run heuristic as a module to keep repo root on sys.path
    cmd = [PYTHON_EXE, "-u", "-m", HEURISTIC_MODULE]
    proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), stdout=log_f, stderr=subprocess.STDOUT, env=env)
    # Attach extra attributes for bookkeeping
    proc._run_meta = {
        "budget": budget,
        "scheme": scheme,
        "gpu_pair": gpu_pair,
        "log_path": str(log_path),
    }
    return proc


def main():
    # Build the full job list
    jobs = [(b, s) for b in BUDGETS for s in SCHEMES]

    running: list[subprocess.Popen] = []
    available = GPU_PAIRS.copy()

    def reap_finished():
        nonlocal running, available
        still_running = []
        for p in running:
            ret = p.poll()
            if ret is None:
                still_running.append(p)
                continue
            meta = getattr(p, "_run_meta", {})
            print(f"[DONE] budget={meta.get('budget')} scheme={meta.get('scheme')} gpus={meta.get('gpu_pair')} log={meta.get('log_path')} status={ret}")
            # Free the GPU pair used by this process
            if meta.get("gpu_pair") and meta["gpu_pair"] not in available:
                available.append(meta["gpu_pair"])
        running = still_running

    # Scheduler loop
    while jobs or running:
        # Launch as many as possible up to available GPU pairs
        while jobs and available:
            budget, scheme = jobs.pop(0)
            gpu_pair = available.pop(0)
            print(f"[LAUNCH] budget={budget} scheme={scheme} gpus={gpu_pair}")
            p = start_run(budget, scheme, gpu_pair)
            running.append(p)
        # Wait a bit and reap
        time.sleep(5)
        reap_finished()

    print("All runs completed.")


if __name__ == "__main__":
    main()
