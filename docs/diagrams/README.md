# Schémas OpsDesk — présentation et technique

| Vue | Source modifiable | Visuel de consultation | Fonction |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | À quoi sert le service, quels acteurs et quelles données essentielles ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Où se trouvent les services et comment communiquent-ils pendant l’essai historique ? |

Ces figures documentent le service et l’essai local sous Ubuntu/WSL2 ; elles ne prouvent ni un déploiement personnel, ni une disponibilité actuelle, ni une production sécurisée. Les trois phases pédagogiques et la cible Fedora/KVM/Rocky/Terraform/Ansible/K3s/Grafana sont détaillées dans le [parcours](../parcours-apprentissage.md), pas dans la topologie historique.

## Conventions

- **Flèche pleine :** interaction ou communication entre éléments.
- **Trait pointillé :** montage de stockage ; pas « prévu » et pas un flux réseau.
- **Zone du réseau Compose :** regroupement logique des services app et db ; ce n’est pas une frontière de sécurité forte.
- **Volume hors du réseau :** données persistantes montées sur l’hôte ; aucune sauvegarde ni restauration n’est démontrée par ce seul volume.
- **Sans pastilles numérotées :** les figures représentent des composants, pas cinq opérations chronologiques. Les permissions du rôle SQL sont une propriété de la base.
- **Couleurs :** elles distinguent des fonctions, toujours nommées par du texte ; aucun état d’avancement n’est déduit d’une couleur.

Les noms de services, les ports et le rôle SQL proviennent de la documentation de l’essai historique, avec les réserves de [l’architecture](../architecture.md), de l’[état](../../STATUS.md) et des [preuves](../preuves.md). Les nouvelles configurations personnelles devront être vérifiées sur leurs environnements réels.

## Limites et conservation de l’information

Le prototype utilise des données fictives et ne dispose pas d’authentification utilisateur. La liaison historique `127.0.0.1:18081` vers `8000` doit être confirmée par la configuration et par un contrôle d’écoute dans un environnement effectivement exécuté. Aucune publication publique ou qualification de production n’est attestée. Les anciennes figures peuvent être retrouvées dans l’historique Git.

## Source éditable, SVG et recette

Les `.drawio` sont les sources éditables. Les SVG en sont exportés avec le moteur de rendu de l'application web diagrams.net (version 32.7.1), appelé par script le 11 novembre 2026, sans copie du diagramme incluse dans le fichier, en variante claire. Un titre et une description textuelle ont été ajoutés ensuite pour l'accessibilité. Ce ne sont donc pas des fichiers produits à la main, mais ils ne proviennent pas non plus du menu *Fichier → Exporter* : refaire l'export par ce menu reste possible et doit donner le même rendu.

Contrôles réalisés le 11 novembre 2026 :

- les deux `.drawio` s'ouvrent dans diagrams.net et affichent les blocs, flèches, libellés et cadres attendus ;
- les deux SVG exportés ont été rendus comme images dans Chromium : aucune collision de texte observée.

Contrôles restant à faire :

1. Mesurer les contrastes et vérifier les polices.
2. Vérifier l'image réellement insérée dans GitHub et Notion, à largeur normale et étroite, en thème clair et sombre.
3. Consigner pour chaque contrôle l'outil utilisé, la date, le résultat observable et les limites. Ne pas confondre XML valide, rendu SVG et test d'usage.

Les SVG incluent un fond opaque, un titre et une description textuelle. Leur présence ne suffit pas à démontrer l'accessibilité complète du diagramme.
