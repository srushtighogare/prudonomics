import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def call_gemini(model_name: str, prompt: str):
    """
    Calls a Gemini model and returns a standardized response dict.
    """
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    usage = response.usage_metadata

    return {
        "text": response.text,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
        "provider": "google",
        "model": model_name
    }