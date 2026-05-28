from pydantic import BaseModel

# ---- Request Model ---
class PromptRequest(BaseModel):
    prompt : str
    system_prompt: str = "You are a helpful assistant"

class AttackRunRequest(BaseModel):
    id: str