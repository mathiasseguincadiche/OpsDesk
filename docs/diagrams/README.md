# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles phases mènent de l'application à une infrastructure exploitée ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Où se trouvent les services de l'essai historique et comment communiquent-ils ? |

## Lire la présentation

- **Cadre à trait plein :** existe dans le dépôt (l'application et sa base).
- **Cadre ou tuile en pointillé :** étape du parcours à réaliser. Aucun exercice n'est réalisé à ce jour (suivi Notion du 12 novembre 2026 : 36 lignes « À faire »). Une couleur seule ne dit jamais l'avancement.
- **Pastille numérotée :** ordre des trois phases.
- **Flèche pleine :** échange entre composants (HTTP, SQL).
- **Flèche pointillée :** enchaînement prévu entre étapes.

Les trois phases reprennent celles du [parcours](../parcours-apprentissage.md) et de Notion : conteneurisation et livraison automatisée, infrastructure et automatisation, orchestration, observabilité et fiabilité. L'essai historique de la phase 1 (application et base fournies, exécutées avec Docker Compose) est décrit dans le schéma technique. Le schéma n'affirme ni déploiement, ni preuve, ni mise en production.

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
2. *Fichier → Exporter en → SVG*, en thème clair et sans l'option « Inclure une copie de mon diagramme ». Le texte alternatif de la page devient le `<title>` du SVG.
3. Enregistrer le `.drawio` et le SVG dans le même commit.

Le SVG de présentation est exporté depuis `presentation.drawio` par le moteur d'export de Draw.io 32.6.10 (page d'export du dépôt jgraph/drawio, Chromium sans interface), en thème clair et sans bordure. Cet export ne remplace pas l'ouverture du fichier dans l'application.

## Contrôles

Réalisés le 12 novembre 2026 sur la présentation :

- export du SVG par le moteur Draw.io 32.6.10 ; aucun `<foreignObject>`, aucune image externe ;
- rendu du SVG par deux moteurs indépendants (Chromium et librsvg) : même figure, aucun texte ne dépasse son cadre (mesure des boîtes de texte) ;
- navigateur en thème sombre : le fond clair du SVG est conservé et tous les logos restent lisibles ;
- contrastes calculés : texte courant entre 6,9:1 et 16:1, titres de phase et chiffres des pastilles au moins 4,7:1 (seuil WCAG AA : 4,5:1) ;
- fichiers XML valides.

Restent à faire : ouverture du `.drawio` dans diagrams.net après cette modification, affichage dans GitHub et Notion à largeur étroite. Le schéma technique est refait dans un second temps selon le même style.
