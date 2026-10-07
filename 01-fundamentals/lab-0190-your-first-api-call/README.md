# Lab 0190 - Your First API Call

Your first live LLM call: install the OpenAI SDK, build a `client`, send a
`messages=[...]` list, and read `response.choices[0].message.content`.

The final version in `hello_llm.py` runs ten side-by-side calls at
`temperature=0.0` and `temperature=2.0` so you can see randomness in
action.

## Run

```bash
pip install openai
python hello_llm.py
```
