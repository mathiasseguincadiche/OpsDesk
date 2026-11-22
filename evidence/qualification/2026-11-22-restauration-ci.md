# Qualification de sauvegarde et restauration — 22 novembre 2026

**Source :** [GitHub Actions, run 45006326819](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/45006326819), job « Conteneurs — build, sonde et parcours HTTP » du commit `262cb21a6d1a8d95f7b8a113d7233e26c96d869d`.

**Résultat constaté :** succès des trois jobs (API, frontend, Compose). Le journal du job affiche : `PASS : 17 tickets sauvegardés et restaurés isolément, API rétablie sans perte.`

## Procédure automatisée sur runner jetable

1. Démarrer PostgreSQL, l'API et nginx via le Compose de démonstration ; exécuter le smoke HTTP qui ajoute un ticket fictif.
2. Relever les 17 tickets présents et produire une sauvegarde `pg_dump --format=custom` dans un fichier temporaire.
3. Créer `opsdesk_reprise_ci` dans le même conteneur PostgreSQL, **distincte de la base active**.
4. Restaurer via `pg_restore --no-owner --no-privileges --exit-on-error`.
5. Vérifier le nombre de tickets et le titre accentué du ticket témoin ; supprimer la seule base `opsdesk_reprise_ci`.
6. Redémarrer uniquement l'API, attendre `/health/ready` et vérifier que les 17 tickets demeurent en base.
7. Supprimer la pile jetable et les volumes en fin de workflow.

**Fichier source :** [`scripts/check_persistence_restore.sh`](../../scripts/check_persistence_restore.sh). Ce script exige les identifiants et données fictives de la pile CI.

## Limites de cette preuve

- La sauvegarde est créée dans le runner, pas sur le stockage indépendant d'un serveur de production.
- Le serveur PostgreSQL lui-même n'a pas été restauré sur une VM externe ; seule une nouvelle base du même conteneur a été utilisée.
- Ni chiffrement, ni rétention, ni RPO/RTO, ni reprise après perte de l'hôte ne sont certifiés.
- Le laboratoire Fedora/KVM/Rocky et ses validations personnelles restent **à réaliser**.

Ce résultat complète la qualification du **socle applicatif fourni**, sans revendiquer un PRA personnel.
