# OpsDesk — préparation fournie et parcours personnel

La V4.4 sépare la réception de l’application et la réalisation des exercices. Une case de préparation Codex ne vaut pas validation personnelle de Mathias.

## Préparation applicative Codex

- Sources Flask, pages/API et règles de tickets conservées ; dépendances verrouillées et schéma métier autonome fourni.
- Contrôle Host et refus CSRF non ASCII testés ; nom du rôle PostgreSQL configurable par `DB_USER`.
- Tests HTTP/SQL et relecture d’un ticket committé ajoutés ; résultats courants dans `evidence/v44/`, premier échec conservé.
- Contrat applicatif à30 rubriques et documentation réconciliés ; alertes de sécurité conservées.
- Parcours et preuves historiques conservés avec leur provenance ; aucune réalisation InfraOps personnelle anticipée.

## Ordre de travail de Mathias

1. Comprendre l’application et lire son contrat.
2. Concevoir son architecture et justifier ressources, flux, accès et stockage.
3. Préparer Linux/Rocky et le réseau du laboratoire autorisé.
4. Écrire son Terraform, lire le plan et vérifier les ressources réellement provisionnées.
5. Écrire son Ansible, contrôler les changements puis la seconde passe.
6. Conteneuriser l’application, choisir ses volumes/réseaux/secrets et vérifier le ticket.
7. Pratiquer Kubernetes/K3s : ressources, probes, stockage, rollout et diagnostic.
8. Construire sa CI/CD à partir d’une livraison manuelle comprise ; étudier le défaut de référence du candidat historique.
9. Choisir des signaux utiles, construire sa supervision et vérifier une alerte.
10. Préparer une maintenance Day-2 et contrôler le service avant/après.
11. Concevoir et exécuter sa sauvegarde et sa restauration isolée ; vérifier les tickets.
12. Diagnostiquer un cas nouveau et rétablir le besoin utilisateur.
13. Réutiliser les acquis sur une tâche de transfert et expliquer ses choix avec une aide limitée.

**Tous ces exercices sont à faire personnellement ; aucun niveau n’est présumé.** OpsDesk propose un accompagnement guidé. BankFlow demandera plus de choix personnels et LogiTrack davantage de réutilisation autonome.

Les anciennes solutions restent accessibles comme références après une première tentative ; elles ne sont pas les fichiers obligatoires à recopier. Toute ressource payante, exposition réelle, destruction ou nettoyage demande son périmètre et l’accord approprié. Ce document ne lance aucun exercice.

[Contrat](docs/contrat-applicatif.md) · [Parcours](docs/parcours-apprentissage.md) · [Provenance](docs/provenance.md)
