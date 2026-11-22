# 08 — CI/CD avec GitHub Actions : tester, construire, publier

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 08, accessible sur invitation. Schéma : [ce que fait la CI, et où elle s'arrête](../diagrams/pedagogique-cicd.svg).

**Objectif.** Tester, construire, analyser et publier automatiquement chaque modification, et prouver que l'image qui tourne sur `srv-app` est exactement celle que la CI a vérifiée.

**Durée estimée** : 4 à 6 heures. **Prérequis** : exercice 06 (images construites et déployées à la main). **État** : chaîne personnelle de livraison prévue, non vérifiée. Un workflow de **qualité documentaire** existe déjà (`.github/workflows/docs-quality.yml`) ; il ne construit ni ne publie les images applicatives.

## Pourquoi

Un chemin manuel finit par laisser passer une version non testée, et personne ne peut dire quel code tourne sur le serveur. La CI rend le chemin systématique et traçable.

## L'essentiel à comprendre

- Quatre étapes, décidées au [registre](../architecture.md#décisions-retenues) : tests `pytest` sur PostgreSQL, construction des deux images, analyse Trivy, publication sur GHCR.
- **CI** : vérifier automatiquement les changements. **Livraison continue** : produire des artefacts qualifiés, publiables, déployables sur décision. **Déploiement continu** : installation automatique d’une version qualifiée sans approbation manuelle. Dans le laboratoire, les runners hébergés ne joignent pas le réseau privé ; le déploiement reste contrôlé depuis `srv-admin`, via Ansible. Ne pas ouvrir le réseau ni installer un runner privilégié pour contourner cette contrainte.
- Les tests de l'API tournent sur PostgreSQL en CI (`TEST_DATABASE_URL`) : certains défauts n'apparaissent pas sur SQLite.
- Un tag peut être déplacé ; un **digest** (`sha256:…`) identifie le contenu d'une image de façon certaine.
- Le `GITHUB_TOKEN` reçoit le minimum de droits, job par job (`packages: write` seulement pour publier).
- Une vulnérabilité trouvée par Trivy se corrige, ou s'accepte par écrit avec une date de réexamen.

## Ce qu'il faut obtenir

1. À chaque pull request : tests de l'API sur PostgreSQL 17, `ruff`, typage et construction du frontend.
2. À chaque push sur `main`, en plus : les deux images, l'analyse Trivy, la publication sur GHCR avec deux tags (version et commit).
3. Une règle écrite pour Trivy : quel niveau fait échouer la CI, comment une exception est acceptée et datée.
4. Le rôle Ansible de l’exercice 06 déploie une version tirée de GHCR, choisie par une variable. Construis un enchaînement local contrôlé sur `srv-admin` : entrée = digests des images qualifiées et cible explicitement choisie ; vérifier la réussite de la livraison et les prérequis, obtenir l’accord avant l’intervention, déployer avec Ansible et vérifier la disponibilité et le parcours métier. En cas d’échec, arrêter la chaîne et appliquer le retour arrière prévu si compatible avec les données. Tester le refus d’une entrée invalide et l’arrêt après un échec sur une cible isolée. Ce n’est pas un déploiement continu entièrement automatique ; expliquer cette différence.

**Livrable** : le workflow, une exécution verte et une rouge provoquée exprès, la règle Trivy, la comparaison des digests des deux images avec GHCR et les preuves de l’enchaînement contrôlé.

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| Une PR qui ne change qu'un commentaire | Coche verte, aucune image publiée |
| Une PR avec un test volontairement faux | Coche rouge, pas d'image |
| Après fusion sur `main` | Deux images sur GHCR, avec version et commit |
| Images des conteneurs API et frontend : relever leur ID via `docker inspect`, puis les `RepoDigests` avec `docker image inspect` | Le digest de registre attendu pour chaque image publiée est présent ; ne pas confondre avec l’ID local. Comparer le même niveau de manifeste (index ou manifeste de plateforme) |
| `curl -i http://192.168.150.10:8080/version` | La version déployée |
| Enchaînement contrôlé, sur cible de test | Déploiement et contrôle métier réussis ; digest invalide refusé ; en cas d’échec, chaîne arrêtée et retour arrière documenté |

## Pièges fréquents

Tests verts en local et rouges en CI (SQLite contre PostgreSQL) ; `permission_denied` sur GHCR (`packages: write` manquant) ; nom d'image en majuscules ; seuil Trivy abaissé en silence ; déploiement par un tag qui a bougé.

Suite : [exercice 07](07-k3s.md).
