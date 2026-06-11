# FSM (Finite State Machine)

FSM is a computational model that represents system behavior as a set of states and transitions connecting those states.

An agent can only be in one active state at a time, and state transitions are determined by events, conditions, or the results of previous executions.

## Components

### State

Representation of the agent's current state or work stage (e.g., Idle, Planning, Researching, Executing, etc.).

#### initial state

The first state when the system starts running (e.g., Idle).

#### terminal state

The final state that terminates the workflow (e.g., Completed, Failed, Canceled, etc.).

### Transitions

Rules for transitioning from one state to another (e.g., Planning -> Executing) after a plan has been successfully created.

### Event

Trigger that causes the transition to occur (e.g., UserInputReceived, TaskCompleted, Timeout, ErrorOccurred, etc.).

### Guard condition

Logical conditions that must be met for the transition to occur. For example:
```text
if confidence > 0.8:
    Planning -> Executing
```

Not all transitions occur immediately after an event; sometimes there are additional conditions.

### Action

Operations executed when entering a state, exiting a state, or when a transition occurs. For example:
```text
Entering Research State:
    call_search_tool()
```

## Example Agent FSM
```text
[Idle]
  |
  v
[Planning]
  |
  v
[Research]
  |
  v
[Execution]
  |
  +------> [Failed]
  |
  v
[Completed]
```

## Why FSM is Useful for Agents

FSM makes agent behavior:

- more predictable
- easier to debug
- easier to visualize
- safer than a completely free agent

Because each state has a clear purpose.

## Limitations of FSM

FSMs start to become difficult to manage when:

- the number of states is very large
- the workflow is dynamic
- the agent needs to create its own plan
- the agent must repeat steps flexibly

For example:
```text
Plan
 ↓
Code
 ↓
Test
 ↓
Reflect
 ↓
Re-plan
 ↓
Code Again
```

Therefore, many modern agent frameworks combine FSM with:

- Planning
- Memory
- ReAct
- Graph-based workflows
- More flexible state machines