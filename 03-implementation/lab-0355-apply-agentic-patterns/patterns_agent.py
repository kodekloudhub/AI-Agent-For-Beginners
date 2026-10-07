"""Lab 0355 - Apply Agentic Patterns.

Starts from the ReAct agent and layers on three production patterns:

  1. Structured output   - the system prompt tells the model to end with a JSON summary block.
  2. Input guardrails    - check_input() refuses blocked topics before any API call runs.
  3. Human-in-the-loop   - send_email requires a y/n confirmation before executing.
"""
import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

system_prompt = """You are a scheduling assistant. Use the ReAct pattern.
Thought: reason about what to do next.
Action: call a tool if needed.
Observation: use the tool result.
Repeat until you can give a final answer.
Always end your final response with a JSON summary block:
{"summary": "...", "actions_taken": ["..."]}"""


def check_input(message):
    blocked = ["medical", "legal", "financial advice"]
    for term in blocked:
        if term in message.lower():
            return "I can only help with scheduling and contacts."
    return None


def check_calendar(date):
    return "10am: Team standup, 2pm: Dentist appointment"


def send_email(to, subject, body):
    return f"Email sent to {to} with subject '{subject}'."


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
            "name": "send_email",
            "description": "Send an email to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email or name"},
                    "subject": {"type": "string", "description": "Email subject line"},
                    "body": {"type": "string", "description": "Email body text"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
]


def run_agent(user_message):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    while True:
        response = client.chat.completions.create(
            model="<model_name>",
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        messages.append(msg)
        if msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                if name == "send_email":
                    print(f"Proposed email: {args}")
                    confirm = input("Send this email? (y/n): ")
                    if confirm.lower() != "y":
                        result = "Email cancelled by user."
                    else:
                        result = send_email(**args)
                elif name == "check_calendar":
                    result = check_calendar(**args)
                else:
                    result = "Unknown tool."
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
        else:
            print(msg.content)
            break


user_message = "Email Sarah my calendar summary for today."

guard_result = check_input(user_message)
if guard_result:
    print(guard_result)
else:
    run_agent(user_message)
