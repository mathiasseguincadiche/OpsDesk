# OpsDesk — un service de tickets pour apprendre l’InfraOps

## Parcours actif et laboratoire personnel

Commencer par [l’exercice personnel V4.4 n° 1 — comprendre l’application](docs/apprentissage/01-application.md) et [le contrat applicatif](docs/contrat-applicatif.md). Les [13 exercices prioritaires](docs/apprentissage/README.md) sont distincts des supports théoriques et preuves historiques conservés. Les corrigés se consultent après une tentative ; les cinq évaluations personnelles sont dans `docs/apprentissage/evaluations.md`.

Le laboratoire prévu est **Fedora 45 hôte → KVM/QEMU/libvirt → Rocky Linux 10.2 invité**. Les exercices 01/02 se font en lecture et dessin ; pour la préparation technique, lire [le guide de laboratoire et ses contrôles](docs/laboratoire-fedora-kvm-rocky.md). Aucune compatibilité, installation ou VM personnelle n’est validée par les essais historiques Ubuntu/WSL de Codex. Une version ou un contrôle non vérifié reste signalé ; aucune substitution silencieuse de Rocky Linux n’est autorisée.

GitHub est l’unique plateforme active de ce parcours. GitLab est laissé en l’état ; ses anciennes références sont historiques et facultatives, sans synchronisation ni second flux quotidien.

Un collaborateur ouvre une demande IT, l’équipe la consulte, la prend en charge puis la clôture. OpsDesk fournit une petite interface web, une API et une persistance PostgreSQL pour rendre ce parcours vérifiable.

**V4.4 : application et tests fournis par Codex ; infrastructure à concevoir et réaliser personnellement par Mathias.** Les anciennes configurations et preuves V4.2 sont conservées comme références assistées. Elles ne valident aucune compétence personnelle.

![Présentation : application fournie et travail personnel réservé](docs/diagrams/presentation.svg)

## Commencer

Lire le [contrat applicatif autonome](docs/contrat-applicatif.md), puis le [parcours personnel](docs/parcours-apprentissage.md). Le premier exercice consiste à comprendre les besoins et proposer son propre schéma d’infrastructure. Il ne demande pas de recopier les anciennes recettes.

| Besoin du lecteur | Document |
|---|---|
| Fonctions, dépendances, démarrage dev, ports, variables, schéma, santé, tests et limites | [Contrat de passation](docs/contrat-applicatif.md) |
| Architecture interne et référence du laboratoire Codex | [Architecture et frontières](docs/architecture.md) |
| Résultats actuels et preuves historiques | [État de réception](STATUS.md) · [Preuves](docs/preuves.md) |
| Authentification absente et contrôles applicatifs | [Sécurité](docs/securite.md) |
| Qui a produit quoi ; anciennes solutions et travail réservé | [Provenance](docs/provenance.md) |
| Objectifs des trois projets et prochaines étapes personnelles | [Feuille de route](ROADMAP.md) · [Notion OpsDesk](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) |

## Application disponible

Pages `/tickets` et `/tickets/<id>`, API `/api/tickets`, statuts ouvert → en cours → clôturé, données fictives durables dans PostgreSQL. La version, la santé et des métriques simples sont exposées. Python/Flask, psycopg et Gunicorn sont verrouillés dans `requirements.lock` ; le schéma métier initial est séparé dans `db/schema.sql`.

Les tests de la source V4.4 couvrent règles, formulaires, CSRF, SQL réel, refus HTTP, Host, santé/version et relecture d’un ticket committé par une autre connexion. [Résultat et contexte des tests](evidence/v44/application-tests.json). Les tests ponctuels réutilisent le développement existant ; aucun déploiement, exercice de reprise, Terraform, Ansible, K3s ou CI n’est réalisé sous V4.4.

## Limites

**Pas d’authentification utilisateur : démonstrateur local, données fictives uniquement.** La session signe un jeton de formulaire ; elle n’est pas un compte. Aucun usage public ou production n’est autorisé par cette réception. Les alertes historiques de sécurité de l’image restent à examiner ; un parcours métier réussi ne les efface pas. Pas de gestion ITSM complète, affectation, commentaire ou pièce jointe.

Les deux familles de schémas sont distinctes et modifiables : [présentation draw.io](docs/diagrams/presentation.drawio) / [SVG](docs/diagrams/presentation.svg), [technique draw.io](docs/diagrams/architecture-technique.drawio) / [SVG](docs/diagrams/architecture-technique.svg). Le schéma technique décrit le laboratoire de développement Codex ; il ne constitue pas l’architecture personnelle déjà réalisée de Mathias.

[GitHub](https://github.com/mathiasseguincadiche/OpsDesk) · [GitLab](https://gitlab.com/mathias.seguincadiche/OpsDesk) · [MIT](LICENSE). Aucun résultat distant CI n’est déduit de la présence des anciens fichiers.
