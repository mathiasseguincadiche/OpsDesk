# Parcours d'apprentissage OpsDesk

L'application et ses tests sont fournis ; l'infrastructure est à construire soi-même, exercice par exercice. Ces 13 exercices mènent d'une application qui tourne en local à un service déployé par du code, livré par une CI, supervisé, sauvegardé et diagnostiqué.

Mise à jour : 18 novembre 2026, pour la version 2 d'OpsDesk (FastAPI, React, PostgreSQL ; Podman et Quadlet en production).

## Deux niveaux de lecture

| Où | Ce qu'on y trouve | Pour qui |
| --- | --- | --- |
| **Ici, dans le dépôt** | L'énoncé de référence de chaque exercice : objectif, notions clés, état voulu, livrable, vérifications, pièges | Tout lecteur, sans compte |
| **Centre de formation Notion** (accès sur invitation) | Le cours complet : explications pas à pas, exemple travaillé sur un autre cas, indices progressifs, suivi personnel | La personne qui fait le parcours |

Les deux décrivent les mêmes exercices, avec les mêmes livrables et les mêmes vérifications. En cas d'écart, les décisions du [registre](../architecture.md#décisions-retenues) et la [référence technique](../reference-technique.md) font foi.

## Les 13 exercices

| N° | Exercice | Pilier | Schéma |
| --- | --- | --- | --- |
| 01 | [Comprendre OpsDesk : HTTP, API et PostgreSQL](01-application.md) | Construire | [Architecture](../diagrams/architecture.svg) |
| 02 | [Architecture et décisions techniques](02-architecture.md) | Construire | [Architecture](../diagrams/architecture.svg) |
| 03 | [Rocky Linux, machines virtuelles, réseau et SSH](03-linux-reseau.md) | Construire | [Accès SSH](../diagrams/pedagogique-acces-ssh.svg) |
| 04 | [Terraform : provider, ressources, state et cycle de vie](04-terraform.md) | Automatiser | [Cycle Terraform](../diagrams/pedagogique-terraform.svg) |
| 05 | [Ansible : configurer un serveur de façon répétable](05-ansible.md) | Automatiser | [Ansible](../diagrams/pedagogique-ansible.svg) |
| 06 | [Déployer OpsDesk avec Podman et Quadlet](06-conteneurs.md) | Livrer | [Quadlet](../diagrams/pedagogique-quadlet.svg) |
| 07 | [Kubernetes avec K3s : une copie d'essai d'OpsDesk](07-k3s.md) | Livrer | [K3s](../diagrams/pedagogique-k3s.svg) |
| 08 | [CI/CD avec GitHub Actions : tester, construire, publier](08-cicd.md) | Livrer | [CI/CD](../diagrams/pedagogique-cicd.svg) |
| 09 | [Superviser avec Prometheus et Grafana](09-supervision.md) | Observer | [Supervision](../diagrams/pedagogique-supervision.svg) |
| 10 | [Maintenir en service : préparer, intervenir, vérifier](10-maintenance.md) | Maintenir | [Architecture](../diagrams/architecture.svg) |
| 11 | [Sauvegarder et restaurer : prouver la reprise des tickets](11-sauvegarde-reprise.md) | Maintenir | [Sauvegarde](../diagrams/pedagogique-sauvegarde.svg) |
| 12 | [Diagnostiquer et rétablir : un incident de bout en bout](12-diagnostic.md) | Observer | [Architecture](../diagrams/architecture.svg) |
| 13 | [Démontrer son autonomie sur une tâche nouvelle](13-autonomie.md) | Transverse | — |

L'ordre des exercices suit les dépendances techniques : chaque exercice s'appuie sur les précédents. L'exercice 07 (K3s) précède l'exercice 08 (CI) : les images sont alors chargées à la main dans K3s.

## Le laboratoire

Hôte **Fedora 45** avec KVM, QEMU et libvirt ; trois VM **Rocky Linux 10.2** sur le réseau `opsdesk-lan` : `srv-admin` (pilotage), `srv-app` (service réel), `srv-k3s` (copie d'essai et supervision). Les exercices 01 et 02 se font sans VM. La préparation suit le [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md).

## Règles communes

- **Lire avant de lancer.** Avant une commande : sur quelle machine, sous quel compte, avec quel effet attendu, et comment revenir en arrière.
- **Ne pas affaiblir les protections.** SELinux reste `Enforcing`, firewalld reste actif ; on cherche la règle précise.
- **Ne jamais exposer de secret.** Ni dans le dépôt, ni dans les preuves, ni dans les captures.
- **Tester sur la copie, pas sur le service réel**, sauf intervention préparée (exercice 10).
- **Un exemple n'est pas une solution.** Chaque fiche Notion montre un cas voisin ; l'exercice demande d'écrire sa propre configuration.

<a id="preuve-et-progression-personnelles"></a>

## Preuve et progression personnelles

Un exercice compte quand ses vérifications ont été menées et consignées avec leur date, leur sortie réelle et l'aide reçue. Une sortie type (illustration) n'est jamais une preuve.

| Niveau | Signification |
| --- | --- |
| L0 — Découverte | Savoir ce qu'est l'outil et à quoi il sert |
| L1 — Compréhension | Prévoir ce qu'une commande va faire avant de la lancer |
| L2 — Réalisation personnelle | L'avoir mis en œuvre soi-même, avec une fiche |
| L3 — Autonomie vérifiée | L'avoir appliqué à un cas nouveau, vérifié séparément (exercice 13) |

Aide déclarée : A0 (documentation officielle), A1 (ressources générales), A2 (indice ciblé), A3 (solution partielle comprise et adaptée).

**État au 18 novembre 2026 :** aucun exercice réalisé ; aucun niveau attribué.

## Corrigés et évaluations

- [Les repères de correction](corriges.md), à lire **après** ta tentative : réponses attendues, contenu d'une bonne solution, points à refuser. Aucun fichier d'infrastructure complet n'y est fourni.
- [Les cinq évaluations transversales](evaluations.md), une par pilier, qui enchaînent plusieurs exercices sur un scénario complet.
