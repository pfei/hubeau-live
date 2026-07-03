# hubeau-live

Real-time French hydrometric data visualisation — built on [hubeau-data](https://github.com/pfei/hubeau-data).

Select a department → select a river station → visualise live discharge and water height.

**Live**: [hubeau-live.pfei.net](https://hubeau-live.pfei.net)

______________________________________________________________________

## Architecture

```
nginx (system, 80/443, Let's Encrypt)
    ├── /*       →  React frontend  (static build, served by nginx)
    └── /api/*   →  FastAPI backend (Docker container, port 8000)
```

## Stack

| Layer | Technology |
|-----------|-------------------------------------------------------------------------|
| Backend | FastAPI, [hubeau-data](https://github.com/pfei/hubeau-data), aiosqlite |
| Frontend | React, TypeScript, Vite, Recharts |
| Cache | SQLite (TTL-based, auto-purge) |
| Infra | Docker, nginx, Let's Encrypt |
| CI | GitHub Actions (ruff, pyright, pytest, build) |
| Host | VPS Debian 13 |

## API

```
GET /api/v1/stations/?department={code}
GET /api/v1/observations/{station_code}?period_hours={1-168}
GET /health
```

Interactive docs: [hubeau-live.pfei.net/docs](https://hubeau-live.pfei.net/docs)

## Local development

```bash
# Clone
git clone git@github.com:pfei/hubeau-live.git
cd hubeau-live

# Backend (dev, port 8001)
cp .env.example .env
docker compose -p hubeau-live-dev up -d --build

# Frontend (dev, port 5173)
cd frontend
npm install
npm run dev -- --host
```

Backend dev API: `http://localhost:8001/docs`
Frontend dev: `http://localhost:5173`

## Production deployment

```bash
# Pull latest
git pull

# Rebuild and restart prod backend
docker compose -f docker-compose.prod.yml -p hubeau-live-prod up -d --build

# Rebuild frontend
npm run build --prefix frontend
```

## Data notes

Hub'Eau API returns raw values:

- Water height (`H`): in mm → converted to metres
- Discharge (`Q`): in l/s → converted to m³/s

Negative height values are normal — they represent stage relative to the station datum.

## Related

- [hubeau-data](https://github.com/pfei/hubeau-data) — typed Python client for Hub'Eau APIs
- [Hub'Eau](https://hubeau.eaufrance.fr) — French water data open API
