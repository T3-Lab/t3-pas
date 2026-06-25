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
    last_replaced_step: str=None

    
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

ALT_ACTION_MAP = {
    ("web_scraper", "no_connection"): "cached_content",
    ("web_scraper", "retry"): "web_scraper",
    ("web_scraper", "fallback"): "unknown",
}

class SimplePlanner:
    def create_plan(self, goal: Goal):
        template = PLAN_MAP.get(goal.intent)
        if template is None:
            return None
            
        plan = deepcopy(template)
        return plan
    
    def replan(self, plan: AgentPlan, tool, reason):
        alt_action = self._get_alt_action(tool, reason)
        if alt_action is None:
            return False
        
        plan.current_step -= 1
        plan.last_replaced_step = plan.steps[plan.current_step]
        plan.steps[plan.current_step] = alt_action

        return True
    
    def _get_alt_action(self, tool, reason):
        alt_action = ALT_ACTION_MAP.get((tool.name, reason))
        return alt_action