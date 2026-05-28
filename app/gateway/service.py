from app.schemas.api import PromptRequest
from app.schemas.gateway import GatewayResponse
from app.schemas.security import SecurityVerdict, PolicyAction
from app.security.inspectors.rule_inspector import RuleInspector
from app.security.llm_client import call_llm


class GatewayInspector:
    def process_input(self, request: PromptRequest) -> SecurityVerdict:
        inspector = RuleInspector()
        return inspector.inspect_input(request.prompt)

    def process_llm_output(self, llm_output: str) -> SecurityVerdict:
        inspector = RuleInspector()
        return inspector.inspect_output(llm_output)

    def process_chat_input(self, prompt_request: PromptRequest) -> GatewayResponse | None:
        input_security_verdict = self.process_input(prompt_request)

        if input_security_verdict.action in {PolicyAction.BLOCK, PolicyAction.REVIEW}:
            return GatewayResponse(
                input_verdict=input_security_verdict,
                output_verdict=None,
                llm_output=None,
            )

        llm_output = call_llm(prompt_request.prompt, prompt_request.system_prompt)
        output_security_verdict = self.process_llm_output(llm_output)

        if output_security_verdict.action == PolicyAction.ALLOW:
            return GatewayResponse(
                input_verdict=input_security_verdict,
                output_verdict=output_security_verdict,
                llm_output=llm_output,
            )

        if output_security_verdict.action in {
            PolicyAction.BLOCK,
            PolicyAction.REVIEW,
            PolicyAction.REDACT,
        }:
            return GatewayResponse(
                input_verdict=input_security_verdict,
                output_verdict=output_security_verdict,
                llm_output="Response withheld by safety policy",
            )

        return GatewayResponse(
            input_verdict=input_security_verdict,
            output_verdict=output_security_verdict,
            llm_output="Response handling fallback triggered",
        )