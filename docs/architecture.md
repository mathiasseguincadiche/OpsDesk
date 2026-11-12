# Architecture opérationnelle d’OpsDesk

**Architecture retenue pour OpsDesk :** une application Flask et PostgreSQL, deux serveurs Rocky Linux 10.2 hébergés sur un poste Fedora, une chaîne de livraison, une sauvegarde et une supervision. Ces choix sont retenus et non vérifiés : aucun n’est encore réalisé. L’essai historique (Ubuntu/WSL2 et Docker Compose) reste une référence, décrite plus bas. Le [contrat autonome](contrat-applicatif.md) porte les besoins à satisfaire.

> **Essai historique.** Les recettes Compose/Docker et les manifests cités ne sont pas présents dans `main` `51e1a489`. Le service observé, son réseau et ses volumes appartiennent à l’essai Ubuntu/WSL documenté par les preuves ; il ne constitue pas une procédure exécutable ni la cible Fedora/KVM/Rocky.

## Besoin et choix de l’essai historique

Un collaborateur doit ouvrir une demande et l’équipe IT doit retrouver son état. Les tickets doivent rester dans une base indépendante de l’image applicative ; l’opérateur doit pouvoir reconnaître une mauvaise livraison et localiser une panne.

| Besoin | Décision du support ou choix historique | Alternative et compromis | Vérification |
|---|---|---|---|
| Petite application compréhensible | Flask, rendu HTML côté serveur et API JSON | Une SPA ajouterait un build et du code métier sans bénéfice pour ce premier lab | UI HTTP et parcours API dans le smoke |
| Donnée relationnelle durable | PostgreSQL 17.11, volume nommé | SQLite simplifierait le démarrage mais ne montrerait pas le flux réseau app → DB attendu | Création puis relecture d’un ticket ; redémarrage/restauration à vérifier séparément |
| Serveur HTTP de l’image | Gunicorn, un worker et quatre threads | Le serveur de développement Flask ne constitue pas le serveur de livraison | Readiness et réponses HTTP dans l’image |
| Laboratoire local reproductible | Docker Compose, secrets en fichiers locaux | Compose n’offre ni cluster ni disponibilité professionnelle | `compose up --wait` et test métier |
| Réduire l’exposition | Port `127.0.0.1:18081` seulement ; aucune publication DB | L’absence d’authentification interdit une exposition Internet | Contrôler la configuration et les ports réellement publiés |

Les alternatives ci-dessus servent à comprendre les compromis. Les sources consultées ne prouvent pas qu’une comparaison formelle SPA/Flask ou SQLite/PostgreSQL a été menée par l’apprenant ; ce ne sont pas ses arbitrages personnels. Pour le choix technique initial détaillé, la raison effectivement consignée reste limitée aux documents disponibles, sans reconstitution rétrospective.

## Architecture technique

![Architecture technique d’OpsDesk en trois cadres, un par phase. Phase 1 : GitHub Actions publie l’image sur GHCR ; la sauvegarde de 02:00 est copiée hors du serveur. Phase 2, srv-app : le navigateur appelle l’application Gunicorn et Flask et ses trois sondes, qui lit et écrit dans PostgreSQL ; la restauration refait le serveur et remet la base. Phase 3, srv-k3s : K3s, Prometheus et Grafana lisent les sondes et les mesures](diagrams/architecture-technique.svg)

Le schéma est découpé en trois cadres, un par phase : livraison et sauvegarde en haut, `srv-app` au milieu, `srv-k3s` en bas. La requête de l’utilisateur traverse le cadre du milieu, du navigateur à la base. Les numéros de 1 à 7 se lisent dans l’ordre. Le [détail des routes, sondes, colonnes, ports et sauvegardes](diagrams/README.md#détail-des-éléments-du-schéma-technique) est dans le README des schémas.

- **Livraison (phase 1) :** GitHub Actions lance les tests `unittest`, construit l’image, l’analyse avec Trivy et la publie sur GHCR. `srv-app` tire cette image.
- **Service (phase 2) :** `srv-app` exécute l’application et la base dans deux conteneurs, `app` et `db`, avec Podman et Quadlet. Le mot de passe de la base est un fichier secret. Le port 8000 est ouvert à l’hôte et à `srv-k3s` ; le port 5432 n’est pas publié.
- **Sauvegarde (phase 1) :** `pg_dump` chaque nuit à 02:00, 7 copies gardées, copiées par `rsync` sur SSH vers `~/sauvegardes` sur l’hôte. **Restauration (phase 2) :** refaire le serveur avec Terraform et Ansible, restaurer avec `pg_restore`, puis contrôler `/health/ready`.
- **Supervision (phase 3) :** `srv-k3s` porte K3s avec Traefik, Prometheus et Grafana. K3s lit `/health/live` et `/health/ready` ; Prometheus lit `/metrics` toutes les 15 secondes et garde 15 jours de mesures ; `node_exporter` mesure les deux serveurs. Deux règles d’alerte Prometheus : base indisponible depuis 1 minute, erreurs 5xx en hausse.

**Portée et limites :** ce dessin montre l’architecture retenue, pas un service réalisé. Tous les éléments des phases 1 à 3 sont au statut Prévu et au contrôle Non vérifié ([STATUS](../STATUS.md)). Données fictives et absence d’authentification utilisateur. Un réseau de laboratoire n’est pas une frontière de sécurité forte. Aucune qualification de production n’est déduite de ce schéma.

## Essai historique : composants et relations

Dans la configuration historique (Ubuntu/WSL2, Docker Compose), le navigateur utilisait `127.0.0.1:18081` en HTTP ; Docker redirigeait vers le port `8000` du service `app`. Le service `app` résolvait `db` dans le réseau Compose du projet et se connectait au port interne `5432`. Le rôle SQL `opsdesk_app` a les droits nécessaires aux tickets sans être le propriétaire d’initialisation : c’est une **propriété de PostgreSQL**, pas une étape de circulation. PostgreSQL utilisait un volume nommé, montage de l’hôte, hors du réseau logique ; la persistance ne prouve ni une sauvegarde indépendante ni une restauration réussie.

Ce dessin décrivait un essai, pas un service actuel. PostgreSQL n’était pas publié sur l’hôte dans la configuration de référence. Un réseau Compose n’est pas une frontière de sécurité forte. Le pilote Python `psycopg` fait partie de l’application ; il ne représente ni un protocole ni un service réseau indépendant.

## Contrat applicatif

| Entrée | Rôle |
|---|---|
| `GET /tickets` et pages de détail | Interface de création et suivi |
| `GET/POST /api/tickets` | Liste/création JSON, entrées bornées |
| `GET/PATCH /api/tickets/{id}` | Lecture et progression contrôlée du statut |
| `GET /health/live` | Le processus peut répondre ; ne prouve pas la DB |
| `GET /health/ready` | Connexion DB et table tickets consultables |
| `GET /version` | Version et révision déclarées réellement servies |
| `GET /metrics` | Compteurs de requêtes et disponibilité DB ; pas un système d’alertes |

Les statuts progressent **open → in_progress → closed**. Sauter une étape ou rouvrir un ticket clôturé est refusé ; répéter le même statut conserve sa valeur métier mais actualise `updated_at` ; ce n’est pas une idempotence complète du document HTTP. Les requêtes SQL transmettent les valeurs comme paramètres, sans concaténation SQL.

## Trois phases, sans changer d’application

- **Point de départ, réalisé :** application et PostgreSQL locaux, parcours positif et négatif, vérifiés par les tests ([STATUS](../STATUS.md)).
- **Phase 1, livrer et conserver — prévue :** conteneur, livraison automatisée, analyse de l’image et sauvegarde de la base.
- **Phase 2, préparer et automatiser — prévue :** Terraform et Ansible, serveur `srv-app` sur Rocky Linux, restauration ; AWS seulement si budget et autorisation sont établis.
- **Phase 3, orchestrer et maintenir — prévue :** K3s sur `srv-k3s`, sondes, Prometheus, Grafana, test de charge k6, incident et retour à l’état sain.

K3s ne remplace ni PostgreSQL, ni ses sauvegardes, ni les tests métier. Un rollback de Deployment ne restaure pas une base ou un volume. Les manifestes et configurations candidats ne sont pas des preuves d’exécution.

## Décisions retenues

« Retenu » est l’état d’une décision, pas la preuve de son exécution. Les décisions du 4 novembre 2026 viennent du mandat de finalisation ; celles du 12 novembre 2026 ont été prises avant toute réalisation, pour ne pas ralentir l’apprentissage par des choix techniques : l’exercice 02 sert à les relire, les justifier et les vérifier. Les détails non établis restent non documentés.

| Décision et état | Contexte, choix et alternatives | Conséquence et source |
|---|---|---|
| Un dépôt / un service / trois phases — retenu | Le mandat conserve OpsDesk et exclut le retour aux trois anciens dépôts spécialisés | Code et preuves restent ensemble ; anciens noms historiques. [Provenance](provenance.md) et mandat utilisateur |
| GitHub seul actif — retenu | GitLab reste une archive facultative ; pas de miroir ni de CI supplémentaire | Évite deux flux à synchroniser ; accès au dépôt privé requis. Mandat utilisateur et README |
| Application fournie / infrastructure personnelle — retenu | Apprendre le métier en construisant et vérifiant soi-même ; écarter les fichiers InfraOps finaux copiés avant tentative | Aide graduée, effort et preuve personnels ; [parcours](apprentissage/README.md) et contrat |
| Usage local fictif sans authentification — retenu dans le périmètre courant | Le programme ne gère pas de comptes ; une future utilisation partagée exige une décision applicative distincte | Exposition Internet bloquée ; pas de promesse de production. [Contrat §23](contrat-applicatif.md#23-sessions-et-authentification) |
| Fedora/KVM/Rocky — cible prévue, réception non vérifiée | Cible personnelle donnée par le mandat ; raison détaillée du choix de ces distributions plutôt que d’autres : non documentée dans les sources consultées | Compatibilités à recevoir ; AWS facultatif. [Guide laboratoire](laboratoire-fedora-kvm-rocky.md) |
| Deux serveurs Rocky Linux 10.2 sur l’hôte Fedora — retenu, non vérifié (12 novembre 2026) | `srv-app` (192.168.150.10 ; 2 vCPU, 4 Go ; disque système 20 Go) porte l’application et la base ; `srv-k3s` (192.168.150.20 ; 2 vCPU, 6 Go ; 30 Go) porte K3s et la supervision. Écartés : une seule VM, qui mélange l’application et le cluster ; trois VM ou plus, trop gourmandes en mémoire pour un seul poste | Un serveur se reconstruit sans toucher l’autre ; 10 Go de mémoire pris à l’hôte. [Guide laboratoire](laboratoire-fedora-kvm-rocky.md) |
| Réseau, accès et protections — retenu, non vérifié (12 novembre 2026) | Réseau libvirt NAT dédié `opsdesk-lan` (192.168.150.0/24) ; utilisateur `mathias` ; SSH par clé, sans mot de passe ni connexion root ; SELinux Enforcing ; firewalld : 22 pour l’hôte seul, 8000 pour l’hôte et `srv-k3s`, 5432 non publié, 9100 pour `srv-k3s`, 80 et 6443 pour l’hôte. Écartés : le réseau `default` de libvirt, dont la configuration n’est pas maîtrisée ; un pont sur le réseau local, qui exposerait les VM ; désactiver SELinux ou le pare-feu | Les VM sont joignables depuis l’hôte seulement. Chaque port ouvert a une raison écrite |
| Exécution : Podman et Quadlet — retenu, non vérifié (12 novembre 2026) | Deux conteneurs, `app` et `db`, gérés par des unités systemd ; mot de passe de la base dans un fichier secret. Écarté : Docker Compose, qui ajoute un démon et s’éloigne des outils natifs de Rocky Linux | Compose reste la référence de l’essai historique, pas la cible |
| Stockage de la base — retenu, non vérifié (12 novembre 2026) | Disque de données séparé de 10 Go (`vdb`), monté sur `/var/lib/opsdesk`. Écarté : données sur le disque système | Les données sont séparées du système ; ce disque ne remplace pas la sauvegarde |
| Terraform et Ansible — retenu, non vérifié (12 novembre 2026) | Terraform avec le fournisseur libvirt et un état local crée les deux VM ; Ansible, avec des rôles, les configure. Écartés : virt-manager à la main, non reproductible ; un état distant, inutile avec un seul poste | L’état Terraform reste local et n’est pas publié |
| Livraison : GitHub Actions et GHCR — retenu, non vérifié (12 novembre 2026) | Tests `unittest`, construction de l’image, analyse Trivy, publication sur GHCR. Écarté : GitLab CI, puisque GitHub est seul actif | `srv-app` tire l’image publiée |
| Sauvegarde et restauration — retenu, non vérifié (12 novembre 2026) | `pg_dump` chaque nuit à 02:00 par un minuteur systemd, 7 copies gardées, `rsync` sur SSH vers `~/sauvegardes` sur l’hôte. Restauration : refaire le serveur avec Terraform et Ansible, `pg_restore`, puis contrôle de `/health/ready`. Écartés : copier le dossier de données pendant que la base tourne ; garder les copies sur la même VM | Une copie hors du serveur survit à la perte de la VM. La restauration reste à vérifier |
| Supervision — retenu, non vérifié (12 novembre 2026) | K3s sur un seul nœud avec Traefik ; Prometheus (lecture toutes les 15 secondes, 15 jours de mesures) et Grafana dans K3s ; `node_exporter` sur les deux serveurs ; deux règles d’alerte : base indisponible depuis 1 minute, erreurs 5xx en hausse. Écartés : Alertmanager et Loki, deux composants de plus sans changer l’essentiel ; un cluster à plusieurs nœuds, trop gourmand en mémoire | Les alertes se lisent dans Prometheus et Grafana ; aucun message n’est envoyé |
| AWS — facultatif, en dernier (12 novembre 2026) | Une instance `t3.micro` à Paris, seulement si budget et autorisation sont établis. Alternative : rester sur le laboratoire local | Aucune ressource payante sans accord préalable |

Pour une nouvelle décision coûteuse à inverser, ajouter date, contexte sourcé, choix, options écartées et conséquences positives/négatives. Une décision remplacée reste présente avec son état « remplacée » et le lien vers la suivante. Ne pas inventer la raison d’une décision ancienne pour compléter le tableau.

## Origine réelle des fichiers de schéma

Deux figures servent désormais des objectifs distincts : [présentation](diagrams/presentation.drawio) / [SVG](diagrams/presentation.svg) et [technique](diagrams/architecture-technique.drawio) / [SVG](diagrams/architecture-technique.svg). Les anciennes figures restent accessibles dans l’historique Git, sans suppression des preuves ni des limites techniques dans les documents.

**Recette graphique partielle :** les SVG sont produits à partir de la même description que les sources `.drawio` (12 novembre 2026). Aucune collision de texte n'a été observée dans un rendu Chromium. Il reste à contrôler la lisibilité dans GitHub et Notion, en thèmes clair et sombre. Voir la [recette de validation](diagrams/README.md).

## Références primaires

[Déploiement Flask](https://flask.palletsprojects.com/en/stable/deploying/) · [Paramètres SQL Psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html) · [Image PostgreSQL et persistance](https://hub.docker.com/_/postgres)
