"""Lab 0395 - personal assistant tools.

Three tools plus a broken one used in the error-recovery step.
TOOLS_SCHEMA is what the model sees; the functions below are what runs.
"""


def check_calendar(day):
    events = {
        "monday": "10am Team Standup, 2pm Client Meeting",
        "tuesday": "No events",
        "wednesday": "1pm Lunch with Alex",
        "thursday": "9am Dentist, 3pm Project Review",
        "friday": "No events",
    }
    return f"Events for {day}: {events.get(day.lower(), 'None')}"


def search_web(query):
    results = {
        "weather": "Sunny, 72F",
        "news": "Tech stocks rally as AI adoption grows",
        "stock": "AAPL: 185.20, MSFT: 420.50",
    }
    for key, value in results.items():
        if key in query.lower():
            return f"Top result: {value}"
    return "No relevant results found."


def get_user_preferences(category):
    prefs = {
        "travel": "Aisle seat, vegetarian meal",
        "communication": "Email preferred, no calls after 6pm",
        "news": "Tech and science focus",
    }
    return f"Preference for {category}: {prefs.get(category.lower(), 'Not specified')}"


def broken_tool():
    raise Exception("Service temporarily unavailable")


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the user's calendar for a specific day",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {"type": "string", "description": "Day of the week"}
                },
                "required": ["day"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_preferences",
            "description": "Get user preferences for a specific category",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Preference category (travel, communication, news)",
                    }
                },
                "required": ["category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "broken_tool",
            "description": "A deliberately broken tool used to test error recovery.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]
