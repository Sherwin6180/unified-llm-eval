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

    else: # Default for language tasks using eval_pal.py
        match = re.search(r"Score is\s*(\d+\.?\d+)", stdout)
        if match:
            return float(match.group(1)) * 100

    return None