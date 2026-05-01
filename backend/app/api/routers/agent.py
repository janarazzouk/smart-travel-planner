import logging
from fastapi import APIRouter, Depends

from app.agent.graph import build_agent_graph
from app.config import get_settings
from app.dependencies import (
    get_embedder,
    get_feature_columns,
    get_http_client,
    get_ml_model,
)
from app.schemas.agent import AgentRunRequest, AgentRunResponse, ToolLogResponse
from app.services.webhook import send_discord_webhook

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(
    payload: AgentRunRequest,
    model=Depends(get_ml_model),
    feature_columns=Depends(get_feature_columns),
    embedder=Depends(get_embedder),
    http_client=Depends(get_http_client),
) -> AgentRunResponse:
    settings = get_settings()
    graph = build_agent_graph()

    final_state = await graph.ainvoke(
        {
            "input_text": payload.input_text,
            "model": model,
            "feature_columns": feature_columns,
            "embedder": embedder,
            "http_client": http_client,
            "settings": settings,
        }
    )
    final_answer = final_state["final_answer"]
    discord_message = f"""
    🧳 New Trip Plan

    💬 Trip idea:
    {payload.input_text}

   📍 Travel recommendation:
    {final_answer}
    """.strip()

    try:
        await send_discord_webhook(
            webhook_url=settings.discord_webhook_url,
            content=discord_message[:1900],
        )
    except Exception:
        logger.exception("Webhook failed, but user response will continue.")


    return AgentRunResponse(
        id=0,
        input_text=payload.input_text,
        output_text=final_state["final_answer"],
    )


@router.get("/history", response_model=list[AgentRunResponse])
async def get_agent_history() -> list[AgentRunResponse]:
    return []


@router.get("/runs/{run_id}/tools", response_model=list[ToolLogResponse])
async def get_run_tool_logs(run_id: int) -> list[ToolLogResponse]:
    return []