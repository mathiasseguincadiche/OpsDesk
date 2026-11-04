# 01 — Comprendre l’application

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Dessine le trajet d’une création de ticket ; relève dans le contrat le rôle de PostgreSQL, les paramètres attendus et l’absence d’authentification. Ne lance rien pour cette première lecture.

## 2. Objectif pédagogique

Comprendre l’application en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Un contrat applicatif décrit ce que le logiciel exige et garantit ; il ne choisit pas ton infrastructure. Un parcours utilisateur relie une entrée HTTP à une donnée persistante.

## 5. Prérequis

Aucun module technique préalable. Lire le contrat applicatif et les règles de responsabilité ; disposer d’un outil de dessin et noter ses questions. Aucun logiciel d’infrastructure n’est supposé installé. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Lecture du contrat et dessin, sans installation ni déploiement. Le poste hôte prévu est Fedora 45 ; aucune VM ni authentification à un laboratoire historique ne sont requises pour comprendre l’application.

## 7. Travail personnel

Lire docs/contrat-applicatif.md ; distinguer code métier, dépendances et responsabilités d’exploitation. Conserver la première proposition avant toute correction. Présenter ta reformulation avant de lire un schéma de référence.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Suivre une action utilisateur et nommer chaque composant qui peut la bloquer.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Présenter le besoin utilisateur, les fonctions disponibles et deux limites réelles du logiciel sans confondre application et hébergement.
- Tracer une requête jusqu’à la donnée durable ; distinguer code fourni, paramètres, secrets et données.
- Poser les questions techniques qui restent ouvertes ; aucun test d’infrastructure n’est nécessaire à cette première lecture.
- Expliquer comment un ticket identifié, son titre, son état et sa relecture dans PostgreSQL seront contrôlés plus tard, sans inventer de sortie ou de capture.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Un schéma fonctionnel personnel, la liste des données durables et les questions posées à l’équipe applicative. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Confondre le laboratoire de Codex avec une architecture personnelle déjà choisie. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si deux documents semblent décrire des capacités différentes, comparer leur version et la source du contrat. Distinguer une ancienne preuve Codex d’une fonction actuelle ; noter la contradiction au lieu d’inventer un résultat.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Un schéma fonctionnel personnel, la liste des données durables et les questions posées à l’équipe applicative. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Déplacer le même besoin vers une autre machine : qu’est-ce qui reste dans le contrat ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-01) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
