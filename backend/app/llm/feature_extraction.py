from pydantic import BaseModel, Field
from google.genai import types

from app.config import get_settings
from app.llm.client import get_gemini_client
from app.llm.prompts import build_feature_extraction_prompt


class ExtractedTravelFeatures(BaseModel):
    budget_usd: float | None = Field(default=None)
    trip_days: int | None = Field(default=None)

    tourism_density: int = Field(ge=0, le=5)
    hiking_trails: int = Field(ge=0, le=5)
    water_sports: int = Field(ge=0, le=5)
    beach_quality: int = Field(ge=0, le=5)
    historical_sites: int = Field(ge=0, le=5)
    museums_galleries: int = Field(ge=0, le=5)
    family_friendly_score: int = Field(ge=0, le=5)
    luxury_resorts: int = Field(ge=0, le=5)

    avg_temp_summer_c: float = Field(
        default=25.0,
        description="Estimated preferred summer temperature from user text, not live API.",
    )


def estimate_cost_features(
    budget_usd: float | None,
    trip_days: int | None,
) -> dict[str, float]:
    if not budget_usd or not trip_days or trip_days <= 0:
        daily_budget = 120.0
    else:
        daily_budget = budget_usd / trip_days

    return {
        "avg_daily_cost_usd": round(daily_budget * 0.68, 2),
        "avg_hotel_price_usd": round(daily_budget * 0.32, 2),
    }


async def extract_features_with_gemini(input_text: str) -> dict:
    settings = get_settings()
    client = get_gemini_client()

    response = await client.aio.models.generate_content(
        model=settings.gemini_model_name,
        contents=build_feature_extraction_prompt(input_text),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExtractedTravelFeatures,
            temperature=0,
        ),
    )

    extracted = response.parsed

    cost_features = estimate_cost_features(
        budget_usd=extracted.budget_usd,
        trip_days=extracted.trip_days,
    )

    ml_features = {
        **cost_features,
        "tourism_density": extracted.tourism_density,
        "hiking_trails": extracted.hiking_trails,
        "water_sports": extracted.water_sports,
        "beach_quality": extracted.beach_quality,
        "historical_sites": extracted.historical_sites,
        "museums_galleries": extracted.museums_galleries,
        "family_friendly_score": extracted.family_friendly_score,
        "luxury_resorts": extracted.luxury_resorts,
        "avg_temp_summer_c": extracted.avg_temp_summer_c,
    }

    return {
        "budget_usd": extracted.budget_usd,
        "trip_days": extracted.trip_days,
        "ml_features": ml_features,
    }