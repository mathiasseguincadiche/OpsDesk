# Apprendre avec OpsDesk

OpsDesk sert de support à un parcours DevOps complet : l'application et ses tests sont fournis, et l'infrastructure se construit soi-même, en 13 exercices. Le détail des exercices, leurs livrables et leurs vérifications sont dans [le parcours d'apprentissage](apprentissage/README.md).

Mise à jour : 18 novembre 2026, pour la version 2 d'OpsDesk.

## L'idée

Chaque exercice part d'un problème réel d'exploitation, explique le mécanisme, montre un exemple sur un cas voisin, puis demande de construire et de **prouver** le résultat. Une configuration écrite ou une coche verte ne suffit pas : on vérifie l'effet réel, et on sait l'expliquer.

## Les cinq piliers

| Pilier | Exercices | La preuve directrice |
| --- | --- | --- |
| Construire | 01, 02, 03 | Le trajet d'une requête compris ; `srv-admin` joignable par clé, protections actives |
| Automatiser | 04, 05 | Les VM recréées par Terraform ; un second passage Ansible à `changed=0` |
| Livrer | 06, 07, 08 | Le service sous Docker Compose qui survit au reboot ; l'image déployée identique à celle vérifiée par la CI |
| Observer | 09, 12 | Une alerte vue passer à `firing` ; un incident inconnu diagnostiqué et rétabli |
| Maintenir | 10, 11 | Une maintenance mesurée avec retour arrière ; une restauration prouvée par un ticket témoin |

L'exercice 13 est transversal : une tâche nouvelle, menée seul, et vérifiée séparément.

## Où se trouve quoi

- **Les énoncés de référence** : [docs/apprentissage/](apprentissage/README.md), lisibles par tous.
- **Le cours complet** (explications, exemples, indices, suivi) : le centre de formation Notion, accessible sur invitation.
- **Les décisions** à respecter : le [registre](architecture.md#décisions-retenues).
- **La préparation du laboratoire** : le [guide Fedora, KVM et Rocky Linux](laboratoire-fedora-kvm-rocky.md).
- **L'état réel**, daté : [STATUS.md](../STATUS.md).

## Les niveaux

L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Ils sont définis dans [le parcours](apprentissage/README.md#preuve-et-progression-personnelles). Aucun niveau n'est attribué à ce jour, et les tests de la version 1 n'en attribuent aucun.
