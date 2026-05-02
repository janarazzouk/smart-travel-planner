from google.genai import types

from app.config import get_settings
from app.llm.client import get_gemini_client
from app.llm.prompts import build_final_answer_prompt


async def generate_final_answer(state: dict) -> str:
    settings = get_settings()
    client = get_gemini_client()

    response = await client.aio.models.generate_content(
        model=settings.gemini_model_name,
        contents=build_final_answer_prompt(state),
        config=types.GenerateContentConfig(
            temperature=0.4,
        ),
    )

    return response.text.replace("\n", " ").strip()