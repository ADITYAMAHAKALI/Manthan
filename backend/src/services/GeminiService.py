from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import Any, Generator, Union
import os

load_dotenv()

class GeminiService:
    """
    GeminiService provides a high-level interface to interact with Gemini models
    for text generation, streaming, structured responses, and configuration support.
    """

    def __init__(
        self,
        model_id: str = "gemini-2.0-flash",
        system_instruction: str = "You are a helpful assistant."
    ):
        """
        Initialize the GeminiService with a model ID and system instruction.

        Args:
            model_id (str): The Gemini model to use.
            system_instruction (str): Instruction to steer model behavior globally.
        """
        self.model_id = model_id
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.system_instruction = system_instruction

    def get_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
        top_p: float = 0.95,
        top_k: int = 40
    ) -> str:
        """
        Generate plain text from a prompt using configured model parameters.

        Args:
            prompt (str): Input text prompt.
            temperature (float): Controls randomness.
            max_output_tokens (int): Max tokens to generate.
            top_p (float): Cumulative probability threshold.
            top_k (int): Limits token selection to top-K choices.

        Returns:
            str: Generated response text.
        """
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_p=top_p,
            top_k=top_k,
            system_instruction=self.system_instruction
        )

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[prompt],
            config=config
        )
        return response.text

    def get_stream_generator(self, prompt: str) -> Generator[str, None, None]:
        """
        Get a streaming response generator for live content generation.

        Args:
            prompt (str): Input prompt.

        Returns:
            Generator[str]: Streaming generator yielding text chunks.
        """
        response = self.client.models.generate_content_stream(
            model=self.model_id,
            contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction
            )
        )
        for chunk in response:
            yield chunk.text

    def get_structured_json(
        self,
        prompt: str,
        response_schema: Any
    ) -> Union[str, Any]:
        """
        Get structured JSON response conforming to a given schema.

        Args:
            prompt (str): Input prompt requesting structured data.
            response_schema (Any): A supported type or Pydantic model.

        Returns:
            Union[str, Any]: Parsed structured response or raw JSON string.
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
                "system_instruction": self.system_instruction
            }
        )
        try:
            return response.parsed or response.text
        except Exception:
            return response.text


if __name__ == "__main__":
    # Example usage
    service = GeminiService()

    print("\n--- Text Generation ---")
    print(service.get_text("Explain quantum computing in simple terms."))

    print("\n--- Streaming Output ---")
    for chunk in service.get_stream_generator("Write a haiku about spring"):
        print(chunk, end="", flush=True)

    print("\n\n--- Structured Output ---")
    from pydantic import BaseModel

    class Recipe(BaseModel):
        recipe_name: str
        ingredients: list[str]

    structured_prompt = "List 2 cookie recipes with ingredients in JSON format."
    result = service.get_structured_json(structured_prompt, list[Recipe])
    print(result)
