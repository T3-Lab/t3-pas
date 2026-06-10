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
(You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history')

* Utility Commands:
intro
history
see artifact
see trace
reset
exit

You > intro

Agent > Hello! I'm PAS, Primitive Agentic System.

You > math problem

Agent > What is 9 + 92?

You > 101

Agent > Correct! Well done.

You > see trace

Agent > New goal assigned: math_problem
Agent State: IDLE -> PLANNING
Plan:                        
 goal: math_problem                        
 type: single_dict                        
 steps: ['math_problem']
Agent State: PLANNING -> WAITING_ANSWER
Current step: math_problem.
Plan completed.
Agent State: WAITING_ANSWER -> IDLE
Goal reached: math_problem

You > exit
Long session: 26.90 seconds
```

## Purpose

Basic introduction to agentic systems with simple programs that can carry out planning and tool selection.