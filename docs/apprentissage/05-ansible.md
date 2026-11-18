# 05 — Ansible : configurer un serveur de façon répétable

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 05, accessible sur invitation. Schéma : [comment Ansible rend un serveur conforme](../diagrams/pedagogique-ansible.svg).

**Objectif.** Préparer un serveur Linux automatiquement, de façon répétable et vérifiable.

**Durée estimée** : 2 à 3 heures. **Prérequis** : `srv-admin` et `srv-app` créées (exercice 04), SSH fonctionnel entre les deux. **État** : prévu, non vérifié.

## Pourquoi

Une vingtaine de commandes tapées à la main ne se rejouent pas de mémoire trois mois plus tard. Un playbook garde une trace exacte et rejouable de ce qu'un serveur doit contenir.

## L'essentiel à comprendre

- Ansible décrit l'**état voulu** d'un serveur dans un playbook YAML et l'applique par SSH, sans agent : seul Python est nécessaire sur la cible.
- Chaque tâche répond `ok` (déjà conforme), `changed` (corrigé) ou `failed`.
- Un second passage à `changed=0` montre l'idempotence ; il ne prouve pas que le service fonctionne : on vérifie sur le serveur.
- Les modules `command` et `shell` répondent `changed` à chaque fois, sauf condition (`creates`, `changed_when`).
- Terraform crée les machines, Ansible les configure, Podman et Quadlet y font tourner l'application.

## Ce qu'il faut obtenir

L'état voulu sur `srv-app`, préparé pour l'exercice 06 :

1. le paquet `podman` est installé ;
2. le compte de service `opsdesk` existe ([décision du 18 novembre 2026](../architecture.md#décisions-retenues)) ;
3. ce compte a le lingering de systemd activé ;
4. le port `8080/tcp` est ouvert de façon permanente.

**Livrable** : `inventory.ini`, le playbook, la sortie de deux passages successifs, et les vérifications ci-dessous.

## Vérifications

| Ce que tu vérifies | Commande sur `srv-app` | Résultat attendu |
| --- | --- | --- |
| Podman | `podman --version` | `podman version 5.x` |
| Compte | `id opsdesk` | `uid=… (opsdesk)` |
| Lingering | `loginctl show-user opsdesk -p Linger` | `Linger=yes` |
| Pare-feu | `sudo firewall-cmd --list-ports` | `8080/tcp` |
| Idempotence | 2ᵉ `ansible-playbook` | `changed=0` |

## Pièges fréquents

| Ce que tu vois | Cause probable |
| --- | --- |
| `UNREACHABLE` | Mauvaise IP, VM éteinte, SSH bloqué : tester SSH seul |
| `Missing sudo password` | Ajouter `-K` |
| `couldn't resolve module ansible.posix.firewalld` | Collection `ansible.posix` absente |
| `changed` à chaque passage | Tâche `command` sans condition |

Suite : [exercice 06](06-conteneurs.md).
