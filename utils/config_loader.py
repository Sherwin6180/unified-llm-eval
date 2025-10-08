# utils/config_loader.py
import yaml
import os
from pathlib import Path

def load_yaml_config(config_path):
    """
    Loads and validates the master YAML configuration file.
    Expands model paths to absolute paths.
    """
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Basic validation
    required_keys = ['run_settings', 'models', 'evaluation_settings', 'environment_config']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key '{key}' in {config_path}")
            
    if 'tasks_to_run' not in config['run_settings']:
        raise ValueError("Missing required key 'tasks_to_run' in 'run_settings' section.")

    # Expand model paths to absolute paths
    for model in config['models']:
        if 'path' in model:
            original_path = model['path']
            # First expand ~ and environment variables
            expanded = os.path.expanduser(original_path)
            expanded = os.path.expandvars(expanded)
            # Then resolve to absolute path
            absolute = os.path.abspath(expanded)
            model['path'] = absolute
            
            # Log the path expansion for debugging (optional but helpful)
            if original_path != absolute:
                print(f"[Config] Expanded model path:")
                print(f"  From: {original_path}")
                print(f"  To:   {absolute}")

    return config
