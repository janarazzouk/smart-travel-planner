from typing import Any

from google import genai
from google.genai import types

from app.agent.feature_extraction import extract_features_with_gemini
from app.agent.tool_executor import (
    run_classify_style_tool,
    run_destination_search_tool,
    run_weather_tool,
)
from app.config import get_settings


async def extract_inputs_node(state: dict[str, Any]) -> dict[str, Any]:
    extracted = await extract_features_with_gemini(state["input_text"])

    return {
        "input_text": state["input_text"],
        "budget_usd": extracted["budget_usd"],
        "trip_days": extracted["trip_days"],
        "features": extracted["ml_features"],
        "tool_logs": [],
        "errors": [],
    }


async def classify_style_node(state: dict[str, Any]) -> dict[str, Any]:
    result = await run_classify_style_tool(state)
    predicted_style = result["predicted_style"]

    tool_log = {
        "tool_name": "classify_style",
        "tool_input": state["features"],
        "tool_output": result,
        "status": "success",
        "error_message": None,
    }

    return {
        "predicted_style": predicted_style,
        "tool_logs": state["tool_logs"] + [tool_log],
    }


async def destination_search_node(state: dict[str, Any]) -> dict[str, Any]:
    result = await run_destination_search_tool(state)
    destinations = result["destinations"]

    selected_destination =  None

    tool_log = {
        "tool_name": "destination_search",
        "tool_input": {"travel_style": state["predicted_style"]},
        "tool_output": result,
        "status": "success",
        "error_message": None,
    }

    return {
        "destinations": destinations,
        "selected_destination": selected_destination,
        "tool_logs": state["tool_logs"] + [tool_log],
    }


async def weather_node(state: dict[str, Any]) -> dict[str, Any]:
    destinations = state.get("destinations", [])

    if not destinations:
        return {"weather_results": []}

    weather_results = []
    tool_logs = state["tool_logs"]
    errors = state["errors"]

    for destination in destinations[:3]:
        city = destination["destination_name"]

        try:
            result = await run_weather_tool(
                {
                    **state,
                    "city": city,
                }
            )

            weather_results.append(
                {
                    "destination": destination,
                    "weather": result,
                }
            )

            tool_logs = tool_logs + [
                {
                    "tool_name": "weather",
                    "tool_input": {"city": city},
                    "tool_output": result,
                    "status": "success",
                    "error_message": None,
                }
            ]

        except Exception as exc:
            errors = errors + [f"{city}: {str(exc)}"]

            tool_logs = tool_logs + [
                {
                    "tool_name": "weather",
                    "tool_input": {"city": city},
                    "tool_output": None,
                    "status": "error",
                    "error_message": str(exc),
                }
            ]

    return {
        "weather_results": weather_results,
        "weather": weather_results[0] if weather_results else None,
        "tool_logs": tool_logs,
        "errors": errors,
    }


async def final_answer_node(state: dict[str, Any]) -> dict[str, Any]:
    settings = get_settings()
    client = genai.Client(api_key=settings.gemini_api_key)

    prompt = f"""
You are a smart travel planning assistant.

User request:
{state.get("input_text")}

Extracted user info:
- Budget USD: {state.get("budget_usd")}
- Trip days: {state.get("trip_days")}
- ML features: {state.get("features")}

ML predicted travel style:
{state.get("predicted_style")}

Candidate destinations from RAG:
{state.get("destinations")}

Selected destination:
None. You must choose the best destination from the candidates.

Live weather results for candidate destinations:
{state.get("weather_results")}

Errors:
{state.get("errors")}

Write a helpful final travel plan.
Do not just list tool outputs.

Important decision rule:
If the live weather conflicts with the user's preference, explain the conflict and prefer another candidate destination if it is a better match.

Explain:
1. the recommended destination
2. why it matches the user
3. weather situation
4. budget fit
5. other possible options if available

Format the answer as clean plain text.
Do not use Markdown.
Do not use **, #, or bullet symbols.
Keep it clear and not too long.
"""

    response = await client.aio.models.generate_content(
        model=settings.gemini_model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
        ),
    )

    clean_answer = response.text.replace("\n", " ").strip()
    return {"final_answer": clean_answer}