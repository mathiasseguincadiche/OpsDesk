# 04 — Provisionner avec Terraform

**Projet : OpsDesk · Pilier : Automatiser · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Écris les ressources du laboratoire autorisé et explique chaque différence du plan. Montre que le state correspond à la bonne cible avant ton apply.

## 2. Objectif pédagogique

Provisionner avec Terraform en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Terraform compare la configuration au state et à l’état distant pour calculer un plan. Le state contient des identités et parfois des secrets ; un fichier terraform_data local ne crée pas une VM.

## 5. Prérequis

Accès libvirt et laboratoire identifiés à l’exercice 03 ; versions de Terraform et du fournisseur vérifiées dans le guide. Distinguer ressource existante, ressource d’essai à créer et ressource déjà gérée. Pas de configuration complète fournie à recopier. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45 ; les ressources à gérer sont des ressources KVM/libvirt identifiées du laboratoire. Terraform et la version du fournisseur libvirt choisi doivent être vérifiés séparément. La VM Rocky Linux 10.2 est la cible ; une VM créée manuellement n’appartient pas automatiquement au state Terraform. Ne pas adopter, remplacer ou supprimer une ressource existante par supposition. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

## 7. Travail personnel

Choisir le fournisseur du laboratoire autorisé ; écrire ressources/variables/backend ; valider et lire le plan avant tout apply personnel. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Localiser l’erreur entre syntaxe, provider/authentification, droits, quota ou dérive ; ne pas supprimer le state comme premier réflexe.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Expliquer le fournisseur, sa version, l’URI libvirt et les ressources visées ; chaque différence du plan doit correspondre au laboratoire autorisé.
- Après son intervention personnelle, rapprocher l’identifiant réel de la ressource et son état du plan lu ; un terraform_data local ne vaut pas création de VM.
- Rejouer le plan sans changement voulu, interpréter le résultat et protéger le state ; ne pas publier un state pour prouver la réussite.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Code personnel, plan expliqué, état protégé et ressources observées correspondant au plan. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Confondre validation syntaxique et ressource créée ; versionner le state ; forcer un apply sur la mauvaise cible. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le plan ne vise pas la VM attendue, distinguer mauvais workspace/backend, mauvais URI libvirt et ressource non gérée. Lire la cible et les identifiants avant toute correction ; ne pas effacer le state, importer ou détruire une VM pour faire disparaître l’écart.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Code personnel, plan expliqué, état protégé et ressources observées correspondant au plan. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Comment reprendre le même besoin dans un second environnement sans partager les identités de ressources ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-04) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
