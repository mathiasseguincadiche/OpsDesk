# Démarrage : parcours actif et laboratoire historique

> **HISTORIQUE — référence non exécutable depuis le dépôt courant.** Au contrôle de `main` du 4 novembre 2026 (`51e1a489`), `compose.yaml`, `Dockerfile` et `scripts/prepare-local.sh` sont absents. Les blocs de commandes conservent les anciennes instructions pour comprendre l’essai Ubuntu/WSL ; ils ne sont pas prêts à copier et ne lancent pas le laboratoire personnel. Les versions et résultats qui suivent sont historiques. [Parcours actif](apprentissage/README.md) · [Pré-checks Fedora/KVM/Rocky](laboratoire-fedora-kvm-rocky.md).

## Parcours actif et laboratoire personnel

Le parcours actif, le laboratoire prévu (Fedora 45, KVM, Rocky Linux 10.2) et la place de GitHub sont décrits dans le [parcours d’apprentissage](parcours-apprentissage.md). Commencer par l’[exercice 1](apprentissage/01-application.md) et le [contrat applicatif](contrat-applicatif.md).

## Ce qui est actif aujourd’hui

| Procédure | Classement | Cible, prérequis et résultat attendu |
|---|---|---|
| Lire l’exercice 01 et le contrat | ACTIF — exécutable depuis les sources actuellement disponibles | Poste de lecture, navigateur ou éditeur, accès au dépôt ; aucune VM ni installation. Retrouver le parcours ticket et les besoins de l’application ; comparer sa reformulation aux rubriques 1–4 et 29–30 du contrat. |
| Relire l’architecture retenue, puis préparer son laboratoire | ACTIF — travail personnel à réaliser | Exercice 02 puis [guide commun](laboratoire-fedora-kvm-rocky.md) : nommer l’hôte, les serveurs et les versions ; relever les pré-checks avant toute installation. Aucune configuration finale n’est fournie. |
| Démarrage Python natif | NON VÉRIFIÉ de bout en bout | Les fichiers applicatifs existent ; base, droits, secrets et environnement restent à préparer. Lire [contrat, section 8](contrat-applicatif.md#8-démarrage-en-développement), effets et réserves compris. |
| Recette Compose ci-dessous | HISTORIQUE — non exécutable depuis ce dépôt | Configurations et script absents ; aucune création de fichiers de remplacement ni relance autorisée par cette lecture. |

Pour commencer sans ambiguïté : lire [l’exercice 01](apprentissage/01-application.md), noter ce qui est compris et ce qui reste une question. Si un fichier lié manque, relever son chemin et la révision consultée ; ne pas lancer une recette historique pour compenser.

## État d’essai des procédures

La lecture 01 est disponible ; sa compréhension sera expliquée par l’apprenant. La procédure native du contrat n’a jamais été rejouée entièrement sur son laboratoire : **non vérifiée**. La recette Compose reste historique et non exécutable depuis main. Une procédure partiellement essayée doit préciser les étapes réellement parcourues et celles qui manquent. Un retour arrière seulement décrit reste non vérifié ; aucune durée de séance n’est annoncée sans mesure.

Avant une installation ou une modification, arrêter si machine/version/droits/état initial sont inconnus, si les données source ne sont pas protégées ou si le retour nécessaire n’est pas établi. Nommer le point de non-retour éventuel avant de l’atteindre. Pour un incident, utiliser d’abord le [triage court](reprise.md#triage-court-avant-une-reprise-personnelle).

## Référence historique — laboratoire conservé, pas la procédure Fedora/KVM personnelle

Les procédures et résultats ci-dessous datent des essais historiques ; ils ne sont pas relancés. Les configurations et opérations InfraOps sont à réaliser personnellement ([contrat applicatif](contrat-applicatif.md), [provenance](provenance.md)). Les niveaux techniques de ce texte suivent un ancien barème et ne sont pas les niveaux personnels du [parcours](parcours-apprentissage.md). Les preuves de reprise récentes sont datées dans [STATUS](../STATUS.md).

## Avant d’agir

Dans l’essai historique, les commandes ci-dessous étaient lancées depuis la racine **OpsDesk**, sur Ubuntu/WSL avec Docker 29.8.0 et Compose 5.5.1. Les accès au moteur étaient déjà autorisés ; aucun privilège nouveau n’est demandé ici. Elles ne doivent pas être exécutées sur un serveur partagé ou professionnel sans qualification.

```bash
git --version
python3 --version
docker version
docker compose version
```

**Succès attendu :** client et moteur Docker accessibles, Compose présent, accès autorisé au moteur. Si le moteur est refusé, identifier les permissions ; ne pas contourner avec un chmod global du socket ni activer un accès réseau distant.

Le contrôle historique utilisait Ubuntu/WSL2. Il ne certifie ni Fedora 45, ni GNOME, ni KVM/libvirt, ni Rocky. Les outils et commandes de ces environnements devront être vérifiés sur leur vraie cible.

## Identifier les ressources

La configuration historique utilisait un projet Compose, un réseau et un volume nommés d’après OpsDesk, et la boucle locale `127.0.0.1:18081`. Vérifier qu’ils n’appartiennent pas déjà à un autre travail avant le premier démarrage.

```bash
docker compose config --quiet
docker compose ps
docker volume ls
```

Avant la préparation des secrets, `compose config` peut signaler leur absence ; c’est une dépendance attendue. L’absence du volume avant le premier lancement n’est pas un échec. Si un volume existe déjà, le conserver et comprendre son origine ; aucun `down -v`, prune ou nettoyage global n’est nécessaire pour le démarrage.

## Préparer sans afficher les secrets

```bash
bash scripts/prepare-local.sh
```

Le script historique créait seulement les secrets absents, sans remplacer ceux existants, puis valide Compose. Ils restent hors Git. Sur un montage Windows, vérifier aussi les ACL réelles : une intention POSIX `0600` ne remplace pas la protection du dossier Windows.

## Construire et vérifier

```bash
docker compose up --build --detach --wait
python3 scripts/smoke.py --base-url http://127.0.0.1:18081
```

Dans cette ancienne procédure, l’interface était ensuite consultée à **http://127.0.0.1:18081/tickets**. Créer un ticket fictif et le faire passer par « Prendre en charge », puis « Clôturer ». Le smoke automatise aussi des erreurs attendues ; il crée de petites données de test dans la base, et ne les supprime pas silencieusement.

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
