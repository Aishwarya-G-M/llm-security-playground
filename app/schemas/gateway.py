from pydantic import BaseModel
from typing import Optional

from app.schemas.security import SecurityVerdict

class GatewayRequest(BaseModel):
    user_prompt: str
    system_prompt: Optional[str] = None

class GatewayResponse(BaseModel):
    input_verdict: SecurityVerdict
    output_verdict: Optional[SecurityVerdict] = None
    llm_output: Optional[str] = None