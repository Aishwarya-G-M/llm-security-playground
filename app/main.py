from pydantic import BaseModel

from app.security.llm_client import call_llm
from app.security.prompt_inspector_adv import inspect_prompt
from app.security.logger import log_request, get_logs
from fastapi import FastAPI, HTTPException
from app.security.attack_catalog import ATTACK_PROMPTS
from app.exceptions.llm_error_exceptions import LLMConfigurationError

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

class AttackRunRequest(BaseModel):
    id: str

# --- Routes ---
@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_prompt(request : PromptRequest):
    result = inspect_prompt(request.prompt)
    log_request(
        endpoint="/analyze",
        prompt=request.prompt,
        is_safe=result["is_safe"],
        reason=result["reason"]
    )
    return result

@app.post("/chat")
async def chat(request: ChatRequest):
    # Step 1:run guardrail before sending it to LLM
    inspection = inspect_prompt(request.prompt)

    if not inspection["is_safe"]:
        log_request(
            endpoint="/chat",
            prompt=request.prompt,
            is_safe=False,
            reason=inspection["reason"]
        )
        return {
            "blocked": True,
            "reason": inspection["reason"],
            "response": None
        }

    # Step 2: Only reaches here is prompt is safe
    try:
        llm_response = call_llm(
            prompt=request.prompt,
            system_prompt=request.system_prompt
        )
    except LLMConfigurationError as e:
        raise HTTPException(status_code=503, detail=str(e))

    log_request(
        endpoint="/chat",
        prompt=request.prompt,
        is_safe=True,
        reason=inspection["reason"],
        response=llm_response
    )

    return {
        "blocked": False,
        "response": llm_response,
        "reason": None
    }
@app.get("/logs")
async def fetch_logs():
    return {"logs": get_logs(), "total": len(get_logs())}


@app.get("/attacks")
async def get_attacks(category: str = None, context: str = None, severity: str = None):
    """
    Returns the curated attack prompt library.
    Optional filters: category, context
    """
    results = ATTACK_PROMPTS

    if category:
        results = [a for a in results if a.get("category").lower() == category.lower()]
    if context:
        results = [a for a in results if a.get("context").lower() == context.lower()]
    if severity:
        results = [a for a in results if a.get("severity", "").lower() == severity.lower()]

    return {"attacks": results, "total": len(results)}

@app.get("/attacks/{attack_id}")
async def get_attack_by_id(attack_id: str):
    attack = next(
        (item for item in ATTACK_PROMPTS if item.get("id", "").lower() == attack_id.lower()),
        None
    )
    if not attack:
        raise HTTPException(status_code=404, detail="Attack scenario not found")
    return attack

@app.post("/attacks/run")
async def run_attack(request: AttackRunRequest):
    attack = next((item for item in ATTACK_PROMPTS if item.get("id") == request.id), None)

    if not attack:
        raise HTTPException(status_code=404, detail="Attack scenario not found")

    inspection = inspect_prompt(attack["prompt"])

    if not inspection["is_safe"]:
        log_request(
            endpoint="/attacks/run",
            prompt=attack["prompt"],
            is_safe=False,
            reason=inspection["reason"]
        )
        return {
            "id": attack["id"],
            "category": attack["category"],
            "context": attack.get("context"),
            "severity": attack.get("severity"),
            "owasp_ref": attack.get("owasp_ref"),
            "blocked": True,
            "reason": inspection["reason"],
            "response": None
        }

    try:
        llm_response = call_llm(
            prompt=attack["prompt"]
        )
    except LLMConfigurationError as e:
        raise HTTPException(status_code=503, detail=str(e))

    log_request(
        endpoint="/attacks/run",
        prompt=attack["prompt"],
        is_safe=True,
        reason=inspection["reason"],
        response=llm_response
    )

    return {
        "id": attack["id"],
        "category": attack["category"],
        "context": attack.get("context"),
        "severity": attack.get("severity"),
        "owasp_ref": attack.get("owasp_ref"),
        "blocked": False,
        "reason": inspection["reason"],
        "response": llm_response
    }
