# Schémas techniques d'OpsDesk

Ce dossier rassemble les schémas **du produit et de son architecture**, pas les supports de formation personnelle. La [vue globale V3](architecture-globale-v3.svg) est publiée en SVG avec sa [source Draw.io](architecture-globale-v3.drawio). Les autres schémas sont publiés en SVG. Le [visuel de présentation V3](../images/opsdesk-presentation-v3.svg) dispose aussi d’une [source Draw.io](../images/opsdesk-presentation-v3.drawio). Les schémas de cours ont été transférés au [wiki Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223), avec leurs sources, sans supprimer les preuves historiques.

## Vues disponibles

La **vue globale de l’architecture V3** présente Terraform et Ansible sur Fedora, administration sur srv-admin, supervision et essais sous K3s, HTTPS, GHCR privé, Borg, K3s et les réseaux internes. Les quatre autres paires documentent l'application et ses usages et sont conservées. Les décisions de référence sont les [sept ADR](../adr/README.md), les [principes des flux](../architecture-v3-flux.md) et le [plan phases 0 à 10](../architecture-v3-deploiement.md). Aucun de ces schémas n'est une preuve de déploiement ; le workflow d’aperçu exporte les deux sources V3 avec Draw.io Desktop sur runner ; une inspection humaine des rendus reste nécessaire avant certification visuelle.

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
- Les cadres et les flux sont en **traits continus**. Bleu : applicatif (HTTPS) ; turquoise : administration, provisionnement et pull des images ; magenta : observabilité ; orange : sauvegarde. La base de données est représentée par un cylindre. Le statut de conception figure dans le badge du schéma.
- La distribution des images utilise des connexions sortantes et ne nécessite pas d'accès SSH entrant de la CI.
- La copie d'essai et l'observabilité sous K3s sont isolées du service principal ; leurs paramètres détaillés restent dans le dossier personnel.
- Les métriques ne sont collectées que par les consommateurs autorisés ; le schéma public ne constitue pas une matrice réseau.
- Les sauvegardes sont externalisées et protégées ; leurs paramètres et procédures de reprise restent personnels.
- Le SVG publié est exporté directement depuis la source `.drawio` par Draw.io Desktop : les deux fichiers représentent le même schéma. Le workflow d'aperçu réexporte les sources en PNG natifs pour contrôler leur rendu.

## Modifier et vérifier un schéma

1. Ouvrir le fichier `.drawio` correspondant dans diagrams.net / Draw.io. Chaque texte, forme, icône et connecteur y est modifiable ; aucun schéma n'est une image collée.
2. Vérifier la cohérence de la vue globale avec les [ADR V3 publics](../adr/README.md) et les [principes de flux](../architecture-v3-flux.md), sans publier les règles exactes du laboratoire.
3. Réexporter le SVG depuis la source, puis contrôler le visuel à taille normale et en thèmes clair et sombre.
4. Conserver la source et le SVG ensemble, puis exécuter `python3 scripts/check_docs.py` depuis la racine.

### Régénérer les SVG depuis les sources Draw.io

Le SVG publié n'est jamais modifié à la main : il est produit à partir du `.drawio` avec Draw.io Desktop, en thème clair et en texte vectoriel. La version de référence est celle du [workflow d'aperçu](../../.github/workflows/diagram-previews.yml), Draw.io Desktop 29.0.3.

Sur Fedora, installer Draw.io Desktop (paquet RPM officiel publié sur GitHub par jgraph, ou Flatpak `com.jgraph.drawio.desktop` depuis Flathub), puis depuis la racine du dépôt :

```bash
# Paquet RPM : la commande s'appelle drawio
DRAWIO=drawio
# Flatpak : DRAWIO="flatpak run com.jgraph.drawio.desktop"

for source in docs/diagrams/architecture-globale-v3.drawio docs/images/opsdesk-presentation-v3.drawio; do
  $DRAWIO --export --format svg --svg-theme light --embed-svg-images \
    --output "${source%.drawio}.svg" "$source"
done
```

Sans session graphique (serveur, conteneur), préfixer la commande par `xvfb-run -a` (`sudo dnf install xorg-x11-server-Xvfb`). Deux exports successifs ne diffèrent que par les identifiants internes des dégradés ; le rendu est identique. L'option `--svg-theme light` fige les couleurs du schéma, qui garde son propre fond en thème sombre.

Les générateurs ayant servi à produire les sources sont conservés dans l'espace Notion personnel avec les [anciens générateurs archivés](https://app.notion.com/p/42065721fa18812e9541ff18d825885f) ; les fichiers `.drawio` du dépôt restent la seule source à modifier.

Les contrôles automatiques valident les chemins, la syntaxe XML et la présence des sources. Ils ne certifient ni le rendu mobile ni la justesse des architectures.

## Séparation des périmètres public et privé

La **vue globale** seule est autorisée dans GitHub. La **vue détaillée personnelle**, contenant les paramètres et flux d'exploitation, est conservée dans une page Notion personnelle privée distincte. Ne pas y faire référence par un lien public, ne pas publier de fichier détaillé dans le dépôt et ne pas créer d'aperçu CI associé.

**Limite de confidentialité :** les anciennes versions de la vue détaillée restent potentiellement accessibles dans l'historique Git public, les anciennes PR et leurs artefacts. Supprimer les fichiers de la branche courante n'efface pas cet historique et ne protège pas les secrets qui auraient pu y figurer ; les informations concernées doivent être évaluées séparément.
