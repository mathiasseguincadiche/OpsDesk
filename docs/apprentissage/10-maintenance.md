# 10 — Exploiter et maintenir

**Projet : OpsDesk · Pilier : Maintenir/rétablir · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Une installation qui fonctionne aujourd’hui doit pouvoir évoluer sans perte de tickets. Une maintenance limitée rend les risques, les contrôles et le retour compréhensibles avant de modifier une version.

Choisis une maintenance limitée de ton environnement ; prépare le contrôle de ticket avant et après. Aucun patch réel n’est déclenché par la lecture de la fiche.

**Livrable attendu :** Fiche avant/action/après, risque justifié, version et vérifications ; aide reçue déclarée. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Day-2 désigne les opérations après la première installation : mises à jour, dérive, accès, capacité et qualité des données. Une maintenance possède un état initial, un risque, un retour et un contrôle métier.

La maintenance Day-2 commence après la mise en service : versions, capacité, accès, dérive et qualité des données. Le périmètre utile est une couche choisie et un effet mesurable. Le point de retour doit rester disponible tant que la validation n’est pas terminée.

Un rollback d’image remplace la version applicative ; il ne remet pas la base dans son état antérieur. Un changement de schéma ou de format peut rendre le retour incompatible. Comparer avant/après le composant, sa configuration et le même ticket permet d’éviter de confondre succès de mise à jour et succès métier.

**Question :** la version répond après maintenance, mais un ancien ticket n’est plus lisible. Quelles observations départagent un problème de format, une mauvaise base cible et une permission modifiée ?

## Préparer la bonne cible

Supervision minimale et contrôle métier disponibles, composant à maintenir identifié. Lire compatibilité, données durables et conditions de retour avant la maintenance. Une dépendance supposée à jour n’est pas un prérequis vérifié.

Les opérations sont lancées depuis `srv-admin`. Identifier la VM Rocky Linux 10.2 (`srv-admin`, `srv-app` ou `srv-k3s`), le composant et la version concernés par une maintenance limitée. Préparer état initial, données témoins, accès, espace, capacité de retour et risque. Aucun changement de paquets, de service ou de version n’est implicite dans la lecture de cet exercice. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Choisir un seul composant et justifier le besoin ; lire compatibilité et limites, identifier versions initiale/cible, accès, données et moyens de retour.
2. Écrire ta fiche avant/action/après avec critères d’arrêt et contrôle métier ; faire revoir une incertitude avant l’intervention personnelle.
3. Réaliser uniquement le changement autorisé, puis comparer état technique, journaux et ticket témoin. Décider de conserver ou revenir selon des faits, en préservant les preuves.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Comparer le premier écart à l’état de référence, isoler une cause et confirmer le retour avec le parcours témoin.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Comparer le premier écart au changement réellement effectué. Vérifier configuration et compatibilité avant de conclure à un défaut applicatif ; ne pas changer une seconde couche pour compenser sans hypothèse vérifiée.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Relever version, état initial, risque et point de retour du seul composant choisi ; vérifier les conditions de compatibilité avant son changement.
- Comparer contrôle technique et invariant métier avant/après ; lire les journaux utiles et rechercher un effet indésirable.
- Expliquer ce qu’un retour de version peut rétablir et ce qui nécessite une restauration de données ; garder les limites et l’aide reçue.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Répétition sans mutation :** simuler la décision d’arrêt si le contrôle préalable de compatibilité échoue. Un refus argumenté d’engager la maintenance est un résultat de préparation ; il ne vaut pas maintenance exécutée.

**Erreurs fréquentes :** Mettre tout à jour pour rendre un scan vert ; confondre retour d’image et retour de schéma ; changer plusieurs couches d’un coup.

**Démarche en cas d’écart :** Si le contrôle échoue après maintenance, comparer la seule couche changée avec l’état initial : incompatibilité de version, paramètre modifié ou permission. Vérifier la cause avant un retour ; un retour d’image ne restaure pas un ancien schéma DB.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Quels contrôles restent valides si la maintenance ne redémarre aucun conteneur ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-10--exploiter-et-maintenir) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](09-supervision.md) · [Retour au parcours](README.md) · [Exercice suivant →](11-sauvegarde-reprise.md)
