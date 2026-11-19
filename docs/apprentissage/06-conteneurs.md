# 06 — Déployer OpsDesk avec Docker Engine et Compose

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 06, accessible sur invitation. Schéma : [de la définition Compose aux conteneurs](../diagrams/pedagogique-compose.svg).

**Objectif.** Faire tourner OpsDesk sur `srv-app` avec Docker Engine et Compose : trois conteneurs qui redémarrent seuls, gardent leurs données et n'exposent que le nécessaire, sous SELinux et firewalld actifs. Puis rendre ce déploiement rejouable avec un rôle Ansible.

**Durée estimée** : 4 à 6 heures, en deux séances. **Prérequis** : `srv-app` préparée par le playbook de l'exercice 05 (Docker Engine installé depuis son dépôt officiel, service `docker` actif). **État** : prévu, non vérifié.

## Pourquoi

`docker compose up` sur un poste prouve qu'une version démarre. Sur un serveur, il faut davantage : des images figées par leur digest, des secrets hors du fichier, des ports publiés seulement où il faut, des données sur le bon disque, et un service qui revient seul après un redémarrage. Le fichier `compose.yaml` du dépôt est la pile de référence livrée avec l'application ; le fichier de production, c'est toi qui l'écris.

## L'essentiel à comprendre

- **Qui fait quoi.** Le fichier Compose décrit ; la commande `docker compose` le lit et le transmet au démon `dockerd` ; le démon crée réseaux, volumes et conteneurs, que containerd et runc exécutent. systemd ne démarre que le démon.
- **Au redémarrage du serveur**, systemd lance `docker` (s'il est activé), puis Docker relance les conteneurs dont la politique est `unless-stopped`. Un conteneur arrêté à la main avec `docker stop` reste arrêté.
- **Le conteneur est jetable** : tout ce qui doit durer va dans un volume.
- **Le démon tourne en root.** Le groupe `docker` vaut root : personne n'y est ajouté, on administre par `sudo`.
- **Docker gère ses propres règles de pare-feu** : un port publié peut être joignable même s'il n'est pas ouvert dans la zone firewalld. On le prouve depuis une autre machine.
- **SELinux ne s'applique aux conteneurs que si le démon l'active** (`"selinux-enabled": true` dans `/etc/docker/daemon.json`). Un dossier monté depuis le serveur doit porter le bon contexte (`:Z`).
- **Les secrets** passent par le bloc `secrets:` de Compose et les variables `*_FILE`, jamais dans le fichier Compose.
- Les contraintes imposées par l'application et par Docker sont dans la [référence technique](../reference-technique.md#déployer-avec-docker-compose-sur-un-serveur).

## Ce qu'il faut obtenir

1. **Les images** : construites sur `srv-app` à partir des sources avec un tag de version, tant que la CI ne publie rien (chemin temporaire prévu au registre). Après l'exercice 08, elles sont tirées de GHCR par digest.
2. **Le fichier Compose de production**, dans `/opt/opsdesk`, avec :
   - les trois services ;
   - deux réseaux, la base n'étant pas joignable depuis nginx ;
   - un volume pour PostgreSQL ;
   - une sonde de santé et une politique de redémarrage par service ;
   - la rotation des journaux ;
   - trois secrets en fichiers ;
   - un seul port publié vers les utilisateurs (8080), sur l'adresse de `srv-app`, et le port 8000 pour la seule supervision.
3. **Une décision écrite** sur l'emplacement des données de PostgreSQL : volume nommé dans le dossier de Docker, dossier de Docker déplacé sur le disque de 10 Go, ou montage d'un dossier de ce disque (droits de l'utilisateur `postgres` de l'image et contexte SELinux). C'est le point « à revoir » du registre.
4. **La configuration du démon** (`/etc/docker/daemon.json`) : SELinux activé, rotation des journaux par défaut. Note ce qui change si le fichier est faux : le démon ne démarre plus.
5. **Un rôle Ansible**, lancé depuis `srv-admin`, qui :
   - dépose le fichier Compose et les secrets avec les bons droits ;
   - lance le déploiement avec un module maintenu (`community.docker.docker_compose_v2`) ;
   - contrôle `/health/ready`.

   Un second passage doit finir à `changed=0`, sans recréer de conteneur.

**Livrable** : le fichier Compose et le rôle (sans secret), `daemon.json`, la décision sur le stockage, les preuves datées ci-dessous.

## Vérifications

| Ce que tu vérifies | Commande | Résultat attendu |
| --- | --- | --- |
| Fichier valide | `sudo docker compose --project-directory /opt/opsdesk config --quiet` | Aucune sortie, code 0 |
| Conteneurs sains | `sudo docker compose --project-directory /opt/opsdesk ps` | Trois `(healthy)` |
| SELinux appliqué | `sudo docker info --format '{{.SecurityOptions}}'` ; `ps -eZ \| grep container_t` | `selinux` présent ; les processus des conteneurs en `container_t` |
| Service joignable | `curl -i http://192.168.150.10:8080/health/ready` depuis `srv-admin` | `200`, `"database":"up"` |
| Ports limités | Depuis `srv-admin` : port 8000, puis 5432 | Refusés ; 8000 accepté depuis `srv-k3s` seulement |
| Parcours complet | `python3 scripts/smoke.py http://192.168.150.10:8080` | `ALL GOOD` |
| Persistance | Ticket témoin relu après `docker compose down` puis `up` | Identique |
| Reboot | `sudo systemctl reboot`, sans aucune commande ensuite | Tout revient seul, ticket témoin intact |
| Aucun secret en clair | `grep -ri password /opt/opsdesk/compose.yaml` | Seulement des `*_FILE` |
| Personne dans le groupe `docker` | `getent group docker` | Aucun membre |
| Idempotence du rôle | 2ᵉ passage | `changed=0`, conteneurs non recréés (même `Created` dans `docker inspect`) |

## Pièges fréquents

- **`permission denied` sur le socket Docker** : c'est voulu, utilise `sudo`, pas le groupe `docker`.
- **PostgreSQL refuse son dossier de données** : mauvais propriétaire ou contexte SELinux sur un montage. Lire `sudo ausearch -m avc -ts recent`, puis corriger le contexte du seul dossier concerné, sans désactiver SELinux.
- **L'API ne lit pas son secret** : fichier illisible par l'UID 10001.
- **Port 8000 joignable depuis toutes les machines** : publié sur `0.0.0.0` ; Docker contourne la zone firewalld.
- **`502` sur `/api`** : service de l'API renommé, sans adapter `BACKEND_URL`.
- **Rien ne revient après un reboot** : `systemctl is-enabled docker` à `disabled`.
- **Le rôle recrée les conteneurs à chaque passage** : un modèle qui change à chaque exécution, une date ou un ordre de clés par exemple.

Suite : [exercice 07](07-k3s.md).
