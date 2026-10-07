"""Lab 0425 - Design Better Tools.

Applies ACI (Agent-Computer Interface) design principles: strong descriptions
that signal when to use each tool, parameter descriptions written for an LLM
rather than a human reader, and enum-constrained categories.
"""
from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_API_BASE"],
)

model = "<model_name>"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurants",
            "description": (
                "Search for restaurants by cuisine, location, and price range. "
                "Returns names, ratings, and availability. Use this when the "
                "user wants to find or book a place to eat."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cuisine": {
                        "type": "string",
                        "description": "The type of cuisine, e.g. italian, thai, mexican",
                    },
                    "location": {
                        "type": "string",
                        "description": (
                            "The area or neighbourhood to search in. If the user "
                            "gives a vague phrase like 'near me' instead of a "
                            "specific place, pass that phrase through as-is."
                        ),
                    },
                },
                "required": ["cuisine", "location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_preferences",
            "description": (
                "Retrieve stored user preferences by category (e.g. 'travel', "
                "'food', 'schedule'). Returns preference key-value pairs. Use "
                "this when personalising a recommendation or action."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The preference category to retrieve",
                        "enum": ["food", "travel", "schedule", "contacts"],
                    }
                },
                "required": ["category"],
            },
        },
    },
]


def search_restaurants(cuisine, location):
    cuisine = cuisine.lower().strip()
    return f"[restaurants: {cuisine} near {location} - Bella Roma 4.7 stars, La Piazza 4.5 stars]"


def get_user_preferences(category):
    return f"[preferences for {category}: vegetarian, no spicy food, prefers outdoor seating]"


def execute_tool(name, args):
    if name == "search_restaurants":
        return search_restaurants(**args)
    if name == "get_user_preferences":
        return get_user_preferences(**args)
    return f"[unknown tool: {name}]"


messages = [
    {"role": "system", "content": "You are a helpful assistant. Use your tools when needed."},
    {"role": "user", "content": "Find Italian restaurants near me"},
]

while True:
    response = client.chat.completions.create(model=model, messages=messages, tools=tools)
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
