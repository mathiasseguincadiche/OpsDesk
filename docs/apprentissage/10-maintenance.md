# 10 — Maintenir en service : préparer, intervenir, vérifier

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 10, accessible sur invitation.

**Objectif.** Mener une intervention sur un service en fonctionnement : la préparer, prévoir son retour arrière, mesurer ce que les utilisateurs ont réellement subi, et prouver l'état obtenu.

**Durée estimée** : 3 à 4 heures. **Prérequis** : déploiement par le rôle Ansible (exercices 06 et 08), supervision (exercice 09), une sauvegarde récente. **État** : prévu, non vérifié.

## Pourquoi

Un service vit longtemps après sa mise en service : correctifs, redémarrages, nouvelles versions. Une intervention improvisée devient un incident ; « ça a l'air de remarcher » n'est pas une conclusion.

## L'essentiel à comprendre

- **Avant** : relever l'état de départ, sauvegarder, écrire les étapes et le retour arrière, fixer le critère d'abandon. **Pendant** : une sonde continue, horodatée. **Après** : comparer à l'état de départ, écrire un compte rendu.
- Redémarrer le service de l'API recrée son conteneur : nginx répond `502` pendant quelques secondes. Mesure réelle sur la pile locale le 18 novembre 2026 : 5 réponses `502` sur 144 requêtes, soit environ 2 secondes.
- Le retour arrière applicatif (redéployer l'image précédente) ne change ni le schéma ni les données. Ce n'est pas une restauration de la base, qui est l'objet de l'exercice 11.
- `dnf needs-restarting -r` dit si un redémarrage est nécessaire après les mises à jour.

## Ce qu'il faut obtenir

- **Maintenance 1** : mises à jour de Rocky Linux sur `srv-app`, redémarrage si nécessaire, retour du service sans intervention.
- **Maintenance 2** : déploiement d'une nouvelle version d'OpsDesk, vérification, puis retour arrière vers la version précédente.

Pour chacune, une **fiche d'intervention** d'une page écrite avant de commencer : but et ce qui ne doit pas changer ; état de départ ; étapes numérotées ; critère d'abandon et retour arrière ; contrôles de fin.

**Livrable** : les deux fiches, la sortie de la sonde continue, l'indisponibilité mesurée, les contrôles de fin, et un compte rendu de cinq lignes au plus pour chacune.

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| Sonde depuis `srv-admin` pendant le redémarrage de `srv-app` | Retour à `200` sans intervention |
| `dnf check-update` sur `srv-app` | Code de retour 0 |
| `/version` et digest après déploiement | Ceux publiés par la CI |
| `/version` et digest après retour arrière | Exactement ceux de départ |
| Ticket témoin | Relu à l'identique après chaque maintenance |
| Indisponibilité | Une durée, en secondes, par maintenance |

## Pièges fréquents

Lancer la sonde sur le serveur qu'on redémarre ; déployer par un tag qui a bougé (le retour arrière redéploie alors la même version) ; décider du critère d'abandon pendant l'incident ; conclure sur l'interface (cache du navigateur) au lieu de `/version`.

Suite : [exercice 12](12-diagnostic.md).
