# Documentation technique d'OpsDesk

Le présent dossier documente le **produit** : son contrat, son architecture, sa mise en route, son exploitation, sa sécurité et les preuves associées. Les cours, exercices, corrigés, évaluations et modèles personnels sont dans le [wiki Notion OpsDesk](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) et ne constituent pas la documentation publique de ce dépôt.

## Comprendre le produit

- [Contrat applicatif](contrat-applicatif.md) — besoins métier, utilisateurs, API, stockage et critères de réception.
- [Architecture et décisions](architecture.md) — composants, réseaux, alternatives et compromis.
- [Schémas techniques](diagrams/README.md) — présentation, flux, frontières et sources Draw.io.
- [Provenance](provenance.md) — origine du socle, contributions et limites.

## Installer et exploiter

- [Démarrage local](demarrage.md) — prérequis, commandes de lancement, vérifications et arrêt.
- [Référence technique](reference-technique.md) — variables, ports, sondes, métriques et tests.
- [Exploitation courante](exploitation-day2.md) — contrôles, maintenance et diagnostic.
- [Reprise](reprise.md) — sauvegarde, diagnostic et restauration des tickets.
- [Sécurité](securite.md) — protections existantes, risques et exigences de déploiement.

## Qualifier et faire évoluer

- [État réel](../STATUS.md) — avancement, contrôles effectués et limites.
- [Preuves techniques](preuves.md) — comment interpréter les rapports et reproduire les contrôles.
- [Feuille de route technique](../ROADMAP.md) — composants à construire, jalons et conditions de réception.
- [Journal des changements](../CHANGELOG.md) — historique des évolutions.
- [Contribuer](../CONTRIBUTING.md) — changements, tests, sécurité et pull requests.
- [Politique de sécurité](../SECURITY.md) — signalement et périmètre d'utilisation.

Les [sources historiques v1](../legacy/) restent accessibles avec leurs preuves. Aucun résultat v1 ne valide automatiquement la version actuelle ou le laboratoire futur.
