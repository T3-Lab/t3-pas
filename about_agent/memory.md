# Memories

In the context of agentic systems, memory is information that agents retain so they can make better decisions in the future.

## Short-Term vs Long-Term

Memory is generally divided into two, short-term memory and long-term memory. Short-term memory such as working memory has temporary characteristics and is lost when the agent session is finished. In long-term memory, such as semantic and episodic memory, information is stored and used between agent sessions, it is persistent and stored in a database or disk.

## Memory Type

### Working memory

Memory that contains information that is actively used, focuses on answering *What is the current context?*. Example:
```python
{
    "goal": "order pizza",
    "current_task": "checkout",
    "retry_count": 1
}
```

Working memory has several general characteristics such as changing quickly, usually being small or not storing as much information as other types of memory, and living during agent execution.

### Episodic memory

Storing information about events that the agent has experienced during execution, the focus is to answer *What happened?*. For example, with agents:
```text
SEARCH
 ↓
FAILED
 ↓
REPLAN
 ↓
SUCCESS
```

Based on the example above, episodic memory can store:
```python
{
    "event": "search_failed",
    "reason": "timeout"
}
```

### Semantic memory

Contains the agent's knowledge of the world, the focus is to answer *What do I as an agent know?*. Example:
```python
{
    "restaurant_rating": 4.8,
    "user_favorite_food": "ramen",
    "preferred_budget": 20
}
```

### Memory Separation Visualization

```text
                   Memory
                     |
      +--------------+--------------+
      |              |              |
      v              v              v

    Working      Episodic        Semantics

    Current      Experience      Knowledge
    Context      Historical      Facts
```

## Various Memory Implementation Techniques

Because the model has a Context Window limitation, long-term memory (Episodic & Semantic) cannot be fully included while the agent is running. Techniques used:

1. Buffer Memory: Stores raw all logs (effective for short tasks).

2. Summarized Memory: Filters old logs into periodic text summaries to save tokens.

3. Vector-Backed Memory: Converts Episodic/Semantic memory into vector queries for relevance-based search (RAG / Retrieval-Augmented Generation).