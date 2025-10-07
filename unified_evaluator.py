#!/usr/bin/env python3
# unified_evaluator.py

import argparse
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

from utils.config_loader import load_yaml_config
from utils.env_manager import EnvironmentManager
from utils.logger import log, display_scoreboard
from tasks.task_registry import TASK_REGISTRY, ALL_TASKS

class UnifiedEvaluator:
    """
    Main orchestrator for the model evaluation pipeline, driven by a single config file.
    """
    def __init__(self, config_path):
        """
        Initializes the evaluator by loading all settings from a single YAML config file.
        
        Args:
            config_path (str): Path to the master config.yml file.
        """
        config = load_yaml_config(config_path)
        
        # Load all configuration sections
        self.run_settings = config['run_settings']
        self.models_to_evaluate = config['models']
        self.eval_settings = config['evaluation_settings']
        self.env_config = config['environment_config']
        
        # Determine tasks to run from the config file
        self.tasks_to_run = self._parse_tasks(self.run_settings.get('tasks_to_run', []))
        
        self.env_manager = EnvironmentManager(
            self.env_config['harness_env'],
            self.env_config['languages_env']
        )
        self.results = []
        self.live_scoreboard = {}

    def _parse_tasks(self, tasks):
        """
        Resolves the list of tasks to run from the config.
        Handles the "all" keyword.
        """
        if not tasks:
            raise ValueError("The 'tasks_to_run' list in config.yml cannot be empty.")
        if "all" in tasks:
            return ALL_TASKS
        
        # Validate that all requested tasks are registered
        unknown_tasks = set(tasks) - set(ALL_TASKS)
        if unknown_tasks:
            raise ValueError(f"Unknown tasks specified in config.yml: {', '.join(unknown_tasks)}")
        return tasks

    def run(self):
        """
        Executes the main evaluation loop for all models, tasks, and runs.
        """
        # 1. Pre-flight checks for environments
        log("Performing pre-flight checks...")
        self.env_manager.check_environments()
        log("All checks passed.")

        # 2. Setup results file
        output_dir = Path(self.eval_settings.get("output_dir", "./evaluation_results"))
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = self.run_settings.get('task_name', 'evaluation').replace(' ', '_')
        csv_path = output_dir / f"{run_name}_{timestamp}.csv"

        # 3. Get runs_per_eval and calculate total tasks for the progress bar
        runs_per_eval = self.eval_settings.get("runs_per_eval", 1)
        total_tasks_count = len(self.models_to_evaluate) * len(self.tasks_to_run) * runs_per_eval
        
        log(f"Starting Run: {self.run_settings.get('task_name', 'N/A')}")
        log(f"Evaluating {len(self.models_to_evaluate)} models on {len(self.tasks_to_run)} tasks, with {runs_per_eval} run(s) per task...")
        
        with tqdm(total=total_tasks_count, desc="Overall Progress") as pbar:
            for model_config in self.models_to_evaluate:
                model_name = model_config['model_name']
                self.live_scoreboard[model_name] = {}
                
                for task_name in self.tasks_to_run:
                    # --- CORE FIX: Added inner loop for runs_per_eval ---
                    for run_id in range(1, runs_per_eval + 1):
                        # Look up the appropriate evaluator and environment for the task
                        task_info = TASK_REGISTRY.get(task_name)
                        if not task_info:
                            log(f"Warning: Task '{task_name}' not found in registry. Skipping.")
                            pbar.update(1)
                            continue

                        env_name = task_info["env"]
                        EvaluatorClass = task_info["evaluator"]

                        # Instantiate the evaluator for the current task
                        evaluator = EvaluatorClass(self.env_manager, self.env_config, self.eval_settings)

                        log(f"Running task '{task_name}' (Run {run_id}/{runs_per_eval}) for model '{model_name}'...")
                        
                        # Execute the evaluation and pass the run_id
                        result = evaluator.evaluate(model_config, task_name, run_id=run_id)
                        
                        # Store and log results in real-time
                        self.results.append(result)
                        pd.DataFrame(self.results).to_csv(csv_path, index=False)
                        
                        # Update the live scoreboard for terminal display
                        score_display = result['score'] if result['status'] == 'SUCCESS' else result['status']
                        # Create a display name that includes the run ID if there are multiple runs
                        display_name_run = f"{task_name}-R{run_id}" if runs_per_eval > 1 else task_name
                        self.live_scoreboard[model_name][f"{display_name_run} ({result['environment']})"] = score_display
                        display_scoreboard(self.live_scoreboard)
                        
                        pbar.update(1)
        
        log(f"Evaluation finished. Results saved to {csv_path}")
        time.sleep(5)

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Unified Model Evaluation Pipeline")
    parser.add_argument(
        "--config", 
        default="config.yml", 
        help="Path to the master YAML configuration file."
    )
    args = parser.parse_args()
    
    try:
        evaluator = UnifiedEvaluator(config_path=args.config)
        evaluator.run()
    except (ValueError, FileNotFoundError) as e:
        log(f"Error: {e}")
        log("Pipeline execution aborted.")

if __name__ == "__main__":
    main()