# Lab 0385 - Build a Safe Agent

Three production safeguards on the baseline tool-calling agent:
`try/except` around every tool call, a `flaky_tool` that always fails so
you can see the recovery in action, and `MAX_ITERATIONS` with a graceful
`else:` block that still returns an answer.

## Run

```bash
pip install openai
python safe_agent.py
```
