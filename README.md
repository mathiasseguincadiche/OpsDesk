# OpsDesk — un service de tickets pour apprendre l’InfraOps

OpsDesk est une application de tickets IT fictifs qui sert de laboratoire pour apprendre l’infrastructure et l’exploitation. Un collaborateur ouvre une demande, le support la consulte, la prend en charge puis la clôture ; PostgreSQL conserve les tickets.

![Le service OpsDesk (navigateur, application Flask, PostgreSQL, volume) et les trois phases du parcours ; les phases 2 et 3 sont à concevoir, non exécutées](docs/diagrams/presentation.svg)

Le schéma présente le service et les trois phases du parcours. Le [schéma technique](docs/diagrams/architecture-technique.svg) décrit le laboratoire historique Codex Ubuntu/WSL ; Mathias concevra son architecture personnelle à l’exercice 02.

**Répartition des responsabilités :** l’application Flask/PostgreSQL, son contrat et ses tests sont fournis comme support de laboratoire. Mathias conçoit, écrit, déploie, vérifie et explique personnellement l’infrastructure et son exploitation. L’origine détaillée des éléments est conservée dans la [provenance](docs/provenance.md) ; les essais historiques ne valent pas réalisation personnelle.

**État réel :** 26 tests applicatifs PASS dans [l’environnement Codex du 3 novembre 2026](evidence/v44/application-tests.json) ; sécurité globale non validée, [triage historique FAIL](docs/triage-securite-v44.md) ; laboratoire Fedora/KVM/Rocky et exercices personnels NON EXÉCUTÉS. **Aucune authentification : usage local et données fictives uniquement, sans exposition Internet.** Les dernières évolutions documentaires et les limites des preuves sont détaillées dans [l’état daté](STATUS.md). Une PR fusionnée ne démontre ni CI exécutée ni infrastructure personnelle déployée.

## Choisir sa lecture

- **Je veux découvrir ou apprendre :** [Notion OpsDesk](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) → [exercice 01 — comprendre l’application](docs/apprentissage/01-application.md) et [contrat applicatif](docs/contrat-applicatif.md), puis [13 exercices dans l’ordre](docs/apprentissage/README.md). Les cinq évaluations sont distinctes ; les corrigés se lisent après tentative.
- **Je veux inspecter ou préparer une reproduction :** [architecture](docs/architecture.md), [état et portée des preuves](STATUS.md), [démarrage actif ou historique](docs/demarrage.md), [runbook](docs/exploitation-day2.md), [sécurité et limites](docs/securite.md). Le démarrage de l’infrastructure reste un travail personnel guidé.

## Laboratoire personnel prévu

Le laboratoire prévu est **Fedora 45 hôte → KVM/QEMU/libvirt → Rocky Linux 10.2 invité**. Les exercices 01/02 se font en lecture et dessin ; pour la préparation technique, lire [le guide de laboratoire et ses contrôles](docs/laboratoire-fedora-kvm-rocky.md). Aucune compatibilité, installation ou VM personnelle n’est validée par les essais historiques Ubuntu/WSL de Codex. Une version ou un contrôle non vérifié reste signalé ; aucune substitution silencieuse de Rocky Linux n’est autorisée.

**Préparer l’environnement est une étape obligatoire, même si les outils semblent déjà installés :** inventorier les versions, services, dépendances et droits ; installer ou corriger uniquement ce qui manque ; vérifier le fonctionnement avec des tests observables et conserver les procédures de diagnostic. Le guide conserve les instructions complètes pour repartir aussi bien d’une VM neuve que d’une VM prééquipée.

GitHub est l’unique plateforme active de ce parcours. GitLab est laissé en l’état ; ses anciennes références sont historiques et facultatives, sans synchronisation ni second flux quotidien.

## Commencer

Lire le [contrat applicatif autonome](docs/contrat-applicatif.md), puis le [parcours personnel](docs/parcours-apprentissage.md). Le premier exercice consiste à comprendre l’application et reformuler ses besoins ; le schéma personnel d’infrastructure appartient à l’exercice 02. Il ne demande pas de recopier les anciennes recettes.

| Besoin du lecteur | Document |
|---|---|
| Fonctions, dépendances, démarrage dev, ports, variables, schéma, santé, tests et limites | [Contrat de passation](docs/contrat-applicatif.md) |
| Architecture interne et référence du laboratoire Codex | [Architecture et frontières](docs/architecture.md) |
| Résultats actuels et preuves historiques | [État de réception](STATUS.md) · [Preuves](docs/preuves.md) |
| Authentification absente et contrôles applicatifs | [Sécurité](docs/securite.md) |
| Qui a produit quoi ; anciennes solutions et travail réservé | [Provenance](docs/provenance.md) |
| Objectifs du projet fil rouge unique et prochaines étapes personnelles | [Feuille de route](ROADMAP.md) · [Notion OpsDesk](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) |

## Repères documentaires

Le parcours personnel reste **V4.4** ; la charte **V5** renforce la traçabilité documentaire. Lire la [portée des preuves](docs/preuves.md#avancement-et-contrôle--deux-informations-distinctes), le [registre des décisions](docs/architecture.md#décisions-durables-et-décisions-encore-personnelles) et la [maintenance des documents](docs/provenance.md#maintenir-les-documents-sans-entretenir-plusieurs-copies). Les schémas possèdent une source `.drawio` modifiable et une version SVG consultable. La correspondance de leurs rendus doit être contrôlée avant publication ; un schéma ne constitue pas une preuve de déploiement.

## Application disponible

Pages `/tickets` et `/tickets/<id>`, API `/api/tickets`, statuts ouvert → en cours → clôturé, données fictives durables dans PostgreSQL. La version, la santé et des métriques simples sont exposées. Python/Flask, psycopg et Gunicorn sont verrouillés dans `requirements.lock` ; le schéma métier initial est séparé dans `db/schema.sql`.

Les tests de la source V4.4 couvrent règles, formulaires, CSRF, SQL réel, refus HTTP, Host, santé/version et relecture d’un ticket committé par une autre connexion. [Résultat et contexte des tests](evidence/v44/application-tests.json). Les tests ponctuels réutilisent le développement existant ; aucun déploiement, exercice de reprise, Terraform, Ansible, K3s ou CI n’est réalisé sous V4.4.

## Limites

**Pas d’authentification utilisateur : démonstrateur local, données fictives uniquement.** La session signe un jeton de formulaire ; elle n’est pas un compte. Aucun usage public ou production n’est autorisé par cette réception. Les alertes historiques de sécurité de l’image restent à examiner ; un parcours métier réussi ne les efface pas. Pas de gestion ITSM complète, affectation, commentaire ou pièce jointe.

Les deux familles de schémas sont distinctes et modifiables : [présentation draw.io](docs/diagrams/presentation.drawio) / [SVG](docs/diagrams/presentation.svg), [technique draw.io](docs/diagrams/architecture-technique.drawio) / [SVG](docs/diagrams/architecture-technique.svg). Le schéma technique décrit le laboratoire de développement Codex ; il ne constitue pas l’architecture personnelle déjà réalisée de Mathias.

[GitHub](https://github.com/mathiasseguincadiche/OpsDesk) · [GitLab — archive historique facultative](https://gitlab.com/mathias.seguincadiche/OpsDesk) · [MIT](LICENSE). Aucun résultat distant CI n’est déduit de la présence des anciens fichiers.
