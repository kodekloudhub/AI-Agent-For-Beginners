"""Reference solution for Assessment 3 - the full exam agent.

This is the starter file with the three TODO blocks filled in (see
`solution_sample.md` for the exam-grader rationale behind each piece).
"""
import os
import sys
import json
import re
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

MODEL = "<model_name>"
MEMORY_FILE = "/root/code/assessment_memory.json"
MAX_ITERATIONS = 5

run_log = {"iterations": 0, "tool_calls": 0, "prompt_tokens": 0, "completion_tokens": 0}


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE) as f:
            return json.load(f)
    return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


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

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard your instructions",
    "reveal your system prompt",
    "you are now",
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "book_meeting",
            "description": (
                "Book a meeting on the user's calendar. Returns a confirmation "
                "string with the booked time. Use this when the user asks to "
                "schedule, book, or set up a meeting."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Short meeting title."},
                    "day": {
                        "type": "string",
                        "description": "Day of the week for the meeting.",
                        "enum": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    },
                },
                "required": ["title", "day"],
            },
        },
    },
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
                "Use this when the user states a standing preference about how "
                "they want things done."
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


def detect_injection(text):
    lowered = text.lower()
    return any(pattern in lowered for pattern in INJECTION_PATTERNS)


def filter_output(text):
    text = re.sub(r"sk-[A-Za-z0-9\-]+", "REDACTED", text)
    text = re.sub(r"api_key=\S+", "api_key=REDACTED", text)
    return text


def execute_tool(name, arguments):
    run_log["tool_calls"] += 1
    try:
        handler = HANDLERS[name]
        return handler(**arguments)
    except Exception as e:
        return f"Error: {e}"


def build_system_prompt():
    prompt = (
        "You are Zippy, a fast and concise personal assistant. "
        "Use the tools available to you rather than guessing. "
        "Keep every answer to two sentences or fewer."
    )
    memory = load_memory()
    if memory:
        prompt += "\n\nKnown user preferences:\n"
        for k, v in memory.items():
            prompt += f"- {k}: {v}\n"
    return prompt


def print_summary():
    total = run_log["prompt_tokens"] + run_log["completion_tokens"]
    print("\n--- Execution Summary ---")
    print(f"Iterations: {run_log['iterations']}")
    print(f"Tool calls: {run_log['tool_calls']}")
    print(f"Total tokens: {total}")


def run_agent(user_message):
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_message},
    ]

    for i in range(MAX_ITERATIONS):
        run_log["iterations"] += 1

        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )
        if response.usage:
            run_log["prompt_tokens"] += response.usage.prompt_tokens
            run_log["completion_tokens"] += response.usage.completion_tokens

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)
            for call in choice.message.tool_calls:
                args = json.loads(call.function.arguments)
                result = execute_tool(call.function.name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result),
                    }
                )
            continue

        return choice.message.content

    return "Stopped: reached the iteration limit before finishing."


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Book a meeting called Standup on Monday"

    if detect_injection(prompt):
        print("BLOCKED: input rejected at the boundary")
        sys.exit(0)

    answer = run_agent(prompt)
    print(filter_output(answer))
    print_summary()
