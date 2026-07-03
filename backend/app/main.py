import asyncio
import logging
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
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
    if settings.sentry_dsn_backend:
        sentry_sdk.init(
            dsn=settings.sentry_dsn_backend,
            environment=settings.app_env,
            traces_sample_rate=0.2,  # 20% of requests traced
            send_default_pii=False,
            integrations=[
                StarletteIntegration(),
                FastApiIntegration(),
            ],
        )
        logger.info("Sentry enabled (env=%s)", settings.app_env)
    task = asyncio.create_task(_purge_loop())
    logger.info("hubeau-live started (env=%s)", settings.app_env)
    yield
    task.cancel()


app = FastAPI(title="hubeau-live", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter

# slowapi handler enforces 'RateLimitExceeded' instead of 'Exception',
# triggering a strict Pyright mismatch
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]


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
