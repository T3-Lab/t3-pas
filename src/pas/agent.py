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
            "goal_type": "sequence_goal",
            "goal": []
        }
        for task in tasks:
            result = self.parse(task)

            if result["goal_type"] == "error":
                return {"goal_type": "error", "goal": "unknown"}

            out["goal"].append(result["goal"])

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
            target = self.context.belief["user_math_skill_advance"]
            return {
                "goal_type": "single_goal",
                "goal": Goal(
                    intent="math_problem", 
                    target=target, 
                    interactive=True, 
                    shift_belief="user_math_skill_advance")
            }
        
        elif lowered.startswith("analyze"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "goal_type": "single_goal",
                "goal": Goal(
                    intent="analyze_web", 
                    target=payload,
                    shift_belief="internet_access")
            }
        
        elif lowered.startswith("scrape"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "goal_type": "single_goal",
                "goal": Goal(
                    intent="web_scrape", 
                    target=payload,
                    shift_belief="internet_access")
            }

        elif lowered.startswith("calc"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "goal_type": "single_goal",
                "goal": Goal(intent="calculate", target=payload)
            }

        elif lowered.startswith("summarize"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "goal_type": "single_goal",
                "goal": Goal(intent="summarize_content", target=payload)
            }
        
        elif lowered.startswith("my name is"):
            parts = user_input.split(maxsplit=3)
            payload = parts[-1] if len(parts) > 3 else ""
            return {
                "goal_type": "memory_management",
                "goal": Goal(intent="update_semantic", target={"key": "user_name", "value": payload}),
                "response": f"Hello {payload}"
            }

        else:
            return {
                "goal_type": "error",
                "goal": "unknown"
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
        memory = self.context.access_memory()

        if self.context.state == AgentState.WAITING_ANSWER and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = memory.search_episode("math_problem")
            if last_problem:
                last_problem = last_problem[0].actions["math_problem"]

                if answer == last_problem["answer"]:
                    result = {
                        "output_type": "single_dict",
                        "success": True,
                        "result": "Correct! Well done.",
                        "correct": True
                    }
                    memory.update_semantic("math_correct_answer", 1, "in_place")

                else:
                    result = {
                        "output_type": "single_dict",
                        "success": True,
                        "result": f"Wrong! The correct answer was {last_problem['answer']}.",
                        "correct": False
                    }

                self.goal_reached()
                memory.update_semantic("total_math_question", 1, "in_place")

                if len(memory.search_episode("math_problem_answer")) >= 3:
                    semantic = memory.semantic.knowledge
                    if (semantic["math_correct_answer"] / semantic["total_math_question"]) > 0.8:
                        self.context.set_belief(memory.working.current_goal.shift_belief, True)

                    else:
                        self.context.set_belief(memory.working.current_goal.shift_belief, False)

            else:
                result = {
                    "output_type": "error",
                    "success": False,
                    "result": "No math question"
                }

            memory.add_episode(memory.working.current_goal, {"math_problem_answer": result})

            self.context.add_history("agent", str(result))

            return result

        parse = self.parse(user_input)

        if parse["goal_type"] == "sequence_goal":
            multi_results = {}
            for goal in parse["goal"]:
                plan = self.planner.create_plan(goal)
            
                self.assign_goal(goal)
                self.assign_plan(plan)

                try:
                    self.context.to_execution()
                    result, results = self.run_workflow(goal.target, plan)

                    if result is None:
                        raise ValueError("Result is None implicating there's no step in the plan")

                    if goal.interactive:
                        self.context.to_waiting_answer()

                    multi_results.update(results)

                    if self.context.state != AgentState.WAITING_ANSWER:
                        if result["success"]:
                            self.goal_reached()

                        else:
                            self.goal_failed()

                    memory.add_episode(goal, results)

                except Exception as e:
                    self.goal_failed()

                    result = self._result_format(goal, {"output_type": "error", "success": False, "result": f"Error when processing user command {goal.intent}({goal.target}) ({str(e)})"})
                    multi_results.update(result)

                    memory.add_episode(goal, result)

            out = {"output_type": "nested_multi_dict", "result": multi_results}

            self.context.add_history("agent", str(out))

            return out
        
        elif parse["goal_type"] == "memory_management":
            goal = parse["goal"]
            if goal.intent == "update_semantic":
                memory.update_semantic(goal.target["key"], goal.target["value"])

                out = {
                    "output_type": "single_dict",
                    "success": True,
                    "result": parse["response"]
                }

            return out

        elif parse["goal_type"] == "error":
            return {"output_type": "error", "success": False, "result": f"Unknown command {user_input}"}

        
        goal = parse["goal"]
        plan = self.planner.create_plan(goal)

        try:
            self.assign_goal(goal)
            self.assign_plan(plan)
        
        except Exception as e:
            return {"output_type": "error", "success": False, "result": f"Failed to assign plan or goal ({str(e)})"}
        
        try:
            self.context.to_execution()
            result, results = self.run_workflow(goal.target, plan)

            if result is None:
                        raise ValueError("Result is None implicating there's no step in the plan")

            if goal.interactive:
                self.context.to_waiting_answer()

        except Exception as e:
            self.goal_failed()
            return {"output_type": "error", "success": False, "result": f"Failed to do {user_input} ({str(e)})"}


        if self.context.state != AgentState.WAITING_ANSWER:
            if result["success"]:
                self.goal_reached()

            else:
                self.goal_failed()

        self.context.add_history("agent", str(results))
        memory.add_episode(goal, results)

        return result