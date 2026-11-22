#!/usr/bin/env bash
# Vérifier la sauvegarde, la restauration isolée et la reprise du socle de démonstration.
# ATTENTION : ce script est réservé à la pile Compose de CI, jamais à une base réelle.
set -euo pipefail

compose=(docker compose)
pg=(docker compose exec -T db)
restore_db="opsdesk_reprise_ci"
dump="$(mktemp)"
trap 'rm -f "$dump"' EXIT

# Le smoke test précédent doit avoir produit au moins un ticket de plus que le seed.
initial="$("${pg[@]}" psql -U opsdesk -d opsdesk -Atqc 'SELECT COUNT(*) FROM tickets;')"
if ! [[ "$initial" =~ ^[0-9]+$ ]] || (( initial < 17 )); then
  echo "Impossible de prouver la sauvegarde : nombre de tickets inattendu ($initial)" >&2
  exit 1
fi

# L'archive custom reste sur le runner éphémère ; aucun secret ni ticket réel.
"${pg[@]}" pg_dump -U opsdesk -d opsdesk --format=custom > "$dump"
test -s "$dump"

# Restaurer dans une AUTRE base et vérifier l'identité des données.
"${pg[@]}" createdb -U opsdesk "$restore_db"
"${pg[@]}" pg_restore -U opsdesk -d "$restore_db" --no-owner --no-privileges --exit-on-error < "$dump"
restored="$("${pg[@]}" psql -U opsdesk -d "$restore_db" -Atqc 'SELECT COUNT(*) FROM tickets;')"
smoke="$("${pg[@]}" psql -U opsdesk -d "$restore_db" -Atqc "SELECT COUNT(*) FROM tickets WHERE title = 'Smoke test — accents éàü';")"
if [[ "$initial" != "$restored" || "$smoke" != "1" ]]; then
  echo "Restauration incohérente : initial=$initial restauré=$restored ticket-test=$smoke" >&2
  exit 1
fi
"${pg[@]}" dropdb -U opsdesk "$restore_db"

# La recréation du processus API doit préserver les données du volume PostgreSQL.
"${compose[@]}" restart backend
ready=0
for _ in $(seq 1 45); do
  if curl --fail --silent --show-error http://127.0.0.1:8080/health/ready >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
if (( ready != 1 )); then
  echo "L'API ne redevient pas prête après son redémarrage." >&2
  exit 1
fi
after="$("${pg[@]}" psql -U opsdesk -d opsdesk -Atqc 'SELECT COUNT(*) FROM tickets;')"
if [[ "$after" != "$initial" ]]; then
  echo "Perte de tickets après redémarrage : avant=$initial après=$after" >&2
  exit 1
fi

echo "PASS : $initial tickets sauvegardés et restaurés isolément, API rétablie sans perte."
