# Référence technique

Ce document rassemble ce qu'il faut savoir pour exploiter, déployer ou faire évoluer OpsDesk : les points d'accès, la configuration, le déploiement avec Quadlet, le développement local et les tests. Pour comprendre les choix qui ont mené à cette architecture, lire [l'architecture](architecture.md) ; pour l'état d'avancement, [STATUS.md](../STATUS.md).

## Les trois services

| Service | Image | Port | Rôle |
| --- | --- | --- | --- |
| `opsdesk-web` | `frontend/Containerfile` (nginx non-root, UID 101) | 8080 | Sert l'interface React et relaie `/api`, `/health` et `/version` vers l'API |
| `opsdesk-api` | `backend/Containerfile` (Python 3.13, UID 10001) | 8000 | API FastAPI : authentification, tickets, statistiques, métriques |
| `opsdesk-db` | `postgres:17-alpine` | 5432 | Stockage des comptes, tickets, commentaires et historique |

Seul le frontend est destiné aux utilisateurs. L'API n'est pas exposée publiquement : nginx bloque `/metrics`, que Prometheus lit directement sur le port 8000.

## Points d'accès pour l'exploitation

| Point | Rôle |
| --- | --- |
| `GET /health/live` (API) | Sonde de vie : le processus répond, sans interroger la base |
| `GET /health/ready` (API, aussi via le frontend) | Sonde de disponibilité : répond 503 tant que PostgreSQL ne répond pas |
| `GET /healthz` (frontend) | Sonde de vie de nginx |
| `GET /metrics` (API uniquement, bloqué par nginx) | Métriques Prometheus : requêtes HTTP par route et statut, latences (histogramme), tickets par statut et priorité, utilisateurs par rôle, connexions, transitions, `opsdesk_database_up` |
| `GET /version` | Version et révision (`APP_VERSION`, `APP_REVISION`, également en étiquettes OCI de l'image) |
| `GET /api/docs` | Documentation interactive de l'API (OpenAPI) |
| Journaux | JSON sur la sortie standard, une ligne par requête (`request_id`, route, statut, durée), prêts pour Loki ou journald |

## Comportements à connaître

- **Configuration par variables d'environnement.** Chaque secret accepte aussi la forme `*_FILE` (`DB_PASSWORD_FILE`, `JWT_SECRET_FILE`, `ADMIN_PASSWORD_FILE`), lue depuis un fichier : c'est la forme attendue des secrets Podman et Kubernetes.
- **L'API attend la base** au démarrage (30 tentatives espacées de 2 secondes), puis crée le schéma et le premier administrateur. L'opération est rejouable sans effet, et un verrou consultatif PostgreSQL évite les conflits quand plusieurs instances démarrent ensemble.
- **L'API ne garde aucun état en mémoire** (sessions par jeton JWT) : plusieurs instances peuvent tourner côte à côte, à condition de partager le même `JWT_SECRET`. Il est obligatoire quand `ENVIRONMENT=production`.
- **Le frontend résout l'adresse de l'API à chaque requête**, toutes les 10 secondes au plus (`resolver` de nginx). Il démarre même si l'API n'est pas encore là, et suit sa nouvelle adresse quand elle est recréée. L'adresse vient de `BACKEND_URL` (par défaut `http://backend:8000`).
- **En-têtes de sécurité** : politique de sécurité du contenu (CSP) stricte, `X-Frame-Options`, `nosniff`. Images non-root, ports non privilégiés.

## Variables d'environnement de l'API

| Variable | Défaut | Rôle |
| --- | --- | --- |
| `DATABASE_URL` | — | URL complète de la base (prioritaire sur les `DB_*`) |
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | `localhost` / `5432` / `opsdesk` / `opsdesk` / — | Connexion à PostgreSQL |
| `JWT_SECRET` | aléatoire en développement | Secret de signature des jetons, 32 caractères au minimum |
| `JWT_EXPIRE_MINUTES` | `720` | Durée d'une session |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | `admin@opsdesk.local` / — | Premier administrateur, créé si aucun n'existe |
| `SEED_DEMO_DATA` | `true` | Données de démonstration si la base est vide |
| `ALLOW_REGISTRATION` | `true` | Inscription libre depuis la page de connexion |
| `ENVIRONMENT` | `development` | `production` rend `JWT_SECRET` obligatoire |
| `LOG_LEVEL` / `LOG_FORMAT` | `INFO` / `json` | Journaux (`json` ou `text`) |
| `DB_POOL_SIZE` | `5` | Taille du pool de connexions |
| `CORS_ORIGINS` | vide | Origines autorisées si le frontend est servi sur un autre domaine |

Le frontend n'a qu'une variable : `BACKEND_URL`.

## Déployer avec Podman et Quadlet

`compose.yaml` sert aux essais locaux. En production, chaque service devient une unité Quadlet (`.container`, `.network`, `.volume`) que systemd démarre et surveille. Les unités elles-mêmes sont à écrire (exercice 06) ; voici les contraintes que l'application impose.

- **Noms sur le réseau.** Quadlet nomme les conteneurs `systemd-<unité>` par défaut. Le frontend cherche l'API sous le nom `backend` : définir `ContainerName=backend` (ou `NetworkAlias=backend`) dans l'unité de l'API, ou adapter `BACKEND_URL`. Même chose pour `DB_HOST` côté API.
- **Ordre de démarrage.** Aucun ordre strict n'est nécessaire : l'API réessaie la base pendant environ une minute, et nginx suit l'API dès qu'elle apparaît. Pour un ordre explicite : `Requires=` et `After=`, et `Notify=healthy` (Podman 5 ou plus) sur les unités qui déclarent un `HealthCmd=`.
- **Sondes de santé.** `podman build` produit par défaut une image au format OCI, qui ignore l'instruction `HEALTHCHECK` des Containerfile. Les déclarer dans les unités, ou construire avec `--format docker` :
  - API : `HealthCmd=python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/ready', timeout=2).status == 200 else 1)"`
  - frontend : `HealthCmd=wget -qO- http://127.0.0.1:8080/healthz`
- **Secrets.** Créer des secrets Podman, puis les monter en fichiers : `Secret=opsdesk-db-password` dans l'unité, et `Environment=DB_PASSWORD_FILE=/run/secrets/opsdesk-db-password`. Même principe pour `JWT_SECRET_FILE` et `ADMIN_PASSWORD_FILE`.
- **Sans root.** Les images tournent avec un utilisateur non privilégié et écoutent sur des ports supérieurs à 1024.
- **Journaux.** Les journaux JSON arrivent dans journald : `journalctl --user -u opsdesk-api`.
- **Mises à jour automatiques.** `AutoUpdate=registry` fonctionne, car les images sont référencées par leur nom complet ; il suffit de les publier sur un registre.

## Lancer les essais locaux

Avec Podman (ou Docker) :

```bash
cp .env.example .env
```

Remplacer les valeurs `change-me` dans `.env`, puis :

```bash
podman compose up -d --build
```

```bash
podman compose ps
```

Les trois services doivent afficher `healthy`. Pour un test de bout en bout de l'API à travers nginx (il utilise les comptes de démonstration) :

```bash
python3 scripts/smoke.py http://127.0.0.1:8080
```

Résultat attendu : une ligne `OK` par contrôle, puis `ALL GOOD`.

## Développer sans conteneur

API, avec SQLite pour aller vite :

```bash
cd backend && python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
```

```bash
DATABASE_URL=sqlite:///./dev.db .venv/bin/uvicorn app.main:app --reload --port 8000
```

Interface (le serveur Vite relaie `/api` vers le port 8000) :

```bash
cd frontend && npm install && npm run dev
```

## Tester

```bash
cd backend && .venv/bin/pytest -q && .venv/bin/ruff check app tests
```

```bash
cd frontend && npm run typecheck && npm run build
```

Les tests de l'API tournent sur SQLite par défaut, et sur un vrai PostgreSQL si `TEST_DATABASE_URL` est défini (par exemple `postgresql://utilisateur:motdepasse@hôte:5432/base_de_test`). C'est le mode à utiliser en CI : certains défauts n'apparaissent que sur PostgreSQL.

## Organisation du dépôt

```text
backend/       API FastAPI (app/), tests (tests/), Containerfile
frontend/      Interface React (src/), configuration nginx, Containerfile
scripts/       smoke.py : test de bout en bout d'un déploiement
compose.yaml   Pile complète pour les essais locaux
docs/          Architecture, référence technique, laboratoire, parcours d'apprentissage
legacy/        Version 1 (Flask), ses preuves et ses schémas, conservés pour référence
```
