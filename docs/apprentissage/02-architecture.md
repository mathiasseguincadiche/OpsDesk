# 02 — Concevoir l’architecture

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Propose une cible simple pour le service IT ; nomme accès utilisateur/opérateur, application et stockage. Explique les ressources et les points de panne sans adopter le schéma Codex comme réponse imposée.

## 2. Objectif pédagogique

Concevoir l’architecture en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

L’architecture traduit un besoin en ressources, flux et frontières de confiance. Un dessin doit expliquer les accès et la persistance, pas seulement aligner des logos.

## 5. Prérequis

Exercice 01 compris et besoins applicatifs reformulés. Connaître les contraintes de données et d’accès ; relever les ressources matérielles réelles ou les marquer NON VÉRIFIÉES. L’architecture sera une proposition à justifier. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Dessin et analyse à partir du contrat, sans création de ressource. Prévoir un hôte Fedora 45 avec KVM/QEMU et libvirt, et Rocky Linux 10.2 comme système invité cible ; disponibilité exacte, compatibilité et ressources restent à qualifier dans le guide de laboratoire. Distinguer le schéma personnel de la référence historique Codex.

## 7. Travail personnel

Produire une proposition de cible, les flux/protocoles, l’accès opérateur et les limites ; justifier ressources et stockage. Conserver la première proposition avant toute correction. Présenter ta reformulation avant de lire un schéma de référence.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Partir du symptôme utilisateur et traverser client, point d’entrée, application puis stockage.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Associer chaque composant proposé à un besoin du contrat ; identifier hôte, VM, application et données sans multiplier les machines.
- Expliquer les flux autorisés, les accès refusés et l’emplacement de chaque donnée durable.
- Comparer une alternative utile et indiquer le coût en ressources, le point de panne et la méthode de reconstruction à vérifier.
- Expliquer comment un ticket identifié, son titre, son état et sa relecture dans PostgreSQL seront contrôlés plus tard, sans inventer de sortie ou de capture.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Schéma technique personnel modifiable, choix argumentés et alternatives raisonnables. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Assimiler namespace, réseau conteneur et isolation de machines ; oublier où vivent les données. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si le schéma paraît répondre au besoin mais qu’un accès reste inexplicable, distinguer flux manquant et dépendance oubliée. Suivre une requête et demander où vit sa donnée durable avant d’ajouter un composant.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Schéma technique personnel modifiable, choix argumentés et alternatives raisonnables. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quel compromis changerait si la charge ou l’exigence de reprise augmentait ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-02) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
