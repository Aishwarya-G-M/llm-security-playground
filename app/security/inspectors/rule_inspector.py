from abc import ABC
import re

from app.schemas.security import SecurityVerdict
from app.security.inspectors.base import BaseInspector
from app.security.policy import build_block_verdict, build_allow_verdict


class RuleInspector(BaseInspector):
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"forget\s+(all\s+)?previous\s+instructions",
        r"reveal\s+(your\s+)?system\s+prompt",
        r"bypass\s+security",
    ]

    def inspect_text(self, text: str) -> SecurityVerdict:
        matched_rules = []

        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                matched_rules.append(pattern)

        if matched_rules:
            return build_block_verdict(
                inspector_used = "rule_inspector",
                risk_score = 8,
                reasons=["Potential prompt injection pattern detected"],
                matched_rules=matched_rules,
            )

        return build_allow_verdict(
            inspector_used="rule_inspector",
            risk_score=1,
            reasons=["No known prompt injection patterns detected"]
        )