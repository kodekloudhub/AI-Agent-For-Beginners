# Assessment 3 - Final Exam

Three hands-on build tasks worth 75 points plus five multiple-choice
questions worth 25 points, 75% to pass.

## Files

- `assessment_agent_starter.py` - what students start from, with three
  `TODO TASK` blocks to complete
- `assessment_agent.py` - the completed reference solution
- `solution_sample.md` - per-task rationale, grader notes, expected
  output, and the quick-check answer key

## Run

```bash
pip install openai
python assessment_agent.py "Book a meeting called Retro on Friday"
```

The exam uses `<model_name>`, which is only available on the
course gateway. To run outside the lab, change `MODEL` at the top of the
file to any model your endpoint serves that supports tool calling.
