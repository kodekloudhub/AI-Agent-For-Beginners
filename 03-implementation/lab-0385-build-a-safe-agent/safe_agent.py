"""Lab 0385 - Build a Safe Agent.

Takes the baseline tool-calling agent and adds the three safety nets a
production loop needs: wrap tools in try/except, demonstrate a tool that
always fails, and bound the loop with MAX_ITERATIONS plus a graceful exit.
"""
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

model = "<model_name>"
MAX_ITERATIONS = 10

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the user's calendar for events on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "The date to check"}
                },
                "required": ["date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "flaky_tool",
            "description": "Search for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
]


def check_calendar(date):
    return "10am: Team standup, 2pm: Dentist appointment"


def flaky_tool(query):
    raise Exception("Service unavailable")


def execute_tool(name, args):
    try:
        if name == "check_calendar":
            return check_calendar(**args)
        if name == "flaky_tool":
            return flaky_tool(**args)
        return "Unknown tool"
    except Exception as e:
        return f"Error: {str(e)}. Try a different approach."


messages = [
    {
        "role": "system",
        "content": "You are a helpful personal assistant. Use your tools when you need real data.",
    },
    {"role": "user", "content": "Search for today's news."},
]

for iteration in range(MAX_ITERATIONS):
    print(f"Iteration {iteration + 1}/{MAX_ITERATIONS}")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
    finish_reason = response.choices[0].finish_reason
    assistant_message = response.choices[0].message
    messages.append(assistant_message)
    if finish_reason == "tool_calls":
        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = execute_tool(name, args)
            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )
    elif finish_reason == "stop":
        print(assistant_message.content)
        break
else:
    messages.append(
        {
            "role": "user",
            "content": "You've reached the maximum number of steps. Give your best answer with what you have.",
        }
    )
    final = client.chat.completions.create(model=model, messages=messages)
    print(final.choices[0].message.content)
