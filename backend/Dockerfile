FROM python:3.13-slim AS deps
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

FROM python:3.13-slim AS runtime
WORKDIR /app
RUN useradd --create-home appuser
COPY --from=deps /usr/local/lib /usr/local/lib
COPY ./app ./app
RUN mkdir -p /app/data && chown appuser:appuser /app/data
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
