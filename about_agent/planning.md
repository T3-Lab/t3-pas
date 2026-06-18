# Planning

Planning is the process of converting high-level goals into a series of executable actions. For example:
```text
Goal:
"Create a competitor report"
```
The Planner changes this to:
```text
1. Research competitors
2. Collect data
3. Summarize data
4. Write the report
```

## Components

### Goal

The target to be achieved.

### Plan

The sequence of steps designed to achieve the goal.

### Planner

The component that produces the plan.

### Executor

The component that carries out the plan.

### Feedback

Information on the results of the execution used to evaluate the plan. For example:
```text
Step:
Search Website

Result:
Website Not Reachable
```
The planner receives feedback *Search failed*, then:
```text
Replan
↓
Use alternative source
```

### Replanning

The process of generating a new plan when the previous plan fails.

## Plan Structures

### Sequential plan
```text
A
↓
B
↓
C
↓
D
```
The simplest.

### Branching plan

```text
Check Website
|
+-- Available -> Scrape
|
+-- Down -> Search Backup
```
There's a decision in the middle.

### Looping plan

```text
Generate
↓
Evaluate
↓
Improve
↓
Generate Again
```
This is what often occurs in modern agents.

## Plan Horizon

How far ahead the planner thinks.

### Short horizon

```text
Goal
↓
Next Action
```
Simply determines the next step.

### Long horizon

```text
Goal
↓
Task 1
↓
Task 2
↓
Task 3
↓
Task 4
```
Planning the entire workflow from scratch.

## Hierarchical Planning

The large goal is broken down into subgoals. For example:
```text
Goal:
Launch Startup

Broken down into:
Market Research
Build MVP
Acquire Users

and Build MVP is further broken down into:
Frontend
Backend
Database
```
So the format is:
```text
Goal
|
+-- Subgoal A
|
+-- Subgoal B
|
+-- Subgoal C
```
Many modern planners work like this.