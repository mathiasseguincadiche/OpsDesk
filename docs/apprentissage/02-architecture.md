# 02 — Concevoir l’architecture

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

L’équipe veut un service compréhensible et reconstructible sur le PC disponible. Une architecture aide à localiser les accès, les données et les points de panne avant d’engager des ressources.

Propose une cible simple pour le service IT ; nomme accès utilisateur/opérateur, application et stockage. Explique les ressources et les points de panne sans adopter le schéma Codex comme réponse imposée.

**Livrable attendu :** Schéma technique personnel modifiable, choix argumentés et alternatives raisonnables. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

L’architecture traduit un besoin en ressources, flux et frontières de confiance. Un dessin doit expliquer les accès et la persistance, pas seulement aligner des logos.

Un schéma de présentation répond « à quoi sert le service et qui l’utilise ? ». Un schéma technique répond « où s’exécute chaque composant, par quel flux et avec quels droits ? ». Les deux dessins ont des publics différents. La cible personnelle est ta proposition ; le schéma Codex décrit une référence historique.

Un composant doit résoudre un besoin : séparer les données du processus évite de les perdre quand on remplace l’application. Cela ne rend pas le disque disponible en cas de panne du PC. Comparer une alternative simple aide à expliquer le compromis coût, mémoire, maintenance et reprise, sans chercher une architecture de production.

**Question de conception :** si le disque hébergeant PostgreSQL devient indisponible, quel besoin n’est plus couvert ? Ajouter une seconde copie du processus Flask résout-il ce problème ?

## Préparer la bonne cible

Exercice 01 compris et besoins applicatifs reformulés. Connaître les contraintes de données et d’accès ; relever les ressources matérielles réelles ou les marquer NON VÉRIFIÉES. L’architecture sera une proposition à justifier.

Dessin et analyse à partir du contrat, sans création de ressource. Prévoir un hôte Fedora 45 avec KVM/QEMU et libvirt, et Rocky Linux 10.2 comme système invité cible ; disponibilité exacte, compatibilité et ressources restent à qualifier dans le guide de laboratoire. Distinguer le schéma personnel de la référence historique Codex.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Pour 01/02, la cible est le document ou le dessin : aucun terminal ni VM requis.

## Réaliser soi-même et demander un indice

1. Dresser la liste des fonctions, données durables, accès utilisateur et accès opérateur ; garder les contraintes du contrat visibles.
2. Proposer tes composants et tracer les flux avec sens, protocole, origine et destination. Dimensionner d’après les ressources mesurées ou signaler NON VÉRIFIÉ.
3. Comparer une alternative utile, identifier les points de panne et expliquer comment tu reconstruirais chaque composant. Produire toi-même source .drawio et export .svg distincts, sans Mermaid.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Partir du symptôme utilisateur et traverser client, point d’entrée, application puis stockage.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Faire parcourir au dessin une requête et son retour, puis un accès SSH opérateur. Un flux qui traverse une frontière doit avoir une destination et un besoin explicites.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Associer chaque composant proposé à un besoin du contrat ; identifier hôte, VM, application et données sans multiplier les machines.
- Expliquer les flux autorisés, les accès refusés et l’emplacement de chaque donnée durable.
- Comparer une alternative utile et indiquer le coût en ressources, le point de panne et la méthode de reconstruction à vérifier.
- Expliquer comment un ticket identifié, son titre, son état et sa relecture dans PostgreSQL seront contrôlés plus tard, sans inventer de sortie ou de capture.

**Revue contradictoire, sans création de ressource :** rechercher un flux sans destination, un stockage sans propriétaire ou une exposition incompatible avec l’absence d’authentification. Corriger le dessin et expliquer la limite restante.

**Erreurs fréquentes :** Assimiler namespace, réseau conteneur et isolation de machines ; oublier où vivent les données.

**Démarche en cas d’écart :** Si le schéma paraît répondre au besoin mais qu’un accès reste inexplicable, distinguer flux manquant et dépendance oubliée. Suivre une requête et demander où vit sa donnée durable avant d’ajouter un composant.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

**Réutilisation :** Quel compromis changerait si la charge ou l’exigence de reprise augmentait ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-02--concevoir-larchitecture) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](01-application.md) · [Retour au parcours](README.md) · [Exercice suivant →](03-linux-reseau.md)
