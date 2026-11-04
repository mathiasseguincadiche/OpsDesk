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

Mécanismes précédents compris, observations et accès nécessaires disponibles sur une cible isolée. Définir le symptôme et le contrôle utilisateur attendu avant de choisir un outil ou une modification. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Utiliser une copie ou une cible de laboratoire explicitement isolée et identifiée, avec le composant concerné et un retour prévu. Observer d’abord un symptôme disponible ; proposer un écart de configuration réversible seulement si une expérience contrôlée est nécessaire et autorisée. Ne pas modifier le réseau principal du PC. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

## 7. Travail personnel

Proposer une hypothèse, collecter les faits puis corriger le minimum sur un incident isolé autorisé ; conserver la chronologie et revalider. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Utiliser symptôme→couche→faits→hypothèse→test→correction→contrôle ; demander une aide précise si une donnée manque.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Formuler au moins deux hypothèses plausibles, ordonner les contrôles et expliquer quel résultat départagerait les hypothèses.
- Distinguer cause confirmée, fait observé et cause encore inconnue ; modifier un seul point après justification.
- Revalider le service et l’invariant utilisateur après correction, puis contrôler le retour et l’absence de régression dans le périmètre testé.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Symptôme, preuves, cause confirmée ou inconnue, correction, résultat métier et retour documentés. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Réinstaller avant de lire les logs ; provoquer une panne hors périmètre ; appeler cause racine la première hypothèse plausible. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Partir du symptôme exact et de son heure. Pour un accès impossible, départager refus de connexion et refus applicatif ; pour une donnée absente, départager requête, mauvais environnement et persistance. Choisir un test discriminant puis confirmer ou laisser la cause inconnue.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

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
