from src.handler.regexing.input_parser import InputParser
from src.handler.memory.triple import TripleStorageThingy
from rich import console

console = console.Console()

class CoreHandler:
    def __init__(self):
        self.parser = InputParser()
        self.memory = TripleStorageThingy()

    def handle_input(self, input_str: str):
        data = self.parser.parse(input_str)
        console.print(f"DEBUG: Parser returned {data}", style='dim')

        intent = data["intent"]
        groups = data["groups"]

        match intent:
            case "QUERY":
                self._query(groups[0].strip())

            case "STORE":
                self._store(groups[0].strip(), groups[1].strip())

            case "NAME":
                 self._name(groups[0].strip())

            case "GREET":
                console.print("Hello!! :3", style='green')

            case "UNKNOWN":
                console.print("Wdym? me no understand :(", style='red')
    def _query(self, query: str):
        results = self.memory.query_fact(query)
        if results:
            objects = [obj for obj, conf, src in results]
            console.print(f"{query} is: {', '.join(objects)}", style='yellow')
        else:
            console.print(f"no idea what {query} is yet :(", style='yellow')

    def _store(self, subject: str, obj: str):
        self.memory.store_fact(subject, "is_a", obj)
        console.print(f"Stored: {subject} is {obj}.", style='green')

    def _name(self, name: str):
        self.memory.store_fact("user", "name", name)
        console.print(f"Nice to meet you, {name}!", style='blue')

