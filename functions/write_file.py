from pathlib import Path
import os


def write_file(working_directory: str, file_path: str, content:str) -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory) # holds the abs path of the current working directory
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    common_path = os.path.commonpath([working_dir_abs, target_file])
    valid_target_dir = common_path == working_dir_abs

    if not valid_target_dir:
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if Path(target_file).is_dir():
      return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
     return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "name": "write_file",
    "description": "Writes text to a file inside the working directory. Creates the file and any missing parent directories if needed. If the file already exists, its entire contents are replaced, so include the full desired file content, not just the changes.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write, relative to the working directory (e.g. 'notes.txt' or 'pkg/new_module.py'). Must not be an existing directory.",
            },
            "content": {
              "type": "string",
              "description": "The complete text to write to the file. This replaces any existing content."
            }
        },
        "required": ["file_path", "content"],
    },
}