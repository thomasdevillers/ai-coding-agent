import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError('You need to set the openai api key')
    client = OpenAI(
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="AIChatBot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output for detailed logging")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role":"user", "content": args.user_prompt}
    ]

    prev_tool_call_id = None
    prev_response_id = None
    for _ in range(20):
        response = client.responses.create(
            model="gpt-6-luna",
            input=messages, # type: ignore,
            tools=available_functions, # type: ignore
            previous_response_id=prev_response_id if prev_response_id is not None else None
        )

        if not response.usage:
            raise RuntimeError("API request to openAI failed.")

        prompt_tokens = response.usage.input_tokens
        completion_tokens = response.usage.output_tokens

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {completion_tokens}")

        messages.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            print(response.output_text)
            break
        
        for item in response.output:
            if item.type == "function_call":
                result_message = call_function(item, args.verbose)
                if not result_message["output"]:
                    raise Exception("Tool call failed.")
                if args.verbose:
                    print(f"-> {result_message['output']}")
                messages.append(result_message)
    tool_calls = [
    item for item in response.output
    if item.type == "function_call"
    ]

    if tool_calls:
        print(f"Error: unable to action this request. please try again with a different prompt.")
        sys.exit(1)

if __name__ == "__main__":
    main()
