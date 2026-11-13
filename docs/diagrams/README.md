# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles trois phases, dans l'ordre, mènent de l'application locale à un service sur deux serveurs, créés depuis un troisième serveur d'administration, livré, sauvegardé puis supervisé ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Qui prépare l'infrastructure, où tournent l'application et ses données, comment une version est construite puis déployée, comment fonctionne la copie d'essai dans K3s, et comment on observe, sauvegarde et restaure, dans l'architecture cible à trois VM. |

## Lire les schémas

### Schéma technique : trois zones

Le schéma se lit de haut en bas, sans ordre chronologique : ce n'est pas une procédure. Une fois l'infrastructure préparée, une mise à jour de l'application passe par GitHub, la CI, GHCR et Ansible, sans recréer de VM.

- **Code et livraison (en haut) :** le développeur pousse son code vers le dépôt GitHub (`push`), qui déclenche GitHub Actions (`CI`) ; Actions teste, construit, analyse avec Trivy et publie les images versionnées sur GHCR. Publier n'est pas déployer. Une ligne sous la chaîne rappelle les deux voies : première livraison (sources clonées sur `srv-admin`, première image construite sur `srv-app`), puis versions suivantes (publiées par la CI, déployées par Ansible à la demande).
- **Infrastructure et responsabilités (au milieu) :** trois VM Rocky Linux 10.2, de gauche à droite : `srv-admin` (piloter), `srv-app` (exécuter), `srv-k3s` (orchestrer).
  - `srv-admin`, installée à la main une fois, porte Terraform, Ansible, Git avec OpenSSH et k6. Elle administre les deux autres : Ansible par SSH (liaison du haut), Terraform vers libvirt sur l'hôte (liaison du bas).
  - `srv-app` exécute avec Podman, Quadlet et systemd, derrière un point d'entrée HTTP du réseau privé du laboratoire, OpsDesk (Flask et Gunicorn, adresses `/health/live`, `/health/ready`, `/metrics`) et PostgreSQL 17 sur un volume persistant. Elle porte aussi la sauvegarde de la base.
  - `srv-k3s` fait tourner, sur un seul nœud K3s, une copie d'essai (Traefik, Service, Pod OpsDesk, base PostgreSQL de test aux données fictives), ainsi que Prometheus et Grafana. Tout ce qui est dessiné dans `srv-k3s` est déployé comme workload Kubernetes ; seul K3s est installé sur la VM. K3s ne pilote pas les conteneurs de `srv-app` ([explication](../architecture.md#podman-et-k3s)).
- **Ressources extérieures et liaisons clés (en bas) :** l'hôte de virtualisation (libvirt), que Terraform utilise pour créer `srv-app` et `srv-k3s` ; les sauvegardes hors VM, stockées sur l'hôte physique ; un rappel des communications entre environnements. L'hôte n'est pas une VM.
- **Cinq couleurs de flèche**, expliquées par la légende du bas : bleu, trafic applicatif (HTTP, SQL, chaîne Traefik, Service, Pod) ; gris foncé, administration (SSH, `qemu+ssh`) ; vert, code et images (push, CI, publie, images récupérées depuis GHCR) ; orange, sauvegarde et restauration ; violet, observabilité (Prometheus, Grafana). Une flèche vers une VM s'arrête au bord de son cadre : elle vise la machine. Les flèches `/metrics` aboutissent sur la carte OpsDesk de `srv-app` et sur le Pod de la copie. Un seul croisement (SSH et images GHCR) est marqué par un saut d'arc.
- **Pastilles violettes :** adresses de contrôle de l'application.
- **Badge « Cible • à déployer » :** l'architecture est décrite, aucune des trois VM n'existe.

### Schéma de présentation

- **Haut, « Le service » :** l'utilisateur appelle OpsDesk (Flask et Gunicorn), qui conserve les tickets dans PostgreSQL ; les flèches `HTTP` et `SQL` le montrent. La ligne sous le bloc précise : service pédagogique en laboratoire local, données fictives, sans authentification, non exposé publiquement.
- **Bas, « Le parcours » :** trois blocs de phase, lus de gauche à droite dans l'ordre où on les construit. Bleu, P1 préparer et automatiser (Rocky Linux, Terraform, Ansible, Podman) ; vert, P2 livrer et conserver (GitHub Actions, Trivy, sauvegarde, restauration) ; violet, P3 orchestrer et maintenir (K3s, Prometheus, Grafana, k6). Chaque bloc se termine par un « résultat attendu », jamais par un résultat obtenu.
- **Flèches grises entre les phases :** enchaînement des trois phases.

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

| De | Vers | Libellé | Type |
| --- | --- | --- | --- |
| Développement | Dépôt GitHub | push | Code |
| Dépôt GitHub | GitHub Actions | CI | Code |
| GitHub Actions | GHCR | publie | Image |
| GHCR | `srv-app`, `srv-k3s` | Images OCI récupérées depuis GHCR | Image tirée par chaque VM |
| `srv-admin` | `srv-app`, `srv-k3s` | SSH | Administration : Ansible configure, puis déploie une version choisie |
| `srv-admin` (Terraform) | Hôte libvirt | qemu+ssh • crée 2 VM | Administration : création des VM |
| Point d'entrée HTTP | OpsDesk | (sans libellé) | Trafic applicatif |
| OpsDesk | PostgreSQL 17 | SQL | Trafic applicatif |
| `srv-app` | Sauvegardes hors VM | copie | Sauvegarde |
| Sauvegardes hors VM | `srv-app` | pg_restore → PostgreSQL | Restauration des données |
| Traefik, Service | Pod OpsDesk | (sans libellé) | Trafic de la copie |
| Pod OpsDesk | PostgreSQL test | SQL | Trafic de la copie |
| Prometheus | OpsDesk (`srv-app`), Pod OpsDesk | /metrics | Observation |
| Grafana | Prometheus | interroge | Observation |

### Première livraison et livraisons suivantes

Chemin de la première livraison : dépôt source → `srv-admin` → transfert par Ansible → `srv-app` → construction initiale de l'image.

| | Première mise en service (P1) | Livraisons suivantes (P2) |
| --- | --- | --- |
| Origine du code livré | Sources du dépôt cloné sur `srv-admin` (`git clone` depuis GitHub, HTTPS 443) | Image publiée sur GHCR par GitHub Actions, une fois la CI verte |
| Rôle d'Ansible, lancé à la main depuis `srv-admin` | Copie les sources sur `srv-app` | Demande à `srv-app` de tirer la version choisie |
| Où l'image est construite | Sur `srv-app`, avec Podman : image d'exercice | Dans GitHub Actions, jamais sur un serveur |
| Contrôle | Test HTTP de l'image d'exercice | `/health/ready` après le déploiement |
| Statut | Chemin temporaire, tant que GHCR ne contient aucune image | Pratique normale à garder |
| Sur le dessin | Texte sous la chaîne GitHub : « P1 : sources clonées sur `srv-admin` → première image sur `srv-app` » ; la liaison SSH d'Ansible est la seule liaison dessinée entre les deux VM | Flèches push, CI, publie, images récupérées depuis GHCR et SSH ; texte « P2 : la CI publie les versions suivantes ; Ansible déploie à la demande » |

La première livraison n'a pas de flèche propre : elle n'apparaît que dans le texte sous la chaîne GitHub. Aucune des deux voies n'est exécutée.

Le dessin ne montre pas : le clone du dépôt vers `srv-admin` ; le transfert initial des sources vers `srv-app` ; `pg_dump` et le transfert `rsync` (écrits dans la carte de sauvegarde, que la flèche « copie » résume) ; la charge de k6 vers Traefik (écrite dans le cadre du laboratoire d'essai) ; la lecture des sondes de la copie par K3s (écrite sur la carte du Pod) ; la lecture de `node_exporter` (port 9100) ; les deux règles d'alerte ; la copie hors de `srv-admin` de l'état Terraform et des clés SSH (la carte dit seulement « état Terraform : protégé et récupérable ») ; les ports, sauf les adresses de contrôle. Ces détails sont dans les tableaux ci-dessus et dans le [registre d'architecture](../architecture.md#décisions-retenues).

### Informations retirées du dessin et où les retrouver

Les versions précédentes affichaient davantage de détails. Ils restent dans le dépôt :

| Information | Où la retrouver |
| --- | --- |
| Sept colonnes de la table `tickets` | Section [Table `tickets`](#table-tickets) ; `db/schema.sql` |
| Rôle détaillé des sondes et codes de réponse | Section [Sondes](#sondes) ; [contrat applicatif](../architecture.md#contrat-applicatif) |
| Disque `vdb`, `/var/lib/opsdesk` | Section Serveurs ci-dessus ; décision « Stockage de la base » |
| Heure de 02:00, minuteur systemd, 7 copies, format custom | Section [Sauvegarde et restauration](#sauvegarde-et-restauration) ; décision « Sauvegarde et restauration » |
| Fichiers `.tf`, état, inventaire, playbooks, secrets | Carte « Ressources de contrôle » ; [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md), sections 6.2 et 6.3 ; exercices 04 et 05 |
| SSH par clé, `root` sans connexion SSH, clés hors de Git | Section Serveurs ; décision « Réseau, accès et protections » |
| Première image construite sur `srv-app` | Texte sous la chaîne GitHub ; section [Première livraison](#première-livraison-et-livraisons-suivantes) ; décision « Première image » ; exercice 06 |
| Choix de la version, contrôle de `/health/ready`, retour arrière | Carte « Version publiée sur GHCR, récupérée par Podman » ; décisions « Déploiement » et « Retour arrière applicatif » ; exercice 08 |
| Reprise de `srv-admin` (état Terraform, clés) | Décision « Reprise de `srv-admin` » ; guide du laboratoire, section 8 |
| Prometheus : 15 s, 15 jours, deux règles d'alerte, `node_exporter` ; contenu des tableaux Grafana | Décision « Supervision » ; exercice 09 |
| Deployment, Service, sondes lues par K3s | Exercice 07 |
| Dimensionnement de k6 (un vCPU) | Décision « Essai de charge » ; exercice 09 |
| Ports et règles firewalld | [Matrice des flux réseau](#matrice-des-flux-réseau) |
| Récit en dix phrases des versions précédentes | Remplacé par les trois zones et le [tableau des flux](#flux-du-schéma-technique) |

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

Les logos et pictogrammes des deux schémas sont des images PNG intégrées aux sources `.drawio` et aux `.svg`. Leur provenance et leur licence ne sont pas vérifiées. Les marques appartiennent à leurs titulaires ; les logos servent seulement à nommer les outils. Avant toute réutilisation, les remplacer par les logos officiels de chaque outil, en SVG, avec leur source et leur version.

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
| Flux et libellés | Tableau des flux ci-dessus, décisions du [registre d'architecture](../architecture.md#décisions-retenues) |

## Modifier et exporter

1. Ouvrir le `.drawio` dans diagrams.net et modifier.
2. *Fichier → Exporter en → SVG*, sans l'option « Inclure une copie de mon diagramme ». Le texte alternatif de la page devient le `<title>` du SVG.
3. Enregistrer le `.drawio` et le SVG dans le même commit.

Chaque bloc (zone, carte, colonne de machine, bandeau) contient ses éléments : le déplacer dans l'éditeur déplace son contenu. Chaque flèche est attachée à ses deux blocs ; ses coudes intermédiaires et les libellés de flèche ne suivent pas : après un déplacement, les reprendre à la main.

Les sources portent `adaptiveColors="none"` : sans ce réglage, diagrams.net en thème sombre inverse les couleurs et les logos sombres deviennent presque invisibles. Les cadres de texte sont ajustés à leur contenu.

Les deux SVG sont exportés depuis les `.drawio` par le moteur d'export de Draw.io 32.6.10 (page d'export du dépôt jgraph/drawio, Chromium sans interface), en thème clair et sans bordure. Cet export ne remplace pas l'ouverture des fichiers dans l'application.

## Contrôles

Réalisés le 13 novembre 2026 sur la version des deux schémas livrée après deux audits externes. Dernière correction du schéma technique : les flèches `/metrics` aboutissent sur la carte OpsDesk de `srv-app` et sur le Pod de la copie, et le flux de restauration porte le libellé « pg_restore → PostgreSQL » ; aucun composant ni cadre n'a été ajouté, aucune VM n'a été déplacée.

- script de contrôle des sources `.drawio` : 0 anomalie et 0 avertissement sur les deux schémas ; il mesure la géométrie, les polices, les contrastes (seuil WCAG AA de 4,5:1), l'attache des flèches et les croisements ; il ne juge ni le rendu réel ni la justesse des faits ;
- ouverture des deux `.drawio` dans l'application Draw.io sous Windows : affichage identique à l'export, aucun élément ne dépasse de la page ; rien n'a été enregistré ;
- export des SVG par le moteur Draw.io 32.6.10, sans `<foreignObject>` ;
- plus petite police : 14 px ; canevas de 1920 × 1400 px (technique) et de 1640 × 1080 px (présentation) ;
- comptes : technique, 111 textes, 453 mots, 16 icônes, 27 flèches ou traits dont 18 attachés ; présentation, 62 textes, 215 mots, 15 icônes, 5 flèches ou traits ;
- ordre des VM : `srv-admin`, `srv-app`, `srv-k3s` de gauche à droite, soit piloter, exécuter, orchestrer ; une seule ligne SSH relie `srv-admin` à ses deux voisines ;
- un seul croisement de flèches (SSH et images GHCR), marqué par un saut d'arc.

Limites connues :

- le trajet de la flèche `/metrics` vers `srv-app` compte sept points dans des couloirs étroits (22 px sous la carte PostgreSQL 17) : déplacer une carte oblige à le reprendre ;
- la restauration est dessinée au niveau de la machine ; son libellé nomme PostgreSQL ;
- la première livraison n'a pas de flèche propre ;
- le script de contrôle ne détecte pas une flèche qui s'arrête à côté de la carte qu'elle devrait viser : ce contrôle est visuel.

Non vérifiés : affichage réel dans GitHub et Notion, thèmes clair et sombre, application mobile, provenance et licence des logos, libellés et textes lus un à un dans Draw.io. Ces contrôles portent sur le dessin : aucune des trois VM n'existe.
