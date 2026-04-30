from typing import Any

from app.tools.classify_style import classify_style_tool
from app.tools.destination_search import destination_search_tool
from app.tools.weather import weather_tool


async def run_classify_style_tool(state: dict[str, Any]) -> dict[str, Any]:
    return classify_style_tool(
        arguments=state["features"],
        model=state["model"],
        feature_columns=state["feature_columns"],
    )


async def run_destination_search_tool(state: dict[str, Any]) -> dict[str, Any]:
    return destination_search_tool(
        arguments={"travel_style": state["predicted_style"]},
        embedder=state["embedder"],
        chroma_path=state["settings"].chroma_path,
        collection_name=state["settings"].chroma_collection_name,
        top_k=state["settings"].rag_top_k,
    )


async def run_weather_tool(state: dict[str, Any]) -> dict[str, Any] | None:
    city = state.get("city")

    if not city:
        return None

    return await weather_tool(
        arguments={"city": city},
        http_client=state["http_client"],
        geocoding_url=state["settings"].weather_geocoding_url,
        forecast_url=state["settings"].weather_base_url,
    )