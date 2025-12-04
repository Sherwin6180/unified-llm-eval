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
    def __init__(self, harness_env_name, languages_env_name, goedelv2_env_name="goedelv2"):
        self.harness_env = harness_env_name
        self.languages_env = languages_env_name
        self.goedelv2_env = goedelv2_env_name
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
            self.languages_env: "config/languages_env.yml",
            self.goedelv2_env: "config/goedelv2_env.yml"
        }
        for env_name, yaml_path in env_yaml_map.items():
            if not self._env_exists(env_name):
                self._create_env_from_yaml(env_name, yaml_path)

    def run_in_env(self, env_name, command_args, cwd=None, timeout=None, stream_output=True):
        """
        Runs a command within the specified Conda environment.
        
        Args:
            env_name: Name of the conda environment
            command_args: List of command arguments
            cwd: Working directory
            timeout: Timeout in seconds
            stream_output: If True, stream output to console in real-time
        """
        # If env_name is "virtualenv", use the user's virtualenv
        if env_name == "ian6-venv":
            # TODO: change this command accordingly.
            venv_activate = "/nethome/ian6/ian6-myenv/bin/activate"
            # Run command with virtualenv activated
            full_command = f"source {venv_activate} && " + " ".join(command_args)
            result = subprocess.run(
                full_command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result

        conda_command = [
            "conda", "run", "-n", env_name, "--no-capture-output"
        ] + command_args
        
        log(f"Executing in '{env_name}': {' '.join(conda_command)}")
        
        try:
            if stream_output:
                # Use Popen for real-time output streaming
                import sys
                process = subprocess.Popen(
                    conda_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=cwd,
                    env=os.environ,
                    bufsize=1,  # Line buffered
                    universal_newlines=True
                )
                
                stdout_lines = []
                try:
                    for line in process.stdout:
                        print(line, end='', flush=True)  # Real-time output
                        stdout_lines.append(line)
                except Exception:
                    pass
                
                process.wait(timeout=timeout)
                
                # Create a CompletedProcess-like object
                result = subprocess.CompletedProcess(
                    args=conda_command,
                    returncode=process.returncode,
                    stdout=''.join(stdout_lines),
                    stderr=''
                )
                return result
            else:
                # Original behavior: capture output
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
            result = subprocess.CompletedProcess(conda_command, returncode=-1, stdout='', stderr='')
            result.timeout = True
            return result
        except Exception as e:
            log(f"An unexpected error occurred during command execution: {e}")
            raise