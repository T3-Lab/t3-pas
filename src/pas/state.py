from enum import StrEnum, auto

class AgentState(StrEnum):
    IDLE = auto()
    PLANNING = auto()

    SUMMARIZING = auto()
    CALCULATING = auto()
    WEB_SCRAPING = auto()

    WAITING_ANSWER = auto()

class GoalStatus(StrEnum):
    NONE = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

class AgentContext:
    def __init__(self):
        self.history = []
        self.trace = []

        self.state = AgentState.IDLE
        self.goal_status = GoalStatus.NONE

        self.last_result = None
        self.current_goal = None

    def receive_new_goal(self, goal):
        self.current_goal = goal
        self.goal_status = GoalStatus.IN_PROGRESS
        self.add_trace(f"New goal assigned: {goal}")
        self.transition_to(AgentState.PLANNING)

    def mark_goal_reached(self):
        self.goal_status = GoalStatus.COMPLETED
        self.transition_to(AgentState.IDLE)
        self.add_trace(f"Goal reached: {self.current_goal}")

    def transition_to(self, new_state: AgentState):
        old_state = self.state.name
        self.state = new_state
        self.add_trace(f"Agent State: {old_state} -> {new_state.name}")

    def add_history(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def set_result(self, result):
        self.last_result = result

    def set_goal(self, goal):
        self.current_goal = goal

    def add_trace(self, trace):
        self.trace.append(trace)