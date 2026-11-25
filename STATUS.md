# État d’OpsDesk

Révision : 22 novembre 2026, heure Martinique. Sont distingués **avancement** (prévu, en cours, réalisé, abandonné) et **contrôle** (vérifié, échec constaté, non vérifié). Le socle fourni n'est pas la réalisation personnelle.

**En bref :** le socle FastAPI/React/PostgreSQL fonctionne sur runner Ubuntu ; l'infrastructure Rocky, la livraison et l'exploitation restent à construire. La recette du socle est réussie ; le scan des images **exécutées** indique zéro HIGH/CRITICAL au 22 novembre. La qualification de production réelle demeure à réaliser. Laboratoire privé uniquement.

## Application v2 (FastAPI, React, PostgreSQL)

| Élément | Avancement | Contrôle et preuve |
| --- | --- | --- |
| API, authentification, rôles | Réalisé | Vérifié sur runner : 30 tests SQLite + 30 PostgreSQL 17, Ruff (22/11/2026) |
| Frontend | Réalisé | Vérifié : typage/build TypeScript 7 et navigation Chromium automatisée (connexion, ticket, session, déconnexion, viewport mobile) ; appareils physiques non vérifiés |
| Sondes, métriques et journaux | Réalisé | Vérifié sur runner pour les sondes ; supervision à installer |

## Conteneurs

| Élément | Avancement | Contrôle et preuve |
| --- | --- | --- |
| Images non-root, Compose local | Réalisé | Vérifié : construction, smoke, isolation des ports, reprise API/base, persistance après recréation |
| Scan Trivy v2 | Réalisé | Vérifié le 22/11 : **0 HIGH / 0 CRITICAL sur les trois images utilisées** (API Python Alpine, frontend, PostgreSQL dérivé). CI bloquante en cas de régression HIGH/CRITICAL ; l'image PostgreSQL officielle d'origine reste scannée séparément et affiche 1 CRITICAL + 26 HIGH. [Issue #51 clôturée dans ce périmètre](https://github.com/mathiasseguincadiche/OpsDesk/issues/51). Cela n'homologue pas une exposition publique. |
| Déploiement Rocky | Prévu | Non vérifié |

[Recette de finition V26](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44646629874) — six jobs réussis sur runner Ubuntu ; code testé `a2d89673980c39abe906e96d78fd88a78b75e7a7`. Les détails, digests et limites sont consignés dans les [preuves V26](evidence/qualification/2026-11-19-v26-mise-en-conformite.md). Le succès du scan ne signifie pas conformité sécurité.

[Recette de stabilisation](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44649917348) — quatre jobs réussis, commit `dbb4939a381c504371cd39ff4ee9f618d549ff80` : démarrage sans `.env`, tests, reprise et persistance, scan des images effectivement exécutées, 308 liens relatifs sur 35 fichiers, 15 paires graphiques. Voir les [preuves V26](evidence/qualification/2026-11-19-v26-mise-en-conformite.md#stabilisation-finale). Le retrait de pip ne modifie pas le code métier ni les dépendances applicatives.

## Qualification continue du socle (22 novembre 2026)

Le [workflow CI applicative](docs/ci-applicative.md) a réussi ses trois jobs sur [le run 45005031412](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45005031412), pour le commit de code `babd1768f8c59c59468774c83a7b21b1628d1f07` : 30 tests SQLite et 30 PostgreSQL 17, Ruff, compilation React/TypeScript 7, construction et démarrage des trois conteneurs, parcours HTTP de démonstration et contrôle d'une limitation de connexions par Nginx. Le job supprime ses volumes de test à la fin. Les détails et limites sont dans la [fiche de qualification](evidence/qualification/2026-11-22-audit-cicd.md).

Les contrôles initiaux du run 45005031412 sont historiques. Depuis, les [scans Trivy actualisés](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45008435034), la [recette Chromium](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45008787169) et le [test d'image de production Alembic](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45009128461) ont réussi. La [preuve consolidée](evidence/qualification/2026-11-22-durcissement-final.md) précise leurs cibles et leurs limites. Le [durcissement de l'infrastructure réelle #68](https://github.com/mathiasseguincadiche/OpsDesk/issues/68) reste ouvert.

## Durcissement ciblé PostgreSQL

Le dépôt contient une image dérivée dans [`db/Dockerfile`](db/Dockerfile), qui conserve le serveur PostgreSQL officiel 17 et remplace l'outil de lancement `gosu` par `su-exec` d'Alpine. **Statut : correctif fusionné et qualifié sur runner (PR #71, scan 0 HIGH/CRITICAL)**, sans garantie d'exposition publique. Le scan compare cette image utilisée par Compose à l'image officielle d'origine, en conservant les résultats et digests.

## Réanalyse des images — automatisation

Le workflow [Image security audit](.github/workflows/image-security.yml) reconstruit les images API/frontend et scanne également PostgreSQL 17 avec Trivy sur chaque changement concerné ou chaque semaine. Il enregistre les rapports JSON et les identifiants dans des artefacts datés. **Toute occurrence HIGH/CRITICAL dans les trois images retenues échoue le job**, tout comme une erreur de scan ; l'image officielle PostgreSQL non exécutée reste analysée pour comparaison. L'[issue #51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51) est clôturée pour les images retenues à cette date. Réévaluer tout résultat ultérieur. Une validation CI ne prouve pas la sécurité de la future infrastructure.

## Restauration fonctionnelle du socle — 22 novembre 2026

Le [run de CI 45006326819](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45006326819) a validé, sur une base de démonstration jetable, un `pg_dump` en format custom, un `pg_restore` dans une **base distincte** et le contrôle des tickets restaurés. **17 tickets** ont été retrouvés, dont le ticket témoin ; l'API a ensuite redémarré et répondu `ready` sans perte des données observées. Voir [preuve datée](evidence/qualification/2026-11-22-restauration-ci.md).

Il s'agit d'un test sur runner, non d'une sauvegarde hors serveur ou d'un plan de reprise personnel testé sur les VM Rocky ; les RPO et RTO ne sont pas qualifiés.

## Architecture V3 — décisions validées, réalisation non commencée

Le 25 novembre 2026, **Architecture OpsDesk V3** remplace la V2 d’infrastructure du 22 novembre, sans changer l’application V2. [Sept ADR](docs/adr/README.md), [flux V3](docs/architecture-v3-flux.md) et [phases 0 à 10](docs/architecture-v3-deploiement.md) décrivent la cible : Terraform et Ansible sur Fedora, cloud-init minimal, inventaire issu des outputs, trois VM Rocky (`srv-app`, `srv-ops`, `srv-k3s`), supervision indépendante et k6 à la demande. HTTPS, GHCR privé par digest, Vault, Borg externe chiffré et notifications Grafana par e-mail sont conservés. Aucun provisionnement ni contrôle Fedora/Rocky n’a été effectué. Les schémas nécessitent une inspection native.

## Infrastructure

| Élément | Avancement | Contrôle |
| --- | --- | --- |
| Fedora/KVM, 3 VM Rocky, Terraform, Ansible | Prévu | Non vérifié |
| Docker Compose de production, rôles, DNS/TLS | Prévu | Non vérifié |
| CI/CD personnelle, K3s | Prévu | Non vérifié |
| Supervision, sauvegarde/restauration, maintenance | Prévu | Non vérifié |

La CI actuelle est un pipeline de **qualification du socle applicatif** ; elle n'enregistre aucune image dans GHCR et n'effectue aucun déploiement. La chaîne personnelle de livraison reste prévue, non vérifiée.

## Documentation technique

Le dépôt contient les contrats, procédures, schémas techniques et résultats de qualification du produit. Les résultats historiques des 15 paires Draw.io/SVG contrôlées le 19 novembre 2026 demeurent datés : les schémas exclusivement pédagogiques ont été transférés dans Notion avec leurs sources. Une recette Chromium sur runner a vérifié un viewport mobile simulé, avec captures réelles ; l'affichage sur de véritables appareils mobiles reste non vérifié. Voir [schémas techniques](docs/diagrams/README.md) et [contrat applicatif](docs/contrat-applicatif.md).

## Historique : application v1 (Flask)

Les preuves v1 restent dans [legacy](legacy/). Le [statut détaillé antérieur à la V26](https://github.com/mathiasseguincadiche/OpsDesk/blob/d2a8e9e204b1bb797c26b1e1c927b9ec4fe166b1/STATUS.md) conserve toutes les observations historiques et leurs périmètres, dont la [recette du socle](evidence/qualification/2026-11-19-socle.txt). Aucun résultat ancien n'est transféré à un nouveau code sans contrôle.
