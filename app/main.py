from fastapi import FastAPI
from pydantic import BaseModel
from app.security.prompt_inspector import inspect_prompt

llm_security_playground = FastAPI(
    title="LLM Security Playground",
    version="0.1.0",
    description="A Playground for testing LLM vulnerabilities"
)

# ---- Request Model ---
class PromptRequest(BaseModel):
    prompt : str

# --- Routes ---
@llm_security_playground.get("/health")
async def health_check():
    return {"status": "ok"}

@llm_security_playground.post("/analyze")
async def analyze_prompt(request : PromptRequest):
    result = inspect_prompt(request.prompt)
    return result