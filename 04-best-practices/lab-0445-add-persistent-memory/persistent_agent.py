"""Lab 0445 - Add Persistent Memory.

Stores user preferences in a JSON file on disk so they survive across runs,
and loads them into the system prompt at the start of every conversation.
"""
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

MAX_ITERATIONS = 10
MEMORY_FILE = "/root/code/agent_memory.json"


def check_calendar(date):
    return f"You have a team standup at 9am and a project review at 2pm on {date}."


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_preference(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return f"Saved: {key} = {value}"


def forget_preference(key):
    memory = load_memory()
    if key in memory:
        del memory[key]
        save_memory(memory)
        return f"Forgotten: {key}"
    return f"Key not found: {key}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check what events are scheduled for a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "The date to check, e.g. today"}
                },
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_preference",
            "description": "Save a user preference to persistent memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "The preference name"},
                    "value": {"type": "string", "description": "The preference value"},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "forget_preference",
            "description": "Remove a stored user preference from memory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "The preference key to remove"}
                },
                "required": ["key"],
            },
        },
    },
]


def run_agent(user_input):
    memory = load_memory()
    base_prompt = "You are a helpful personal assistant. Use your tools when you need real data."
    if memory:
        sys_prompt = f"{base_prompt}\n\nKnown user preferences: {json.dumps(memory)}"
    else:
        sys_prompt = base_prompt

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_input},
    ]

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="<model_name>",
            messages=messages,
            tools=tools,
        )
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "stop":
            return response.choices[0].message.content
        if finish_reason == "tool_calls":
            messages.append(response.choices[0].message)
            for tool_call in response.choices[0].message.tool_calls:
                fn_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                try:
                    if fn_name == "check_calendar":
                        result = check_calendar(**args)
                    elif fn_name == "save_preference":
                        result = save_preference(**args)
                    elif fn_name == "forget_preference":
                        result = forget_preference(**args)
                    else:
                        result = f"Unknown tool: {fn_name}"
                except Exception as e:
                    result = f"Tool error: {e}"
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                )
        else:
            break


if __name__ == "__main__":
    user_input = "Forget that I am vegetarian."
    print(f"\nUser: {user_input}")
    response = run_agent(user_input)
    print(f"\nAssistant: {response}")
