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
- Terraform crée les machines, Ansible les configure, Docker Engine et Compose y font tourner l'application.

## Ce qu'il faut obtenir

L'état voulu sur `srv-app`, préparé pour l'exercice 06 :

1. `podman` et `runc` sont absents, comme le demande la [procédure officielle de Docker](https://docs.docker.com/engine/install/rhel/) ;
2. le dépôt de Docker pour RHEL est déclaré, et les paquets `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin` et `docker-compose-plugin` sont installés ;
3. le service `docker` est actif et démarre au boot ;
4. aucun compte n'appartient au groupe `docker` ([décision du 18 novembre 2026](../architecture.md#décisions-retenues)) ;
5. le dossier `/opt/opsdesk` existe, propriété de root, droits `0750` ;
6. le port `8080/tcp` est ouvert de façon permanente dans firewalld. Tu verras à l'exercice 06 que cette règle ne suffit pas à décrire l'exposition réelle d'un port publié par Docker.

**Livrable** : `inventory.ini`, le playbook, la sortie de deux passages successifs, et les vérifications ci-dessous.

## Vérifications

| Ce que tu vérifies | Commande sur `srv-app` | Résultat attendu |
| --- | --- | --- |
| Docker | `docker --version` ; `docker compose version` | Une version de Docker Engine, puis du plugin Compose |
| Service | `systemctl is-active docker` ; `systemctl is-enabled docker` | `active`, `enabled` |
| Moteur fonctionnel | `sudo docker run --rm hello-world` | Le message de bienvenue |
| Groupe | `getent group docker` | Aucun membre |
| Dossier | `stat -c '%U %a' /opt/opsdesk` | `root 750` |
| Pare-feu | `sudo firewall-cmd --list-ports` | `8080/tcp` |
| Idempotence | 2ᵉ `ansible-playbook` | `changed=0` |

## Pièges fréquents

| Ce que tu vois | Cause probable |
| --- | --- |
| `UNREACHABLE` | Mauvaise IP, VM éteinte, SSH bloqué : tester SSH seul |
| `Missing sudo password` | Ajouter `-K` |
| `couldn't resolve module ansible.posix.firewalld` | Collection `ansible.posix` absente |
| `changed` à chaque passage | Tâche `command` sans condition |
| Conflit de paquets à l'installation de Docker | `podman` ou `runc` encore présents |
| Clé GPG du dépôt refusée | Clé non importée, ou dépôt d'une autre distribution |

Suite : [exercice 06](06-conteneurs.md).
