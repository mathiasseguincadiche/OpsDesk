# 05 — Configurer avec Ansible

**Projet : OpsDesk · Pilier : Automatiser · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Configure la cible choisie, rejoue le playbook et explique une tâche non convergente. Un rendu JSON localhost historique ne remplit pas cette évaluation.

## 2. Objectif pédagogique

Configurer avec Ansible en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Ansible applique des tâches à un inventaire. Un module convergent décrit un état ; l’idempotence se vérifie par une seconde passe et par l’état effectif, pas par un commentaire.

## 5. Prérequis

Exercice 04 compris et résultats utiles disponibles ; pré-check du laboratoire à refaire avant une action. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Laboratoire personnel identifié par Mathias : machine, utilisateur, répertoire, version, ressources et accès. Les exercices mutateurs attendent une cible autorisée ; les essais WSL de Codex ne la qualifient pas.

## 7. Travail personnel

Écrire inventaire, variables et playbook pour la cible choisie ; limiter become ; protéger les valeurs sensibles ; vérifier puis rejouer personnellement. Configure la cible choisie, rejoue le playbook et explique une tâche non convergente. Un rendu JSON localhost historique ne remplit pas cette évaluation. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Lire le premier hôte/tâche/code en défaut ; vérifier accès, chemin, variable, module et privilège avant correction ciblée.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

Expliquer le composant et son rôle, confronter attendu/observé, vérifier un ticket identifié, son titre et son état. Chaque contrôle doit appartenir à ta cible, ta version et ton exécution. Signaler ce qui n’a pas pu être testé.

## 11. Résultat attendu

Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Utiliser shell pour chaque action ; confondre changed=0 avec service fonctionnel ; laisser une variable sensible dans un log. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Lire le premier hôte/tâche/code en défaut ; vérifier accès, chemin, variable, module et privilège avant correction ciblée. Noter symptôme, hypothèse, contrôle discriminant, cause observée ou encore inconnue, correction et test final.

## 14. Preuves à conserver

Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quelle partie de ta configuration peut être réutilisée sans copier les secrets ni les adresses ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-05) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
