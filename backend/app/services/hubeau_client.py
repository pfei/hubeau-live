from datetime import datetime, timedelta, timezone

from hubeau_data.async_client import AsyncHubeauClient
from hubeau_data.models.hydrometrie import ObservationTrParams, StationParams

from app.core.database import cache_get, cache_set
from app.models.station import Observation, ObservationSeries, Station


async def get_stations_by_department(department: str) -> list[Station]:
    """Return active hydrometric stations for a given department code (e.g. '33')."""
    cache_key = f"stations:{department}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return [Station(**s) for s in cached]

    async with AsyncHubeauClient() as client:
        result = await client.hydrometrie.get_stations(
            StationParams(code_departement=department, en_service=True, size=1000)
        )

    stations = [
        Station(
            code=s.code_station,
            name=s.libelle_station or s.code_station,
            river=s.libelle_cours_eau or "",
            department=s.code_departement or department,
            latitude=s.latitude_station,
            longitude=s.longitude_station,
        )
        for s in result.data
    ]
    await cache_set(cache_key, [s.model_dump(mode="json") for s in stations])
    return stations


async def get_observations(
    station_code: str, period_hours: int = 24
) -> ObservationSeries:
    """Return discharge/height time series for one station."""
    cache_key = f"obs:{station_code}:{period_hours}h"
    cached = await cache_get(cache_key)
    if cached is not None:
        return ObservationSeries(**cached)

    date_debut = datetime.now(tz=timezone.utc) - timedelta(hours=period_hours)

    async with AsyncHubeauClient() as client:
        stations_result = await client.hydrometrie.get_stations(
            StationParams(code_station=[station_code])
        )
        obs_result = await client.hydrometrie.get_observations_tr(
            ObservationTrParams(
                code_entite=[station_code],
                date_debut_obs=date_debut.strftime("%Y-%m-%dT%H:%M:%SZ"),
                sort="asc",
                size=20000,
            )
        )

    raw = stations_result.data[0] if stations_result.data else None
    station = Station(
        code=station_code,
        name=raw.libelle_station if raw else station_code,
        river=raw.libelle_cours_eau if raw else "",
        department=raw.code_departement if raw else "",
        latitude=raw.latitude_station if raw else None,
        longitude=raw.longitude_station if raw else None,
    )

    # Hub'Eau returns interleaved H and Q rows — merge by timestamp
    merged: dict[str, dict] = {}
    for o in obs_result.data:
        ts = o.date_obs
        if ts not in merged:
            merged[ts] = {"timestamp": ts, "flow_m3s": None, "height_m": None}
        if o.grandeur_hydro == "Q":
            # Hub'Eau returns streamflow in l/s — convert to m3/s
            merged[ts]["flow_m3s"] = (
                o.resultat_obs / 1000 if o.resultat_obs is not None else None
            )
        elif o.grandeur_hydro == "H":
            # Hub'Eau returns height in mm — convert to metres
            merged[ts]["height_m"] = (
                o.resultat_obs / 1000 if o.resultat_obs is not None else None
            )

    series = ObservationSeries(
        station=station,
        observations=[Observation(**v) for v in merged.values()],
        period_hours=period_hours,
    )
    # Short TTL for real-time data — Hub'Eau updates every ~15 min
    await cache_set(cache_key, series.model_dump(mode="json"), ttl=60)
    return series
