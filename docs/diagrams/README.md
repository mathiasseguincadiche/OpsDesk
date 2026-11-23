# Schémas techniques d'OpsDesk

Ce dossier rassemble les schémas **du produit et de son architecture**, pas les supports de formation personnelle. Chaque schéma technique conserve sa source modifiable `.drawio` et son export `.svg`. La vue globale V2 est publiée en PNG. Les schémas de cours ont été transférés au [wiki Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223), avec leurs sources, sans supprimer les preuves historiques.

## Vues disponibles

La **vue globale de l’architecture V2** présente Terraform sur Fedora, HTTPS, GHCR privé, Borg, K3s et les réseaux internes. Les quatre autres paires documentent l'application et ses usages et sont conservées. Les décisions de référence sont les [sept ADR](../adr/README.md), la [matrice des flux](../architecture-v2-flux.md) et le [plan phases 0 à 6](../architecture-v2-deploiement.md). Aucun de ces schémas n'est une preuve de déploiement ; une inspection graphique native finale des sources Draw.io reste nécessaire avant publication comme plan visuel certifié.

| Schéma | Utilité |
| --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Finalité du produit, acteurs et principaux composants |
| [Présentation mobile](presentation-mobile.svg) ([source](presentation-mobile.drawio)) | Variante lisible sur petit écran |
| [Architecture globale V2](architecture-globale.png) ([source](architecture-globale.drawio)) | Vue synthétique : Fedora / Terraform, trois VM, HTTPS, GHCR privé, Borg et statut cible |
| [Séquence de consultation](sequence-consultation.svg) ([source](sequence-consultation.drawio)) | Chemin d'une requête authentifiée |
| [Diagnostic par couches](diagnostic-service.svg) ([source](diagnostic-service.drawio)) | Triage technique d'un incident de service |

## Convention et limites

- Un cadre désigne une frontière (hôte, VM, réseau ou service) ; une flèche indique le sens du flux.
- Sur la vue globale **Architecture V2**, les frontières des VM et les flux sont représentés **en traits continus**, avec des couleurs distinctes pour l'applicatif, l'administration, l'observabilité et les sauvegardes. Cette convention présente l'architecture cible validée ; elle ne prouve pas son déploiement sur Fedora/Rocky. Le socle applicatif a été contrôlé séparément sur runner.
- Un schéma décrit une intention et une structure ; il ne prouve ni le déploiement ni la sécurité. Le [statut vérifié](../../STATUS.md) fait foi.
- Le fichier `.drawio` est la source éditable. Modifier un SVG seul ne suffit pas à maintenir la paire cohérente.

## Conventions de lecture de la vue globale publique

- La composition de la **vue globale officielle retenue** est conservée, mais toutes les responsabilités techniques relèvent des **sept ADR V2**.
- Les cadres et les flux sont en **traits continus**. Bleu : applicatif ; turquoise : administration et pulls de conteneurs ; magenta : observabilité ; orange : sauvegarde ; vert : données.
- La distribution des images utilise des connexions sortantes et ne nécessite pas d'accès SSH entrant de la CI.
- La copie d'essai et l'observabilité sont isolées du service principal ; leurs paramètres détaillés restent dans le dossier personnel.
- Les métriques ne sont collectées que par les consommateurs autorisés ; le schéma public ne constitue pas une matrice réseau.
- Les sauvegardes sont externalisées et protégées ; leurs paramètres et procédures de reprise restent personnels.
- Le PNG fourni sert de visuel de référence sur GitHub. Le fichier Draw.io conserve une version éditable du schéma. Les ADR V2 documentent les décisions techniques.

## Modifier et vérifier un schéma

1. Ouvrir le fichier `.drawio` correspondant dans diagrams.net / Draw.io.
2. Vérifier la cohérence de la vue globale avec les [ADR V2 publics](../adr/README.md) et les [principes de flux](../architecture-v2-flux.md), sans publier les règles exactes du laboratoire.
3. Exporter en SVG depuis Draw.io ; relire le résultat à taille normale et en thème clair/sombre.
4. Conserver les deux fichiers et exécuter `python3 scripts/check_docs.py` depuis la racine.

L'ancien générateur de schémas, mêlant vues techniques et pédagogiques, est [archivé dans Notion avec ses sources](https://app.notion.com/p/42065721fa18812e9541ff18d825885f). Les fichiers `.drawio` restent disponibles pour les modifications.

Les contrôles automatiques valident les chemins, la syntaxe XML et la présence des sources. Ils ne certifient ni le rendu mobile ni la justesse des architectures.

## Séparation des périmètres public et privé

La **vue globale** seule est autorisée dans GitHub. La **vue détaillée personnelle**, contenant les paramètres et flux d'exploitation, est conservée dans une page Notion personnelle privée distincte. Ne pas y faire référence par un lien public, ne pas publier de fichier détaillé dans le dépôt et ne pas créer d'aperçu CI associé.

**Limite de confidentialité :** les anciennes versions de la vue détaillée restent potentiellement accessibles dans l'historique Git public, les anciennes PR et leurs artefacts. Supprimer les fichiers de la branche courante n'efface pas cet historique et ne protège pas les secrets qui auraient pu y figurer ; les informations concernées doivent être évaluées séparément.
