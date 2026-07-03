#!/usr/bin/env bash
set -e

uv run ruff check .
uv run pyright backend/app
uv run pytest

NODE_BIN=$(ls -d ~/.nvm/versions/node/*/bin | tail -1)
"$NODE_BIN/npm" run build --prefix frontend
