from typing import List

from app.schemas.security import SecurityVerdict, PolicyAction

def build_allow_verdict(
        inspector_used: str,
        risk_score: int=0,
        reasons: List[str] | None=None,
        matched_rules: List[str] | None=None
) -> SecurityVerdict:
    return SecurityVerdict(
        allowed = True,
        action = PolicyAction.ALLOW,
        risk_score = risk_score,
        reasons = reasons or [],
        matched_rules = matched_rules or [],
        inspector_used = inspector_used
    )

def build_block_verdict(
        inspector_used: str,
        risk_score: int,
        reasons: List[str] | None=None,
        matched_rules: List[str] | None=None
) -> SecurityVerdict:
    return SecurityVerdict(
        allowed = False,
        action = PolicyAction.BLOCK,
        risk_score = risk_score,
        reasons=reasons or [],
        matched_rules=matched_rules or [],
        inspector_used=inspector_used,
)