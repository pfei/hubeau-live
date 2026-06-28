"""
SQLite-backed cache layer.

Table: cache (key TEXT PK, value TEXT, expires_at REAL)
Key format: "stations:33", "obs:K123401001:24h"
"""

import asyncio
import json
import time
from pathlib import Path

import aiosqlite

from app.core.config import settings

_db: aiosqlite.Connection | None = None
_lock = asyncio.Lock()


async def get_db() -> aiosqlite.Connection:
    """Return the shared database connection, creating it if needed."""
    global _db
    if _db is None:
        async with _lock:
            if _db is None:
                Path(settings.db_path).parent.mkdir(parents=True, exist_ok=True)
                _db = await aiosqlite.connect(settings.db_path)
                await _db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cache (
                        key        TEXT PRIMARY KEY,
                        value      TEXT NOT NULL,
                        expires_at REAL NOT NULL
                    )
                    """
                )
                await _db.commit()
    return _db


async def cache_get(key: str) -> dict | list | None:
    """Return cached value, or None if missing or expired."""
    db = await get_db()
    async with db.execute(
        "SELECT value, expires_at FROM cache WHERE key = ?", (key,)
    ) as cursor:
        row = await cursor.fetchone()
    if row is None:
        return None
    value, expires_at = row
    if time.time() > expires_at:
        await cache_delete(key)
        return None
    return json.loads(value)


async def cache_set(key: str, value: dict | list, ttl: int | None = None) -> None:
    """Store a value with a TTL in seconds (defaults to settings.cache_ttl_seconds)."""
    ttl = ttl if ttl is not None else settings.cache_ttl_seconds
    expires_at = time.time() + ttl
    db = await get_db()
    await db.execute(
        "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
        (key, json.dumps(value), expires_at),
    )
    await db.commit()


async def cache_delete(key: str) -> None:
    """Delete a single cache entry."""
    db = await get_db()
    await db.execute("DELETE FROM cache WHERE key = ?", (key,))
    await db.commit()


async def cache_purge_expired() -> int:
    """Delete all expired entries. Returns the number of rows deleted."""
    db = await get_db()
    cursor = await db.execute("DELETE FROM cache WHERE expires_at < ?", (time.time(),))
    await db.commit()
    return cursor.rowcount
