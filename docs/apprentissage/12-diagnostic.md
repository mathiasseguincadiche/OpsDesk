# 12 — Diagnostiquer et rétablir

**Projet : OpsDesk · Pilier : Observer/diagnostiquer · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Un incident doit être réduit à des faits vérifiables avant de corriger. Le support doit pouvoir expliquer pourquoi un ticket est inaccessible et démontrer le rétablissement utile après une action limitée.

À partir d’un symptôme nouveau de ticket inaccessible ou non enregistrable, propose deux hypothèses et un test pour les départager ; ne provoque aucune panne sans cible et accord.

**Livrable attendu :** Symptôme, preuves, cause confirmée ou inconnue, correction, résultat métier et retour documentés. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Diagnostiquer consiste à éliminer des hypothèses avec des vérifications discriminantes. Rétablir exige un contrôle utilisateur après la correction ; une commande sans erreur n’est pas la fin de l’incident.

Un **symptôme** est ce qui est observé ; une **hypothèse** propose une cause ; un **test discriminant** produit un résultat qui distingue plusieurs hypothèses. Le premier message d’erreur n’est pas forcément la cause racine. La chronologie et l’identité de l’environnement empêchent de rapprocher des faits provenant de machines différentes.

Par exemple, un refus de connexion indique une difficulté avant une réponse HTTP ; un refus applicatif suppose qu’une application a répondu. Un ticket absent peut venir d’une requête incorrecte, d’une mauvaise base ou d’une écriture non persistée. Choisir le contrôle qui apporte une information nouvelle réduit les modifications au hasard.

**Micro-exercice fictif :** `/health/live` répond, `/health/ready` échoue et la création de ticket est impossible. Proposer deux hypothèses liées à PostgreSQL et un contrôle en lecture seule dont les résultats les départagent. Ne pas arrêter de service pour fabriquer le symptôme.

## Préparer la bonne cible

Mécanismes précédents compris, observations et accès nécessaires disponibles sur une cible isolée. Définir le symptôme et le contrôle utilisateur attendu avant de choisir un outil ou une modification.

Le poste de contrôle prévu est Fedora 45. Utiliser une copie ou une cible de laboratoire explicitement isolée et identifiée, avec le composant concerné et un retour prévu. Observer d’abord un symptôme disponible ; proposer un écart de configuration réversible seulement si une expérience contrôlée est nécessaire et autorisée. Ne pas modifier le réseau principal du PC. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Décrire heure, utilisateur, opération, cible et symptôme exact ; conserver les observations expurgées et l’état initial.
2. Écrire au moins deux hypothèses et prévoir pour chaque contrôle les conclusions possibles. Collecter le fait le plus discriminant sans multiplier les outils.
3. Corriger le seul point confirmé sur la cible autorisée ; refaire le contrôle métier, vérifier le retour et expliciter ce qui reste inconnu.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Utiliser symptôme→couche→faits→hypothèse→test→correction→contrôle ; demander une aide précise si une donnée manque.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Distinguer accès réseau, réponse applicative et accès SQL. Choisir un contrôle dont un résultat contredirait ton hypothèse ; si aucun résultat ne peut la réfuter, préciser d’abord la question.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Formuler au moins deux hypothèses plausibles, ordonner les contrôles et expliquer quel résultat départagerait les hypothèses.
- Distinguer cause confirmée, fait observé et cause encore inconnue ; modifier un seul point après justification.
- Revalider le service et l’invariant utilisateur après correction, puis contrôler le retour et l’absence de régression dans le périmètre testé.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Contre-test :** chercher une observation qui invaliderait l’explication retenue. Si elle existe, garder la cause inconnue ou réviser l’hypothèse. Une réinstallation ou une panne volontaire n’est pas nécessaire pour documenter ce raisonnement.

**Erreurs fréquentes :** Réinstaller avant de lire les logs ; provoquer une panne hors périmètre ; appeler cause racine la première hypothèse plausible.

**Démarche en cas d’écart :** Partir du symptôme exact et de son heure. Pour un accès impossible, départager refus de connexion et refus applicatif ; pour une donnée absente, départager requête, mauvais environnement et persistance. Choisir un test discriminant puis confirmer ou laisser la cause inconnue.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Quel nouveau test permettrait de réfuter ton explication sur un cas proche ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-12--diagnostiquer-et-rétablir) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](11-sauvegarde-reprise.md) · [Retour au parcours](README.md) · [Exercice suivant →](13-autonomie.md)
