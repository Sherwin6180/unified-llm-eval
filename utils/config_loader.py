# utils/config_loader.py
import yaml
from pathlib import Path

def load_yaml_config(config_path):
    """
    Loads and validates the master YAML configuration file.
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

    return config