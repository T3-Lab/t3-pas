from .tools import TOOLS, STATE_MAP

class SimpleAgent:
    def __init__(self, context):
        self.context = context

    def assign_goal(self, goal):
        self.context.receive_new_goal(goal)

    def set_state(self, new_state):
        self.context.transition_to(new_state)
    
    def goal_reached(self):
        self.context.mark_goal_reached()

    def think(self, user_input):
        """
        Simple decision making.
        """

        lowered = user_input.lower()

        if " then " in lowered:
            tasks = [t.strip() for t in lowered.split(" then ") if t.strip()]
            return {
                "action": "multi_step",
                "input": tasks
            }
        
        if "math problem" in lowered:
            return {
                "action": "math_problem"
            }
        
        elif lowered.startswith("analyze"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": ["web_scrapper", "summarizer"],
                "input": payload
            }
        
        elif lowered.startswith("scrape"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "web_scrapper",
                "input": payload
            }

        elif lowered.startswith("calc"):
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "calculator",
                "input": payload
            }

        elif "summarize" in lowered:
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "summarizer",
                "input": payload
            }

        else:
            return {
                "action": "unknown"
            }

    def act(self, plan):
        """
        Run tool.
        """

        action = plan["action"]

        if action == "multi_step":
            results = []
            for task in plan["input"]:
                plan = self.think(task)
                result = self.act(plan)
                results.append(result)

            return {
                "type": "multi_task",
                "success": True,
                "result": results
            }

        if isinstance(action, list):
            results = []
            tool = TOOLS.get(action[0], None)
            for i, act in enumerate(action):
                if i == 0:
                    self.set_state(STATE_MAP.get(act))
                    result = tool(plan["input"])
                    results.append(result)

                else:
                    tool = TOOLS.get(act, None)
                    if not tool:
                        results.append({
                            "type": "error",
                            "success": False,
                            "result": f"{act} tool not found"
                        })
                        continue

                    self.set_state(STATE_MAP.get(act))
                    result = tool(results[-1]["result"])
                    results.append(result)

            return {
                "type": "state_multi_task",
                "success": True,
                "result": results
            }
        
        if action == "math_problem":
            self.set_state(STATE_MAP.get("math_problem"))
            return TOOLS["math_problem"]()

        elif action == "unknown":
            return {
                "type": "ood",
                "success": True,
                "result": "I don't understand that command."
                }

        tool = TOOLS.get(action, None)

        if not tool:
            return {
                "type": "error",
                "success": False,
                "result": f"{action} tool not found"
            }

        try:
            self.set_state(STATE_MAP.get(action))
            result = tool(plan["input"])
        except Exception as e:
            result = {"type": "error", "success": False, "result": str(e)}

        return result

    def run(self, user_input):
        """
        Full agent loop.
        """
        if self.context.state.value == "waiting_answer" and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = self.context.last_result
            if last_problem.get("type") != "state_single_task":
                if last_problem.get("type") == "multi_task":
                    for res in reversed(last_problem.get("result", [])):
                        if isinstance(res, dict) and "answer" in res.keys():
                            last_problem = res
                            break

                else:
                    return {
                        "type": "error",
                        "success": False,
                        "result": "No math problem awaiting answer."
                    }
                
            if answer == last_problem["answer"]:
                result = {
                    "type": "single_task",
                    "success": True,
                    "result": "Correct! Well done."
                }
            else:
                result = {
                    "type": "single_task",
                    "success": True,
                    "result": f"Wrong! The correct answer was {last_problem['answer']}."
                }
            self.context.set_result(result)
            self.goal_reached()
            return result

        self.context.add_history("user", user_input)

        self.assign_goal(user_input)

        plan = self.think(user_input)

        result = self.act(plan)

        if self.context.state.value != "waiting_answer":
            self.goal_reached()

        self.context.set_result(result)

        self.context.add_history("agent", str(result))

        return result