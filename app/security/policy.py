from app.schemas.security import PolicyAction, SecurityVerdict

def build_allow_verdict(
    inspector_used: str,
    risk_score: int = 1,
    reasons: list[str] | None = None,
    matched_rules: list[str] | None = None,
) -> SecurityVerdict:
    return SecurityVerdict(
        allowed=True,
        action=PolicyAction.ALLOW,
        risk_score=risk_score,
        reasons=reasons or [],
        matched_rules=matched_rules or [],
        inspector_used=inspector_used,
    )


def build_block_verdict(
    inspector_used: str,
    risk_score: int,
    reasons: list[str] | None = None,
    matched_rules: list[str] | None = None,
) -> SecurityVerdict:
    return SecurityVerdict(
        allowed=False,
        action=PolicyAction.BLOCK,
        risk_score=risk_score,
        reasons=reasons or [],
        matched_rules=matched_rules or [],
        inspector_used=inspector_used,
    )