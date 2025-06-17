import json
from pathlib import Path

DEFAULT_OUTPUT = Path("pump_results.json")


def save_results(tokens, path: Path = DEFAULT_OUTPUT):
    path.write_text(json.dumps(tokens, indent=2))

