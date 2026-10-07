# Lab 0355 - Apply Agentic Patterns

Layers three production patterns on top of the ReAct agent:

- **Structured output** - the system prompt tells the model to end with a
  JSON summary block.
- **Input guardrails** - `check_input()` refuses blocked topics before any
  API call is made.
- **Human-in-the-loop** - `send_email` requires a `y/n` confirmation before
  executing.

Reads input from stdin, so run it interactively.

## Run

```bash
pip install openai
python patterns_agent.py
```
