from fastapi import APIRouter, Depends, HTTPException, Query, status
from httpx import AsyncClient

from app.config import get_settings
from app.dependencies import get_http_client
from app.schemas.weather import WeatherResponse
from app.services.weather import get_weather_for_city

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", response_model=WeatherResponse)
async def get_weather(
    city: str = Query(..., min_length=1),
    http_client: AsyncClient = Depends(get_http_client),
) -> WeatherResponse:
    settings = get_settings()

    try:
        return await get_weather_for_city(
            city=city,
            http_client=http_client,
            geocoding_url=settings.weather_geocoding_url,
            forecast_url=settings.weather_base_url,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weather service is temporarily unavailable.",
        ) from exc