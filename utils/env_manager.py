# utils/env_manager.py
import subprocess
import shutil
import os
from .logger import log

class EnvironmentManager:
    """
    Manages Conda environments, including checking for existence,
    creation from YAML, and running commands within them.
    """
    def __init__(self, harness_env_name, languages_env_name):
        self.harness_env = harness_env_name
        self.languages_env = languages_env_name
        self.conda_path = self._find_conda()

    def _find_conda(self):
        """Find the path to the conda executable."""
        conda_exe = shutil.which("conda")
        if not conda_exe:
            raise FileNotFoundError("Conda executable not found. Please ensure Conda is installed and in your PATH.")
        return conda_exe

    def _env_exists(self, env_name):
        """Check if a Conda environment exists."""
        try:
            result = subprocess.run(
                [self.conda_path, "env", "list"],
                capture_output=True, text=True, check=True
            )
            return any(line.split()[0] == env_name for line in result.stdout.splitlines() if line and not line.startswith('#'))
        except subprocess.CalledProcessError as e:
            log(f"Error checking for Conda environments: {e.stderr}")
            return False

    def _create_env_from_yaml(self, env_name, yaml_file):
        """Create a Conda environment from a YAML file."""
        if not os.path.exists(yaml_file):
            raise FileNotFoundError(f"YAML file not found: {yaml_file}. Cannot create environment '{env_name}'.")
        
        log(f"Environment '{env_name}' not found. Creating from {yaml_file}...")
        try:
            # Using Popen for real-time output streaming
            process = subprocess.Popen(
                [self.conda_path, "env", "create", "-f", yaml_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # DONE: FIX - Prevent Race Condition
            process.wait()
            
            if process.returncode != 0:
                 raise subprocess.CalledProcessError(process.returncode, process.args)

            log(f"Environment '{env_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            log(f"Failed to create Conda environment '{env_name}'. Please check the logs above.")
            raise

    def check_environments(self):
        """
        Check for the existence of required environments and create them if they
        are defined in YAML files (e.g., config/harness_env.yml, config/languages_env.yml).
        """
        env_yaml_map = {
            self.harness_env: "config/harness_env.yml",
            self.languages_env: "config/languages_env.yml"
        }
        for env_name, yaml_path in env_yaml_map.items():
            if not self._env_exists(env_name):
                self._create_env_from_yaml(env_name, yaml_path)

    def run_in_env(self, env_name, command_args, cwd=None, timeout=None):
        """
        Runs a command within the specified Conda environment.
        """
        conda_command = [
            "conda", "run", "-n", env_name, "--no-capture-output"
        ] + command_args
        
        log(f"Executing in '{env_name}': {' '.join(conda_command)}")
        try:
            result = subprocess.run(
                conda_command,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=timeout,
                env=os.environ
            )
            return result
        except FileNotFoundError:
            log(f"Error: 'conda' command not found. Is conda installed and in your PATH?")
            raise
        except subprocess.TimeoutExpired as e:
            log(f"Command timed out after {timeout} seconds.")
            return subprocess.CompletedProcess(e.args, timeout=True, stdout=e.stdout, stderr=e.stderr)
        except Exception as e:
            log(f"An unexpected error occurred during command execution: {e}")
            raise