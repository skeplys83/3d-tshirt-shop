#!/bin/bash
# ============================================================
#  3D T-Shirt Shop — unified startup script
#  Starts the backend (PostgreSQL + Django) and the frontend
#  (SvelteKit) using their respective docker-compose files.
# ============================================================

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend/shopcore"
FRONTEND_DIR="$ROOT_DIR/frontend/shop-app"
NETWORK_NAME="3d-shop"

# ── Colours ──────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── Pre-flight checks ─────────────────────────────────────────
command -v docker >/dev/null 2>&1 || error "Docker is not installed or not in PATH."
docker info >/dev/null 2>&1      || error "Docker daemon is not running."

# ── Check backend .env ────────────────────────────────────────
ENV_FILE="$BACKEND_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  error "Missing backend .env file at $ENV_FILE"
fi

# Warn if critical env vars are empty
for VAR in SECRET_KEY POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD; do
  VALUE=$(grep -E "^${VAR}=" "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
  if [[ -z "$VALUE" ]]; then
    warn "$VAR is not set in $ENV_FILE — fill it in before starting."
  fi
done

# ── Create shared Docker network ──────────────────────────────
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  info "Creating Docker network '$NETWORK_NAME'..."
  docker network create "$NETWORK_NAME"
else
  info "Docker network '$NETWORK_NAME' already exists."
fi

# ── Start backend (PostgreSQL + Django) ───────────────────────
info "Starting backend (PostgreSQL + Django) ..."
docker compose -f "$BACKEND_DIR/docker-compose.yml" up -d --build

# ── Run Django migrations ─────────────────────────────────────
info "Waiting for the database to be ready..."
sleep 4   # give postgres a moment before migrating

info "Running Django migrations..."
docker compose -f "$BACKEND_DIR/docker-compose.yml" \
  exec -T web python manage.py migrate --noinput \
  || warn "Migrations failed or already up to date — check django-app logs."

# ── Start frontend (SvelteKit) ────────────────────────────────
info "Starting frontend (SvelteKit) ..."
docker compose -f "$FRONTEND_DIR/docker-compose.yml" up -d --build

# ── Done ──────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}✔ All services are up!${NC}"
echo ""
echo "  Frontend  →  http://localhost:3000"
echo "  Backend   →  http://localhost:8000"
echo "  Database  →  localhost:5432"
echo ""
echo "  Logs:   docker compose -f backend/shopcore/docker-compose.yml logs -f"
echo "          docker compose -f frontend/shop-app/docker-compose.yml  logs -f"
echo "  Stop:   ./stop.sh"
