# Schémas OpsDesk

| Vue | Source modifiable | Image | Question à laquelle elle répond |
| --- | --- | --- | --- |
| Présentation | [presentation.drawio](presentation.drawio) | [presentation.svg](presentation.svg) | Que fait OpsDesk, et quelles phases mènent de l'application à une infrastructure exploitée ? |
| Technique | [architecture-technique.drawio](architecture-technique.drawio) | [architecture-technique.svg](architecture-technique.svg) | Comment l'application est construite, ce qu'a montré l'essai historique et ce que le laboratoire personnel doit accueillir. |

## Lire les schémas

- **Cadre à trait plein :** existe dans le dépôt (l'application et sa base).
- **Cadre à points fins (technique) :** référence historique, observée hors du dépôt.
- **Cadre ou tuile en pointillé :** à réaliser (étape du parcours en présentation, laboratoire personnel en technique). Aucun exercice n'est réalisé à ce jour (suivi Notion du 12 novembre 2026 : 36 lignes « À faire »). Une couleur seule ne dit jamais l'avancement.
- **Pastille numérotée (présentation) :** ordre des trois phases. Le schéma technique n'en a pas : il montre des emplacements, pas une chronologie.
- **Flèche pleine :** échange entre composants (HTTP, SQL) ou montage d'un volume.
- **Flèche pointillée :** enchaînement ou livraison prévus.

Les trois phases reprennent celles du [parcours](../parcours-apprentissage.md) et de Notion : conteneurisation et livraison automatisée, infrastructure et automatisation, orchestration, observabilité et fiabilité. Le schéma technique ne décide pas de la topologie du laboratoire : la case « exécution d'OpsDesk » reste à décider à l'exercice 02. L'essai historique de la phase 1 (application et base fournies, exécutées avec Docker Compose) est décrit dans la référence historique du schéma technique. Aucun des deux schémas n'affirme un déploiement, une preuve ou une mise en production.

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

## D'où viennent les faits

| Ce que montre le schéma | Source dans le dépôt |
| --- | --- |
| Gunicorn sert Flask ; pages `/tickets`, API `/api/tickets` | [`app/opsdesk/web.py`](../../app/opsdesk/web.py), [`requirements.lock`](../../requirements.lock), [`docs/architecture.md`](../architecture.md) |
| Sondes `/health/live`, `/health/ready`, `/version`, `/metrics` | [`app/opsdesk/web.py`](../../app/opsdesk/web.py) |
| PostgreSQL, requêtes paramétrées, schéma | [`db/schema.sql`](../../db/schema.sql), [`app/opsdesk/web.py`](../../app/opsdesk/web.py) |
| Aucune authentification, données fictives | [`README.md`](../../README.md), [`docs/securite.md`](../securite.md) |
| Essai historique : `127.0.0.1:18081` vers le port 8000, `db:5432`, volume nommé | [`docs/architecture.md`](../architecture.md), [`docs/demarrage.md`](../demarrage.md) |
| Laboratoire prévu : Fedora 45, KVM/QEMU/libvirt, Rocky Linux 10.2 | [`ROADMAP.md`](../../ROADMAP.md), [`docs/laboratoire-fedora-kvm-rocky.md`](../laboratoire-fedora-kvm-rocky.md) |
| AWS facultatif (budget et autorisation) | [`docs/architecture.md`](../architecture.md) |
| Phases 1 à 3 et leurs outils | [`docs/parcours-apprentissage.md`](../parcours-apprentissage.md), [`docs/apprentissage/README.md`](../apprentissage/README.md) |

Les fichiers Compose de l'essai historique ne sont pas dans le dépôt : le schéma technique les décrit d'après `docs/architecture.md` et ne prouve ni leur contenu ni leur exécution.

## Modifier et exporter

1. Ouvrir le `.drawio` dans diagrams.net et modifier.
2. *Fichier → Exporter en → SVG*, sans l'option « Inclure une copie de mon diagramme ». Le texte alternatif de la page devient le `<title>` du SVG.
3. Enregistrer le `.drawio` et le SVG dans le même commit.

Les sources portent `adaptiveColors="none"` : sans ce réglage, diagrams.net en thème sombre inverse les couleurs et les logos sombres deviennent presque invisibles. Les cadres de texte sont ajustés à leur contenu.

Les deux SVG sont exportés depuis les `.drawio` par le moteur d'export de Draw.io 32.6.10 (page d'export du dépôt jgraph/drawio, Chromium sans interface), en thème clair et sans bordure. Cet export ne remplace pas l'ouverture des fichiers dans l'application.

## Contrôles

Réalisés le 12 novembre 2026 sur les deux schémas :

- export des SVG par le moteur Draw.io 32.6.10 ; aucun `<foreignObject>` ; aucune image externe (les logos sont embarqués) ;
- rendu par deux moteurs indépendants (Chromium et librsvg) : même figure, chaque composant affiche son icône ;
- aucun texte ne dépasse son cadre (mesure des boîtes de texte sur le rendu Chromium) ; plus petite police : 13 px sur un canevas de 1600 px de large ;
- navigateur en thème sombre : le fond clair du SVG est conservé et tous les logos restent lisibles ;
- contrastes calculés : texte courant entre 6,7:1 et 16:1, titres colorés et chiffres des pastilles au moins 4,7:1 (seuil WCAG AA : 4,5:1) ;
- fichiers XML valides ; `.drawio` ouverts dans diagrams.net (application web) en thème sombre, sans inversion de couleurs.

Non vérifiés : affichage dans GitHub (largeur étroite, thème sombre), affichage dans Notion, ouverture dans l'application de bureau Draw.io, lisibilité de la plus petite police à la largeur réelle d'insertion.
