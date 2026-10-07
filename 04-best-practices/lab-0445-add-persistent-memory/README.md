# Lab 0445 - Add Persistent Memory

Writes user preferences to `agent_memory.json` on disk and loads them into
the system prompt at the start of every run. Shows that "the agent
remembers you" is file I/O plus a prompt injection, not model state.

Preferences are saved to `/root/code/agent_memory.json` by default (the
lab path). Edit `MEMORY_FILE` if you run it outside the lab environment.

## Run

```bash
pip install openai
python persistent_agent.py
```
