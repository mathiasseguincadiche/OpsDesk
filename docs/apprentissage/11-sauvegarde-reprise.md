# 11 — Sauvegarder et restaurer : prouver la reprise des tickets

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 11, accessible sur invitation. Schéma : [sauvegarder, puis restaurer et prouver](../diagrams/pedagogique-sauvegarde.svg).

**Objectif.** Sauvegarder la base d'OpsDesk chaque nuit hors du serveur, et prouver, chiffres à l'appui, qu'on sait la restaurer sans toucher l'original.

**Durée estimée** : 4 à 5 heures. **Prérequis** : OpsDesk sur `srv-app` (exercice 06), un accès SSH de `srv-app` vers l'hôte à préparer, la copie d'essai dans K3s (exercice 07) comme cible de restauration. **État** : prévu, non vérifié.

## Pourquoi

Un volume garde les données quand le conteneur disparaît ; il ne les protège ni d'une erreur, ni d'une panne de disque, ni de la perte de la VM. Et une sauvegarde jamais restaurée n'est qu'un espoir.

## L'essentiel à comprendre

- Dispositif retenu au [registre](../architecture.md#décisions-retenues) : `pg_dump` au format custom chaque nuit à 02:00 sur `srv-app`, par un minuteur systemd ; 7 copies gardées ; copie par `rsync` sur SSH dans `~/sauvegardes` sur l'hôte ; restauration testée avec un ticket témoin.
- `pg_dump` lit la base dans une seule transaction : une copie cohérente, sans arrêt. Copier le dossier de données à chaud ne l'est pas.
- `pg_restore --list` vérifie qu'un fichier est lisible ; `--no-owner` évite les erreurs de rôle absent ; `pg_restore` doit être d'une version au moins égale à `pg_dump`.
- Une empreinte `sha256` vérifiée après chaque copie détecte un fichier abîmé.
- **RPO** : ce qu'on peut perdre (jusqu'à 24 heures avec une sauvegarde nocturne). **RTO** : le temps pour revenir, à mesurer.
- La copie sur l'hôte survit à la perte de la VM, pas à celle du PC.

## Ce qu'il faut obtenir

1. Un minuteur systemd du système lance chaque nuit à 02:00 un `pg_dump` au format custom, exécuté dans le conteneur de la base (`docker compose exec -T db pg_dump …`). C'est une vraie responsabilité de systemd : planifier, journaliser, rattraper une nuit manquée.
2. Seules les 7 dernières copies restent sur `srv-app`.
3. Chaque copie part sur l'hôte avec une clé SSH dédiée ; son empreinte est vérifiée à l'arrivée.
4. Une restauration complète dans la base de la copie d'essai ; le ticket témoin est relu dans l'interface de la copie.
5. RPO et RTO mesurés et écrits.

**Livrable** : `.service` et `.timer` (dans le rôle Ansible), la liste des copies avec leurs empreintes, un procès-verbal de restauration (heures, étapes, RTO, RPO).

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| `systemctl list-timers` | Prochaine exécution à 02:00 |
| `pg_restore --list` sur la copie de la nuit | Les tables d'OpsDesk |
| `sha256sum` sur `srv-app` et sur l'hôte | Empreintes identiques |
| Fichiers après 8 nuits | 7 fichiers |
| Ticket témoin dans l'interface de la copie | Même numéro, même titre |
| Service réel pendant le test | Aucune erreur |

## Pièges fréquents

Fichier de 0 octet laissé par une commande en échec ; minuteur jamais activé ; `exec` sans `-T`, qui échoue hors d'un terminal ; restauration dans une base qui n'est pas vide ; ticket témoin absent parce que la copie est plus ancienne (c'est le RPO, pas une panne).

Suite : [exercice 09](09-supervision.md).
