# Provenance des éléments du dépôt

| Ensemble | Origine | Usage |
| --- | --- | --- |
| Application `app/`, schéma `db/schema.sql`, tests, contrat applicatif | Produits avec l’aide d’un assistant d’IA, pour une équipe de développement fictive | Support applicatif du laboratoire |
| Python, Flask/Jinja, psycopg, Gunicorn, PostgreSQL | Composants tiers, sous leurs propres licences ; la licence MIT du dépôt ne les remplace pas | Dépendances de l’application |
| Anciennes recettes conteneurs, Terraform, Ansible, K3s, CI, reprise | Générées avec l’aide d’un assistant d’IA, puis partiellement essayées | Références historiques, à comparer après une tentative personnelle |
| Énoncés, indices, corrigés, évaluations | Préparés avec l’aide d’un assistant d’IA | Aide progressive ; aucun niveau personnel attribué |
| Schémas | Dessinés pour le projet ; logos du paquet simple-icons (licence CC0) | Voir [`diagrams/README.md`](diagrams/README.md) |
| Infrastructure cible et opérations | À concevoir, écrire, exécuter et expliquer par l’apprenant | Réalisation personnelle à prouver |

Un essai historique ou un PASS n’est pas une réalisation personnelle. Le détail des preuves est dans [STATUS](../STATUS.md) et [preuves](preuves.md).

## Fichiers historiques absents du dépôt

Au contrôle de `main` du 4 novembre 2026 (`51e1a489`), les fichiers suivants ne sont plus dans le dépôt ; les rapports JSON de `evidence/` restent disponibles. La conservation des originaux dans un autre espace est **NON VÉRIFIÉE**.

- Conteneurs : `Dockerfile`, `.dockerignore`, `compose.yaml`, `scripts/prepare-local.sh`.
- Base de données : `db/001-initial.sql`, qui mélange schéma et création du rôle.
- Terraform et Ansible : `infra/terraform/main.tf`, `infra/ansible/`, `infra/verify.py`.
- K3s : `k8s/`, `infra/verify_k8s.py` (rendus hors cluster seulement).
- CI : `.github/workflows/verify.yml`, `.gitlab-ci.yml` (candidats jamais exécutés à distance).
- Exploitation : `scripts/probe.py`, `scripts/recovery_lab.py`.

Les configurations Terraform ne créaient que des contrats locaux ; les rendus Ansible écrivaient des fichiers sur localhost. Aucune machine Rocky ou KVM, aucun cloud et aucun cluster K3s n’ont été créés.

## Usage pédagogique

Les anciens guides techniques servent après une première tentative. L’apprenant décide de son architecture et écrit ses propres fichiers. Les niveaux du [parcours](parcours-apprentissage.md) (L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée) ne se déduisent d’aucun résultat historique.

Le défaut `ci-business.json` / `business-smoke.json` du candidat CI est conservé pour un exercice de diagnostic. Les durées de reprise historiques ne sont pas des objectifs de production.

## Une source de vérité par sujet

| Question du lecteur | Source de vérité | Quand la mettre à jour |
| --- | --- | --- |
| Découvrir le projet | [README](../README.md) | Quand le périmètre ou l’état change |
| Apprendre et comprendre | [Exercices](apprentissage/README.md) et Notion | Dans le même changement que les notions concernées, sans copier le README |
| Connaître l’interface, les champs, les contraintes | [Contrat applicatif](contrat-applicatif.md), vérifié contre `business.py`, `web.py` et `schema.sql` | À chaque évolution de l’API |
| Expliquer un choix durable | [Registre des décisions](architecture.md#décisions-durables-et-décisions-encore-personnelles) | Après une vraie décision ; les raisons inconnues ne sont pas inventées |
| Constater un résultat | [STATUS](../STATUS.md) et [preuves](preuves.md), avec date, méthode et portée | À chaque nouveau contrôle ; un résultat périmé n’est plus présenté comme actuel |
| Agir en incident | [Triage](reprise.md#triage-court-avant-une-reprise-personnelle) | Après chaque exercice de reprise |

Avant un déplacement de fichier, recenser les liens entrants. Les versions d’outils, les compatibilités et les interfaces vieillissent : les revérifier dans leurs sources officielles avant de pratiquer.

## Vocabulaire

- **Hôte** : le poste Fedora prévu. **Invité** : la VM Rocky prévue.
- **Application** : le programme fourni. **Infrastructure personnelle** : ce que l’apprenant construit. **Référence historique** : un essai daté, antérieur au travail personnel.
- **Réalisé** : l’élément existe. **Vérifié** : un contrôle traçable l’a confirmé. **PASS** : le résultat de ce contrôle. **L3** : une adaptation ou un diagnostic personnel sur une tâche nouvelle.
