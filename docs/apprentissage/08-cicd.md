# 08 — CI/CD avec GitHub Actions : tester, construire, publier

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 08, accessible sur invitation. Schéma : [ce que fait la CI, et où elle s'arrête](../diagrams/pedagogique-cicd.svg).

**Objectif.** Tester, construire, analyser et publier automatiquement chaque modification, et prouver que l'image qui tourne sur `srv-app` est exactement celle que la CI a vérifiée.

**Durée estimée** : 4 à 6 heures. **Prérequis** : exercice 06 (images construites et déployées à la main). **État** : prévu, non vérifié ; aucun workflow dans le dépôt à ce jour.

## Pourquoi

Un chemin manuel finit par laisser passer une version non testée, et personne ne peut dire quel code tourne sur le serveur. La CI rend le chemin systématique et traçable.

## L'essentiel à comprendre

- Quatre étapes, décidées au [registre](../architecture.md#décisions-retenues) : tests `pytest` sur PostgreSQL, construction des deux images, analyse Trivy, publication sur GHCR.
- La CI ne touche jamais aux serveurs : ses machines ne joignent pas le réseau privé. Le déploiement part de `srv-admin`, par Ansible, vers une version choisie.
- Les tests de l'API tournent sur PostgreSQL en CI (`TEST_DATABASE_URL`) : certains défauts n'apparaissent pas sur SQLite.
- Un tag peut être déplacé ; un **digest** (`sha256:…`) identifie le contenu d'une image de façon certaine.
- Le `GITHUB_TOKEN` reçoit le minimum de droits, job par job (`packages: write` seulement pour publier).
- Une vulnérabilité trouvée par Trivy se corrige, ou s'accepte par écrit avec une date de réexamen.

## Ce qu'il faut obtenir

1. À chaque pull request : tests de l'API sur PostgreSQL 17, `ruff`, typage et construction du frontend.
2. À chaque push sur `main`, en plus : les deux images, l'analyse Trivy, la publication sur GHCR avec deux tags (version et commit).
3. Une règle écrite pour Trivy : quel niveau fait échouer la CI, comment une exception est acceptée et datée.
4. Le rôle Ansible de l'exercice 06 déploie une version tirée de GHCR, choisie par une variable.

**Livrable** : le workflow, une exécution verte et une rouge provoquée exprès, la règle Trivy, et la preuve que le digest sur `srv-app` est celui publié.

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| Une PR qui ne change qu'un commentaire | Coche verte, aucune image publiée |
| Une PR avec un test volontairement faux | Coche rouge, pas d'image |
| Après fusion sur `main` | Deux images sur GHCR, avec version et commit |
| Digest de l'API sur `srv-app` (`podman inspect --format '{{.ImageDigest}}'`) et sur GHCR | Identiques |
| `curl -i http://192.168.150.10:8080/version` | La version déployée |

## Pièges fréquents

Tests verts en local et rouges en CI (SQLite contre PostgreSQL) ; `permission_denied` sur GHCR (`packages: write` manquant) ; nom d'image en majuscules ; seuil Trivy abaissé en silence ; déploiement par un tag qui a bougé.

Suite : [exercice 09](09-supervision.md).
