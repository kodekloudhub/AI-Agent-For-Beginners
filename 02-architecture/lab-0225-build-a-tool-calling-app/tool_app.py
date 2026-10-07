"""Lab 0225 - Build a Tool-Calling App.

Five pieces: the client, the tool definition, the tool implementation, the
first API call that returns `tool_calls`, and the follow-up call that feeds
the tool result back to the model.
"""
import os
import json
from datetime import date as _date
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

system_message = (
    "You are a helpful personal assistant. "
    f"Today's date is {_date.today().isoformat()}."
)

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
                        "description": "The date to check in YYYY-MM-DD format.",
                    }
                },
                "required": ["date"],
            },
        },
    }
]


def check_calendar(date):
    return "10am: Team standup, 2pm: Dentist appointment"


def execute_tool(name, args):
    if name == "check_calendar":
        return check_calendar(**args)
    return f"Unknown tool: {name}"


messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": "What's on my calendar today?"},
]

response = client.chat.completions.create(
    model="<model_name>",
    messages=messages,
    tools=tools,
)

finish_reason = response.choices[0].finish_reason
print(f"Finish reason: {finish_reason}")

if finish_reason == "tool_calls":
    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = execute_tool(name, args)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    final_response = client.chat.completions.create(
        model="<model_name>",
        messages=messages,
        tools=tools,
    )
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
