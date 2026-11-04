# Provenance et séparation des responsabilités — OpsDesk

| Ensemble | Origine constatée | Usage V4.4 |
|---|---|---|
| Application `app/`, schéma `db/schema.sql`, tests et contrat | Fournis par Codex pour une équipe de développement fictive | Support applicatif de laboratoire |
| Python, Flask/Jinja, psycopg, Gunicorn et PostgreSQL | Composants tiers, licences propres conservées | Dépendances du support ; la licence MIT du dépôt ne les remplace pas |
| Anciennes recettes conteneurs, Terraform, Ansible, K3s, CI et reprise | Générées et partiellement essayées par Codex sous V4.2 | Références historiques, à comparer après une tentative personnelle |
| Énoncés, indices, corrigés séparés et évaluations | Préparation pédagogique Codex | Aide progressive, aucun niveau personnel attribué |
| Infrastructure cible et opérations personnelles | À concevoir, écrire, exécuter et expliquer par Mathias | Réalisation personnelle à prouver |

## Chemins historiques identifiés et disponibilité actuelle

Les chemins suivants décrivent l’antériorité locale V4.2 rapportée dans les notes et preuves. Au contrôle de `main` `51e1a489` le 4 novembre 2026, ces configurations et scripts InfraOps sont absents du dépôt ; les JSON sous `evidence/` y restent disponibles. La conservation de leurs originaux dans un autre espace local est **NON VÉRIFIÉE** dans cette passe. Ils ne sont pas des solutions personnelles réalisées :

- Conteneurs : `Dockerfile`, `.dockerignore`, `compose.yaml`, `scripts/prepare-local.sh`.
- Administration DB : `db/001-initial.sql`, qui mélange schéma et création/droits du rôle.
- Terraform/Ansible : `infra/terraform/main.tf`, `infra/ansible/`, `infra/verify.py`.
- K3s : `k8s/` et `infra/verify_k8s.py`, rendus hors cluster seulement.
- CI : `.github/workflows/verify.yml`, `.gitlab-ci.yml`, candidats non exécutés à distance.
- Exploitation : `scripts/probe.py`, `scripts/recovery_lab.py`, contrôles et preuves sous `evidence/`.

La présente passe documentaire ne supprime, déplace, corrige ni exécute aucun de ces éléments. Elle conserve les chemins rapportés et les preuves présentes ; elle ne recrée pas les configurations absentes. Les configurations Terraform ne créaient que des contrats locaux ; les rendus Ansible écrivaient des fichiers localhost ; aucun provisioning Rocky/KVM/cloud ou cluster K3s n’était reçu.

## Usage pédagogique honnête

Les anciens guides techniques sont balisés comme références Codex, avec contexte historique. Ils peuvent aider après la première tentative, mais Mathias décide de son architecture et écrit ses propres fichiers. Les résultats V4.2 ne renseignent pas son niveau : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée sur une tâche nouvelle.

Le défaut `ci-business.json`/`business-smoke.json` du candidat CI est documenté pour son diagnostic personnel, sans reconstruction du pipeline par Codex. Les preuves de reprise sont historiques et n’imposent pas leurs durées comme objectifs de production.
