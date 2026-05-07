#!/bin/bash
# ============================================================
#  3D T-Shirt Shop — unified stop script
# ============================================================

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend/shopcore"
FRONTEND_DIR="$ROOT_DIR/frontend/shop-app"

GREEN='\033[0;32m'
NC='\033[0m'

echo "Stopping frontend..."
docker compose -f "$FRONTEND_DIR/docker-compose.yml" down

echo "Stopping backend..."
docker compose -f "$BACKEND_DIR/docker-compose.yml" down

echo -e "${GREEN}✔ All services stopped.${NC}"
