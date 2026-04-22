# I have 0 experience with regex, so this(and rules.toml) is a bit of a mess
# Regex stuff was mostly done by Claude

import re
import tomllib
from pathlib import Path

class InputParser:
    def __init__(self):
        self.file_path = Path(__file__).parent / "rules.toml"
        with open(self.file_path, "rb") as f:
            self.config = tomllib.load(f)
        
        self.intents = {
            "QUERY": {"intent": "query", "keys": ["query"]},
            "STORE": {"intent": "store", "keys": ["subject", "object"]},
            "GREET": {"intent": "greet", "keys": []},
            "NAME": {"intent": "name", "keys": ["name"]},
        }

        self.patterns = []
        for name, info in self.intents.items():
            for pattern in self.config["intents"][name]["patterns"]:
                self.patterns.append({
                    "intent": info["intent"],
                    "keys": info["keys"],
                    "pattern": re.compile(pattern)
                })

    @staticmethod
    def _match_pattern(pattern_info, text):
        match = pattern_info["pattern"].search(text)
        if not match:
            return None

        result = {"intent": pattern_info["intent"]}
        groups = match.groups()

        for key, value in zip(pattern_info["keys"], groups):
            result[key] = value

        return result

    def parse(self, input_str: str):
        text = input_str.lower().strip()
        for pattern in self.patterns:
            result = self._match_pattern(pattern, text)
            if result:
                return result
        return None