"""Lab 0465 - Add Monitoring.

Tracks iteration count, prompt + completion tokens, per-tool duration and
a wall-clock timer. Prints a run summary at the end so you can see what
the run cost without hunting through logs.
"""
from openai import OpenAI
import os
import json
import time

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_API_BASE"],
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
    }
]


def check_calendar(date):
    return "10am: Team standup, 2pm: Project review, 4pm: One-on-one with manager"


def execute_tool(name, args, run_log):
    start_time = time.time()
    try:
        if name == "check_calendar":
            result = check_calendar(**args)
        else:
            result = "Unknown tool"
    except Exception as e:
        result = f"Error: {str(e)}. Try a different approach."
    duration = time.time() - start_time
    run_log.append(
        {
            "tool": name,
            "args": args,
            "result": result[:100],
            "duration_ms": round(duration * 1000),
        }
    )
    return result


if __name__ == "__main__":
    run_log = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    messages = [
        {
            "role": "system",
            "content": "You are a helpful personal assistant. Use your tools when you need real data.",
        },
        {
            "role": "user",
            "content": "What's on my calendar today and summarise it in one sentence.",
        },
    ]

    iteration_count = 0
    wall_start = time.time()
    for iteration in range(MAX_ITERATIONS):
        iteration_count += 1
        if iteration_count >= MAX_ITERATIONS - 2:
            print(f"WARNING: approaching iteration limit ({iteration_count}/{MAX_ITERATIONS})")
        response = client.chat.completions.create(model=model, messages=messages, tools=tools)
        if response.usage:
            total_prompt_tokens += response.usage.prompt_tokens
            total_completion_tokens += response.usage.completion_tokens
        finish_reason = response.choices[0].finish_reason
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        if finish_reason == "tool_calls":
            for tool_call in assistant_message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = execute_tool(name, args, run_log)
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

    elapsed = round(time.time() - wall_start, 2)
    print("\n=== Execution Summary ===")
    print(f"Iterations used: {iteration_count}/{MAX_ITERATIONS}")
    print(
        f"Total tokens: {total_prompt_tokens + total_completion_tokens} "
        f"(prompt={total_prompt_tokens}, completion={total_completion_tokens})"
    )
    print(f"Tools called: {len(run_log)}")
    for entry in run_log:
        print(f"  - {entry['tool']}({entry['args']}): {entry['duration_ms']}ms")
    print(f"Wall-clock time: {elapsed}s")
