# Schémas techniques d'OpsDesk

Ce dossier rassemble les schémas **du produit et de son architecture**, pas les supports de formation personnelle. Chaque schéma technique conserve sa source modifiable `.drawio` et son export `.svg`. Les schémas de cours ont été transférés au [wiki Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223), avec leurs sources, sans supprimer les preuves historiques.

## Vues disponibles

**Architecture V2 :** les paires **architecture globale** et **architecture détaillée** sont actualisées avec les nouvelles responsabilités (Terraform sur Fedora), HTTPS, GHCR privé, Borg, K3s et réseaux internes. Les autres quatre paires documentent l'application et ses usages et sont conservées. Les décisions de référence sont les [sept ADR](../adr/README.md), la [matrice des flux](../architecture-v2-flux.md) et le [plan phases 0 à 6](../architecture-v2-deploiement.md). Aucun de ces schémas n'est une preuve de déploiement ; une inspection graphique native finale des sources Draw.io reste nécessaire avant publication comme plan visuel certifié.

| Schéma | Utilité |
| --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Finalité du produit, acteurs et principaux composants |
| [Présentation mobile](presentation-mobile.svg) ([source](presentation-mobile.drawio)) | Variante lisible sur petit écran |
| [Architecture globale V2](architecture-globale.svg) ([source](architecture-globale.drawio)) | Vue synthétique : Fedora / Terraform, trois VM, HTTPS, GHCR privé, Borg et statut cible |
| [Architecture détaillée V2](architecture.svg) ([source](architecture.drawio)) | Réseau, ports, frontières, Nginx/React, FastAPI, PostgreSQL, K3s et sauvegardes |
| [Séquence de consultation](sequence-consultation.svg) ([source](sequence-consultation.drawio)) | Chemin d'une requête authentifiée |
| [Diagnostic par couches](diagnostic-service.svg) ([source](diagnostic-service.drawio)) | Triage technique d'un incident de service |

## Convention et limites

- Un cadre désigne une frontière (hôte, VM, réseau ou service) ; une flèche indique le sens du flux.
- Sur les deux vues **Architecture V2**, les frontières de VM et les flux d'exploitation prévus sont en pointillés : ils ne sont **pas** exécutés sur Fedora/Rocky. Le socle applicatif a été contrôlé séparément sur runner ; les traits internes décrivent son chemin de données.
- Un schéma décrit une intention et une structure ; il ne prouve ni le déploiement ni la sécurité. Le [statut vérifié](../../STATUS.md) fait foi.
- Le fichier `.drawio` est la source éditable. Modifier un SVG seul ne suffit pas à maintenir la paire cohérente.

## Modifier et vérifier un schéma

1. Ouvrir le fichier `.drawio` correspondant dans diagrams.net / Draw.io.
2. Vérifier les ports et flux d'infrastructure auprès des [ADR V2](../adr/README.md) et de la [matrice V2](../architecture-v2-flux.md) ; distinguer `compose.yaml` **local** (`127.0.0.1:8080`) du futur Compose **serveur** (HTTPS :443).
3. Exporter en SVG depuis Draw.io ; relire le résultat à taille normale et en thème clair/sombre.
4. Conserver les deux fichiers et exécuter `python3 scripts/check_docs.py` depuis la racine.

L'ancien générateur de schémas, mêlant vues techniques et pédagogiques, est [archivé dans Notion avec ses sources](https://app.notion.com/p/42065721fa18812e9541ff18d825885f). Les fichiers `.drawio` du présent dépôt restent les sources de référence pour la maintenance des vues techniques.

Les contrôles automatiques valident les chemins, la syntaxe XML et la présence des sources. Ils ne certifient ni le rendu mobile ni la justesse des architectures.
