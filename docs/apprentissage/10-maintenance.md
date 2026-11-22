# 10 — Maintenir en service : préparer, intervenir, vérifier

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 10, accessible sur invitation.

**Objectif.** Mener une intervention sur un service en fonctionnement : la préparer, prévoir son retour arrière, mesurer ce que les utilisateurs ont réellement subi, et prouver l'état obtenu.

**Durée estimée** : 3 à 4 heures. **Prérequis** : déploiement par le rôle Ansible (exercices 06 et 08), supervision (exercice 09), une sauvegarde récente vérifiée (exercice 11). **État** : prévu, non vérifié.

## Pourquoi

Un service vit longtemps après sa mise en service : correctifs, redémarrages, nouvelles versions. Une intervention improvisée devient un incident ; « ça a l'air de remarcher » n'est pas une conclusion.

## L'essentiel à comprendre

- **Avant** : relever l'état de départ, sauvegarder, écrire les étapes et le retour arrière, fixer le critère d'abandon. **Pendant** : une sonde continue, horodatée. **Après** : comparer à l'état de départ, écrire un compte rendu.
- Redémarrer un conteneur et le recréer sont deux opérations distinctes. Pendant l'indisponibilité de l'API, nginx peut répondre `502` ou `504`. Mesure historique du 18 novembre : 5 réponses `502` sur 144 requêtes, environ 2 secondes lors d'une recréation. Le 19 novembre, une API arrêtée a renvoyé `504` en environ 3 secondes sur runner après la correction du délai de connexion. Aucun de ces résultats ne garantit la durée de ta maintenance.
- Le retour arrière applicatif redéploie l'image précédente mais ne restaure pas les données. Vérifier la compatibilité du schéma avant le changement ; si elle n'est pas établie, prévoir une procédure de migration/reprise spécifique et ne pas improviser une restauration en écrasant les écritures.
- `dnf needs-restarting -r` dit si un redémarrage est nécessaire après les mises à jour.

## Cas voisin : un correctif sans changement de version applicative

**Exemple fictif.** Une mise à jour de paquet système sur une machine de test ne modifie pas les images d'une application. Pourtant, si elle impose un redémarrage de la VM, l'application peut devenir momentanément indisponible. Le succès du gestionnaire de paquets et le retour du service sont deux résultats différents.

**Méthode.** Fixer l'état initial (version, ticket témoin, santé, heure), les conditions d'arrêt, la sauvegarde et le retour arrière ; observer depuis **une autre machine** pendant l'intervention ; comparer ensuite les résultats. `dnf check-update` peut retourner `100` lorsque des mises à jour sont disponibles : ce code n'est pas, en soi, une panne. Les durées historiques de l'application ne garantissent aucune durée pour la VM Rocky.

## Ce qu'il faut obtenir

- **Maintenance 1** : mises à jour de Rocky Linux sur `srv-app`, redémarrage si nécessaire, retour du service sans intervention.
- **Maintenance 2** : déploiement d'une nouvelle version d'OpsDesk, vérification, puis retour arrière vers la version précédente.

Pour chacune, une **fiche d'intervention** d'une page écrite avant de commencer : but et ce qui ne doit pas changer ; état de départ ; étapes numérotées ; critère d'abandon et retour arrière ; contrôles de fin.

**Livrable** : les deux fiches, la sortie de la sonde continue, l'indisponibilité mesurée, les contrôles de fin, et un compte rendu de cinq lignes au plus pour chacune.

## Vérifications

| Ce que tu vérifies | Résultat attendu |
| --- | --- |
| Sonde depuis `srv-admin` pendant le redémarrage de `srv-app` | Retour à `200` sans intervention |
| `dnf check-update` sur `srv-app` | Code `0` : aucune mise à jour ; code `100` : mises à jour disponibles ; code `1` : erreur à diagnostiquer. Voir le [manuel DNF](https://man7.org/linux/man-pages/man8/dnf.8.html). |
| `/version` et digest après déploiement | Ceux publiés par la CI |
| `/version` et digest après retour arrière | Exactement ceux de départ |
| Ticket témoin | Relu à l'identique après chaque maintenance |
| Indisponibilité | Une durée, en secondes, par maintenance |

## Pièges fréquents

Lancer la sonde sur le serveur qu'on redémarre ; déployer par un tag qui a bougé (le retour arrière redéploie alors la même version) ; décider du critère d'abandon pendant l'incident ; conclure sur l'interface (cache du navigateur) au lieu de `/version`.

Suite : [exercice 12](12-diagnostic.md).
