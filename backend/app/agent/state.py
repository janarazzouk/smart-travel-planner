from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    input_text: str
    features: dict[str, Any]
    predicted_style: str | None
    destinations: list[dict[str, Any]]
    selected_destination: dict[str, Any] | None
    weather: dict[str, Any] | None
    tool_logs: list[dict[str, Any]]
    final_answer: str
    errors: list[str]

    model: Any
    feature_columns: list[str]
    embedder: Any
    http_client: Any
    settings: Any