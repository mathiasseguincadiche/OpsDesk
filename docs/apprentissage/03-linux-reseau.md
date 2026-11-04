# 03 — Préparer Linux et le réseau

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Sur ton laboratoire identifié, vérifie séparément nom, route, écoute et droits. Prépare un compte ordinaire et l’accès requis au service ; garde les protections actives.

## 2. Objectif pédagogique

Préparer Linux et le réseau en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Linux porte des processus, fichiers et services avec des droits. DNS résout un nom ; une route choisit un trajet ; un port écoute ; le pare-feu autorise un flux. Ces contrôles répondent à des questions différentes.

## 5. Prérequis

Proposition d’architecture issue de l’exercice 02 ; accès autorisé au PC et résultats du pré-check hôte. Vérifier la disponibilité officielle de Rocky Linux 10.2 et son média avant d’en planifier l’installation. Aucun outil de virtualisation ni VM n’est considéré prêt sans contrôle. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le pré-check de l’hôte Fedora 45 se fait sur le PC personnel, pas dans WSL ni dans une VM. La première VM cible Rocky Linux 10.2 est préparée personnellement sous KVM/QEMU/libvirt uniquement après qualification du média et des prérequis. Identifier ensuite séparément l’hôte, la VM, son utilisateur, son réseau et son stockage. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

## 7. Travail personnel

Identifier le laboratoire autorisé ; préparer le système et l’accès ordinaire ; vérifier DNS, routes, écoute, permissions et protections nécessaires. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Observer utilisateur, processus/service, résolution, trajet, écoute puis autorisation ; changer une chose après confirmation.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Confirmer l’identité et la version de l’hôte puis de l’invité ; relever CPU, mémoire, disque et outils effectivement disponibles.
- Distinguer réseau prévu, route, résolution, écoute et autorisation : un résultat positif de l’un ne valide pas les autres.
- Vérifier SSH, utilisateur et permissions attendues ; relever les états de SELinux et firewalld sans les désactiver.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Identité de cible, carte de flux, accès vérifiés et diagnostic d’un défaut borné. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Désactiver SELinux/le pare-feu en bloc ; utiliser root partout ; diagnostiquer une route avec un test DNS seulement. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si SSH échoue, distinguer route ou nom incorrect, absence d’écoute et refus d’authentification. Contrôler successivement identité, trajet, écoute puis droits ; un accès par IP mais pas par nom oriente vers la résolution, sans la prouver à lui seul.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Identité de cible, carte de flux, accès vérifiés et diagnostic d’un défaut borné. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Comment montrer qu’un refus vient des droits et non du réseau ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-03) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
