from typing import Any

from app.llm.feature_extraction import extract_features_with_gemini
from app.llm.final_answer import generate_final_answer

from app.agent.tool_executor import (
    run_classify_style_tool,
    run_destination_search_tool,
    run_weather_tool,
)


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

    tool_log = {
        "tool_name": "destination_search",
        "tool_input": {"travel_style": state["predicted_style"]},
        "tool_output": result,
        "status": "success",
        "error_message": None,
    }

    return {
        "destinations": destinations,
        "selected_destination": None,
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
    final_answer = await generate_final_answer(state)

    return {
        "final_answer": final_answer,
    }