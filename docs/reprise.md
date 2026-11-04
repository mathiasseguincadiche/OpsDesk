# Reprise minimale d’un ticket — essai exécuté

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

Le 3 novembre2026, `scripts/recovery_lab.py` a exporté PostgreSQL puis restauré les tickets dans une base et une application sur volumes/réseau neufs. Le ticket fermé a été relu via HTTP : ID, titre, description, priorité, statut et dates strictement identiques. La source18081 est restée disponible, la cible18086 distincte. Durée observée10,769s, dans `evidence/recovery.json`.

Prérequis : laboratoire local OpsDesk sain, ticket référencé dans business-smoke.json, Docker autorisé, PyYAML6.0.3 et port18086 libre. À la racine du dépôt :

```sh
python3 scripts/recovery_lab.py --port 18086
```

Le script refuse un port utilisé, crée un nom de cible aléatoire et n’exécute ni suppression de source ni `down -v`. Le dump, les fichiers privés de cible et les secrets restent dans `.local/`. Le dump de cet exercice OpsDesk n’est pas chiffré ; il ne constitue pas une politique de sauvegarde exploitable. Prévoir chiffrement, destination indépendante, rétention, fraîcheur et identités protégées avant usage réel.

Un ticket comparé démontre ce contrôle précis ; il ne qualifie pas tous les volumes, les écritures concurrentes, une perte physique, K3s ni Rocky. Un redéploiement d’image seul n’aurait pas restauré un ticket perdu. Le code utilise l’image locale exacte par son ID et des droits applicatifs limités après restauration.
