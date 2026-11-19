# Sécurité d'OpsDesk

Ce document dit ce que l'application protège, comment, et ce qu'elle laisse à l'infrastructure. Mise à jour : 18 novembre 2026, pour la version 2.0.0, par relecture du code.

## Le cadre

OpsDesk est un service de laboratoire : **données fictives, aucune exposition sur Internet**. Les protections décrites ici sont réelles et testées, mais elles ne suffisent pas à exposer le service publiquement (voir « Limites »).

## Ce que l'application protège

| Risque | Protection | Où |
| --- | --- | --- |
| Accès sans compte | Toutes les routes métier exigent un jeton JWT signé ; sinon `401` | `backend/app/deps.py` |
| Accès au-delà de son rôle | Rôle vérifié par l'API à chaque requête (`user`, `agent`, `admin`) ; sinon `403` | `backend/app/deps.py`, `routers/` |
| Lecture des tickets d'autrui | Un collaborateur ne voit que ses propres tickets ; un ticket non visible répond `404` | `routers/tickets.py` |
| Changement de statut abusif | Cycle de vie et droits par rôle vérifiés côté serveur ; sinon `403` ou `409` | `backend/app/workflow.py` |
| Mots de passe volés en base | Empreinte PBKDF2-SHA256, sel aléatoire, 390 000 itérations par défaut ; jamais de mot de passe en clair | `backend/app/security.py` |
| Compte compromis | Un administrateur peut désactiver un compte : il ne peut plus se connecter, et ses jetons sont refusés | `routers/users.py`, `deps.py` |
| Données invalides ou démesurées | Validation de chaque champ (longueurs, valeurs permises) ; sinon `422` | `backend/app/schemas.py` |
| Injection SQL | Requêtes construites par SQLAlchemy, toujours paramétrées | `backend/app/` |
| Fuite d'informations par les erreurs | Erreurs internes réduites à « Erreur interne du serveur. » ; détail seulement dans les journaux | `backend/app/main.py` |
| Fuite de secrets dans les journaux | Ni mot de passe ni jeton journalisé | `backend/app/observability.py` |
| Injection de scripts dans l'interface | Politique de sécurité du contenu stricte (`default-src 'self'`, script en ligne autorisé par empreinte), `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy` | `frontend/nginx.conf.template` |
| Exposition des mesures internes | `/metrics` bloqué par nginx | `frontend/nginx.conf.template` |
| Conteneur compromis | Images non-root (UID 10001 pour l'API, 101 pour nginx), ports non privilégiés | `backend/Dockerfile`, `frontend/Dockerfile` ; `no-new-privileges` dans `compose.yaml` |

Les refus (`401`, `403`, compte désactivé, visibilité par rôle) sont couverts par les tests de l'API ; dernier contrôle consigné le 17 novembre 2026 dans [STATUS.md](../STATUS.md).

## Les secrets

| Secret | Usage | Règle |
| --- | --- | --- |
| `DB_PASSWORD` | Connexion à PostgreSQL | Fourni à l'exécution |
| `JWT_SECRET` | Signature des jetons | 32 caractères au moins ; **obligatoire** quand `ENVIRONMENT=production` ; le changer déconnecte tout le monde |
| `ADMIN_PASSWORD` | Premier administrateur | Utilisé une seule fois, à la création du compte |

Chaque secret accepte une forme `*_FILE` qui lit sa valeur dans un fichier : c'est la forme attendue des secrets de Compose et de Kubernetes. Aucun secret n'est dans les images ni dans le dépôt : `.env` et les dossiers `secrets/` sont exclus par `.gitignore`, seul `.env.example` (sans valeur réelle) est versionné.

## Ce qui revient à l'infrastructure

L'application ne peut pas se protéger seule. Les décisions suivantes sont prises au [registre](architecture.md#décisions-retenues) et se construisent dans le [parcours](apprentissage/README.md) :

- **Réseau** : seul le port 8080 ouvert aux utilisateurs ; 8000 ouvert à la supervision seulement ; 5432 jamais publié ; firewalld actif.
- **Système** : SELinux en mode `Enforcing` ; SSH par clé, sans mot de passe ni connexion `root`.
- **Exécution** : Docker Engine, dont le démon tourne en root. Personne n'est dans le groupe `docker` (qui vaut root) : administration par `sudo`, tracée. Le socket Docker n'est monté dans aucun conteneur et l'API Docker n'écoute pas sur le réseau. Les conteneurs tournent sans root, avec `no-new-privileges`.
- **Pare-feu et SELinux face à Docker** : Docker écrit ses propres règles de filtrage (zone firewalld `docker`) ; l'exposition réelle d'un port se prouve depuis une autre machine. SELinux ne s'applique aux conteneurs que si le démon l'active (`selinux-enabled`).
- **Secrets** : fichiers lisibles par le seul conteneur qui les lit, montés par le bloc `secrets:` de Compose ; jamais dans le fichier Compose, ni dans Git, ni en clair dans les rôles Ansible.
- **Images** : analyse Trivy dans la CI, avec une règle écrite pour les vulnérabilités graves (exercice 08).
- **Sauvegardes** : copies hors du serveur, avec une clé SSH limitée à ce seul usage (exercice 11).

## Limites connues

- **Aucune analyse de vulnérabilités des images v2** n'a encore été faite.
- Pas de limitation du nombre de tentatives de connexion.
- Pas d'authentification à deux facteurs ni de renouvellement automatique du jeton.
- Pas de HTTPS dans l’application : il se termine devant elle. L’atelier DNS/TLS de l’exercice 06 le met en pratique sur une cible privée, sans exposer le laboratoire. Ce contrôle reste à réaliser.
- Le port 8000 ouvert à `srv-k3s` donne accès à toute l'API, pas seulement à `/metrics` (question ouverte relevée à l'exercice 02).

Ces limites interdisent une exposition sur Internet en l'état ; elles sont acceptables pour un laboratoire aux données fictives.

## Historique

La version 1 n'avait pas d'authentification. Son scan Trivy (3 novembre 2026, échec constaté : 185 occurrences dont 45 HIGH) et sa lecture sont conservés dans [`legacy/docs/triage-securite.md`](../legacy/docs/triage-securite.md) ; ils ne s'appliquent pas à la version 2.

## Licence

Le code du dépôt est sous licence [MIT](../LICENSE) ; chaque dépendance garde sa propre licence. L'origine de chaque partie du dépôt est décrite dans [la provenance](provenance.md).
