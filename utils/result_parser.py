# utils/result_parser.py
import re

def parse_score(stdout, task_name):
    """
    Parses the score from the stdout of different evaluation scripts.
    Returns:
        float: The parsed score (as a percentage), or None if parsing fails.
    """
    if task_name == "humaneval":
        match = re.search(r"\|\s*humaneval\s*\|.*?\|\s*pass@1\s*\|.*?(\d+\.?\d*)", stdout)
        if match:
            return float(match.group(1)) * 100
        
        match = re.search(r"'pass@1':\s*(\d+\.?\d+)", stdout)
        if match:
            return float(match.group(1)) * 100
            
    elif task_name in ["gsm8k-cot", "gsm8k-pal"]:
        # --- FIX: Add a more robust regex and a fallback pattern ---
        # Method 1: Look for the 'acc' key in a dictionary format
        match = re.search(r"'acc':\s*([\d\.]+)", stdout)
        if match:
            return float(match.group(1)) # GSM8K score is already a percentage
        
        # Method 2 (Fallback): Look for lines that just contain the score, like "8.21  8.3"
        lines = stdout.strip().split('\n')
        for line in reversed(lines):
             # This pattern looks for a line starting with a float, possibly followed by another
            if re.match(r'^\d+\.\d+(\s+\d+\.\d+)?$', line.strip()):
                score = float(line.strip().split()[0])
                return score

    # For tinyBenchmarks tasks (tinyMMLU, tinyArc, tinyHellaswag, etc.)
    # These use acc_norm with custom aggregation functions
    if task_name.startswith("tiny"):
        # Pattern 1: acc_norm in table format
        # |tinyMMLU|...|acc_norm|...|0.5234|±|0.0125|
        match = re.search(r'\|\s*' + re.escape(task_name) + r'\s*\|.*?\|\s*acc_norm\s*\|.*?\|([0-9.]+)\|', stdout)
        if match:
            return float(match.group(1)) * 100
        
        # Pattern 2: acc_norm in dictionary format
        match = re.search(r"'acc_norm':\s*([0-9.]+)", stdout)
        if match:
            return float(match.group(1)) * 100
        
        # Pattern 3: JSON format with acc_norm
        match = re.search(r'"acc_norm[^"]*":\s*([0-9.]+)', stdout)
        if match:
            return float(match.group(1)) * 100

    # For lm-eval-harness tasks (medqa, mmlu, etc.)
    # These tasks use lm-eval and output results in various formats
    
    # Pattern 1: lm-eval table format
    # |task_name|...|acc|...|0.2742|±|0.0125|
    match = re.search(r'\|\s*[\w_]+\s*\|.*?\|\s*acc\s*\|.*?\|([0-9.]+)\|', stdout)
    if match:
        return float(match.group(1)) * 100
    
    # Pattern 2: Dictionary-like format from lm-eval
    # 'task_name': {'acc': 0.2742, ...}
    match = re.search(r"'acc':\s*([0-9.]+)", stdout)
    if match:
        return float(match.group(1)) * 100
    
    # Pattern 3: JSON format from lm-eval
    # {"task_name": {"acc,none": 0.2742}}
    match = re.search(r'"acc[^"]*":\s*([0-9.]+)', stdout)
    if match:
        return float(match.group(1)) * 100
    
    # Pattern 4: lm-eval final results line
    # |task_name|1|none|0|acc|↑|0.2742|±|0.0125|
    match = re.search(r'\|\s*acc\s*\|[^|]*\|([0-9.]+)\s*\|', stdout)
    if match:
        return float(match.group(1)) * 100

    # Default for language tasks using eval_pal.py
    match = re.search(r"Score is\s*(\d+\.?\d+)", stdout)
    if match:
        return float(match.group(1)) * 100

    return None
