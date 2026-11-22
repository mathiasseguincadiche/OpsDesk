# État d’OpsDesk

Révision : 19 novembre 2026, heure Martinique. Sont distingués **avancement** (prévu, en cours, réalisé, abandonné) et **contrôle** (vérifié, échec constaté, non vérifié). Le socle fourni n'est pas la réalisation personnelle.

**En bref :** le socle FastAPI/React/PostgreSQL fonctionne sur runner Ubuntu ; l'infrastructure Rocky, la livraison et l'exploitation restent à construire. La recette locale est réussie ; les alertes résiduelles des images officielles restent suivies. Laboratoire privé uniquement.

## Application v2 (FastAPI, React, PostgreSQL)

| Élément | Avancement | Contrôle et preuve |
| --- | --- | --- |
| API, authentification, rôles | Réalisé | Vérifié : 28 tests SQLite + 28 PostgreSQL 17, Ruff |
| Frontend | Réalisé | Vérifié : typage/build ; navigation manuelle historique, pas de test d'interface automatisé |
| Sondes, métriques et journaux | Réalisé | Vérifié sur runner pour les sondes ; supervision à installer |

## Conteneurs

| Élément | Avancement | Contrôle et preuve |
| --- | --- | --- |
| Images non-root, Compose local | Réalisé | Vérifié : construction, smoke, isolation des ports, reprise API/base, persistance après recréation |
| Scan Trivy v2 | Réalisé | Alertes résiduelles : API 47 HIGH (11 CVE Debian sans correctif indiqué) ; frontend 0 ; PostgreSQL 1 CRITICAL + 26 HIGH dans `gosu` (aucun symbole vulnérable détecté par govulncheck). Pas de qualification de sécurité pour une exposition publique. [Suivi #51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51) |
| Déploiement Rocky | Prévu | Non vérifié |

[Recette de finition V26](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44646629874) — six jobs réussis sur runner Ubuntu ; code testé `a2d89673980c39abe906e96d78fd88a78b75e7a7`. Les détails, digests et limites sont consignés dans les [preuves V26](evidence/qualification/2026-11-19-v26-mise-en-conformite.md). Le succès du scan ne signifie pas conformité sécurité.

[Recette de stabilisation](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44649917348) — quatre jobs réussis, commit `dbb4939a381c504371cd39ff4ee9f618d549ff80` : démarrage sans `.env`, tests, reprise et persistance, scan des images effectivement exécutées, 308 liens relatifs sur 35 fichiers, 15 paires graphiques. Voir les [preuves V26](evidence/qualification/2026-11-19-v26-mise-en-conformite.md#stabilisation-finale). Le retrait de pip ne modifie pas le code métier ni les dépendances applicatives.

## Infrastructure

| Élément | Avancement | Contrôle |
| --- | --- | --- |
| Fedora/KVM, 3 VM Rocky, Terraform, Ansible | Prévu | Non vérifié |
| Docker Compose de production, rôles, DNS/TLS | Prévu | Non vérifié |
| CI/CD personnelle, K3s | Prévu | Non vérifié |
| Supervision, sauvegarde/restauration, maintenance | Prévu | Non vérifié |

La recette ponctuelle sur runner ne constitue pas un pipeline de livraison de l'application. Aucun pipeline GHCR de livraison personnelle n'est validé.

## Documentation technique

Le dépôt contient les contrats, procédures, schémas techniques et résultats de qualification du produit. Les résultats historiques des 15 paires Draw.io/SVG contrôlées le 19 novembre 2026 demeurent datés : les schémas exclusivement pédagogiques ont été transférés dans Notion avec leurs sources. L'affichage sur les appareils réels n'est pas certifié par les tests automatisés. Voir [schémas techniques](docs/diagrams/README.md) et [contrat applicatif](docs/contrat-applicatif.md).

## Historique : application v1 (Flask)

Les preuves v1 restent dans [legacy](legacy/). Le [statut détaillé antérieur à la V26](https://github.com/mathiasseguincadiche/OpsDesk/blob/d2a8e9e204b1bb797c26b1e1c927b9ec4fe166b1/STATUS.md) conserve toutes les observations historiques et leurs périmètres, dont la [recette du socle](evidence/qualification/2026-11-19-socle.txt). Aucun résultat ancien n'est transféré à un nouveau code sans contrôle.

