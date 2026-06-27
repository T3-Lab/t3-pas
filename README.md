[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/t3-lab/t3-pas/blob/main/LICENSE)
![Docs](https://img.shields.io/badge/docs-available-blue)

# PAS — Primitive Agentic System

PAS is a personal learning project — built to answer a specific question, open for anyone curious about the same question:

> *"What are the minimal components for a system to be called an agent? And how can that concept live as systematic lines of code?"*

This is not a framework. It's a documented exploration — built as a personal learning record, published as a portfolio, and open to anyone who wants to explore the same question or build on top of it.

---

## Principle

- No ML in agent logic — the agent's decision-making is entirely rule-based
- Minimal but complete — every component exists for a reason
- Readable over clever — code is written to be understood, not impressed

---

## How It Works

PAS processes user input in four stages:

**1. Parsing** — translates the user's request into a structured `Goal` that the agent can process. This is keyword-based: PAS looks for known command prefixes to determine intent.

**2. Workflow** — once a goal is assigned, the `SimplePlanner` maps it to a predefined sequence of tool steps (`AgentPlan`). The agent executes each step recursively, passing outputs as inputs to the next step. If a step fails, PAS attempts to replan using a fallback map.

**3. State & Memory Update** — after each tool execution, PAS updates its internal state. Results are stored as episodes in episodic memory, key facts persist in semantic memory, and beliefs about the user and environment are revised when evidence warrants it. This is what separates PAS from a stateless input-output pipeline.

**4. Render** — the final result, stored internally as a typed dictionary, is translated into human-readable output and printed to the terminal.

Throughout this process, PAS maintains a layered memory (working, episodic, semantic) and updates its internal beliefs based on what it observes — for example, adapting math problem difficulty based on the user's track record.

---

## Project Structure

```text
pas/
├── agent.py      # Main agent loop, parsing, and workflow execution
├── planning.py   # Goal and plan definitions, SimplePlanner
├── state.py      # Agent state, memory layers, and context
├── tools.py      # Tool registry and implementations
└── main.py       # CLI entry point
```

---

## Quick Start

```bash
python -m src.pas
```

---

## 💬 Example Conversation

```bash
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 131/131 [00:00<00:00, 3003.91it/s]
=== Welcome! ===
* Agent Commands:
my name is <str>
calc <expression>
summarize <text>
scrape <url>
analyze <url>
math problem
(You can also chain tasks using 'then', e.g. 'calc 2 + 2 then math problem')

* Utility Commands:
intro
see history
see trace
access memory <kind>
belief
reset
exit

You > intro

System > Hello! I'm PAS, Primitive Agentic System.

You > my name is Nexo Usagi

Agent > Hello nexo usagi

You > math problem

Agent > What is 22 + 17?

You > 39

Agent > Correct! Well done.

You > math problem

Agent > What is 20 + 19?

You > 39

Agent > Correct! Well done.

You > math problem

Agent > What is 16 + 12?

You > 28

Agent > Correct! Well done.

You > math problem

Agent > What is 7 + 8?

You > 15

Agent > Correct! Well done.

You > math problem

Agent > What is 93 + 73?

You > 166

Agent > Correct! Well done.

You > access memory semantic

System > {'user_name': 'nexo usagi', 'last_connection_problem': None, 'math_correct_answer': 5, 'total_math_question': 5}

You > access memory episodic

System > Episode(goal='math_problem', action='math_problem', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'What is 22 + 17?',
'answer': 39}, timestamp=1782381741.9932764)
Episode(goal='math_problem', action='math_problem_answer', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'Correct! Well 
done.', 'correct': True}, timestamp=1782381746.95265)
Episode(goal='math_problem', action='math_problem', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'What is 20 + 19?', 
'answer': 39}, timestamp=1782381748.2639463)
Episode(goal='math_problem', action='math_problem_answer', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'Correct! Well 
done.', 'correct': True}, timestamp=1782381750.5592747)
Episode(goal='math_problem', action='math_problem', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'What is 16 + 12?', 
'answer': 28}, timestamp=1782381751.4248188)
Episode(goal='math_problem', action='math_problem_answer', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'Correct! Well 
done.', 'correct': True}, timestamp=1782381755.656385)
Episode(goal='math_problem', action='math_problem', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'What is 7 + 8?', 'answer': 
15}, timestamp=1782381756.7973795)
Episode(goal='math_problem', action='math_problem_answer', target=False, result={'output_type': 'single_dict', 'success': True, 'result': 'Correct! Well 
done.', 'correct': True}, timestamp=1782381759.6095989)
Episode(goal='math_problem', action='math_problem', target=True, result={'output_type': 'single_dict', 'success': True, 'result': 'What is 93 + 73?', 'answer':
166}, timestamp=1782381760.8326375)
Episode(goal='math_problem', action='math_problem_answer', target=True, result={'output_type': 'single_dict', 'success': True, 'result': 'Correct! Well done.',
'correct': True}, timestamp=1782381766.428391)

You > belief

System > {'internet_access': True, 'user_math_skill_advance': True}

You > see trace

System > New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 steps: ['math_problem']                        
 output type: single_dict
Agent State: PLANNING -> EXECUTING
Current step: math_problem.
Plan completed.
Agent State: EXECUTING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem
New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 steps: ['math_problem']                        
 output type: single_dict
Agent State: PLANNING -> EXECUTING
Current step: math_problem.
Plan completed.
Agent State: EXECUTING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem
New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 steps: ['math_problem']                        
 output type: single_dict
Agent State: PLANNING -> EXECUTING
Current step: math_problem.
Plan completed.
Agent State: EXECUTING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem
New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 steps: ['math_problem']                        
 output type: single_dict
Agent State: PLANNING -> EXECUTING
Current step: math_problem.
Plan completed.
Agent State: EXECUTING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem
New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 steps: ['math_problem']                        
 output type: single_dict
Agent State: PLANNING -> EXECUTING
Current step: math_problem.
Plan completed.
Agent State: EXECUTING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem

You > exit
System > Long session: 67.48 seconds
```

---

## What PAS Is Not

PAS is intentionally primitive. It does not use LLM-based reasoning, dynamic planning, or natural language understanding. Those are problems for the next project.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
PAS started as a personal project — contributions are welcome from anyone curious about the same questions.