# Démarrer le laboratoire local en comprenant la cible

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

## Avant d’agir

Les commandes ci-dessous se lancent depuis la racine **OpsDesk**, sur la machine de laboratoire. Elles ne doivent pas être exécutées sur un serveur partagé ou professionnel sans qualification.

```bash
git --version
python3 --version
docker version
docker compose version
```

**Succès attendu :** client et moteur Docker accessibles, Compose présent, accès autorisé au moteur. Si le moteur est refusé, identifier les permissions ; ne pas contourner avec un chmod global du socket ni activer un accès réseau distant.

Le contrôle effectué dans cette mission utilise Ubuntu/WSL2. Il ne certifie ni Fedora 45, ni GNOME, ni KVM/libvirt, ni Rocky. Les outils et commandes de ces environnements devront être vérifiés sur leur vraie cible.

## Identifier les ressources

La configuration utilise le projet Compose `v42opsdesk`, le réseau `v42opsdesk_net`, le volume `v42opsdesk_pgdata` et la boucle locale `127.0.0.1:18081`. Vérifier qu’ils n’appartiennent pas déjà à un autre travail avant le premier démarrage.

```bash
docker compose config --quiet
docker compose ps
docker volume inspect v42opsdesk_pgdata
```

Avant la préparation des secrets, `compose config` peut signaler leur absence ; c’est une dépendance attendue. L’absence du volume avant le premier lancement n’est pas un échec. Si un volume existe déjà, le conserver et comprendre son origine ; aucun `down -v`, prune ou nettoyage global n’est nécessaire pour le démarrage.

## Préparer sans afficher les secrets

```bash
bash scripts/prepare-local.sh
```

Le script crée seulement les secrets absents, sans remplacer ceux existants, puis valide Compose. Ils restent hors Git. Sur un montage Windows, vérifier aussi les ACL réelles : une intention POSIX `0600` ne remplace pas la protection du dossier Windows.

## Construire et vérifier

```bash
docker compose up --build --detach --wait
python3 scripts/smoke.py --base-url http://127.0.0.1:18081
```

Ouvrir ensuite **http://127.0.0.1:18081/tickets**. Créer un ticket fictif et le faire passer par « Prendre en charge », puis « Clôturer ». Le smoke automatise aussi des erreurs attendues ; il crée de petites données de test dans la base, et ne les supprime pas silencieusement.

```bash
curl --fail http://127.0.0.1:18081/version
curl --fail http://127.0.0.1:18081/health/ready
docker compose logs --tail=50 app db
```

Ne pas copier des journaux sans les relire : garder seulement l’information de diagnostic et aucune donnée personnelle ou secret.

## En cas de problème

| Symptôme | Première vérification | Sens du résultat |
|---|---|---|
| Le port 18081 répond déjà avant le lab | Identité du service existant et `compose ps` | Ne pas l’arrêter pour libérer le port sans connaître son propriétaire |
| App non prête | Logs `app` et `db`, état des healthchecks | Une DB démarrée ne signifie pas que son schéma est initialisé |
| Erreur de rôle/mot de passe après modification d’un secret | Historique d’initialisation du volume | Les scripts init DB s’exécutent au premier volume neuf ; changer le fichier ne modifie pas automatiquement le rôle existant |
| HTTP 400/409 sur un ticket | Message JSON et règle de statut | Peut être un refus métier prévu, pas une panne d’infrastructure |
| Image introuvable | Tag exact et accès au registre | Ne pas remplacer arbitrairement par `latest` |

Les identifiants de ressources servent à sélectionner la cible, pas à justifier un effacement. [Exploitation et retour arrière](exploitation-day2.md).
