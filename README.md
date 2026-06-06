[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/sancheck/blob/main/LICENSE)

# PAS

`PAS` or `Primitive Agentic System` is a non-ML agentic system that is capable of doing several things from the commands available through basic agentic processes.

## Example Conversation 💬

To start conversation with PAS, use this command:
```bash
python -m src.pas
```

```bash
=== Welcome! ===
* Agent Commands:
calc <expression>
summarize <text>
scrape <url>
analyze <url>
math problem

* Utility Commands:
intro
history
last result
see trace
reset
exit
* You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history'

You > intro

Agent > Hello! I'm PAS, Primitive Agentic System.

You > math problem

Agent > What is 81 + 14?

You > 95

Agent > Correct! Well done.

You > see trace

Agent > New goal assigned: math problem
Agent State: IDLE -> PLANNING
Agent State: PLANNING -> WAITING_ANSWER
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math problem

You > history

Agent > math problem
{'type': 'state_single_task', 'success': True, 'result': 'What is 81 + 14?', 'answer': 95}

You > exit
Long session: 32.47 seconds
```

## Purpose

Basic introduction to agentic systems with simple programs that can carry out planning and tool selection.