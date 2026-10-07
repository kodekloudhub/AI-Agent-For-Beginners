"""Lab 0395 - Build a Personal Assistant Agent (capstone of Module 3).

Multiple tools, bounded iterations, tool-level try/except, and a
`conversation_history` argument that threads memory across turns.
"""
import os
import json
from openai import OpenAI
from tools import (
    check_calendar,
    search_web,
    get_user_preferences,
    broken_tool,
    TOOLS_SCHEMA,
)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

MAX_ITERATIONS = 10

system_prompt = """You are a helpful personal assistant.
Use your tools to find information when needed.
Before calling a tool, use 'Thought:' to explain your reasoning.
After a tool result, use 'Observation:' to note what you learned.
Provide clear, concise answers."""


def run_agent(user_message, conversation_history=None):
    messages = [{"role": "system", "content": system_prompt}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="<model_name>",
            messages=messages,
            tools=TOOLS_SCHEMA,
        )
        msg = response.choices[0].message
        messages.append(msg)

        if msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                try:
                    if name == "check_calendar":
                        result = check_calendar(**args)
                    elif name == "search_web":
                        result = search_web(**args)
                    elif name == "get_user_preferences":
                        result = get_user_preferences(**args)
                    elif name == "broken_tool":
                        result = broken_tool(**args)
                    else:
                        result = f"Unknown tool: {name}"
                except Exception as e:
                    result = f"Error: {str(e)}. Please try a different approach."
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
        else:
            print(msg.content)
            return msg.content


if __name__ == "__main__":
    history = []

    # Turn 1
    response1 = run_agent("What's on my calendar for monday?", history)
    print("Turn 1:", response1)

    history.append({"role": "user", "content": "What's on my calendar for monday?"})
    history.append({"role": "assistant", "content": response1})

    # Turn 2 - references Turn 1
    response2 = run_agent("Am I free after 3pm?", history)
    print("Turn 2:", response2)
