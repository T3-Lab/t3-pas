# Agent With Tools

Tools on an agent serve to increase the range of actions performed. The agent uses tools based on the needs of a set of existing actions to achieve a goal.

## Tool Selection

Tools are not always selected statically.

In some agent architectures, tools can be selected dynamically based on:

- current goal
- current task
- current state
- memory
- recent observations

This process is generally carried out by the policy or reasoning layer.

## Relationship Between Tool and Action

Action realization can be further enhanced using tools that allow the agent to interact with the environment. For example, the agent is given a goal:
```text
Goal: "Order the best food for me"
```

Then the planner generates:
```python
[
"search_restaurant",
"select_restaurant",
"checkout"
]
```

The executor must now execute the step:
```python
["search_restaurant"]
```

In modern agents, a tool call will typically occur like this:
```text
GoogleMapsTool
```
based on the example above.

Why not just hardcode it? Because tools can increase the range and flexibility of the executor's actions, this can affect the quality of the agent's output in achieving the goal.

## Relationships Between Tools and Memory

The output from a tool can generate new observations that the agent can then use to update its memory. For example, the agent is given the goal:
```text
Goal: "Find the best food in my area"
```

Then the tool produces the following output:
```python
{
"restaurants": [
{"name": "A", "rating": 4.2},
{"name": "B", "rating": 4.8}
]
}
```

Based on the example above, the changes that generally occur in memory are...

### Working memory

```python
working_memory = {
"goal": "find the best food",
"current_step": "select_restaurant",
"candidate_restaurants": [...],
"full_plan": [...]
}
```

It should be noted that the stored information has the following characteristics:
- currently in use
- relevant for the next step
- can be discarded after the goal is completed

### Episodic memory

```python
episodic_memory = [
{
"event": "restaurant_search",
"status": "success",
"num_results": 15
}
]
```

The information stored in episodic memory answers "What happened?".

### Semantic memory

Unlike other types of memory, semantic memory contains knowledge that can be reused across goals and episodes, such as:
```python
{
"user_prefers_high_rating_restaurants": True
}
```

or

```python
{
"preferred_area": ​​"Central Jakarta"
}
```

It can be noted that the stored information is more like reusable knowledge.