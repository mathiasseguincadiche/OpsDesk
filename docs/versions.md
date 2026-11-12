# Versions et périmètres

**les versions et configurations d’infrastructure ci-dessous décrivent l’antériorité historique.** Le [contrat applicatif](contrat-applicatif.md) distingue combinaison testée, paramètres et besoins à satisfaire par l’apprenant. La source actuellement testée est identifiée par ses hashes dans `evidence/v44/application-tests.json`, sans faux SHA publié.

Cette fiche sépare la version déclarée par l’application, les outils de l’essai et les cibles encore à qualifier. Les tags d’images ne sont pas des digests immuables ; relier toute nouvelle livraison au contenu réellement construit.

| Composant | Version/fichier de référence | État et limite |
|---|---|---|
| OpsDesk | `0.1.0` ; première preuve `uncommitted-v42` | Version servie lors du smoke initial ; ce texte n’est pas un commit Git |
| Python app | `3.14.10-slim-trixie` dans `Dockerfile` | Base déclarée du build ; identité et scan de l’image finale à vérifier |
| Flask / Psycopg / Gunicorn | 3.1.3 / 3.3.6 / 26.2.0 dans `requirements.lock` | Dépendances verrouillées avec hashes ; licences conservées |
| PostgreSQL | `17.11-bookworm` dans Compose et candidat K3s | Runtime local exécuté ; stockage de cluster non qualifié |
| Poste d’essai | Ubuntu/WSL2, Docker 29.8.0, Compose 5.5.1 | Ne qualifie pas Fedora/Rocky/Podman rootless |
| Contrat Terraform | Terraform 1.15.8, `terraform_data` intégré | Init/plan/apply répétés sur contrat non secret ; aucun provisionnement |
| Rendu Ansible | core 2.20.1, connexion locale | Rendu JSON et seconde passe sans changement ; aucune configuration Linux distante |
| Manifests K3s | kubectl 1.36.2 / Kustomize 5.8.1 pour le rendu | Treize ressources rendues hors ligne ; version K3s cible NON QUALIFIÉE |
| Pod Security | Candidat `restricted` versionné dans le namespace | Contrôler sa compatibilité avec le vrai cluster avant toute application |
| CI / registre | Candidats historiques `.github/workflows/verify.yml` et `.gitlab-ci.yml`, absents du dépôt courant | Workflow GitHub personnel à construire ; aucun run distant ni registre publié attestés par cette fiche |
| Scan image | Version, base et identité dans le rapport Trivy | Lire le rapport complet et son état ; ne pas conclure « zéro vulnérabilité » |

Une mise à jour bénigne doit préserver le ticket témoin, les variables/Secrets nécessaires et la compatibilité du schéma. Une image saine de retour et une archive restaurable sont deux éléments distincts. [Livraison](livraison.md) · [Day-2](exploitation-day2.md) · [Preuves](preuves.md).
