from pydantic import BaseModel
from typing import Optional

from app.schemas.security import SecurityVerdict


class GatewayRequest(BaseModel):
    user_prompt: str
    system_prompt: Optional[str] = None

class GatewayResponse(BaseModel):
    request_id: str
    blocked: bool
    input_verdict: SecurityVerdict
    output_verdict: Optional[SecurityVerdict] = None
    response: Optional[str] = None