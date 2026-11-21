# Contribuer à OpsDesk

Merci de contribuer de façon reproductible, mesurable et proportionnée au besoin. OpsDesk est un **laboratoire InfraOps**, pas un service destiné à être exposé sur Internet.

## Avant de proposer un changement

1. Lire le [README](README.md), le [contrat applicatif](docs/contrat-applicatif.md), les [décisions techniques](docs/architecture.md) et [STATUS.md](STATUS.md).
2. Vérifier si une issue existe déjà et expliquer le besoin avant d'ajouter une technologie ou une couche de complexité.
3. Créer une branche dédiée à partir de `main` (`fix/…`, `feat/…`, `docs/…` ou `test/…`).
4. Conserver les interfaces et décisions existantes sauf ADR motivé, revue des conséquences et validation.
5. Ne jamais intégrer dans Git des mots de passe, jetons, certificats privés, données personnelles, `.env`, states Terraform ou sauvegardes.

## Comprendre puis vérifier

La **pile locale de démonstration** se lance à partir de la racine :

```bash
docker compose up -d --build
docker compose ps
python3 scripts/smoke.py
docker compose down
```

Les ports de démonstration sont liés à `127.0.0.1`. `docker compose down` conserve le volume de données ; **ne pas utiliser `down -v` sans intention explicite de supprimer la base**. Pour préparer les outils sur Fedora et Rocky, suivre le [guide du laboratoire](docs/laboratoire-fedora-kvm-rocky.md), avec inventaire avant installation.

- Code applicatif : exécuter les tests concernés, le typage et les contrôles décrits dans la [référence technique](docs/reference-technique.md). Fournir l'environnement et les versions.
- Documentation et schémas : `python3 scripts/check_docs.py` ; relire également le rendu GitHub en clair, sombre et sur mobile.
- InfraOps : ne pas prétendre qu'un plan, un lint ou une CI sur runner constitue un déploiement réussi sur Rocky. Exiger les [preuves et limites](docs/preuves.md).

L'exercice personnel **08 — CI/CD avec GitHub Actions** reste à concevoir, exécuter et expliquer par l'apprenant. La vérification automatique de documentation ne livre pas cet exercice à sa place.

## Que fournir dans une pull request ?

- Le problème, le périmètre et les alternatives envisagées.
- Les chemins et comportements modifiés, avec lien à l'issue si applicable.
- Les commandes **réellement exécutées**, sur quelle cible, à quel commit, et leurs résultats.
- Les risques de sécurité, compatibilité, perte de données et un retour arrière approprié.
- Pour les schémas : source `.drawio`, export `.svg` cohérent, légende et rendu vérifié.
- Pour les interfaces : capture **réelle**, expurgée, avec sa version et son contexte.
- Les limites et validations restantes ; ne jamais transformer un résultat illustratif en preuve.

Le [modèle de PR](.github/pull_request_template.md) rappelle ces contrôles. Un contributeur ne doit pas recopier le suivi personnel Notion dans les fichiers publics.

## Où mettre la documentation ?

La [charte du dépôt](docs/CHARTE_GITHUB.md) décrit les différentes familles de documents et leurs critères. Le README présente le projet, `docs/` explique l'architecture et l'exploitation, `evidence/` conserve les preuves versionnées et `STATUS.md` indique ce qui a réellement été vérifié.

## Sécurité et divulgation

Lire [SECURITY.md](SECURITY.md) avant de partager une vulnérabilité. Ne jamais publier de secrets ni de données exploitables contre une instance réelle dans une issue ou une PR.
