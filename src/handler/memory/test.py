from src.handler.core.core import CoreHandler

while True:
    user_input = input("Enter a statement or query (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    handler = CoreHandler()
    handler.handle_input(user_input)