import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.router import router
from app.core.config import settings
from app.core.database import cache_purge_expired

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"],
)


async def _purge_loop():
    """Delete expired cache entries every 10 minutes."""
    while True:
        await asyncio.sleep(600)
        deleted = await cache_purge_expired()
        if deleted:
            logger.info("Cache purge: %d entries deleted", deleted)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_purge_loop())
    logger.info("hubeau-live started (env=%s)", settings.app_env)
    yield
    task.cancel()


app = FastAPI(title="hubeau-live", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
