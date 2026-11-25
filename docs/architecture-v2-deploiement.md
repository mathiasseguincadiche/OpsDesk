# OpsDesk — Architecture V2 : plan public de réalisation

> **Archive V2 — remplacée le 25 novembre 2026.** [Référence active](architecture-v3-deploiement.md). Les informations ci-dessous ne décrivent plus la cible.

**Architecture validée en conception ; laboratoire Fedora/Rocky non encore qualifié.**

Ce document décrit l'**ordre des travaux et les preuves attendues**, sans publier la procédure opérationnelle. Les inventaires, commandes, ressources détaillées, plan d'adressage, accès, secrets et paramètres de sauvegarde restent dans le dossier technique personnel.

## Phases 0 à 6

| Phase | Objectif public | Validation attendue |
| --- | --- | --- |
| 0 — Fondations | Vérifier le poste, l'hyperviseur, le stockage et les prérequis de sécurité | Capacité, permissions et récupération |
| 1 — Administration | Provisionner et préparer l'environnement d'administration | Accès fonctionnels, configuration reproductible |
| 2 — Machines applicatives | Provisionner les workloads et appliquer le durcissement | Séparation des rôles, tests d'accès, idempotence |
| 3 — Livraison | Construire, identifier et installer une version applicative | HTTPS, santé du service, persistance et retour arrière |
| 4 — Reprise | Mettre en place les sauvegardes indépendantes | Restauration isolée et mesure de récupération |
| 5 — Supervision et essai | Installer l'observabilité et la copie de validation | Alertes effectives et tests sans impact sur le principal |
| 6 — Qualification | Consolider les preuves de bout en bout | Conformité, reconstruction, restauration et supervision |

## Quatre épreuves finales

1. Configuration conforme et reproductible.
2. Reconstruction du laboratoire sur une cible jetable.
3. Restauration d'une copie protégée indépendante.
4. Supervision, alertes et essai de charge sur la copie isolée.

Le passage d'une phase à l'autre dépend des preuves obtenues, non de la seule présence des fichiers ou des commandes.

## Limites et confidentialité

Les étapes d'administration, secrets, identités et tests de sécurité détaillés ne sont pas inclus dans le dépôt public. Les documents de conception publics ne constituent pas une preuve de déploiement.

[Registre public des ADR](adr/README.md) · [État du projet](../STATUS.md)
