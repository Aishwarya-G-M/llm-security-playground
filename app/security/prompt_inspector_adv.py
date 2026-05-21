import re
import yaml
from pathlib import Path

# Evolved from prompt_inspector.py (hardcoded patterns) to a
# domain-specific YAML-based pattern library.
# Sources: OWASP AITG-APP-01, puppetry-detector (BSD-3)

# --- Load patterns from YAML files at module startup ---
def _load_patterns(filename : str) -> list[re.Pattern]:
    """
    Loads regex patterns from a YAML file in the patterns/ directory.
    Compiles each pattern with IGNORECASE flag.
    """

    path = Path(__file__).parent / "patterns" / filename
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return [re.compile(pattern, re.IGNORECASE) for pattern in data["patterns"]]

# Load all pattern sets once when the module is first imported
BANKING_PATTERNS: list[re.Pattern] = _load_patterns("banking.yaml")
PAYMENTS_PATTERNS: list[re.Pattern] = _load_patterns("payments.yaml")
KYC_PATTERNS: list[re.Pattern] = _load_patterns("kyc.yaml")

ALL_PATTERNS: list[re.Pattern] = BANKING_PATTERNS + PAYMENTS_PATTERNS + KYC_PATTERNS


# --- Inspection Logic ---

def inspect_prompt(prompt: str) -> dict:
    """
    Checks a prompt against all fintech attack patterns.
    Returns is_safe flag, matched pattern if any, and original prompt.
    """
    matched = next(
        (pattern for pattern in ALL_PATTERNS if pattern.search(prompt)),
        None
    )

    if matched:
        return {
            "is_safe": False,
            "reason": f"Potential attack detected: pattern '{matched.pattern}' matched",
            "original_prompt": prompt
        }

    return {
        "is_safe": True,
        "reason": "No attack patterns detected",
        "original_prompt": prompt
    }
