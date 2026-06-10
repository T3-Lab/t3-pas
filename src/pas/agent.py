from .tools import TOOLS, STATE_MAP, TYPE_MAP, TOOL_KIND_MAP
from .planning import SimplePlanner, Goal, GOAL_KIND_MAP

class SimpleAgent:
    def __init__(self, context):
        self.context = context
        self.planner = SimplePlanner()

    def _multi_parsing(self, user_input):
        tasks = [t.strip() for t in user_input.lower().split(" then ") if t.strip()]
        out = {
            "type": "sequence_goal",
            "goal": [],
            "target": []
        }
        for task in tasks:
            result = self.parse(task)

            if result.get("type") == "error":
                return {"type": "error", "goal": "unknown", "target": None}

            out.get("goal").append(result.get("goal"))
            out.get("target").append(result.get("target"))

        return out

    def extract_content(self, content):
        layer_1 = content["result"]
        if isinstance(layer_1, dict) and "content" in layer_1.keys():
            layer_2 = layer_1["content"]
            return layer_2
        
        return layer_1

    def assign_goal(self, goal):
        self.context.receive_new_goal(goal)

    def assign_plan(self, plan):
        self.context.set_plan(plan)

    def set_state(self, new_state):
        self.context.transition_to(new_state)
    
    def goal_reached(self):
        self.context.mark_goal_reached()

    def goal_failed(self):
        self.context.mark_goal_failed()

    def parse(self, user_input):
        """
        Parse user input.
        """
        lowered = user_input.lower().strip()

        if " then " in lowered:
            result = self._multi_parsing(user_input)
            return result
        
        if lowered.startswith("math problem"):
            return {
                "type": "single_goal",
                "goal": "math_problem",
                "target": None
            }
        
        elif lowered.startswith("analyze"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "type": "single_goal",
                "goal": "analyze_web",
                "target": payload
            }
        
        elif lowered.startswith("scrape"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "type": "single_goal",
                "goal": "web_scrape",
                "target": payload
            }

        elif lowered.startswith("calc"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "type": "single_goal",
                "goal": "calculate",
                "target": payload
            }

        elif lowered.startswith("summarize"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "type": "single_goal",
                "goal": "summarize_content",
                "target": payload
            }

        else:
            return {
                "type": "error",
                "goal": "unknown",
                "target": None
            }

    def act(self, target, plan, last_result=None):
        """
        Run tool.
        """
        if last_result is None:
            last_result = {}
        current_step = plan.steps[plan.current_step]
        self.set_state(STATE_MAP[current_step])
        tool = TOOLS.get(current_step)
        result = tool(target) if current_step in TOOL_KIND_MAP["with_input"] else tool()

        if current_step in GOAL_KIND_MAP["interactive"]:
            last_result[current_step] = result

        else:
            last_result[f"{current_step}({plan.goal.target})"] = result

        next_step = self.context.next_plan_step(plan)
        
        if next_step is None:
            return result, last_result
        
        result = self.extract_content(result)
        return self.act(result, plan, last_result)
        
    def run(self, user_input):
        """
        Full agent loop.
        """
        if self.context.state.value == "waiting_answer" and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = self.context.artifacts["math_problem"]
                
            if answer == last_problem["answer"]:
                result = {
                    "type": "single_dict",
                    "success": True,
                    "result": "Correct! Well done."
                }
            else:
                result = {
                    "type": "single_dict",
                    "success": True,
                    "result": f"Wrong! The correct answer was {last_problem['answer']}."
                }
            self.context.set_artifacts({"math_problem_answer": result})
            self.goal_reached()
            
            self.context.add_history("user", user_input)
            self.context.add_history("agent", str(result))

            return result

        self.context.add_history("user", user_input)
        parse = self.parse(user_input)

        if parse.get("type") == "error":
            return {"type": "error", "success": False, "result": f"Unknown command {user_input}"}

        if parse.get("type") == "sequence_goal":
            multi_results = {}
            for i, target in enumerate(parse.get("target")):
                try:
                    current_goal = parse.get("goal")[i]
                    goal = Goal(intent=current_goal, target=target)
                    plan = self.planner.create_plan(TYPE_MAP[current_goal], goal, user_input.split(" then ")[i])
                
                except Exception as e:
                    return {"type": "error", "success": False, "result": f"Unknown command {user_input}"}

                try:
                    self.assign_goal(goal)
                    self.assign_plan(plan)

                except Exception as e:
                    return {"type": "error", "success": False, "result": f"Failed to assign plan or goal"}

                try:
                    result, _ = self.act(plan.goal.target, plan)
                    if goal.intent in GOAL_KIND_MAP["interactive"]:
                        multi_results[goal.intent] = result
                    
                    else:
                        multi_results[f"{goal.intent}({goal.target})"] = result

                except Exception as e:
                    self.goal_failed()
                    return {"type": "error", "success": False, "result": f"unknown command {user_input}"}

            self.context.set_artifacts(multi_results)
            out = {"type": "multi_dict", "result": multi_results}

            if self.context.state.value != "waiting_answer":
                self.goal_reached()

            self.context.add_history("agent", str(out))

            return out
        
        goal = Goal(intent=parse["goal"], target=parse["target"])
        plan = self.planner.create_plan(TYPE_MAP[goal.intent], goal, user_input)

        try:
            self.assign_goal(goal)
            self.assign_plan(plan)
        
        except Exception as e:
            return {"type": "error", "success": False, "result": f"Failed to assign plan or goal"}
        
        try:
            result, results = self.act(plan.goal.target, plan)

        except Exception as e:
            self.goal_failed()
            return {"type": "error", "success": False, "result": f"Failed to do {user_input}"}

        if self.context.state.value != "waiting_answer":
            self.goal_reached()

        self.context.set_artifacts(results)

        self.context.add_history("agent", str(results))

        return result