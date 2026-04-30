import logging
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI

from app.config import get_settings
from app.db.session import create_engine, create_session_maker
from app.rag.embedder import load_embedding_model
import httpx

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    logger.info("Starting %s", settings.app_name)

    # Shared singletons
    app.state.settings = settings

    # Database singleton
    #app.state.db_engine = create_engine(settings)
    #app.state.session_maker = create_session_maker(app.state.db_engine)

    # ML model singleton
    app.state.model = joblib.load(settings.ml_model_path)
    app.state.feature_columns = joblib.load(settings.feature_columns_path)
    logger.info("ML model loaded from %s", settings.ml_model_path)
    logger.info("Feature columns loaded from %s", settings.feature_columns_path)

    # Embedding model singleton
    app.state.embedder = load_embedding_model(settings.embedding_model)
    logger.info("Embedding model loaded: %s", settings.embedding_model)

    # Other shared singletons - add later
    app.state.http_client = httpx.AsyncClient(
        timeout=settings.webhook_timeout_seconds,
    )
    app.state.llm_client = None

    try:
        yield
    finally:
        app.state.model = None
        app.state.feature_columns = None
        app.state.embedder = None

        await app.state.http_client.aclose()
        await app.state.db_engine.dispose()

        logger.info("Shutting down %s", settings.app_name)