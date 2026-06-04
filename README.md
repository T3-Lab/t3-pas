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
= Commands:
intro
calc <expression>
summarize <text>
scrape <url>
analyze <url>
history
last result
math problem
exit
= You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history'

You > intro

Agent > Hello! I'm PAS, Primitive Agentic System.

You > math problem

Agent > What is 100 + 43?

You > 143

Agent > Correct! Well done.

You > last result

Agent > {'type': 'single_task', 'success': True, 'result': 'Correct! Well done.'}

You > history

Agent > intro
{'type': 'single_task', 'success': True, 'result': "Hello! I'm PAS, Primitive Agentic System."}
math problem
{'type': 'state_single_task', 'success': True, 'result': 'What is 100 + 43?', 'answer': 143}
last result
{'type': 'single_task', 'success': True, 'result': {'type': 'single_task', 'success': True, 'result': 'Correct! Well done.'}}
history
{'type': 'nested', 'success': True, 'result': [{'role': 'user', 'content': 'intro'}, {'role': 'agent', 'content': '{\'type\': \'single_task\', \'success\': 
True, \'result\': "Hello! I\'m PAS, Primitive Agentic System."}'}, {'role': 'user', 'content': 'math problem'}, {'role': 'agent', 'content': "{'type': 
'state_single_task', 'success': True, 'result': 'What is 100 + 43?', 'answer': 143}"}, {'role': 'user', 'content': 'last result'}, {'role': 'agent', 'content':
"{'type': 'single_task', 'success': True, 'result': {'type': 'single_task', 'success': True, 'result': 'Correct! Well done.'}}"}, {'role': 'user', 'content': 
'history'}]}

You > exit
Long session: 34.96 seconds
```

## Purpose

Basic introduction to agentic systems with simple programs that can carry out planning and tool selection.