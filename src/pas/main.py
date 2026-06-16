from .agent import SimpleAgent
from .state import AgentContext
from rich.console import Console
import time

def render(result):
    if result["type"] in ["single_dict", "error"]:
        return result["result"]

    elif result["type"] == "nested_multi_dict":
        rendered = ""
        for key, res in result["result"].items():
            rendered += f"\nTask {key}: {render(res)}\n\n"

        return rendered.strip()
    
    elif result["type"] == "nested_single_dict":
        return result["result"]["content"]
    
    elif result["type"] == "single_list":
        return "\n".join(
            str(v) for v in result["result"]
        )

    else:
        return str(result)
        
def cli_level(console, lowered, agent):
    if lowered.startswith("see history"):
        return {
            "type": "single_list",
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
    
    elif lowered.startswith("access memory"):
        splitted = lowered.split(" ")
        if len(splitted) < 3 or splitted[-1] not in ["episodic", "semantic"]:
          which = console.input("[cyan]System >[/cyan] Which memory (episodic, semantic): ").lower().strip()\
        
        else:
            which = splitted[-1]

        memory = agent.context.access_memory(which)
        if which == "episodic":
            return {
                "type": "single_list",
                "success": True,
                "result": memory
            }
        
        elif which == "semantic":
            return {
                "type": "single_dict",
                "success": True,
                "result": memory
            }

        else:
            return {
                "type": "error",
                "success": False,
                "result": f"can't access {which}"
            }

    elif lowered.startswith("reset"):
        agent.context.access_memory().reset_memory()
        return {
            "type": "single_dict",
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
    console.print("my name is <str>")
    console.print("calc <expression>")
    console.print("summarize <text>")
    console.print("scrape <url>")
    console.print("analyze <url>")
    console.print("math problem")
    console.print("[dim](You can also chain tasks using 'then', e.g. 'calc 2 + 2 then math problem')[/dim]")
    console.print("\n[blue]* Utility Commands:[/blue]")
    console.print("intro")
    console.print("see history")
    console.print("see trace")
    console.print("access memory <kind>")
    console.print("reset")
    console.print("exit")

    while True:

        user_input = console.input("\nYou > ")

        if user_input.lower() == "exit":
            console.print(f"[cyan]System >[/cyan] Long session: {(time.time() - elapsed):.2f} seconds")
            break

        cli_res = cli_level(console, user_input.lower(), agent)
        if cli_res is not None:
            result = cli_res

            console.print(f"\n[cyan]System >[/cyan] {render(result)}")

            continue
        
        with console.status("[blue]Agent >[/blue] ..."):
            result = agent.run_agent(user_input)

            console.print(f"\n[blue]Agent >[/blue] {render(result)}")