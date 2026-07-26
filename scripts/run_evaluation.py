import json
from pathlib import Path


def load_evaluation_data(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)
