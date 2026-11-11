# Schémas OpsDesk

| Schéma | Source | Export | Usage |
|---|---|---|---|
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Vue du service et des trois phases, pour le README |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Chemin d’une demande en cinq étapes, pour `docs/architecture.md` |

La source `.drawio` fait foi. Pour modifier un schéma, l’ouvrir dans Draw.io, puis exporter en SVG : `drawio -x -f svg -o schema.svg schema.drawio`. Après chaque export, ajouter les balises `title` et `desc` du SVG, puis l’ouvrir dans un navigateur et dans un second visionneur, en thème clair et sombre. Les SVG actuels ont été exportés avec le moteur de rendu de Draw.io 16.0.0 ; un export par l’application de bureau peut différer légèrement (non vérifié).

## Lecture

Un cadre plein est observé dans l’essai Codex historique ou fourni et testé ; un cadre pointillé reste à concevoir et à réaliser par Mathias. Dans le schéma technique, une pastille en haut à droite d’un cadre donne l’ordre de l’étape ; dans le schéma de présentation, elle donne le numéro de la phase. La couleur indique la fonction et est toujours doublée par le libellé du bloc. Les schémas ne prouvent aucun déploiement.

## Icônes

| Icône | Origine | Licence |
|---|---|---|
| Navigateur (ordinateur), disque, clé | Bibliothèques de formes intégrées à Draw.io 16.0.0 (`mxgraph.office.devices.laptop`, `mxgraph.office.devices.hard_disk`, `mxgraph.office.security.key_permissions`) | Draw.io : Apache 2.0 |
| Docker, Flask, Gunicorn, PostgreSQL, GitHub, Terraform, Ansible, K3s, Rocky Linux, Fedora, QEMU, Grafana | Simple Icons 16.37.0 (`simple-icons` sur npm), SVG embarqués avec la couleur officielle de la marque | CC0 pour la collection ; les marques appartiennent à leurs propriétaires |

Le logo QEMU représente aussi KVM et libvirt, faute de logo dédié. Les logos ne figurent pas dans les bibliothèques de Draw.io : ils sont embarqués dans les fichiers, sans référence externe.
