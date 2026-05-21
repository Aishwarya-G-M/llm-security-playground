from fastapi import FastAPI
from pydantic import BaseModel

from app.security.llm_client import call_llm
from app.security.prompt_inspector_adv import inspect_prompt

app = FastAPI(
    title="LLM Security Playground",
    version="0.1.0",
    description="A Playground for testing LLM vulnerabilities"
)

# ---- Request Model ---
class PromptRequest(BaseModel):
    prompt : str

class ChatRequest(BaseModel):
    prompt : str
    system_prompt : str = "You are a helpful assistant"

# --- Routes ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_prompt(request : PromptRequest):
    result = inspect_prompt(request.prompt)
    return result

@app.post("/chat")
async def chat(request: ChatRequest):
    # Step 1:run guardrail before sending it to LLM
    inspection = inspect_prompt(request.prompt)

    if not inspection["is_safe"]:
        return {
            "blocked": True,
            "reason": inspection["reason"],
            "response": None
        }

    # Step 2: Only reaches here is prompt is safe
    llm_response = call_llm(
        prompt=request.prompt,
        system_prompt=request.system_prompt
    )

    return {
        "blocked": False,
        "response": llm_response,
        "reason": None
    }
