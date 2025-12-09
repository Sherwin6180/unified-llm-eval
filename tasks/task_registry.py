# tasks/task_registry.py
from evaluators.language_evaluator import LanguageEvaluator
from evaluators.harness_evaluator import HarnessEvaluator
from evaluators.simple_evaluator import SimpleEvaluator

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
    
    # Tasks for direct execution (no conda env)
    "medqa_4options": {"evaluator": SimpleEvaluator, "env": None},
    "mmlu_international_law": {"evaluator": SimpleEvaluator, "env": None},
    "mmlu_professional_accounting": {"evaluator": SimpleEvaluator, "env": None},
    "wmdp_cyber": {"evaluator": SimpleEvaluator, "env": None},
    "sst2": {"evaluator": SimpleEvaluator, "env": None},
    "truthfulqa_mc2": {"evaluator": SimpleEvaluator, "env": None},
    "global_mmlu_full_en_professional_law": {"evaluator": SimpleEvaluator, "env": None},
    "mmlu_econometrics": {"evaluator": SimpleEvaluator, "env": None},
    "ceval-valid_middle_school_biology": {"evaluator": SimpleEvaluator, "env": None},
    "tinyMMLU": {"evaluator": SimpleEvaluator, "env": None},
    "financial_tweets": {"evaluator": SimpleEvaluator, "env": None},
    "ceval-valid_middle_school_biology": {"evaluator": SimpleEvaluator, "env": None},

    # financial candiates
    "mmlu_corporate_finance": {"evaluator": SimpleEvaluator, "env": None},
    "mmlu_management": {"evaluator": SimpleEvaluator, "env": None},

    # Medical:
    "mmlu_professional_medicine": {"evaluator": SimpleEvaluator, "env": None},
    # Legal:
    "mmlu_professional_law": {"evaluator": SimpleEvaluator, "env": None},
    # Wellness:
    "persona_maximizing-human-well-being-over-HHH": {"evaluator": SimpleEvaluator, "env": None},

    # replacing toxicity
    "toxigen": {"evaluator": SimpleEvaluator, "env": None},



}

ALL_TASKS = list(TASK_REGISTRY.keys())
