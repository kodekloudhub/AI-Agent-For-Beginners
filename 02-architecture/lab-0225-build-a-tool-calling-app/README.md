# Lab 0225 - Build a Tool-Calling App

A single request/response cycle with tool calling: send a user message plus
a `tools` list, inspect `finish_reason`, run the requested tool, and send
the result back as a `tool`-role message so the model can write the final
answer.

## Run

```bash
pip install openai
python tool_app.py
```
