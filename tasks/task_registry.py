# tasks/task_registry.py
from evaluators.language_evaluator import LanguageEvaluator
from evaluators.harness_evaluator import HarnessEvaluator

# This registry is the single source of truth for mapping tasks to their
# respective evaluation logic and environment.
TASK_REGISTRY = {
    # Tasks for harness_env
    "humaneval": {"evaluator": HarnessEvaluator, "env": "harness_env"},
    "gsm8k-cot": {"evaluator": HarnessEvaluator, "env": "harness_env"},
    "gsm8k-pal": {"evaluator": HarnessEvaluator, "env": "harness_env"},
    
    # Tasks for languages_env
    "python":    {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "cpp":       {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "java":      {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "cs":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "php":       {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "ts":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "js":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "sh":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "scala":     {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "rust":      {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "go":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "julia":     {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "rb":        {"evaluator": LanguageEvaluator, "env": "languages_env"},
    "ocaml":     {"evaluator": LanguageEvaluator, "env": "languages_env"},
}

ALL_TASKS = list(TASK_REGISTRY.keys())