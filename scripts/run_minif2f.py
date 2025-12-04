#!/usr/bin/env python3
"""
Unified MiniF2F Evaluation Pipeline Script

This script provides a unified interface to run the complete MiniF2F evaluation
pipeline (inference -> compilation -> summarization) from the unified-llm-eval 
framework.

The script handles:
1. Proof generation using vLLM
2. Lean 4 compilation and verification
3. Results summarization and accuracy computation
4. Optional self-correction rounds

Usage:
    python run_minif2f.py \
        --model_path /path/to/model \
        --dataset_path dataset/minif2f.jsonl \
        --output_dir results/run_xxx \
        --num_samples 32 \
        --num_gpus 4
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
# Default goedel-prover directory (can be overridden via --goedel_prover_dir)
DEFAULT_GOEDEL_DIR = PROJECT_ROOT / "vendor" / "goedel-prover"
sys.path.insert(0, str(PROJECT_ROOT))


def run_command(cmd, cwd=None, env=None):
    """
    Run a command and return the result.
    
    Args:
        cmd: Command list to execute
        cwd: Working directory
        env: Environment variables
        
    Returns:
        subprocess.CompletedProcess
    """
    print(f"\n{'='*60}")
    print(f"Executing: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=False,  # Stream output to console
        text=True
    )
    return result


def run_inference(args, round_num, prev_output_dir=None):
    """
    Run the inference step to generate proofs.
    
    Args:
        args: Parsed command line arguments
        round_num: Current correction round (0 for initial)
        prev_output_dir: Output directory from previous round (for correction)
        
    Returns:
        Path to inference output file
    """
    print(f"\n{'#'*60}")
    print(f"# Step 1: Running Inference (Round {round_num})")
    print(f"{'#'*60}")
    
    cmd = [
        "python", str(args.goedel_prover_dir / "src" / "inference.py"),
        "--model_path", args.model_path,
        "--output_dir", args.output_dir,
        "--n", str(args.num_samples if round_num == 0 else args.num_samples_correction),
        "--gpu", str(args.num_gpus),
        "--inference_handler", args.inference_handler,
        "--correction_round", str(round_num),
        "--max_model_len", str(args.max_model_len),
        "--temp", str(args.temperature),
    ]
    
    if round_num == 0:
        # Initial inference needs input dataset
        cmd.extend(["--input_path", args.dataset_path])
        if args.split != "none":
            cmd.extend(["--split", args.split])
    else:
        # Correction rounds use previous output
        cmd.extend(["--previous_run_output_dir", prev_output_dir or args.output_dir])
    
    result = run_command(cmd, cwd=str(args.goedel_prover_dir))
    
    if result.returncode != 0:
        raise RuntimeError(f"Inference failed with return code {result.returncode}")
    
    # Determine output file path
    suffix = f"_corr{round_num}" if round_num > 0 else ""
    output_file = Path(args.output_dir) / f"to_inference_codes{suffix}.json"
    
    if not output_file.exists():
        raise FileNotFoundError(f"Expected inference output not found: {output_file}")
    
    return output_file


def run_compilation(args, inference_output, round_num):
    """
    Run the compilation step to verify proofs.
    
    Args:
        args: Parsed command line arguments
        inference_output: Path to inference output file
        round_num: Current correction round
        
    Returns:
        Path to compilation output file
    """
    print(f"\n{'#'*60}")
    print(f"# Step 2: Running Compilation (Round {round_num})")
    print(f"{'#'*60}")
    
    suffix = f"_corr{round_num}" if round_num > 0 else ""
    compile_output = Path(args.output_dir) / f"code_compilation_repl{suffix}.json"
    
    cmd = [
        "python", str(args.goedel_prover_dir / "src" / "compile.py"),
        "--input_path", str(inference_output),
        "--output_path", str(compile_output),
        "--cpu", str(args.num_cpus),
    ]
    
    result = run_command(cmd, cwd=str(args.goedel_prover_dir))
    
    if result.returncode != 0:
        raise RuntimeError(f"Compilation failed with return code {result.returncode}")
    
    if not compile_output.exists():
        raise FileNotFoundError(f"Expected compilation output not found: {compile_output}")
    
    return compile_output


def run_summarization(args, compile_output, round_num):
    """
    Run the summarization step to compute metrics.
    
    Args:
        args: Parsed command line arguments
        compile_output: Path to compilation output file
        round_num: Current correction round
        
    Returns:
        dict: Summary results
    """
    print(f"\n{'#'*60}")
    print(f"# Step 3: Generating Summary (Round {round_num})")
    print(f"{'#'*60}")
    
    suffix = f"_corr{round_num}" if round_num > 0 else ""
    full_records = Path(args.output_dir) / f"full_records{suffix}.json"
    summary_dir = Path(args.output_dir) / f"summary_round_{round_num}"
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python", str(args.goedel_prover_dir / "src" / "summarize.py"),
        "--input_path", str(compile_output),
        "--full_record_path", str(full_records),
        "--output_dir", str(summary_dir),
    ]
    
    result = run_command(cmd, cwd=str(args.goedel_prover_dir))
    
    if result.returncode != 0:
        raise RuntimeError(f"Summarization failed with return code {result.returncode}")
    
    # Read and return summary
    meta_file = summary_dir / "meta_summarize.json"
    if meta_file.exists():
        with open(meta_file) as f:
            return json.load(f)
    
    return None


def print_final_results(all_summaries, args):
    """
    Print final results in a format that can be parsed by unified-llm-eval.
    
    The self-correction mechanism is CUMULATIVE:
    - Round 0: Try all N problems
    - Round 1+: Try only the problems that failed in previous rounds
    - Final score = (total solved across all rounds) / (total problems)
    
    Args:
        all_summaries: List of summary results from each round
        args: Command line arguments
    """
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    
    # Track cumulative solved count
    total_problems = 0  # Set from Round 0
    cumulative_solved = 0
    
    for round_num, summary in enumerate(all_summaries):
        if summary:
            for item in summary:
                if item.get("level") == "origin_problem_id":
                    value = item.get("value", {})
                    solved = value.get("solved_num", 0)
                    problems_this_round = value.get("problem_num", 0)
                    
                    if round_num == 0:
                        total_problems = problems_this_round
                    
                    cumulative_solved += solved
                    
                    print(f"\nRound {round_num}:")
                    print(f"  Attempted: {problems_this_round} problems")
                    print(f"  Newly Solved: {solved}")
                    print(f"  Cumulative: {cumulative_solved}/{total_problems}")
    
    # Calculate cumulative score
    if total_problems > 0:
        cumulative_score = (cumulative_solved / total_problems) * 100
    else:
        cumulative_score = 0.0
    
    # Print in a format parseable by result_parser.py
    print(f"\n{'='*60}")
    print(f"CUMULATIVE RESULT:")
    print(f"  Total Solved: {cumulative_solved}/{total_problems}")
    print(f'"solved_ratio": "{cumulative_score:.2f}"')
    print(f"MiniF2F Score: {cumulative_score:.2f}%")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Unified MiniF2F Evaluation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument("--model_path", required=True, type=str,
                        help="Path to the model (local path or HuggingFace model ID)")
    parser.add_argument("--dataset_path", required=True, type=str,
                        help="Path to the MiniF2F dataset (JSONL format)")
    parser.add_argument("--output_dir", required=True, type=str,
                        help="Output directory for results")
    
    # Optional arguments
    parser.add_argument("--split", default="test", type=str,
                        choices=["test", "valid", "none"],
                        help="Dataset split to evaluate (default: test)")
    parser.add_argument("--num_samples", default=32, type=int,
                        help="Number of proof samples per problem for initial round")
    parser.add_argument("--num_samples_correction", default=2, type=int,
                        help="Number of samples per failed problem in correction rounds")
    parser.add_argument("--num_gpus", default=4, type=int,
                        help="Number of GPUs to use for vLLM inference")
    parser.add_argument("--gpu_ids", default=None, type=str,
                        help="Comma-separated GPU IDs (e.g., '2,3,5,6'). Sets CUDA_VISIBLE_DEVICES.")
    parser.add_argument("--num_cpus", default=64, type=int,
                        help="Number of CPU cores for Lean compilation")
    parser.add_argument("--max_correction_rounds", default=0, type=int,
                        help="Maximum number of self-correction rounds (0 = no correction)")
    parser.add_argument("--inference_handler", default="dpskcot", type=str,
                        choices=["dpskcot", "dpsknoncot", "kiminacot"],
                        help="Inference handler type")
    parser.add_argument("--temperature", default=1.0, type=float,
                        help="Sampling temperature for inference")
    parser.add_argument("--max_model_len", default=40960, type=int,
                        help="Maximum model sequence length")
    parser.add_argument("--goedel_prover_dir", default=None, type=str,
                        help="Path to Goedel-Prover-V2 directory (default: vendor/goedel-prover)")
    
    args = parser.parse_args()
    
    # Set goedel_prover_dir
    if args.goedel_prover_dir:
        args.goedel_prover_dir = Path(args.goedel_prover_dir).resolve()
    else:
        args.goedel_prover_dir = DEFAULT_GOEDEL_DIR.resolve()
    
    # Set CUDA_VISIBLE_DEVICES if gpu_ids is specified
    if args.gpu_ids:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_ids
        print(f"Setting CUDA_VISIBLE_DEVICES={args.gpu_ids}")
    
    # Create output directory
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save configuration (convert Path objects to strings for JSON serialization)
    config_file = Path(args.output_dir) / "run_config.json"
    config_data = {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()}
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print(f"\n{'='*60}")
    print("MiniF2F Evaluation Pipeline")
    print(f"{'='*60}")
    print(f"Model: {args.model_path}")
    print(f"Dataset: {args.dataset_path}")
    print(f"Split: {args.split}")
    print(f"Samples: {args.num_samples}")
    print(f"GPU IDs: {args.gpu_ids or 'auto'} (num_gpus={args.num_gpus})")
    print(f"CPUs: {args.num_cpus}")
    print(f"Correction rounds: {args.max_correction_rounds}")
    print(f"Output: {args.output_dir}")
    print(f"{'='*60}")
    
    all_summaries = []
    
    # Run pipeline for each round
    for round_num in range(args.max_correction_rounds + 1):
        print(f"\n\n{'#'*60}")
        print(f"{'#'*20} ROUND {round_num} {'#'*20}")
        print(f"{'#'*60}")
        
        try:
            # Step 1: Inference
            inference_output = run_inference(args, round_num)
            
            # Step 2: Compilation
            compile_output = run_compilation(args, inference_output, round_num)
            
            # Step 3: Summarization
            summary = run_summarization(args, compile_output, round_num)
            all_summaries.append(summary)
            
        except Exception as e:
            print(f"\nError in round {round_num}: {e}")
            all_summaries.append(None)
            # Continue to next round if possible
            if round_num == 0:
                raise  # Initial round failure is fatal
    
    # Print final results
    print_final_results(all_summaries, args)
    
    print(f"\n{'='*60}")
    print("Pipeline completed successfully!")
    print(f"Results saved to: {args.output_dir}")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

