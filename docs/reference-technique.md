# Référence technique

Ce document rassemble ce qu'il faut savoir pour exploiter, déployer ou faire évoluer OpsDesk : les points d'accès, la configuration, le déploiement avec Docker Compose, le développement local et les tests. Pour comprendre les choix qui ont mené à cette architecture, lire [l'architecture](architecture.md) ; pour l'état d'avancement, [STATUS.md](../STATUS.md).

## Les trois services

| Service | Image | Port | Rôle |
| --- | --- | --- | --- |
| `frontend` | `frontend/Dockerfile` (nginx non-root, UID 101) | 8080 | Sert l'interface React et relaie `/api`, `/health` et `/version` vers l'API |
| `backend` | `backend/Dockerfile` (Python 3.13, UID 10001) | 8000 | API FastAPI : authentification, tickets, statistiques, métriques |
| `db` | `postgres:17-alpine` | 5432 | Stockage des comptes, tickets, commentaires et historique |

Les noms sont ceux des services de `compose.yaml` ; Compose nomme les conteneurs `opsdesk-<service>-1`. Seul le frontend est destiné aux utilisateurs. L'API n'est pas exposée publiquement : nginx bloque `/metrics` sur l’entrée utilisateur. Dans la cible initiale, Prometheus lira le port 8000 ; l’exercice 09 prévoit ensuite une entrée privée limitée aux métriques, avec contrôle des sources et fermeture du port direct. Aucun Prometheus n’est encore connecté.

## Points d'accès pour l'exploitation

| Point | Rôle |
| --- | --- |
| `GET /health/live` (API) | Sonde de vie : le processus répond, sans interroger la base |
| `GET /health/ready` (API, aussi via le frontend) | Sonde de disponibilité : répond 503 tant que PostgreSQL ne répond pas |
| `GET /healthz` (frontend) | Sonde de vie de nginx |
| `GET /metrics` (API uniquement, bloqué par nginx) | Métriques Prometheus : requêtes HTTP par route et statut, latences (histogramme), tickets par statut et priorité, utilisateurs par rôle, connexions, transitions, `opsdesk_database_up` |
| `GET /version` | Version et révision (`APP_VERSION`, `APP_REVISION`, également en étiquettes OCI de l'image) |
| `GET /api/docs` | Documentation interactive de l'API (OpenAPI) |
| Journaux | JSON sur la sortie standard, une ligne par requête (`request_id`, route, statut, durée), lisibles par `docker compose logs` |

## Comportements à connaître

- **Configuration par variables d'environnement.** Chaque secret accepte aussi la forme `*_FILE` (`DB_PASSWORD_FILE`, `JWT_SECRET_FILE`, `ADMIN_PASSWORD_FILE`), lue depuis un fichier : c'est la forme attendue des secrets de Compose et de Kubernetes.
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
| `ENVIRONMENT` | `development` | `production` exige JWT (32 caractères au moins), admin et DB (sauf `DATABASE_URL` explicite), distincts et non factices |
| `LOG_LEVEL` / `LOG_FORMAT` | `INFO` / `json` | Journaux (`json` ou `text`) |
| `DB_POOL_SIZE` | `5` | Taille du pool de connexions |
| `CORS_ORIGINS` | vide | Origines autorisées si le frontend est servi sur un autre domaine |

Le frontend n'a qu'une variable : `BACKEND_URL`.

## Déployer avec Docker Compose sur un serveur

`compose.yaml` est la pile de référence livrée avec l'application : il construit les images et prouve qu'une version démarre. Sur `srv-app`, le déploiement utilise un fichier Compose de production, à écrire à l'exercice 06, qui **tire** les images de GHCR par digest au lieu de les construire. Voici ce que l'application et Docker imposent à ce fichier et au serveur.

**Ce que l'application impose**

- **Noms sur le réseau.** Compose inscrit chaque service dans le DNS de son réseau sous son nom. Le frontend cherche l'API sous le nom `backend` (`BACKEND_URL`), et l'API cherche la base sous `DB_HOST` : garder ces noms de service, ou adapter les deux variables.
- **Ordre de démarrage.** `depends_on` avec `condition: service_healthy` fait attendre l'API jusqu'à ce que la base soit prête, et nginx jusqu'à ce que l'API le soit. Sans cet ordre, l'API réessaie la base pendant environ une minute et nginx suit l'API dès qu'elle apparaît : la pile finit par démarrer, mais plus lentement et avec des erreurs dans les journaux.
- **Sondes de santé.** Les deux images portent un `HEALTHCHECK`, que Docker applique. Le redéclarer dans le fichier Compose le rend visible et réglable sans reconstruire l'image. L'API a deux sondes : `/health/live` pour dire si le processus vit, `/health/ready` pour dire s'il peut servir. Une sonde Docker qui viserait `/health/ready` marquerait l'API malade à chaque coupure de la base.
- **Secrets.** Chaque secret de l'API accepte la forme `*_FILE`. Avec un bloc `secrets:` de Compose (`file: /opt/opsdesk/secrets/db_password`), le fichier est monté dans `/run/secrets/<nom>` ; on donne alors `DB_PASSWORD_FILE=/run/secrets/db_password`. Hors de Swarm, ce montage garde le propriétaire et les droits du fichier sur le serveur : il doit rester lisible par l'utilisateur du conteneur (UID 10001 pour l'API). Ce comportement n'a pas encore été vérifié sur `srv-app`.
- **Sans root dans le conteneur.** Les images tournent avec un utilisateur non privilégié (10001 pour l'API, 101 pour nginx) et écoutent sur des ports supérieurs à 1024. `no-new-privileges` empêche un processus d'y regagner des droits ; il a été vérifié le 18 novembre 2026 sur les trois services.

**Ce que Docker impose au serveur**

- **Le démon tourne en root.** Qui peut parler au socket `/var/run/docker.sock` peut lancer un conteneur qui monte `/` : appartenir au groupe `docker` revient à être root. On administre donc par `sudo`, on ne monte jamais ce socket dans un conteneur, et l'API Docker n'écoute pas sur le réseau. Docker sans root (*rootless*) existe ; il est écarté ici, car il complique le réseau, les ports et la supervision ([registre](architecture.md#décisions-retenues)).
- **Pare-feu.** Docker écrit ses propres règles et crée une zone firewalld `docker`, qui accepte le trafic vers ses réseaux. Un port publié peut donc être joignable même s'il n'est pas ouvert dans la zone du serveur. Publier sur une adresse précise (`192.168.150.10:8080:8080`) plutôt que sur toutes, puis prouver l'accès et le refus depuis les autres machines, pas seulement avec `firewall-cmd --list-all`.
- **SELinux.** Le démon n'applique SELinux aux conteneurs que si `"selinux-enabled": true` figure dans `/etc/docker/daemon.json` ; `docker info` doit alors afficher `selinux` dans ses options de sécurité. Un dossier du serveur monté dans un conteneur doit porter le bon contexte : l'option `:Z` le réétiquette pour ce seul conteneur. Un volume nommé n'en a pas besoin.
- **Journaux.** Le pilote par défaut, `json-file`, ne fait tourner ses fichiers que si on le lui demande (`max-size`, `max-file`, dans le fichier Compose ou dans `daemon.json`). Lecture : `docker compose logs backend`. Le pilote `journald` est une autre option : les journaux se lisent alors avec `journalctl CONTAINER_NAME=…`.
- **Démarrage au boot.** systemd démarre le service `docker` s'il est activé (`systemctl enable docker`). Docker relance ensuite les conteneurs dont la politique est `unless-stopped`, sauf ceux arrêtés à la main. Aucune unité systemd propre à OpsDesk n'est nécessaire.
- **Mises à jour.** Aucune mise à jour automatique : on change le digest de l'image dans le fichier, puis `docker compose pull` et `docker compose up -d`. Compose ne recrée que les services dont la définition ou l'image a changé.

## Lancer les essais locaux

Avec Docker Engine et le plugin Compose, depuis la racine du dépôt. Aucun `.env` nécessaire pour la démonstration locale :

```bash
docker compose up -d --build
```

```bash
docker compose ps
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
backend/       API FastAPI (app/), tests (tests/), Dockerfile
frontend/      Interface React (src/), configuration nginx, Dockerfile
scripts/       smoke.py : test de bout en bout d'un déploiement
compose.yaml   Pile de référence : construit les images et démarre la pile
docs/          Architecture, référence technique, laboratoire, parcours d'apprentissage
legacy/        Version 1 (Flask), ses preuves et ses schémas, conservés pour référence
```
