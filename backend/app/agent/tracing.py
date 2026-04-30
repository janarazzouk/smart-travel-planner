from typing import Any


def build_trace(tool_logs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "tool_name": log["tool_name"],
            "status": log["status"],
            "input": log["tool_input"],
            "output": log["tool_output"],
            "error": log["error_message"],
        }
        for log in tool_logs
    ]