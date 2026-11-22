# Documents de la version 1

Ces documents décrivaient l'infrastructure, la livraison et la sécurité de la version 1 d'OpsDesk (application Flask, sans authentification). Ils ont été déplacés ici le 18 novembre 2026 : la version 2 les rend obsolètes, et ce qu'ils décrivaient est désormais à construire dans le parcours d'apprentissage. Ils ne sont plus tenus à jour.

| Document | Ce qu'il décrivait | Équivalent pour la version 2 |
| --- | --- | --- |
| [CI](cicd.md) | Commandes et résultats de la CI d'essai | Exercice 08 du [parcours](../../docs/apprentissage/08-cicd.md)  ; aucun pipeline personnel de livraison GHCR n'est encore validé |
| [Infrastructure](infrastructure.md) | Contrat Terraform et Ansible local, candidat K3s | Exercices 04 à 07 ; [registre des décisions](../../docs/architecture.md#décisions-retenues) |
| [Livraison](livraison.md) | Chaîne de livraison et rollback de la v1 | Exercices 08 et 10 ; [contrat applicatif](../../docs/contrat-applicatif.md), points 24 à 26 |
| [Triage de sécurité](triage-securite.md) | Lecture du scan Trivy de l'image v1 | [Sécurité](../../docs/securite.md)  ; les scans ponctuels v2 sont consignés dans [STATUS.md](../../STATUS.md) |
| [Versions](versions.md) | Versions des composants de la v1 et de l'essai | [Contrat applicatif](../../docs/contrat-applicatif.md), points 6 et 7 |

Les preuves de la v1 citées par ces documents sont dans [`legacy/evidence/`](../evidence/).
