from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):
    city: str = Field(..., min_length=1)


class WeatherResponse(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature_c: float
    wind_speed_kmh: float | None = None
    weather_code: int | None = None
    source: str = "Open-Meteo"


class WeatherToolOutput(BaseModel):
    city: str
    result: WeatherResponse