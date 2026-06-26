# Architecture

## Project Philosophy
Defining the minimum requirements for a system to be categorized as an agent, and the effort to bring that concept to life within a stable system.

## Roles

### User
Sends commands and receives output. Interacts exclusively 
through the CLI prompt.

### Agent
Processes goals, executes workflows, and manages memory. 
The core of PAS.

### System
Manages CLI-level utilities — history, trace, memory inspection, 
belief state, and session reset. Operates independently from 
agent logic, providing direct observability into agent internals.

## Agent Workflow

User input first goes through a parsing stage, where PAS 
translates the request into a structured `Goal` using 
keyword-based matching with looks for known command prefixes to determine intent.

Once a goal is assigned from parsing user's request, the `SimplePlanner` maps it to a predefined sequence of tool steps (`AgentPlan`). The agent executes each step recursively, passing outputs as inputs to the next step. If a step fails, PAS attempts to replan using a fallback map.

after each tool execution, PAS updates its internal state. Results are stored as episodes in episodic memory, key facts persist in semantic memory, and beliefs about the user and environment are revised when evidence warrants it.

## Internal Module Structure

### __main__.py
CLI entrypoint for module-based execution.

### __init__.py
Contain package initiation.

### main.py
Run and start PAS project.

### agen.py
The PAS system, which also serves as the orchestration point for several separate modules.

### state.py
Contains context objects, state types, and memory for PAS.

### planning.py
Contains the planner object and utilities for mapping a goal to a sequence of actions accompanied by tools.

### tools.py
Contains a collection of tools enabling PAS to perform actions.

## Final Design Decisions

### Why 'primitive'?
PAS was conceived as a personal exploration project stemming from a simple question regarding the concept of an agent. The 'primitive' architecture adopted by PAS aims to address two questions: *What are the minimum requirements for a system to be considered an agent?* and *How can these requirements manifest as a stable system?* These questions can be answered by constructing a simple system—utilizing a set of basic concepts—that is sufficient for PAS to qualify as an 'agentic system'.

### Why doesn't it use ML as a router?
While PAS does employ ML for specific components—such as tools—its core logic does not rely on ML. This design choice stems from the system's primary objective: meeting the minimum criteria required for a system to be classified as an agent. Under the fundamental concept of an agent, a system qualifies if it meets a specific set of criteria—criteria that do not directly include the use of ML.

### Why CLI instead of GUI
One reason is the inadequate skills of the stack maintainer, but a PAS demo in GUI format on Streamlit will be available soon at an unspecified time.