# Contrat de passation applicative — OpsDesk V4.4

**Destinataire : Mathias, ingénieur InfraOps.** Le code métier, son schéma et les tests sont fournis par Codex. La conception des machines, réseaux, rôles PostgreSQL, conteneurs, K3s, CI/CD, supervision, sauvegardes et exploitation appartient à Mathias. Ce contrat décrit les besoins de l’application ; il ne livre pas cette infrastructure à sa place.

## 1. Présentation

OpsDesk est un petit service de tickets IT : un collaborateur déclare une demande, l’équipe IT la consulte, la prend en charge puis la clôture. Il sert de support métier aux exercices InfraOps. Il n’est pas un produit ITSM complet.

## 2. Utilisateurs et scénarios métier

Dans le laboratoire fictif, tout visiteur local peut lister les demandes, créer un ticket et faire évoluer son état. Le scénario de réception est : création → consultation → prise en charge → clôture → nouvelle consultation. Les identités de collaborateur et de support décrivent des usages, pas des rôles authentifiés déjà implémentés.

## 3. Fonctionnalités disponibles

Pages HTML `/tickets` et `/tickets/<id>` ; API JSON GET/POST `/api/tickets` et GET/PATCH `/api/tickets/<id>`. Le PATCH attend uniquement `status`. Titre : 3–120 caractères ; description : 0–2000 ; priorité : `low`, `normal` ou `high`. Statuts : `open`, `in_progress`, `closed`. Les sauts et réouvertures sont refusés ; la liste se limite aux 100 derniers tickets.

### Référence de l’API locale fournie

Référence de la source V4.4, relue le 4 novembre 2026 : [routes et sérialisation](../app/opsdesk/web.py), [validation et transitions](../app/opsdesk/business.py), [schéma SQL](../db/schema.sql). Les fonctions Python sont internes ; les routes ci-dessous forment l’interface consommée par le laboratoire. Toute évolution de cette interface doit mettre à jour ce contrat dans le même changement ; aucun engagement de compatibilité non démontré n’est annoncé.

**Accès :** aucune authentification ni autorisation utilisateur. Les opérations JSON de création/modification exigent `Content-Type: application/json`, sans jeton CSRF ; les formulaires HTML ont leur propre contrôle CSRF. Un Host non autorisé est refusé en 400, en texte brut. Cette référence ne donne aucune autorisation d’exposition Internet.

| Méthode et chemin | Entrée | Réponse normale, à vérifier sur la cible personnelle |
|---|---|---|
| GET `/api/tickets` | Aucun paramètre requis ; pas de pagination configurable | 200, tableau JSON des 100 derniers tickets au maximum, identifiant décroissant |
| POST `/api/tickets` | Objet JSON décrit ci-dessous | 201, ticket créé ; en-tête Location vers son API ; statut initial `open` |
| GET `/api/tickets/{id}` | Identifiant entier dans le chemin | 200, ticket ; 404 si absent ou chemin non reconnu |
| PATCH `/api/tickets/{id}` | Objet contenant uniquement `status` | 200, ticket modifié ; absence de ticket : 404 ; transition/statut refusé : 409 |

| Champ de création | Type, obligation, défaut et limite |
|---|---|
| `title` | Chaîne obligatoire en pratique : défaut vide, refusé ; 3–120 caractères après retrait des espaces aux extrémités |
| `description` | Chaîne facultative, défaut vide ; 0–2000 caractères après retrait des espaces aux extrémités |
| `priority` | Chaîne facultative, défaut `normal` ; `low`, `normal` ou `high`, sans normalisation automatique |

Les textes refusent NUL et les substituts Unicode isolés. À la création, les autres clés ne sont pas utilisées ; fournir `status` ne choisit pas l’état initial. Pour PATCH, une clé supplémentaire, un objet absent ou une forme autre qu’un objet contenant seulement `status` vaut 400. Les transitions permises sont `open` vers lui-même ou `in_progress`, `in_progress` vers lui-même ou `closed`, et `closed` vers lui-même. Répéter le statut actualise `updated_at` : ce n’est pas une réponse totalement idempotente.

Un ticket renvoyé contient `id` (entier), `title`, `description`, `priority`, `status` (chaînes), `created_at` et `updated_at` (dates sérialisées en UTC). Les identifiants et dates sont produits par PostgreSQL : ne pas les traiter comme des constantes d’un exemple.

**Exemples fictifs de corps JSON, sans requête exécutée ni ticket créé.** Création minimale valide :

```json
{"title": "Écran de laboratoire indisponible"}
```

Modification à proposer seulement après identification d’un ticket fictif `open` :

```json
{"status": "in_progress"}
```

**Erreurs à distinguer :** 400 pour JSON/champ/forme invalide ; 404 pour ticket absent ; 409 pour statut ou transition refusé ; 413 si le corps dépasse 16 Kio ; 415 pour POST/PATCH API sans type JSON ; 503 pour une erreur PostgreSQL gérée. Les erreurs API gérées renvoient un objet `error`, sauf le refus Host en texte brut. Cette liste ne garantit pas qu’une erreur de programmation ne puisse produire un autre statut.

Les routes de diagnostic ne sont pas des preuves métier complètes : `/health/live` répond 200 sans accès DB, `/health/ready` répond 200 si la requête à `tickets` aboutit (503 pour l’erreur SQL gérée), `/version` donne l’identité déclarée. `/metrics` peut répondre **200 avec `opsdesk_database_up 0`** : examiner la valeur et les journaux, pas seulement le statut HTTP. Les compteurs sont propres à chaque worker ; aucune série de durée p95 n’est fournie par cette seule route. Les méthodes exactes et sorties réellement observées seront consignées par Mathias sur sa cible.

## 4. Architecture interne

`app/opsdesk/business.py` porte les validations indépendantes de HTTP. `web.py` relie routes, rendu Jinja, requêtes SQL paramétrées, santé et journaux. `app/wsgi.py` expose l’application au serveur WSGI. Les modèles HTML et le CSS sont fournis sous `app/opsdesk/templates/` et `static/`. La base PostgreSQL contient une table métier `tickets`.

## 5. Langages et frameworks

Python, Flask 3.1.3, Jinja2, psycopg 3.3.6 et Gunicorn 26.2.0. La source des versions résolues est `requirements.lock`. Le contrôle V4.4 utilise Python 3.14.10 de l’image de développement déjà disponible ; une autre version Python n’est pas reçue par cette seule observation.

## 6. Dépendances

Les dépendances directes et transitives sont figées avec leurs hashes PyPI dans `requirements.lock`. PostgreSQL est nécessaire au métier et à la readiness. Les tests de règles pures utilisent uniquement la bibliothèque standard ; les tests HTTP/SQL utilisent les dépendances applicatives. Aucun cloud, registre public ou bibliothèque Terraform/Ansible n’est requis par le code métier.

## 7. Versions compatibles

Combinaison vérifiée : Python 3.14.10, Flask/psycopg/Gunicorn aux versions ci-dessus et PostgreSQL 17.11. Il s’agit de la combinaison réellement testée, pas d’une matrice exhaustive. Aucun support SQLite n’est implémenté. Les autres versions PostgreSQL/Python nécessitent des tests de compatibilité avant adoption.

## 8. Démarrage en développement

Préconditions : PostgreSQL accessible, base et rôle préparés, schéma métier présent, fichiers secrets locaux lisibles et port libre. Mathias préparera les accès et droits ; ce document n’exécute aucune administration de base.

**NON VÉRIFIÉ de bout en bout — méthode native proposée, à préparer personnellement.** Cible : machine personnelle autorisée (la VM Rocky après réception si ce choix est retenu), racine du dépôt, utilisateur ordinaire sans `sudo`. La combinaison historique testée est Python 3.14.10/PostgreSQL 17.11 ; relever les versions de la nouvelle cible. Le premier bloc crée un environnement privé et installe les paquets verrouillés (accès aux paquets nécessaire), puis démarre Gunicorn sur la seule boucle locale de cette machine. Il ne prépare pas la DB, les rôles, le schéma ou les secrets :

```sh
python3 -m venv .local/venv
.local/venv/bin/pip install --require-hashes -r requirements.lock
PYTHONPATH=app .local/venv/bin/gunicorn --bind 127.0.0.1:18081 --workers 1 wsgi:app
```

Définir auparavant les paramètres de la section 11, en particulier les fichiers secrets et l’adresse réelle de PostgreSQL. Ces commandes constituent une méthode de développement ; l’installation native complète n’a pas été exécutée dans cette réception. Les tests V4.4 ont réutilisé ponctuellement l’image et le réseau du laboratoire existant, avec le code actuel monté en lecture seule, sans reconstruire ni redéployer le service. Les anciennes recettes conteneurs demeurent des références historiques de Codex.

Validation attendue après préparation personnelle : `/version` identifie OpsDesk, `/health/ready` répond 200 et le parcours ticket fonctionne. Si le démarrage échoue, distinguer interpréteur/paquets, fichiers secrets, port occupé, nom/port DB, droits et schéma ; conserver l’erreur sans afficher les secrets. Un refus de readiness n’autorise ni désactivation de contrôle ni effacement de volume. Pour arrêter son propre processus lancé au premier plan, utiliser son interruption normale ; ne pas arrêter un service dont on n’a pas identifié le propriétaire. Ces vérifications sont NON EXÉCUTÉES sur le laboratoire personnel.

## 9. Ports et protocoles

Le processus WSGI écoute sur l’adresse/port demandés à Gunicorn ; le choix de bind appartient à l’opérateur. Le laboratoire historique publie HTTP sur `127.0.0.1:18081` et l’application y écoute en interne sur 8000. La connexion SQL utilise TCP PostgreSQL, port par défaut 5432 ; aucun besoin applicatif de publier ce port vers Internet. Aucun TLS applicatif n’est fourni dans le profil local ; la stratégie TLS cible relève de l’architecture de Mathias.

## 10. Paramètres de configuration

La configuration applicative est lue dans l’environnement au démarrage ou à la connexion. La limite HTTP est fixée à 16 Kio. Le secret de session est chargé au démarrage ; le mot de passe DB est relu à chaque connexion. Les validations et transitions métier sont dans le code, pas dans un fichier d’administration d’hôte.

## 11. Variables d’environnement

| Variable | Valeur par défaut / besoin | Effet |
|---|---|---|
| `DB_HOST` | `db` ; adresse à définir pour une autre topologie | Hôte PostgreSQL |
| `DB_PORT` | `5432` | Port SQL |
| `DB_NAME` | `opsdesk` | Base métier |
| `DB_USER` | `opsdesk_app` | Rôle de connexion, configurable sans modifier le code |
| `DB_PASSWORD_FILE` | Obligatoire ; chemin d’un fichier UTF-8, secret d’au moins 32 caractères après trim | Mot de passe du rôle applicatif ; jamais une valeur dans Git |
| `SESSION_SECRET_FILE` | Obligatoire ; même contrainte de longueur | Signature de la session et du jeton CSRF |
| `TRUSTED_HOSTS` | `127.0.0.1,localhost` | Liste d’hôtes HTTP autorisés, séparés par virgules ; ajuster explicitement si une cible personnelle utilise un autre nom |
| `APP_VERSION` | `0.1.0` | Identité applicative déclarée |
| `APP_REVISION` | `uncommitted-v42` | Révision déclarée ; cette valeur historique n’est pas un SHA publié |

Ne pas placer de mot de passe dans les paramètres de commande ou dans une URL. Le contrôle de l’en-tête Host limite les noms acceptés ; il ne remplace ni authentification ni protection réseau.

## 12. Besoins de stockage

Les tickets doivent rester dans PostgreSQL au remplacement du processus applicatif. Le processus web n’écrit pas de fichiers métier : aucun stockage de pièces jointes n’est fourni. Prévoir seulement les fichiers secrets lisibles et les fichiers temporaires nécessaires au serveur Python. Les journaux et leurs politiques de stockage sont un choix d’exploitation distinct.

## 13. Base de données

PostgreSQL, une table `tickets` : identifiant bigint généré, titre, description, priorité, statut et dates `timestamptz`. Le code réalise SELECT, INSERT et UPDATE, ainsi que l’usage de la séquence d’identité. Il ne demande pas DELETE, administration de rôles, création de bases ou superutilisateur. Mathias détermine et applique les droits adaptés ; aucun script de création d’utilisateur n’est imposé par ce contrat.

## 14. Migrations

`db/schema.sql` fournit uniquement le schéma métier initial. Il s’applique une fois à un schéma applicatif vide par une identité autorisée. Il n’y a pas de moteur de migrations incrémentales ni de conversion SQLite. L’ancien `db/001-initial.sql`, cité dans les preuves V4.2, mélangeait création de rôle/droits et schéma. Il est absent du dépôt courant ; sa conservation locale hors dépôt est non vérifiée. Il n’est pas le contrat applicatif à recopier.

Tout changement de schéma futur doit fournir une migration explicite, sa compatibilité avec l’ancienne application, les tests et ses limites de retour. Ne pas remplacer silencieusement une table existante.

## 15. Données persistantes et démonstration

Le ticket et ses dates/statuts sont les données durables. Les données sont strictement fictives. La réception V4.4 ajoute un ticket nommé `FICTIF-V44-…`, volontairement conservé, puis le relit par des connexions distinctes. Les autres tests SQL travaillent principalement sur une table temporaire propre à leur connexion ; ils ne suppriment ni ne réinitialisent les tickets existants.

## 16. Endpoints de santé

`GET /health/live` vérifie le processus et retourne l’identité. `GET /health/ready` interroge la table métier ; indisponibilité PostgreSQL : 503. `GET /version` expose application/version/révision. `GET /metrics` fournit des compteurs par worker et `opsdesk_database_up`. Un code 200 sur live ne démontre pas l’écriture d’un ticket ni une collecte Prometheus déjà construite.

## 17. Journaux applicatifs

Le code journalise méthode, nom de route, statut et durée. L’erreur DB publiée reste générique et le journal d’application ne contient pas DSN, mot de passe ou texte de requête SQL. Gunicorn peut produire ses journaux sur stdout/stderr selon ses options. La rotation, la centralisation, journald et les alertes relèvent de l’exploitation personnelle de Mathias.

## 18. Tests unitaires

`python3 -m unittest discover -s tests/unit -v` vérifie validations, limites et transitions, sans DB. La suite complète a exécuté 26 tests (sept unitaires et dix-neuf HTTP/SQL). Le texte contenant NUL ou un substitut Unicode isolé est refusé en 400 avant PostgreSQL. Les nouveaux tests HTTP/SQL sont dans `tests/integration/test_http_postgres.py`. Le code de test ne doit pas être transformé en pipeline prêt à recopier : Mathias construira ses jobs à partir de commandes qu’il comprend.

## 19. Tests fonctionnels

Les tests de la source actuelle couvrent routes/API, formulaires CSRF dont entrée non ASCII, SQL paramétré, contraintes PostgreSQL, échappement HTML, limites de taille, Host autorisé/refusé, live/ready/version et erreur DB simulée. Un cas dédié relit un ticket committé à travers des connexions distinctes. `scripts/smoke.py` reste un client HTTP applicatif et ajoute deux tickets fictifs sur une instance déjà identifiée ; il ne redéploie pas et ne restaure pas.

## 20. Commandes de vérification

**ACTIF — fichiers de test disponibles ; environnement personnel à préparer, NON EXÉCUTÉ ici.** Depuis la racine de la machine choisie à la section 8, avec son environnement Python, ses dépendances et paramètres préparés, sans privilège système supplémentaire. La dernière commande contacte la boucle locale de cette même machine, qui doit héberger l’instance autorisée :

```sh
PYTHONPATH=app .local/venv/bin/python -m unittest discover -s tests/unit -v
PYTHONPATH=app .local/venv/bin/python -m unittest discover -s tests/integration -v
.local/venv/bin/python scripts/smoke.py --base-url http://127.0.0.1:18081
```

Attendu : sept tests unitaires puis dix-neuf tests HTTP/SQL sans échec ; le smoke affiche un JSON `status: PASS` seulement si son parcours complet réussit. Ce sont des critères attendus, pas un résultat personnel. En cas d’échec, lire d’abord le cas et son erreur, puis séparer paramètre/secret/DB de règle HTTP/métier ; conserver les refus négatifs attendus.

La seconde commande nécessite une base de développement autorisée, des secrets présents et la permission TEMP pour ses tables de test (elle n’est pas un besoin du rôle runtime de production). Elle conserve un ticket témoin ; ne pas l’exécuter sur des données réelles. Lire le rapport `evidence/v44/application-tests.json` et son journal, en distinguant la source montée pour les tests du service historique déjà en cours. Aucun test de redémarrage, sauvegarde ou restauration n’a été relancé sous V4.4.

## 21. Ressources recommandées

Point de départ proposé pour ce petit démonstrateur : un processus applicatif et PostgreSQL, environ 1 vCPU et 512 Mio disponibles pour l’app, puis une enveloppe DB et stockage séparée à mesurer. Ce sont des hypothèses de dimensionnement, pas un benchmark ou un minimum garanti. Les limites, le nombre de workers et la capacité cible seront choisis et testés par Mathias.

## 22. Contraintes de sécurité

Usage local et fictif uniquement ; aucune autorisation d’exposition Internet ou de production. En-têtes de protection, CSRF des formulaires, corps JSON imposé pour l’API mutante, taille limitée, paramètres SQL et hôtes HTTP bornés sont des contrôles applicatifs. Les scans d’image historiques restent défavorables : les occurrences résiduelles et leur contexte sont documentés, sans prétendre exploiter chaque avis. La sécurité de l’hôte, l’image finale, le réseau et les accès restent des exercices personnels.

## 23. Sessions et authentification

**Aucune authentification utilisateur n’est implémentée.** La session Flask stocke le jeton CSRF signé ; ce n’est pas un compte ou un rôle. Les cookies sont HTTPOnly et SameSite=Lax dans le profil local ; aucune garantie TLS/cookie Secure n’est revendiquée. Une authentification de démonstration a été évaluée : elle ajouterait comptes, stockage des mots de passe et gestion de sessions au premier exercice. Le périmètre retenu conserve le démonstrateur local sans auth, affiché comme tel, plutôt qu’une pseudo-sécurité. Une utilisation partagée nécessitera une décision applicative explicite.

## 24. Compatibilité des versions

Version de travail déclarée : 0.1.0, schéma initial inchangé. Les corrections V4.4 ajoutent la configuration `DB_USER`, le contrôle Host et le refus contrôlé d’un CSRF non ASCII ; elles ne transforment ni les tickets ni leurs statuts. La preuve donne les hashes des sources testées. Un label de version ou une révision déclarée ne doit pas être présenté comme un commit publié avant sa création effective.

## 25. Contraintes de mise à jour

Avant de livrer un artefact, vérifier son identité, les paramètres requis, la compatibilité du schéma et le scénario ticket. Les dépendances ne sont pas mises à jour aveuglément. Aucune migration DB ni écrasement des secrets n’est requis pour ces corrections applicatives. Mathias construira et déploiera personnellement l’image de son exercice.

## 26. Conditions de rollback

Les corrections applicatives actuelles n’ont pas de migration de données : une ancienne application utilisant le même schéma peut relire les tickets, sous réserve de ses paramètres. La construction d’images, leur sélection, le rollout/rollback, la CI et le contrôle opérationnel sont à réaliser par Mathias. Un retour de code ne récupère pas des données perdues.

## 27. Conditions de sauvegarde et restauration

Données à protéger : PostgreSQL et les configurations/secrets nécessaires à l’accès et à la session. L’application attend que la même table et les mêmes références métier soient disponibles après reprise. Mathias définira la cohérence, la destination, le chiffrement, la rétention, le RPO/RTO d’exercice et la restauration. Les reprises V4.2 par Codex restent des observations historiques sur le même hôte, sans SLO ni perte physique qualifiée ; elles ne sont pas rejouées ici.

## 28. Dépendances externes

Aucun service financier, cloud ou messagerie n’est appelé. Le développement nécessite l’accès aux paquets Python si leur cache n’est pas disponible. Les accès réseau de l’application sont les requêtes HTTP entrantes et PostgreSQL sortant. Les choix de registre, DNS cible, TLS, supervision et sauvegarde ne sont pas codés comme une infrastructure obligatoire.

## 29. Limites connues

Pas d’auth, d’affectation, de commentaires, de pièces jointes, de recherche/pagination complète ni de suppression de tickets. Les compteurs métriques sont en mémoire de chaque worker. Rejouer le même statut garde le statut mais actualise `updated_at` : ne pas annoncer une idempotence complète du document HTTP. Les tests de disponibilité simulée sont des tests applicatifs, pas un incident réel injecté. Les scans complets et les contraintes d’environnement restent à examiner avant toute évolution du périmètre.

## 30. Critères de réception applicative

Application et routes disponibles dans un environnement identifié ; créer/lire/faire progresser un ticket ; relire une écriture par une autre connexion ; refus attendus cohérents ; pages échappées et CSRF contrôlé ; live/ready/version corrects ; paramètres documentés ; tests reproductibles et datés ; schéma métier distinct de l’administration PostgreSQL ; absence de secret dans les preuves. Une réception applicative ne valide aucun exercice InfraOps ni niveau d’autonomie personnel de Mathias.

[État de réception](../STATUS.md) · [Provenance et références](provenance.md) · [Parcours personnel](parcours-apprentissage.md)
