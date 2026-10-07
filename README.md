# AI Agents for Beginners with OpenClaw - Course Code

All code written across the course, organised by module and lab. Shared in
response to learner feedback asking for a downloadable bundle of the course
code.

## Layout

```
course-code/
├── 01-fundamentals/
│   └── lab-0190-your-first-api-call/      hello_llm.py
├── 02-architecture/
│   └── lab-0225-build-a-tool-calling-app/ tool_app.py
├── 03-implementation/
│   ├── lab-0315-your-first-agent-loop/    agent_loop.py
│   ├── lab-0325-wire-up-components/       agent_components.py
│   ├── lab-0335-agent-memory-in-action/   agent_memory.py, tools.py
│   ├── lab-0345-build-a-react-agent/      react_agent.py
│   ├── lab-0355-apply-agentic-patterns/   patterns_agent.py
│   ├── lab-0385-build-a-safe-agent/       safe_agent.py
│   └── lab-0395-build-personal-assistant-agent/ agent.py, tools.py
├── 04-best-practices/
│   ├── lab-0425-design-better-tools/      better_tools.py
│   ├── lab-0445-add-persistent-memory/    persistent_agent.py
│   ├── lab-0455-test-your-agent/          test_agent.py, agent_components.py
│   ├── lab-0465-add-monitoring/           monitored_agent.py
│   ├── lab-0485-harden-your-agent/        secure_agent.py
│   └── lab-0500-explore-openclaw/         openclaw-map.md (reference lab)
└── 05-assessments/
    ├── assessment-01-knowledge-check/     (MCQ only - no code)
    ├── assessment-02-practical/           assessment_agent.py
    └── assessment-03-exam/                assessment_agent_starter.py,
                                           assessment_agent.py,
                                           solution_sample.md
```

Each lab folder contains the final version of the code the lab builds up to,
plus a short `README.md`.

## Running the code

### Install Python 3.11 or later and the OpenAI SDK

```bash
python3 -m venv venv
source venv/bin/activate
pip install openai
```

### Set your API credentials

The scripts read these from the environment:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

Inside the KodeKloud lab environment these are pre-set to the KodeKey proxy.
If you are running outside the lab, point them at any OpenAI-compatible
endpoint you have access to. A couple of scripts pin specific model names
(`<model_name>`, `<model_name>`) that only exist on the course
gateway - swap them for a model your endpoint actually serves.

### Run any lab

```bash
cd 03-implementation/lab-0315-your-first-agent-loop
python agent_loop.py
```

## Notes

- Lab 0500 is a code-reading lab against an OpenClaw codebase provisioned
  only inside the KodeKloud environment, so this bundle ships only the
  reference map.
- Assessment 1 is multiple-choice only, so there is nothing to download for
  it beyond this README stub.
- Assessment 3 ships both the unsolved `assessment_agent_starter.py` and the
  completed `assessment_agent.py`, plus the grader's `solution_sample.md`
  with per-task rationale.
# AI-Agent-For-Beginners
