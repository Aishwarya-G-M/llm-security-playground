import os

from dotenv import load_dotenv
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam

from app.exceptions.llm_error_exceptions import LLMConfigurationError

load_dotenv()


class GroqLlmClient:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMConfigurationError(
                "GROQ_API_KEY is not configured. Add it to your .env file or environment variables."
            )

        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def generate(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return chat_completion.choices[0].message.content or ""