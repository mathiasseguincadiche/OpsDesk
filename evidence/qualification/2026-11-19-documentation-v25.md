# Recette documentaire — application de la V25

Date : 19 novembre 2026. Base de revue : `ac08472e4ef79684c6d9ced593dae7c0a49798a5`. Périmètre : navigation, premier exercice, démarrage, diagnostic et maintien des schémas ; pas de modification du code d'exécution ni des dessins.

## Constat et correction

| Priorité | Constat sur la base de revue | Correction |
| --- | --- | --- |
| Nécessaire | Exercice 01 : noms de services différents de `compose.yaml` | Utiliser frontend/backend/db, distinguer les images et le chemin utilisateur de l'accès local direct |
| Nécessaire | Exercice 12 : incidents Compose proposés indistinctement sur K3s ou le serveur principal | Cible de test isolée, choix de carte selon la plateforme, contrôle de la sauvegarde et du retour |
| Forte valeur | Guide : un seul port vérifié alors que Compose publie 8080 et 8000 | Prérequis et diagnostic des deux ports, contrôle readiness distinct du healthcheck |
| Forte valeur | Pas d'index central dans docs/ | Navigation par usage sans déplacer les références |
| Forte valeur | Notice graphique V24 et historique de rendus | Maintien de la référence V25 et contrôle des nouveaux rattachements |

## Parcours simulés par relecture

| Lecteur | Chemin | Critère observable |
| --- | --- | --- |
| Débutant | README → démarrage → exercice 01 | Pré-requis et résultat attendu ; exercice accessible sans installation |
| Ingénieur | README → index → contrat / architecture / référence | Sources distinctes, décisions, limites et flux |
| Recruteur | README → rôle → STATUS → preuves | Contribution et état avant le grand visuel ; aucune compétence anticipée |
| Contributeur | README → index → provenance / preuve | Méthode de contribution et sources de vérité accessibles |

Ces parcours sont une relecture des contenus et chemins, pas un test utilisateur chronométré ni un rendu natif. Les critères techniques du socle restent ceux de la [recette antérieure](../../STATUS.md). Aucun test du laboratoire ou exercice personnel n'est validé. Les 13 paires Draw.io/SVG sont conservées ; la recette historique figure dans la [notice](../../docs/diagrams/README.md). Les rendus natifs, l'import Draw.io et la consultation sur les appareils réels ne sont pas vérifiés dans cette intervention.

Stabilisation conditionnelle : engager la pratique après revue du changement documentaire ; améliorer ensuite sur la base d'une difficulté, d'une régression, d'une preuve ou d'un besoin réel.
