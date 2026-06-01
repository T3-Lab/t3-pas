class AgentState:
    def __init__(self):
        self.history = []
        self.mode = "idle"
        self.last_result = None
        self.current_goal = None

    def add_history(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def set_result(self, result):
        self.last_result = result

    def set_goal(self, goal):
        self.current_goal = goal