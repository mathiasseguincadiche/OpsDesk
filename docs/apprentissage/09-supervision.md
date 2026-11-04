# 09 — Superviser

**Projet : OpsDesk · Pilier : Observer/diagnostiquer · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

## 1. Situation professionnelle

L’équipe attend des demandes IT créées, consultables et suivies sans perdre les tickets. Utilise les signaux applicatifs fournis et un contrôle de ticket. Relie une alerte à l’indisponibilité réelle du besoin, puis explique le retour attendu.

## 2. Objectif pédagogique

Superviser en reliant décision, action, observation et explication. Tu peux demander une explication avant chaque étape ; rédige néanmoins toi-même le schéma, la configuration et les preuves.

## 3. Besoin applicatif

Un ticket identifié, son titre et son état doit rester contrôlable. Le contrat applicatif, pas une ancienne recette d’hébergement, définit les besoins du logiciel.

## 4. Concepts à comprendre

Une métrique est une mesure, un journal explique un événement et une alerte signale un besoin d’action. La disponibilité d’un processus ne garantit pas le succès d’un parcours métier.

## 5. Prérequis

Parcours applicatif et points de santé compris ; cible et version identifiées, collecte proposée. Vérifier les outils réellement installés et les accès autorisés. Ne pas définir une alerte à partir d’un compteur dont le sens ou la portée reste inconnu. Lire [le contrat](../contrat-applicatif.md) et le [cadre du parcours](README.md). Ne pas importer un résultat Codex comme preuve personnelle.

## 6. Environnement et matériel

Le poste de contrôle prévu est Fedora 45. Choisir une collecte et une visualisation proportionnées au laboratoire déjà qualifié, sans créer une VM par outil. Identifier source de métriques, collecteur, destinataire d’alerte autorisé, réseau et limites de ressources. Les métriques d’une application ne signifient pas que Prometheus ou Grafana est installé. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Prévoir Prometheus pour la collecte et Grafana pour une vue utile. k6 reste un essai de charge personnel, borné sur une cible locale autorisée : choisir débit/concurrence, durée, seuil d’arrêt et mesure de latence/erreurs avant exécution. Ne pas charger une cible publique ou le PC sans limite. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

## 7. Travail personnel

Choisir des signaux utiles ; écrire collecte, tableau et règle d’alerte ; vérifier la détection et la route autorisée sur un cas borné. Prévoir Prometheus pour la collecte et Grafana pour une vue utile. k6 reste un essai de charge personnel, borné sur une cible locale autorisée : choisir débit/concurrence, durée, seuil d’arrêt et mesure de latence/erreurs avant exécution. Ne pas charger une cible publique ou le PC sans limite. Conserver la première proposition avant toute correction.

## 8. Contraintes

Application fictive sans authentification utilisateur ; accès local ; PostgreSQL durable ; santé live/ready et version distinctes. Identifier état initial, effet attendu et retour. Un cloud payant, une exposition réelle, un réseau sensible ou une panne/destruction exige un accord ciblé ; la lecture de cette fiche n’autorise pas ces actions.

## 9. Indices progressifs

**Indice :** Formuler le symptôme, comparer métriques/logs/événements et contrôler la dépendance suspecte sans multiplier les modifications.

**Explication ciblée, sur demande :** relier le concept à un ticket identifié, son titre et son état, avec un exemple limité et un résultat observable.

**Correction accompagnée :** montrer ta tentative et le premier écart ; Codex corrige le point précis puis te demande de revalider et d’expliquer.

## 10. Vérifications à effectuer

- Distinguer une mesure du processus, une dépendance prête et un contrôle du besoin utilisateur ; vérifier les unités, la portée et les labels.
- Montrer collecte, visualisation utile, règle et destinataire autorisé ; un tableau sans données ou un /metrics isolé n’est pas une supervision reçue.
- Sur un cas réversible autorisé, rapprocher signal, alerte, journaux et retour à l’état attendu ; consigner aussi les faux positifs ou contrôles non exécutés.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

Pour chaque observation, écrire d’abord le résultat attendu, puis lire et interpréter le résultat réel. Un exemple fourni par Codex ne remplace pas ta mesure.

## 11. Résultat attendu

Signal choisi pour le métier, alerte constatée, logs corrélés et retour observé ; pas seulement une capture de tableau vide. Le résultat est à produire, pas déjà obtenu.

## 12. Erreurs fréquentes

Compter uniquement HTTP200 ; alerte sans destinataire ; générer un identifiant de ticket comme label à forte cardinalité. En cas d’écart, conserver les faits utiles sans secret et ne pas multiplier les modifications.

## 13. Démarche de diagnostic

Si un tableau est vide, distinguer absence d’échantillons, mauvaise requête et fenêtre de temps. Vérifier la cible collectée avant le panneau. Si aucune alerte n’arrive, distinguer règle non déclenchée et routage non configuré avant de provoquer une panne.

Conserver le fil : symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale. Une observation en lecture seule suffit tant qu’aucun changement n’est nécessaire.

## 14. Preuves à conserver

Signal choisi pour le métier, alerte constatée, logs corrélés et retour observé ; pas seulement une capture de tableau vide. Ajouter date, environnement, version/commit, action personnelle, attendu/observé, difficulté, correction et aide reçue. Ne joindre aucun secret, cookie, token ou state privé.

## 15. Synthèse

En quelques phrases : quel besoin as-tu couvert, quelle décision as-tu prise et quel contrôle la soutient ? Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

## 16. Réutilisation des acquis

Quel indicateur garde son sens quand on change le nombre de réplicas ou redémarre le processus ? Relier ta réponse à un autre projet sans en recopier une solution complète.

## 17. Validation et autonomie

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication sont vérifiés séparément. L0=découverte ; L1=compréhension ; L2=réalisation personnelle ; L3=adaptation/diagnostic d’un cas nouveau avec aide limitée. Aucun niveau n’est attribué par la présence de la fiche.

## 18. Corrigé séparé

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-09) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.
