#!/usr/bin/env bash
# Vérifier que l'image Docker sait migrer et démarrer en production sur une base jetable.
# DANGER : ce test utilise EXCLUSIVEMENT la pile Compose de CI et une base vide dédiée.
set -euo pipefail

compose=(docker compose)
name="opsdesk_prod_ci"
# Les valeurs sont volontairement publiques, fictives et réservées au runner.
url="postgresql+psycopg://opsdesk:change-me-db-password@db:5432/${name}"
secrets=(
  -e JWT_SECRET="ci-jwt-secret-unique-for-production-guard-20261122"
  -e ADMIN_PASSWORD="ci-admin-password-not-for-production"
  -e ENVIRONMENT=production
  -e SEED_DEMO_DATA=false
  -e ALLOW_REGISTRATION=false
  -e DATABASE_URL="$url"
)
trap '"${compose[@]}" exec -T db dropdb -U opsdesk --if-exists "$name" || true' EXIT

# Les deux fichiers doivent être réellement copiés dans l'image non-root.
"${compose[@]}" run --rm -T --no-deps --entrypoint sh backend \
  -c 'test -f /app/alembic.ini && test -f /app/migrations/env.py && test -f /app/migrations/versions/opsdesk_20261122_02_auth_throttle.py'

"${compose[@]}" exec -T db createdb -U opsdesk "$name"

# Refus attendu : aucune table Alembic avant migration.
if "${compose[@]}" run --rm -T --no-deps "${secrets[@]}" backend \
  python -c 'from app.bootstrap import init_database; init_database()'; then
  echo "ERREUR : production démarrée sans migrations Alembic." >&2
  exit 1
fi

# Migrer une base vierge sans privilèges root dans le conteneur applicatif.
"${compose[@]}" run --rm -T --no-deps -e DATABASE_URL="$url" -e ENVIRONMENT=development \
  backend python -m alembic upgrade head
"${compose[@]}" run --rm -T --no-deps -e DATABASE_URL="$url" -e ENVIRONMENT=development \
  backend python -m alembic check

# La production démarre alors uniquement sur le schéma attendu.
"${compose[@]}" run --rm -T --no-deps "${secrets[@]}" backend \
  python -c 'from app.bootstrap import init_database; init_database()'

users="$("${compose[@]}" exec -T db psql -U opsdesk -d "$name" -Atqc "SELECT count(*) FROM users WHERE role = 'admin'")"
version="$("${compose[@]}" exec -T db psql -U opsdesk -d "$name" -Atqc "SELECT version_num FROM alembic_version")"
if [[ "$users" != "1" || "$version" != "opsdesk_20261122_02" ]]; then
  echo "Schéma ou administrateur inattendu : admin=$users revision=$version" >&2
  exit 1
fi
echo "PASS : production refusée sans Alembic, deux migrations contrôlées, admin créé."
