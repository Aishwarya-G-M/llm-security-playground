from typing import Optional

# NOTE: This is the original rule-based inspector using hardcoded patterns.
# Kept for reference to show evolution to the YAML-based pattern library.
# See prompt_inspector_adv.py for the current implementation.

# List of known prompt injection patterns
INJECTION_PATTERNS: list[str] = [
    "ignore previous instructions",
    "ignore all instructions",
    "you are now",
    "forget your instructions",
    "disregard your",
    "override instructions",
    "system prompt",
    "act as if",
    "pretend you are",
    "your new instructions are",
    "ignore all previous instructions",
]

def inspect_prompt(prompt_text: str) -> dict:
    """
    Checks a prompt for known injection patterns.
    Returns a result dict with is_safe flag and matched pattern if any.
    """
    prompt_lower: str = prompt_text.lower()

    matched: Optional[str] = next(
        (pattern for pattern in INJECTION_PATTERNS if pattern in prompt_lower),
        None
    )
    if matched:
        return {
            "is_safe": False,
            "reason": f"Potential prompt injection detected: '{matched}'",
            "original_prompt": prompt_text
        }
    return {
        "is_safe": True,
        "reason": "No injection pattern detected.",
        "original_prompt": prompt_text
    }