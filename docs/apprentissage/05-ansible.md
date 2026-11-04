# 05 — Configurer avec Ansible

**Projet : OpsDesk · Pilier : Automatiser · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Configure la cible choisie, rejoue le playbook et explique une tâche non convergente. Un rendu JSON localhost historique ne remplit pas cette évaluation.

## 2. Objectif pédagogique

Configurer avec Ansible en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Ansible applique des tâches à un inventaire. Un module convergent décrit un état ; l’idempotence se vérifie par une seconde passe et par l’état effectif, pas par un commentaire.

## 5. Prérequis

Cible VM et propriétaire de ressources identifiés aux exercices 03/04 ; accès SSH vérifié avec le compte ordinaire prévu. Vérifier la version d’Ansible sur le contrôleur et les prérequis Python des modules sur l’invité. Ne pas supposer un inventaire correct parce qu’un nom répond au ping ICMP. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Ansible est piloté depuis le poste Fedora 45 vers la VM Rocky Linux 10.2 identifiée. Vérifier inventaire, résolution, SSH, utilisateur distant, Python requis par les modules et élévation ciblée avant une tâche mutatrice. Les paquets, services et protections sont ceux de la VM cible, pas ceux du poste de contrôle. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

## 7. Travail personnel

Écrire inventaire, variables et playbook pour la cible choisie ; limiter become ; protéger les valeurs sensibles ; vérifier puis rejouer personnellement. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Lire le premier hôte/tâche/code en défaut ; vérifier accès, chemin, variable, module et privilège avant correction ciblée.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Vérifier l’inventaire et l’identité SSH réelle de la VM avant les changements ; un test Ansible de connexion vérifie aussi son prérequis Python.
- Comparer première et seconde passes ; expliquer chaque changement restant sans masquer un échec avec une condition arbitraire.
- Contrôler le paramètre ou service réellement configuré et son effet utile ; changed=0 seul ne démontre pas le fonctionnement.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Utiliser shell pour chaque action ; confondre changed=0 avec service fonctionnel ; laisser une variable sensible dans un log. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si Ansible échoue, distinguer accès SSH, Python distant et élévation. Si une seconde passe change encore, lire la tâche concernée et son état attendu ; corriger la cause puis vérifier le service, sans rendre silencieusement la tâche inconditionnelle.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quelle partie de ta configuration peut être réutilisée sans copier les secrets ni les adresses ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-05) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
