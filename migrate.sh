#!/bin/bash
# ============================================================
#  3D T-Shirt Shop — first-time database migration script
#  Run this once after ./start.sh to set up the database.
# ============================================================

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$ROOT_DIR/backend/shopcore/docker-compose.yml"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── Check Django container is running ─────────────────────────
if ! docker ps --format '{{.Names}}' | grep -q "^django-app$"; then
  error "django-app container is not running. Run ./start.sh first."
fi

# ── Make migrations (detects model changes) ───────────────────
info "Running makemigrations..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py makemigrations

# ── Apply migrations to the database ─────────────────────────
info "Running migrate..."
docker compose -f "$COMPOSE_FILE" exec web python manage.py migrate

# ── Optional: create a superuser ─────────────────────────────
echo ""
read -p "Do you want to create a superuser now? (y/n): " CREATE_SUPER
if [[ "$CREATE_SUPER" =~ ^[Yy]$ ]]; then
  info "Creating superuser..."
  docker compose -f "$COMPOSE_FILE" exec web python manage.py createsuperuser
fi

# ── Done ──────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}✔ Migrations complete!${NC}"
echo ""
echo "  Admin panel  →  http://localhost:8000/admin"
echo "  Auth info    →  http://localhost:8000/api/v1/auth/info"
echo "  Register     →  http://localhost:8000/api/v1/auth/register"
echo "  Login        →  http://localhost:8000/api/v1/auth/login"
