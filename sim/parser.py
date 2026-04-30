from __future__ import annotations
import json
from pathlib import Path


class Parser:
    @staticmethod
    def load(filepath: str) -> dict:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        with open(path) as f:
            return json.load(f)
