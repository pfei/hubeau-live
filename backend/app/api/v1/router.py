from fastapi import APIRouter

from app.api.v1.endpoints import observations, stations

router = APIRouter(prefix="/api/v1")
router.include_router(stations.router)
router.include_router(observations.router)
