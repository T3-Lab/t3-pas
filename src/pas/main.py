from .agent import SimpleAgent
from .state import AgentState
from rich.console import Console
import time

def render(result):
    if result["type"] in ["single_task", "state_single_task", "ood"]:
        return result["result"]

    elif result["type"] == "multi_task":
        rendered = ""
        for idx, res in enumerate(result["result"]):
            rendered += f"Task {idx + 1}:\n{render(res)}\n\n"

        return rendered.strip()
    
    elif result["type"] == "state_multi_task":
        return result["result"]

    elif result["type"] == "nested":
        return "\n".join(
            item["content"]
            for item in result["result"]
        )

    elif result["type"] == "nested_single":
        return "\n".join(
            f"{key.capitalize()}: {value}"
            for key, value in result["result"].items()
        )

    else:
        return str(result)

def main():
    elapsed = time.time()
    console = Console()

    state = AgentState()

    agent = SimpleAgent(state)

    console.print("[yellow]=== Welcome! ===[/yellow]")
    console.print("[blue]= Commands:[/blue]")
    console.print("intro")
    console.print("calc <expression>")
    console.print("summarize <text>")
    console.print("scrape <url>")
    console.print("analyze <url>")
    console.print("history")
    console.print("last result")
    console.print("math problem")
    console.print("exit")
    console.print("[blue]= You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history'[/blue]")

    while True:

        user_input = console.input("\nYou > ")

        if user_input.lower() == "exit":
            console.print(f"[cyan]Long session:[/cyan] {(time.time() - elapsed):.2f} seconds")
            break
        
        with console.status("[blue]Agent >[/blue] ...") as status:
            result = agent.run(user_input)

            console.print(f"\n[blue]Agent >[/blue] {render(result)}")