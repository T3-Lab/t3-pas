from .agent import SimpleAgent
from .state import AgentContext
from rich.console import Console
import time

def render(result):
    if result["type"] in ["single_dict", "error"]:
        return result["result"]

    elif result["type"] == "multi_dict":
        rendered = ""
        for key, res in result["result"].items():
            rendered += f"\nTask {key}: {render(res)}\n\n"

        return rendered.strip()
    
    elif result["type"] == "single_list":
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
    if lowered.startswith("see artifact"):
            return {
                "type": "single_dict",
                "success": True,
                "result": agent.context.artifacts
            }

    elif lowered.startswith("history"):
        return {
            "type": "nested_dict",
            "success": True,
            "result": agent.context.history
        }
    
    elif lowered.startswith("intro"):
        return {
            "type": "single_dict",
            "success": True,
            "result": "Hello! I'm PAS, Primitive Agentic System."
        }
    
    elif lowered.startswith("see trace"):
        return {
            "type": "single_list",
            "success": True,
            "result": agent.context.agent_trace
        }

    elif lowered.startswith("reset"):
        agent.context = AgentContext()
        return {
            "type": "single_list",
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
    console.print("[dim](You can also chain tasks using 'then', e.g. 'calc 2 + 2 then history')[/dim]")
    console.print("\n[blue]* Utility Commands:[/blue]")
    console.print("intro")
    console.print("history")
    console.print("see artifact")
    console.print("see trace")
    console.print("reset")
    console.print("exit")

    while True:

        user_input = console.input("\nYou > ")

        if user_input.lower() == "exit":
            console.print(f"[cyan]Long session:[/cyan] {(time.time() - elapsed):.2f} seconds")
            break
        
        with console.status("[blue]Agent >[/blue] ..."):
            cli_res = cli_level(user_input.lower(), agent)
            if cli_res is not None:
                result = cli_res
            else:
                result = agent.run(user_input)

            console.print(f"\n[blue]Agent >[/blue] {render(result)}")