from .tools import TOOLS
from .planning import Goal, ALT_ACTION_MAP, SimplePlanner
from .state import AgentState, AgentContext

class SimpleAgent:
    def __init__(self, context: AgentContext):
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

            if result["goal"] == "unknown":
                return {"goal_type": "error", "goal": "unknown"}

            out["goal"].append(result["goal"])

        return out
    
    def _result_format(self, refer, action, target, result):
        out = {}
        if isinstance(refer, Goal):
            if refer.interactive:
                out[action] = result

            else:
                out[f"{action}({target})"] = result

        return out
    
    def _connection_check(self, status_code):
        if status_code == 200:
            return "success"
        elif status_code == 0:
            return "no_connection"
        elif status_code == -1:
            return "parse_failed"
        elif status_code in (429, 500, 502, 503, 504):
            return "retry"
        elif status_code in (400, 401, 403, 404, 410):
            return "fallback"
        else:
            return "unknown"
        
    def _get_cached_content(self, goal, action, target):
        memory = self.context.access_memory()
        results = []

        if not goal.interactive:
            episodes = memory.search_episode(action, target)

        else:
            episodes = memory.search_episode(action, target)

        for episode in episodes:
            result = episode.result
            results.append(result)

        return results

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

    def replanning(self, tool, reason):
        self.context.transition_to(AgentState.REPLANNING)
        memory = self.context.access_memory("working")
        valid = self.planner.replan(memory.current_plan, tool, reason)
        if valid:
            self.context.add_trace(f"[Replan] New plan: \
                       \n goal: {memory.current_plan.goal} \
                       \n steps: {memory.current_plan.steps} \
                       \n output type: {memory.current_plan.output_type}")
            
        else:
            self.context.add_trace(
                f"Replan failed: {reason}"
            )
        
        return valid

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

    def execute_single_goal(self, goal):
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

            if self.context.state != AgentState.WAITING_ANSWER:
                if result["success"]:
                    self.goal_reached()

                else:
                    self.goal_failed()

        except Exception as e:
            self.goal_failed()

            result = {"output_type": "single_dict", "success": False, "result": f"Error when processing user command {goal.intent}({goal.target}) ({str(e)})"}
            results = self._result_format(goal, goal.intent, goal.target, result)

        return result, results

    def run_workflow(self, target, plan, result=None, results=None):
        """
        Run tool.
        """
        if results is None:
            results = {}

        memory = self.context.access_memory()
        goal = memory.working.current_goal
        current_step = self.context.next_plan_step()
        success = True

        if current_step is not None:
            tool = TOOLS.get(current_step)
            if not tool:
                if current_step in ALT_ACTION_MAP.values():
                    if current_step == "cached_content":
                        content = self._get_cached_content(goal, plan.last_replaced_step, goal.target)

                        if not content:
                            result = {"output_type": "single_dict", "success": False, "result": f"Unable to get cached content, no relevant cache"}
                            success = False

                        else:
                            result = content[0]

                    else:
                        result = {"output_type": "single_dict", "success": False, "result": f"Unable to fallback {current_step}"}
                        success = False

                else:
                    result = {"output_type": "single_dict", "success": False, "result": f"Invalid plan step {current_step}"}
                    success = False

                if not success:
                    memory.add_episode(goal, plan.last_replaced_step, result)
                    return result, results

                results.update(self._result_format(goal, plan.last_replaced_step, target, result))
                memory.add_episode(goal, plan.last_replaced_step, result)

            else:
                result = tool.func(target) if tool.requires_input else tool.func()
                results.update(self._result_format(goal, current_step, target, result))

                memory.add_episode(goal, current_step, result)

            if tool and tool.requires_internet:
                status = self._connection_check(result["result"]["status"])

                if status != "success":
                    memory.update_semantic("last_connection_problem", result["result"])

                    if status == "no_connection":
                        self.context.set_belief("internet_access", False)

                        success = self.replanning(tool, status)

                        if success:
                            self.context.to_execution()

                    else:
                        return result, results
                
                else:
                    self.context.set_belief("internet_access", True)

            extracted = self.extract_content(result)
            return self.run_workflow(extracted, plan, result, results)

        else:
            return result, results
        
    def run_agent(self, user_input):
        """
        Full agent loop.
        """
        self.context.add_history("user", user_input)
        memory = self.context.access_memory()

        if self.context.state == AgentState.WAITING_ANSWER and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = memory.search_episode("math_problem", memory.working.current_goal.target)
            if last_problem:
                last_problem = last_problem[0].result

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

                if len(memory.search_episode("math_problem_answer", memory.working.current_goal.target)) >= 3:
                    semantic = memory.semantic.knowledge
                    if (semantic["math_correct_answer"] / semantic["total_math_question"]) > 0.8:
                        self.context.set_belief("user_math_skill_advance", True)

                    else:
                        self.context.set_belief("user_math_skill_advance", False)

            else:
                result = {
                    "output_type": "single_dict",
                    "success": False,
                    "result": "No math question"
                }

            memory.add_episode(memory.working.current_goal, "math_problem_answer", result)

            self.context.add_history("agent", str(result))

            return result

        parse = self.parse(user_input)

        if parse["goal_type"] == "sequence_goal":
            multi_results = {}
            for goal in parse["goal"]:
                _, results = self.execute_single_goal(goal)
                multi_results.update(results)

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

        elif parse["goal"] == "unknown":
            return {"output_type": "single_dict", "success": False, "result": f"Unknown command {user_input}"}

        
        goal = parse["goal"]
        result, results = self.execute_single_goal(goal)

        self.context.add_history("agent", str(results))

        return result