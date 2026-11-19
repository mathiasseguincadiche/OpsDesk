# 13 — Démontrer son autonomie sur une tâche nouvelle

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple de fiche de cas, indices) est dans la fiche Notion de l'exercice 13, accessible sur invitation.

**Objectif.** Mener seul une tâche jamais faite, de la décision à la preuve, et la défendre devant quelqu'un qui pose des questions.

**Durée estimée** : une journée, bornée à l'avance. **Prérequis** : exercices 01 à 12, une personne disponible 20 minutes. **État** : prévu, non vérifié.

## Pourquoi

Suivre une fiche guidée prouve qu'on sait exécuter. En poste, personne ne donne de fiche : il faut découper le problème, trouver l'information fiable, décider, vérifier et expliquer.

## L'essentiel à comprendre

| Niveau | Ce qu'il signifie |
| --- | --- |
| L0 — Découverte | Savoir ce qu'est l'outil et à quoi il sert |
| L1 — Compréhension | Prévoir ce qu'une commande va faire avant de la lancer |
| L2 — Réalisation personnelle | L'avoir mis en œuvre soi-même, avec une fiche |
| L3 — Autonomie vérifiée | L'avoir appliqué à un cas nouveau, vérifié par un contrôle séparé |

Toute aide est déclarée : A0 (documentation officielle seulement), A1 (ressources générales), A2 (indice ciblé), A3 (solution partielle comprise et adaptée). Une aide déclarée ne disqualifie pas ; une aide cachée retire sa valeur à la preuve.

## Ce qu'il faut obtenir

Une tâche jamais faite, parmi celles-ci ou de taille comparable :

1. Sur la copie d'essai, diagnostiquer et corriger un accès aux métriques depuis une source interdite (variante nouvelle préparée par une autre personne), sans réexposer l'API ni interrompre la collecte autorisée. Ne pas simplement rejouer l'exercice 09.
2. HTTPS sur l'Ingress de la copie d'essai, avec redirection.
3. Adapter Terraform et Ansible à une nouvelle cible de test isolée avec une contrainte différente de stockage ou de ressources, puis restaurer une sauvegarde et mesurer le temps total. Ne pas reproduire à l'identique l'évaluation 2.
4. Changer `JWT_SECRET` sur le service réel, avec annonce et preuve.
5. Une alerte « aucune sauvegarde depuis 26 heures », testée.
6. Une analyse Trivy hebdomadaire et le traitement complet d'une vulnérabilité.

**Livrable** : une **fiche de cas** en dix rubriques (demande ; ce que je sais et ne sais pas ; borne de temps et critère d'abandon ; faits relevés ; décision et option écartée ; réalisation ; preuve ; limites ; aide reçue ; auto-évaluation), les preuves datées, une explication orale de 10 minutes, et le résultat de la vérification séparée.

## Vérification séparée

Le niveau L3 n'est noté qu'après l'une de ces deux vérifications, avec sa date et le nom de la personne :

- **rejouer** la tâche de zéro, au moins une semaine plus tard, sans notes, sur une cible neuve ;
- **défense orale** de 20 minutes : questions, puis une modification demandée en direct, réalisée et prouvée.

## Pièges fréquents

Choisir une tâche déjà faite ou trop grande ; écrire la fiche de cas après coup ; minimiser l'aide reçue ; s'attribuer L3 sans vérification séparée.

Retour : [le parcours](README.md).
