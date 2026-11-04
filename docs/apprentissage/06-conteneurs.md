# 06 — Conteneuriser

**Projet : OpsDesk · Pilier : Faciliter la livraison · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Conteneurise le programme fourni ; montre quelle version répond et relis un ticket après le remplacement applicatif prévu, avec stockage conservé.

## 2. Objectif pédagogique

Conteneuriser en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Une image fige le programme et ses dépendances ; un conteneur est un processus qui l’utilise. Réseau, volumes, paramètres et secrets déterminent son fonctionnement. L’image n’est pas une sauvegarde de la base.

## 5. Prérequis

Exercice 05 compris et résultats utiles disponibles ; pré-check du laboratoire à refaire avant une action. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Laboratoire personnel identifié par Mathias : machine, utilisateur, répertoire, version, ressources et accès. Les exercices mutateurs attendent une cible autorisée ; les essais WSL de Codex ne la qualifient pas.

## 7. Travail personnel

Écrire ta recette et ta configuration d’exécution à partir du contrat ; construire, identifier la version et contrôler la donnée persistante. Conteneurise le programme fourni ; montre quelle version répond et relis un ticket après le remplacement applicatif prévu, avec stockage conservé. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Séparer erreur de build, commande de lancement, droits, DNS, connexion DB et schéma ; regarder le premier message utile.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

Expliquer le composant et son rôle, confronter attendu/observé, vérifier un ticket identifié, son titre et son état. Chaque contrôle doit appartenir à ta cible, ta version et ton exécution. Signaler ce qui n’a pas pu être testé.

## 11. Résultat attendu

Recette personnelle, image identifiable, configuration privée et parcours métier vérifié. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Inclure secrets/données dans l’image ; utiliser latest sans identité ; croire qu’un conteneur démarré prouve le métier. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Séparer erreur de build, commande de lancement, droits, DNS, connexion DB et schéma ; regarder le premier message utile. Noter symptôme, hypothèse, contrôle discriminant, cause observée ou encore inconnue, correction et test final.

## 14. Preuves à conserver

Recette personnelle, image identifiable, configuration privée et parcours métier vérifié. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Comment donner au développeur un test reproductible sans lui donner les droits administrateur de l’hôte ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-06) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
