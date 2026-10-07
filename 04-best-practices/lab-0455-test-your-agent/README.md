# Lab 0455 - Test Your Agent

Three layers of tests: pure-function unit tests for tools, a dispatch test
with `unittest.mock`, and an evaluation test that actually hits the model
to check the agent responds plausibly.

## Files

- `test_agent.py` - the test suite
- `agent_components.py` - pre-created in the lab environment; imported by
  the test file

## Run

```bash
pip install openai
python -m unittest test_agent.py
```
