import os
from pathlib import Path
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory) # holds the abs path of the current working directory
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_file])
    valid_target_dir = common_path == working_dir_abs

    if not valid_target_dir:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not Path(target_file).is_file():
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file'

    command = ["python", target_file]
    if args:
      command.extend(args)
    process = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)
    output_string = ""
    if process.returncode != 0:
      return f'Process exited with code {process.returncode}'
    if not process.stderr and not process.stdout:
      return 'No output produced'
    output_string += f"STDOUT: {process.stdout} STDERR: {process.stderr}"
    return output_string
  except Exception as e:
    return f'Error: executing Python file: {e}'

schema_run_python_file = {
    "type": "function",
    "name": "run_python_file",
    "description": "Executes a Python (.py) file inside the working directory and returns its stdout and stderr. The script runs with the working directory as its cwd and is killed after 30 seconds.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the .py file to run, relative to the working directory (e.g. 'main.py' or 'tests.py').",
            },
            "args": {
              "type": "array",
              "items": {"type": "string"},
              "description": "Optional command-line arguments passed to the script, in order (e.g. ['3 + 5']). Omit if the script takes no arguments."
            }
        },
        "required": ["file_path"],
    },
}