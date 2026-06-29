# ── Stage 1: install dependencies ─────────────────────────────────────────
FROM python:3.13-slim AS deps
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# uv works directly on the system Python (no .venv)
ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ── Stage 2: runtime ───────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime
WORKDIR /app

RUN useradd --create-home appuser

# Copy installed packages and executables (uvicorn, etc.) from deps stage
COPY --from=deps /usr/local/lib /usr/local/lib
COPY --from=deps /usr/local/bin /usr/local/bin

COPY ./backend/app ./app

RUN mkdir -p /app/data && chown appuser:appuser /app/data

USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
