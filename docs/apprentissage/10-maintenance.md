# 10 — Exploiter et maintenir

**Projet : OpsDesk · Pilier : Maintenir/rétablir · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Choisis une maintenance limitée de ton environnement ; prépare le contrôle de ticket avant et après. Aucun patch réel n’est déclenché par la lecture de la fiche.

## 2. Objectif pédagogique

Exploiter et maintenir en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Day-2 désigne les opérations après la première installation : mises à jour, dérive, accès, capacité et qualité des données. Une maintenance possède un état initial, un risque, un retour et un contrôle métier.

## 5. Prérequis

Supervision minimale et contrôle métier disponibles, composant à maintenir identifié. Lire compatibilité, données durables et conditions de retour avant la maintenance. Une dépendance supposée à jour n’est pas un prérequis vérifié. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Identifier la VM Rocky Linux 10.2, le composant et la version concernés par une maintenance limitée. Préparer état initial, données témoins, accès, espace, capacité de retour et risque. Aucun changement de paquets, de service ou de version n’est implicite dans la lecture de cet exercice. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

## 7. Travail personnel

Choisir une maintenance proportionnée ; préparer compatibilité, état initial et retour ; l’exécuter personnellement sur la cible autorisée puis contrôler. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Comparer le premier écart à l’état de référence, isoler une cause et confirmer le retour avec le parcours témoin.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Relever version, état initial, risque et point de retour du seul composant choisi ; vérifier les conditions de compatibilité avant son changement.
- Comparer contrôle technique et invariant métier avant/après ; lire les journaux utiles et rechercher un effet indésirable.
- Expliquer ce qu’un retour de version peut rétablir et ce qui nécessite une restauration de données ; garder les limites et l’aide reçue.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Fiche avant/action/après, risque justifié, version et vérifications ; aide reçue déclarée. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Mettre tout à jour pour rendre un scan vert ; confondre retour d’image et retour de schéma ; changer plusieurs couches d’un coup. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le contrôle échoue après maintenance, comparer la seule couche changée avec l’état initial : incompatibilité de version, paramètre modifié ou permission. Vérifier la cause avant un retour ; un retour d’image ne restaure pas un ancien schéma DB.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Fiche avant/action/après, risque justifié, version et vérifications ; aide reçue déclarée. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quels contrôles restent valides si la maintenance ne redémarre aucun conteneur ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-10) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
