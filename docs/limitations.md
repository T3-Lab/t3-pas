# Limitations

## Scope of the Project

As outlined in the 'Final Design Decisions' section of [architecture.md](./architecture.md), PAS is built upon fundamental agentic system concepts sufficient to qualify it as an 'agentic system'. However, PAS does not focus on industrial-grade agent systems or align fully with modern implementations; consequently, there is a conceptual gap between PAS and real-world industrial agent implementations.

### Why this matters

Understanding the conceptual or capability limits of a system is crucial for shaping one's perspective on a project—in this case, PAS. Knowing the extent to which a project addresses conceptual gaps or meets functional requirements enables more informed conclusions regarding its objectives, targets, appropriate use cases, and so forth.

## Known Tradeoffs

### Prompt flexibility
User interaction with PAS relies on a parser with a limited command set. This can result in rigid interactions, as users are required to type specific available *keywords* to instruct PAS to achieve a goal. As a result, PAS is not suitable for natural language interaction and assumes the user is familiar with its command set.

### Incomplete ReAct implementation
Architecturally, PAS does not fully implement the ReAct concept, as it lacks an iterative 'observation -> thinking -> action' process; goal achievement remains dependent on the completion of steps within the plan. The current architecture follows a simple workflow:
```text
Goal defined -> plan mapped based on goal -> full plan execution -> potential replanning -> goal achieved/not achieved
```

## What This Project Does Not Cover
PAS aims to answer the question, "What are the minimum requirements for a system to be considered an agent?" and it successfully addresses this. However, in a broader context—particularly within real-world industry—this does not imply that questions falling outside the PAS project's philosophy (such as "How can agents solve real-world industrial problems?" or "How can we create cost-efficient agents capable of solving complex problems?") are also answered.