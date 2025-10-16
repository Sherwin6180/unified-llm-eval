# evaluators/harness_evaluator.py
from .base_evaluator import BaseEvaluator
import os
import json

class HarnessEvaluator(BaseEvaluator):
    """Evaluator for HumanEval (lm-eval) and GSM8K (math-harness)."""
    def _construct_command(self, model_path, task_name):
        env_name = self.env_manager.harness_env
        gpu_ids = self.eval_settings.get("gpu_ids", "0")
        tp_size = len(gpu_ids.split(','))

        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_ids
        os.environ["VLLM_USE_V1"] = "0"
        
        if task_name == "humaneval":
            os.environ["HF_ALLOW_CODE_EVAL"] = "1"
            
            batch_size = self.eval_settings.get("batch_size", "auto")
            
            temperature = self.eval_settings.get("temperature", 0.0)
            
            model_args = f"pretrained={model_path},tensor_parallel_size={tp_size},dtype=bfloat16"
            
            # Create generation arguments for temperature and sampling
            gen_kwargs = {
                "temperature": temperature,
                "do_sample": False if temperature == 0.0 else True
            }
            gen_kwargs_str = json.dumps(gen_kwargs)
            
            command = [
                "python", "-m", "lm_eval",
                "--model", "vllm",
                "--tasks", "humaneval",
                "--model_args", model_args,
                "--gen_kwargs", gen_kwargs_str,
                # Consider removing this device flag
                "--device", "cuda",
                "--batch_size", str(batch_size),
                "--output_path", "./evaluation_results/humaneval_output.json",
                "--confirm_run_unsafe_code"
            ]
            return command, None, env_name
            
        elif task_name in ["gsm8k-cot", "gsm8k-pal"]:
            math_dir = self.env_config['math_harness_dir']
            prompt_type = "cot" if task_name == "gsm8k-cot" else "pal"
            
            temperature = self.eval_settings.get("temperature", 0.0)
            batch_size = self.eval_settings.get("batch_size", 32)
            
            math_script_path = os.path.abspath(os.path.join(math_dir, "math_eval.py"))
            if not os.path.exists(math_script_path):
                raise FileNotFoundError(f"Math eval script not found at expected path: {math_script_path}")

            command = [
                "python", math_script_path,
                "--model_name_or_path", model_path,
                "--data_names", "gsm8k",
                "--prompt_type", prompt_type,
                "--use_vllm",
                "--temperature", str(temperature),
                "--save_outputs",
                "--overwrite",
                "--batch_size", str(batch_size),
                "--use_safetensors"
            ]
            return command, math_dir, env_name
        
        else:
            raise ValueError(f"HarnessEvaluator does not support task: {task_name}")
