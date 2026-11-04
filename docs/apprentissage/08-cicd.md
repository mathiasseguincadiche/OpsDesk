# 08 — Construire la CI/CD

**Projet : OpsDesk · Pilier : Faciliter la livraison · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Construis une première chaîne GitHub Actions. Étudie le cas historique où le smoke écrit ci-business.json mais la reprise lit business-smoke.json : explique quel ticket est utilisé et comment prouver la correction, sans recopier le pipeline.

## 2. Objectif pédagogique

Construire la CI/CD en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

La CI formalise des contrôles déjà compris ; la livraison déplace un artefact identifié vers une cible autorisée. Une preuve doit appartenir au commit/run courant, pas être un ancien PASS joint au hasard.

## 5. Prérequis

Procédure manuelle de test et de livraison comprise, artefact identifié et cible de validation autorisée. L’étude K3s est disponible ; une livraison conteneur sur la cible retenue reste possible si K3s n’a pas encore été qualifié. Ne pas contourner un blocage en prétendant un déploiement de cluster. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Les sources personnelles sont conservées dans le dépôt GitHub principal du projet. Identifier séparément le runner choisi et la VM Rocky Linux 10.2 cible sous KVM ; un runner hébergé n’accède pas implicitement au laboratoire local. La cible de livraison, son accès et ses permissions doivent être proposés et vérifiés avant tout déploiement. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

La chaîne étudiée est GitHub Actions, avec GHCR pour un artefact identifié et Trivy pour conserver le verdict de scan. Définir permissions minimales, secrets, rétention des preuves et arrêt sur échec. Le diagnostic du contrat de preuve historique ci-business.json/business-smoke.json reste un cas à expliquer, pas un pipeline à recopier.

## 7. Travail personnel

Définir déclencheurs, jobs, dépendances, permissions, variables, artefacts et critères ; construire ta chaîne à partir de la procédure manuelle vérifiée. La chaîne étudiée est GitHub Actions, avec GHCR pour un artefact identifié et Trivy pour conserver le verdict de scan. Définir permissions minimales, secrets, rétention des preuves et arrêt sur échec. Le diagnostic du contrat de preuve historique ci-business.json/business-smoke.json reste un cas à expliquer, pas un pipeline à recopier. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Nommer job, étape, commande, message, hypothèse et test final ; distinguer refus d’accès, variable absente, test métier et mauvais artefact.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Relier commit, run, jobs et artefact testé ; conserver le premier échec utile et vérifier que la preuve appartient au run courant.
- Promouvoir le même artefact vers la cible retenue, avec accès justifiés et accord d’environnement ; ne pas reconstruire sous le même tag entre test et livraison.
- Contrôler version et données après livraison et après le retour prévu ; un job de succès sans contrôle de la cible ne vaut pas déploiement.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Jobs personnels expliqués, échec discriminant diagnostiqué, même artefact testé livré et contrôle métier après livraison. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Déployer depuis un runner public en supposant un accès au KVM local ; secrets dans les logs ; ancien JSON PASS présenté comme preuve du run. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le pipeline passe mais la cible affiche une autre version, distinguer artefact reconstruit, mauvais environnement et preuve périmée. Comparer commit/run/digest à l’identité servie ; corriger le point démontré et refaire le contrôle utilisateur.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Jobs personnels expliqués, échec discriminant diagnostiqué, même artefact testé livré et contrôle métier après livraison. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Comment prouver qu’une promotion n’a pas reconstruit une image différente ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-08) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
