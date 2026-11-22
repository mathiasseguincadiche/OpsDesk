# Architecture d'OpsDesk — produit et historique

**Architecture d'infrastructure V2 validée en conception :** consulter en priorité le [registre des sept ADR](adr/README.md), la [matrice des flux V2](architecture-v2-flux.md) et le [plan phases 0 à 6](architecture-v2-deploiement.md). Les décisions de déploiement plus anciennes conservées dans ce document sont **historiques et remplacées** lorsqu'elles contredisent ces ADR (par exemple Terraform dans `srv-admin`, HTTP :8080 pour la cible serveur, sauvegardes dans `~/sauvegardes`). Les schémas actuels représentent encore l'ancienne cible et seront remplacés en paire Draw.io/SVG ; voir [STATUS](../STATUS.md).

OpsDesk est une application web en trois parties : une interface, une API et une base de données, chacune dans son conteneur. L'application (version 2) est construite et testée ; l'infrastructure qui doit la faire tourner sur trois machines Rocky Linux est décidée mais pas encore construite. Ce document explique le fonctionnement, puis justifie chaque choix, du plus visible au plus détaillé. L'état de chaque élément est tenu dans [STATUS.md](../STATUS.md) ; les détails d'exploitation sont dans la [référence technique](reference-technique.md).

## Vue d'ensemble

[![Vue d'ensemble de l'architecture d'OpsDesk : sur l'hôte Fedora, un réseau privé relie trois machines prévues. Sur srv-app, nginx (port 8080) transmet /api à l'API, qui lit et écrit dans PostgreSQL, non publié. srv-admin pilote srv-app par SSH, Prometheus sur srv-k3s lit /metrics, et pg_dump copie la base hors de la VM.](diagrams/architecture-globale.svg)](diagrams/architecture.svg)

[Voir le schéma détaillé](diagrams/architecture.svg) : les trois machines, Docker Engine et Compose sur `srv-app`, chaque flux typé avec son port, et ce qui est réalisé ou prévu.

Le navigateur ne parle qu'au **frontend**. Celui-ci sert l'interface et relaie les appels à l'**API**, qui seule accède à la **base**. Sur le schéma, le trait plein montre l'application, testée en conteneurs locaux ; les pointillés montrent l'infrastructure prévue.

## Le trajet d'une requête

Suivre une action de bout en bout aide à comprendre qui fait quoi. Quand un agent du support prend un ticket en charge :

1. **Le navigateur** envoie `POST /api/tickets/6/status` au frontend, avec le jeton de session de l'agent.
2. **nginx** (frontend) reconnaît le préfixe `/api` et relaie la requête à l'API. Il retrouve l'adresse de l'API par son nom sur le réseau, à chaque requête.
3. **L'API** vérifie le jeton et le rôle (seul le support peut prendre un ticket en charge), puis vérifie que la transition est permise (`open` → `in_progress`).
4. **L'API** verrouille la ligne du ticket dans **PostgreSQL**, change son statut, l'assigne à l'agent s'il n'avait pas de responsable, et enregistre deux événements dans l'historique. Tout est validé en une seule transaction.
5. **La réponse** remonte jusqu'au navigateur, qui met à jour la page.

Si la base ne répond pas, l'API renvoie une erreur 503 explicite, et sa sonde `/health/ready` passe en échec : un orchestrateur ou une supervision peut le détecter.

## Les décisions de l'application

<details>
<summary><b>Trois parties séparées, chacune dans son conteneur</b></summary>

- **Problème** : une application de démonstration doit se comporter comme un vrai service, pour que son exploitation ait du sens.
- **Choix** : une interface (React servie par nginx), une API (FastAPI) et une base (PostgreSQL), dans trois conteneurs.
- **Pourquoi** : chaque partie se construit, se met à jour, se surveille et redémarre indépendamment ; c'est l'organisation la plus courante en entreprise, donc la plus utile à apprendre.
- **Alternatives écartées** : un seul conteneur, plus simple mais qui mélange les responsabilités ; des microservices, sans besoin réel à cette taille.
- **Compromis** : trois éléments à configurer, un réseau entre eux.
- **Vérifier** : `docker compose ps` affiche trois services `healthy`, et `scripts/smoke.py` réussit.

</details>

<details>
<summary><b>FastAPI et SQLAlchemy pour l'API</b></summary>

- **Problème** : une API qui valide ses entrées, gère des rôles et documente son contrat.
- **Choix** : FastAPI (Python 3.13), SQLAlchemy 2, psycopg 3.
- **Pourquoi** : validation automatique des données, documentation OpenAPI générée (`/api/docs`), code court et lisible ; SQLAlchemy permet de tester sur SQLite comme sur PostgreSQL.
- **Compromis** : un seul processus par conteneur ; on augmente la capacité en ajoutant des instances, pas des processus.
- **Quand choisir autrement** : fortes contraintes de performance, ou équipe déjà experte d'un autre écosystème.
- **Vérifier** : 28 tests (`backend/tests/`), joués sur PostgreSQL 17.

</details>

<details>
<summary><b>nginx devant l'interface, avec résolution dynamique de l'API</b></summary>

- **Problème** : servir l'interface et donner au navigateur une seule adresse, sans exposer l'API.
- **Choix** : nginx non-root sert les fichiers React et relaie `/api`, `/health` et `/version` ; il bloque `/metrics`.
- **Comment ça fonctionne** : nginx résout le nom de l'API à chaque requête (directive `resolver`, cache de 10 secondes) au lieu de le résoudre une fois au démarrage.
- **Pourquoi ce détail compte** : quand Docker recrée le conteneur de l'API, comme quand Kubernetes relance son pod, l'API peut revenir avec une nouvelle adresse IP. Avec une résolution unique, nginx garderait l'ancienne adresse et répondrait en erreur 502 ; il refuserait même de démarrer si l'API n'existait pas encore.
- **Vérifier** : l'essai du 18 novembre 2026 (API recréée avec une nouvelle adresse, frontend démarré sans API) est consigné dans [STATUS.md](../STATUS.md).

</details>

<details>
<summary><b>Authentification par jeton et trois rôles</b></summary>

- **Problème** : distinguer ce que peut faire un collaborateur, un agent du support et un administrateur.
- **Choix** : connexion par e-mail et mot de passe, jeton JWT signé, trois rôles vérifiés par l'API à chaque requête.
- **Pourquoi** : l'API ne garde aucune session en mémoire, donc plusieurs instances peuvent tourner côte à côte ; c'est le modèle attendu sur une infrastructure conteneurisée.
- **Limites** : pas de renouvellement automatique du jeton, pas d'authentification à deux facteurs ; les données restent fictives et le service ne doit pas être exposé sur Internet.
- **Remplace** la décision v1 « usage local sans authentification » (voir le registre ci-dessous).

</details>

<details>
<summary><b>Observabilité intégrée dès l'application</b></summary>

- **Problème** : pouvoir dire si le service fonctionne, et pourquoi il ne fonctionne pas.
- **Choix** : deux sondes (`/health/live` : le processus répond ; `/health/ready` : la base répond), des métriques Prometheus sur `/metrics`, des journaux JSON avec un identifiant par requête.
- **Pourquoi** : sans ces points d'accès, ni Docker, ni Kubernetes, ni Prometheus ne peuvent juger de l'état du service.
- **Limites** : aucune supervision n'est encore branchée ; les alertes restent à construire (phase 3).

</details>

## L'infrastructure prévue

L'application tourne d'abord en local, puis sur des serveurs créés et configurés par du code. Les phases regroupent les responsabilités ; les jalons techniques et leurs dépendances figurent dans la [feuille de route](../ROADMAP.md).

- **Phase 1, préparer et automatiser :** `srv-admin`, installée à la main, porte Terraform, Ansible, Git, OpenSSH et k6. Depuis elle, Terraform crée `srv-app` et `srv-k3s` par libvirt, et Ansible les configure. Sur `srv-app`, Docker Engine fait tourner les trois conteneurs, décrits dans un fichier Compose ; le port 8080 du frontend est ouvert à l'hôte, à `srv-admin` et à `srv-k3s`, le port 8000 de l'API seulement à `srv-k3s` (supervision), et la base n'est jamais publiée.
- **Phase 2, livrer et conserver :** GitHub Actions lance les tests, construit les images, les analyse avec Trivy et les publie sur GHCR. Ansible, lancé depuis `srv-admin`, déploie la version choisie après contrôle et approbation. La base est sauvegardée chaque nuit par `pg_dump`, copiée hors de la machine, et sa restauration est testée.
- **Phase 3, orchestrer et observer :** sur `srv-k3s`, K3s fait tourner une copie d'essai de l'application, avec Prometheus et Grafana. Prometheus lit les métriques de `srv-app` et de la copie ; l'architecture cible prévoit de restreindre l’accès aux seules métriques et de fermer le port direct de l’API. k6 envoie une charge limitée à la copie, jamais au service réel. Les schémas représentent la cible initiale, pas cette évolution encore à éprouver.

## Docker Compose et K3s

L'application tourne deux fois, sur deux serveurs indépendants.

- **Sur `srv-app`, avec Docker Engine et Compose (phase 1) :** c'est le service réel. Un fichier Compose décrit les trois conteneurs, leurs réseaux, le volume de la base et leurs sondes. systemd démarre le service `docker` au boot ; la politique de redémarrage `unless-stopped` relance ensuite les conteneurs, y compris après un arrêt imprévu. La sauvegarde et la restauration portent sur cette base.
- **Sur `srv-k3s`, avec K3s (phase 3) :** K3s tire les mêmes images sur GHCR et en fait tourner une copie d'essai, avec sa propre base de test (données fictives, non sauvegardées). On y apprend ce qu'un orchestrateur ajoute : sondes, redémarrage, retrait du trafic, mise à jour progressive.

Les deux ne se voient pas. K3s garde son propre moteur, containerd, et ne pilote que ce qu'il lance lui-même : Docker n'y joue aucun rôle. Prometheus, sur `srv-k3s`, lit seulement `/metrics` par le réseau. Les images sont les mêmes (format OCI), donc ce qui s'apprend avec Compose (ports, volumes, variables, secrets, sondes) se retrouve dans K3s, sous d'autres noms.

| Couche | Sur `srv-app` | Sur `srv-k3s` |
| --- | --- | --- |
| Ce qui décrit le service | `compose.yaml` | Manifestes Kubernetes (Deployment, Service, Ingress) |
| Ce qui applique la description | `docker compose` (client) et le démon `dockerd` | Le plan de contrôle de K3s |
| Ce qui fait tourner les conteneurs | containerd et runc, pilotés par `dockerd` | containerd et runc, pilotés par le kubelet |
| Ce qui relance après un arrêt | La politique de redémarrage de Docker | Le kubelet et le Deployment |

**Pourquoi K3s, alors ?** Une seule application sur un seul serveur n'en a pas besoin : Compose suffit. K3s est là pour pratiquer Kubernetes. Avec un seul nœud, il n'apporte pas de haute disponibilité, et la supervision qui y tourne s'arrête avec lui.

## Conditions de réexamen

Ces conditions ne sont pas des exigences supplémentaires pour le laboratoire : elles aident à défendre une décision et à reconnaître ses limites. Réexaminer Compose si un besoin de disponibilité, de placement sur plusieurs nœuds ou de gestion de flotte est démontré ; le K3s mono-nœud actuel ne résout pas à lui seul ces problèmes. Réexaminer le stockage des sauvegardes si la protection contre la perte du poste devient une exigence. Réexaminer le dimensionnement après mesures de charge, et l'état Terraform distant si plusieurs opérateurs doivent travailler ensemble. Dans chaque cas, comparer le risque, le bénéfice, le coût et une méthode de validation avant de modifier la cible. Aucun changement de stack n'est présumé.

## Repères pour lire le registre

Lire d'abord les décisions qui déterminent **où vivent le service et les données, qui prépare les machines, comment une version est livrée et comment revenir en arrière**. Ce tableau est un index, pas une deuxième source de vérité.

| Question | Décision actuelle | Contrôle à prévoir |
| --- | --- | --- |
| Qui prépare l'environnement ? | Fedora et trois VM Rocky ; `srv-admin` pilote les deux autres | Inventaire libvirt, SSH, contrôle des frontières |
| Comment tourne le service ? | Docker Engine/Compose sur `srv-app`, K3s uniquement sur la copie d'essai | Sondes, exposition des ports, parcours de ticket |
| Comment limiter les privilèges ? | Administration Docker par `sudo`, SELinux et firewalld conservés | Droits, contextes et accès depuis sources autorisées/interdites |
| Comment protéger les données ? | Volume, sauvegarde PostgreSQL hors VM, restauration isolée | Ticket témoin restauré, perte et délai mesurés |

Pour chaque choix, chercher ensuite son **alternative, son coût, sa limite et sa condition de réexamen**. Les anciennes décisions restent conservées pour expliquer l'évolution du projet ; elles ne représentent plus la cible active.

## Décisions retenues

« Retenu » est l'état d'une décision, pas la preuve de son exécution. Une décision remplacée reste présente, avec son état et la décision qui la remplace. Les décisions du 12 et du 13 novembre 2026 ont été prises avant toute réalisation : elles restent à revalider avant mise en œuvre.

| Décision et état | Contexte, choix et alternatives | Conséquence et source |
|---|---|---|
| Un dépôt / un service / trois phases — retenu | Le mandat conserve OpsDesk et exclut le retour aux trois anciens dépôts spécialisés | Code et preuves restent ensemble. [Provenance](provenance.md) |
| GitHub seul actif — retenu | GitLab reste une archive facultative ; pas de miroir ni de CI supplémentaire | Évite deux flux à synchroniser |
| Application fournie / infrastructure personnelle — retenu | Établir une responsabilité explicite entre le socle fourni et les configurations d'infrastructure à produire | Aide graduée, effort et preuve personnels ; [provenance](provenance.md) |
| Usage local fictif sans authentification — **remplacée le 17 novembre 2026** par « Authentification par jeton et rôles » | La v1 ne gérait pas de comptes | La v2 ajoute comptes, rôles et jetons ; l'exposition Internet reste exclue (données fictives) |
| Application v2 en trois conteneurs — retenu, vérifié en local le 18 novembre 2026 | Interface React et nginx, API FastAPI, PostgreSQL 17. Écartés : la v1 Flask (pas d'authentification, interface minimale) ; un conteneur unique | Voir « Les décisions de l'application » ci-dessus ; preuves dans [STATUS.md](../STATUS.md) |
| Fedora/KVM/Rocky — cible prévue, réception non vérifiée | Cible personnelle donnée par le mandat | Compatibilités à recevoir ; AWS facultatif. [feuille de route](../ROADMAP.md) |
| Deux serveurs Rocky Linux 10.2 sur l'hôte Fedora — **remplacée le 13 novembre 2026** par « Trois serveurs Rocky Linux 10.2 » | `srv-app` (192.168.150.10 ; 2 vCPU, 4 Go ; 20 Go) portait l'application et la base ; `srv-k3s` (192.168.150.20 ; 2 vCPU, 6 Go ; 30 Go) portait K3s, sa copie d'essai et la supervision ; outils d'infrastructure sur l'hôte. Écartés : une seule VM ; trois VM ou plus, jugées trop gourmandes | Remplacé, pas effacé : `srv-app` et `srv-k3s` gardent rôle, adresse et taille |
| Trois serveurs Rocky Linux 10.2 sur l'hôte Fedora — retenu, non vérifié (13 novembre 2026) | `srv-admin` (192.168.150.5 ; 1 vCPU, 2 Go ; 20 Go) porte Terraform, Ansible, Git, OpenSSH et k6 ; `srv-app` (192.168.150.10 ; 2 vCPU, 4 Go ; 20 Go) porte l'application et la base ; `srv-k3s` (192.168.150.20 ; 2 vCPU, 6 Go ; 30 Go) porte K3s, sa copie d'essai et la supervision. Écartés : outils sur l'hôte Fedora, qui lient la reconstruction au poste ; outils dans `srv-app` ; une seule VM ; un cluster à plusieurs nœuds | Outils d'infrastructure dans un lieu nommé et refaisable ; 12 Go de mémoire pris à l'hôte ; `srv-admin` à protéger (état Terraform, clés SSH). Dimensionnement de `srv-admin` à mesurer, notamment pour k6 |
| Amorçage de `srv-admin` — retenu, non vérifié (13 novembre 2026) | Créée à la main dans virt-manager, une seule fois, sur `opsdesk-lan` ; Terraform ne peut pas créer la VM qui le porte. Une procédure écrite permet de la refaire | Seule étape non automatisée ; sa reproductibilité dépend de la procédure écrite |
| Reprise de `srv-admin` — retenu, non vérifié (13 novembre 2026) | L'état Terraform et les clés SSH sont copiés hors de `srv-admin` (sur l'hôte, hors de Git) ; code et playbooks sont dans GitHub. Si `srv-admin` est perdue : la refaire, y remettre l'état et les clés, relire le plan Terraform avant tout apply | Sans copie de l'état, Terraform voudrait recréer les VM. La copie contient des secrets : chiffrement à décider |
| Réseau, accès et protections — retenu, non vérifié (12 novembre 2026), précisé le 13 novembre 2026, **ports mis à jour le 18 novembre 2026 pour la v2** | Réseau libvirt NAT dédié `opsdesk-lan` (192.168.150.0/24) ; SSH par clé, sans mot de passe ni connexion root ; SELinux Enforcing ; firewalld. `srv-admin` : 22 pour l'hôte seul. `srv-app` : 22 pour `srv-admin` seule, **8080 (frontend) pour l'hôte, `srv-admin` et `srv-k3s`, 8000 (API, métriques) pour `srv-k3s` seule**, 5432 non publié, 9100 pour `srv-k3s`. `srv-k3s` : 22 pour `srv-admin` seule, 80 pour l'hôte et `srv-admin`, 6443 pour l'hôte. Hôte : 22 pour `srv-admin` (libvirt distant) et `srv-app` (copie des sauvegardes). Écartés : le réseau `default` de libvirt ; un pont sur le réseau local ; désactiver SELinux ou le pare-feu | Chaque port ouvert a une raison écrite. La v1 ouvrait le port 8000 de l'application ; en v2, le point d'entrée est le frontend (8080). Les règles du pare-feu de l'hôte restent à vérifier |
| Exécution : Podman et Quadlet — **remplacée le 18 novembre 2026** par « Exécution : Docker Engine et Docker Compose » | **Trois conteneurs** (`opsdesk-db`, `opsdesk-api`, `opsdesk-web`) gérés par des unités systemd, sans root, sous le compte de service `opsdesk` (décision suivante) : fichiers Quadlet dans `~/.config/containers/systemd/`, commandes `systemctl --user`, `loginctl enable-linger` pour démarrer sans session ouverte ; secrets dans des secrets Podman. Écartés : Docker Compose, qui ajoute un démon et s'éloigne des outils natifs ; conteneurs en root | Remplacé, pas effacé. Aucune unité Quadlet n'avait été écrite : rien n'est à migrer sur un serveur |
| Exécution : Docker Engine et Docker Compose — retenu, non vérifié sur serveur (18 novembre 2026) | Sur `srv-app`, Docker Engine et son plugin Compose, installés depuis le dépôt officiel de Docker pour RHEL (qui retire d'abord `podman` et `runc`) ; le service `docker` activé par systemd ; un fichier Compose de production qui tire les images de GHCR par digest, sans rien construire. Raison : orientation InfraOps généraliste, sur les outils les plus répandus en entreprise. Écartés : Podman et Quadlet (décision précédente), plus spécialisés ; Docker sans root (*rootless*), qui protège mieux mais complique réseau, ports et supervision ; des unités systemd autour de Compose, sans besoin réel | Docker est un démon qui tourne en root : appartenir au groupe `docker` revient à être root, donc aucun compte n'y est ajouté. Docker gère lui-même ses règles de pare-feu (zone firewalld `docker`) et n'applique SELinux aux conteneurs que si on l'active. Contraintes dans la [référence technique](reference-technique.md#déployer-avec-docker-compose-sur-un-serveur) |
| Compte de service dédié `opsdesk` — **remplacée le 18 novembre 2026** par « Administration de Docker par `sudo` » | Les conteneurs tournent sous un compte `opsdesk` créé pour cela : ni mot de passe, ni `sudo`, ni connexion SSH. `mathias` reste le compte d'administration (SSH, Ansible, `sudo`). Raison : moindre privilège ; un conteneur compromis n'aurait accès ni aux clés SSH ni aux droits d'administration. Écarté : garder `mathias` pour tout, plus simple mais qui mélange administration et exécution du service | Ce compte n'avait de sens qu'avec Podman sans root : sous Docker, les conteneurs sont lancés par le démon, pas par un compte |
| Administration de Docker par `sudo` — retenu, non vérifié (18 novembre 2026) | Aucun compte dans le groupe `docker`. `mathias` administre par `sudo docker …`, Ansible par `become: true`, et chaque action est tracée dans le journal système. Les fichiers du déploiement sont dans `/opt/opsdesk`, propriété de root, et les secrets ne sont lisibles que par l'utilisateur du conteneur qui les lit. Les conteneurs eux-mêmes tournent sans root (UID 10001 pour l'API, 101 pour nginx, `postgres` pour la base), avec `no-new-privileges`. Écarté : ajouter `mathias` au groupe `docker`, plus confortable mais qui donne un accès root sans mot de passe ni trace | Une étape de plus à chaque commande, en échange de la traçabilité. Le socket Docker n'est monté dans aucun conteneur et l'API Docker n'écoute pas sur le réseau |
| Stockage de la base — retenu, non vérifié (12 novembre 2026) | Disque de données séparé de 10 Go (`vdb`), monté sur `/var/lib/opsdesk`. Écarté : données sur le disque système | Données séparées du système ; ce disque ne remplace pas la sauvegarde. **À revoir avant déploiement** : soit le dossier de données de Docker (`data-root`) sur ce disque, soit un montage du dossier de PostgreSQL, qui doit alors appartenir à l'utilisateur `postgres` de l'image et porter le bon contexte SELinux (option `:Z`) |
| Terraform et Ansible — retenu, non vérifié (12 novembre 2026), précisé le 13 novembre 2026 | Terraform avec le fournisseur libvirt, lancé depuis `srv-admin`, crée `srv-app` et `srv-k3s` par une URI `qemu+ssh` vers l'hôte ; état local sur `srv-admin`, copié hors de la VM. Ansible, avec des rôles et un inventaire sur `srv-admin`, configure les deux VM. Écartés : virt-manager à la main (sauf pour `srv-admin`) ; un état distant ; Terraform sur l'hôte | Par `qemu+ssh`, `srv-admin` obtient un large pouvoir sur les VM de l'hôte : risque connu, à relire. Le mode d'installation de Rocky Linux (image cloud et cloud-init, ou ISO et Kickstart) reste à décider à l'exercice 04 |
| Livraison : GitHub Actions et GHCR — retenu, non vérifié (12 novembre 2026), **mis à jour le 18 novembre 2026** | Tests **`pytest`** (sur PostgreSQL), construction **des deux images**, analyse Trivy, publication sur GHCR. Écarté : GitLab CI | `srv-app` tire les images publiées |
| Déploiement : Ansible — retenu, non vérifié (13 novembre 2026) | Les images publiées sont déployées sur `srv-app` par Ansible, lancé à la main depuis `srv-admin` : version choisie quand la CI est verte, puis contrôle de `/health/ready`. Écartés : tirer les images à la main ; lancer Ansible depuis GitHub Actions, dont les exécuteurs ne joignent pas le réseau privé | GitHub Actions publie et ne touche pas aux serveurs ; Ansible configure et déploie |
| Première image sur `srv-app` — retenu, non vérifié (13 novembre 2026) | Tant que GHCR ne contient aucune image, Ansible copie les sources sur `srv-app`, qui construit les images avec Docker et les teste en HTTP. Écarté : attendre la CI pour tester | Chemin temporaire, distinct du chemin normal |
| Retour arrière applicatif — retenu, non vérifié (13 novembre 2026) | Revenir à la version précédente en la redéployant avec Ansible (une image GHCR par version), puis contrôler `/health/ready`. Écarté : confondre ce retour avec la restauration de la base | Ne change ni le schéma ni les données |
| Sauvegarde et restauration — retenu, non vérifié (12 novembre 2026), précisé le 13 novembre 2026 | `pg_dump` au format custom chaque nuit à 02:00 sur `srv-app`, par un minuteur systemd, 7 copies gardées, `rsync` sur SSH vers `~/sauvegardes` sur l'hôte. Restauration : refaire le serveur, `pg_restore`, contrôler `/health/ready`, relire un ticket témoin. Écartés : copier le dossier de données à chaud ; garder les copies sur la VM ; lancer la sauvegarde depuis `srv-admin` | Une copie hors du serveur survit à la perte de la VM, pas à celle du PC. La restauration reste à vérifier |
| Supervision — retenu, non vérifié (12 novembre 2026), précisé le 13 novembre 2026 | K3s sur un seul nœud avec Traefik, une copie d'essai de l'application (mêmes images, base de test) ; Prometheus (lecture de `/metrics` toutes les 15 secondes, 15 jours de mesures) et Grafana dans K3s ; `node_exporter` sur `srv-app` et `srv-k3s` ; deux alertes : base indisponible depuis 1 minute, erreurs 5xx en hausse. Écartés : Alertmanager et Loki ; un cluster multi-nœuds ; K3s à la place de Docker Compose ; K3s sans application | Les alertes se lisent dans Prometheus et Grafana, aucun message n'est envoyé. Si `srv-k3s` tombe, la supervision tombe avec |
| Essai de charge : k6 depuis `srv-admin` — retenu, non vérifié (13 novembre 2026) | k6 envoie à la demande une charge limitée à la copie d'essai de `srv-k3s`. Écartés : charger le service réel ; k6 sur l'hôte | La charge reste hors du service réel ; un seul vCPU borne la charge |
| AWS — facultatif, en dernier (12 novembre 2026) | Une instance `t3.micro` à Paris, seulement si budget et autorisation sont établis | Aucune ressource payante sans accord préalable |

Pour une nouvelle décision coûteuse à inverser : date, contexte, choix, options écartées, conséquences. Ne jamais inventer la raison d'une décision ancienne pour compléter le tableau.

## Historique : la version 1 et l'essai Ubuntu/WSL

La version 1 d'OpsDesk était une application Flask avec rendu HTML côté serveur, servie par Gunicorn, sans authentification, en deux conteneurs (`app` et `db`). Elle a été testée le 3 novembre 2026 lors d'un essai sur Ubuntu/WSL2 avec Docker Compose (port `127.0.0.1:18081`). Ses tests, ses preuves, son scan de sécurité et ses schémas sont conservés dans [`legacy/`](../legacy/) ; ils ne s'appliquent pas à la v2.

## Références

[FastAPI](https://fastapi.tiangolo.com/) · [PostgreSQL 17](https://www.postgresql.org/docs/17/) · [Docker Engine sur RHEL](https://docs.docker.com/engine/install/rhel/) · [Docker Compose](https://docs.docker.com/compose/) · [Docker et les pare-feu](https://docs.docker.com/engine/network/packet-filtering-firewalls/) · [Directive `resolver` de nginx](https://nginx.org/en/docs/http/ngx_http_core_module.html#resolver)
