from src.handler.regexing.input_parser import InputParser
from src.handler.memory.triple import TripleStorageThingy

class CoreHandler:
    def __init__(self):
        self.parser = InputParser()
        self.memory = TripleStorageThingy()

    def handle_input(self, input_str: str):
        data = self.parser.parse(input_str)
        print(f"DEBUG: Parser returned {data}")
        if not data:
            print("[ERR] Invalid input format. Please try again.")
            return

        if "user" in data:
            name = data["user"]
            self.memory.store_fact("user", "name", name)
            print(f"Nice to meet you, {name}!")

        elif "query" in data:
            query = data["query"]
            result = self.memory.query_fact(query)
            print(f"{query} is {result}.")

        elif "subject" in data:
            subject = data["subject"]
            obj = data["object"]
            self.memory.store_fact(subject, "is", obj)
            print(f"Stored: {subject} is {obj}.")

        else:
            print("[ERR] Unrecognized input. Please try again.")