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

Contrat applicatif compris, VM et accès qualifiés ; stratégie de stockage et de secrets proposée. Vérifier la compatibilité et la disponibilité du moteur choisi avant son installation. Aucun Dockerfile ou Compose historique n’est obligatoire. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Le moteur de conteneurs est préparé personnellement dans la VM Rocky Linux 10.2 qualifiée ; ne pas confondre un moteur Windows/WSL historique avec celui de la VM. Relever moteur, version, utilisateur, chemins persistants et ports réellement choisis. La recette du conteneur est à écrire à partir du contrat applicatif. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Le moteur étudié dans ce projet est Docker dans la VM ; vérifier sa version et son accès avant de proposer Dockerfile/Compose. Le service sans authentification reste un démonstrateur privé de laboratoire.

## 7. Travail personnel

Écrire ta recette et ta configuration d’exécution à partir du contrat ; construire, identifier la version et contrôler la donnée persistante. Le moteur étudié dans ce projet est Docker dans la VM ; vérifier sa version et son accès avant de proposer Dockerfile/Compose. Le service sans authentification reste un démonstrateur privé de laboratoire. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Séparer erreur de build, commande de lancement, droits, DNS, connexion DB et schéma ; regarder le premier message utile.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Relier code/commit, version de l’application et image réellement exécutée ; distinguer tag et digest.
- Vérifier séparément écoute, disponibilité des dépendances, paramètres privés et parcours utilisateur.
- Contrôler la donnée témoin après le remplacement applicatif prévu, avec stockage préservé et sans supprimer un volume existant.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Recette personnelle, image identifiable, configuration privée et parcours métier vérifié. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Inclure secrets/données dans l’image ; utiliser latest sans identité ; croire qu’un conteneur démarré prouve le métier. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le conteneur est vivant mais le service inutilisable, distinguer port non écouté, dépendance non prête et mauvais paramètre. Lire les journaux du seul composant concerné et tester le chemin de dépendance ; ne pas supprimer les données pour obtenir un redémarrage propre.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

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
