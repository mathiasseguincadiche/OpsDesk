# Schémas d'OpsDesk

Chaque schéma existe en deux fichiers côte à côte : la source **Draw.io** (`.drawio`), que l'on modifie, et son export **SVG**, que l'on affiche. Le SVG est toujours exporté depuis la source, jamais retouché à la main. Tous suivent le système graphique de la collection V24 : mêmes couleurs, icônes, formes et conventions de flux, mais une composition propre à chaque sujet.

## Les schémas

| Schéma | Question à laquelle il répond | Composition | Largeur | Utilisé dans |
| --- | --- | --- | --- | --- |
| [Présentation](presentation.svg) ([source](presentation.drawio)) | Qu'est-ce qu'OpsDesk, pour qui, et où en est le projet ? | Infographie : point focal, acteurs, garanties, ligne de temps | 1 000 | Affichage en grand |
| [Présentation pour Notion](presentation-notion.svg) ([source](presentation-notion.drawio)) | La même, dans la largeur d'une page Notion | Même infographie, colonnes resserrées | 760 | Accueil Notion |
| [Présentation pour téléphone](presentation-mobile.svg) ([source](presentation-mobile.drawio)) | La même, pour un petit écran | Une colonne, ligne de temps verticale | 400 | Petits écrans |
| [Architecture, vue d'ensemble](architecture-globale.svg) ([source](architecture-globale.drawio)) | Quelles machines, et quels flux principaux ? | Zones : hôte, réseau, trois machines, quatre flux | 760 | [README](../../README.md), [architecture](../architecture.md), Notion (exercices 01, 02, 10, 12) |
| [Architecture détaillée](architecture.svg) ([source](architecture.drawio)) | Qu'est-ce qui s'exécute où, et par quel flux, avec quel port ? | Zones imbriquées, flux typés | 1 200 | Lien « Voir le schéma détaillé » |
| [Accès SSH](pedagogique-acces-ssh.svg) ([source](pedagogique-acces-ssh.drawio)) | Une connexion SSH échoue : par où commencer ? | Deux couloirs (poste, VM), six étapes | 760 | Notion, exercice 03 |
| [Terraform](pedagogique-terraform.svg) ([source](pedagogique-terraform.drawio)) | Que compare Terraform pour calculer un plan ? | Trois sources qui convergent, issues, cycle | 760 | Notion, exercice 04 |
| [Ansible](pedagogique-ansible.svg) ([source](pedagogique-ansible.drawio)) | Comment Ansible rend-il un serveur conforme ? | Mécanisme en trois temps, avec décision | 760 | Notion, exercice 05 |
| [Compose](pedagogique-compose.svg) ([source](pedagogique-compose.drawio)) | Comment une définition Compose devient-elle des conteneurs ? | Transformation en trois colonnes, puis cycle de vie | 760 | Notion, exercice 06 |
| [K3s](pedagogique-k3s.svg) ([source](pedagogique-k3s.drawio)) | Que fait K3s des déclarations ? | Boucle de contrôle, pod prêt ou non | 760 | Notion, exercice 07 |
| [CI/CD](pedagogique-cicd.svg) ([source](pedagogique-cicd.drawio)) | Du commit au service : qui fait quoi ? | Deux couloirs (automatique, humain), points d'arrêt | 760 | Notion, exercice 08 |
| [Supervision](pedagogique-supervision.svg) ([source](pedagogique-supervision.drawio)) | De la mesure à l'alerte ? | Collecte, puis machine à états | 760 | Notion, exercice 09 |
| [Sauvegarde](pedagogique-sauvegarde.svg) ([source](pedagogique-sauvegarde.drawio)) | Que peut-on perdre, et combien de temps pour revenir ? | Ligne de temps (RPO, RTO), étapes de restauration | 760 | Notion, exercice 11 |

Les vues pédagogiques font 760 px de large : affichées dans une fiche Notion (environ 700 px), leurs textes restent au-dessus de 11 px.

## Lire les schémas

- **Un cadre est une vraie frontière** : un hôte, un réseau, une machine, un environnement d'exécution. Un fond sans trait regroupe seulement pour la lecture.
- **La couleur d'un flux dit sa nature** : ardoise pour l'applicatif, bleu-vert pour l'administration et le déploiement, framboise pour l'observabilité, orange pour la sauvegarde.
- **Le trait dit l'avancement** : plein, réalisé (l'application v2 et ses flux internes, testés en conteneurs locaux) ; pointillé, prévu (toute l'infrastructure). L'état réel de chaque élément est dans [STATUS.md](../../STATUS.md).
- **Les badges** : « Vérifié », « Prévu », « Schéma de principe » (un mécanisme illustré, valeurs d'exemple).
- La couleur n'est jamais seule : chaque composant porte une icône et un libellé.

## Sources des faits représentés

| Élément | Source |
| --- | --- |
| Conteneurs, ports, noms | [`compose.yaml`](../../compose.yaml), [`frontend/nginx.conf.template`](../../frontend/nginx.conf.template) |
| Machines, réseau, ouvertures de ports, sauvegarde, supervision | [Registre des décisions](../architecture.md#décisions-retenues) |
| Sondes, métriques, authentification | [`backend/app/`](../../backend/app/), [référence technique](../reference-technique.md) |
| Mécanismes pédagogiques | Fiches et énoncés du [parcours](../apprentissage/README.md) |
| Phases du projet | [ROADMAP.md](../../ROADMAP.md) |

## Régénérer

Les sources sont produites par un générateur, à partir du système graphique (couleurs, icônes, composants) :

```bash
python docs/diagrams/outils/generer_schemas.py docs/diagrams
```

Puis, pour chaque source, depuis ce dossier :

```bash
draw.io --export --format svg --theme light --embed-svg-fonts false --border 0 --output architecture.svg architecture.drawio
```

Sous Windows, l'exécutable est `"C:\Program Files\draw.io\draw.io.exe"`. `--theme light` garde la palette identique en thème sombre ; `--embed-svg-fonts false` n'intègre aucune police. Une retouche faite à la main dans Draw.io est perdue si l'on régénère : la reporter dans le générateur.

## Contrôles

| Contrôle | Résultat |
| --- | --- |
| Exports produits par Draw.io depuis les sources | Fait le 18 novembre 2026, pour les douze schémas ; refait le 19 novembre 2026 pour les six schémas touchés par le passage à Docker Compose, et pour la présentation à 760 px |
| Structure des sources | Fait le 18 novembre 2026 : aucun identifiant en double, aucun connecteur orphelin, cinq calques nommés |
| Rendu à la largeur réelle | Refait le 19 novembre 2026 pour la vue d'ensemble, l'architecture détaillée, Ansible et Compose. Fait le 18 novembre 2026 : vues pédagogiques et vue d'ensemble à 700 px, présentation et architecture détaillée à 950 px, présentation pour téléphone à 375 px ; aucun texte coupé, aucune flèche à travers une forme |
| Thème sombre | Fait le 18 novembre 2026, sur fond `#0d1117` : fond du schéma intégré, palette intacte |
| Rendu dans GitHub | Fait le 19 novembre 2026 dans un navigateur à 1 280 px, thème sombre de GitHub : README, `architecture.md` et `pedagogique-compose.svg` lisibles, fond du schéma conservé |
| Rendu dans Notion | Fait le 19 novembre 2026 dans l'application Notion pour Windows, thème sombre : la présentation à 760 px de l'accueil et le schéma Compose de l'exercice 06 sont lisibles sans zoom, légendes affichées |
| Édition dans l'interface de Draw.io | Fait le 19 novembre 2026 sur `architecture.drawio` : ouverture sans erreur, calques nommés visibles, une machine sélectionnée comme conteneur avec son contenu ; fichier refermé sans modification |

## Historique

Les schémas de la version 1 (application Flask, deux conteneurs), leur fiche de contrôle et la provenance de leurs logos sont conservés dans [`legacy/diagrams/`](../../legacy/diagrams/).
