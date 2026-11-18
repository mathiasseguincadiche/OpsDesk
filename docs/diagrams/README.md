# Schémas d'OpsDesk

Chaque schéma existe en deux fichiers côte à côte : la source **Draw.io** (`.drawio`), que l'on modifie, et son export **SVG**, que l'on affiche. Le SVG est toujours exporté depuis la source, jamais retouché à la main.

| Schéma | Question à laquelle il répond | Utilisé dans | Mis à jour |
| --- | --- | --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Qu'est-ce qu'OpsDesk, et comment le projet DevOps avance-t-il ? | Accueil Notion | 18 novembre 2026 |
| [Architecture](architecture.svg) ([source](architecture.drawio)) | Qu'est-ce qui tourne sur `srv-app`, et qui parle à qui ? | [README](../../README.md), [architecture](../architecture.md) | 18 novembre 2026 |

## Lire les schémas

- **Trait plein** : l'application v2, construite et testée en conteneurs locaux.
- **Pointillés** : l'infrastructure prévue, pas encore construite. L'état réel de chaque élément est tenu dans [STATUS.md](../../STATUS.md).
- **Un cadre** représente une machine réelle ; chaque composant est placé là où il s'exécute.
- **Les couleurs** distinguent les familles de composants (bleu : frontend et machines, violet : API, vert : données, orange : sauvegarde), toujours doublées d'un libellé.

## Sources des faits représentés

| Élément | Source |
| --- | --- |
| Conteneurs, ports, noms | [`compose.yaml`](../../compose.yaml), [`frontend/nginx.conf.template`](../../frontend/nginx.conf.template) |
| Machines, réseau, ouvertures de ports | [Registre des décisions](../architecture.md#décisions-retenues) |
| Phases du projet | [ROADMAP.md](../../ROADMAP.md) |

## Régénérer un export

Après toute modification d'une source, depuis ce dossier :

```bash
draw.io --export --format svg --theme light --embed-svg-fonts false --border 0 --output architecture.svg architecture.drawio
```

Sous Windows, l'exécutable est `"C:\Program Files\draw.io\draw.io.exe"`. L'option `--theme light` garde la palette identique en thème sombre ; `--embed-svg-fonts false` évite d'intégrer la police (fichier léger, pas de police sous licence redistribuée).

## Contrôles

| Contrôle | Résultat |
| --- | --- |
| Exports produits par Draw.io depuis les sources | Fait le 18 novembre 2026 |
| Rendu de l'export vérifié visuellement (largeur 1 000 px) | Fait le 18 novembre 2026 : aucun texte coupé, aucune étiquette sur une forme |
| Rendu dans GitHub, clair, sombre et mobile | Vérifié avec le moteur Markdown de GitHub sur la branche de travail ; à confirmer sur `main` après fusion |

## Historique

Les schémas de la version 1 (application Flask, deux conteneurs), leur fiche de contrôle détaillée et la provenance de leurs logos sont conservés dans [`legacy/diagrams/`](../../legacy/diagrams/).
