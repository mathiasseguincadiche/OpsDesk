# Lire une preuve et ses limites

Une affirmation sur OpsDesk (« les tests passent », « la sauvegarde fonctionne ») ne vaut que par la preuve qui la soutient. Ce document dit comment une preuve est tenue, et comment la lire sans lui faire dire plus qu'elle ne dit. Mise à jour : 18 novembre 2026.

L'état daté de chaque élément est tenu dans [STATUS.md](../STATUS.md) : c'est la seule source à jour.

## Avancement et contrôle : deux informations distinctes

- **Avancement** — qu'est-ce qui existe ? Prévu, En cours, Réalisé, Abandonné.
- **Contrôle** — qu'a-t-on établi ? Vérifié, Échec constaté, Non vérifié.

Un élément peut être **réalisé et non vérifié** (un playbook écrit, jamais rejoué), ou **réalisé avec échec constaté** (un scan qui trouve des vulnérabilités). « Exécuté » dit qu'une action a eu lieu, jamais qu'elle a réussi. Les niveaux personnels L0 à L3 du [parcours](apprentissage/README.md#preuve-et-progression-personnelles) sont une troisième information, distincte des deux autres.

## Ce que contient une preuve

| Élément | Exemple |
| --- | --- |
| **Date** | 18 novembre 2026 |
| **Cible** | Pile locale (`compose.yaml`, Docker 29.8 sous Ubuntu WSL2), ou `srv-app` |
| **Version** | OpsDesk 2.0.0, commit ou digest d'image si disponible |
| **Méthode** | La commande exacte, ou le parcours suivi |
| **Attendu** | `200` et `"database":"up"` |
| **Observé** | La sortie réelle, éventuellement raccourcie, jamais retouchée |
| **Portée et limites** | Ce que la preuve ne couvre pas |

Si une pièce manque, on écrit qu'elle manque ; on ne reconstitue pas une sortie probable. Une déclaration sans pièce se note « déclaré, non vérifié ».

## Sortie réelle ou sortie type

Les fiches du parcours contiennent deux sortes d'exemples, toujours signalées :

- **Sortie réelle** : obtenue sur une machine identifiée, à une date donnée. Exemples du 18 novembre 2026 : les réponses de l'API (`401`, `403`, connexion), les métriques `/metrics`, une sauvegarde et une restauration PostgreSQL, une panne de base diagnostiquée, la coupure mesurée lors de la recréation de l'API, le cycle Terraform sur `terraform_data`.
- **Sortie type** : écrite pour illustrer, non exécutée. Elle n'est jamais une preuve.

## Quand une preuve cesse de valoir

Une preuve vaut pour les fichiers, la version, la cible et la méthode qu'elle identifie. Si l'un change, le contrôle de la nouvelle situation redevient **non vérifié** ; l'ancienne preuve reste, datée, comme observation historique. Une correction n'efface pas l'échec qui l'a précédée : on garde les deux. Une modification purement rédactionnelle ne remet pas en cause un résultat portant sur un code inchangé.

**Exemple.** Les 19 tests de l'API ont réussi sur PostgreSQL 17 le 17 novembre 2026. Si une route change, ce résultat ne couvre plus la nouvelle version : il faut rejouer les tests, et dater le nouveau résultat.

## Rejouer les contrôles de l'application

Les commandes et leurs résultats attendus sont dans le [contrat applicatif, point 20](contrat-applicatif.md#20-commandes-de-vérification) : tests de l'API, typage et construction de l'interface, test de bout en bout `scripts/smoke.py`, sonde de disponibilité. Avant de lancer le test de bout en bout, vérifier la cible avec `/version` : il crée des tickets fictifs et ne les efface pas.

On archive seulement la sortie réellement obtenue, avec sa date, sa version et sa cible. Pour la v2, conserver à mesure des essais les rapports bruts expurgés de secrets (tests PostgreSQL, frontend, Compose, smoke, isolation réseau, redémarrage, scans) dans un répertoire de preuves datées ou des artefacts de CI identifiables, et relier chaque pièce depuis `STATUS.md`. Ne pas fabriquer de journaux pour combler les pièces historiques manquantes.

## Recette ponctuelle du socle (19 novembre 2026)

Les [extraits datés des journaux](../evidence/qualification/2026-11-19-socle.txt) conservent les résultats du [premier essai](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44605747954) et de la [recette finale](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44606981184). Le premier a échoué sur le contrôle d’API arrêtée après une attente d’environ une minute ; le second a prouvé une réponse `504` en 3,003651 s, la reprise et la persistance d’un ticket. Les captures SVG sont accessibles dans les artefacts du run (durée de conservation 7 jours). Aucun exercice personnel n’est validé par cette recette.

## Recette d'une modification documentaire

Pour une évolution significative, constater le problème, expliquer son impact, proposer la correction et vérifier son bénéfice plutôt que refaire un document pour sa seule apparence. Sur les deux supports, examiner quatre situations de lecture : découverte (finalité, statut et accès au parcours), apprentissage (prérequis, exercice, contrôle), recherche ciblée (commande ou preuve accessible), analyse approfondie (contrat, choix, compromis, limites). Vérifier les liens, la terminologie et la correspondance avec le code ; contrôler les rendus et sources lorsque les schémas changent. Indiquer les vérifications non réalisées. Voir également [les sources de vérité](parcours-apprentissage.md#où-se-trouve-quoi).

## Ce qui reste à prouver

Toute l'infrastructure : machines virtuelles, configuration, déploiement Docker Compose, CI, K3s, supervision, sauvegarde et restauration, maintenance. Ce sont les exercices du [parcours](apprentissage/README.md) ; aucun n'est réalisé à ce jour, et un essai historique ne vaut pas réalisation personnelle.

## Preuves de la version 1

Les rapports bruts de la version 1 (tests, smoke HTTP, navigateur, contrat Terraform et Ansible local, rendu Kustomize, scan Trivy, reprise) sont conservés sans modification dans [`legacy/evidence/`](../legacy/evidence/). Ils datent du 3 novembre 2026 et ne s'appliquent pas à la version 2.
