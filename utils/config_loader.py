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

    for model in config['models']:
        if 'path' not in model:
            continue

        original_path = model['path']
        
        location_type = model.get('location', 'local').lower()

        if location_type == 'local':
            expanded = os.path.expanduser(original_path)
            expanded = os.path.expandvars(expanded)
            absolute = os.path.abspath(expanded)
            model['path'] = absolute
            
            if original_path != absolute and original_path != absolute.split('/')[-1]:
                print(f"[Config] Expanded local model path:")
                print(f"  From: {original_path}")
                print(f"  To:   {absolute}")
        
        elif location_type == 'hf':
            print(f"[Config] Detected Hugging Face model ID (location='hf'): {original_path}")
        
        else:
            raise ValueError(f"Unknown location type '{model.get('location')}' for model '{model.get('model_name')}' in {config_path}")

    return config
