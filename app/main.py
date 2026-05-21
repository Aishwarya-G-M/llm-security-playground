from fastapi import FastAPI

llm_security_playground = FastAPI(
    title="LLM Security Playground",
    version="0.1.0",
    description="A Playground for testing LLM vulnerabilities"
)

@llm_security_playground.get("/")
async def health_check():
    return {"status": "ok"}