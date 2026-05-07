#!/bin/bash
# ============================================================
#  3D T-Shirt Shop — superuser management script
#  Create or delete a Django superuser.
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

# ── Menu ──────────────────────────────────────────────────────
echo ""
echo "  Superuser Management"
echo "  ────────────────────"
echo "  1) Create superuser"
echo "  2) Delete superuser"
echo ""
read -p "Choose an option (1/2): " CHOICE

case "$CHOICE" in

  # ── Create ────────────────────────────────────────────────
  1)
    info "Starting superuser creation..."
    echo "  You will be prompted for: Email, First name, Last name, Phone number, Password"
    echo ""
    docker compose -f "$COMPOSE_FILE" exec web python manage.py createsuperuser
    echo ""
    echo -e "${GREEN}✔ Superuser created.${NC}"
    echo "  Admin panel  →  http://localhost:8000/admin"
    ;;

  # ── Delete ────────────────────────────────────────────────
  2)
    info "Existing superusers:"
    docker compose -f "$COMPOSE_FILE" exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
supers = User.objects.filter(is_superuser=True)
if supers.exists():
    for u in supers:
        print(f'  - {u.email}')
else:
    print('  (none)')
"
    echo ""
    read -p "Enter the email address of the superuser to delete: " EMAIL
    if [[ -z "$EMAIL" ]]; then
      error "No email provided."
    fi

    warn "This will permanently delete the superuser with email: $EMAIL"
    read -p "Are you sure? (y/n): " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
      echo "Aborted."
      exit 0
    fi

    info "Deleting superuser '$EMAIL'..."
    docker compose -f "$COMPOSE_FILE" exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.get(email='$EMAIL')
    if not user.is_superuser:
        print('ERROR: $EMAIL is not a superuser.')
        exit(1)
    user.delete()
    print('Deleted.')
except User.DoesNotExist:
    print('ERROR: No user found with email $EMAIL')
    exit(1)
"
    echo -e "${GREEN}✔ Superuser '$EMAIL' deleted.${NC}"
    ;;

  *)
    error "Invalid option. Please enter 1 or 2."
    ;;
esac
