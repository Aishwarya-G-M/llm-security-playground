from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class PolicyAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    REDACT = "redact"
    REVIEW = "review"


class SecurityVerdict(BaseModel):
    allowed: bool
    action: PolicyAction
    risk_score: int = Field(ge=0, le=10)
    reasons: List[str] = Field(default_factory=list)
    matched_rules: List[str] = Field(default_factory=list)
    inspector_used: str
