# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles trois phases, dans l'ordre, mènent de l'application locale à un service sur deux serveurs, créés depuis un troisième serveur d'administration, livré, sauvegardé puis supervisé ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Qui prépare l'infrastructure, où tournent l'application et ses données, comment une version est construite puis déployée, comment fonctionne la copie d'essai dans K3s, et comment on observe, sauvegarde et restaure, dans l'architecture cible à trois VM. |

## Lire les schémas

### Schéma technique : trois niveaux

- **En haut, la livraison :** le développeur pousse son code vers le dépôt GitHub ; le dépôt déclenche GitHub Actions, qui teste, construit, analyse avec Trivy et publie l'image sur GHCR. Publier n'est pas déployer. L'utilisateur, à droite, ouvre OpsDesk dans son navigateur.
- **Au centre, les trois VM**, cadres noirs côte à côte. `srv-admin` (contrôle) porte Git, OpenSSH, les fichiers IaC, Terraform, Ansible et k6. `srv-k3s` (essai) fait tourner, en workloads Kubernetes, la copie d'essai (Traefik, Service, Pod, base de test), Prometheus et Grafana. `srv-app` (service principal) fait tourner les conteneurs `app` et `db` avec Podman, Quadlet et systemd, et la sauvegarde. `srv-k3s` est au centre pour que chaque flèche reste courte : `srv-admin` pilote ses deux voisines, Prometheus lit `srv-app` d'à côté. Dans `srv-k3s`, tout ce qui est dessiné (Traefik, Service, Pod, base de test, Prometheus, Grafana) est déployé comme workloads Kubernetes ; seul K3s est installé sur la VM. K3s ne pilote pas les conteneurs de `srv-app` ([explication](../architecture.md#podman-et-k3s)). Une disposition avec `srv-app` au centre a été comparée à contenu identique et n'est pas retenue ([Contrôles](#contrôles)).
- **En bas, l'hôte des VM**, cadre gris clair qui contient les trois VM : libvirt, que Terraform pilote pour créer les VM, et le dossier des sauvegardes hors VM. L'hôte n'est pas une VM.
- **Cinq couleurs de flèche**, chacune avec son libellé : bleu, trafic applicatif (HTTP, SQL, chaîne Traefik, Service, Pod) ; gris foncé, pilotage et déploiement (SSH, `qemu+ssh`) ; vert, code et images (push, déclenche, publie, image tirée) ; orange, sauvegarde et restauration ; violet, observation et tests (Prometheus, Grafana, k6). Une flèche vers une VM s'arrête au bord de son cadre : elle vise la machine, pas un conteneur. Pour GHCR, la flèche suit le trajet de l'image ; c'est la VM qui la demande (pull).
- **Cinq numéros noirs :** les grandes étapes, reprises dans l'encadré du bas avec leur phase (1 et 2 : P1 ; 3 et 4 : P2 ; 5 : P3). Les échanges permanents (HTTP, SQL, collecte des mesures) n'ont pas de numéro. Les capsules P1 à P3 sont grises : les couleurs de phase restent celles de la présentation et ne se confondent pas avec celles des flux.
- **Capsule violette en police à chasse fixe :** une adresse de contrôle de l'application (`/health/live`, `/health/ready`, `/metrics`).

### Schéma de présentation

- **Cadre noir :** le service OpsDesk (utilisateur, application, base de données).
- **Bloc coloré :** une phase, dans l'ordre où on la construit. Bleu : phase 1, préparer et automatiser. Vert : phase 2, livrer et conserver. Violet : phase 3, orchestrer et maintenir.
- **Flèche grise entre les phases :** enchaînement des trois phases.

Les phases reprennent celles du [parcours](../parcours-apprentissage.md). Les schémas décrivent l'architecture cible, pas son avancement : l'application existe en local, l'infrastructure à trois VM reste à déployer et à valider ; l'avancement est suivi dans [STATUS](../../STATUS.md) et la [feuille de route](../../ROADMAP.md).

## Détail des éléments du schéma technique

### Routes de l'application

| Route | Rôle | Codes de réponse |
| --- | --- | --- |
| `GET /`, `GET /tickets`, `GET /tickets/<id>` | Pages : accueil (redirige vers la liste), liste et détail d'un ticket | 302 pour `/`, 200 sinon ; 404 si le ticket n'existe pas |
| `POST /tickets`, `POST /tickets/<id>/status` | Formulaires : créer un ticket, changer son statut | 303 puis redirection ; 400, 404 ou 409 en cas de refus |
| `GET /api/tickets`, `POST /api/tickets` | API JSON : lister, créer | 200 ; 201 à la création ; 400 si les données sont invalides |
| `GET /api/tickets/<id>`, `PATCH /api/tickets/<id>` | API JSON : lire un ticket, changer son statut (le champ `status` seul) | 200 ; 400, 404 ou 409 |

Le statut avance dans l'ordre `open`, `in_progress`, `closed`. Sauter une étape ou rouvrir un ticket clôturé renvoie 409. Si PostgreSQL ne répond pas, les pages et l'API renvoient 503.

### Sondes

| Adresse | Question posée | Réponse | Lue par |
| --- | --- | --- | --- |
| `/health/live` | Le programme tourne-t-il ? | 200, sans interroger la base | K3s, sur la copie d'essai de `srv-k3s` (redémarrage si la sonde échoue) |
| `/health/ready` | La base répond-elle ? | 200 si la lecture de `tickets` réussit, 503 sinon | K3s, sur la copie d'essai de `srv-k3s` (retrait du trafic si la sonde échoue) ; contrôle manuel d'un déploiement ou d'une restauration sur `srv-app` |
| `/metrics` | Quels compteurs ? | Toujours 200 : `opsdesk_http_requests_total` (méthode, route, code), `opsdesk_database_up` (1 ou 0), `opsdesk_tickets` (par statut) | Prometheus, toutes les 15 secondes, sur l'application de `srv-app` et sur la copie |
| `/version` | Quelle version est servie ? | 200, version et révision déclarées | Contrôle manuel |

Les compteurs de requêtes sont gardés en mémoire : ils repartent de zéro à chaque redémarrage de l'application. Sur `srv-app`, aucun outil ne lit `/health/live` ni `/health/ready` en continu : K3s ne lit que les sondes de sa propre copie.

### Table `tickets`

| Colonne | Type | Règle |
| --- | --- | --- |
| `id` | `bigint` | Clé primaire, générée automatiquement |
| `title` | `varchar(120)` | Obligatoire, au moins 3 caractères après suppression des espaces de bord |
| `description` | `varchar(2000)` | Obligatoire, vide par défaut |
| `priority` | `varchar(10)` | `low`, `normal` ou `high` ; l'application propose `normal` |
| `status` | `varchar(20)` | `open` (défaut), `in_progress` ou `closed` |
| `created_at` | `timestamptz` | Date de création, remplie par la base |
| `updated_at` | `timestamptz` | Date de dernière modification, mise à jour par l'application à chaque changement de statut |

### Serveurs, ports et accès

| Serveur | Rôle | Ressources prévues |
| --- | --- | --- |
| `srv-admin` (192.168.150.5) | Terraform, Ansible, Git, OpenSSH, k6 | 1 vCPU, 2 Go, disque de 20 Go |
| `srv-app` (192.168.150.10) | Application et base avec Podman, Quadlet et systemd ; sauvegarde | 2 vCPU, 4 Go, disque système de 20 Go et disque de données de 10 Go (`vdb`) monté sur `/var/lib/opsdesk` |
| `srv-k3s` (192.168.150.20) | K3s sur un nœud : copie d'essai, base de test, Traefik, Prometheus, Grafana | 2 vCPU, 6 Go, 30 Go |

Les trois serveurs sont des machines Rocky Linux 10.2 sur le réseau NAT libvirt `opsdesk-lan` (192.168.150.0/24), avec SELinux en mode Enforcing et firewalld. L'utilisateur d'administration est `mathias`. La connexion SSH directe de `root` est interdite ; les opérations privilégiées passent par `sudo`, depuis Ansible quand c'est nécessaire. Ces valeurs sont des choix de départ, non mesurés : le disque `vdb` et `/var/lib/opsdesk` restent des caractéristiques de la cible tant qu'ils ne sont ni créés ni testés.

### Matrice des flux réseau

Le sens va de la source, qui ouvre la connexion, à la destination. La règle firewalld s'applique sur la destination. Aucun de ces flux n'est vérifié.

| Source | Destination | Protocole et port | Fonction | Déclencheur | Règle prévue sur la destination |
| --- | --- | --- | --- | --- | --- |
| Hôte (développeur) | `srv-admin` | SSH, 22 | Administration | Développeur | 22 depuis l'hôte seul |
| `srv-admin` | Hôte | SSH, 22 (`qemu+ssh`) | Terraform pilote libvirt | `terraform plan`, `apply` | Hôte : 22 depuis 192.168.150.5, clé dédiée ; liaison à valider |
| `srv-admin` | `srv-app`, `srv-k3s` | SSH, 22 | Ansible configure et déploie | Développeur | 22 depuis `srv-admin` seule |
| `srv-admin` | `srv-app` | HTTP, 8000 | Contrôle de `/health/ready` après un déploiement | Ansible | 8000 depuis l'hôte, `srv-admin` et `srv-k3s` |
| Navigateur de l'hôte | `srv-app` | HTTP, 8000 | Utiliser OpsDesk | Utilisateur | Même règle 8000 |
| Conteneur `app` | Conteneur `db` | PostgreSQL, 5432 | Requêtes SQL | Application | Port non publié hors de `srv-app` |
| Prometheus (`srv-k3s`) | `srv-app` | HTTP, 8000 (`/metrics`) et 9100 (`node_exporter`) | Collecte toutes les 15 s | Prometheus | 8000 et 9100 depuis `srv-k3s` ; la requête d'un Pod sort normalement avec l'adresse du nœud, à vérifier |
| Prometheus | Pod OpsDesk de la copie | HTTP, 8000, dans le cluster | Collecte de la copie | Prometheus | Réseau interne du cluster ; voir la ligne suivante |
| Pods et Services de K3s | Nœud `srv-k3s`, autres Pods | Réseaux 10.42.0.0/16 (Pods) et 10.43.0.0/16 (Services), valeurs par défaut de K3s | Trafic interne du cluster | K3s | `srv-k3s` : ces deux réseaux en zone `trusted` si firewalld est gardé (exigence de la [documentation K3s](https://docs.k3s.io/installation/requirements?os=rhel), qui recommande plutôt de l'arrêter ; ce projet ne le désactive pas) ; règles à vérifier |
| Grafana | Prometheus | HTTP, 9090, dans le cluster | Source de données | Grafana | Réseau interne du cluster |
| k6 (`srv-admin`) | Traefik (`srv-k3s`) | HTTP, 80 | Charge de test bornée | Développeur | 80 depuis l'hôte et `srv-admin` |
| Hôte | `srv-k3s` | HTTPS, 6443 | API K3s (`kubectl`) | Développeur | 6443 depuis l'hôte |
| `srv-app` | Hôte | SSH, 22 (`rsync`) | Copie des sauvegardes vers `~/sauvegardes` | Minuteur de 02:00 | Hôte : 22 depuis 192.168.150.10, clé limitée à cette copie |
| `srv-admin` | GitHub | HTTPS, 443 sortant | `git clone`, `git pull` | Développeur | Sortie par le NAT libvirt |
| `srv-app`, `srv-k3s` | GHCR (`ghcr.io`) | HTTPS, 443 sortant | Tirer l'image | Ansible, K3s | Sortie par le NAT ; jeton de lecture si le paquet est privé |
| GitHub Actions | GHCR | HTTPS, 443, dans le cloud | Publier l'image | Événements configurés dans les workflows | — |

Le dessin montre ces flux ; il ne prouve pas qu'ils passent. Les contrôles ci-dessous sont à exécuter une fois les VM créées ; aucun ne l'a été.

| Flux | Contrôle, depuis la source | Résultat attendu | Statut |
| --- | --- | --- | --- |
| `srv-admin` vers l'hôte | `virsh -c qemu+ssh://<utilisateur>@<adresse de l'hôte>/system list --all` | Liste des domaines libvirt | NON EXÉCUTÉ |
| `srv-admin` vers les VM | `ansible all -m ping`, inventaire de `srv-app` et `srv-k3s` | `pong` des deux VM | NON EXÉCUTÉ |
| `srv-admin` vers `srv-app` | `curl -fsS http://192.168.150.10:8000/health/ready` | Réponse 200 | NON EXÉCUTÉ |
| `srv-k3s` vers `srv-app` | `curl -fsS http://192.168.150.10:8000/metrics` depuis `srv-k3s`, puis depuis un Pod temporaire | Compteurs `opsdesk_*` ; un échec depuis le Pod seul indique une règle de Pod ou de pare-feu à revoir | NON EXÉCUTÉ |
| `srv-admin` vers Traefik | `curl -sS -o /dev/null -w '%{http_code}\n' http://192.168.150.20/` | Un code HTTP, sans erreur de connexion | NON EXÉCUTÉ |
| `srv-app`, `srv-k3s` vers GHCR | `curl -sS -o /dev/null -w '%{http_code}\n' https://ghcr.io/v2/` | Une réponse HTTP, quel que soit le code : la sortie HTTPS et le DNS fonctionnent | NON EXÉCUTÉ |
| Pare-feu de chaque VM | `sudo firewall-cmd --get-active-zones`, puis `--list-all` | Ports et sources conformes à la matrice | NON EXÉCUTÉ |

Les flux sortants supposent la route par défaut et le DNS fournis par le réseau NAT libvirt ; ils sont à vérifier au pré-check réseau. L'utilisateur est le navigateur de l'hôte, en laboratoire : aucun accès depuis Internet n'est prévu.

### Flux du schéma technique

| Étape | De | Vers | Libellé | Type |
| --- | --- | --- | --- | --- |
| 1 | Développeur | `srv-admin` | SSH | Pilotage |
| 1 | Terraform | libvirt (hôte) | qemu+ssh | Pilotage : création des VM |
| 1, 3 | Ansible | `srv-k3s`, `srv-app` | SSH | Pilotage : configuration, puis déploiement d'une version choisie |
| 3 | Développeur | Dépôt GitHub | push | Code |
| 3 | Dépôt GitHub | GitHub Actions | déclenche | Code |
| 3 | GitHub Actions | GHCR | publie | Image |
| 3, 5 | GHCR | `srv-app`, `srv-k3s` | image (pull) | Image tirée par la VM |
| — | Utilisateur | OpsDesk | HTTP | Trafic applicatif permanent |
| — | OpsDesk | PostgreSQL 17 | SQL | Trafic applicatif permanent |
| 4 | PostgreSQL 17 | Sauvegarde | pg_dump | Sauvegarde |
| 4 | Sauvegarde | Sauvegardes hors VM | rsync, SSH | Sauvegarde |
| 4 | Sauvegardes hors VM | PostgreSQL 17 | pg_restore | Restauration des données |
| 5 | Traefik, Service | Pod OpsDesk | (sans libellé) | Trafic de la copie |
| 5 | Pod OpsDesk | PostgreSQL test | SQL | Trafic de la copie |
| 5 | Prometheus | OpsDesk (`srv-app`), Pod OpsDesk | lit /metrics, lit | Observation |
| 5 | Grafana | Prometheus | lit | Observation |
| 5 | k6 | Traefik | charge | Test de charge |

### Première livraison et livraisons suivantes

| | Première mise en service (étape 2) | Livraisons suivantes (étape 3) |
| --- | --- | --- |
| Origine du code livré | Sources du dépôt cloné sur `srv-admin` (`git clone` depuis GitHub, HTTPS 443) | Image publiée sur GHCR par GitHub Actions, une fois la CI verte |
| Rôle d'Ansible, lancé à la main depuis `srv-admin` | Copie les sources sur `srv-app` | Demande à `srv-app` de tirer la version choisie |
| Où l'image est construite | Sur `srv-app`, avec Podman : image d'exercice | Dans GitHub Actions, jamais sur un serveur |
| Contrôle | Test HTTP de l'image d'exercice | `/health/ready` après le déploiement |
| Statut | Chemin temporaire, tant que GHCR ne contient aucune image | Pratique normale à garder |
| Sur le dessin | Étape 2, flèche SSH d'Ansible vers `srv-app`, carte « Git · OpenSSH : dépôt cloné » | Étape 3, flèches push, déclenche, publie, image (pull), SSH |

L'étape 2 n'a pas de flèche propre : elle réutilise le lien SSH d'Ansible. Aucune des deux voies n'est exécutée.

Le dessin ne montre pas : la flèche de Git vers le dépôt GitHub (le clone est écrit sur la carte) ; la lecture des sondes de la copie par K3s, écrite sur la carte du Pod ; la lecture de `node_exporter` (port 9100) ; les deux règles d'alerte ; le contrôle de `/health/ready` après un déploiement, écrit dans l'étape 3 ; la copie hors de `srv-admin` de l'état Terraform et des clés SSH ; les ports, sauf les adresses de contrôle. Ces détails sont dans les tableaux ci-dessus et dans le [registre d'architecture](../architecture.md#décisions-retenues).

### Informations retirées du dessin et où les retrouver

La V10 affichait davantage de détails. Ils restent dans le dépôt :

| Information | Où la retrouver |
| --- | --- |
| Sept colonnes de la table `tickets` | Section [Table `tickets`](#table-tickets) ; `db/schema.sql` |
| Rôle détaillé des sondes et codes de réponse | Section [Sondes](#sondes) ; [contrat applicatif](../architecture.md#contrat-applicatif) |
| Disque `vdb`, `/var/lib/opsdesk` | Section Serveurs ci-dessus ; décision « Stockage de la base » |
| Heure de 02:00, minuteur systemd, 7 copies, format custom | Section [Sauvegarde et restauration](#sauvegarde-et-restauration) ; décision « Sauvegarde et restauration » |
| Fichiers `.tf`, état, inventaire, playbooks, secrets (pastilles de la V10) | Carte « Fichiers IaC » ; [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md), sections 6.2 et 6.3 ; exercices 04 et 05 |
| SSH par clé, `root` sans connexion SSH, clés hors de Git | Section Serveurs ; décision « Réseau, accès et protections » |
| Première image construite sur `srv-app` | Étape 2 ; décision « Première image » ; exercice 06 |
| Choix de la version, contrôle de `/health/ready`, retour arrière | Étape 3 et note du dessin ; décisions « Déploiement » et « Retour arrière applicatif » ; exercice 08 |
| Reprise de `srv-admin` (état Terraform, clés) | Décision « Reprise de `srv-admin` » ; guide du laboratoire, section 8 |
| Prometheus : 15 s, 15 jours, deux règles d'alerte, `node_exporter` ; contenu des tableaux Grafana | Décision « Supervision » ; exercice 09 |
| Deployment, Service, sondes lues par K3s | Exercice 07 |
| Dimensionnement de k6 (un vCPU) | Décision « Essai de charge » ; exercice 09 |
| Ports et règles firewalld | [Matrice des flux réseau](#matrice-des-flux-réseau) |
| Récit en dix phrases de la V10 | Remplacé par les cinq étapes et le [tableau des flux](#flux-du-schéma-technique) |

### Sauvegarde et restauration

| Étape | Détail |
| --- | --- |
| Sauvegarde | `pg_dump` au format custom chaque nuit à 02:00 sur `srv-app`, lancé par un minuteur systemd ; 7 copies gardées |
| Copie hors du serveur | `rsync` par SSH vers `~/sauvegardes` sur l'hôte Fedora |
| Restauration des données | `pg_restore` remet la base ; contrôle de `/health/ready`, puis relecture d'un ticket témoin. Le format custom de `pg_dump` est celui que lit `pg_restore` |
| Reconstruction de la VM | Si `srv-app` est perdue, `srv-admin` la refait avec Terraform et Ansible avant la restauration des données |
| Retour arrière applicatif | Redéployer la version précédente de l'image ; ne touche pas aux données |
| Limite | L'hôte et les trois VM sont sur le même PC : la copie survit à la perte d'une VM, pas à celle du PC ou de son disque |
| `srv-admin` | L'état Terraform et les clés SSH ne sont pas dans le dépôt : ils sont copiés hors de la VM (sur l'hôte, hors de Git). Sans eux, Terraform ne connaît plus `srv-app` ni `srv-k3s` |

## Logos et pictogrammes

Les logos proviennent du paquet [simple-icons](https://github.com/simple-icons/simple-icons) 13.21.0, dont les fichiers sont publiés sous licence CC0. Les marques appartiennent à leurs titulaires ; les logos servent seulement à nommer les outils.

| Outil | Fichier source | Couleur d'origine |
| --- | --- | --- |
| Flask | `flask.svg` | #000000 |
| PostgreSQL | `postgresql.svg` | #4169E1 |
| Podman | `podman.svg` | #892CA0 |
| GitHub Actions | `githubactions.svg` | #2088FF |
| Trivy | `trivy.svg` | #1904DA |
| Terraform | `terraform.svg` | #844FBA |
| Rocky Linux | `rockylinux.svg` | #10B981 |
| Ansible | `ansible.svg` | #EE0000 |
| K3s | `k3s.svg` | #FFC61C |
| Prometheus | `prometheus.svg` | #E6522C |
| Grafana | `grafana.svg` | #F46800 |
| k6 | `k6.svg` | #7D64FF |
| GitHub et GHCR | `github.svg` | #181717 |
| Git | `git.svg` | #F05032 |
| Traefik | `traefikproxy.svg` | #24A1C1 |

Les pictogrammes de la personne (acteur et développeur), du navigateur, du volume, du dossier, de l'horloge, de la restauration et du terminal (OpenSSH, `srv-admin`) sont dessinés pour ce projet et suivent la licence MIT du dépôt.

## D'où viennent les faits

| Ce que montre le schéma | Source dans le dépôt |
| --- | --- |
| Gunicorn sert Flask ; pages et API de tickets | [`app/opsdesk/web.py`](../../app/opsdesk/web.py), [`requirements.lock`](../../requirements.lock), [`docs/architecture.md`](../architecture.md) |
| Sondes `/health/live`, `/health/ready`, `/version`, `/metrics` et leurs réponses | [`app/opsdesk/web.py`](../../app/opsdesk/web.py) |
| PostgreSQL, table `tickets` et ses colonnes | [`db/schema.sql`](../../db/schema.sql) |
| Aucune authentification, données fictives | [`README.md`](../../README.md), [`docs/securite.md`](../securite.md) |
| Serveurs, réseau, ports, sauvegarde, supervision | Décisions du [registre d'architecture](../architecture.md#décisions-retenues) |
| `srv-admin`, amorçage, reprise, liaison libvirt, première image, retour arrière, k6 | Décisions du [registre d'architecture](../architecture.md#décisions-retenues) et [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md) (sections 5, 6.2 et 6.3) |
| Hôte Fedora 45, KVM, libvirt, Rocky Linux 10.2 | [`ROADMAP.md`](../../ROADMAP.md), [`docs/laboratoire-fedora-kvm-rocky.md`](../laboratoire-fedora-kvm-rocky.md) |
| Rôle de K3s : copie d'essai, indépendante de Podman | [`docs/architecture.md`](../architecture.md#podman-et-k3s), [`docs/apprentissage/07-k3s.md`](../apprentissage/07-k3s.md) |
| Phases 1 à 3, leur ordre et leurs outils | [`docs/architecture.md`](../architecture.md#trois-phases-sans-changer-dapplication), [`ROADMAP.md`](../../ROADMAP.md), [`docs/parcours-apprentissage.md`](../parcours-apprentissage.md), [`docs/apprentissage/README.md`](../apprentissage/README.md) |
| Développeur : application et PostgreSQL en local | [`STATUS.md`](../../STATUS.md), [`docs/architecture.md`](../architecture.md#trois-phases-sans-changer-dapplication) |
| Flux, libellés et numéros | Tableau des flux ci-dessus, décisions du [registre d'architecture](../architecture.md#décisions-retenues) |

## Modifier et exporter

1. Ouvrir le `.drawio` dans diagrams.net et modifier.
2. *Fichier → Exporter en → SVG*, sans l'option « Inclure une copie de mon diagramme ». Le texte alternatif de la page devient le `<title>` du SVG.
3. Enregistrer le `.drawio` et le SVG dans le même commit.

Les sources portent `adaptiveColors="none"` : sans ce réglage, diagrams.net en thème sombre inverse les couleurs et les logos sombres deviennent presque invisibles. Les cadres de texte sont ajustés à leur contenu.

Les deux SVG sont exportés depuis les `.drawio` par le moteur d'export de Draw.io 32.6.10 (page d'export du dépôt jgraph/drawio, Chromium sans interface), en thème clair et sans bordure. Cet export ne remplace pas l'ouverture des fichiers dans l'application.

## Contrôles

Réalisés le 13 novembre 2026, après la restructuration du schéma technique (variante C, retenue après comparaison de deux maquettes complètes), puis après l'audit de la V11, qui demandait une correction ciblée et non une nouvelle refonte :

- corrections de l'audit : sous-titre du schéma technique (l'application existe en local, l'infrastructure reste à déployer et à valider), phase 1 de la présentation (OpsDesk fonctionne sur `srv-app` ; la copie K3s n'arrive qu'en phase 3, qui nomme `srv-k3s`), étape 2 (sources du dépôt cloné) distinguée de l'étape 3 (images de GHCR), descriptions secondaires de `srv-admin` réduites ; Prometheus et Grafana confirmés comme workloads Kubernetes ;
- ordre des VM : la disposition `srv-admin`, `srv-app`, `srv-k3s` a été construite avec les mêmes 102 textes, 363 mots, polices et flux, puis comparée à la disposition retenue (`srv-admin`, `srv-k3s`, `srv-app`) :

| Mesure | `srv-admin`, `srv-k3s`, `srv-app` (retenue) | `srv-admin`, `srv-app`, `srv-k3s` |
| --- | --- | --- |
| Croisements de flèches | 0 | 5 |
| Longueur totale des flèches | 3 404 px | 4 430 px |
| Flèches de plus de 400 px | 1 | 2 (jusqu'à 1 032 px) |
| Coudes | 2 | 7 |
| Hauteur du canevas | 1 364 px | 1 424 px |
| Textes barrés par une flèche | 0 | 3 |

  Avec `srv-app` au centre, l'utilisateur doit passer au-dessus de `srv-app` (une ligne de plus) et les liens de `srv-admin` vers `srv-k3s` (SSH, charge k6) passent sous `srv-app`, en coupant la sauvegarde et la restauration. Les numéros 1, 2 et 5 du dessin et l'encadré des cinq étapes donnent l'ordre de lecture dans les deux cas ; la disposition retenue est conservée ;
- export des SVG par le moteur Draw.io 32.6.10 ; aucun `<foreignObject>` ; logos embarqués ;
- source `.drawio` : identifiants uniques, texte alternatif présent, aucun pointillé, aucune forme `mxgraph.*`, polices Arial et Courier New ;
- rendu par deux moteurs indépendants (Chromium et librsvg) : écart moyen 0,48 sur 255 (technique) et 0,62 (présentation) ;
- aucune flèche ne croise une autre flèche ; aucune flèche ne traverse une carte qui n'est pas la sienne ; aucun texte ne chevauche une flèche, une pastille ou un autre texte (mesure sur la géométrie de la source) ;
- plus petite police : 14 px ; canevas technique de 1600 × 1364 px ; les titres des VM font 20 px ;
- contraste minimal calculé : 4,68:1 (technique) et 4,75:1 (présentation), seuil WCAG AA 4,5:1 ;
- comptes du schéma technique : 102 textes et 363 mots (535 mots dans la V10), 21 flèches de flux (et 5 flèches d'exemple dans la légende), 5 numéros ; une seule flèche dépasse 400 px (Ansible vers `srv-app`, sous `srv-k3s`) ;
- rendu réduit à 880 px de large (colonne d'un README GitHub) : les trois VM, leurs rôles et les flux se lisent ; les petits textes (14 px deviennent environ 8 px) demandent un agrandissement.

Non vérifiés : ouverture des `.drawio` dans diagrams.net, affichage réel dans GitHub et Notion, thèmes clair et sombre, application mobile. Ces contrôles portent sur le dessin : aucune des trois VM n'existe.
