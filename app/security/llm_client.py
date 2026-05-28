import os
from dotenv import load_dotenv
from app.exceptions.llm_error_exceptions import LLMConfigurationError

# loads variables from .env file into the environment
load_dotenv()

# Initialize Groq client using the API key from .env
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise LLMConfigurationError(
            "GROQ_API_KEY is not configured. Add it to your .env file or environment variables."
        )
    return Groq(api_key=api_key)

def call_llm(prompt : str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Sends a prompt to Groq LLM and returns the response text.
        """
        messages: list[ChatCompletionMessageParam] =[
                {
                    "role":"system",
                    "content": system_prompt
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ]

        groq_client = get_groq_client()
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
        )

        return chat_completion.choices[0].message.content