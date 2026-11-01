# OpsDesk — état réel et preuves

**Référence documentaire : 1er novembre 2026.** Ce dépôt vient d’être créé. Les documents de conception ne valent pas implémentation.

## Niveaux de maturité

- **Prévu** : fonctionnalité définie ou architecture dessinée.
- **En cours** : fichiers de travail présents, mais fonctionnement pas encore confirmé.
- **Implémenté** : code/configuration disponible, exécuté avec vérification locale.
- **Vérifié** : résultat reproduit, daté et documenté, avec commande/scénario, preuve, limite et commit.

| Élément | Statut | Ce qu’il faudra vérifier |
| --- | --- | --- |
| Application tickets + PostgreSQL | Prévu | Création, liste, changement d’état, données conservées après redémarrage |
| Docker Compose | Prévu | Démarrage reproductible, santé, réseau interne, arrêt propre |
| Tests et GitHub Actions | Prévu | Tests réels exécutés, échec bloquant visible |
| Image GHCR et analyse Trivy | Prévu | Tag immuable, rapport et traitement des résultats |
| Terraform AWS | Prévu | Format/validation/plan puis application autorisée et destruction |
| Ansible et Rocky Linux | Prévu | Durcissement contrôlé, seconde exécution idempotente |
| K3s | Prévu | Déploiement, sondes, stockage et retour arrière |
| Prometheus, Grafana, alertes, journaux | Prévu | Indicateurs, alerte provoquée, diagnostic vérifiable |
| k6 | Prévu | Profil de charge, critères, mesures et interprétation |

**Aucune phase technique n’est actuellement déclarée terminée.** Cette page doit être actualisée après chaque vraie validation, et non au moment où un fichier est seulement écrit.

## Journal de preuves à remplir

| Date UTC | Commit / version | Scénario | Résultat obtenu | Pièce de preuve | Limites |
| --- | --- | --- | --- | --- | --- |
| — | — | Aucune exécution vérifiée à ce jour | — | — | — |

Des captures non datées ou des exemples de commande ne suffisent pas. Expliquer aussi les échecs rencontrés et leur résolution.