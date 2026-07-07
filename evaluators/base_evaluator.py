# evaluators/base_evaluator.py

from abc import ABC, abstractmethod
import time
import subprocess
from datetime import datetime
from utils.result_parser import parse_score

class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluation runners.
    It defines the common interface and orchestrates the evaluation execution flow.
    """
    def __init__(self, env_manager, env_config, eval_settings):
        """
        Initializes the evaluator with necessary managers and configurations.
        """
        self.env_manager = env_manager
        self.env_config = env_config
        self.eval_settings = eval_settings

    @abstractmethod
    def _construct_command(self, model_path, task_name):
        """
        Constructs the specific command to be executed for a given task.
        This method MUST be implemented by all subclasses.

        Args:
            model_path (str): Absolute path to the model directory.
            task_name (str): The name of the task to run.

        Returns:
            tuple: A tuple containing (command_list, working_directory, environment_name).
                   environment_name can be None for direct execution.
        """
        pass

    def evaluate(self, model_config, task_name, run_id=1):
        """
        Executes the evaluation for a given model and task, handles results,
        and returns a structured dictionary.

        Args:
            model_config (dict): The configuration dictionary for the model.
            task_name (str): The name of the task to run.
            run_id (int): The identifier for the current run, for multiple executions.

        Returns:
            dict: A dictionary containing the structured results of the evaluation.
        """
        start_time = time.time()
        model_name = model_config['model_name']
        model_path = model_config['path']
        
        # Delegate command construction to the specific subclass
        command, cwd, env_name = self._construct_command(model_path, task_name)
        
        timeout = self.eval_settings.get("timeout_minutes", 30) * 60
        
        # If env_name is None, run directly without conda
        if env_name is None:
            # DEBUG print
            print(f"\n[DEBUG] EXECUTING COMMAND:\n{' '.join(command)}\n")
            try:
                result = subprocess.run(
                    command,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            except subprocess.TimeoutExpired:
                result = subprocess.CompletedProcess(
                    args=command,
                    returncode=-1,
                    stdout="",
                    stderr=f"Command timed out after {timeout} seconds"
                )
                result.timeout = True
            except Exception as e:
                result = subprocess.CompletedProcess(
                    args=command,
                    returncode=-1,
                    stdout="",
                    stderr=f"Error running command: {e}"
                )
        else:
            # Run the command in the appropriate environment via the EnvironmentManager
            result = self.env_manager.run_in_env(env_name, command, cwd=cwd, timeout=timeout)
        
        duration = time.time() - start_time
        
        # Initialize default result values
        status = "FAILED"
        score = "N/A"
        error_log = ""

        # Parse the result from the subprocess
        if hasattr(result, 'timeout') and result.timeout:
            status = "TIMEOUT"
            error_log = f"Task timed out after {timeout/60} minutes."
        elif result.returncode == 0:
            full_output = result.stdout + "\n" + result.stderr
            print("\n[DEBUG] LM_EVAL OUTPUT:\n", full_output)
            parsed_score = parse_score(full_output, task_name)
            if parsed_score is not None:
                status = "SUCCESS"
                score = f"{parsed_score:.2f}%"
            else:
                status = "PARSE_ERROR"
                error_log = "Could not parse score from output."
        else:
            # Capture the error log if the command failed
            error_log = result.stderr or result.stdout

        # Return a structured dictionary that will become a row in the final CSV
        return {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "model_name": model_name,
            "task": task_name,
            "run_id": run_id,
            "environment": env_name or "direct",
            "score": score,
            "status": status,
            "duration": f"{duration/60:.2f}min",
            "error_log": str(error_log).strip()[-2000:]
        }
