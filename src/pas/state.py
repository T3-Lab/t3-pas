from enum import StrEnum, auto
from dataclasses import dataclass, field
from typing import Literal
import time

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: float = field(default_factory=time.time)


class GoalStatus(StrEnum):
    NONE = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class Episode:
    goal: str
    goal_status: GoalStatus
    actions: dict
    timestamp: float = field(default_factory=time.time)


class AgentState(StrEnum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    WAITING_ANSWER = auto()


class WorkingMemory:
    def __init__(self):
        self.current_plan = None
        self.current_goal = None  


class EpisodicMemory:
    def __init__(self):
        self.episodes: list[Episode] = []


class SemanticMemory:
    def __init__(self):
        self.knowledge = {
            "user_name": None,
            "user_math_problem_correct": None
        }


class AgentMemory:
    def __init__(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def goal_status(self, status):
        self.working.current_goal.status = status

    def set_goal(self, goal):
        self.working.current_goal = goal

    def set_plan(self, plan):
        self.working.current_plan = plan

    def add_episode(self, goal, actions):
        self.episodic.episodes.append(Episode(goal.intent, goal.status, actions))

    def update_semantic(self, key, value):
        self.semantic.knowledge[key] = value

    def search_semantic(self, key):
        return self.semantic.knowledge.get(key)

    def reset_memory(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()


class AgentContext:
    def __init__(self):
        self.history = []
        self.agent_trace = []

        self.state = AgentState.IDLE

        self.memory = AgentMemory()

    def receive_new_goal(self, goal):
        self.memory.set_goal(goal)
        self.memory.goal_status(GoalStatus.IN_PROGRESS)
        self.add_trace(f"New goal assigned: {goal.intent}")
        self.transition_to(AgentState.PLANNING)

    def mark_goal_reached(self):
        self.memory.goal_status(GoalStatus.COMPLETED)
        self.transition_to(AgentState.IDLE)
        self.add_trace(f"Goal reached: {self.memory.working.current_goal.intent}")

    def mark_goal_failed(self):
        self.memory.goal_status(GoalStatus.FAILED)
        self.transition_to(AgentState.IDLE)
        self.add_trace(f"Goal failed: {self.memory.working.current_goal.intent}")

    def transition_to(self, new_state: AgentState):
        old_state = self.state.name
        self.state = new_state
        self.add_trace(f"Agent State: {old_state} -> {new_state.name}")

    def to_execution(self):
        self.transition_to(AgentState.EXECUTING)

    def to_waiting_answer(self):
        self.transition_to(AgentState.WAITING_ANSWER)

    def next_plan_step(self):
        current_plan = self.access_memory("working").current_plan

        if not current_plan.steps:
            self.add_trace("No steps in the plan")
            return None

        if current_plan.current_step >= len(current_plan.steps):
            self.add_trace("Plan completed.")
            return None
        
        current_action = current_plan.steps[current_plan.current_step]
        self.add_trace(f"Current step: {current_action}.")
        
        current_plan.current_step += 1
        return current_action

    def add_history(self, role, content):
        self.history.append(ChatMessage(role, content))

    def set_plan(self, plan):
        memory = self.access_memory("working")
        self.memory.set_plan(plan)
        self.add_trace(f"Plan: \
                       \n goal: {memory.current_plan.goal} \
                       \n steps: {memory.current_plan.steps} \
                       \n output type: {memory.current_plan.output_type}")

    def add_trace(self, trace):
        self.agent_trace.append(trace)

    def access_memory(self, kind: Literal["working", "episodic", "semantic"]=None):
        if kind == "working":
            return self.memory.working

        elif kind == "episodic":
            return self.memory.episodic.episodes
        
        elif kind == "semantic":
            return self.memory.semantic.knowledge
        
        return self.memory