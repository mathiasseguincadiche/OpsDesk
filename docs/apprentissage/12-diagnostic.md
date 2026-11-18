# 12 — Diagnostiquer et rétablir : un incident de bout en bout

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices, cartes d'incident) est dans la fiche Notion de l'exercice 12, accessible sur invitation.

**Objectif.** Mener un incident sur une panne qu'on n'a pas préparée : partir du symptôme, réunir des faits, trancher entre plusieurs hypothèses, rétablir, puis écrire un post-mortem utile.

**Durée estimée** : 3 à 4 heures, dont une séance avec une autre personne. **Prérequis** : supervision (exercice 09), sauvegarde récente (exercice 11), une personne qui prépare la panne sans dire laquelle. **État** : prévu, non vérifié.

## Pourquoi

Sous pression, le réflexe est de tout redémarrer : les indices disparaissent et la panne reviendra. Diagnostiquer, c'est observer avant d'agir, puis agir de façon ciblée.

## L'essentiel à comprendre

- Sept temps : **symptôme, faits, hypothèses, test qui tranche, correction, recontrôle, post-mortem**.
- On descend couche par couche : `/healthz` (nginx), `/health/live` (API vivante), `/health/ready` (API prête, base joignable), puis les journaux (`journalctl --user -u opsdesk-api`) et le système (disque, mémoire, SELinux, pare-feu).
- La supervision date le début de la panne ; les sondes du moment ne le savent pas.
- Une seule action à la fois ; le recontrôle va jusqu'au parcours d'un utilisateur, pas seulement une sonde.
- Le post-mortem est sans reproche : il cherche ce qui a rendu la panne possible.

## Ce qu'il faut obtenir

Trois incidents différents, préparés par une autre personne sur la copie d'essai ou sur `srv-app` pendant une fenêtre annoncée. Pour chacun : le journal d'incident (commandes, sorties, heures), le temps jusqu'au diagnostic et jusqu'au rétablissement.

Pour le plus intéressant, un **post-mortem** d'une page : résumé ; impact ; chronologie ; cause et ce qui l'a rendue possible ; détection par la supervision ou non ; trois actions.

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| Chaque correction | Une seule action, notée |
| La cause | Confirmée par un test qui écarte au moins une autre hypothèse |
| Le service | Connexion, création et lecture d'un ticket réussies |
| Les données | Ticket témoin relu |
| La supervision | Début et fin de l'incident visibles, ou absence expliquée |
| Le post-mortem | Aucune phrase de reproche ; des actions sur le système |

## Pièges fréquents

Redémarrer avant d'avoir relevé les faits ; changer plusieurs choses à la fois ; s'arrêter à la première hypothèse compatible ; conclure sur une sonde verte ; désactiver une protection pour « voir ».

Suite : [exercice 13](13-autonomie.md).
