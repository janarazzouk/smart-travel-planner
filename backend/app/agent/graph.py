from langgraph.graph import END, StateGraph

from app.agent.nodes import (
    classify_style_node,
    destination_search_node,
    extract_inputs_node,
    final_answer_node,
    weather_node,
)
from app.agent.state import AgentState


def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("extract_inputs", extract_inputs_node)
    graph.add_node("classify_style", classify_style_node)
    graph.add_node("destination_search", destination_search_node)
    graph.add_node("weather", weather_node)
    graph.add_node("final_answer", final_answer_node)

    graph.set_entry_point("extract_inputs")

    graph.add_edge("extract_inputs", "classify_style")
    graph.add_edge("classify_style", "destination_search")
    graph.add_edge("destination_search", "weather")
    graph.add_edge("weather", "final_answer")
    graph.add_edge("final_answer", END)

    return graph.compile()