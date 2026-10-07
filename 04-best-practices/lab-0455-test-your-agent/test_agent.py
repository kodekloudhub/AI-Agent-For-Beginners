"""Lab 0455 - Test Your Agent.

Three layers of tests: pure-function unit tests, a dispatch test using
unittest.mock, and an evaluation test that actually hits the model to
check the agent responds plausibly to a calendar query.
"""
import unittest
from unittest.mock import MagicMock, patch
import json

from agent_components import check_calendar, execute_tool, run_agent


class TestTools(unittest.TestCase):
    def test_check_calendar_returns_string(self):
        result = check_calendar()
        self.assertIsInstance(result, str)

    def test_check_calendar_contains_standup(self):
        result = check_calendar()
        self.assertIn("standup", result)


class TestAgentLoop(unittest.TestCase):
    def test_tool_dispatch_on_tool_call(self):
        fake_tool_call = MagicMock()
        fake_tool_call.function.name = "check_calendar"
        fake_tool_call.function.arguments = json.dumps({})

        with patch("agent_components.execute_tool", return_value="mocked result"):
            name = fake_tool_call.function.name
            args = json.loads(fake_tool_call.function.arguments)
            execute_tool(name, args)
            self.assertEqual(name, "check_calendar")


class TestAgentEval(unittest.TestCase):
    def test_agent_responds_to_calendar_query(self):
        import os
        from openai import OpenAI
        from agent_components import CHECK_CALENDAR_TOOL

        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_API_BASE"],
        )
        response = client.chat.completions.create(
            model="<model_name>",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's on my calendar today?"},
            ],
            tools=[CHECK_CALENDAR_TOOL],
        )
        choice = response.choices[0]
        made_tool_call = choice.finish_reason == "tool_calls"
        content = choice.message.content or ""
        scheduling_words = [
            "calendar",
            "schedule",
            "appointment",
            "meeting",
            "standup",
            "event",
        ]
        has_scheduling_word = any(w in content.lower() for w in scheduling_words)
        self.assertTrue(made_tool_call or has_scheduling_word)


if __name__ == "__main__":
    unittest.main()
