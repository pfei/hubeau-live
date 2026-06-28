from fastapi import APIRouter, HTTPException, Path, Query

from app.models.station import ObservationSeries
from app.services.hubeau_client import get_observations

router = APIRouter(prefix="/observations", tags=["observations"])


@router.get("/{station_code}", response_model=ObservationSeries)
async def get_station_observations(
    station_code: str = Path(...),
    period_hours: int = Query(24, ge=1, le=168),
):
    """Return discharge/height time series for one station."""
    try:
        return await get_observations(station_code, period_hours)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Hub'Eau error: {exc}") from exc
