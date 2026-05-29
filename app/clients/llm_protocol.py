from typing import Protocol
from app.schemas.llm import LLMRequest, LLMResponse


class LlmClientProtocol(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        ...