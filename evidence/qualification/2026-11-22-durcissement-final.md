# Durcissement du socle OpsDesk — bilan vérifié du 22 novembre 2026

Ce document établit **quels contrôles ont réellement été exécutés**, sur quels runners, et ce qui n'a pas encore été essayé. Les fichiers de configuration de production présents dans Git ne constituent pas une preuve de déploiement sur les futures VM.

## Images utilisées — Trivy

| Image exécutée | CRITICAL | HIGH | Source |
| --- | ---: | ---: | --- |
| API Python 3.13 Alpine | 0 | 0 | [Scan PR #75](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45008435034) |
| Frontend nginx non-root | 0 | 0 | Même scan |
| PostgreSQL 17 dérivé, sans couches de l'ancien `gosu` | 0 | 0 | Même scan |
| PostgreSQL 17-alpine **officiel non exécuté** | 1 | 26 | Rapport comparatif du même scan |

Les rapports complets sont disponibles dans les artefacts du workflow. La règle CI actuelle **échoue** si les images retenues portent des résultats HIGH ou CRITICAL ; ce contrôle est daté et ne garantit pas l'absence de toutes les failles. Le suivi spécifique des anciennes images a été [clôturé dans l'issue #51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51).

## Base et démarrage de production sur runner

[PR #77](https://github.com/mathiasseguincadiche/OpsDesk/pull/77), [run applicatif 45009128461](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45009128461) :

- L'image API inclut `alembic.ini`, `migrations/` et les deux révisions SQLAlchemy/Alembic, lisibles sous UID 10001.
- La base `opsdesk_prod_ci` créée pour le test est distincte de la base de démonstration.
- L'initialisation en mode `production` **échoue comme attendu** avant la migration : révision absente.
- `alembic upgrade head`, `alembic check`, puis initialisation de production avec `SEED_DEMO_DATA=false`, `ALLOW_REGISTRATION=false` et secrets fictifs passent.
- Le compte administrateur existe et la révision `opsdesk_20261122_02` est enregistrée.
- Sortie du job : `PASS : production refusée sans Alembic, deux migrations contrôlées, admin créé.`

Ceci ne teste pas une migration d'une base métier préexistante ni une exécution sur Rocky.

## Sauvegarde, parcours applicatif et navigateur

- [Run 45009128461](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45009128461) : tests API SQLite et PostgreSQL, build React, Compose et parcours HTTP, `pg_dump` / `pg_restore` dans une base séparée, vérification de 17 tickets après redémarrage.
- [Run Chromium 45008787169](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45008787169) : cookie de session HttpOnly SameSite=Strict, cookie CSRF, refus HTTP 403 sans en-tête, création d'un ticket et rechargement, déconnexion, absence de JWT en localStorage, viewport mobile simulé.
- [Captures bureau et mobile](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45008787169/artifacts/14749330367) : fichiers issus du navigateur du runner, non des maquettes.
- Limitation commune des tentatives de connexion en PostgreSQL testée par l'API, en complément du 429 Nginx.

## Ce qui reste hors périmètre

Le laboratoire Fedora/KVM/Rocky, le TLS réel, le filtrage réseau et firewalld, les secrets de production, les sauvegardes hors serveur, la mesure de RPO/RTO, les permissions de stockage et la livraison GHCR **n'ont pas été réalisés dans ces runs**. La recette mobile n'a pas été faite sur appareil physique. Les impacts d'un frontal reverse proxy de production et les migrations de bases réelles restent à vérifier.

[Issue #68 — qualification infrastructurelle restante](https://github.com/mathiasseguincadiche/OpsDesk/issues/68) · [Architecture](../../docs/architecture.md) · [Reprise](../../docs/reprise.md) · [Statut](../../STATUS.md)
