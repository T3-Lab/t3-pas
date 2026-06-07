from .agent import SimpleAgent
from .state import AgentContext
from rich.console import Console
import time

def render(result):
    if result["type"] in ["single_task", "state_single_task", "ood", "external_single", "error"]:
        return result["result"]

    elif result["type"] == "multi_task":
        rendered = ""
        for idx, res in enumerate(result["result"]):
            rendered += f"\nTask {idx + 1}: {render(res)}\n\n"

        return rendered.strip()
    
    elif result["type"] == "state_multi_task":
        return result["result"][-1]["result"]

    elif result["type"] == "external_nested":
        return "\n".join(
            item["content"]
            for item in result["result"]
        )
    
    elif result["type"] == "external_list":
        return "\n".join(
            v for v in result["result"]
        )

    elif result["type"] == "nested_single":
        return "\n".join(
            f"{key.capitalize()}: {value}"
            for key, value in result["result"].items()
        )

    else:
        return str(result)
    
def cli_level(lowered, agent):
    if "last result" in lowered:
            return {
                "type": "external_single",
                "success": True,
                "result": agent.context.last_result
            }

    elif "history" in lowered:
        return {
            "type": "external_nested",
            "success": True,
            "result": agent.context.history
        }
    
    elif "intro" in lowered:
        return {
            "type": "external_single",
            "success": True,
            "result": "Hello! I'm PAS, Primitive Agentic System."
        }
    
    elif "see trace" in lowered:
        return {
            "type": "external_list",
            "success": True,
            "result": agent.context.trace
        }

    elif "reset" in lowered:
        agent.context = AgentContext()
        return {
            "type": "external_single",
            "success": True,
            "result": "Agent context has been reset."
        }
    
    else:
        return None

def main():
    elapsed = time.time()
    console = Console()

    context = AgentContext()

    agent = SimpleAgent(context)

    console.print("[yellow]=== Welcome! ===[/yellow]")
    console.print("[blue]* Agent Commands:[/blue]")
    console.print("calc <expression>")
    console.print("summarize <text>")
    console.print("scrape <url>")
    console.print("analyze <url>")
    console.print("math problem")
    console.print("\n[blue]* Utility Commands:[/blue]")
    console.print("intro")
    console.print("history")
    console.print("last result")
    console.print("see trace")
    console.print("reset")
    console.print("exit")
    console.print("[blue]* You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history'[/blue]")

    while True:

        user_input = console.input("\nYou > ")

        if user_input.lower() == "exit":
            console.print(f"[cyan]Long session:[/cyan] {(time.time() - elapsed):.2f} seconds")
            break
        
        with console.status("[blue]Agent >[/blue] ..."):
            result = cli_level(user_input.lower(), agent)
            if not result:
                result = agent.run(user_input)

            console.print(f"\n[blue]Agent >[/blue] {render(result)}")