# evaluators/minif2f_evaluator.py

"""
MinIF2F Evaluator for Lean 4 theorem proving.

This evaluator integrates the Goedel-Prover-V2 pipeline into the unified-llm-eval
framework for evaluating LLM performance on the MiniF2F benchmark.

The pipeline consists of three stages:
1. Inference: Generate Lean 4 proofs using vLLM
2. Compilation: Verify proofs using Lean 4 REPL
3. Summarization: Aggregate results and compute accuracy

Key features:
- Supports GPU configuration via config.yml
- Automatic environment setup (Lean 4 + Mathlib4)
- Support for self-correction rounds
"""

import os
from pathlib import Path
from datetime import datetime
from .base_evaluator import BaseEvaluator


class MinIF2FEvaluator(BaseEvaluator):
    """
    Evaluator for MiniF2F theorem proving benchmark using Goedel-Prover pipeline.
    
    This evaluator runs the complete pipeline:
    1. Generate proofs with vLLM
    2. Compile proofs with Lean 4 REPL
    3. Summarize results
    """
    
    # Default paths relative to project root
    DEFAULT_GOEDEL_DIR = "vendor/goedel-prover"
    DEFAULT_DATASET_PATH = "dataset/minif2f.jsonl"
    
    # Get project root directory (parent of evaluators/)
    PROJECT_ROOT = Path(__file__).parent.parent.resolve()
    
    def __init__(self, env_manager, env_config, eval_settings):
        super().__init__(env_manager, env_config, eval_settings)
        
        # Get goedel-prover directory from config or use default
        self.goedel_dir = Path(
            env_config.get("goedel_prover_dir", self.DEFAULT_GOEDEL_DIR)
        ).resolve()
        
        # Get minif2f-specific settings
        self.minif2f_settings = eval_settings.get("minif2f_settings", {})
        
    def _get_gpu_env(self):
        """
        Configure environment variables for GPU usage.
        
        Returns:
            dict: Environment variables with CUDA_VISIBLE_DEVICES set
        """
        env = os.environ.copy()
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        env["CUDA_VISIBLE_DEVICES"] = gpu_ids
        return env
    
    def _get_num_gpus(self):
        """Get number of GPUs from configuration."""
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        return len(gpu_ids.split(','))
    
    def _construct_command(self, model_path, task_name):
        """
        Constructs the command to run the MiniF2F evaluation pipeline.
        
        For minif2f, we need to run a multi-step pipeline:
        1. inference.py - Generate proofs
        2. compile.py - Verify proofs  
        3. summarize.py - Compute metrics
        
        Since this is complex, we use a wrapper script that runs all steps.
        
        Args:
            model_path (str): Path to the model
            task_name (str): Task name (minif2f or minif2f-test)
            
        Returns:
            tuple: (command_list, working_directory, environment_name)
        """
        env_name = self.env_config.get("goedelv2_env", "goedelv2")
        
        # Determine the split (valid or test)
        split = "test"
        if "-valid" in task_name:
            split = "valid"
        elif "-test" in task_name:
            split = "test"
            
        # Get dataset path
        dataset_path = self.minif2f_settings.get(
            "dataset_path", 
            str(self.goedel_dir / self.DEFAULT_DATASET_PATH)
        )
        if not os.path.isabs(dataset_path):
            dataset_path = str(self.goedel_dir / dataset_path)
            
        # Create output directory (use absolute path to avoid issues with cwd)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = os.path.basename(model_path.rstrip('/'))
        output_dir = Path(self.eval_settings.get("output_dir", "./evaluation_results")).resolve()
        output_dir = output_dir / "minif2f" / f"{model_name}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get pipeline parameters from settings
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        num_gpus = self._get_num_gpus()
        num_samples = self.minif2f_settings.get("num_samples", 32)
        num_cpus = self.minif2f_settings.get("num_cpus", 64)
        max_correction_rounds = self.minif2f_settings.get("max_correction_rounds", 0)
        inference_handler = self.minif2f_settings.get("inference_handler", "dpskcot")
        temperature = self.minif2f_settings.get("temperature", 1.0)
        max_model_len = self.minif2f_settings.get("max_model_len", 40960)
        
        # Build the wrapper script command (located in project scripts/ directory)
        wrapper_script = str(self.PROJECT_ROOT / "scripts" / "run_minif2f.py")
        
        command = [
            "python", wrapper_script,
            "--model_path", model_path,
            "--dataset_path", dataset_path,
            "--output_dir", str(output_dir),
            "--goedel_prover_dir", str(self.goedel_dir),  # Path to Goedel-Prover-V2
            "--split", split,
            "--num_samples", str(num_samples),
            "--num_gpus", str(num_gpus),
            "--gpu_ids", gpu_ids,  # Pass specific GPU IDs for CUDA_VISIBLE_DEVICES
            "--num_cpus", str(num_cpus),
            "--max_correction_rounds", str(max_correction_rounds),
            "--inference_handler", inference_handler,
            "--temperature", str(temperature),
            "--max_model_len", str(max_model_len),
        ]
        
        return command, str(self.goedel_dir), env_name
    
    def evaluate(self, model_config, task_name, run_id=1):
        """
        Execute the MiniF2F evaluation.
        
        This overrides the base evaluate method to handle the multi-step
        pipeline and custom result parsing.
        
        Args:
            model_config (dict): Model configuration
            task_name (str): Task name
            run_id (int): Run identifier
            
        Returns:
            dict: Evaluation results
        """
        import time
        from utils.result_parser import parse_score
        from utils.logger import log
        
        start_time = time.time()
        model_name = model_config['model_name']
        model_path = model_config['path']
        
        # Construct command
        command, cwd, env_name = self._construct_command(model_path, task_name)
        
        # Longer timeout for minif2f (theorem proving takes time)
        timeout = self.eval_settings.get("timeout_minutes", 120) * 60
        
        # Check verbose setting for console output
        verbose = self.eval_settings.get("verbose", True)
        
        log(f"Starting MiniF2F evaluation for '{model_name}' on task '{task_name}'")
        log(f"GPU IDs: {self.eval_settings.get('gpu_ids', '0')}, Verbose: {verbose}")
        
        # Run the command (stream_output controlled by verbose setting)
        result = self.env_manager.run_in_env(
            env_name, command, cwd=cwd, timeout=timeout, stream_output=verbose
        )
        
        duration = time.time() - start_time
        
        # Parse results
        status = "FAILED"
        score = "N/A"
        error_log = ""
        
        if hasattr(result, 'timeout') and result.timeout:
            status = "TIMEOUT"
            error_log = f"Task timed out after {timeout/60} minutes."
        elif result.returncode == 0:
            full_output = result.stdout + "\n" + result.stderr
            parsed_score = parse_score(full_output, task_name)
            if parsed_score is not None:
                status = "SUCCESS"
                score = f"{parsed_score:.2f}%"
            else:
                # Try to parse from summary file
                parsed_score = self._parse_summary_file(full_output)
                if parsed_score is not None:
                    status = "SUCCESS"
                    score = f"{parsed_score:.2f}%"
                else:
                    status = "PARSE_ERROR"
                    error_log = "Could not parse score from output."
        else:
            error_log = result.stderr or result.stdout
            
        return {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model_name": model_name,
            "task": task_name,
            "run_id": run_id,
            "environment": env_name,
            "score": score,
            "status": status,
            "duration": f"{duration/60:.2f}min",
            "error_log": str(error_log).strip()[-2000:]
        }
    
    def _parse_summary_file(self, output):
        """
        Parse the summary file to extract the score.
        
        The summary file contains JSON with solved_ratio.
        
        Args:
            output (str): Command output containing path to summary file
            
        Returns:
            float: Parsed score or None
        """
        import re
        
        # Look for the score pattern in output
        # Pattern: "solved_ratio": "XX.XXXX"
        match = re.search(r'"solved_ratio":\s*"?\s*([\d.]+)', output)
        if match:
            return float(match.group(1))
        
        # Alternative pattern: solved_num / problem_num
        match = re.search(r'"solved_num":\s*(\d+).*?"problem_num":\s*(\d+)', output, re.DOTALL)
        if match:
            solved = int(match.group(1))
            total = int(match.group(2))
            if total > 0:
                return (solved / total) * 100
                
        return None

