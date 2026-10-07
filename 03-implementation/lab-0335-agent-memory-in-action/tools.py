"""Pre-created helper for lab 0335.

Kept separate so the lab can focus on memory management, not tool wiring.
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Returns today's calendar events.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }
]


def check_calendar():
    return "10am: Team standup, 2pm: Dentist appointment"


def execute_tool(name, args):
    if name == "check_calendar":
        return check_calendar()
    return f"Unknown tool: {name}"
