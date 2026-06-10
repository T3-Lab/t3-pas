from enum import StrEnum, auto


class GoalStatus(StrEnum):
    NONE = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


class AgentState(StrEnum):
    IDLE = auto()
    PLANNING = auto()

    SUMMARIZING = auto()
    CALCULATING = auto()
    WEB_SCRAPING = auto()

    WAITING_ANSWER = auto()

class AgentContext:
    def __init__(self):
        self.history = []
        self.agent_trace = []

        self.state = AgentState.IDLE
        self.goal_status = GoalStatus.NONE

        self.artifacts = None
        self.current_goal = None
        self.current_plan = None

    def receive_new_goal(self, goal):
        self.current_goal = goal
        self.current_goal.status = GoalStatus.IN_PROGRESS
        self.add_trace(f"New goal assigned: {goal.intent}")
        self.transition_to(AgentState.PLANNING)

    def mark_goal_reached(self):
        self.current_goal.status = GoalStatus.COMPLETED
        self.transition_to(AgentState.IDLE)
        self.add_trace(f"Goal reached: {self.current_goal.intent}")

    def mark_goal_failed(self):
        self.current_goal.status = GoalStatus.FAILED
        self.transition_to(AgentState.IDLE)
        self.add_trace(f"Goal failed: {self.current_goal.intent}")

    def transition_to(self, new_state: AgentState):
        old_state = self.state.name
        self.state = new_state
        self.add_trace(f"Agent State: {old_state} -> {new_state.name}")

    def next_plan_step(self, plan):
        current_action = plan.steps[plan.current_step]
        self.add_trace(f"Current step: {current_action}.")
        if not plan.steps:
            self.add_trace("No steps in the plan")
            return None

        if plan.current_step >= len(plan.steps) - 1:
            self.add_trace("Plan completed.")
            return None
        
        plan.current_step += 1
        return plan.steps[plan.current_step]

    def add_history(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def set_plan(self, plan):
        self.current_plan = plan
        self.add_trace(f"Plan: \
                       \n goal: {self.current_plan.goal.intent} \
                       \n type: {self.current_plan.type} \
                       \n steps: {self.current_plan.steps}")

    def set_artifacts(self, artifacts):
        self.artifacts = artifacts

    def set_goal(self, goal):
        self.current_goal = goal

    def add_trace(self, trace):
        self.agent_trace.append(trace)