# AI Agent

This is a small AI coding assistant that runs in your terminal. You type a request in plain English, like "run main.py" or "fix the bug in the calculator," and the AI works out which steps to take. It can look around a folder, read files, run Python scripts, and write files on its own until the job is done.

## How it works

A normal chatbot can only send text back. This one also has **tools**: Python functions it is allowed to call. The program runs in a loop:

1. Your request is sent to the AI model, along with a list of the tools it can use.
2. The model either answers you directly or asks to use a tool (for example, "read `pkg/calculator.py`").
3. The program runs that tool and sends the result back to the model.
4. Steps 2–3 repeat until the model has a final answer, up to 20 times.

It's a bit like texting a friend who can't see your computer. They ask "what's in that file?", you send them the contents, and they tell you what to do next. The difference is that this program answers those questions automatically.

## The tools

All tools live in the `functions/` folder.

| Tool | What it does |
|---|---|
| `get_files_info` | Lists the files and folders in a directory, with their sizes |
| `get_file_content` | Reads a file and returns its text (cut off after 10,000 characters) |
| `write_file` | Creates or overwrites a file, and creates any missing folders |
| `run_python_file` | Runs a Python file and returns what it printed (stops after 30 seconds) |

Each tool also has a **schema**, a short description of what the tool does and which inputs it takes. The model reads these schemas to decide which tool to use.

## Safety

Letting an AI read, write, and run files is risky, so the agent is locked inside one folder: `calculator/`. Every tool checks that the path it was given stays inside that folder. If the AI tries something like `../secret.txt`, the tool refuses and returns an error. The working directory is set by the program, not by the AI, so the AI can't change it.

## Project layout

```
ai-agent/
├── main.py              # Starts the program and runs the agent loop
├── call_function.py     # Connects the model's tool requests to the real Python functions
├── prompts.py           # The system prompt: instructions that tell the AI how to behave
├── config.py            # Settings, like the maximum number of characters to read
├── functions/           # The four tools
├── calculator/          # The sandbox project the AI is allowed to work on
└── test_*.py            # Scripts that test each tool by hand
```

The `calculator/` folder is a simple calculator app that gives the agent something to practise on. You can ask the agent to run it, explain it, or change it.

## Setup

You need [uv](https://docs.astral.sh/uv/) and an OpenAI API key.

1. Install the dependencies:
   ```bash
   uv sync
   ```
2. Create a file called `.env` in the project folder containing your key:
   ```
   OPENAI_API_KEY=your-key-here
   ```
   Never share this file or commit it to Git. Anyone with your key can spend your money.

## Usage

```bash
uv run main.py "your request here"
```

Examples:

```bash
uv run main.py "what files are in the root directory?"
uv run main.py "run main.py with the argument '3 + 5'"
uv run main.py "read pkg/calculator.py and explain how it works"
```

Add `--verbose` to see every tool call, its result, and how many tokens each request used:

```bash
uv run main.py "run tests.py" --verbose
```

## Testing the tools

Each tool has its own test script. You can run them without an API key:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```
