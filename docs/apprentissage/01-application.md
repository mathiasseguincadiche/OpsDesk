# 01 — Comprendre l’application

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Le support doit pouvoir retrouver une demande après sa création et expliquer son état. Avant de choisir une machine, comprendre ce que le programme fait permet de distinguer une panne du logiciel, de son accès et de sa base.

Dessine le trajet d’une création de ticket ; relève dans le contrat le rôle de PostgreSQL, les paramètres attendus et l’absence d’authentification. Ne lance rien pour cette première lecture.

**Livrable attendu :** Un schéma fonctionnel personnel, la liste des données durables et les questions posées à l’équipe applicative. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Un contrat applicatif décrit ce que le logiciel exige et garantit ; il ne choisit pas ton infrastructure. Un parcours utilisateur relie une entrée HTTP à une donnée persistante.

HTTP est l’échange entre client et application ; l’API fournit des réponses JSON, tandis que les pages HTML servent l’utilisateur. Flask traite la requête ; psycopg communique avec PostgreSQL. La mémoire du processus n’est pas la donnée durable : le ticket doit être enregistré dans la base pour survivre au remplacement de l’application.

Dans le contrat, distinguer une entrée, une règle et un effet : un titre accepté n’autorise pas toutes les transitions de statut. Une réponse de santé renseigne un aspect du service ; elle ne prouve pas, seule, qu’un ticket peut être créé puis relu. La protection CSRF limite certains envois de formulaire ; elle n’identifie aucun utilisateur.

**Question de lecture :** quel composant conserve le titre d’un ticket si le processus Flask s’arrête ? Quelle information manquerait encore après un simple HTTP 200 sur `/health/live` ?

## Préparer la bonne cible

Aucun module technique préalable. Lire le contrat applicatif et les règles de responsabilité ; disposer d’un outil de dessin et noter ses questions. Aucun logiciel d’infrastructure n’est supposé installé.

Lecture du contrat et dessin, sans installation ni déploiement. Le poste hôte prévu est Fedora 45 ; aucune VM ni authentification à un laboratoire historique ne sont requises pour comprendre l’application.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Pour 01/02, la cible est le document ou le dessin : aucun terminal ni VM requis.

## Réaliser soi-même et demander un indice

1. Lire les fonctions, les données persistantes et les limites du contrat ; relever les termes inconnus sans installer d’outil.
2. Dessiner soi-même le trajet d’une création puis d’une consultation ; placer les paramètres et les secrets hors des données métier.
3. Présenter en quelques phrases le besoin, deux garanties du programme, deux limites et trois questions à poser avant son hébergement.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Suivre une action utilisateur et nommer chaque composant qui peut la bloquer.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Comparer les rubriques fonctionnalités, stockage, santé et authentification du contrat. Chercher ce qui relève du programme, puis ce qui dépendra de ton infrastructure.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Présenter le besoin utilisateur, les fonctions disponibles et deux limites réelles du logiciel sans confondre application et hébergement.
- Tracer une requête jusqu’à la donnée durable ; distinguer code fourni, paramètres, secrets et données.
- Poser les questions techniques qui restent ouvertes ; aucun test d’infrastructure n’est nécessaire à cette première lecture.
- Expliquer comment un ticket identifié, son titre, son état et sa relecture dans PostgreSQL seront contrôlés plus tard, sans inventer de sortie ou de capture.

**Contre-exemple de lecture, sans exécution :** une capture de page tickets ne démontre pas leur persistance. Indiquer quel contrôle ultérieur pourrait réfuter cette conclusion ; aucune sortie ni preuve technique n’est à produire aujourd’hui.

**Erreurs fréquentes :** Confondre le laboratoire historique avec l’architecture retenue pour le projet.

**Démarche en cas d’écart :** Si deux documents semblent décrire des capacités différentes, comparer leur version et la source du contrat. Distinguer une ancienne preuve historique d’une fonction actuelle ; noter la contradiction au lieu d’inventer un résultat.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Déplacer le même besoin vers une autre machine : qu’est-ce qui reste dans le contrat ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-01--comprendre-lapplication) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[Retour au parcours](README.md) · [Exercice suivant →](02-architecture.md)
