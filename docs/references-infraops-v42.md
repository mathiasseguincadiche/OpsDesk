# Provenance des références InfraOps V4.2

Ces fichiers ont été préparés par **Codex avant la séparation des responsabilités V4.4**. Les notes antérieures indiquent une conservation locale aux chemins ci-dessous, pour consultation après tentative personnelle ou diagnostic ciblé. Ces fichiers InfraOps sont absents de `main` `51e1a489` contrôlé le 4 novembre 2026 ; la disponibilité de leurs originaux hors dépôt est **NON VÉRIFIÉE** dans cette passe. Aucune exécution historique ne valide une compétence de Mathias.

La préparation applicative antérieure n’a pas publié leurs fichiers actifs Terraform, Ansible, Docker/Compose, Kubernetes, CI/CD ou exploitation. Cette page décrit leur antériorité ; les noms ci-dessous ne sont pas des liens vers des solutions à recopier ni des fichiers promis dans la branche applicative. Cette passe ne déplace ni ne supprime les sources ou preuves accessibles et ne prétend pas avoir contrôlé une sauvegarde externe.

| Famille | Chemin historique local | Fonction et validation historique | Reprise personnelle |
|---|---|---|---|
| infra_conteneurs_codex | `.dockerignore` | Recette du laboratoire de développement Codex ; pas une réalisation de Mathias | Exercice 06 : écrire sa recette à partir du contrat applicatif |
| infra_cicd_codex | `.github/workflows/verify.yml` | Candidat local, aucune pipeline distante validée ; aucun fichier CI actif fourni dans cette préparation | Exercice 08 : construire et expliquer ses jobs, artefacts et erreurs |
| infra_cicd_codex | `.gitlab-ci.yml` | Candidat local, aucune pipeline distante validée ; aucun fichier CI actif fourni dans cette préparation | Exercice 08 : construire et expliquer ses jobs, artefacts et erreurs |
| infra_conteneurs_codex | `Dockerfile` | Recette du laboratoire de développement Codex ; pas une réalisation de Mathias | Exercice 06 : écrire sa recette à partir du contrat applicatif |
| infra_conteneurs_codex | `compose.yaml` | Recette du laboratoire de développement Codex ; pas une réalisation de Mathias | Exercice 06 : écrire sa recette à partir du contrat applicatif |
| infra_ansible_codex | `infra/ansible/inventory.yml` | Rendu localhost nonsecret ; seconde passe sans changement, aucun serveur configuré | Exercice 05 : inventaire/playbook personnel, configuration cible et idempotence |
| infra_ansible_codex | `infra/ansible/render.yml` | Rendu localhost nonsecret ; seconde passe sans changement, aucun serveur configuré | Exercice 05 : inventaire/playbook personnel, configuration cible et idempotence |
| infra_ansible_codex | `infra/ansible/templates/opsdesk-contract.json.j2` | Rendu localhost nonsecret ; seconde passe sans changement, aucun serveur configuré | Exercice 05 : inventaire/playbook personnel, configuration cible et idempotence |
| infra_terraform_codex | `infra/terraform/main.tf` | Contrat terraform_data local seulement ; aucun provisioning VM/cloud | Exercices 04/02 : choisir fournisseur, écrire ressources et expliquer state/plan |
| infra_automatisation_exploitation_codex | `infra/verify.py` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |
| infra_automatisation_exploitation_codex | `infra/verify_k8s.py` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |
| infra_kubernetes_codex | `k8s/delivery-rbac.yaml` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_kubernetes_codex | `k8s/init-configmap.json` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_kubernetes_codex | `k8s/kustomization.yaml` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_kubernetes_codex | `k8s/namespace.yaml` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_kubernetes_codex | `k8s/policies.yaml` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_kubernetes_codex | `k8s/runtime.yaml` | Candidat, au plus rendu hors cluster ; aucune infrastructure K3s réalisée | Exercice 07 : ressources et diagnostics K3s personnels sous réserve de faisabilité |
| infra_automatisation_exploitation_codex | `scripts/check.py` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |
| infra_automatisation_exploitation_codex | `scripts/prepare-local.sh` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |
| infra_automatisation_exploitation_codex | `scripts/probe.py` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |
| infra_automatisation_exploitation_codex | `scripts/recovery_lab.py` | Contrôle, sonde, livraison ou reprise du laboratoire Codex ; portée dans les preuves historiques | Exercices 08–12 : livrer, observer, maintenir et rétablir personnellement |

Le code applicatif, ses migrations et ses tests restent du périmètre développeur. Les décisions définitives d’infrastructure, permissions système, stockage, sauvegarde et exploitation appartiennent à Mathias. Les comptes de démonstration et preuves applicatives actuelles sont eux aussi produits par Codex, sans niveau personnel attribué.

## Diagnostic CI à traiter après une tentative

Dans le candidat OpsDesk historique, la commande de smoke écrit ci-business.json tandis que la reprise lit business-smoke.json et peut sélectionner un ticket issu d’un ancien essai. Impact : erreur 404 sur base CI neuve ou fausse association de preuve. Critères de correction à démontrer personnellement : une source de référence du run, même identifiant créé puis relu, séparation des preuves courantes/historiques, commit/run identifiés et échec visible si le contrôle échoue. Aucune correction ni exécution de ce pipeline n’est réalisée dans la préparation V4.4.

## Proposition de rangement, non appliquée

Une copie explicitement étiquetée de ces références pourrait être placée dans un espace de corrigés distinct, après examen de son périmètre. Les originaux garderaient leurs empreintes et leur provenance. Aucun déplacement physique, nettoyage de volume ou activation automatique n’est nécessaire pour commencer l’apprentissage.
