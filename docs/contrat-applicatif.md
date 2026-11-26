# Contrat de passation applicative — OpsDesk

Ce document dit ce que l'application **exige** et ce qu'elle **garantit**, pour quiconque doit l'héberger, l'exploiter ou la faire évoluer. Il ne choisit pas l'infrastructure : les choix retenus sont dans le [registre des décisions](architecture.md#décisions-retenues), et le détail des réglages dans la [référence technique](reference-technique.md).

Version décrite : **OpsDesk 2.0.0**. Mise à jour : 18 novembre 2026, par relecture du code de `backend/`, `frontend/` et de `compose.yaml`. L'état de chaque vérification est tenu dans [STATUS.md](../STATUS.md).

## 1. Présentation

OpsDesk est une application de tickets de support informatique. Des collaborateurs signalent un problème, le support le prend en charge et le résout, l'administration gère les comptes. Elle sert de support à un projet DevOps : son exploitation compte autant que ses fonctions.

## 2. Utilisateurs et scénarios métier

| Rôle | Valeur technique | Scénarios |
| --- | --- | --- |
| Collaborateur | `user` | Créer un ticket, suivre ses propres tickets, commenter, accepter ou refuser une résolution |
| Support | `agent` | Voir tous les tickets, prendre en charge, assigner, changer le statut, commenter |
| Administrateur | `admin` | Tout ce que fait le support, plus créer, modifier et désactiver des comptes, supprimer un ticket |

Scénario de référence : un collaborateur crée un ticket, un agent le prend en charge puis le résout, le collaborateur accepte la résolution et le ticket est clôturé.

## 3. Fonctionnalités disponibles

- Connexion par e-mail et mot de passe ; inscription libre si `ALLOW_REGISTRATION=true` ; changement de mot de passe.
- Tickets : création, liste paginée et filtrée, fiche détaillée, modification, assignation, commentaires, historique des changements.
- Cycle de vie : `open` → `in_progress` → `resolved` → `closed`, avec retours possibles (`resolved` → `in_progress`, `closed` → `open`) ; les sauts interdits sont refusés.
- Tableau de bord : statistiques par statut, priorité et catégorie.
- Gestion des comptes par l'administrateur.
- Interface web en clair et en sombre, utilisable sur mobile.

### Référence de l'API locale fournie

Toutes les routes métier sont sous `/api` et attendent un jeton (`Authorization: Bearer …`), sauf la connexion, l'inscription et `/api/auth/config`. La documentation interactive est servie sur `/api/docs`.

| Méthode et route | Rôle minimal | Effet |
| --- | --- | --- |
| `POST /api/auth/login` | aucun | Renvoie un jeton et le compte |
| `POST /api/auth/register` | aucun | Crée un compte `user` (si l'inscription est ouverte) |
| `GET /api/auth/me` ; `PUT /api/auth/me/password` | connecté | Profil ; changement de mot de passe |
| `GET /api/auth/config` | aucun | Réglages publics (inscription ouverte ou non) |
| `GET /api/tickets` ; `POST /api/tickets` | connecté | Liste (ses tickets pour un `user`, tous pour le support) ; création |
| `GET`, `PATCH /api/tickets/{id}` | connecté | Fiche ; modification (l'assignation est réservée au support) |
| `POST /api/tickets/{id}/status` | connecté | Changement de statut, selon le cycle de vie et le rôle |
| `POST /api/tickets/{id}/comments` | connecté | Ajout d'un commentaire |
| `DELETE /api/tickets/{id}` | `admin` | Suppression |
| `GET /api/stats` | connecté | Statistiques du tableau de bord |
| `GET /api/users/agents` | `agent` | Liste des membres du support |
| `GET`, `POST /api/users` ; `PATCH /api/users/{id}` | `admin` | Gestion des comptes |

Codes d'erreur : `401` sans jeton valide, `403` rôle insuffisant ou ticket non modifiable, `404` absent ou non visible, `409` transition interdite ou adresse déjà utilisée, `422` données invalides, `503` base indisponible. Les erreurs sont en JSON, avec un champ `detail` en français.

## 4. Architecture interne

Trois composants, chacun dans son conteneur ([schéma](diagrams/architecture-globale.png)) :

- **`frontend`** : nginx non-root qui sert l'interface React et relaie `/api`, `/health` et `/version` vers l'API. Il résout le nom de l'API dynamiquement (cache de 10 secondes) et bloque `/metrics`.
- **`backend`** : FastAPI. Authentification, règles métier, accès à la base, sondes, métriques, journaux. Aucun état en mémoire entre deux requêtes.
- **`db`** : PostgreSQL. Seule source de vérité des données.

## 5. Langages et frameworks

API en Python 3.13 avec FastAPI, SQLAlchemy 2 et psycopg 3. Interface en TypeScript avec React 19, React Router, Tailwind CSS 4 et Recharts, construite par Vite.

## 6. Dépendances

| Partie | Dépendances directes (versions figées) |
| --- | --- |
| API (`backend/requirements.txt`) | fastapi 0.163.2, uvicorn 0.54.0, sqlalchemy 2.1.9, psycopg 3.3.9, pydantic 2.14.3, pydantic-settings 2.16.3, PyJWT 2.15.1, prometheus-client 0.26.0 |
| Interface (`frontend/package.json`) | react 19.3.1, react-router-dom 7.18.5, recharts 3.11.0, tailwindcss 4.3.5, typescript 5.9.3, vite 8.3.8 |

## 7. Versions compatibles

| Élément | Version de référence | Remarque |
| --- | --- | --- |
| Python (image de l'API) | 3.13 | `python:3.13-slim` |
| Node (construction de l'interface) | 22 | Seulement à la construction |
| nginx (image de l'interface) | 1.29 | `nginxinc/nginx-unprivileged:1.29-alpine` |
| PostgreSQL | 17 | Testé sur PostgreSQL 17 ; SQLite seulement pour le développement et les tests |
| Moteur de conteneurs | Docker Engine avec le plugin Compose ; Docker 29.8 et Compose 5.5.1 utilisés pour les essais du 17 et du 18 novembre 2026 | Images au format OCI, donc utilisables aussi par K3s (containerd) |

## 8. Démarrage en développement

Pile complète, en conteneurs, depuis la racine du dépôt. Aucun `.env` nécessaire pour la démonstration locale :

```bash
docker compose up -d --build
```

Sans conteneur, API sur SQLite et interface avec Vite : voir la section [Développer sans conteneur](reference-technique.md#développer-sans-conteneur) de la référence technique.

## 9. Ports et protocoles

| Composant | Port | Protocole | Exposition attendue |
| --- | --- | --- | --- |
| `frontend` | 8080 | HTTP | Seule porte destinée aux utilisateurs |
| `backend` | 8000 | HTTP | Pile locale : boucle locale uniquement ; cible serveur initiale : supervision autorisée, puis restriction aux métriques à mettre en œuvre |
| `db` | 5432 | PostgreSQL | Jamais publié |

Aucun port privilégié ; aucun TLS dans l'application : HTTPS, s'il est voulu, se termine devant elle.

## 10. Paramètres de configuration

Toute la configuration passe par des variables d'environnement ; aucun fichier de configuration n'est lu au démarrage. Chaque secret accepte aussi une forme `*_FILE` qui lit sa valeur dans un fichier : c'est la forme attendue des secrets de Compose et de Kubernetes.

## 11. Variables d'environnement

| Variable | Défaut | Rôle |
| --- | --- | --- |
| `DATABASE_URL` | — | URL complète de la base, prioritaire sur `DB_*` |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` (`_FILE`) | `localhost`, `5432`, `opsdesk`, `opsdesk`, — | Connexion à PostgreSQL |
| `DB_POOL_SIZE` | `5` | Connexions gardées ouvertes |
| `JWT_SECRET` (`_FILE`) | aléatoire en développement | Signature des jetons, 32 caractères au moins ; obligatoire en production |
| `JWT_EXPIRE_MINUTES` | `720` | Durée d'une session |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` (`_FILE`) | `admin@opsdesk.local`, — | Premier administrateur, créé s'il n'en existe aucun |
| `ALLOW_REGISTRATION` | `true` | Inscription libre |
| `SEED_DEMO_DATA` | `true` | Données fictives si la base est vide ; **doit être `false` en production, sinon démarrage refusé** |
| `ENVIRONMENT` | `development` | `production` exige JWT (32 caractères au moins), admin et DB (sauf `DATABASE_URL` explicite), distincts et non factices |
| `LOG_LEVEL`, `LOG_FORMAT` | `INFO`, `json` | Journaux |
| `CORS_ORIGINS` | vide | Origines autorisées si l'interface est servie ailleurs |
| `APP_VERSION`, `APP_REVISION` | `2.0.0`, `dev` | Identité affichée par `/version` et les sondes |
| `BACKEND_URL` (interface) | `http://backend:8000` | Adresse de l'API vue depuis nginx |

## 12. Besoins de stockage

Un seul stockage persistant : le dossier de données de PostgreSQL. L'API et l'interface n'écrivent rien qui doive survivre. Les images mesurées le 18 novembre 2026 pèsent 309 Mo (API), 83 Mo (interface) et 424 Mo (`postgres:17-alpine`). Le volume de la base est de quelques mégaoctets avec les données de démonstration ; sa croissance réelle n'a pas été mesurée.

## 13. Base de données

PostgreSQL 17, une base, quatre tables :

| Table | Contenu |
| --- | --- |
| `users` | Comptes : e-mail unique, nom, empreinte du mot de passe, rôle, actif ou non, dates |
| `tickets` | Titre (3 à 120 caractères), description, statut, priorité (`low` à `critical`), catégorie, demandeur, agent assigné, dates |
| `comments` | Commentaires d'un ticket, supprimés avec lui |
| `ticket_events` | Historique d'un ticket : création, changements de statut, assignations |

## 14. Migrations

Il n'y a pas encore d'outil de migration (à concevoir avant toute évolution de schéma, [suivi #68](https://github.com/mathiasseguincadiche/OpsDesk/issues/68)). Au démarrage, l'API crée les tables absentes (`create_all`) et ne modifie jamais une table existante. Conséquence : une version qui changerait le schéma devra fournir sa propre migration, et son retour arrière demandera une restauration de la base. La version 2.0.0 n'a qu'un seul schéma.

## 15. Données persistantes et démonstration

Au premier démarrage sur une base vide, l'API crée le premier administrateur, puis, si `SEED_DEMO_DATA=true`, cinq comptes de démonstration (deux agents, trois collaborateurs, mot de passe commun défini dans `backend/app/bootstrap.py`) et des tickets fictifs. L'opération est rejouable sans effet ; un verrou consultatif PostgreSQL évite les conflits quand plusieurs instances démarrent ensemble. En service réel, définir explicitement `SEED_DEMO_DATA=false` : en mode `production`, toute autre configuration est refusée au démarrage.

## 16. Endpoints de santé

| Route | Réponse | Usage |
| --- | --- | --- |
| `GET /health/live` | `200` `{"status":"alive",…}`, sans interroger la base | Sonde de vie |
| `GET /health/ready` | `200` `{"status":"ready","database":"up",…}`, ou `503` `"database":"down"` | Sonde de disponibilité |
| `GET /version` | Nom, version, révision, environnement | Identifier ce qui tourne |
| `GET /healthz` (nginx) | `200` `ok` | Sonde de vie de l'interface |
| `GET /metrics` (API seulement) | Format Prometheus | Supervision |

## 17. Journaux applicatifs

Une ligne JSON par événement sur la sortie standard, avec l'heure, le niveau et un identifiant de requête (`request_id`, renvoyé aussi dans l'en-tête `x-request-id`). Les mots de passe et les jetons ne sont jamais journalisés. Docker les garde par conteneur (`docker compose logs`) ; leur rotation se règle dans Compose ou dans la configuration du démon.

## 18. Tests unitaires

Les tests de l'API sont dans `backend/tests/` : authentification, rôles et visibilité, cycle de vie, commentaires, statistiques, sondes. Ils tournent sur SQLite par défaut et sur PostgreSQL si `TEST_DATABASE_URL` est défini. Dernier contrôle : 30 tests SQLite et 30 PostgreSQL 17 réussis sur runner le 22 novembre 2026 ([CI applicative](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45005031412)).

## 19. Tests fonctionnels

`scripts/smoke.py` rejoue un parcours complet à travers nginx (sondes, page d'accueil et en-tête CSP, `/metrics` bloqué, refus sans jeton, connexion d'un agent et d'une collaboratrice, création d'un ticket, prise en charge, commentaire, résolution puis clôture par la demandeuse, statistiques) et se termine par `ALL GOOD`. Dernier contrôle consigné : réussi sur la pile locale le 18 novembre 2026. L'interface n'a pas de test automatisé : elle a été vérifiée à la main dans un navigateur.

## 20. Commandes de vérification

```bash
cd backend && .venv/bin/pytest -q && .venv/bin/ruff check app tests
```

```bash
cd frontend && npm run typecheck && npm run build
```

```bash
python3 scripts/smoke.py http://127.0.0.1:8080
```

```bash
curl -i http://127.0.0.1:8080/health/ready
```

Résultats attendus : tous les tests réussis, aucune erreur de typage ni de construction, `ALL GOOD`, puis `200` avec `"database":"up"`.

## 21. Ressources recommandées

Non mesurées sous charge. Dimensionnement prévu pour la machine qui porte le service : 2 vCPU et 4 Go de mémoire (`srv-app`), avec les données PostgreSQL conservées dans le volume Docker nommé `db-data` sur le disque de la VM. Aucun disque supplémentaire n'est imposé par la cible V3 ; la capacité initiale est définie dans le référentiel du laboratoire et reste à confirmer lors de la qualification. L'API tourne en un seul processus par conteneur ; on augmente la capacité en ajoutant des instances. La mesure sous charge est prévue avec k6, sur la copie d'essai.

## 22. Contraintes de sécurité

- Images non-root (UID 10001 pour l'API, 101 pour nginx) et ports non privilégiés.
- En-têtes envoyés par nginx : politique de sécurité du contenu stricte, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`.
- `/metrics` bloqué par nginx ; la base jamais publiée.
- Secrets fournis à l'exécution, jamais dans les images ni dans le dépôt.
- Données fictives uniquement ; le service ne doit pas être exposé sur Internet en l'état.

## 23. Sessions et authentification

Connexion par e-mail et mot de passe. Les mots de passe sont stockés sous forme d'empreinte PBKDF2-SHA256 (390 000 itérations par défaut, sel aléatoire). La session est un jeton JWT signé en HS256 avec `JWT_SECRET`, valable 12 heures par défaut, sans état côté serveur : plusieurs instances de l'API peuvent tourner si elles partagent le même secret. Changer `JWT_SECRET` invalide toutes les sessions en cours ; changer le mot de passe invalide les anciens jetons du compte via une empreinte HMAC. Pas de renouvellement automatique du jeton, pas d'authentification à deux facteurs. Un compte désactivé ne peut plus se connecter.

## 24. Compatibilité des versions

L'API et l'interface sont livrées ensemble, sous le même numéro de version, et doivent être déployées ensemble. L'interface ne dépend que des routes décrites au point 3.

## 25. Contraintes de mise à jour

L'API attend la base au démarrage (30 tentatives espacées de 2 secondes) : l'ordre de démarrage n'est pas critique. La recréation du conteneur de l’API interrompt brièvement les requêtes : environ 2 secondes dans l’essai local du 18 novembre 2026, sans garantie pour un autre scénario. Lors d’une API indisponible, nginx peut répondre `502` (connexion impossible) ou `504` (délai dépassé). Le délai de connexion au backend est limité à 3 secondes ; le délai de lecture reste à 30 secondes. L’interface suit la nouvelle adresse de l’API sans redémarrage. Le réglage a été qualifié le 19 novembre sur un runner jetable : API arrêtée, `504` en 3,003651 s, puis retour à la disponibilité ([preuve](../STATUS.md)).

## 26. Conditions de rollback

Revenir à l'image précédente suffit tant que le schéma de la base n'a pas changé, ce qui est le cas pour toutes les versions 2.0.x. Une future version qui modifierait le schéma imposerait une sauvegarde avant mise à jour, et une restauration en cas de retour arrière (point 14).

## 27. Conditions de sauvegarde et restauration

Seule la base est à sauvegarder. Méthode attendue : `pg_dump` au format custom, cohérent sans arrêt du service, puis `pg_restore` dans une base vide, avec `--no-owner` si les rôles diffèrent. Le `pg_restore` doit être d'une version au moins égale au `pg_dump`. Les secrets (`DB_PASSWORD`, `JWT_SECRET`, `ADMIN_PASSWORD`) se conservent à part : sans le même `JWT_SECRET`, les sessions sont simplement à rouvrir ; sans le mot de passe de la base, la restauration se fait avec un nouveau. La méthode a été démontrée sur une base de démonstration le 18 novembre 2026 ; la restauration de la base d'OpsDesk elle-même reste à faire (exercice 11).

## 28. Dépendances externes

Aucune à l'exécution : ni service tiers, ni appel sortant, ni police ou script chargé depuis Internet. À la construction seulement : les registres d'images, PyPI et npm.

## 29. Limites connues

- Pas d'outil de migration du schéma.
- Pas de renouvellement de jeton ni d'authentification à deux facteurs.
- Pas de pièces jointes aux tickets, pas de notification par e-mail.
- Pas de test automatisé de l'interface.
- Une seule instance de base : point unique de défaillance.
- Non mesurée sous charge.

## 30. Critères de réception applicative

L'application est reçue sur une cible quand, sur cette cible et avec une date :

1. les trois conteneurs sont sains ;
2. `/health/ready` répond `200` avec `"database":"up"`, à travers nginx ;
3. `scripts/smoke.py` se termine par `ALL GOOD` ;
4. un ticket témoin créé est relu après redémarrage des trois conteneurs ;
5. `/version` affiche la version attendue ;
6. `/metrics` n'est pas joignable par le port 8080 ;
7. aucun secret n'apparaît dans les images, le dépôt ou les journaux.

État au 19 novembre 2026 : sur la pile de référence exécutée sur runner jetable, critères 1 à 6 vérifiés (ticket n°18 relu après recréation des conteneurs). Les scans distincts de la revue V26 ont été exécutés ; des vulnérabilités résiduelles interdisent une qualification de sécurité ([suivi](https://github.com/mathiasseguincadiche/OpsDesk/issues/51)). Aucune cible d’infrastructure n’a encore été reçue. Voir [STATUS.md](../STATUS.md).
