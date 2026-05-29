from fastapi.testclient import TestClient

from app.main import app, get_gateway_inspector
from app.exceptions.llm_error_exceptions import (
    LLMConfigurationError,
    LLMProviderError,
    LLMTimeoutError,
)
from app.schemas.gateway import GatewayResponse
from app.schemas.security import PolicyAction, SecurityVerdict

client = TestClient(app)


class TimeoutGateway:
    def process_chat_input(self, request):
        raise LLMTimeoutError("LLM provider request timed out.")


class ProviderErrorGateway:
    def process_chat_input(self, request):
        raise LLMProviderError("Failed to connect to the LLM provider.")


class ConfigErrorGateway:
    def process_chat_input(self, request):
        raise LLMConfigurationError("GROQ_API_KEY is not configured.")


class SuccessGateway:
    def process_chat_input(self, request):
        verdict = SecurityVerdict(
            allowed=True,
            action=PolicyAction.ALLOW,
            risk_score=0,
            reasons=[],
            matched_rules=[],
            inspector_used="test-inspector",
        )
        return GatewayResponse(
            input_verdict=verdict,
            output_verdict=verdict,
            llm_output="safe model response",
        )


class TestChatEndpoint:
    def teardown_method(self):
        app.dependency_overrides = {}

    def test_chat_returns_504_on_llm_timeout(self):
        app.dependency_overrides[get_gateway_inspector] = lambda: TimeoutGateway()

        response = client.post(
            "/chat",
            json={
                "prompt": "hello",
                "system_prompt": "You are a helpful assistant.",
            },
        )

        assert response.status_code == 504
        assert response.json()["detail"] == "LLM provider request timed out."

    def test_chat_returns_502_on_provider_error(self):
        app.dependency_overrides[get_gateway_inspector] = lambda: ProviderErrorGateway()

        response = client.post(
            "/chat",
            json={
                "prompt": "hello",
                "system_prompt": "You are a helpful assistant.",
            },
        )

        assert response.status_code == 502
        assert response.json()["detail"] == "Failed to connect to the LLM provider."

    def test_chat_returns_503_on_configuration_error(self):
        app.dependency_overrides[get_gateway_inspector] = lambda: ConfigErrorGateway()

        response = client.post(
            "/chat",
            json={
                "prompt": "hello",
                "system_prompt": "You are a helpful assistant.",
            },
        )

        assert response.status_code == 503
        assert response.json()["detail"] == "GROQ_API_KEY is not configured."

    def test_chat_returns_200_on_success(self):
        app.dependency_overrides[get_gateway_inspector] = lambda: SuccessGateway()

        response = client.post(
            "/chat",
            json={
                "prompt": "hello",
                "system_prompt": "You are a helpful assistant.",
            },
        )

        assert response.status_code == 200
        assert response.json()["llm_output"] == "safe model response"