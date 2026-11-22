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

## Comprendre le mécanisme et ses limites

**Pourquoi trois contrôles différents ?** Un conteneur `healthy` prouve seulement que sa sonde répond ; un `curl` depuis `srv-admin` prouve que cette origine atteint l'entrée HTTP ; un ticket relu après recréation atteste la persistance sur la cible observée. Aucun de ces contrôles, isolément, ne prouve la confidentialité des secrets ou le filtrage de toutes les sources. Pour les ports publiés par Docker, tester aussi depuis une machine qui ne devrait pas pouvoir se connecter.

## Ce qu'il faut obtenir

1. **Les images** : construites sur `srv-app` à partir des sources avec un tag de version, tant que la CI ne publie rien (chemin temporaire prévu au registre). Après l'exercice 08, elles sont tirées de GHCR par digest.
2. **Le fichier Compose de production**, dans `/opt/opsdesk`, avec :
   - les trois services ;
   - deux réseaux, la base n'étant pas joignable depuis nginx ;
   - un volume pour PostgreSQL ;
   - une sonde de santé et une politique de redémarrage par service ;
   - la rotation des journaux ;
   - trois secrets distincts en fichiers, avec `SEED_DEMO_DATA=false` et `ALLOW_REGISTRATION=false` sur la cible non démonstrative ; le smoke fourni utilise des comptes de démonstration et doit être exécuté sur une cible jetable dédiée, ou adapté avec des comptes de test autorisés ;
   - un seul port publié vers les utilisateurs (8080), sur l'adresse de `srv-app`, et le port 8000 pour la seule supervision.
3. **Une décision écrite** sur l'emplacement des données de PostgreSQL : volume nommé dans le dossier de Docker, dossier de Docker déplacé sur le disque de 10 Go, ou montage d'un dossier de ce disque (droits de l'utilisateur `postgres` de l'image et contexte SELinux). C'est le point « à revoir » du registre.
4. **La configuration du démon** (`/etc/docker/daemon.json`) : SELinux activé, rotation des journaux par défaut. Valide d'abord le fichier avec `sudo dockerd --validate --config-file=/etc/docker/daemon.json` ; sauvegarde la configuration et prévois le retour arrière. N'expérimente un fichier invalide que sur une VM jetable.
5. **Un rôle Ansible**, lancé depuis `srv-admin`, qui :
   - dépose le fichier Compose et les secrets avec les bons droits ;
   - lance le déploiement avec un module maintenu (`community.docker.docker_compose_v2`) ;
   - contrôle `/health/ready`.

   Un second passage doit finir à `changed=0`, sans recréer de conteneur.

**Livrable** : le fichier Compose et le rôle (sans secret), `daemon.json`, la décision sur le stockage, les preuves datées ci-dessous et celles de l’atelier DNS/TLS.

## Vérifications

| Ce que tu vérifies | Commande | Résultat attendu |
| --- | --- | --- |
| Fichier valide | `sudo docker compose --project-directory /opt/opsdesk config --quiet` | Aucune sortie, code 0 |
| Conteneurs sains | `sudo docker compose --project-directory /opt/opsdesk ps` | Trois `(healthy)` |
| SELinux appliqué | `sudo docker info --format '{{.SecurityOptions}}'` ; `ps -eZ \| grep container_t` | `selinux` présent ; les processus des conteneurs en `container_t` |
| Service joignable | `curl -i http://192.168.150.10:8080/health/ready` depuis `srv-admin` | `200`, `"database":"up"` |
| Ports limités | Depuis `srv-admin` : port 8000, puis 5432 | Refusés ; 8000 accepté depuis `srv-k3s` seulement |
| Parcours complet | Sur une instance jetable avec données fictives : `python3 scripts/smoke.py http://URL-DE-TEST` ; sur srv-app non démonstrative, parcours avec comptes de test autorisés | `ALL GOOD` sur la pile de démonstration ; création et lecture d'un ticket de test sur la cible |
| Persistance | Ticket témoin relu après `docker compose down` puis `up` | Identique |
| Reboot | Après sauvegarde, identification de la VM et accord ciblé, `sudo systemctl reboot` ; observer depuis une autre machine | Tout revient seul, ticket témoin intact |
| Secret accessible par l’API | `sudo docker compose --project-directory /opt/opsdesk exec -T backend sh -c 'test -n "$DB_PASSWORD_FILE" && test -r "$DB_PASSWORD_FILE" && test -s "$DB_PASSWORD_FILE"'` | Code 0, aucune valeur affichée ; répéter pour JWT et admin |
| Personne dans le groupe `docker` | `getent group docker` | Aucun membre |
| Idempotence du rôle | 2ᵉ passage | `changed=0`, conteneurs non recréés (même `Created` dans `docker inspect`) |

## Pièges fréquents

- **`permission denied` sur le socket Docker** : c'est voulu, utilise `sudo`, pas le groupe `docker`.
- **PostgreSQL refuse son dossier de données** : mauvais propriétaire ou contexte SELinux sur un montage. Lire `sudo ausearch -m avc -ts recent`, puis corriger le contexte du seul dossier concerné, sans désactiver SELinux.
- **L'API ne lit pas son secret** : fichier illisible par l'UID 10001.
- **Port 8000 joignable depuis une machine non autorisée** : vérifier les liaisons d’adresse, les règles de filtrage Docker et les tests depuis les sources autorisées et interdites ; une adresse de publication précise ne filtre pas à elle seule les clients.
- **`502` sur `/api`** : service de l'API renommé, sans adapter `BACKEND_URL`.
- **Rien ne revient après un reboot** : `systemctl is-enabled docker` à `disabled`.
- **Le rôle recrée les conteneurs à chaque passage** : un modèle qui change à chaque exécution, une date ou un ordre de clés par exemple.

## Atelier réseau et TLS — partie intégrante de l’exercice

Sur une cible privée et isolée, ajoute un nom `opsdesk.lab` résolu par le DNS du laboratoire (une entrée `hosts` peut servir de comparaison, mais ne prouve pas un DNS fonctionnel). Configure un point d’entrée HTTPS Nginx sur un port dédié, par exemple 8443, avec certificat valable pour ce nom (SAN), signé par une autorité de laboratoire approuvée par le client. N’expose ni la clé ni les données ; garde le point d’entrée HTTP de référence jusqu’à validation. Le choix de l’implantation Nginx et des flux est à justifier, pas à recopier.

**Preuves attendues :** résolution du nom et adresse attendue (`getent ahosts`, interrogation du DNS avec `dig` si disponible), chaîne et nom vérifiés (`openssl s_client` avec SNI et vérification du nom, puis `curl --cacert` sans `-k`), refus d’un certificat non approuvé, réponse `/health/ready` et parcours fonctionnel via HTTPS. Documente les accès autorisés, le retour arrière et le retrait des éléments temporaires. Aucun domaine public ni exposition Internet.

Suite : [exercice 08](08-cicd.md).
