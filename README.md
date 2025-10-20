# Unified LLM Evaluation Pipeline

## Overview

This project provides a unified and automated pipeline for evaluating LLMs across a diverse set of benchmarks, including programming languages and mathematical reasoning. It is designed to simplify complex evaluation workflows by managing multiple Conda environments and centralizing all configurations into a single file.

The core of the pipeline is the main entry point `unified_evaluator.py`, which orchestrates the entire process based on the settings defined in `config.yml`.

## Features

  * **Centralized Configuration**: All settings—models, tasks, evaluation parameters, and paths—are managed in a single `config.yml` file for easy configuration and reproducibility.
  * **Automatic Environment Management**: The pipeline automatically checks if the required Conda environments (`harness_env`, `languages_env`) exist and creates them from their respective `.yml` files if they are missing.
  * **Multi-Environment Orchestration**: Intelligently switches between two separate Conda environments to run different evaluation suites:
      * `harness_env`: Used for the LM Evaluation Harness (HumanEval) and Math Evaluation Harness (GSM8K).
      * `languages_env`: Used for custom evaluation of multiple programming languages (Go, Rust, Java, etc.).
  * **Flexible Task Selection**: Easily specify which tasks to run for a given evaluation.
  * **Robust Execution**: Features a live scoreboard in the terminal, detailed CSV logging for all results, and a modular architecture that is resilient to single-task failures.

## Project Structure

```
.
├── config.yml                    # Master configuration for runs, models, and paths
├── config/
│   ├── harness_env.yml           # Conda environment for math/harness tasks
│   └── languages_env.yml         # Conda environment for language tasks
├── evaluators/
│   ├── base_evaluator.py         # Abstract base class for all evaluators
│   ├── harness_evaluator.py      # Evaluator for GSM8K and HumanEval (lm-eval)
│   └── language_evaluator.py     # Evaluator for Go, Rust, etc.
├── tasks/
│   └── task_registry.py          # Maps tasks to their respective evaluators and environments
├── utils/
│   ├── config_loader.py          # Loads and validates config.yml
│   ├── env_manager.py            # Manages Conda environments (creation and execution)
│   ├── logger.py                 # Handles console logging and the scoreboard
│   └── result_parser.py          # Parses scores from script outputs
├── scripts/                      # Helper scripts
│   └── populate_models_from_dir.py # Populate models list in config.yml
├── vendor/
│   ├── HumanEval/                # Vendored code for language evaluation
│   └── math-evaluation-harness/  # Vendored code for math evaluation
└── unified_evaluator.py          # Main entry point for the pipeline
```

## Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Sherwin6180/unified-llm-eval
    cd unified-llm-eval
    ```

2.  **Ensure Conda is Installed:** This pipeline relies on Conda to manage environments.

    1. Install miniConda3: `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
    2. Accept automatic initialization option for conda (works compatibly with Python venv)
    3. Accept Conda terms:
        ```bash
        # Term 1
        conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
        # Term 2
        conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

        ```


3.  **Populate `vendor/` Directory:** Make sure the `HumanEval` and `math-evaluation-harness` codebases are correctly placed inside the `vendor/` directory.

4.  **Set Up Conda Environments:** You have two options for creating the necessary Conda environments.

      * **Option 1: Automatic Creation (Recommended)**
        Simply run the main script. The pipeline is designed to automatically detect if `harness_env` and `languages_env` are missing and will create them for you using the `.yml` files in the `config/` directory. This is the easiest, hands-off approach.

        **Prerequisite**: Install `unified_evaluator.py`'s dependencies first:
        ```bash
        # Optional: set up venv
        python3 -m venv /path/to/new/virtual/environment # or python

        # Required:
        pip install -r requirements.txt
        ```

        **Run the main script**
        ```bash
        python unified_evaluator.py
        ```

      * **Option 2: Manual Creation**
        If you prefer to create the environments manually before the first run, execute the following commands in your terminal:

        ```bash
        # Create the environment for math and harness tasks
        conda env create -f config/harness_env.yml

        # Create the environment for multi-language evaluation
        conda env create -f config/languages_env.yml
        ```

5.  **Ensure Compilers are Installed (for Language Tasks)**
    To evaluate performance on compiled programming languages (e.g., Rust, Go, Java, C++), the corresponding compilers must be installed and accessible. The evaluation script works by compiling and running the code generated by the model.The current `languages_env.yml` is already configured with `rust`.

      1. Consider configuring compilers using Docker Containers or Podman
      2. Refer to MultiPL-E's repo: [MultiPL-E](https://github.com/nuprl/MultiPL-E)

6.  **Configure `config.yml`:** Before running, open `config.yml` and customize it for your evaluation run. See the detailed `Configuration` section below.

## Configuration (`config.yml`)

The `config.yml` file is the single source of truth for the pipeline. It is organized into four main sections:

```yaml
# 1. Settings for the specific evaluation run
run_settings:
  task_name: "Final Evaluation Run"
  description: "Evaluating deepseek-coder on all tasks."
  tasks_to_run:
    - "all"

# 2. List of models to evaluate
models:
  - model_name: "deepseek-coder-instruct"
    path: "/path/to/your/model"
    type: "instruct"
    description: "Base instructed model"
    location: "local"

# 3. General evaluation parameters
evaluation_settings:
  gpu_ids: "0,1"
  timeout_minutes: 30
  runs_per_eval: 1
  output_dir: "./evaluation_results"

# 4. Environment names and paths to vendored code
environment_config:
  harness_env: "harness_env" # DON'T CHANGE
  languages_env: "languages_env" # DON'T CHANGE
  math_harness_dir: "./vendor/math-evaluation-harness" # DON'T CHANGE
  language_eval_dir: "./vendor/HumanEval" # DON'T CHANGE
```

### `run_settings`

This section defines the scope of the current evaluation run.

  * `task_name`, `description`: Metadata for your run, used in logs and output filenames.
  * `tasks_to_run`: A list specifying which tasks to execute. This is a critical parameter.
      * You can specify individual tasks: `["rust", "humaneval"]`.
      * You can use `"all"` to run every supported task: `["all"]`.
      * **Available Tasks**:
          * **Harness (`harness_env`)**: `humaneval`, `gsm8k-cot`, `gsm8k-pal`
          * **Languages (`languages_env`)**: `python`, `cpp`, `java`, `cs`, `php`, `ts`, `js`, `sh`, `scala`, `rust`, `go`, `julia`, `rb`, `ocaml`

### `models`

A list of model objects to be evaluated.

  * `model_name`: A unique identifier for the model.
  * `path`: The absolute path to the model's directory on your filesystem.
  * `type`: A category for the model (e.g., "instruct", "base"). Used for logging.
  * `description`: Optional descriptive text.
  * `location`: Local model ("local") or huggingface online model ("hf"). If location is not specified, default to "local".

### `evaluation_settings`

Parameters that control the evaluation process.

  * `gpu_ids`: A comma-separated string of GPU IDs to use (e.g., `"0,1,2,3"`).
  * `timeout_minutes`: The maximum time in minutes to allow for a single task before it times out. Default is 30.
  * `runs_per_eval`: How many times to repeat each evaluation task for a given model. The final CSV will include a `run_id` column.
  * `output_dir`: The directory where result CSVs and logs will be saved.
  * `temperature`: Ranging from 0 to 1.0
  * `batch size`: To set batch size for gsm8k, you first need to comment out `--use_vllm` in ./evaluators/harness_evaluator.py. Otherwise, vllm will set the batch size automatically. Also, you need to make sure you are only using 1 GPU if you want to try different batch sizes for gsm8k evaluations.

### `environment_config`

Defines the names of the Conda environments and paths to the evaluation scripts. Usually you don't need to change these.

  * `harness_env`, `languages_env`: The names of the two Conda environments.
  * `math_harness_dir`, `language_eval_dir`: The paths of two vendors.

## Utility: Populate models list from a directory

Use the helper script to auto-generate the `models` section in `config.yml` from all immediate subdirectories under a root directory (non-recursive). The rest of the YAML remains unchanged.

```bash
python scripts/populate_models_from_dir.py \
  --root "/scratch/shared_dir/oduran6/" \
  --config "config.yml" \
  --model-name-prefix "deepseek-coder-instruct" \
  --type "instruct" \
  --description "Auto-populated model"
```

Notes:
- Only immediate subdirectories are considered as model paths.
- The `models` list is replaced; other sections are preserved.
- `model_name` is constructed as `<prefix>-<leaf-dir>` (customize with `--model-name-prefix`).

## Usage

Once `config.yml` is configured, run the entire pipeline with a single command:

```bash
python unified_evaluator.py
```

To use a different configuration file, specify it with the `--config` flag:

```bash
python unified_evaluator.py --config config/my_special_run.yml
```

## Extensibility

Adding a new task is straightforward:

1.  Add the new task name to `tasks/task_registry.py`, mapping it to an environment and an `Evaluator` class.
2.  If the task requires new execution logic, create a new class in `evaluators/` that inherits from `BaseEvaluator`.
3.  If a new environment is needed, add its `.yml` file to `config/` and update the logic in `utils/env_manager.py`.