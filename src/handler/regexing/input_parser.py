# I have 0 experience with regex, so this is a bit of a mess

import re

class InputParser:
    def __init__(self):
        self.rules = [
            (r"user is (\w+)", ("user", "name")),
            (r"what is (\w+)", ("query", "is_a")),
            (r"(\w+) is (.+)", ("subject", "object")),
        ]

    def parse(self, input_str: str):
        input_str = input_str.lower().strip()
        for pattern, template in self.rules:
            match = re.search(pattern, input_str)
            if match:
                return dict(zip(template, match.groups()))
        return None