# evaluators/language_evaluator.py
from .base_evaluator import BaseEvaluator
import os
import random

class LanguageEvaluator(BaseEvaluator):
    """
    Evaluator for programming languages.
    Now uses 'torchrun' for multi-GPU, which is more robust than 'accelerate launch'.
    """
    def _construct_command(self, model_path, task_name):
        env_name = self.env_manager.languages_env
        eval_dir = self.env_config['language_eval_dir']
        
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        num_gpus = len(gpu_ids.split(','))

        # Set environment variables for the subprocess to see
        # PYTHONPATH is crucial for local imports
        os.environ["PYTHONPATH"] = os.path.abspath(eval_dir) + os.pathsep + os.environ.get("PYTHONPATH", "")
        # CUDA_VISIBLE_DEVICES tells torchrun which GPUs are available
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_ids
        
        eval_script_path = os.path.abspath(os.path.join(eval_dir, "eval_pal.py"))
        dataroot_path = os.path.abspath(os.path.join(eval_dir, "data/"))

        if num_gpus <= 1:
            print("\n[INFO] Single GPU detected. Running with simple 'python' command.\n")
            command = [
                "python",
                eval_script_path,
                "--logdir", model_path,
                "--language", task_name,
                "--dataroot", dataroot_path
            ]
        else:
            print(f"\n[INFO] {num_gpus} GPUs detected. Using 'torchrun' for distributed evaluation.\n")
            master_port = random.randint(20000, 29999)
            command = [
                "torchrun",
                "--nproc_per_node", str(num_gpus),
                "--master_port", str(master_port),
                eval_script_path,
                "--logdir", model_path,
                "--language", task_name,
                "--dataroot", dataroot_path
            ]
        
        return command, eval_dir, env_name