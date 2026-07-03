#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "==> Pulling latest changes..."
git pull --ff-only

echo "==> Rebuilding prod backend..."
docker compose -f docker-compose.prod.yml -p hubeau-live-prod up -d --build

echo "==> Rebuilding frontend..."
NODE_BIN=$(ls -d ~/.nvm/versions/node/*/bin | tail -1)
"$NODE_BIN/npm" run build --prefix frontend

echo "==> Done. https://hubeau-live.pfei.net"
