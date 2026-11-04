# 12 — Diagnostiquer et rétablir

**Projet : OpsDesk · Pilier : Observer/diagnostiquer · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. À partir d’un symptôme nouveau de ticket inaccessible ou non enregistrable, propose deux hypothèses et un test pour les départager ; ne provoque aucune panne sans cible et accord.

## 2. Objectif pédagogique

Diagnostiquer et rétablir en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Diagnostiquer consiste à éliminer des hypothèses avec des vérifications discriminantes. Rétablir exige un contrôle utilisateur après la correction ; une commande sans erreur n’est pas la fin de l’incident.

## 5. Prérequis

Exercice 11 compris et résultats utiles disponibles ; pré-check du laboratoire à refaire avant une action. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Laboratoire personnel identifié par Mathias : machine, utilisateur, répertoire, version, ressources et accès. Les exercices mutateurs attendent une cible autorisée ; les essais WSL de Codex ne la qualifient pas.

## 7. Travail personnel

Proposer une hypothèse, collecter les faits puis corriger le minimum sur un incident isolé autorisé ; conserver la chronologie et revalider. À partir d’un symptôme nouveau de ticket inaccessible ou non enregistrable, propose deux hypothèses et un test pour les départager ; ne provoque aucune panne sans cible et accord. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Utiliser symptôme→couche→faits→hypothèse→test→correction→contrôle ; demander une aide précise si une donnée manque.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

Expliquer le composant et son rôle, confronter attendu/observé, vérifier un ticket identifié, son titre et son état. Chaque contrôle doit appartenir à ta cible, ta version et ton exécution. Signaler ce qui n’a pas pu être testé.

## 11. Résultat attendu

Symptôme, preuves, cause confirmée ou inconnue, correction, résultat métier et retour documentés. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Réinstaller avant de lire les logs ; provoquer une panne hors périmètre ; appeler cause racine la première hypothèse plausible. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Utiliser symptôme→couche→faits→hypothèse→test→correction→contrôle ; demander une aide précise si une donnée manque. Noter symptôme, hypothèse, contrôle discriminant, cause observée ou encore inconnue, correction et test final.

## 14. Preuves à conserver

Symptôme, preuves, cause confirmée ou inconnue, correction, résultat métier et retour documentés. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quel nouveau test permettrait de réfuter ton explication sur un cas proche ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-12) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
