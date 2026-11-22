# Qualification CI du socle — 22 novembre 2026

**Cible :** GitHub Actions sur Ubuntu 24.04, sur le commit `babd1768f8c59c59468774c83a7b21b1628d1f07` de la PR #67. Ce document décrit une qualification sur runner **jetable**, pas une exécution du laboratoire personnel.

**Exécution source :** [Application quality — run 45005031412](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45005031412).

| Job | Résultat enregistré | Portée |
| --- | --- | --- |
| API | Succès ; 30 tests SQLite, 30 tests PostgreSQL 17 ; Ruff sans erreur | Endpoints et règles couverts par les tests, garde-fous de production et révocation de JWT |
| Interface | Succès ; compilation TypeScript 7 et build Vite | Résolution d'alias adaptée à la version de TypeScript |
| Conteneurs | Succès ; `docker compose config`, build, démarrage sain, parcours HTTP via nginx, HTTP 429 d'authentification | Version du socle de démonstration, avec données fictives uniquement |
| Nettoyage | Succès ; `docker compose down -v --remove-orphans` | La base créée pour ce test est supprimée sur le runner |

## Ce que le résultat ne prouve pas

- Aucune VM Fedora/KVM/Rocky n'a été construite ou administrée.
- Aucune image n'a été publiée dans GHCR et aucune restauration de la base d'OpsDesk n'a été validée ici.
- Aucun scan Trivy **actualisé** n'a été exécuté dans ce workflow : les vulnérabilités historiques restent sous [#51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51).
- Aucune campagne de sécurité, de performance, de navigation mobile native ou de reprise réelle n'est certifiée.
- La limitation Nginx est calculée sur l'IP de son pair réseau et ne protège pas un accès direct à l'API.

L'exposition publique demeure exclue. Les évolutions de session, migration de schéma, frontal et filtrage sont suivies dans [#68](https://github.com/mathiasseguincadiche/OpsDesk/issues/68).

**Traçabilité :** cette preuve est datée et attachée au commit testé ; tout nouveau changement de code nécessite de nouveaux contrôles.
