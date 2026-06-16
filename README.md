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
reset
exit

You > intro

System > Hello! I'm PAS, Primitive Agentic System.

You > my name is Nexo Usagi

Agent > Hello Nexo Usagi

You > math problem

Agent > What is 1 + 25?

You > 26

Agent > Correct! Well done.

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

You > access memory episodic

System > Episode(goal='math_problem', goal_status=<GoalStatus.IN_PROGRESS: 'in_progress'>, actions={'math_problem': {'type': 'single_dict', 'success': True, 
'result': 'What is 1 + 25?', 'answer': 26}}, timestamp=1781620195.3422866)
Episode(goal='math_problem', goal_status=<GoalStatus.COMPLETED: 'completed'>, actions={'math_problem': {'type': 'single_dict', 'success': True, 'result': 
'Correct! Well done.'}}, timestamp=1781620198.6771617)

You > exit
System > Long session: 47.09 seconds
```

## Purpose

Basic introduction to agentic systems with simple programs that can carry out planning and tool selection.