# Definitions

Agent is a system that observes an environment (observation), maintains relevant state representations, and selects actions based on policies to achieve certain goals. As an illustration, an agent can be defined as:

```math
agent = Policy(Environment, State) → action
```

or

```math
π(s) → a
```

Where:

π = policy
s = state
a = action

## Components

### Goals

Agent goals that can be achieved through a series of decisions.

### Observations

Observation of the environment or state regarding the decisions that will be made by the agent or simply means the information that the agent can see at this time.

### State

Representations of the world that are relevant for decision making.

#### Environment state

Representation of the environmental conditions in which the agent operates (e.g. room temperature, database status, robot position, etc.)

#### Internal state

Representation of the agent's internal state (e.g. Current goal, current plan, selected tools, etc.)

### Policies

Rules that serve as a benchmark for decision making by agents.

### Actions

Actions or actions carried out by agents.

### Environment

The environment the agent operates in.