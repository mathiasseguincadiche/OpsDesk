# Migrations versionnées du schéma PostgreSQL

En production, OpsDesk **n'effectue plus de changement de schéma automatique au démarrage**. L'opérateur doit exécuter la migration Alembic, vérifier la révision et disposer d'une sauvegarde restaurable. Le mode laboratoire conserve son démarrage simple en `development`.

## Nouvelle base, strictement vierge

Définir d'abord les variables de connexion et les secrets hors Git. Depuis `backend/` :

```bash
python -m alembic current
python -m alembic upgrade head
python -m alembic check
python -m alembic current
```

Les commandes doivent cibler la base attendue ; une commande validée sur runner n'autorise pas la même opération sur un serveur sans vérification.

## Base existante sans table alembic_version

1. Arrêter les écritures, effectuer une sauvegarde et restaurer dans une base isolée.
2. Comparer les tables, contraintes, index, types et relations à la révision initiale versionnée.
3. Après **validation explicite et documentée** du schéma, exécuter `python -m alembic stamp head` sur la copie seulement. `stamp` n'applique aucune modification ; il inscrit simplement la révision.
4. Vérifier `python -m alembic check` puis tester l'application, la persistance et la reprise.
5. Reproduire sur la cible choisie uniquement avec fenêtre de maintenance, sauvegarde qualifiée et plan de retour arrière.

**Ne jamais lancer `alembic upgrade head` sur une base existante non estampillée** : la première révision tente de créer des tables déjà présentes. L'API refuse volontairement de démarrer en mode production si la révision attendue est absente ou divergente. Les fichiers `alembic.ini` et `migrations/` sont intégrés à l'image Docker API (sans dépendre des sources du runner). Le [test de production en CI](../scripts/check_production_migrations.sh) vérifie l'échec avant migration, l'application des deux révisions et la création d'un administrateur dans une base PostgreSQL isolée.

Les migrations futures sont relues manuellement (autogénération non fiable pour certaines contraintes). Le retour arrière de la première révision n'est volontairement pas destructif : en cas d'incident, restaurer la sauvegarde validée.

[Contrat](contrat-applicatif.md) · [Exploitation](exploitation-day2.md) · [Reprise](reprise.md)
