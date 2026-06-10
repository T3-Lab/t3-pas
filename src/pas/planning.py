from .state import GoalStatus
from dataclasses import dataclass

PLAN_MAP = {
    "analyze": [
        "web_scrapper",
        "summarizer"
    ],
    "scrape": [
        "web_scrapper"
    ],
    "summarize": [
        "summarizer"
    ],
    "calc": [
        "calculator"
    ],
    "math problem": [
        "math_problem"
    ]
}

GOAL_KIND_MAP = {
    "interactive": ["math_problem"]
}

@dataclass
class Goal:
    intent: str
    target: str
    status: GoalStatus = GoalStatus.NONE

@dataclass
class AgentPlan():
    goal: object
    type: str
    steps: list[str]
    current_step: int = 0

class SimplePlanner:
    def create_plan(self, type, goal, user_input: str):
        lowered = user_input.lower().strip()

        for intent, steps in PLAN_MAP.items():
            if lowered.startswith(intent):
                return AgentPlan(
                    goal=goal,
                    type=type,
                    steps=steps
                )
            
        return AgentPlan(
            goal=goal,
            type="unknown",
            steps=["unknown"]
        )