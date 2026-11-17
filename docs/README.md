# Documentation OpsDesk

Choisir un point d’entrée selon son objectif. Le [README](../README.md) présente le projet ; ce guide oriente vers les références existantes sans les dupliquer.

## Comprendre

| Document | Utilité |
| --- | --- |
| [Contrat applicatif](contrat-applicatif.md) | Besoin métier, API, dépendances, paramètres et garanties |
| [Architecture](architecture.md) | Cible retenue et décisions techniques |
| [Schémas](diagrams/README.md) | Présentation, architecture technique et sources Draw.io |

## Préparer et pratiquer

1. [Parcours et 13 exercices personnels](apprentissage/README.md) — ordre de travail unique.
2. [Installation des outils et préparation du laboratoire](laboratoire-fedora-kvm-rocky.md) — Fedora, KVM/libvirt, Rocky, précontrôles et compatibilités.
3. [Exercice 01](apprentissage/01-application.md) — comprendre le service sans VM.
4. [Évaluations](apprentissage/evaluations.md) et [corrigés](apprentissage/corriges.md) — après tentative personnelle.

## Références techniques

| Domaine | Référence |
| --- | --- |
| Infrastructure | [Infrastructure](infrastructure.md) |
| Livraison et chaîne CI/CD | [Livraison](livraison.md) · [CI/CD](cicd.md) |
| Exploitation et reprise | [Maintenance](exploitation-day2.md) · [Reprise](reprise.md) |
| Sécurité | [Sécurité](securite.md) · [Triage](triage-securite.md) |
| Versions et concepts | [Versions](versions.md) · [Références InfraOps](references-infraops.md) |

Les références peuvent inclure des recettes historiques. Les indications de cible et de validité de chaque fichier priment : ne pas exécuter une recette historique ou non qualifiée comme un guide actif.

## État et traçabilité

[STATUS.md](../STATUS.md) est la référence d’avancement et de contrôle ; [preuves.md](preuves.md) précise la méthode et les limites des observations. [Provenance](provenance.md) distingue l’application fournie, les éléments historiques et le travail personnel. [Démonstration](demonstration.md) et [démarrage historique](demarrage.md) à consulter comme références, en respectant leur périmètre.

Le projet est réservé au laboratoire : aucune authentification et aucun déploiement d’infrastructure personnel vérifié.
