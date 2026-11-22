# Documentation d'OpsDesk

Le socle applicatif est fourni et qualifié sur un runner jetable. L'infrastructure personnelle reste à construire. Pour distinguer une cible prévue d'une réalisation vérifiée, consulter [STATUS.md](../STATUS.md).

## Choisir son parcours de lecture

- **Découvrir** : lire le [README](../README.md), puis le [statut vérifié](../STATUS.md) pour distinguer le socle fourni, les réalisations personnelles et les objectifs.
- **Apprendre** : suivre le [parcours de 13 exercices](apprentissage/README.md) et préparer les outils avec le [guide du laboratoire](laboratoire-fedora-kvm-rocky.md).
- **Exploiter ou auditer** : confronter le [contrat applicatif](contrat-applicatif.md), les [décisions](architecture.md) et la [référence technique](reference-technique.md), puis lire [l'exploitation](exploitation-day2.md) et la [reprise](reprise.md).

Ces chemins guident la lecture : ils ne valident pas l'infrastructure prévue.

## Découvrir et comprendre

- [Présentation du projet](../README.md) — finalité, contribution personnelle, aperçu et architecture.
- [Contrat applicatif](contrat-applicatif.md) — besoins techniques, flux, données, contraintes et critères de réception.
- [Architecture et décisions](architecture.md) — choix, alternatives, compromis et conditions de réexamen.
- [Schémas](diagrams/README.md) — vues de présentation, architecture globale et détaillée, illustrations pédagogiques.

## Essayer et apprendre

- [Démarrage local](demarrage.md) — prérequis, configuration, lancement, contrôle et arrêt sans suppression du volume.
- [Le parcours des 13 exercices](apprentissage/README.md) — ordre de travail, critères et progression.
- [Compétences et axes professionnels](parcours-apprentissage.md) — lien entre les exercices, les responsabilités et les preuves.
- [Préparer Fedora, KVM et Rocky Linux](laboratoire-fedora-kvm-rocky.md) — outils et contrôles avant le laboratoire.
- [Centre de formation Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) — cours détaillés et suivi personnel, accessible sur invitation.
- [Évaluations transversales](apprentissage/evaluations.md) — exercices de synthèse. [Corrigés](apprentissage/corriges.md) : à lire après une tentative personnelle.

## Exploiter et diagnostiquer

- [Référence technique](reference-technique.md) — ports, configuration, tests et contraintes de déploiement.
- [Exploitation courante](exploitation-day2.md) — opérations, contrôles et limites.
- [Sauvegarde et reprise](reprise.md) — diagnostic, protection des données et restauration.
- [Sécurité](securite.md) — risques, protections et contrôles attendus.

## Qualité du dépôt et modèles

- [Charte universelle GitHub InfraOps](CHARTE_GITHUB.md) — identité, sept modèles, architecture documentaire et critères de recette.
- [Bibliothèque de modèles](templates/README-PROJET.md) — point d'entrée vers les gabarits versionnés.
- [Contribuer](../CONTRIBUTING.md) — branches, tests, PR et preuves.
- [Politique de sécurité](../SECURITY.md) — périmètre du laboratoire et signalement.
- [Journal des changements](../CHANGELOG.md) — historique publiable distinct de la qualification.
- [Inventaire de références historiques](references-infraops.md) — anciennes sources absentes de la branche active ; pas un guide de cours.

## Évaluer et contribuer

- [État et preuves](../STATUS.md) — résultats datés et périmètre de qualification.
- [Méthode de preuve](preuves.md) — distinguer résultat, hypothèse et objectif.
- [Feuille de route](../ROADMAP.md) — travaux et dépendances.
- [Préparer une démonstration](demonstration.md) — présenter les résultats sans revendiquer les travaux futurs.
- [Provenance et sources de vérité](provenance.md) — origine des livrables, responsabilités et maintenance.
- [Contribuer ou reprendre le projet](../README.md#contribuer-ou-reprendre-le-projet) — reproduction, branche, contrôle et preuve.

Les [archives v1](../legacy/) restent accessibles pour l'historique ; elles ne sont pas le parcours actif. Les résultats personnels sont suivis dans Notion, non dans un second journal GitHub.
