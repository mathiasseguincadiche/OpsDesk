# Livrer une évolution : développeur et opérateur

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

## Contrat simple

Le développeur fictif modifie le code métier et ses tests. L’opérateur InfraOps fournit l’image, la cible, les autorisations, les contrôles et le retour arrière. Le développeur ne devrait pas avoir besoin de SSH administrateur pour une livraison ordinaire ; **ce parcours CI autonome n’est pas encore démontré dans ce laboratoire**.

## Ce qui est déjà rejouable localement

Depuis la racine du dépôt :

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

Après création d’un commit réel, sur une cible de laboratoire autorisée :

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

La chaîne principale reste **GitHub Actions**. GitLab est un deuxième hébergement tant qu’une autre fonction n’a pas été implémentée et testée. Les deux plateformes ne doivent pas se concurrencer pour déployer la même cible ; aucune synchronisation automatique n’est revendiquée.

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
