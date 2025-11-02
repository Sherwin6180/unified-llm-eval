import os
import shutil
import yaml
import pandas as pd
from mergekit.config import MergeConfiguration
from mergekit.merge import MergeOptions, run_merge
from typing import Dict, List
from pathlib import Path
from utils.env_manager import EnvironmentManager
from tasks.task_registry import TASK_REGISTRY

CONFIG_FILE_PATH = "algorithms/sandhi_config.yml"

def process_individual_layer_data(profiling_file: str, tasks: List[str], baseline_accs: Dict[str, float]) -> Dict[str, pd.Series]:
    """
    Loads and processes the individual layer profiling data to calculate deltas.
    """
    # Mappings to translate internal task names to the names used in the CSV file.
    TASK_TO_METRIC = {
        "coder": "humaneval",
        "math": "gsm8k"
    }
    TASK_TO_BASEMODEL = {
        "coder": "code",
        "math": "math"
    }

    task1, task2 = tasks
    metric1 = TASK_TO_METRIC.get(task1, task1)
    metric2 = TASK_TO_METRIC.get(task2, task2)
    basetype1 = TASK_TO_BASEMODEL.get(task1, task1)
    basetype2 = TASK_TO_BASEMODEL.get(task2, task2)

    print(f"Loading and processing individual layer data from: {profiling_file}")

    if not os.path.exists(profiling_file):
        print(f"Error: Profiling file not found at '{profiling_file}'")
        return None

    df = pd.read_csv(profiling_file)
    
    # Convert accuracy from proportion (0.x) to percentage (0-100)
    df['accuracy'] = df['accuracy'] * 100

    # Filter using the correct basetype and metric names from the mappings.
    # This logic assumes we want the performance of the 'coder'-based merge on the 'humaneval' task, etc.
    perf1 = df[(df['base_model'] == basetype1) & (df['metric'] == metric1)][['layer_id', 'accuracy']]
    perf1 = perf1.rename(columns={'accuracy': f'{task1}_acc'})

    perf2 = df[(df['base_model'] == basetype2) & (df['metric'] == metric2)][['layer_id', 'accuracy']]
    perf2 = perf2.rename(columns={'accuracy': f'{task2}_acc'})

    results = pd.merge(perf1, perf2, on='layer_id')

    # This calculation correctly compares percentages with percentages.
    deltas = {}
    deltas[task1] = (results[f'{task1}_acc'] - baseline_accs[task1]) / baseline_accs[task1]
    deltas[task1].index = results['layer_id']

    deltas[task2] = (results[f'{task2}_acc'] - baseline_accs[task2]) / baseline_accs[task2]
    deltas[task2].index = results['layer_id']
    
    if results.empty:
        print("\nWARNING: The profiling data processing resulted in an empty DataFrame.")
        print("Please check for mismatches between script task names and CSV 'base_model'/'metric' columns.")
        return None

    return deltas


def run_greedy(deltas: Dict[str, pd.Series], budget: int, weights: Dict[str, float]) -> List[int]:
    """
    Selects the top N layers based on a weighted score of performance deltas.
    """
    layer_ids = next(iter(deltas.values())).index
    layer_scores = pd.Series(0.0, index=layer_ids)

    for lang, delta_series in deltas.items():
        layer_scores += delta_series * weights[lang]

    sorted_layers = layer_scores.sort_values(ascending=False)
    selected_layers = sorted_layers.head(budget).index.tolist()

    return sorted(selected_layers)

# --- Functions reused from greedy.py for merging and evaluation ---

def create_yaml_for_merge(layers_to_merge: list, base_language: str, models_subset: Dict[str, str], output_dir: str, total_layers: int) -> str:
    """
    Generates a mergekit YAML configuration for a given set of layers.
    """
    os.makedirs(output_dir, exist_ok=True)
    lang_names = list(models_subset.keys())
    model_paths = list(models_subset.values())
    model_0_path, model_1_path = model_paths[0], model_paths[1]

    if base_language == lang_names[0]:
        base_model_path, unmerged_t = model_0_path, 0.0
    else:
        base_model_path, unmerged_t = model_1_path, 1.0

    slices = []
    current_pos = 0
    for layer_idx in sorted(layers_to_merge):
        if current_pos < layer_idx:
            slices.append({'sources': [{'model': model_0_path, 'layer_range': [int(current_pos), int(layer_idx)]}, {'model': model_1_path, 'layer_range': [int(current_pos), int(layer_idx)]}], 'parameters': {'t': [{'value': unmerged_t}]}})
        slices.append({'sources': [{'model': model_0_path, 'layer_range': [int(layer_idx), int(layer_idx + 1)]}, {'model': model_1_path, 'layer_range': [int(layer_idx), int(layer_idx + 1)]}], 'parameters': {'t': [{'value': 0.5}]}})
        current_pos = layer_idx + 1
    
    if current_pos < total_layers:
        slices.append({'sources': [{'model': model_0_path, 'layer_range': [int(current_pos), int(total_layers)]}, {'model': model_1_path, 'layer_range': [int(current_pos), int(total_layers)]}], 'parameters': {'t': [{'value': unmerged_t}]}})

    config_data = {'merge_method': 'slerp', 'base_model': base_model_path, 'dtype': 'bfloat16', 'slices': slices}
    
    layers_str = '_'.join(map(str, layers_to_merge))
    filename = f"merge_layers_{layers_str}_base_{base_language}.yaml"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        yaml.dump(config_data, f, sort_keys=False)
        
    return filepath

def evaluate_model(
    model_path: str, 
    task_name: str, 
    env_manager: EnvironmentManager, 
    env_config: dict, 
    eval_settings: dict
) -> float:
    
    TASK_NAME_TO_REGISTRY_KEY = {
        "coder": "humaneval",
        "math": "gsm8k-cot",
        "go": "go",
        "rust": "rust"
    }
    
    task_name = TASK_NAME_TO_REGISTRY_KEY.get(task_name, task_name)

    absolute_model_path = Path(model_path).resolve()
    model_name = os.path.basename(absolute_model_path)
    print(f"  Evaluation task: model '{model_name}' on '{task_name}'")

    task_info = TASK_REGISTRY.get(task_name)
    if not task_info:
        print(f"    Error: Task '{task_name}' not found in TASK_REGISTRY. Skipping.")
        return 0.0
    EvaluatorClass = task_info["evaluator"]

    evaluator = EvaluatorClass(env_manager, env_config, eval_settings)

    model_config = {
        'model_name': model_name,
        'path': str(absolute_model_path),
        'location': 'local'
    }

    result_dict = evaluator.evaluate(model_config, task_name, run_id=1)

    if result_dict['status'] == 'SUCCESS':
        try:
            score_str = result_dict['score'].replace('%', '')
            score = float(score_str)
            print(f"    Evaluation complete, score: {score:.4f}")
            return score
        except (ValueError, TypeError):
            print(f"    Error: Could not parse score '{result_dict['score']}' from result.")
            return 0.0
    else:
        print(f"    Error: Evaluation failed with status '{result_dict['status']}'.")
        print(f"    Error Log: {result_dict['error_log']}")
        return 0.0

def main():
    """Main execution function for the greedy script."""
    
    # --- Step 0: Load Config and Init Framework ---
    print(f"Loading configuration from {CONFIG_FILE_PATH}...")
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"Error: Config file not found at {CONFIG_FILE_PATH}")
        return

    with open(CONFIG_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f)

    algo_config = config['algorithm_settings']
    greedy_config = algo_config['greedy_settings']
    eval_settings = config['evaluation_settings']
    env_config = config['environment_config']

    tasks = algo_config['tasks']
    task1, task2 = tasks[0], tasks[1]
    layer_budget = greedy_config['layer_budget']
    weights = {task1: greedy_config['weights'][0], task2: greedy_config['weights'][1]}
    profiling_file = greedy_config['profiling_file_path']
    run_prefix = algo_config['run_prefix']
    
    models_to_merge = algo_config['models_to_merge']
    total_layers = algo_config['total_layers']

    tmp_dir = algo_config['tmp_dir']
    os.environ["TMPDIR"] = tmp_dir
    os.makedirs(tmp_dir, exist_ok=True)
    
    env_manager = EnvironmentManager(
        env_config['harness_env'], 
        env_config['languages_env']
    )
    print("Evaluation framework initialized.")


    # --- Step 1: Performing cross-evaluation to determine baselines ---
    print("\n--- Step 1: Performing cross-evaluation to determine baselines ---")
    
    models_subset = {task: models_to_merge[task] for task in tasks}
    model1_path = models_subset[task1]
    model2_path = models_subset[task2]

    print(f"\nEvaluating '{task2}' model on '{task1}' task...")
    model2_on_task1_acc = evaluate_model(
        model2_path, task1, env_manager, env_config, eval_settings
    )

    print(f"\nEvaluating '{task1}' model on '{task2}' task...")
    model1_on_task2_acc = evaluate_model(
        model1_path, task2, env_manager, env_config, eval_settings
    )
    
    baseline_accs = {
        task1: model2_on_task1_acc,
        task2: model1_on_task2_acc
    }

    if any(acc == 0.0 for acc in baseline_accs.values()):
        print(f"Error: Failed to obtain all cross-evaluation baselines: {baseline_accs}. Terminating.")
        return
        
    print(f"\nNew cross-evaluation baselines -> {baseline_accs}")

    # --- Step 2: Process Profiling Data ---
    deltas = process_individual_layer_data(profiling_file, tasks, baseline_accs)
    if deltas is None:
        return

    # --- Step 3: Run the Greedy to Select Layers ---
    print(f"\nRunning greedy with budget={layer_budget} and weights={weights}")
    selected_layers = run_greedy(deltas, layer_budget, weights)

    print("\n--- Greedy Selection Complete ---")
    print(f"Selected {len(selected_layers)} layers: {selected_layers}")

    if not selected_layers:
        print("No layers were selected. Exiting.")
        return

    # --- Step 4: Build and Save the Final Model ---
    print("\n--- Building and Saving Final Model ---")
    final_model_dir = f"algorithms/outputs/greedy_merged_model_{run_prefix}_{'_'.join(tasks)}"
    if os.path.exists(final_model_dir):
        shutil.rmtree(final_model_dir)

    final_base_task = tasks[0]
    final_config_path = create_yaml_for_merge(
        selected_layers, final_base_task, models_subset, "algorithms/outputs/greedy_model_config", total_layers
    )
    print(f"[Mergekit] Creating final model using config: {final_config_path}")
    
    with open(final_config_path, "r") as f:
        merge_config = MergeConfiguration.model_validate(yaml.safe_load(f))
    
    run_merge(merge_config, out_path=final_model_dir, options=MergeOptions(cuda=True, copy_tokenizer=True))
    
    tokenizer_path = list(models_subset.values())[0]
    shutil.copy(os.path.join(tokenizer_path, "tokenizer.json"), final_model_dir)
    shutil.copy(os.path.join(tokenizer_path, "tokenizer_config.json"), final_model_dir)
    
    print(f"Final model saved to: {final_model_dir}")
    
    # --- Step 5: Perform a Final Evaluation ---
    print("\n--- Performing Final Evaluation ---")
    final_accuracies = {}
    for task in tasks:
        final_accuracies[task] = evaluate_model(
            final_model_dir, task, env_manager, env_config, eval_settings
        )
        
    print(f"\n--- Process Finished ---")
    print(f"Final Merged Model Performance -> {final_accuracies}")


if __name__ == '__main__':
    if os.path.exists("algorithms/outputs/greedy_model_config"):
        shutil.rmtree("algorithms/outputs/greedy_model_config")
    
    main()