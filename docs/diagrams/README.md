# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles trois phases, dans l'ordre, mènent de l'application locale à un service sur deux serveurs, livré, sauvegardé puis supervisé ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Comment les composants sont reliés et sur quelle machine ils tournent, dans l'architecture cible : préparation des serveurs, requête, base, livraison, déploiement, sauvegarde, copie d'essai dans K3s, supervision et essai de charge. |

## Lire les schémas

- **Cadre noir :** le service OpsDesk (navigateur, application, base de données).
- **Cadre ou bloc coloré :** une phase du projet, dans l'ordre où on la construit. Bleu : phase 1, préparer et automatiser. Vert : phase 2, livrer et conserver. Violet : phase 3, orchestrer et maintenir. Dans le schéma technique, trois cadres se suivent de haut en bas, chacun titré du nom de sa phase et précédé de sa capsule P1, P2 ou P3 ; la présentation reprend cette capsule sous la forme « Phase 1 », « Phase 2 », « Phase 3 ».
- **Développeur (technique) :** à gauche, il lance Terraform, Ansible et k6, teste l'application dans son navigateur et pousse son code vers GitHub. Terraform, Ansible et k6 sont trois cartes de la phase 1.
- **Groupe gris (technique) :** un lieu. « Podman · VM srv-app » réunit les deux conteneurs, `app` et `db`. « GitHub · cloud » réunit GitHub Actions et GHCR : c'est le seul élément dans le cloud, les deux serveurs sont des machines virtuelles locales. « K3s · VM srv-k3s » réunit ce que K3s fait tourner : une copie d'essai de l'application (avec sa base de test et Traefik), puis Prometheus et Grafana. Les deux serveurs sont indépendants : K3s ne pilote pas les conteneurs de Podman ([explication](../architecture.md#podman-et-k3s)). La sauvegarde et la restauration sont hors des groupes : elles agissent sur `srv-app`.
- **Capsule violette en police à chasse fixe (technique) :** l'adresse de contrôle d'une sonde de l'application (`/health/live`, `/health/ready`, `/metrics`).
- **Flèche bleue :** une requête vers le service : celle du navigateur (HTTP), de l'application vers la base (SQL) et la charge envoyée par k6.
- **Flèche grise :** tous les autres flux, chacun avec son libellé : lance, prépare, déploie, push, publie, tire l'image, sauvegarde, restauration, lecture des mesures. Le [tableau des flux](#flux-du-schéma-technique) les détaille.
- **Pastille numérotée (technique) :** ordre de l'histoire, de 1 à 9, repris dans l'encadré « Comment ça fonctionne ». Elle ne suit pas la position : l'étape 4 (Ansible déploie) et l'étape 9 (k6) sont en haut parce que le serveur visé y est dessiné. Les flèches d'un même pas portent le même numéro.
- **Flèche grise entre les phases (présentation) :** enchaînement des trois phases.

Les phases reprennent celles du [parcours](../parcours-apprentissage.md). Les schémas décrivent l'architecture cible du projet, pas son avancement : rien n'est encore réalisé, et l'avancement et le contrôle de chaque élément sont suivis dans [STATUS](../../STATUS.md) et la [feuille de route](../../ROADMAP.md).

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
| `/health/ready` | La base répond-elle ? | 200 si la lecture de `tickets` réussit, 503 sinon | K3s, sur la copie d'essai de `srv-k3s` (retrait du trafic si la sonde échoue) ; contrôle de la restauration sur `srv-app` |
| `/metrics` | Quels compteurs ? | Toujours 200 : `opsdesk_http_requests_total` (méthode, route, code), `opsdesk_database_up` (1 ou 0), `opsdesk_tickets` (par statut) | Prometheus, toutes les 15 secondes, sur l'application de `srv-app` |
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

| Serveur | Rôle | Port | Accessible depuis |
| --- | --- | --- | --- |
| `srv-app` (192.168.150.10) | Application et base avec Podman | 22 (SSH) | L'hôte seulement, par clé, sans mot de passe ni connexion root |
| | | 8000 (application) | L'hôte et `srv-k3s` |
| | | 5432 (base) | Non publié : seule l'application l'atteint |
| | | 9100 (mesures du serveur) | `srv-k3s` |
| `srv-k3s` (192.168.150.20) | K3s (copie d'essai de l'application, base de test), Prometheus, Grafana | 80 (Traefik), 6443 (API K3s) | L'hôte |

Les deux serveurs sont des machines Rocky Linux 10.2 sur le réseau privé `opsdesk-lan` (192.168.150.0/24), avec SELinux en mode Enforcing et firewalld. L'utilisateur d'administration est `mathias`. `srv-app` a 2 vCPU, 4 Go de mémoire, un disque système de 20 Go et un disque de données de 10 Go monté sur `/var/lib/opsdesk` ; `srv-k3s` a 2 vCPU, 6 Go et 30 Go.

### Flux du schéma technique

| N° | De | Vers | Libellé | Nature |
| --- | --- | --- | --- | --- |
| 1 | Développeur | Terraform, Ansible, k6 | lance | Il lance les outils depuis son poste |
| 1 | Terraform | `srv-app` (groupe Podman) | prépare | Terraform crée le serveur ; Ansible le configure |
| 2 | Développeur (navigateur) | Application | HTTP · navigateur | Requête de l'utilisateur |
| 2 | Application | PostgreSQL | SQL | Requête vers la base |
| 3 | Développeur | GitHub Actions | push | Le code est poussé sur GitHub, ce qui lance le pipeline |
| 3 | GitHub Actions | GHCR | publie | Publication de l'image, après les tests et l'analyse Trivy |
| 4 | Ansible | `srv-app` (groupe Podman) | déploie | Ansible, lancé par le développeur, déploie l'application |
| 4 | `srv-app` | GHCR | tire l'image | `srv-app` tire l'image publiée |
| 5 | Sauvegarde | PostgreSQL | pg_dump | Sauvegarde de 02:00 |
| 6 | Restauration | PostgreSQL | pg_restore | Remise de la base |
| 7 | K3s (copie d'essai) | GHCR | tire l'image | K3s tire la même image que `srv-app` et lance une copie, avec sa base de test |
| 8 | Prometheus | Application de `srv-app` | lit /metrics | Lecture toutes les 15 secondes |
| 8 | Grafana | Prometheus | lit | Prometheus est la source de données de Grafana |
| 9 | k6 | Application de `srv-app` | charge | Essai de charge limité, à la demande |

Terraform et Ansible font la même chose pour `srv-k3s` ; la flèche n'est dessinée que vers `srv-app`. La copie de la sauvegarde hors du serveur (`rsync` par SSH vers `~/sauvegardes` sur l'hôte) est écrite dans la carte Sauvegarde, sans flèche propre ; une copie sert ensuite à restaurer.

Le dessin ne montre pas : la lecture des sondes de la copie par K3s, écrite dans la carte de la copie parce qu'elle se passe à l'intérieur du cluster ; la base de test de la copie, nommée dans sa carte, sans carte ni flèche propre ; la lecture de `node_exporter` (port 9100) par Prometheus, indiquée seulement dans la carte Prometheus ; les deux règles d'alerte ; la connexion SSH d'administration ; l'hôte Fedora, KVM et libvirt qui font tourner les deux machines virtuelles ; les ports, sauf les adresses de contrôle des sondes. Les deux règles d'alerte sont dans le [registre d'architecture](../architecture.md#décisions-retenues).

### Sauvegarde et restauration

| Étape | Détail |
| --- | --- |
| Sauvegarde | `pg_dump` chaque nuit à 02:00, lancé par un minuteur systemd ; 7 copies gardées |
| Copie hors du serveur | `rsync` par SSH vers `~/sauvegardes` sur l'hôte Fedora |
| Restauration | Refaire le serveur avec Terraform et Ansible, restaurer avec `pg_restore`, puis contrôler `/health/ready` |

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
| Traefik | `traefikproxy.svg` | #24A1C1 |

Les pictogrammes de la personne (acteur et développeur), du navigateur, du volume, du dossier, de l'horloge et de la restauration sont dessinés pour ce projet et suivent la licence MIT du dépôt.

## D'où viennent les faits

| Ce que montre le schéma | Source dans le dépôt |
| --- | --- |
| Gunicorn sert Flask ; pages et API de tickets | [`app/opsdesk/web.py`](../../app/opsdesk/web.py), [`requirements.lock`](../../requirements.lock), [`docs/architecture.md`](../architecture.md) |
| Sondes `/health/live`, `/health/ready`, `/version`, `/metrics` et leurs réponses | [`app/opsdesk/web.py`](../../app/opsdesk/web.py) |
| PostgreSQL, table `tickets` et ses colonnes | [`db/schema.sql`](../../db/schema.sql) |
| Aucune authentification, données fictives | [`README.md`](../../README.md), [`docs/securite.md`](../securite.md) |
| Serveurs, réseau, ports, sauvegarde, supervision | Décisions du [registre d'architecture](../architecture.md#décisions-retenues) |
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

Réalisés le 13 novembre 2026 sur les deux schémas, après la refonte du schéma technique (architecture cible, trois outils d'infra, groupe GitHub dans le cloud, neuf numéros) :

- export des SVG par le moteur Draw.io 32.6.10 ; aucun `<foreignObject>` ; aucune image externe (les logos sont embarqués) ;
- source `.drawio` : XML valide, identifiants uniques, texte alternatif présent, aucun pointillé, aucune forme de la bibliothèque `mxgraph.*`, polices Arial et Courier New seulement ;
- rendu par deux moteurs indépendants (Chromium et librsvg) : même figure, chaque composant affiche son icône ;
- aucun texte ne dépasse son cadre sur le rendu Chromium ; aucune flèche ne traverse une carte qui n'est pas la sienne ; aucune pastille ni aucun libellé ne chevauche un texte (mesure sur la géométrie de la source) ; plus petite police : 14 px sur un canevas de 1200 px de large ;
- contrastes calculés : tous les textes au moins 4,75:1 (seuil WCAG AA : 4,5:1) ;
- comptes : schéma technique, 124 textes et 24 pastilles dans la source, 148 éléments texte dans le SVG ; 24 icônes dans la source, 17 images dans le SVG, les 7 autres étant des icônes répétées (Flask, PostgreSQL, GitHub, Rocky Linux, Terraform, Ansible) que l'export réutilise ; présentation, 62 textes et 15 images dans la source comme dans le SVG ;
- numéros du schéma technique : de 1 à 9 sans trou, une phrase du récit par numéro ; ils suivent l'histoire, non la position sur la page ;
- concordance des deux schémas : mêmes noms et mêmes couleurs de phase ; chaque outil de la présentation figure dans le schéma technique, k6 compris.

Non vérifiés sur cette version : ouverture des `.drawio` dans diagrams.net (application web ou de bureau), affichage dans GitHub et dans Notion (thèmes clair et sombre, largeur étroite, application mobile de Notion) ; la largeur affichée de l'image, et donc la police effective, n'est pas remesurée.
