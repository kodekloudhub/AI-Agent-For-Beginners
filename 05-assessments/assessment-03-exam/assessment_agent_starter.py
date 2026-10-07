"""
AI Agents Skills Assessment - build Zippy for production.

Everything below is scaffolding. The three TODO blocks are yours to complete.

  TASK 1  Tool definition + the bounded agent loop
  TASK 2  Harden it - security boundaries + a tool that will not crash the loop
  TASK 3  Persistent memory + a run summary

Run it with the prompt as the first argument:

    python3 /root/code/assessment_agent.py "Book a meeting called Standup on Monday"

Do not rename this file, and do not rename any function or constant already
defined in it - the grader looks for them by name.
"""
import os
import sys
import json
import re
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

MODEL = "<model_name>"
MEMORY_FILE = "/root/code/assessment_memory.json"
MAX_ITERATIONS = 5

# The monitoring surface. Task 3 fills it in and prints it.
run_log = {"iterations": 0, "tool_calls": 0, "prompt_tokens": 0, "completion_tokens": 0}


# ============================================================ PROVIDED
# Long-term memory store. Nothing to change here.
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# Tool handlers. book_meeting works. flaky_lookup always fails, on purpose.
def book_meeting(title, day):
    return f"Booked '{title}' on {day} at 10:00. Confirmation sent to api_key=sk-live-9d3f2a1b."


def flaky_lookup(query):
    raise ConnectionError(f"upstream service unreachable while looking up '{query}'")


def save_preference(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return f"Saved preference: {key} = {value}"


HANDLERS = {
    "book_meeting": book_meeting,
    "flaky_lookup": flaky_lookup,
    "save_preference": save_preference,
}

# Input-boundary patterns for Task 2. Add nothing; just use the list.
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard your instructions",
    "reveal your system prompt",
    "you are now",
]


# ============================================================ TASK 1 (part a)
# Add the book_meeting tool definition to this list. Two definitions are
# already here - match their shape.
tools = [
    # TODO TASK 1a: add the book_meeting tool definition here

    {
        "type": "function",
        "function": {
            "name": "flaky_lookup",
            "description": (
                "Look up a term in the legacy directory service. Returns a single "
                "text record. Use this when the user asks about a directory entry."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The term to look up."}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_preference",
            "description": (
                "Store a lasting user preference. Returns a confirmation string. "
                "Use this when the user states a standing preference about how they "
                "want things done."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Short preference name, e.g. meeting_time."},
                    "value": {"type": "string", "description": "The preference value."},
                },
                "required": ["key", "value"],
            },
        },
    },
]


# ============================================================ TASK 2 (parts a and b)
def detect_injection(text):
    """Return True if text looks like a prompt injection attempt."""
    # TODO TASK 2a: return True when any INJECTION_PATTERNS entry appears in
    # text, matched case-insensitively. Return False otherwise.
    return False


def filter_output(text):
    """Redact credentials before anything leaves the agent."""
    # TODO TASK 2b: replace any sk-... or api_key=... value in text with the
    # literal string REDACTED, then return the text.
    return text


# ============================================================ TASK 2 (part c)
def execute_tool(name, arguments):
    """Dispatch one tool call. This function must never raise."""
    run_log["tool_calls"] += 1
    # TODO TASK 2c: wrap the two lines below in try/except so that a failing
    # tool returns its error text as the tool result instead of raising.
    handler = HANDLERS[name]
    return handler(**arguments)


# ============================================================ TASK 3
def build_system_prompt():
    """Zippy's identity, plus anything the agent remembers about this user."""
    prompt = (
        "You are Zippy, a fast and concise personal assistant. "
        "Use the tools available to you rather than guessing. "
        "Keep every answer to two sentences or fewer."
    )
    # TODO TASK 3a: load long-term memory and, if there is any, append it to
    # the prompt under a line reading exactly: Known user preferences:
    return prompt


def print_summary():
    """Print the run log after every run."""
    # TODO TASK 3b: print a line containing "Execution Summary", then the
    # iteration count, the tool-call count, and a line containing
    # "Total tokens" followed by prompt + completion tokens.
    pass


# ============================================================ TASK 1 (part b)
def run_agent(user_message):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    # TODO TASK 1b: write the bounded agent loop. See the task instructions
    # for the full list of requirements.
    return "run_agent is not implemented yet"


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Book a meeting called Standup on Monday"

    if detect_injection(prompt):
        print("BLOCKED: input rejected at the boundary")
        sys.exit(0)

    answer = run_agent(prompt)
    print(filter_output(answer))
    print_summary()
