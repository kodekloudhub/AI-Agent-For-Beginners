"""Lab 0325 - Wire Up the Five Components.

Five components wired together: system prompt, tool definition, memory
(the messages list), orchestration loop, and model call.
"""
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

model = "<model_name>"

messages = [
    {
        "role": "system",
        "content": "You are a helpful personal assistant. Use your tools when you need real data.",
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the user's calendar for events on a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date to check, e.g. 2026-03-14",
                    }
                },
                "required": ["date"],
            },
        },
    }
]


def check_calendar(date):
    return "10am: Team standup, 2pm: Dentist appointment"


messages.append({"role": "user", "content": "What's on my calendar today?"})

while True:
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
            if name == "check_calendar":
                result = check_calendar(**args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )
    elif finish_reason == "stop":
        print(assistant_message.content)
        break
