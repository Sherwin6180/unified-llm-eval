import os
import shutil
import tempfile
import hashlib
import yaml
import pandas as pd
import time
from mergekit.config import MergeConfiguration
from mergekit.merge import MergeOptions, run_merge
from typing import Dict, List
from pathlib import Path
from utils.env_manager import EnvironmentManager
from tasks.task_registry import TASK_REGISTRY

CONFIG_FILE_PATH = "algorithms/sandhi_config.yml"


def evaluate_model(
    model_path: str, 
    task_name: str,  # main() 将传入 "coder" 或 "math"
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
    registry_task_name = TASK_NAME_TO_REGISTRY_KEY.get(task_name, task_name)

    absolute_model_path = Path(model_path).resolve()
    model_name = os.path.basename(absolute_model_path)
    print(f"  Evaluation task: model '{model_name}' on '{task_name}' (as {registry_task_name})")

    task_info = TASK_REGISTRY.get(registry_task_name)
    if not task_info:
        print(f"    Error: Task '{registry_task_name}' (from '{task_name}') not found in TASK_REGISTRY. Skipping.")
        return 0.0

    EvaluatorClass = task_info["evaluator"]
    evaluator = EvaluatorClass(env_manager, env_config, eval_settings)

    model_config = {
        'model_name': model_name,
        'path': str(absolute_model_path),
        'location': 'local'
    }

    result_dict = evaluator.evaluate(model_config, registry_task_name, run_id=1)

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


def process_window_data(profiling_dir: str, tasks: List[str], baseline_accuracies: Dict[str, float]) -> pd.DataFrame:
    """
    Loads and processes the profiling data.
    It filters results for the two specified tasks, merges them into a single
    DataFrame, and calculates the performance delta against the provided baselines.
    """
    # Map internal task names to names found in the CSV file for both metric and base_type.
    TASK_TO_METRIC = {
        "coder": "humaneval",
        "math": "gsm8k" 
    }
    # This new mapping solves the 'code' vs 'coder' mismatch.
    TASK_TO_BASETYPE = {
        "coder": "code",
        "math": "math"
    }

    task1, task2 = tasks
    metric1 = TASK_TO_METRIC.get(task1, task1)
    metric2 = TASK_TO_METRIC.get(task2, task2)
    basetype1 = TASK_TO_BASETYPE.get(task1, task1)
    basetype2 = TASK_TO_BASETYPE.get(task2, task2)
    
    csv_path = os.path.join(profiling_dir, 'window_merge.csv')
    df = pd.read_csv(csv_path)

    # Convert accuracy from proportion (0.x) to percentage (0-100)
    df['accuracy'] = df['accuracy'] * 100

    # Filter using the correct basetype and metric names from the mappings.
    perf1 = df[(df['base_type'] == basetype1) & (df['metric'] == metric1)]
    perf1 = perf1[['start_layer', 'accuracy', 'window_size']].rename(columns={'accuracy': f'{task1}_acc'})

    perf2 = df[(df['base_type'] == basetype2) & (df['metric'] == metric2)]
    perf2 = perf2[['start_layer', 'accuracy', 'window_size']].rename(columns={'accuracy': f'{task2}_acc'})

    # Merge the two dataframes on the window identifiers.
    results = pd.merge(perf1, perf2, on=['start_layer', 'window_size'])

    # This calculation remains correct as it uses percentages for all values.
    results[f'{task1}_delta'] = (results[f'{task1}_acc'] - baseline_accuracies[task1]) / baseline_accuracies[task1]
    results[f'{task2}_delta'] = (results[f'{task2}_acc'] - baseline_accuracies[task2]) / baseline_accuracies[task2]
    
    # Check if the results DataFrame is empty and print a warning if so.
    if results.empty:
        print("\nWARNING: The profiling data processing resulted in an empty DataFrame.")
        print("This is likely due to a mismatch between task names in the script and 'base_type'/'metric' columns in the CSV.")
        print(f"Script is looking for (base_type='{basetype1}', metric='{metric1}') and (base_type='{basetype2}', metric='{metric2}').")
        print("Please check your 'window_merge.csv' file.\n")
        
    return results


def create_yaml_for_merge(layers_to_merge: list, base_language: str, models_subset: Dict[str, str], output_dir: str, total_layers: int) -> str: 
    """
    Generates a mergekit YAML configuration for a given set of layers.
    """
    os.makedirs(output_dir, exist_ok=True)
    lang_names = list(models_subset.keys())
    model_paths = list(models_subset.values())
    model_0_path, model_1_path = model_paths[0], model_paths[1]

    # Determine the base model and the interpolation parameter 't' for unmerged layers.
    if base_language == lang_names[0]:
        base_model_path, unmerged_t = model_0_path, 0.0
    else:
        base_model_path, unmerged_t = model_1_path, 1.0

    slices = []
    current_pos = 0
    for layer_idx in sorted(layers_to_merge):
        # Add a slice for unmerged layers before the current merge window.
        if current_pos < layer_idx:
            slices.append({
                'sources': [
                    {'model': model_0_path, 'layer_range': [int(current_pos), int(layer_idx)]},
                    {'model': model_1_path, 'layer_range': [int(current_pos), int(layer_idx)]}
                ],
                'parameters': {'t': [{'value': unmerged_t}]}
            })
        # Add a slice for the layers to be merged.
        slices.append({
            'sources': [
                {'model': model_0_path, 'layer_range': [int(layer_idx), int(layer_idx + 1)]},
                {'model': model_1_path, 'layer_range': [int(layer_idx), int(layer_idx + 1)]}
            ],
            'parameters': {'t': [{'value': 0.5}]}
        })
        current_pos = layer_idx + 1
    
    # Add a final slice for any remaining unmerged layers.
    if current_pos < total_layers:
        slices.append({
            'sources': [
                {'model': model_0_path, 'layer_range': [int(current_pos), int(total_layers)]},
                {'model': model_1_path, 'layer_range': [int(current_pos), int(total_layers)]}
            ],
            'parameters': {'t': [{'value': unmerged_t}]}
        })

    config_data = {
        'merge_method': 'slerp',
        'base_model': base_model_path,
        'dtype': 'bfloat16',
        'slices': slices
    }

    layers_str = '_'.join(map(str, layers_to_merge))
    filename = f"merge_layers_{layers_str}_base_{base_language}.yaml"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w') as f:
        yaml.dump(config_data, f, sort_keys=False)
        
    return filepath


def run_merge_and_eval(layers_to_merge: List[int], models_subset: Dict[str, str], env_manager, env_config, eval_settings, total_layers, tmp_dir) -> Dict[str, float]:
    """
    A helper function that performs a full merge-and-evaluate cycle for a
    given set of layers, once for each task base.
    """
    accuracies = {}
    for task in models_subset.keys():
        config_path = create_yaml_for_merge(layers_to_merge, task, models_subset, "algorithms/outputs/tmp_iter_configs", total_layers)
        
        # Use a temporary directory to store the merged model, which is cleaned up automatically.
        with tempfile.TemporaryDirectory(dir=tmp_dir) as tmp_model_dir:
            print(f"\n[Mergekit] Merging model (base: {task}) to temporary directory: {os.path.basename(tmp_model_dir)}")
            with open(config_path, "r") as f:
                merge_config = MergeConfiguration.model_validate(yaml.safe_load(f))
            
            # This is where the mergekit library is called to perform the merge.
            run_merge(merge_config, out_path=tmp_model_dir, options=MergeOptions(cuda=True, copy_tokenizer=True))
            
            # Evaluate the newly created merged model.
            accuracies[task] = evaluate_model(tmp_model_dir, task, env_manager, env_config, eval_settings)
            
    return accuracies


def format_time(seconds: float) -> str:
    """Formats seconds into a human-readable 'Xm Ys' string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}m {remaining_seconds}s"


def heuristic_iterative_merge(
    profiling_df: pd.DataFrame,
    total_budget: int,
    models_subset: Dict[str, str],
    importance_weights: Dict[str, float],
    acc_thresholds: Dict[str, float],
    k_candidates: int = 3,
    max_random_tries: int = 3,
    env_manager=None, 
    env_config=None, 
    eval_settings=None, 
    total_layers=None,
    tmp_dir=None
):
    """
    Performs the iterative heuristic search for the best layers to merge.
    """
    tasks = list(models_subset.keys())
    task1, task2 = tasks[0], tasks[1]
    
    unmerged = set(range(total_layers))
    merged_layers = set()
    remaining_budget = total_budget
    consecutive_random_failures = 0

    # Pre-calculate the combined score for ranking candidates.
    profiling_df['combined_score'] = (
        importance_weights[task1] * profiling_df[f'{task1}_delta'] + 
        importance_weights[task2] * profiling_df[f'{task2}_delta']
    ) * profiling_df['window_size']
    
    try:
        scored_dataframe_path = "algorithms/outputs/profiling_with_scores.csv"
        profiling_df.to_csv(scored_dataframe_path, index=False, encoding='utf-8')
        print(f"\n[INFO] DataFrame with deltas and scores saved to: {scored_dataframe_path}")
    except Exception as e:
        print(f"\n[WARN] Failed to save scored dataframe: {e}")

    # Initialize timers for ETA calculation.
    process_start_time = time.time()
    initial_budget = total_budget

    while remaining_budget > 0:
        if consecutive_random_failures >= max_random_tries:
            print(f"\nTerminating due to {consecutive_random_failures} consecutive random-pick failures.")
            break
        
        print(f"\n{'='*20} Iteration | Remaining Budget: {remaining_budget}, Random Failures: {consecutive_random_failures} {'='*20}")

        # --- Candidate Selection ---
        # 1. Filter candidates by remaining budget.
        df = profiling_df.loc[profiling_df["window_size"] <= remaining_budget].copy()
        
        # 2. Filter out candidates that overlap with already merged layers.
        def _is_window_available(row):
            start = int(row["start_layer"])
            size = int(row["window_size"])
            return all(layer in unmerged for layer in range(start, start + size))
        df = df[df.apply(_is_window_available, axis=1)]

        if df.empty:
            print("No more valid merge windows available. Stopping.")
            break

        # 3. Select the top k candidates based on the pre-calculated score.
        top_candidates = df.sort_values("combined_score", ascending=False).head(k_candidates)
        
        # --- Live Evaluation ---
        print(f"--- Evaluating Top-{k_candidates} Candidates ---")
        best_of_top_k = {"score": float("-inf"), "layers": None, "accuracies": None}
        
        iteration_start_time = time.time()
        for i, (_, row) in enumerate(top_candidates.iterrows()):
            layers = list(range(int(row["start_layer"]), int(row["start_layer"]) + int(row["window_size"])))
            print(f"-> Evaluating window: {layers} ({i + 1}/{k_candidates})")
            
            current_accuracies = run_merge_and_eval(layers, models_subset, env_manager, env_config, eval_settings, total_layers, tmp_dir)
            cand_score = sum(importance_weights[task] * current_accuracies.get(task, 0.0) for task in tasks)

            if cand_score > best_of_top_k["score"]:
                best_of_top_k = {"score": cand_score, "layers": layers, "accuracies": current_accuracies}
            
            # Update and display the ETA for the current iteration.
            elapsed_time = time.time() - iteration_start_time
            avg_time_per_candidate = elapsed_time / (i + 1)
            remaining_candidates = k_candidates - (i + 1)
            if remaining_candidates > 0:
                eta_seconds = avg_time_per_candidate * remaining_candidates
                print(f"    ETA for this iteration: {format_time(eta_seconds)}")

        print("--- Top-K Evaluation Complete ---")
        top_k_best_layers = best_of_top_k["layers"]
        top_k_best_accs = best_of_top_k["accuracies"]
        print(f"Best Top-K Candidate: {top_k_best_layers}, Accuracy: {top_k_best_accs}")

        # --- Decision Making ---
        is_satisfied = top_k_best_accs and all(top_k_best_accs.get(task, 0.0) >= acc_thresholds.get(task, 0.0) for task in tasks)
        
        if is_satisfied:
            print("Top-K candidate meets the threshold. Adopting this solution.")
            chosen_layers = top_k_best_layers
            consecutive_random_failures = 0
        else:
            print("Top-K candidates did not meet the threshold.")
            print("--- Attempting a random merge candidate... ---")
            if df.empty:
                print("No available candidates for random selection.")
                break
                
            random_row = df.sample(1).iloc[0]
            random_layers = list(range(int(random_row["start_layer"]), int(random_row["start_layer"]) + int(random_row["window_size"])))
            print(f"-> Randomly selected window: {random_layers}")
            
            random_accuracies = run_merge_and_eval(random_layers, models_subset, env_manager, env_config, eval_settings, total_layers, tmp_dir)
            print(f"Random solution accuracy: {random_accuracies}")
            
            chosen_layers = random_layers
            if all(random_accuracies.get(task, 0.0) >= acc_thresholds.get(task, 0.0) for task in tasks):
                print("Random solution meets the threshold! Resetting failure count.")
                consecutive_random_failures = 0
            else:
                print("Random solution also failed to meet the threshold.")
                consecutive_random_failures += 1
            
        # --- State Update ---
        for layer in chosen_layers:
            unmerged.remove(layer)
            merged_layers.add(layer)
        remaining_budget -= len(chosen_layers)
        print(f"Layers merged in this iteration: {chosen_layers}")
        print(f"All merged layers so far: {sorted(list(merged_layers))}")

        # Update and display the total ETA for the entire process.
        total_elapsed_time = time.time() - process_start_time
        budget_consumed = initial_budget - remaining_budget
        if budget_consumed > 0 and remaining_budget > 0:
            time_per_budget_unit = total_elapsed_time / budget_consumed
            total_eta_seconds = time_per_budget_unit * remaining_budget
            print(f"    [Total ETA] Budget consumed: {budget_consumed}/{initial_budget}. Estimated time remaining: {format_time(total_eta_seconds)}")

    return sorted(list(merged_layers)) if merged_layers else None


def run_main() -> None:
    """The main execution function."""

    # --- Step 0: Load Config and Init Framework ---
    print(f"Loading configuration from {CONFIG_FILE_PATH}...")
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"Error: Config file not found at {CONFIG_FILE_PATH}")
        return

    with open(CONFIG_FILE_PATH, 'r') as f:
        config = yaml.safe_load(f)

    algo_config = config['algorithm_settings']
    heuristic_config = algo_config['heuristic_settings']
    eval_settings = config['evaluation_settings']
    env_config = config['environment_config']

    tasks = algo_config['tasks']
    models_to_merge = algo_config['models_to_merge']
    total_layers = algo_config['total_layers']
    layer_budget = heuristic_config['layer_budget']
    profiling_dir = heuristic_config['profiling_dir']
    run_prefix = algo_config['run_prefix']

    tmp_dir = algo_config['tmp_dir']
    os.environ["TMPDIR"] = tmp_dir
    os.makedirs(tmp_dir, exist_ok=True)

    env_manager = EnvironmentManager(
        env_config['harness_env'], 
        env_config['languages_env']
    )
    print("Evaluation framework initialized.")

    try:
        models_subset = {task: models_to_merge[task] for task in tasks}
    except KeyError as e:
        print(f"Error: Task '{e.args[0]}' is not defined in the models_to_merge dictionary in config.")
        return

    print("--- Starting Heuristic Merge Process ---")
    print(f"Tasks to merge: {tasks}")

    # Step 1: Perform cross-evaluation to establish dynamic baselines.
    print("\n--- Step 1: Performing cross-evaluation to determine baselines ---")
    task1, task2 = tasks[0], tasks[1]
    model1_path, model2_path = models_subset[task1], models_subset[task2]

    print(f"\nEvaluating '{task2}' model on '{task1}' task (to be baseline for {task1})...")
    model2_on_task1_acc = evaluate_model(model2_path, task1, env_manager, env_config, eval_settings)

    print(f"\nEvaluating '{task1}' model on '{task2}' task (to be baseline for {task2})...")
    model1_on_task2_acc = evaluate_model(model1_path, task2, env_manager, env_config, eval_settings)
    
    baseline_accuracies = {
        task1: model2_on_task1_acc,
        task2: model1_on_task2_acc
    }

    if any(acc == 0.0 for acc in baseline_accuracies.values()):
        print(f"Error: Failed to obtain all cross-evaluation baselines: {baseline_accuracies}. Terminating.")
        return
        
    print(f"\nNew cross-evaluation baselines -> {baseline_accuracies}")
    print(f"Interpretation: Performance gains for {task1} will be compared against {model2_on_task1_acc:.4f}, and for {task2} against {model1_on_task2_acc:.4f}.")

    # Step 2: Dynamically set the acceptance thresholds to equal the baselines.
    acc_thresholds = baseline_accuracies
    print(f"Acceptance thresholds dynamically set to baseline values: {acc_thresholds}")
    
    # Step 3: Load and process the profiling data using the new baselines.
    print("\n--- Step 2: Loading and processing profiling data ---")
    profiling_df = process_window_data(profiling_dir, tasks, baseline_accuracies)
    
    # Define the importance weights for each task's score.
    importance_weights = {task: 0.5 for task in tasks}
    
    # Step 4: Run the main heuristic search algorithm.
    print("\n--- Step 3: Running Heuristic Iterative Merge Algorithm ---")
    final_layers = heuristic_iterative_merge(
        profiling_df=profiling_df,
        total_budget=layer_budget,
        models_subset=models_subset,
        importance_weights=importance_weights,
        acc_thresholds=acc_thresholds,
        env_manager=env_manager,
        env_config=env_config,
        eval_settings=eval_settings,
        total_layers=total_layers,
        tmp_dir=tmp_dir
    )

    print("\n--- Process Finished ---")
    if final_layers:
        print(f"Successfully completed merge search! Final recommended layers: {final_layers}")
        
        # Step 5: Build and save the final model based on the search results.
        print("\nBuilding and saving the final model...")
        final_model_dir = f"algorithms/outputs/heuristic_merged_model_final_{run_prefix}_{'_'.join(tasks)}"
        if os.path.exists(final_model_dir):
            shutil.rmtree(final_model_dir)

        final_base_lang = tasks[0]
        final_config_path = create_yaml_for_merge(final_layers, final_base_lang, models_subset, "algorithms/outputs/final_model_config", total_layers)
        print(f"[Mergekit] Creating final model using config: {final_config_path}")
        
        with open(final_config_path, "r") as f:
            merge_config = MergeConfiguration.model_validate(yaml.safe_load(f))
        
        run_merge(merge_config, out_path=final_model_dir, options=MergeOptions(cuda=True, copy_tokenizer=True))
        
        tokenizer_path = list(models_subset.values())[0]
        shutil.copy(os.path.join(tokenizer_path, "tokenizer.json"), final_model_dir)
        shutil.copy(os.path.join(tokenizer_path, "tokenizer_config.json"), final_model_dir)
        
        print(f"Final model saved to: {final_model_dir}")
        
        # Step 6: Perform a final evaluation of the created model.
        print("\nPerforming final evaluation on the merged model...")
        final_accuracies = {}
        for task in tasks:
            final_accuracies[task] = evaluate_model(final_model_dir, task, env_manager, env_config, eval_settings)
            
        print(f"\nFinal Merged Model Performance -> {final_accuracies}")

    else:
        print("Could not find a satisfactory merge solution.")


if __name__ == '__main__':
    # Clean up temporary directories from previous runs.
    if os.path.exists("algorithms/outputs/tmp_iter_configs"):
        shutil.rmtree("algorithms/outputs/tmp_iter_configs")
    if os.path.exists("algorithms/outputs/final_model_config"):
        shutil.rmtree("algorithms/outputs/final_model_config")

    run_main()