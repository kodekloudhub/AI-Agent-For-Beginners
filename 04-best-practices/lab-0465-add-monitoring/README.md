# Lab 0465 - Add Monitoring

Tracks what every run actually costs - iteration count, prompt and
completion tokens, per-tool duration, and wall-clock time - then prints a
run summary at the end so a runaway agent becomes visible instead of
quiet.

## Run

```bash
pip install openai
python monitored_agent.py
```
