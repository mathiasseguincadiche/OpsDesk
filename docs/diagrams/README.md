# Schémas techniques d'OpsDesk

Ce dossier rassemble les schémas **du produit et de son architecture**, pas les supports de formation personnelle. La [vue globale V3](architecture-globale-v3.svg) est publiée en SVG avec sa [source Draw.io](architecture-globale-v3.drawio). Les autres schémas sont publiés en SVG. Les schémas de cours ont été transférés au [wiki Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223), avec leurs sources, sans supprimer les preuves historiques.

## Vues disponibles

La **vue globale de l’architecture V3** présente Terraform et Ansible sur Fedora, supervision indépendante sur srv-ops, HTTPS, GHCR privé, Borg, K3s et les réseaux internes. Les quatre autres paires documentent l'application et ses usages et sont conservées. Les décisions de référence sont les [sept ADR](../adr/README.md), la [principes des flux](../architecture-v3-flux.md) et le [plan phases 0 à 10](../architecture-v3-deploiement.md). Aucun de ces schémas n'est une preuve de déploiement ; une inspection graphique native finale des sources Draw.io reste nécessaire avant publication comme plan visuel certifié.

| Schéma | Utilité |
| --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Finalité du produit, acteurs et principaux composants |
| [Présentation mobile](presentation-mobile.svg) ([source](presentation-mobile.drawio)) | Variante lisible sur petit écran |
| [Architecture globale V3](architecture-globale-v3.svg) ([source](architecture-globale-v3.drawio)) | Vue synthétique : Fedora / Terraform et Ansible, trois VM, HTTPS, GHCR privé, Borg et statut cible |
| [Séquence de consultation](sequence-consultation.svg) ([source](sequence-consultation.drawio)) | Chemin d'une requête authentifiée |
| [Diagnostic par couches](diagnostic-service.svg) ([source](diagnostic-service.drawio)) | Triage technique d'un incident de service |

## Convention et limites

- Un cadre désigne une frontière (hôte, VM, réseau ou service) ; une flèche indique le sens du flux.
- Sur la vue globale **Architecture V3**, les frontières des VM et les flux sont représentés **en traits continus**, avec des couleurs distinctes pour l'applicatif, l'administration, l'observabilité et les sauvegardes. Cette convention présente l'architecture cible validée ; elle ne prouve pas son déploiement sur Fedora/Rocky. Le socle applicatif a été contrôlé séparément sur runner.
- Un schéma décrit une intention et une structure ; il ne prouve ni le déploiement ni la sécurité. Le [statut vérifié](../../STATUS.md) fait foi.
- Le fichier `.drawio` est la source éditable. Vérifier également le visuel publié après chaque modification.

## Conventions de lecture de la vue globale publique

- La vue globale V3 remplace le rendu V2, conservé pour l’historique. Les responsabilités relèvent des sept ADR V3.
- Les cadres et les flux sont en **traits continus**. Bleu : applicatif ; turquoise : administration et pulls de conteneurs ; magenta : observabilité ; orange : sauvegarde ; vert : données.
- La distribution des images utilise des connexions sortantes et ne nécessite pas d'accès SSH entrant de la CI.
- La copie d'essai et l'observabilité sont isolées du service principal ; leurs paramètres détaillés restent dans le dossier personnel.
- Les métriques ne sont collectées que par les consommateurs autorisés ; le schéma public ne constitue pas une matrice réseau.
- Les sauvegardes sont externalisées et protégées ; leurs paramètres et procédures de reprise restent personnels.
- Le SVG fourni sert de visuel de référence sur GitHub. Le fichier Draw.io conserve une version éditable du schéma. Les ADR V3 documentent les décisions techniques.

## Modifier et vérifier un schéma

1. Ouvrir le fichier `.drawio` correspondant dans diagrams.net / Draw.io.
2. Vérifier la cohérence de la vue globale avec les [ADR V3 publics](../adr/README.md) et les [principes de flux](../architecture-v3-flux.md), sans publier les règles exactes du laboratoire.
3. Vérifier le visuel publié à taille normale et en thèmes clair et sombre. Utiliser le SVG publié pour la vue globale et les autres schémas.
4. Conserver la source et le visuel publié, puis exécuter `python3 scripts/check_docs.py` depuis la racine.

L'ancien générateur de schémas, mêlant vues techniques et pédagogiques, est [archivé dans Notion avec ses sources](https://app.notion.com/p/42065721fa18812e9541ff18d825885f). Les fichiers `.drawio` restent disponibles pour les modifications.

Les contrôles automatiques valident les chemins, la syntaxe XML et la présence des sources. Ils ne certifient ni le rendu mobile ni la justesse des architectures.

## Séparation des périmètres public et privé

La **vue globale** seule est autorisée dans GitHub. La **vue détaillée personnelle**, contenant les paramètres et flux d'exploitation, est conservée dans une page Notion personnelle privée distincte. Ne pas y faire référence par un lien public, ne pas publier de fichier détaillé dans le dépôt et ne pas créer d'aperçu CI associé.

**Limite de confidentialité :** les anciennes versions de la vue détaillée restent potentiellement accessibles dans l'historique Git public, les anciennes PR et leurs artefacts. Supprimer les fichiers de la branche courante n'efface pas cet historique et ne protège pas les secrets qui auraient pu y figurer ; les informations concernées doivent être évaluées séparément.
