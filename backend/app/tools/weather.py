from typing import Any

import httpx
from pydantic import BaseModel, Field

from app.schemas.weather import WeatherResponse
from app.services.weather import get_weather_for_city


TOOL_NAME = "weather"


class WeatherToolInput(BaseModel):
    city: str = Field(..., min_length=1)


def validate_weather_arguments(arguments: dict[str, Any]) -> WeatherToolInput:
    return WeatherToolInput(**arguments)


async def weather_tool(
    arguments: dict[str, Any],
    http_client: httpx.AsyncClient,
    geocoding_url: str,
    forecast_url: str,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = validate_weather_arguments(arguments)

    weather = await get_weather_for_city(
        city=payload.city,
        http_client=http_client,
        geocoding_url=geocoding_url,
        forecast_url=forecast_url,
    )

    return {
        "city": payload.city,
        "result": weather.model_dump(),
    }