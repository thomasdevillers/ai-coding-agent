from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

import json
from collections.abc import Callable

available_functions = [
  schema_get_files_info,
  schema_write_file,
  schema_get_file_content,
  schema_run_python_file
]

# function that takes any number of arguments and returns a string
function_map: dict[str, Callable[..., str]] ={
  "get_file_content": get_file_content,
  "get_files_info": get_files_info,
  "write_file": write_file,
  "run_python_file": run_python_file
}

def call_function(tool_call, verbose: bool = False) -> dict:
  function_name = tool_call.name
  function_args = json.loads(tool_call.arguments or "{}")
  if verbose:
    print(f"- Calling function: {function_name}({function_args})")
  else:
    print(f"Calling function: {function_name}")

  function_args["working_directory"] = "./calculator"

  if function_name not in function_map:
    return {
      "type": "function_call_output",
      "call_id": tool_call.call_id,
      "output": f"Error: Unknown function: {function_name}",
    }

  result = function_map[function_name](**function_args)

  return {
      "type": "function_call_output",
      "call_id": tool_call.call_id,
      "output": result,
    }
  