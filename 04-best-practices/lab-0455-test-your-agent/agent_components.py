"""Pre-created module imported by test_agent.py.

In the lab this is written by the startup script; it's included here so the
test file can be imported and run without additional setup.
"""
import os
import json
from openai import OpenAI


def check_calendar(date=None):
    """Return today's calendar events."""
    return "10am: Team standup, 2pm: Dentist appointment"


def execute_tool(name, args):
    """Execute a tool by name with given arguments."""
    try:
        if name == "check_calendar":
            return check_calendar(**args)
        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Error: {str(e)}"


CHECK_CALENDAR_TOOL = {
    "type": "function",
    "function": {
        "name": "check_calendar",
        "description": "Check the user's calendar for events on a given date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
            },
            "required": [],
        },
    },
}


def run_agent(prompt, client=None):
    """Run the agent with a given prompt."""
    if not client:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE"),
        )

    response = client.chat.completions.create(
        model="<model_name>",
        messages=[{"role": "user", "content": prompt}],
        tools=[CHECK_CALENDAR_TOOL],
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        tc = msg.tool_calls[0]
        args = json.loads(tc.function.arguments)
        return execute_tool(tc.function.name, args)

    return msg.content
