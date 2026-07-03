from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "info"

    # SQLite cache
    cache_ttl_seconds: int = 300  # default TTL: 5 min
    db_path: str = "./data/cache.sqlite"

    # Basic abuse protection
    rate_limit_per_minute: int = 60

    # Comma-separated list of allowed CORS origins
    cors_origins: str = "http://localhost:5173"

    # Sentry — optional, disabled if empty
    sentry_dsn_backend: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()
