from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.config import get_settings
from app.dependencies import (
    get_embedder,
    get_feature_columns,
    get_http_client,
    get_ml_model,
)
from app.tools.registry import get_tool

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.post("/call")
async def call_tool(
    request: dict[str, Any],
    model: Any = Depends(get_ml_model),
    feature_columns: list[str] = Depends(get_feature_columns),
    embedder: Any = Depends(get_embedder),
    http_client: Any = Depends(get_http_client),
):
    settings = get_settings()

    tool_name = request.get("tool_name")
    arguments = request.get("arguments", {})

    tool = get_tool(tool_name)

    if tool is None:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    try:
        result = tool(
            arguments=arguments,
            model=model,
            feature_columns=feature_columns,
            embedder=embedder,
            http_client=http_client,
            geocoding_url=settings.weather_geocoding_url,
            forecast_url=settings.weather_base_url,
        )

        if hasattr(result, "__await__"):
            result = await result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "tool_name": tool_name,
        "result": result,
    }