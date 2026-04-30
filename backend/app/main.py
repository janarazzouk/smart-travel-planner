from fastapi import FastAPI

from app.api.routers.health import router as health_router
from app.config import get_settings
from app.lifespan import lifespan
from app.utils.logging import setup_logging

from app.api.routers import predict
from app.api.routers import tools
from app.api.routers import rag
from app.api.routers import weather
#from app.api.routers import auth
from app.api.routers import agent

settings = get_settings()

setup_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(predict.router, prefix=settings.api_prefix)
app.include_router(tools.router, prefix=settings.api_prefix)
app.include_router(rag.router, prefix=settings.api_prefix)
app.include_router(weather.router, prefix=settings.api_prefix)
#app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(agent.router, prefix=settings.api_prefix)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_name}