from typing import Any

from app.agent.constants import DEFAULT_FEATURES
from app.agent.tool_executor import (
    run_classify_style_tool,
    run_destination_search_tool,
    run_weather_tool,
)


def extract_inputs_node(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "features": DEFAULT_FEATURES,
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

    selected_destination = destinations[0] if destinations else None

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
    selected_destination = state.get("selected_destination")

    if not selected_destination:
        return {"weather": None}

    city = selected_destination["destination_name"]

    try:
        result = await run_weather_tool(
            {
                **state,
                "city": city,
            }
        )

        tool_log = {
            "tool_name": "weather",
            "tool_input": {"city": city},
            "tool_output": result,
            "status": "success",
            "error_message": None,
        }

        return {
            "weather": result,
            "tool_logs": state["tool_logs"] + [tool_log],
        }

    except Exception as exc:
        tool_log = {
            "tool_name": "weather",
            "tool_input": {"city": city},
            "tool_output": None,
            "status": "error",
            "error_message": str(exc),
        }

        return {
            "weather": None,
            "tool_logs": state["tool_logs"] + [tool_log],
            "errors": state["errors"] + [str(exc)],
        }


def final_answer_node(state: dict[str, Any]) -> dict[str, Any]:
    predicted_style = state.get("predicted_style")
    selected_destination = state.get("selected_destination")
    destinations = state.get("destinations", [])

    if selected_destination:
        main_destination = (
            f"{selected_destination['destination_name']}, "
            f"{selected_destination['country']}"
        )
    else:
        main_destination = "no destination found"

    other_options = ", ".join(
        f"{item['destination_name']} ({item['country']})"
        for item in destinations[1:]
    )

    answer = (
        f"Based on your preferences, your predicted travel style is {predicted_style}. "
        f"I recommend {main_destination}."
    )

    if other_options:
        answer += f" Other good options are: {other_options}."

    weather = state.get("weather")

    if weather:
        weather_result = weather["result"]
        answer += (
            f" Current weather in {weather_result['city']} is "
            f"{weather_result['temperature_c']}°C with wind speed "
            f"{weather_result.get('wind_speed_kmh')} km/h."
        )

    return {"final_answer": answer}