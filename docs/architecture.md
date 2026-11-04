# Architecture opérationnelle d’OpsDesk

**V4.4 : architecture interne de l’application et référence du laboratoire de développement Codex.** La cible d’hébergement reste à concevoir personnellement par Mathias. Les choix Compose, noms de ressources et ports ci-dessous décrivent cet essai historique ; ils ne sont pas une architecture personnelle déjà réalisée ou imposée. Le [contrat autonome](contrat-applicatif.md) porte les besoins à satisfaire.

> **Lecture des schémas : historique Codex.** Les recettes Compose/Docker et les manifests cités ne sont pas présents dans `main` `51e1a489`. Le service observé, son réseau et ses volumes appartiennent à l’essai Ubuntu/WSL documenté par les preuves ; cette page ne constitue pas une procédure exécutable ni la cible Fedora/KVM/Rocky personnelle.

## Besoin et choix

Un collaborateur doit ouvrir une demande et l’équipe IT doit retrouver son état. Les tickets doivent rester dans une base indépendante de l’image applicative ; l’opérateur doit pouvoir reconnaître une mauvaise livraison et localiser une panne.

| Besoin | Décision du support ou choix historique | Alternative et compromis | Vérification |
|---|---|---|---|
| Petite application compréhensible | Flask, rendu HTML côté serveur et API JSON | Une SPA ajouterait un build et du code métier sans bénéfice pour ce premier lab | UI HTTP et parcours API dans le smoke |
| Donnée relationnelle durable | PostgreSQL 17.11, volume nommé | SQLite simplifierait le démarrage mais ne montrerait pas le flux réseau app → DB attendu | Création puis relecture d’un ticket ; redémarrage/restauration à vérifier séparément |
| Serveur HTTP de l’image | Gunicorn, un worker et quatre threads | Le serveur de développement Flask ne constitue pas le serveur de livraison | Readiness et réponses HTTP dans l’image |
| Laboratoire local reproductible | Docker Compose, secrets en fichiers locaux | Compose n’offre ni cluster ni disponibilité professionnelle | `compose up --wait` et test métier |
| Réduire l’exposition | Port `127.0.0.1:18081` seulement ; aucune publication DB | L’absence d’authentification interdit une exposition Internet | Contrôler la configuration et les ports réellement publiés |

Les alternatives ci-dessus servent à comprendre les compromis. Les sources consultées ne prouvent pas qu’une comparaison formelle SPA/Flask ou SQLite/PostgreSQL a été menée par Mathias ; ce ne sont pas ses arbitrages personnels. Pour le choix technique initial détaillé de Codex, la raison effectivement consignée reste limitée aux documents disponibles, sans reconstitution rétrospective.

## Chemin d’une demande

![Architecture du laboratoire réellement exécuté](diagrams/architecture-technique.svg)

1. Le navigateur de la machine de laboratoire contacte `127.0.0.1:18081` en HTTP. Il n’y a pas de DNS public, TLS public, VPC ou Ingress dans cette tranche.
2. Docker transmet au port `8000` du conteneur `app`. Gunicorn sert Flask ; Jinja échappe le contenu HTML.
3. L’application résout **`db`** grâce au DNS du réseau Compose `v42opsdesk_net`, puis contacte PostgreSQL sur `5432`.
4. Le rôle **`opsdesk_app`** possède les droits de lecture/création/modification des tickets, pas ceux du propriétaire d’initialisation.
5. PostgreSQL écrit dans **`v42opsdesk_pgdata`**. Cette persistance ne garantit pas qu’une restauration fonctionne : il faut tester les données et le service après reprise.

Un réseau Compose n’est pas une VM et n’est pas une frontière de sécurité forte. Seul le port applicatif est publié ; ne pas présenter cette topologie comme une architecture de production cloisonnée.

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

- **Phase 1 exécutée partiellement :** application et PostgreSQL locaux, parcours positif et négatif.
- **Phase 2 cible :** Terraform et configuration Ansible sur Rocky ; AWS seulement si budget et autorisation sont établis.
- **Phase 3 cible :** K3s, services, stockage, probes, observabilité, incident et retour à l’état sain.

K3s ne remplace ni PostgreSQL, ni ses sauvegardes, ni les tests métier. Un rollback de Deployment ne restaure pas une base ou un volume. Les manifestes et configurations candidats ne sont pas des preuves d’exécution.

## Décisions durables et décisions encore personnelles

Ce registre conserve les choix établis ; il ne reconstitue pas les arbitrages d’une infrastructure que Mathias n’a pas encore conçue. « Retenu » est l’état d’une décision, pas la preuve de son exécution. Les raisons ci-dessous viennent du mandat de finalisation du 4 novembre 2026 et des sources citées ; les détails non établis restent non documentés.

| Décision et état | Contexte, choix et alternatives | Conséquence et source |
|---|---|---|
| Un dépôt / un service / trois phases — retenu | Le mandat conserve OpsDesk et exclut le retour aux trois anciens dépôts spécialisés | Code et preuves restent ensemble ; anciens noms historiques. [Provenance](provenance.md) et mandat utilisateur |
| GitHub seul actif — retenu | GitLab reste une archive facultative ; pas de miroir ni de CI supplémentaire | Évite deux flux à synchroniser ; accès au dépôt privé requis. Mandat utilisateur et README |
| Application fournie / infrastructure personnelle — retenu | Apprendre le métier en concevant et vérifiant soi-même ; écarter les fichiers InfraOps finaux copiés avant tentative | Aide graduée, effort et preuve personnels ; [parcours](apprentissage/README.md) et contrat |
| Usage local fictif sans authentification — retenu dans le périmètre courant | Le programme ne gère pas de comptes ; une future utilisation partagée exige une décision applicative distincte | Exposition Internet bloquée ; pas de promesse de production. [Contrat §23](contrat-applicatif.md#23-sessions-et-authentification) |
| Fedora/KVM/Rocky — cible prévue, réception non vérifiée | Cible personnelle donnée par le mandat ; raison détaillée du choix de ces distributions plutôt que d’autres : non documentée dans les sources de cette passe | Compatibilités à recevoir ; AWS facultatif. [Guide laboratoire](laboratoire-fedora-kvm-rocky.md) |
| Topologie, stockage, providers et accès personnels — à décider | L’exercice 02 appartient à Mathias ; aucune ancienne recette ne vaut décision personnelle | Documenter options, conséquences, version et contrôles après sa proposition |

Pour une nouvelle décision coûteuse à inverser, ajouter date, contexte sourcé, choix, options écartées et conséquences positives/négatives. Une décision remplacée reste présente avec son état « remplacée » et le lien vers la suivante. Ne pas inventer la raison d’une décision ancienne pour compléter le tableau.

## Origine réelle des fichiers de schéma

Les paires [présentation](diagrams/presentation.drawio) / [SVG](diagrams/presentation.svg) et [technique](diagrams/architecture-technique.drawio) / [SVG](diagrams/architecture-technique.svg) sont produites séparément par [generate.py](diagrams/generate.py). Les SVG sont des représentations autonomes écrites par ce générateur, **pas des exports obtenus en ouvrant les `.drawio` dans diagrams.net**. Un futur export par l’éditeur pourra différer, notamment pour les libellés HTML de la source. Les fichiers et le générateur ne sont pas exécutés ni modifiés par cette passe.

La structure XML, les libellés et le rendu SVG local ont été contrôlés lors de la réception documentaire précédente, pour les hashes indiqués dans son rapport. La réouverture Draw.io et l’affichage natif GitHub/Notion restent non vérifiés. Les libellés, le fond opaque et les flèches n’autorisent aucune affirmation d’architecture personnelle déjà réalisée. Les identifiants internes des deux SVG doivent rester isolés si l’on tente de les intégrer ensemble dans un même document HTML ; leur usage actuel en images distinctes n’équivaut pas à cette intégration.

## Références primaires

[Déploiement Flask](https://flask.palletsprojects.com/en/stable/deploying/) · [Paramètres SQL Psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html) · [Image PostgreSQL et persistance](https://hub.docker.com/_/postgres)
