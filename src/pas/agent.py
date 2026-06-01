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
            tasks = lowered.split(" then ")
            return {
                "action": "multi_step",
                "input": tasks
            }
        
        if "math problem" in lowered:
            self.state.mode = "waiting_answer"
            return {
                "action": "math_problem"
            }

        if lowered.startswith("calc"):
            self.state.mode = "idle"
            return {
                "action": "calculator",
                "input": user_input[5:]
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
                "success": True,
                "result": results
            }

        if action == "show_history":
            return {"success": True,
                    "result": self.state.history}

        elif action == "unknown":
            return {"success": True,
                    "result": "I don't understand that command."}

        elif action == "last_result":
            return {"success": True,
                    "result": self.state.last_result}
        
        elif action == "intro":
            return {"success": True,
                    "result": "Hello! I'm PAS, Primitive Agentic System."}
        
        elif action == "math_problem":
            result = TOOLS["math_problem"]()
            self.state.set_result(result)
            return {
                "success": True,
                "result": result["result"]
            }

        tool = TOOLS.get(action)

        if not tool:
            return f"{action} tool not founded"

        result = tool(plan["input"])

        self.state.set_result(result)

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
                    "success": True,
                    "result": "Correct! Well done."
                }
            else:
                result = {
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

        self.state.add_history("agent", str(result))

        return result