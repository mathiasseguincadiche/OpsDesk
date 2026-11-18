# OpsDesk - Application de Gestion de ticket IT

OpsDesk est une application web de helpdesk : les collaborateurs déclarent leurs incidents, l'équipe support les prend en charge, les commente et les résout, et un tableau de bord suit l'activité en temps réel.

C'est une application **3 tiers conteneurisée**, prête à être déployée (Podman, Docker, Kubernetes…) :

```
 navigateur ──► frontend (nginx :8080) ──/api──► backend (FastAPI :8000) ──► PostgreSQL :5432
                React + Tailwind                 JWT · métriques Prometheus
```

| Composant | Technologie | Image |
|---|---|---|
| `frontend/` | React 19, TypeScript, Vite, Tailwind CSS 4, Recharts | `nginx-unprivileged`, utilisateur non-root, port 8080 |
| `backend/` | Python 3.13, FastAPI, SQLAlchemy 2, psycopg 3, JWT | `python:3.13-slim`, utilisateur 10001, port 8000 |
| base | PostgreSQL 17 | `postgres:17-alpine` |

## Fonctionnalités

- **Authentification** JWT, trois rôles : *collaborateur* (voit ses propres tickets), *support* (voit et traite tous les tickets), *administrateur* (gère aussi les utilisateurs).
- **Tickets** : priorité (basse → critique), catégorie, recherche plein texte, filtres, tri, pagination.
- **Cycle de vie** contrôlé : `ouvert → en cours → résolu → clôturé`, avec réouverture ; le demandeur confirme ou refuse la résolution.
- **Assignation**, **commentaires** et **historique complet** (qui a changé quoi, et quand).
- **Tableau de bord** : indicateurs, activité sur 14 jours, répartition par statut, priorité et catégorie, charge de l'équipe.
- **Administration** : création de comptes, rôles, désactivation, réinitialisation des mots de passe.
- Thème clair/sombre, interface responsive (mobile → grand écran).

## Démarrage rapide

```bash
cp .env.example .env
```

Modifier les mots de passe et le secret dans `.env` (`openssl rand -base64 48`), puis :

```bash
podman compose up -d --build
```

(ou `docker compose up -d --build`). Ouvrir **http://localhost:8080** et se connecter avec `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

Avec `SEED_DEMO_DATA=true`, 16 tickets et 5 comptes de démonstration sont créés au premier démarrage (mot de passe `Demo1234!`, boutons de connexion rapide sur la page de login) :

| Compte | Rôle |
|---|---|
| `sophie.martin@opsdesk.local`, `karim.benali@opsdesk.local` | Support |
| `julie.durand@opsdesk.local`, `thomas.petit@opsdesk.local`, `lea.moreau@opsdesk.local` | Collaborateur |

Vérifier ensuite le déploiement :

```bash
python3 scripts/smoke.py http://127.0.0.1:8080
```

## Points d'intégration pour l'exploitation

| Point | Rôle |
|---|---|
| `GET /health/live` (backend) | Liveness probe : le processus répond |
| `GET /health/ready` (backend, aussi via le frontend) | Readiness probe : 503 tant que PostgreSQL ne répond pas |
| `GET /healthz` (frontend) | Liveness de nginx |
| `GET /metrics` (backend uniquement, bloqué côté nginx) | Prometheus : requêtes HTTP par route/statut, latences (histogramme), tickets par statut/priorité, utilisateurs par rôle, connexions, transitions, `opsdesk_database_up` |
| `GET /version` | Version et révision (`APP_VERSION`, `APP_REVISION`, aussi en labels OCI de l'image) |
| `GET /api/docs` | Documentation OpenAPI / Swagger interactive |
| Journaux | JSON sur stdout, une ligne par requête (`request_id`, route, statut, durée) : prêt pour Loki / Promtail |

Comportements utiles en production :

- **Configuration 12-factor** : tout passe par des variables d'environnement ; chaque secret accepte aussi la forme `*_FILE` (`DB_PASSWORD_FILE`, `JWT_SECRET_FILE`, `ADMIN_PASSWORD_FILE`) pour les secrets Podman et Kubernetes.
- Le backend **attend la base** au démarrage (30 tentatives), puis crée le schéma et le premier administrateur de façon idempotente. Un **verrou consultatif PostgreSQL** évite les conflits quand plusieurs réplicas démarrent ensemble.
- Le backend est **sans état** (JWT) : il se met à l'échelle horizontalement. Un `JWT_SECRET` commun à tous les réplicas est obligatoire en `ENVIRONMENT=production`.
- Le frontend lit `BACKEND_URL` au démarrage (par défaut `http://backend:8000`), ce qui permet de pointer vers un Service Kubernetes.
- En-têtes de sécurité (CSP stricte, `X-Frame-Options`, `nosniff`), images non-root, healthchecks intégrés aux images.

### Déploiement avec Podman et Quadlet

`compose.yaml` sert au développement. En production sous systemd, chaque service devient une unité Quadlet (`.container`, `.network`, `.volume`). Points à respecter :

- **Noms DNS.** Quadlet nomme les conteneurs `systemd-<unité>` par défaut. Le frontend cherche le backend sous le nom `backend` : définir `ContainerName=backend` (ou `NetworkAlias=backend`) dans l'unité de l'API, ou bien changer `BACKEND_URL` côté frontend. Même chose pour `DB_HOST` côté API.
- **Ordre de démarrage.** Aucun ordre strict n'est nécessaire. L'API réessaie la connexion à PostgreSQL pendant environ 60 s. nginx démarre sans backend et re-résout son adresse toutes les 10 s, donc il suit aussi la nouvelle IP après un redémarrage de l'API. Pour un ordre propre malgré tout : `Requires=`/`After=` et `Notify=healthy` (Podman ≥ 5) sur les unités qui ont un `HealthCmd=`.
- **Healthchecks.** `podman build` (format OCI) ne conserve pas le `HEALTHCHECK` des Containerfile : les déclarer dans les unités, ou construire avec `--format docker`.
  - API : `HealthCmd=python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/ready', timeout=2).status == 200 else 1)"`
  - frontend : `HealthCmd=wget -qO- http://127.0.0.1:8080/healthz`
- **Secrets.** Créer des secrets Podman, puis les monter en fichiers : `Secret=opsdesk-db-password` dans l'unité, et `Environment=DB_PASSWORD_FILE=/run/secrets/opsdesk-db-password`. Faire de même pour `JWT_SECRET_FILE` et `ADMIN_PASSWORD_FILE`.
- **Rootless.** Les images tournent en non-root (UID 10001 pour l'API, 101 pour nginx) et écoutent sur des ports non privilégiés (8000, 8080).
- **Journaux.** Les logs JSON sur stdout arrivent dans journald (`journalctl --user -u opsdesk-api`).
- **Mises à jour.** `AutoUpdate=registry` fonctionne, car les images sont référencées par leur nom complet. Il suffit de les pousser sur un registre.

### Variables d'environnement du backend

| Variable | Défaut | Description |
|---|---|---|
| `DATABASE_URL` | — | URL complète (prioritaire sur les `DB_*`) |
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | `localhost` / `5432` / `opsdesk` / `opsdesk` / — | Connexion PostgreSQL |
| `JWT_SECRET` | aléatoire (dev) | Secret de signature des jetons, 32 caractères minimum |
| `JWT_EXPIRE_MINUTES` | `720` | Durée de session |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | `admin@opsdesk.local` / — | Premier administrateur |
| `SEED_DEMO_DATA` | `true` | Données de démonstration si la base est vide |
| `ALLOW_REGISTRATION` | `true` | Inscription libre depuis la page de connexion |
| `ENVIRONMENT` | `development` | `production` rend `JWT_SECRET` obligatoire |
| `LOG_LEVEL` / `LOG_FORMAT` | `INFO` / `json` | Journaux (`json` ou `text`) |
| `DB_POOL_SIZE` | `5` | Taille du pool de connexions |
| `CORS_ORIGINS` | vide | Origines autorisées si le frontend est servi sur un autre domaine |

## Développement local (sans conteneur)

Backend (SQLite automatique si `DATABASE_URL=sqlite:///./dev.db`) :

```bash
cd backend && python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
```

```bash
DATABASE_URL=sqlite:///./dev.db .venv/bin/uvicorn app.main:app --reload --port 8000
```

Frontend (le serveur Vite redirige `/api` vers le port 8000) :

```bash
cd frontend && npm install && npm run dev
```

Tests et qualité :

```bash
cd backend && .venv/bin/pytest -q && .venv/bin/ruff check app tests
```

```bash
cd frontend && npm run typecheck && npm run build
```

Les tests backend tournent sur SQLite par défaut et sur un vrai PostgreSQL si `TEST_DATABASE_URL=postgresql://user:pass@host:5432/base_de_test` est défini (à utiliser en CI).

## Structure

```
backend/     API FastAPI (app/), tests (tests/), Containerfile
frontend/    Interface React (src/), configuration nginx, Containerfile
scripts/     smoke.py : test HTTP de bout en bout d'un déploiement
compose.yaml Pile complète pour Podman / Docker
docs/        Parcours d'apprentissage InfraOps (rédigé pour la v1)
legacy/      Ancienne version Flask (v1), conservée pour référence
```

## Licence

[MIT](LICENSE)
