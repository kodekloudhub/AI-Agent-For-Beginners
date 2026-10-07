# Lab 0335 - Agent Memory in Action

Shows what happens when the messages list grows unboundedly, then adds a
sliding-window `trim_history()` that keeps the system prompt pinned and
drops the oldest turns.

## Files

- `agent_memory.py` - the main agent with history trimming
- `tools.py` - pre-created in the lab environment; imported by the agent

## Run

```bash
pip install openai
python agent_memory.py
```
