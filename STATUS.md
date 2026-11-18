# État d’OpsDesk

Dernière révision : 18 novembre 2026, après la fusion de la v2 ([PR #30](https://github.com/mathiasseguincadiche/OpsDesk/pull/30)). Chaque preuve porte sa date.

**Avancement** : Prévu, En cours, Réalisé, Abandonné. **Contrôle** : Vérifié, Échec constaté, Non vérifié. Les deux informations sont distinctes : un élément réalisé peut rester non vérifié.

## Application v2 (FastAPI, React, PostgreSQL)

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| API : tickets, cycle de vie, commentaires, historique, statistiques | Réalisé | Vérifié le 17 novembre 2026 : 19 tests réussis sur SQLite et sur PostgreSQL 17 | `backend/tests/` ; relancer avec `pytest -q`, ou `TEST_DATABASE_URL=…` pour PostgreSQL |
| Authentification JWT et rôles (collaborateur, support, administrateur) | Réalisé | Vérifié le 17 novembre 2026 : mêmes tests (accès refusé, visibilité par rôle, compte désactivé) | `backend/app/deps.py` ; remplace la décision v1 « authentification abandonnée » |
| Interface web : tableau de bord, tickets, fiche, utilisateurs, profil | Réalisé | Vérifié le 18 novembre 2026 : parcours complet dans un navigateur, thèmes clair et sombre, largeur mobile 375 px | Vérification manuelle, sans test automatisé de l’interface |
| Typage et build du frontend | Réalisé | Vérifié le 18 novembre 2026 : `tsc` et build Vite sans erreur | `frontend/` |
| Sondes, métriques et journaux | Réalisé | Vérifié le 17 novembre 2026 : `/health/live` et `/health/ready` répondent 200 sur PostgreSQL ; `/metrics` expose `opsdesk_database_up 1`, les requêtes et les tickets. Réponse 503 sans base non testée | `backend/app/observability.py` ; aucun Prometheus ni Grafana branché |

## Conteneurs

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Images API et frontend (multi-étapes, non-root) | Réalisé | Vérifié le 17 novembre 2026 : construites avec Docker 29.8 sous WSL2 Ubuntu | `backend/Containerfile`, `frontend/Containerfile` ; **non construites avec Podman** |
| Pile complète (PostgreSQL 17, API, frontend) | Réalisé | Vérifié le 18 novembre 2026 : 3 services *healthy*, `scripts/smoke.py` réussi à travers nginx | `compose.yaml`, réservé aux tests locaux |
| Résilience nginx face au backend | Réalisé | Vérifié le 18 novembre 2026 : API recréée avec une nouvelle IP puis suivie sans redémarrage ; frontend démarré sans API | `frontend/nginx.conf.template` (résolution DNS dynamique) |
| Déploiement Podman + Quadlet sur Rocky Linux | Prévu | Non vérifié | Cible de production retenue ; contraintes dans la section « Déploiement avec Podman et Quadlet » du [README](README.md) |
| Analyse de vulnérabilités des images v2 | Prévu | Non vérifié | Aucun scan Trivy des images v2 ; le scan v1 ci-dessous ne s’applique pas |

## Infrastructure

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Laboratoire Fedora 45, KVM, Rocky Linux 10.2 | Prévu | Non vérifié | [Guide](docs/laboratoire-fedora-kvm-rocky.md) |
| Trois VM Rocky Linux 10.2 (`srv-admin`, `srv-app`, `srv-k3s`) | Prévu | Non vérifié | Aucune VM créée, aucun code Terraform ni Ansible dans le dépôt ; décisions du [registre](docs/architecture.md#décisions-retenues) |
| Unités Quadlet et rôle Ansible de déploiement | Prévu | Non vérifié | À écrire : un réseau, un volume PostgreSQL, trois conteneurs, secrets Podman |
| CI GitHub Actions | Prévu | Non vérifié | Aucun workflow dans le dépôt ; la PR #30 a été fusionnée sans vérification automatique |
| K3s, supervision, sauvegarde et restauration | Prévu | Non vérifié | [Parcours](docs/parcours-apprentissage.md) |

## Documentation

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| README vitrine | Réalisé | Vérifié le 18 novembre 2026 : liens contrôlés, rendu par le moteur Markdown de GitHub en clair, sombre et largeur mobile | [README](README.md) ; rendu sur `main` à confirmer après fusion |
| Architecture et référence technique (v2) | Réalisé | Vérifié le 18 novembre 2026, par relecture contre le code et `compose.yaml` | [Architecture](docs/architecture.md), [référence technique](docs/reference-technique.md) |
| Schémas de présentation et d’architecture (v2) | Réalisé | Vérifié le 18 novembre 2026 : exportés par Draw.io depuis leurs sources, rendu contrôlé | [Schémas](docs/diagrams/README.md) ; schémas v1 dans `legacy/diagrams/` |
| Exercices du parcours et contrat applicatif | En cours | Non vérifié pour la v2 | Écrits pour la v1 ; signalés par un bandeau en tête de chaque document concerné |

## Historique : application v1 (Flask)

L’application Flask, ses tests et ses preuves sont conservés sans modification dans [`legacy/`](legacy/). Ces résultats concernent la v1 uniquement.

| Élément | Contrôle | Preuve |
| --- | --- | --- |
| Pages, API, statuts, persistance | Vérifié le 3 novembre 2026 : 26 tests réussis | [Rapport](legacy/evidence/qualification/application-tests.json) |
| Analyse Trivy 0.74.0 de l’image `0.1.0-local` | Échec constaté le 3 novembre 2026 : 185 occurrences, dont 45 HIGH | [Rapport](legacy/evidence/vulnerability-scan.json) et [triage](docs/triage-securite.md) |
| Smoke HTTP et reprise après arrêt (Ubuntu/WSL2, Docker Compose) | Vérifié le 3 novembre 2026 | [Smoke](legacy/evidence/business-smoke.json), [reprise](legacy/evidence/recovery.json) |

## Apprentissage

Aucun exercice d’infrastructure n’a été réalisé à ce jour. Les niveaux du [parcours](docs/parcours-apprentissage.md) (L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée) ne sont attribués par aucun test. Les [preuves](docs/preuves.md) décrivent la manière de les consigner.

Les pull requests fusionnées documentent l’historique des modifications ; elles ne prouvent ni exécution de la CI ni déploiement.
