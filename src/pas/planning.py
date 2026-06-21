from .state import GoalStatus
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Goal:
    intent: str
    target: str
    status: GoalStatus = GoalStatus.NONE
    interactive: bool = False
    shift_belief: str=None


@dataclass
class AgentPlan():
    goal: str
    steps: list
    output_type: str
    current_step: int = 0

    
PLAN_MAP = {
    "analyze_web": AgentPlan(
        goal="analyze_web",
        steps=["web_scraper", "summarizer"],
        output_type="nested_multi_dict"
    ),
    "web_scrape": AgentPlan(
        goal="web_scrape",
        steps=["web_scraper"],
        output_type="nested_single_dict"
    ),
    "summarize_content": AgentPlan(
        goal="summarize_content",
        steps=["summarizer"],
        output_type="single_dict"
        ),
    "calculate": AgentPlan(
        goal="calculate",
        steps=["calculator"],
        output_type="single_dict"
    ),
    "math_problem": AgentPlan(
        goal="math_problem",
        steps=["math_problem"],
        output_type="single_dict"
    )
}

class SimplePlanner:
    def create_plan(self, goal: Goal):
        template = PLAN_MAP.get(goal.intent)
        if template is None:
            return None
            
        plan = deepcopy(template)
        return plan