# Schémas techniques d'OpsDesk

Ce dossier rassemble les schémas **du produit et de son architecture**, pas les supports de formation personnelle. Chaque schéma technique conserve sa source modifiable `.drawio` et son export `.svg`. Les schémas de cours ont été transférés au [wiki Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223), avec leurs sources, sans supprimer les preuves historiques.

## Vues disponibles

**Attention :** les schémas d'infrastructure existants reflètent une **cible antérieure**. Les nouvelles décisions **Architecture V2** sont définies par les [sept ADR](../adr/README.md), la [matrice de flux](../architecture-v2-flux.md) et le [plan de déploiement](../architecture-v2-deploiement.md). Les paires `.drawio` / `.svg` devront être mises à jour et inspectées graphiquement dans un lot séparé **avant** de présenter les vues comme Architecture V2. Les schémas existants ne sont pas des preuves de déploiement.

| Schéma | Utilité |
| --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Finalité du produit, acteurs et principaux composants |
| [Présentation mobile](presentation-mobile.svg) ([source](presentation-mobile.drawio)) | Variante lisible sur petit écran |
| [Architecture globale](architecture-globale.svg) ([source](architecture-globale.drawio)) | VM, réseaux et principaux échanges |
| [Architecture détaillée](architecture.svg) ([source](architecture.drawio)) | Composants, ports, frontières et responsabilités |
| [Séquence de consultation](sequence-consultation.svg) ([source](sequence-consultation.drawio)) | Chemin d'une requête authentifiée |
| [Diagnostic par couches](diagnostic-service.svg) ([source](diagnostic-service.drawio)) | Triage technique d'un incident de service |

## Convention et limites

- Un cadre désigne une frontière (hôte, VM, réseau ou service) ; une flèche indique le sens du flux.
- Le trait plein représente l'application et les flux réellement contrôlés ; les éléments pointillés représentent la cible InfraOps prévue, non réalisée.
- Un schéma décrit une intention et une structure ; il ne prouve ni le déploiement ni la sécurité. Le [statut vérifié](../../STATUS.md) fait foi.
- Le fichier `.drawio` est la source éditable. Modifier un SVG seul ne suffit pas à maintenir la paire cohérente.

## Modifier et vérifier un schéma

1. Ouvrir le fichier `.drawio` correspondant dans diagrams.net / Draw.io.
2. Vérifier ports, identités et flux auprès de [`compose.yaml`](../../compose.yaml), de la [référence technique](../reference-technique.md) et des [décisions](../architecture.md).
3. Exporter en SVG depuis Draw.io ; relire le résultat à taille normale et en thème clair/sombre.
4. Conserver les deux fichiers et exécuter `python3 scripts/check_docs.py` depuis la racine.

L'ancien générateur de schémas, mêlant vues techniques et pédagogiques, est [archivé dans Notion avec ses sources](https://app.notion.com/p/42065721fa18812e9541ff18d825885f). Les fichiers `.drawio` du présent dépôt restent les sources de référence pour la maintenance des vues techniques.

Les contrôles automatiques valident les chemins, la syntaxe XML et la présence des sources. Ils ne certifient ni le rendu mobile ni la justesse des architectures.
