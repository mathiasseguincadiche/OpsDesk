# Mise en conformité V26 — revue ciblée
Base : `d2a8e9e204b1bb797c26b1e1c927b9ec4fe166b1`, le 19 novembre 2026.

| Périmètre | Correction | Contrôle restant |
| --- | --- | --- |
| Démarrage | Création protégée de .env | Rejouer en environnement jetable |
| Configuration | Garde-fous de secrets au démarrage + tests pytest dédiés | Exécuter les tests SQLite et PostgreSQL, puis smoke |
| Reprise | RPO conditionnel, cible isolée, rétention par nombre | Exercice 11 personnel |
| Exercices 05–07 | Socle K3s, contrôle non divulguant, séparation rôles | Réalisation personnelle |
| Graphismes | Compositions existantes conservées | Recette native et ajout des vues utiles |

Les résultats du run historique ne qualifient pas cette révision. Aucun exercice personnel ni niveau d’autonomie n’est validé. Aucun pipeline de livraison ou code d’infrastructure fourni pour l’exercice.
