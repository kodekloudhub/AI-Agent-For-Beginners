# OpenClaw Codebase Navigation Guide

A reference for navigating the simplified OpenClaw codebase at `/root/openclaw/`.

---

## Directory Overview

```
/root/openclaw/
  src/
    agent.py            Main agent loop (perceive-reason-act cycle)
    orchestrator.py     Request routing and response handling
  tools/
    calendar_tool.py    Calendar tool definition and handler
    email_tool.py       Email tool definition and handler
    search_tool.py      Web search tool definition and handler
  memory/
    session_memory.py   Conversation history management
    persistent_memory.py  User preferences storage
  tests/
    test_tools.py       Unit tests for tool handlers
    test_agent.py       Integration tests with mock API
```

To list every file in the repo:

```bash
find /root/openclaw -type f | sort
```

---

## Key Files

### src/agent.py

The main agent loop. This is the most important file in the codebase.

Contains:
- `MAX_ITERATIONS = 15` — the loop guard you learned in Lab 0385
- `run_agent()` — the `for` loop that checks `finish_reason` on every LLM response
- `execute_tool()` — the router that dispatches tool calls to handlers
- `filter_output()` — the output security layer from Lab 0485
- `load_system_prompt()` — the system prompt with ReAct-style instructions
- `print_execution_summary()` — the run log and token counter from Lab 0465

Lab equivalent: Lab 0385 (agent loop), Lab 0465 (monitoring), Lab 0485 (security)

### src/orchestrator.py

The entry point for all incoming user requests. Sits in front of the agent loop.

Contains:
- `handle_request()` — validates input, loads memory, calls `run_agent()`, updates memory
- `detect_injection()` — prompt injection detection from Lab 0485
- `load_tools()` — assembles the tools list passed to the LLM

Lab equivalent: Lab 0485 (input validation), Lab 0335 (memory loading pattern)

---

### tools/calendar_tool.py

Self-contained tool module for calendar access.

Contains:
- `DEFINITION` — the JSON schema dict passed to the LLM (same structure as Lab 0225)
- `handle()` — the function executed when the LLM calls `check_calendar`

The `DEFINITION` dict uses the same `type/function/name/description/parameters` structure you wrote in Lab 0225. The `handle()` function strips whitespace from input before using it — the poka-yoke normalisation pattern from Lab 0425.

Lab equivalent: Lab 0225 (tool schema), Lab 0325 (tool handler), Lab 0425 (ACI principles)

### tools/email_tool.py

Self-contained tool module for sending email.

Contains:
- `DEFINITION` — tool schema with carefully scoped description
- `handle()` — normalises the email address to lowercase before sending

Note the description: "Use this only when the user explicitly asks to send, compose, or draft an email. Do not use for checking emails or reading inbox." This is precise scoping — the ACI principle of writing descriptions that prevent misuse.

Lab equivalent: Lab 0355 (human-in-the-loop email tool), Lab 0425 (ACI principles)

### tools/search_tool.py

Self-contained tool module for web search.

Contains:
- `DEFINITION` — tool schema with detailed usage guidance in the description
- `handle()` — strips whitespace from the query before searching

Lab equivalent: Lab 0225 (tool schema structure), Lab 0425 (ACI description writing)

---

### memory/session_memory.py

Short-term memory. Stores the conversation history for one session. Resets when the session ends.

Contains:
- `SessionMemory` class with `session_id` and a JSON file path per session
- `get_history()` — loads the messages list (equivalent to reading your `messages` variable)
- `append()` — adds a message and trims to the last 20 entries (equivalent to `messages.append()` plus the `trim_history()` function from Lab 0335)
- `clear()` — deletes the session file

Lab equivalent: Lab 0335 (conversation history, trim_history)

### memory/persistent_memory.py

Long-term memory. Stores user preferences that survive between sessions.

Contains:
- `PersistentMemory` class with `user_id` and a per-user JSON file
- `load()` — reads user preferences (equivalent to `load_memory()` in Lab 0445)
- `save()` — writes a preference (equivalent to `save_memory()` in Lab 0445)
- `forget()` — removes a preference (equivalent to `forget_preference()` in Lab 0445)
- `inject_into_system_prompt()` — appends preferences to the system prompt before each LLM call

Lab equivalent: Lab 0445 (persistent memory, load_memory, save_memory)

---

### tests/test_tools.py

Unit tests for the three tool handlers.

Contains:
- `TestCalendarTool` — tests that the handler returns a string and contains expected content
- `TestEmailTool` — tests that email is sent and the address is normalised to lowercase
- `TestSearchTool` — tests that the query appears in the returned results

These follow the exact same pattern as the unit tests you wrote in Lab 0455: import the module, call the handler directly, assert on the returned string.

Lab equivalent: Lab 0455 (unit tests for tool handlers)

### tests/test_agent.py

Integration test that checks the agent loop's routing logic using mocks.

Contains:
- `TestAgentLoop` — builds mock response objects with `finish_reason = "tool_calls"` and `finish_reason = "stop"`, then verifies the loop would handle each correctly

Lab equivalent: Lab 0455 (mock-based integration tests)

---

## Navigation Commands

List all files:
```bash
find /root/openclaw -type f | sort
```

Find the agent loop:
```bash
grep -r "MAX_ITERATIONS\|finish_reason" /root/openclaw/src/
```

Find all tool definitions:
```bash
grep -r "DEFINITION" /root/openclaw/tools/
```

Find all error handling:
```bash
grep -r "except\|try:" /root/openclaw/src/
```

Find all memory operations:
```bash
grep -r "def load\|def save\|def append\|def get_history" /root/openclaw/memory/
```

Find security layers:
```bash
grep -r "filter_output\|detect_injection\|rate_limit" /root/openclaw/src/
```

---

## Pattern Map: Labs to Files

| Lab  | What you built            | OpenClaw equivalent                          |
|------|---------------------------|----------------------------------------------|
| 0205 | First API call            | `client.chat.completions.create()` in agent.py |
| 0225 | First tool schema         | `DEFINITION` dict in any tools/*.py file      |
| 0315 | System prompt             | `load_system_prompt()` in agent.py            |
| 0325 | Tool handler function     | `handle()` in any tools/*.py file             |
| 0335 | messages list + trimming  | `SessionMemory` class in session_memory.py    |
| 0355 | Email tool (HITL)         | `email_tool.py` with send_email handler       |
| 0385 | Agent loop (for loop)     | `run_agent()` loop in agent.py                |
| 0425 | ACI tool descriptions     | Description fields in all DEFINITION dicts   |
| 0445 | load_memory / save_memory | `PersistentMemory` class in persistent_memory.py |
| 0455 | Unit and integration tests| tests/test_tools.py and tests/test_agent.py  |
| 0465 | run_log and token counter | `run_log`, `total_tokens`, `print_execution_summary()` in agent.py |
| 0485 | Security hardening        | `filter_output()`, `detect_injection()` in agent.py and orchestrator.py |
