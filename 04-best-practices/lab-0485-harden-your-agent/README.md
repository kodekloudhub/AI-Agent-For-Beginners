# Lab 0485 - Harden Your Agent

Three security layers around the same loop you've been building:

- `detect_injection()` at the input boundary refuses obvious prompt-
  injection phrases before the model ever runs.
- Per-tool rate limits at the tool boundary stop a runaway from calling
  one tool more than `TOOL_RATE_LIMIT` times.
- `filter_output()` at the output boundary redacts emails and phone
  numbers before display.

## Run

```bash
pip install openai
python secure_agent.py
```
