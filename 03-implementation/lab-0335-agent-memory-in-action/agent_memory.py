"""Lab 0335 - Agent Memory in Action.

Keeps the system prompt pinned and trims the rest of the history to a
sliding window of the N most recent messages.
"""
import os
import json
from openai import OpenAI
from tools import tools, execute_tool

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

SYSTEM_PROMPT = "You are a helpful personal assistant. Use your tools when you need real data."


def run_agent(messages):
    while True:
        response = client.chat.completions.create(
            model="<model_name>",
            messages=messages,
            tools=tools,
        )
        choice = response.choices[0]
        messages.append(choice.message)
        if choice.finish_reason == "tool_calls":
            for tc in choice.message.tool_calls:
                args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                result = execute_tool(tc.function.name, args)
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
        else:
            return choice.message.content


def trim_history(messages, max_messages=6):
    if len(messages) > max_messages:
        return [messages[0]] + messages[-(max_messages - 1):]
    return messages


messages = [{"role": "system", "content": SYSTEM_PROMPT}]

questions = [
    "What's on my calendar today?",
    "Tell me about the standup.",
    "What time is my dentist?",
    "Am I free at 3pm?",
    "Summarise my day.",
]

for q in questions:
    messages.append({"role": "user", "content": q})
    answer = run_agent(messages)
    messages = trim_history(messages, max_messages=6)
    print(f"Q: {q}")
    print(f"A: {answer}")
    print(f"Messages in history: {len(messages)}")
    print()
