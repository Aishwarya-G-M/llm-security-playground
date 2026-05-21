import os
from groq import Groq
from groq.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv

# loads variables from .env file into the environment
load_dotenv()

# Initialize Groq client using the API key from .env
groq_client = Groq(
    api_key = os.getenv("GROQ_API_KEY"),
)

def call_llm(prompt : str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Sends a prompt to Groq LLM and returns the response text.
        """
        messages: list[ChatCompletionMessageParam] =[
                {
                    "role":"systems",
                    "content": system_prompt
                },
                {
                    "role":"user",
                    "content": prompt
                }
            ]

        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
        )

        return chat_completion.choices[0].message.content