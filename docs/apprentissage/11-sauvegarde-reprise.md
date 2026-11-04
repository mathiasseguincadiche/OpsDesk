# 11 — Sauvegarder et restaurer

**Projet : OpsDesk · Pilier : Maintenir/rétablir · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Définis ce qui doit être retrouvé pour un ticket témoin, puis écris et pratique ta sauvegarde/restauration sur une cible distincte. Le script historique reste un corrigé après tentative.

## 2. Objectif pédagogique

Sauvegarder et restaurer en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Une sauvegarde doit permettre une restauration utile. Un dump, ses médias, la configuration nécessaire et les identités doivent être cohérents. Âge de capture, perte réellement observée et durée de reprise sont des mesures distinctes.

## 5. Prérequis

Données témoins connues et état métier vérifié, source identifiée, destination distincte et clé privée disponibles selon la stratégie proposée. Vérifier l’espace et les droits avant l’archivage, puis les prérequis de reconstruction avant la reprise. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Identifier la VM source et une cible de reprise distincte, créée seulement lorsqu’elle est utile et selon les ressources vérifiées du PC Fedora 45/KVM. Ne pas restaurer sur la source. Relever version applicative, base, médias éventuels, configuration privée, emplacement d’archive et clés nécessaires. Un second disque virtuel sur le même PC n’est pas une sauvegarde hors site. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

## 7. Travail personnel

Définir données, cohérence, chiffrement, destination, rétention et clé ; écrire ta procédure puis restaurer personnellement sur une cible isolée. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Identifier version, archive, clé, espace, accès, ordre DB/médias et référence attendue ; arrêter sur cible ou archive ambiguë.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Vérifier que l’archive, ses versions, ses données et sa clé permettent la reconstruction ; contrôler intégrité et cohérence, sans écraser une archive existante.
- Restaurer sur une cible distincte et vérifier l’accès au service ainsi que les mêmes références métier ; une archive créée n’est pas une preuve de reprise.
- Mesurer les bornes de capture, la perte de données et la durée de retour utiles ; distinguer RPO/RTO visés et réellement observés.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Intégrité contrôlée, mêmes références métier et mesures expliquées ; source préservée et limites explicites. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Stocker clé et archive au même endroit en parlant de hors-site ; restaurer seulement la DB ; prétendre cohérence sous écritures continues non testée. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le service restauré démarre mais qu’une donnée manque, départager mauvais point de capture, archive incomplète et média absent. Comparer référence, version et hash sur la cible de reprise ; conserver la source et la dernière archive connue.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Intégrité contrôlée, mêmes références métier et mesures expliquées ; source préservée et limites explicites. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quelle preuve démontrerait une reprise utile après perte de la machine plutôt qu’un simple remplacement de conteneur ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-11) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
