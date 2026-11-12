# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles phases mènent de l'application à une infrastructure exploitée ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Où se trouvent les services de l'essai historique et comment communiquent-ils ? |

## Lire la présentation

- **Cadre à trait plein :** existe dans le dépôt (l'application et sa base).
- **Cadre ou tuile en pointillé :** prévu, pas encore réalisé. Une couleur seule ne dit jamais l'avancement.
- **Pastille numérotée :** ordre des trois phases.
- **Flèche pleine :** échange entre composants (HTTP, SQL).
- **Flèche pointillée :** enchaînement prévu entre étapes.

Les trois phases reprennent celles du [parcours](../parcours-apprentissage.md) et de Notion : conteneurisation et livraison automatisée, infrastructure et automatisation, orchestration, observabilité et fiabilité. Le schéma n'affirme ni déploiement, ni preuve, ni mise en production.

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

Les pictogrammes de la personne, du bouclier (durcissement), des journaux et de l'alerte sont dessinés pour ce projet et suivent la licence MIT du dépôt.

## Modifier et exporter

1. Ouvrir le `.drawio` dans diagrams.net et modifier.
2. *Fichier → Exporter → SVG*, sans l'option « Inclure une copie de mon diagramme ».
3. Rouvrir le SVG, ajouter `role="img"`, un `<title>` et un `<desc>`, puis vérifier le rendu.

Le `.drawio` et le SVG de présentation décrivent la même figure ; le SVG a été produit à partir de la même description que le `.drawio`, pas par le menu d'export.

## Contrôles

Réalisés le 12 novembre 2026 sur la présentation :

- rendu du SVG dans Chromium : aucun texte ne dépasse son cadre (mesure des boîtes de texte) ;
- contrastes calculés : texte courant entre 6,9:1 et 16:1, titres de phase et chiffres des pastilles au moins 4,7:1 (seuil WCAG AA : 4,5:1) ;
- fichiers XML valides.

Restent à faire : ouverture du `.drawio` dans diagrams.net, affichage dans GitHub et Notion à largeur étroite, thème sombre. Le schéma technique sera refait dans un second temps selon le même style.
