# Lab 0395 - Build a Personal Assistant Agent (Module 3 Capstone)

Separates tools from the loop, dispatches between multiple tools, bounds
iterations with `MAX_ITERATIONS`, wraps execution in `try/except`, and
accepts a `conversation_history` argument so turns can build on each other.

## Files

- `agent.py` - the agent loop and `__main__` demo (two chained turns)
- `tools.py` - `check_calendar`, `search_web`, `get_user_preferences`,
  `broken_tool`, plus `TOOLS_SCHEMA`

## Run

```bash
pip install openai
python agent.py
```
