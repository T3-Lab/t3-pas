from .tools import TOOLS
from .planning import SimplePlanner, Goal
from .state import AgentState

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
    
    def _result_format(self, refer, result):
        out = {}
        if isinstance(refer, Goal):
            if refer.interactive:
                out[refer.intent] = result

            else:
                out[f"{refer.intent}({refer.target})"] = result

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
                "target": self.context.access_memory().search_semantic("user_math_problem_correct")
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
        
        elif lowered.startswith("my name is"):
            parts = user_input.split(maxsplit=3)
            payload = parts[-1] if len(parts) > 3 else ""
            return {
                "type": "memory_management",
                "goal": "update_semantic",
                "target": {"key": "user_name", "value": payload},
                "response": f"Hello {payload}"
            }

        else:
            return {
                "type": "error",
                "goal": "unknown",
                "target": None
            }

    def run_workflow(self, target, plan, result=None, results=None):
        """
        Run tool.
        """
        if results is None:
            results = {}

        memory = self.context.access_memory("working")
        current_step = self.context.next_plan_step()

        if current_step is not None:
            tool = TOOLS.get(current_step)
            result = tool.func(target) if tool.requires_input else tool.func()

            results.update(self._result_format(memory.current_goal, result))

        if current_step is None:
            return result, results

        if not result.get("success"):
            return result, results

        extracted = self.extract_content(result)
        
        return self.run_workflow(extracted, plan, result, results)
        
    def run_agent(self, user_input):
        """
        Full agent loop.
        """
        self.context.add_history("user", user_input)

        if self.context.state == AgentState.WAITING_ANSWER and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = self.context.access_memory("episodic")[-1].actions["math_problem"]
            memory = self.context.access_memory()

            if answer == last_problem["answer"]:
                result = {
                    "type": "single_dict",
                    "success": True,
                    "result": "Correct! Well done."
                }
                memory.update_semantic("user_math_problem_correct", True)

            else:
                result = {
                    "type": "single_dict",
                    "success": True,
                    "result": f"Wrong! The correct answer was {last_problem['answer']}."
                }
                memory.update_semantic("user_math_problem_correct", False)

            self.goal_reached()
            
            self.context.access_memory().add_episode(self.context.access_memory("working").current_goal, {"math_problem": result})

            self.context.add_history("agent", str(result))

            return result

        parse = self.parse(user_input)

        if parse.get("type") == "sequence_goal":
            multi_results = {}
            for i, target in enumerate(parse.get("target")):
                current_goal = parse.get("goal")[i]
                goal = Goal(intent=current_goal, target=target)
                plan = self.planner.create_plan(goal)
                goal.interactive = TOOLS.get("math_problem").name in plan.steps
            
                self.assign_goal(goal)
                self.assign_plan(plan)
                try:
                    self.context.to_execution()
                    result, results = self.run_workflow(goal.target, plan)
                    if goal.interactive:
                        self.context.to_waiting_answer()

                    multi_results.update(results)

                    if self.context.state != AgentState.WAITING_ANSWER:
                        if result["success"]:
                            self.goal_reached()

                        else:
                            self.goal_failed()

                    self.context.access_memory().add_episode(goal, results)

                except Exception as e:
                    self.goal_failed()

                    result = self._result_format(goal, {"type": "error", "success": False, "result": f"Error when processing user command {goal.intent}({goal.target}) ({str(e)})"})
                    multi_results.update(result)

                    self.context.access_memory().add_episode(goal, result)

            out = {"type": "nested_multi_dict", "result": multi_results}

            self.context.add_history("agent", str(out))

            return out
        
        elif parse.get("type") == "memory_management":
            if parse.get("goal") == "update_semantic":
                memory = self.context.access_memory()
                target = parse["target"]
                memory.update_semantic(target["key"], target["value"])

                out = {
                    "type": "single_dict",
                    "success": True,
                    "result": parse["response"]
                }

            return out

        elif parse.get("type") == "error":
            return {"type": "error", "success": False, "result": f"Unknown command {user_input}"}

        
        goal = Goal(intent=parse["goal"], target=parse["target"])
        plan = self.planner.create_plan(goal)
        goal.interactive = TOOLS.get("math_problem").name in plan.steps

        try:
            self.assign_goal(goal)
            self.assign_plan(plan)
        
        except Exception as e:
            return {"type": "error", "success": False, "result": f"Failed to assign plan or goal ({str(e)})"}
        
        try:
            self.context.to_execution()
            result, results = self.run_workflow(goal.target, plan)
            if goal.interactive:
                self.context.to_waiting_answer()

        except Exception as e:
            self.goal_failed()
            return {"type": "error", "success": False, "result": f"Failed to do {user_input} ({str(e)})"}


        if self.context.state != AgentState.WAITING_ANSWER:
            if result["success"]:
                self.goal_reached()

            else:
                self.goal_failed()

        self.context.add_history("agent", str(results))
        self.context.access_memory().add_episode(goal, results)

        return result