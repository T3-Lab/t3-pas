from .tools import TOOLS

class SimpleAgent:

    def __init__(self, state):
        self.state = state

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
            self.state.mode = "waiting_answer"
            return {
                "action": "math_problem"
            }
        
        elif lowered.startswith("analyze"):
            self.state.mode = "thinking"
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": ["web_scrapper", "summarizer"],
                "input": payload
            }
        
        elif lowered.startswith("scrape"):
            self.state.mode = "idle"
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "web_scrapper",
                "input": payload
            }

        elif lowered.startswith("calc"):
            self.state.mode = "idle"
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "calculator",
                "input": payload
            }

        elif "last result" in lowered:
            self.state.mode = "idle"
            return {
                "action": "last_result",
                "input": None
            }

        elif lowered == "history":
            self.state.mode = "idle"
            return {
                "action": "show_history"
            }
        
        elif "intro" in lowered:
            self.state.mode = "idle"
            return {
                "action": "intro"
            }

        elif "summarize" in lowered:
            self.state.mode = "idle"
            parts = user_input.split(maxsplit=1)
            payload = parts[1] if len(parts) > 1 else ""
            return {
                "action": "summarizer",
                "input": payload
            }

        else:
            self.state.mode = "idle"
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
            last_output = plan.get("input")
            for i, act in enumerate(action):
                tool = TOOLS.get(act)
                if not tool:
                    err = {
                        "type": "error",
                        "success": False,
                        "result": f"Tool '{act}' not found in pipeline"
                    }
                    results.append({act: err})
                    break

                try:
                    res = tool(last_output)
                except Exception as e:
                    res = {"type": "error", "success": False, "result": str(e)}

                results.append({act: res})

                if isinstance(res, dict):
                    if "result" in res and isinstance(res["result"], (str, list, dict)):
                        last_output = res["result"]
                    elif "result" in res and isinstance(res["result"], dict) and "content" in res["result"]:
                        last_output = res["result"]["content"]
                    else:
                        last_output = res
                else:
                    last_output = res

            self.state.add_trace(results)

            return {
                "type": "state_multi_task",
                "success": True,
                "result": results
            }


        if action == "show_history":
            return {
                "type": "nested",
                "success": True,
                "result": self.state.history
                }

        elif action == "last_result":
            return {
                "type": "single_task",
                "success": True,
                "result": self.state.last_result
                }
        
        elif action == "intro":
            return {
                "type": "single_task",
                "success": True,
                "result": "Hello! I'm PAS, Primitive Agentic System."
                }
        
        elif action == "math_problem":
            self.state.mode = "waiting_answer"
            return TOOLS["math_problem"]()

        elif action == "unknown":
            return {
                "type": "ood",
                "success": True,
                "result": "I don't understand that command."
                }

        tool = TOOLS.get(action)

        if not tool:
            return {
                "type": "error",
                "success": False,
                "result": f"{action} tool not found"
            }

        try:
            result = tool(plan["input"])
        except Exception as e:
            result = {"type": "error", "success": False, "result": str(e)}

        return result

    def run(self, user_input):
        """
        Full agent loop.
        """
        if self.state.mode == "waiting_answer" and user_input.strip().isdigit():
            answer = int(user_input.strip())
            last_problem = self.state.last_result
            if answer == last_problem["answer"]:
                result = {
                    "type": "single_task",
                    "success": True,
                    "result": "Correct! Well done."
                }
            else:
                result = {
                    "type": "single_task",
                    "success": False,
                    "result": f"Wrong! The correct answer was {last_problem['answer']}."
                }
            self.state.set_result(result)
            self.state.mode = "idle"
            return result
        
        self.state.mode = "idle"

        self.state.add_history("user", user_input)

        plan = self.think(user_input)

        result = self.act(plan)

        self.state.set_result(result)

        self.state.add_history("agent", str(result))

        return result