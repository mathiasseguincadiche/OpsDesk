# 13 — Démontrer son autonomie

**Projet : OpsDesk · Pilier : Transverse · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Après les modules précédents, recevoir une nouvelle révision applicative identifiée et un symptôme borné différent de l’exemple. Proposer la livraison, la vérifier puis diagnostiquer avec une aide limitée.

## 2. Objectif pédagogique

Démontrer son autonomie en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

L’autonomie se constate sur une tâche nouvelle : comprendre le besoin, adapter une méthode, vérifier et expliquer. Un pipeline vert ou un fichier généré par Codex ne donne pas un niveau personnel.

## 5. Prérequis

Travaux précédents et preuves personnelles disponibles ; limites et aide reçue déclarées. Le nouveau cas est défini avant toute intervention et doit différer de l’exemple déjà guidé. Un module non exécuté reste identifié comme tel. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Reprendre un environnement personnel déjà qualifié et une variante nouvelle bornée ; identifier ce qui peut être réutilisé et ce qui doit être revalidé. Si une reconstruction est demandée, employer une cible neuve distincte et conserver l’ancienne. L’hôte, la VM invitée, la version et l’aide autorisée sont explicités avant l’épreuve. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

## 7. Travail personnel

Proposer et réaliser une solution à un scénario nouveau ; demander seulement le niveau d’aide nécessaire et expliquer tes décisions. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Décrire le blocage et les observations avant de demander une correction ; conserver ce qui a fonctionné et revoir une hypothèse à la fois.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Proposer sa démarche et ses risques avant l’aide, puis adapter la méthode à la variante nouvelle.
- Montrer un résultat technique, un diagnostic représentatif et une explication de ses choix ; les sorties copiées du laboratoire Codex ne sont pas des preuves personnelles.
- Déclarer l’assistance reçue et les points non vérifiés ; un L3 exige une adaptation ou un diagnostic nouveau avec aide limitée.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Démonstration personnelle sur un cas proche nouveau, diagnostic et justification ; conclusion qualitative argumentée. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Recopier une référence puis revendiquer L3 ; cacher l’aide reçue ; inventer une note de certification. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

La difficulté est une variante nouvelle, pas une panne forcée. Présenter les faits et ses hypothèses avant toute aide, choisir le test le plus discriminant et défendre la correction ; revalider le besoin utilisateur et déclarer ce qui n’a pas été couvert.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Démonstration personnelle sur un cas proche nouveau, diagnostic et justification ; conclusion qualitative argumentée. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Comment adapterais-tu cette solution à un autre besoin sans dépendre d’une procédure copiée ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-13) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
