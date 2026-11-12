# 13 — Démontrer son autonomie

**Projet : OpsDesk · Pilier : Transverse · Accompagnement : limité et déclaré.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

L’équipe doit pouvoir confier une adaptation nouvelle à un opérateur qui justifie ses choix. L’épreuve porte sur une situation définie après les tentatives guidées, avec un degré d’aide convenu et déclaré.

Après les modules précédents, recevoir une nouvelle révision applicative identifiée et un symptôme borné différent de l’exemple. Proposer la livraison, la vérifier puis diagnostiquer avec une aide limitée.

**Livrable attendu :** Démonstration personnelle sur un cas proche nouveau, diagnostic et justification ; conclusion qualitative argumentée. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

L’autonomie se constate sur une tâche nouvelle : comprendre le besoin, adapter une méthode, vérifier et expliquer. Un pipeline vert ou un fichier généré ne donne pas un niveau personnel.

Réutiliser une méthode consiste à reconnaître le besoin et les contrôles qui restent valides, puis à adapter les éléments qui changent. L’autonomie ne signifie pas travailler sans documentation : elle exige de choisir les bonnes références, de tester ses hypothèses et d’expliquer ses limites.

Avant l’épreuve, définir la variante, les accès, les risques, le livrable et l’aide admise. Un exemple déjà résolu n’est pas une tâche nouvelle. Si une aide ciblée devient nécessaire, la consigner et réévaluer la portée du résultat ; une difficulté ne constitue pas un échec définitif du parcours.

**Question préalable :** quelle différence entre le scénario connu et la variante obligera réellement à prendre une décision ou diagnostiquer ? Si tout peut être recopié sans raisonnement, reformuler la variante avant de commencer.

## Préparer la bonne cible

Travaux précédents et preuves personnelles disponibles ; limites et aide reçue déclarées. Le nouveau cas est défini avant toute intervention et doit différer de l’exemple déjà guidé. Un module non exécuté reste identifié comme tel.

Le poste de contrôle prévu est Fedora 45. Reprendre un environnement personnel déjà qualifié et une variante nouvelle bornée ; identifier ce qui peut être réutilisé et ce qui doit être revalidé. Si une reconstruction est demandée, employer une cible neuve distincte et conserver l’ancienne. L’hôte, la VM invitée, la version et l’aide autorisée sont explicités avant l’épreuve. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Recevoir un cas nouveau borné et identifier ce qui est réutilisable ; proposer ta méthode et les critères de réussite avant de demander des indices.
2. Réaliser et diagnostiquer personnellement sur la cible qualifiée ; noter chaque aide demandée et son effet sur la suite.
3. Démontrer résultat technique, ticket témoin, diagnostic et justification ; rendre une conclusion qualitative sur les cinq responsabilités, avec limites et prochaine adaptation.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Décrire le blocage et les observations avant de demander une correction ; conserver ce qui a fonctionné et revoir une hypothèse à la fois.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Reprendre tes propres preuves et expliquer pourquoi leurs conditions s’appliquent encore. Pour le blocage nouveau, présenter les faits, deux hypothèses et le test envisagé avant une demande d’aide.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Proposer sa démarche et ses risques avant l’aide, puis adapter la méthode à la variante nouvelle.
- Montrer un résultat technique, un diagnostic représentatif et une explication de ses choix ; les sorties copiées du laboratoire historique ne sont pas des preuves personnelles.
- Déclarer l’assistance reçue et les points non vérifiés ; un L3 exige une adaptation ou un diagnostic nouveau avec aide limitée.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Contre-épreuve :** expliquer quel fait montrerait que la solution connue ne convient plus. Si un corrigé complet a été consulté, conserver le travail réalisé avec assistance et prévoir une autre variante pour évaluer L3 ; ne pas attribuer un niveau à l’avance.

**Erreurs fréquentes :** Recopier une référence puis revendiquer L3 ; cacher l’aide reçue ; inventer une note de certification.

**Démarche en cas d’écart :** La difficulté est une variante nouvelle, pas une panne forcée. Présenter les faits et ses hypothèses avant toute aide, choisir le test le plus discriminant et défendre la correction ; revalider le besoin utilisateur et déclarer ce qui n’a pas été couvert.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Comment adapterais-tu cette solution à un autre besoin sans dépendre d’une procédure copiée ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-13--démontrer-son-autonomie) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](12-diagnostic.md) · [Retour au parcours](README.md)
