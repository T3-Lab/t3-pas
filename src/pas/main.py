from .agent import SimpleAgent
from .state import AgentState
from rich.console import Console

def main():
    console = Console()

    state = AgentState()

    agent = SimpleAgent(state)

    console.print("=== [yellow]Welcome![/yellow] ===")
    console.print("[blue]= Commands:[/blue]")
    console.print("intro")
    console.print("calc 2 + 2")
    console.print("history")
    console.print("last result")
    console.print("math problem")
    console.print("exit")
    console.print("[blue]= You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history'[/blue]")

    while True:

        user_input = console.input("\nYou > ")

        if user_input.lower() == "exit":
            break

        result = agent.run(user_input)

        if not isinstance(result['result'], list):
            console.print(f"\n[blue]Agent >[/blue] {result['result']}")

        else:
            for r in result['result']:
                console.print(f"\n[blue]Agent >[/blue] {r["result"]}")