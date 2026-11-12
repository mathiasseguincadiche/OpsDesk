# Livrer une évolution : développeur et opérateur

> **HISTORIQUE — référence non exécutable depuis le dépôt courant.** Au contrôle de `main` du 4 novembre 2026 (`51e1a489`), `compose.yaml` et `Dockerfile` sont absents. Les blocs de commandes conservent les anciennes instructions pour comprendre l’essai Ubuntu/WSL ; ils ne sont pas prêts à copier et ne lancent pas le laboratoire personnel. Les versions et résultats qui suivent sont historiques. [Parcours actif](apprentissage/README.md) · [Pré-checks Fedora/KVM/Rocky](laboratoire-fedora-kvm-rocky.md).

## Référence historique — laboratoire de développement

Les procédures et résultats ci-dessous datent des essais historiques ; ils ne sont pas relancés. Les configurations et opérations InfraOps sont à réaliser personnellement ([contrat applicatif](contrat-applicatif.md), [provenance](provenance.md)). Les niveaux techniques de ce texte suivent un ancien barème et ne sont pas les niveaux personnels du [parcours](parcours-apprentissage.md). Les preuves de reprise récentes sont datées dans [STATUS](../STATUS.md).

## Contrat simple

Le développeur fictif modifie le code métier et ses tests. L’opérateur InfraOps fournit l’image, la cible, les autorisations, les contrôles et le retour arrière. Le développeur ne devrait pas avoir besoin de SSH administrateur pour une livraison ordinaire ; **ce parcours CI autonome n’est pas encore démontré dans ce laboratoire**.

## Chaîne de livraison historique — non rejouable depuis les fichiers courants

Ancienne chaîne depuis la racine du laboratoire Ubuntu/WSL, avec Docker 29.8.0, Compose 5.5.1, secrets, DB et accès moteur déjà préparés ; effet : construction puis remplacement de l’application et création de tickets fictifs. Ne pas la lancer depuis ce dépôt :

```bash
python3 -m unittest discover -s tests/unit -v
python3 -m compileall -q app scripts
docker compose config --quiet
docker compose up --build --detach --wait
python3 scripts/smoke.py --base-url http://127.0.0.1:18081
curl --fail http://127.0.0.1:18081/version
```

Cette chaîne locale ne prouve pas un job GitHub exécuté, un push GHCR ou une connexion runner → laboratoire. Consulter les fichiers CI réellement présents et leurs résultats datés avant de qualifier la livraison distante.

## Interface de versionnement

L’image reçoit `APP_VERSION` et `APP_REVISION` à sa construction. La version réellement servie se lit dans `/version`. La valeur `uncommitted-v42` de la première preuve signifie explicitement qu’aucun commit n’existait encore pour cette exécution.

Exemple historique de paramètres de livraison, conservé pour lecture. Il modifiait le service Compose du laboratoire préparé ; les fichiers requis sont absents du dépôt courant :

```bash
APP_VERSION=0.1.1 APP_REVISION="$(git rev-parse HEAD)"   docker compose up --build --detach --wait
python3 scripts/smoke.py --base-url http://127.0.0.1:18081
```

Ne pas exécuter cette commande si elle remplace sans préparation une instance utilisée. Une version déclarée est une entrée de build ; elle ne garantit pas à elle seule que l’image contient ce commit. Capturer l’image locale/digest, le commit, les commandes et le résultat du parcours.

## Contrôles que doit fournir la CI

1. Pré-check lisible et validation des sources/configurations.
2. Tests unitaires positifs et négatifs.
3. Construction d’une image identifiable.
4. Analyse de sécurité avec outil et base de données à jour ; échec visible selon une politique documentée.
5. Vérification readiness **et** ticket métier dans une cible de test identifiée.
6. Publication/promotion seulement avec permissions et autorisations réelles.

**GitHub est la seule plateforme active.** GitHub Actions est le chantier personnel de l’exercice 08, sans résultat distant présumé. GitLab reste une référence historique facultative ; aucun miroir, synchronisation ou nouveau pipeline GitLab n’est à mettre en place.

## En cas d’échec

| Signal | Qui intervient ? | Action sûre |
|---|---|---|
| Test métier rouge | Développeur, puis opérateur si dépendance en panne | Lire le cas qui échoue ; ne pas supprimer le test |
| Image non construite | Développeur/opérateur | Lire le verrou de dépendances et le build, sans changer de tag au hasard |
| Readiness rouge | Opérateur | Séparer processus app, DNS `db`, authentification et schéma DB |
| Version servie différente | Opérateur | Comparer configuration, image et `/version` |
| Données manquantes | Opérateur | Arrêter les modifications, qualifier le volume et la restauration ; un rollback d’image ne restaure pas les données |

## Promotion et rollback : limite actuelle

Le premier succès local n’est pas une promotion en staging/prod-like. Avant une démonstration de rollback, identifier l’image saine, l’état du schéma et les données à conserver, disposer d’une sauvegarde contrôlée, puis définir le test de retour. Aucun reset de volume n’est une stratégie de rollback.
