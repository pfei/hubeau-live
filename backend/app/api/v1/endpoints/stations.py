from fastapi import APIRouter, HTTPException, Query

from app.models.station import Station
from app.services.hubeau_client import get_stations_by_department

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/", response_model=list[Station])
async def list_stations(
    department: str = Query(..., pattern=r"^\d{2,3}$"),
):
    """List hydrometric stations for a given French department."""
    try:
        return await get_stations_by_department(department)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Hub'Eau error: {exc}") from exc
