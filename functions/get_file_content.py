import os
from pathlib import Path
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path:str) -> str:
    try :
      working_dir_abs = os.path.abspath(working_directory) # holds the abs path of the current working directory
      target_file = os.path.join(working_dir_abs, file_path)
      common_path = os.path.commonpath([working_dir_abs, target_file])
      valid_target_dir = common_path == working_dir_abs

      if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
      if not Path(target_file).is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

      with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
          file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

      return file_content_string
      
    except Exception as e:
      return f"Error: {e}"
       
schema_get_file_content = {
    "type": "function",
    "name": "get_file_content",
    "description": f"Reads and returns the text content of a file inside the working directory. Content longer than {MAX_CHARS} characters is truncated, with a note appended saying so.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to read, relative to the working directory (e.g. 'main.py' or 'pkg/calculator.py'). Must be a regular file, not a directory.",
            },
        },
        "required": ["file_path"],
    },
}