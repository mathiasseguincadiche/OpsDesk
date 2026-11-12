# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles phases mènent de l'application à une infrastructure exploitée ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Comment l'application est construite, ce qu'a montré l'essai historique et ce que le laboratoire personnel doit accueillir. |

## Lire les schémas

- **Cadre à trait plein :** existe dans le dépôt (l'application et sa base).
- **Cadre à points fins (technique) :** référence historique, observée hors du dépôt.
- **Cadre ou tuile en pointillé :** prévu, pas encore réalisé. Une couleur seule ne dit jamais l'avancement.
- **Pastille numérotée (présentation) :** ordre des trois phases. Le schéma technique n'en a pas : il montre des emplacements, pas une chronologie.
- **Flèche pleine :** échange entre composants (HTTP, SQL) ou montage d'un volume.
- **Flèche pointillée :** enchaînement ou livraison prévus.

Les trois phases reprennent celles du [parcours](../parcours-apprentissage.md) et de Notion : conteneurisation et livraison automatisée, infrastructure et automatisation, orchestration, observabilité et fiabilité. Le schéma technique ne décide pas de la topologie du laboratoire : la case « exécution d'OpsDesk » reste à décider à l'exercice 02. Aucun des deux schémas n'affirme un déploiement, une preuve ou une mise en production.

## Logos et pictogrammes

Les logos proviennent du paquet [simple-icons](https://github.com/simple-icons/simple-icons) 13.21.0, dont les fichiers sont publiés sous licence CC0. Les marques appartiennent à leurs titulaires ; les logos servent seulement à nommer les outils.

| Outil | Fichier source | Couleur d'origine |
| --- | --- | --- |
| Flask | `flask.svg` | #000000 |
| PostgreSQL | `postgresql.svg` | #4169E1 |
| Docker | `docker.svg` | #2496ED |
| GitHub Actions | `githubactions.svg` | #2088FF |
| GHCR (GitHub) | `github.svg` | #181717 |
| Trivy | `trivy.svg` | #1904DA |
| AWS | `amazonwebservices.svg` | #232F3E |
| Terraform | `terraform.svg` | #844FBA |
| Rocky Linux | `rockylinux.svg` | #10B981 |
| Ansible | `ansible.svg` | #EE0000 |
| K3s | `k3s.svg` | #FFC61C |
| Prometheus | `prometheus.svg` | #E6522C |
| Grafana | `grafana.svg` | #F46800 |
| k6 | `k6.svg` | #7D64FF |
| Fedora | `fedora.svg` | #51A2DA |
| QEMU (pour KVM, QEMU et libvirt) | `qemu.svg` | #FF6600 |

Les pictogrammes de la personne, du navigateur, du bouclier (durcissement), des journaux, de l'alerte et du volume sont dessinés pour ce projet et suivent la licence MIT du dépôt.

## Modifier et exporter

1. Ouvrir le `.drawio` dans diagrams.net et modifier.
2. *Fichier → Exporter → SVG*, sans l'option « Inclure une copie de mon diagramme ».
3. Rouvrir le SVG, ajouter `role="img"`, un `<title>` et un `<desc>`, puis vérifier le rendu.

Pour les deux schémas, le `.drawio` et le SVG décrivent la même figure ; le SVG a été produit à partir de la même description que le `.drawio`, pas par le menu d'export de diagrams.net.

## Contrôles

Réalisés le 12 novembre 2026 :

- rendu des SVG dans Chromium : aucun texte ne dépasse son cadre (mesure des boîtes de texte) ;
- contrastes calculés sur les deux schémas : texte courant entre 6,7:1 et 16:1, titres colorés et chiffres des pastilles au moins 4,7:1 (seuil WCAG AA : 4,5:1) ;
- fichiers XML valides ;
- les deux `.drawio` ouverts dans diagrams.net : rendu identique aux SVG.

Restent à faire : affichage dans GitHub et Notion à largeur étroite, thème sombre.
