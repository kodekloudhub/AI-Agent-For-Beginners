# Lab 0345 - Build a ReAct Agent

Runs the same loop twice - once with a plain prompt, once with a ReAct
prompt that asks the model to write `Thought:` and `Observation:` lines
around each tool call. Shows that ReAct is a system-prompt change, not a
code change.

## Run

```bash
pip install openai
python react_agent.py
```
