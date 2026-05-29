# app/schemas/llm.py

from typing import Optional
from pydantic import BaseModel, Field


class LLMMetadata(BaseModel):
    request_id: Optional[str] = Field(
        default=None,
        description="Provider request or response identifier if available."
    )
    provider: str = Field(
        ...,
        description="LLM provider name, for example 'groq'."
    )
    model: str = Field(
        ...,
        description="Model name used for the request."
    )
    latency_ms: int = Field(
        ...,
        ge=0,
        description="End-to-end provider call latency in milliseconds."
    )


class LLMRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="End-user input prompt."
    )
    system_prompt: str = Field(
        default="You are a helpful assistant.",
        description="System instruction sent to the model."
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Application-generated correlation ID for tracing."
    )


class LLMResponse(BaseModel):
    content: str = Field(
        ...,
        description="Generated text returned by the provider."
    )
    metadata: LLMMetadata
    input_tokens: Optional[int] = Field(
        default=None,
        ge=0,
        description="Number of input/prompt tokens if reported by provider."
    )
    output_tokens: Optional[int] = Field(
        default=None,
        ge=0,
        description="Number of generated/completion tokens if reported by provider."
    )
    total_tokens: Optional[int] = Field(
        default=None,
        ge=0,
        description="Total token count if reported by provider."
    )