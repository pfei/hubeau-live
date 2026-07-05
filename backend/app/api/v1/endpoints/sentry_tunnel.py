import httpx
from fastapi import APIRouter, Request, Response

SENTRY_HOST = "o4508966689308672.ingest.de.sentry.io"
SENTRY_PROJECT_ID = "4511671367565392"

router = APIRouter()


@router.post("/sentry-tunnel")
async def sentry_tunnel(request: Request) -> Response:
    """Proxy Sentry events to bypass adblockers."""
    body = await request.body()
    # First line of envelope is the header JSON
    envelope_header = body.split(b"\n")[0]

    import json

    header = json.loads(envelope_header)
    dsn = header.get("dsn", "")
    if SENTRY_PROJECT_ID not in dsn:
        return Response(status_code=403)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://{SENTRY_HOST}/api/{SENTRY_PROJECT_ID}/envelope/",
            content=body,
            headers={"Content-Type": "application/x-sentry-envelope"},
        )
    return Response(status_code=resp.status_code)
