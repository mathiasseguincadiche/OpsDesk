# CI applicative d'OpsDesk

Le workflow [Application quality (no deployment)](../.github/workflows/application-quality.yml) qualifie le **socle applicatif fourni** lorsqu'un fichier pertinent change, sur une pull request ou sur `main`. Il ne construit pas ton laboratoire Fedora/Rocky et ne remplace pas les preuves personnelles.

## Ce qui est contrôlé

| Job | Contrôle | Limites |
| --- | --- | --- |
| API | Ruff et tests avec SQLite **puis** PostgreSQL 17 sur runner Ubuntu | Aucun essai de déploiement Rocky |
| Interface | Installation depuis `package-lock.json`, contrôle TypeScript et build Vite | Recette E2E Chromium séparée dans le job conteneurs ; pas de test sur appareil physique |
| Conteneurs | `docker compose config`, construction, sondes, parcours HTTP fictif, sauvegarde `pg_dump`, restauration isolée, redémarrage API, limitation de connexions et navigation réelle sous Chromium | Exécution sur runner jetable, pas sur `srv-app` ni sur les données réelles |

Le [workflow documentaire](../.github/workflows/docs-quality.yml) reste indépendant : il vérifie les liens, les ancres, les sources Draw.io/SVG et les contrats documentaires.

### Précautions

- Le smoke test `scripts/smoke.py` **crée et clôture un ticket fictif**. Il ne doit être exécuté que sur une base de test.
- `scripts/check_browser_e2e.py` contrôle Chromium sur une pile éphémère : session HttpOnly, CSRF, ticket, rechargement, déconnexion et affichage mobile. Les captures d'écran du navigateur sont des preuves réelles du runner, pas des maquettes.
- `scripts/check_persistence_restore.sh` crée temporairement une base `opsdesk_reprise_ci` dans le conteneur PostgreSQL du runner ; il vérifie la restauration sans écraser la base en service.
- Le contrôle `scripts/check_auth_throttle.py` provoque volontairement des HTTP 429 : ne pas le lancer sur une instance partagée.
- La pile Compose utilisée en CI est la configuration de **démonstration locale**. Ses mots de passe et données fictives ne sont jamais destinés à la production.
- La limitation Nginx porte sur l'adresse IP du pair réseau. En présence d'un proxy ou d'un répartiteur frontal, ses adresses de confiance et la politique de limitation doivent être revues.
- Aucun artefact GHCR ni déploiement n'est créé par ces jobs. Le [workflow de sécurité des images](../.github/workflows/image-security.yml) construit les images et lance Trivy chaque semaine et après les changements concernés (PostgreSQL dérivé et image officielle d'origine, pour comparaison). Les rapports JSON, comptes par gravité et identifiants d'images sont disponibles en artefacts ; la politique CI échoue si une image retenue présente HIGH ou CRITICAL ; [#51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51) est clôturée pour les images exécutées qualifiées. Un scan réussi ne garantit pas l'absence de toute vulnérabilité.
- La CI exécute Alembic sur une base vierge distincte et vérifie **dans l'image Docker** le refus d'un démarrage de production sans migration, les deux révisions, le contrôle de schéma et le démarrage après migration (`scripts/check_production_migrations.sh`). Elle ne teste ni les migrations de données réelles préexistantes, ni la charge, ni une campagne de sécurité complète.
- Les risques résiduels avant un déploiement serveur sont suivis dans [l'issue #68](https://github.com/mathiasseguincadiche/OpsDesk/issues/68).

## Interpréter les résultats

Consulter le dernier run sur le commit étudié, pas une ancienne exécution verte. Un workflow réussi prouve seulement les contrôles explicités ci-dessus. Les preuves d'exploitation réelles, avec leur version et leur cible, se consignent dans [STATUS.md](../STATUS.md) et [Preuves](preuves.md).
