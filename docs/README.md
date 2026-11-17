# Documentation OpsDesk

Le [README du projet](../README.md) donne la vue d’ensemble. Choisir la référence selon le travail à réaliser.

## Comprendre

| Document | Ce qu’il permet de comprendre |
| --- | --- |
| [Contrat applicatif](contrat-applicatif.md) | Besoin métier, API, paramètres, dépendances |
| [Architecture](architecture.md) | Trois VM, flux, décisions et limites |
| [Schémas](diagrams/README.md) | Deux vues, sources Draw.io et contrôles |

## Préparer et pratiquer

1. [Exercice 01 — Comprendre l’application](apprentissage/01-application.md) et [02 — Architecture](apprentissage/02-architecture.md), sans installation.
2. [Installation des outils et préparation du laboratoire](laboratoire-fedora-kvm-rocky.md) avant l’exercice 03.
3. [Parcours personnel — 13 exercices](apprentissage/README.md) : ordre unique.
4. [Évaluations](apprentissage/evaluations.md) et [corrigés](apprentissage/corriges.md) après une tentative.

## Exploiter et vérifier

| Objectif | Point d’entrée actif |
| --- | --- |
| Écrire l’infrastructure | [Terraform](apprentissage/04-terraform.md) · [Ansible](apprentissage/05-ansible.md) |
| Livrer | [Podman](apprentissage/06-conteneurs.md) · [K3s](apprentissage/07-k3s.md) · [CI/CD](apprentissage/08-cicd.md) |
| Observer et maintenir | [Supervision](apprentissage/09-supervision.md) · [Maintenance](apprentissage/10-maintenance.md) |
| Rétablir | [Sauvegarde et reprise](apprentissage/11-sauvegarde-reprise.md) · [Diagnostic](apprentissage/12-diagnostic.md) |
| Évaluer les risques | [Sécurité](securite.md) · [Triage de l’image historique](triage-securite.md) |

[État et contrôle](../STATUS.md) · [Preuves](preuves.md) · [Provenance](provenance.md) · [Versions](versions.md) · [Références InfraOps](references-infraops.md)

## Références historiques

Les anciennes recettes Ubuntu/WSL2 et Compose restent consultables, mais leurs fichiers d’infrastructure ne sont plus présents et elles ne constituent pas des guides actifs. Accéder à leur [index historique](historique.md), au [scénario de démonstration](demonstration.md) et aux preuves associées.

Le laboratoire actuel reste à construire et à vérifier. Aucun résultat personnel ne découle de la seule lecture.
