# Curated fintech attack prompt library
# Used for red team testing and demos
# Sources: OWASP AITG-APP-01, puppetry-detector (BSD-3)
import json
import os
import glob


def load_attack_catalog() -> list[dict]:
    catalog = []
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    for filepath in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(filepath, "r") as f:
            entires = json.load(f)
            catalog.extend(entires)
    return catalog

ATTACK_PROMPTS: list[dict] = load_attack_catalog()