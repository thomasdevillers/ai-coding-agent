import os
from pathlib import Path

def get_files_info(working_directory: str, directory: str = ".") -> str:
  try: 
    # fetches current working directory and appends the variable in working_directory
    working_dir_abs = os.path.abspath(working_directory) # holds the abs path of the current working directory
    full_path = os.path.join(working_dir_abs, directory)
    target_dir = os.path.normpath(full_path)
    common_path = os.path.commonpath([working_dir_abs, target_dir])
    valid_target_dir = common_path == working_dir_abs
    if not valid_target_dir:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
      return f'Error: "{directory}" is not a directory'
    file_info = []
    for item in Path(target_dir).iterdir():
        try: 
          data = f"-{item.name}: file_size={item.stat().st_size} bytes, is_dir={item.is_dir() == True}"
          file_info.append(data)
        except Exception as e:
          return "Error: {e}"
    return "\n".join(file_info)
  except Exception as e:
    return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "name": "get_files_info",
    "description": "Lists the immediate contents (non-recursive) of a directory inside the working directory. Each entry shows its name, size in bytes, and whether it is a directory. Use this to explore the project structure before reading or writing files.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory to list, relative to the working directory (e.g. 'pkg'). Defaults to '.', the working directory itself. Paths outside the working directory are rejected.",
            },
        },
        "required": [],
    },
}

  
  