# evaluators/simple_evaluator.py
from .base_evaluator import BaseEvaluator
import os
import json

class SimpleEvaluator(BaseEvaluator):
    """Evaluator that runs directly in the current environment without conda."""
    
    def _construct_command(self, model_path, task_name):
        """
        Constructs command to run lm-eval in the current environment.
        
        Args:
            model_path (str): Absolute path to the model directory.
            task_name (str): The name of the task to run.
            
        Returns:
            tuple: (command_list, working_directory, environment_name)
                   environment_name will be None to indicate direct execution.
        """
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        tp_size = len(gpu_ids.split(','))
        
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_ids
        
        batch_size = self.eval_settings.get("batch_size", "auto")
        temperature = self.eval_settings.get("temperature", 0.0)
        
        # Use hf model for simpler execution (no vllm)
        model_args = f"pretrained={model_path},dtype=bfloat16"
        
        gen_kwargs = {
            "temperature": temperature,
            "do_sample": False if temperature == 0.0 else True
        }
        gen_kwargs_str = json.dumps(gen_kwargs)
        
        command = [
            "python", "-m", "lm_eval",
            "--model", "hf",
            "--tasks", task_name,
            "--model_args", model_args,
            "--gen_kwargs", gen_kwargs_str,
            "--device", "cuda",
            "--batch_size", str(batch_size),
            "--output_path", f"./evaluation_results/{task_name}_output.json"
        ]

        # support `samples` command for random sampling eval
        samples_file = self.eval_settings.get("indices_file")
        if samples_file:
            # Read the file contents as a string since lm_eval expects a JSON string or file path parsing
            with open(samples_file, 'r') as f:
                samples_json = f.read()
            command.extend(["--samples", samples_json])
        
        # Return None for env_name to indicate direct execution
        return command, None, None
