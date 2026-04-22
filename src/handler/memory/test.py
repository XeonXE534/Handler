from src.handler.core.core import CoreHandler
from rich.console import Console

console = Console()

while True:
    user_input = console.input("[yellow]Enter a statement or query (or 'exit' to quit): [/]")
    if user_input.lower() == "exit":
        break
    handler = CoreHandler()
    handler.handle_input(user_input)