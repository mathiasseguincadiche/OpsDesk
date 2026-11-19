# État d’OpsDesk

Dernière révision documentaire : 19 novembre 2026, après la fusion de la v2 ([PR #30](https://github.com/mathiasseguincadiche/OpsDesk/pull/30)). Chaque preuve porte sa date.

**Recette du socle du 19 novembre 2026 — réussie sur runner GitHub Actions jetable Ubuntu** : [exécution finale](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44606981184), code testé `a1a2bb65b6455c4ec7d38b738e53ee6f0e41235d`, schémas régénérés intégrés en `15ddac96a03fc35ea4d18e4cf34809d58a9f6404`. [Extraits authentiques des journaux](evidence/qualification/2026-11-19-socle.txt). Cette recette ponctuelle ne constitue pas la CI/CD personnelle de l’exercice 08 et ne qualifie pas Rocky Linux, AWS ou Kubernetes. Les ateliers DNS/TLS, livraison contrôlée et restriction de l’accès aux métriques restent prévus, non vérifiés.

**Avancement** : Prévu, En cours, Réalisé, Abandonné. **Contrôle** : Vérifié, Échec constaté, Non vérifié. Les deux informations sont distinctes : un élément réalisé peut rester non vérifié.

## Application v2 (FastAPI, React, PostgreSQL)

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| API : tickets, cycle de vie, commentaires, historique, statistiques | Réalisé | Rejoué le 19 novembre 2026 : 19 tests réussis sur SQLite, 19 sur PostgreSQL 17 ; Ruff réussi | `backend/tests/` ; relancer avec `pytest -q`, ou `TEST_DATABASE_URL=…` pour PostgreSQL |
| Authentification JWT et rôles (collaborateur, support, administrateur) | Réalisé | Rejoué le 19 novembre 2026 : mêmes tests (accès refusé, visibilité par rôle, compte désactivé) | `backend/app/deps.py` ; remplace la décision v1 « authentification abandonnée » |
| Interface web : tableau de bord, tickets, fiche, utilisateurs, profil | Réalisé | Vérifié le 18 novembre 2026 : parcours complet dans un navigateur, thèmes clair et sombre, largeur mobile 375 px | Vérification manuelle, sans test automatisé de l’interface |
| Typage et build du frontend | Réalisé | Rejoué le 19 novembre 2026 : `npm ci`, typage TypeScript et build Vite réussis | `frontend/` |
| Sondes, métriques et journaux | Réalisé | Vérifié le 17 novembre 2026 : `/health/live` et `/health/ready` répondent 200 sur PostgreSQL ; `/metrics` expose `opsdesk_database_up 1`, les requêtes et les tickets. Le 19 novembre sur runner : base arrêtée, `/health/ready` = 503, `/health/live` = 200, puis retour à 200 après reprise | `backend/app/observability.py` ; aucun Prometheus ni Grafana branché |

## Conteneurs

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Images API et frontend (multi-étapes, non-root) | Réalisé | Vérifié le 17 novembre 2026, puis le 18 novembre 2026 après le renommage en `Dockerfile` : construites avec Docker 29.8 sous WSL2 Ubuntu | `backend/Dockerfile`, `frontend/Dockerfile` |
| Pile de référence (PostgreSQL 17, API, frontend) | Réalisé | Vérifié le 18 novembre 2026 avec Docker 29.8 et Compose 5.5.1 sous WSL2 Ubuntu : `docker compose config` valide ; 3 services *healthy* ; `scripts/smoke.py` réussi à travers nginx ; base non joignable depuis nginx ; `no-new-privileges` et rotation des journaux appliqués ; API relancée seule après un SIGTERM ; 17 tickets conservés après `down` puis `up`. Rejoué le 19 novembre sur runner : configuration valide, 3 services sains, smoke `ALL GOOD`, ports 8000/8080 liés à `127.0.0.1` et refusés depuis un autre espace réseau, PostgreSQL non publié, ticket témoin n°18 relu après `down`/`up` sans suppression du volume. **Non testé** : redémarrage du démon Docker ou du serveur Rocky | `compose.yaml` : construit les images, ne remplace pas le fichier de production |
| Résilience nginx face au backend | Réalisé | Vérifié le 18 novembre : résolution dynamique et démarrage sans API. Le 19 novembre, après correction du délai de connexion : API arrêtée, réponse `504` en 3,003651 s, frontend vivant, puis disponibilité rétablie | `frontend/nginx.conf.template` (résolution DNS dynamique) |
| Déploiement Docker Engine + Compose sur Rocky Linux | Prévu | Non vérifié | Cible retenue le 18 novembre 2026, à la place de Podman et Quadlet ; contraintes dans la [référence technique](docs/reference-technique.md#déployer-avec-docker-compose-sur-un-serveur) |
| Analyse de vulnérabilités des images v2 | Prévu | Non vérifié | Aucun scan Trivy des images v2 ; le scan v1 ci-dessous ne s’applique pas |

## Infrastructure

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Laboratoire Fedora 45, KVM, Rocky Linux 10.2 | Prévu | Non vérifié | [Guide](docs/laboratoire-fedora-kvm-rocky.md) |
| Trois VM Rocky Linux 10.2 (`srv-admin`, `srv-app`, `srv-k3s`) | Prévu | Non vérifié | Aucune VM créée, aucun code Terraform ni Ansible dans le dépôt ; décisions du [registre](docs/architecture.md#décisions-retenues) |
| Fichier Compose de production et rôles Ansible (Docker, déploiement) | Prévu | Non vérifié | À écrire (exercices 05, 06, 08) : installation de Docker depuis son dépôt officiel, images par digest, secrets en fichiers, SELinux et pare-feu prouvés |
| CI GitHub Actions | Prévu | Non vérifié | Aucun workflow de livraison sur `main` ; la [recette ponctuelle](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44606981184) vit sur une branche isolée, sans publication GHCR ; l’exercice 08 reste à écrire |
| K3s, supervision, sauvegarde et restauration | Prévu | Non vérifié | [Parcours](docs/parcours-apprentissage.md) |

## Documentation

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| README vitrine | Réalisé | Vérifié le 18 novembre 2026 : liens contrôlés, rendu par le moteur Markdown de GitHub en clair, sombre et largeur mobile | [README](README.md) ; rendu confirmé sur `main` le 18 novembre 2026 après fusion (#33) |
| Architecture et référence technique (v2) | Réalisé | Vérifié le 18 novembre 2026, par relecture contre le code et `compose.yaml` | [Architecture](docs/architecture.md), [référence technique](docs/reference-technique.md) |
| Schémas de présentation et d’architecture (v2) | Réalisé | Requalifié le 19 novembre : les 13 sources contrôlées, six corrections régénérées par Draw.io 32.7.4, les 26 rendus navigateur inspectés (clair/sombre) | [Schémas](docs/diagrams/README.md) ; schémas v1 dans `legacy/diagrams/` |
| Exercices du parcours (13 énoncés) | Réalisé | Vérifié le 18 novembre 2026 par relecture contre le code, `compose.yaml` et le registre ; liens contrôlés | [Parcours](docs/apprentissage/README.md) ; cours complet dans Notion. Les exemples réels des fiches (sorties de l'API, sauvegarde et restauration PostgreSQL, panne de base, coupure mesurée) ont été obtenus sur l'environnement local le 18 novembre 2026 ; les autres sont marqués « sortie type » |
| Schémas pédagogiques des exercices 03 à 11 | Réalisé | Requalifié le 19 novembre : voir les 13 schémas et rendus navigateur ; sept exports inchangés | [Schémas](docs/diagrams/README.md) |
| Repères de correction et cinq évaluations | Réalisé | Vérifié le 18 novembre 2026 par relecture contre le code et le registre | [Corrigés](docs/apprentissage/corriges.md), [évaluations](docs/apprentissage/evaluations.md) ; aucune évaluation menée |
| Contrat applicatif (v2) | Réalisé | Vérifié le 18 novembre 2026 par relecture contre le code, `compose.yaml` et `scripts/smoke.py` | [Contrat](docs/contrat-applicatif.md) : routes, droits, configuration, données, sécurité, limites, critères de réception |
| Sécurité, preuves, provenance, démarrage, exploitation et reprise (v2) | Réalisé | Vérifié le 18 novembre 2026 par relecture contre le code et `compose.yaml` | [Sécurité](docs/securite.md), [preuves](docs/preuves.md), [provenance](docs/provenance.md), [démarrage](docs/demarrage.md), [exploitation](docs/exploitation-day2.md), [reprise](docs/reprise.md) ; les documents propres à la v1 (CI, infrastructure, livraison, triage, versions) sont archivés dans [`legacy/docs/`](legacy/docs/README.md) |

## Historique : application v1 (Flask)

L’application Flask, ses tests et ses preuves sont conservés sans modification dans [`legacy/`](legacy/). Ces résultats concernent la v1 uniquement.

| Élément | Contrôle | Preuve |
| --- | --- | --- |
| Pages, API, statuts, persistance | Vérifié le 3 novembre 2026 : 26 tests réussis | [Rapport](legacy/evidence/qualification/application-tests.json) |
| Analyse Trivy 0.74.0 de l’image `0.1.0-local` | Échec constaté le 3 novembre 2026 : 185 occurrences, dont 45 HIGH | [Rapport](legacy/evidence/vulnerability-scan.json) et [triage](legacy/docs/triage-securite.md) |
| Smoke HTTP et reprise après arrêt (Ubuntu/WSL2, Docker Compose) | Vérifié le 3 novembre 2026 | [Smoke](legacy/evidence/business-smoke.json), [reprise](legacy/evidence/recovery.json) |

## Apprentissage

Aucun exercice d’infrastructure n’a été réalisé à ce jour. Les niveaux du [parcours](docs/parcours-apprentissage.md) (L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée) ne sont attribués par aucun test. Les [preuves](docs/preuves.md) décrivent la manière de les consigner.

Les pull requests fusionnées documentent l’historique des modifications. Les journaux d’exécution liés ci-dessus prouvent uniquement la recette sur le runner, ni un déploiement sur Rocky ni la maîtrise personnelle.
