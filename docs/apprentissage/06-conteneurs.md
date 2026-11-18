# 06 — Déployer OpsDesk avec Podman et Quadlet

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 06, accessible sur invitation. Schéma : [de Quadlet aux services systemd](../diagrams/pedagogique-quadlet.svg).

**Objectif.** Faire tourner OpsDesk sur `srv-app` : trois conteneurs gérés par systemd, sans root, qui redémarrent seuls et gardent leurs données, puis rendre ce déploiement rejouable avec un rôle Ansible.

**Durée estimée** : 4 à 6 heures, en deux séances. **Prérequis** : `srv-app` préparée par le playbook de l'exercice 05. **État** : prévu, non vérifié.

## Pourquoi

`podman compose up` suffit en local. Sur un serveur, il faut que les conteneurs redémarrent au boot et après un arrêt, sans session ouverte, avec des journaux centralisés. C'est le rôle de systemd ; Quadlet fait le pont avec Podman.

## L'essentiel à comprendre

- Une image contient le programme ; un conteneur l'exécute ; un volume garde les données quand le conteneur disparaît.
- Quadlet transforme des fichiers `.container`, `.volume` et `.network` de `~/.config/containers/systemd/` en services systemd, à chaque `systemctl --user daemon-reload`.
- Le conteneur est recréé à chaque démarrage du service : tout ce qui dure va dans un volume.
- Les conteneurs tournent sous `opsdesk` ; pour agir sous ce compte : `sudo -iu opsdesk`, puis `export XDG_RUNTIME_DIR=/run/user/$(id -u)`.
- Les secrets passent par des secrets Podman et les variables `*_FILE`, jamais dans les fichiers.
- Contraintes imposées par l'application : voir la section [Déployer avec Podman et Quadlet](../reference-technique.md#déployer-avec-podman-et-quadlet) de la référence technique (nom `backend` de l'API, `HealthCmd=` car le format OCI ignore `HEALTHCHECK`).

## Ce qu'il faut obtenir

1. **Les images** construites sur `srv-app` à partir des sources, avec un tag de version (chemin temporaire prévu au registre tant qu'aucune image n'est publiée).
2. **Les unités**, sous `opsdesk` : un réseau, un volume PostgreSQL, trois conteneurs (`opsdesk-db`, `opsdesk-api`, `opsdesk-web`) avec chacun un test de santé, trois secrets Podman, et seul `opsdesk-web` publiant un port (8080).
3. **Une décision écrite** sur l'emplacement du volume de PostgreSQL : stockage par défaut de Podman, ou disque de données de 10 Go (point « à revoir » du registre).
4. **Un rôle Ansible**, lancé depuis `srv-admin`, qui dépose les unités, crée les secrets manquants et démarre les services ; second passage à `changed=0`.

**Livrable** : unités et rôle (sans secret), la décision sur le stockage, les preuves datées ci-dessous.

## Vérifications

| Ce que tu vérifies | Commande | Résultat attendu |
| --- | --- | --- |
| Services actifs | `systemctl --user is-active opsdesk-db opsdesk-api opsdesk-web` | Trois `active` |
| Conteneurs sains | `podman ps` | Trois `(healthy)` |
| Service joignable | `curl -i http://192.168.150.10:8080/health/ready` depuis `srv-admin` | `200`, `"database":"up"` |
| Parcours complet | `python3 scripts/smoke.py http://192.168.150.10:8080` | `ALL GOOD` |
| Persistance | Ticket témoin relu après redémarrage des services | Identique |
| Reboot | `sudo systemctl reboot`, sans ouvrir de session `opsdesk` | Tout revient seul |
| Aucun secret en clair | `grep -ri password ~/.config/containers/systemd/` | Seulement des `*_FILE` |
| Idempotence du rôle | 2ᵉ passage | `changed=0` |

## Pièges fréquents

`Failed to connect to bus` (`XDG_RUNTIME_DIR` absent) ; unité introuvable après `daemon-reload` (lire `/usr/libexec/podman/quadlet -dryrun -user`) ; `502` sur `/api` (nom `backend` manquant) ; jamais `(healthy)` (pas de `HealthCmd=`) ; services arrêtés à la déconnexion (lingering absent).

Suite : [exercice 07](07-k3s.md).
