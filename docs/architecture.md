# Architecture opérationnelle d’OpsDesk

**architecture interne de l’application et référence du laboratoire de développement historique.** La cible d’hébergement reste à concevoir personnellement par l’apprenant. Les choix Compose, noms de ressources et ports ci-dessous décrivent cet essai historique ; ils ne sont pas une architecture personnelle déjà réalisée ou imposée. Le [contrat autonome](contrat-applicatif.md) porte les besoins à satisfaire.

> **Lecture des schémas : référence historique.** Les recettes Compose/Docker et les manifests cités ne sont pas présents dans `main` `51e1a489`. Le service observé, son réseau et ses volumes appartiennent à l’essai Ubuntu/WSL documenté par les preuves ; cette page ne constitue pas une procédure exécutable ni la cible Fedora/KVM/Rocky personnelle.

## Besoin et choix

Un collaborateur doit ouvrir une demande et l’équipe IT doit retrouver son état. Les tickets doivent rester dans une base indépendante de l’image applicative ; l’opérateur doit pouvoir reconnaître une mauvaise livraison et localiser une panne.

| Besoin | Décision du support ou choix historique | Alternative et compromis | Vérification |
|---|---|---|---|
| Petite application compréhensible | Flask, rendu HTML côté serveur et API JSON | Une SPA ajouterait un build et du code métier sans bénéfice pour ce premier lab | UI HTTP et parcours API dans le smoke |
| Donnée relationnelle durable | PostgreSQL 17.11, volume nommé | SQLite simplifierait le démarrage mais ne montrerait pas le flux réseau app → DB attendu | Création puis relecture d’un ticket ; redémarrage/restauration à vérifier séparément |
| Serveur HTTP de l’image | Gunicorn, un worker et quatre threads | Le serveur de développement Flask ne constitue pas le serveur de livraison | Readiness et réponses HTTP dans l’image |
| Laboratoire local reproductible | Docker Compose, secrets en fichiers locaux | Compose n’offre ni cluster ni disponibilité professionnelle | `compose up --wait` et test métier |
| Réduire l’exposition | Port `127.0.0.1:18081` seulement ; aucune publication DB | L’absence d’authentification interdit une exposition Internet | Contrôler la configuration et les ports réellement publiés |

Les alternatives ci-dessus servent à comprendre les compromis. Les sources consultées ne prouvent pas qu’une comparaison formelle SPA/Flask ou SQLite/PostgreSQL a été menée par l’apprenant ; ce ne sont pas ses arbitrages personnels. Pour le choix technique initial détaillé, la raison effectivement consignée reste limitée aux documents disponibles, sans reconstitution rétrospective.

## Déploiement de l’essai historique — composants et relations

![Architecture technique : l’application Flask et PostgreSQL du dépôt, la référence historique Ubuntu/WSL2 avec Docker Compose, et le laboratoire personnel prévu sur Fedora, KVM et Rocky Linux](diagrams/architecture-technique.svg)

Cette **vue de déploiement statique** indique où résident les composants et comment ils sont reliés. Elle ne constitue pas une séquence chronologique numérotée.

- **Accès :** dans la configuration historique, le navigateur utilise `127.0.0.1:18081` en HTTP ; Docker redirige vers le port `8000` du service `app`. L’adresse saisie ne prouve pas à elle seule l’interface d’écoute réelle ; il faut vérifier la configuration et l’environnement d’exécution.
- **Application :** Gunicorn sert Flask et les fonctionnalités de tickets. Le pilote Python `psycopg` fait partie de l’application ; il ne représente ni un protocole ni un service réseau indépendant.
- **Base :** le service `app` résout `db` dans le réseau Compose `v42opsdesk_net` et se connecte au port interne `5432`. Le rôle SQL `opsdesk_app` a les droits nécessaires aux tickets sans être le propriétaire d’initialisation : c’est une **propriété de PostgreSQL**, pas une étape de circulation.
- **Stockage :** PostgreSQL utilise le volume nommé `v42opsdesk_pgdata`. Il s’agit d’un **montage de l’hôte**, hors du réseau logique. La persistance ne prouve ni une sauvegarde indépendante ni une restauration réussie.

**Portée et limites :** ce dessin décrit l’essai Ubuntu/WSL2 historique, pas un service actuel ni une infrastructure personnelle reçue. Données fictives et absence d’authentification utilisateur. PostgreSQL n’était pas publié sur l’hôte dans la configuration de référence. Un réseau Compose n’est pas une frontière de sécurité forte. Aucune qualification de production n’est déduite de ce schéma.

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
- **Phase 1, livrer et conserver — prévue :** conteneur, livraison automatisée et analyse de l’image.
- **Phase 2, préparer et automatiser — prévue :** Terraform et Ansible sur Rocky Linux ; AWS seulement si budget et autorisation sont établis.
- **Phase 3, orchestrer et maintenir — prévue :** K3s, services, stockage, probes, observabilité, incident et retour à l’état sain.

K3s ne remplace ni PostgreSQL, ni ses sauvegardes, ni les tests métier. Un rollback de Deployment ne restaure pas une base ou un volume. Les manifestes et configurations candidats ne sont pas des preuves d’exécution.

## Décisions durables et décisions encore personnelles

Ce registre conserve les choix établis ; il ne reconstitue pas les arbitrages d’une infrastructure que l’apprenant n’a pas encore conçue. « Retenu » est l’état d’une décision, pas la preuve de son exécution. Les raisons ci-dessous viennent du mandat de finalisation du 4 novembre 2026 et des sources citées ; les détails non établis restent non documentés.

| Décision et état | Contexte, choix et alternatives | Conséquence et source |
|---|---|---|
| Un dépôt / un service / trois phases — retenu | Le mandat conserve OpsDesk et exclut le retour aux trois anciens dépôts spécialisés | Code et preuves restent ensemble ; anciens noms historiques. [Provenance](provenance.md) et mandat utilisateur |
| GitHub seul actif — retenu | GitLab reste une archive facultative ; pas de miroir ni de CI supplémentaire | Évite deux flux à synchroniser ; accès au dépôt privé requis. Mandat utilisateur et README |
| Application fournie / infrastructure personnelle — retenu | Apprendre le métier en concevant et vérifiant soi-même ; écarter les fichiers InfraOps finaux copiés avant tentative | Aide graduée, effort et preuve personnels ; [parcours](apprentissage/README.md) et contrat |
| Usage local fictif sans authentification — retenu dans le périmètre courant | Le programme ne gère pas de comptes ; une future utilisation partagée exige une décision applicative distincte | Exposition Internet bloquée ; pas de promesse de production. [Contrat §23](contrat-applicatif.md#23-sessions-et-authentification) |
| Fedora/KVM/Rocky — cible prévue, réception non vérifiée | Cible personnelle donnée par le mandat ; raison détaillée du choix de ces distributions plutôt que d’autres : non documentée dans les sources consultées | Compatibilités à recevoir ; AWS facultatif. [Guide laboratoire](laboratoire-fedora-kvm-rocky.md) |
| Topologie, stockage, providers et accès personnels — à décider | L’exercice 02 appartient à l’apprenant ; aucune ancienne recette ne vaut décision personnelle | Documenter options, conséquences, version et contrôles après sa proposition |

Pour une nouvelle décision coûteuse à inverser, ajouter date, contexte sourcé, choix, options écartées et conséquences positives/négatives. Une décision remplacée reste présente avec son état « remplacée » et le lien vers la suivante. Ne pas inventer la raison d’une décision ancienne pour compléter le tableau.

## Origine réelle des fichiers de schéma

Deux figures servent désormais des objectifs distincts : [présentation](diagrams/presentation.drawio) / [SVG](diagrams/presentation.svg) et [technique](diagrams/architecture-technique.drawio) / [SVG](diagrams/architecture-technique.svg). Les anciennes figures restent accessibles dans l’historique Git, sans suppression des preuves ni des limites techniques dans les documents.

**Recette graphique partielle :** les SVG sont produits à partir de la même description que les sources `.drawio` (12 novembre 2026). Aucune collision de texte n'a été observée dans un rendu Chromium. Il reste à contrôler la lisibilité dans GitHub et Notion, en thèmes clair et sombre. Voir la [recette de validation](diagrams/README.md).

## Références primaires

[Déploiement Flask](https://flask.palletsprojects.com/en/stable/deploying/) · [Paramètres SQL Psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html) · [Image PostgreSQL et persistance](https://hub.docker.com/_/postgres)
