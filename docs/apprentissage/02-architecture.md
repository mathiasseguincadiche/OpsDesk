# 02 — Relire, justifier et vérifier l’architecture retenue

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-12. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

L’équipe veut un service compréhensible et reconstructible sur le PC disponible. L’architecture a été arrêtée avant toute réalisation, pour que les choix techniques ne ralentissent pas l’apprentissage : trois serveurs Rocky Linux sur un réseau privé (un d’administration, un pour l’application, un pour K3s), Podman, une sauvegarde copiée hors du serveur, K3s et la supervision. Elle est décrite dans le [registre des décisions](../architecture.md#décisions-retenues) et sur le [schéma technique](../diagrams/architecture-technique.svg).

Relis cette architecture, puis justifie-la : pour chaque choix, quel besoin il couvre, quelle alternative a été écartée et ce qui se passe s’il tombe en panne. Vérifie ensuite qu’elle tient : chaque flux a une origine et une destination, chaque donnée durable a un emplacement, chaque port ouvert a une raison. Un choix que tu n’arrives pas à justifier est à signaler, pas à corriger en silence.

**Livrable attendu :** Une note personnelle qui reprend chaque décision (besoin couvert, alternative écartée, point de panne, contrôle prévu), les flux redessinés de mémoire puis comparés au schéma technique, et la liste des écarts ou des questions. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

L’architecture traduit un besoin en ressources, flux et frontières de confiance. Un dessin doit expliquer les accès et la persistance, pas seulement aligner des logos.

Un schéma de présentation répond « à quoi sert le service et qui l’utilise ? ». Un schéma technique répond « où s’exécute chaque composant, par quel flux et avec quels droits ? ». Les deux dessins ont des publics différents. Ils décrivent l’architecture retenue, pas son avancement : tout reste à réaliser et à vérifier.

Un composant doit résoudre un besoin : séparer les données du processus évite de les perdre quand on remplace l’application. Cela ne rend pas le disque disponible en cas de panne du PC. Comparer avec l’alternative écartée aide à expliquer le compromis coût, mémoire, maintenance et reprise, sans chercher une architecture de production. Si le registre ne donne pas la raison d’un choix, le dire plutôt que d’en inventer une.

**Question de conception :** si le disque hébergeant PostgreSQL devient indisponible, quel besoin n’est plus couvert ? Ajouter une seconde copie du processus Flask résout-il ce problème ?

## Préparer la bonne cible

Exercice 01 compris et besoins applicatifs reformulés. Lire le [registre des décisions](../architecture.md#décisions-retenues), le [schéma technique](../diagrams/architecture-technique.svg) et sa [notice de lecture](../diagrams/README.md) (routes, sondes, table `tickets`, ports). Relever les ressources réelles du PC ou les marquer NON VÉRIFIÉES : les trois serveurs retenus prennent 12 Go de mémoire à l’hôte.

Lecture, dessin et analyse à partir du contrat, sans création de ressource. L’hôte est Fedora 45 avec KVM/QEMU et libvirt, et le système invité Rocky Linux 10.2 ; disponibilité exacte, compatibilité et ressources restent à qualifier dans le guide de laboratoire.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Pour 01/02, la cible est le document ou le dessin : aucun terminal ni VM requis.

## Réaliser soi-même et demander un indice

1. Lire le registre et le schéma, puis retrouver pour chaque décision le besoin qu’elle couvre : fonctions, données durables, accès utilisateur et accès opérateur, en gardant les contraintes du contrat visibles.
2. Remplir un tableau personnel : décision, besoin couvert, alternative écartée, point de panne, façon de reconstruire, contrôle prévu plus tard. Comparer les tailles retenues aux ressources mesurées du PC ou signaler NON VÉRIFIÉ.
3. Redessiner de mémoire les flux d’une requête, d’une sonde, d’une sauvegarde et d’une restauration, avec sens, protocole, origine et destination, puis comparer au schéma technique. Source .drawio et export .svg distincts, sans Mermaid.

Conserver ta première version avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

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

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta note, tu la relis et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Associer chaque composant du schéma à un besoin du contrat ; identifier l’hôte, les trois serveurs (`srv-admin`, `srv-app`, `srv-k3s`), application et données.
- Expliquer le rôle de `srv-admin`, ce qui s’y trouve (outils, état Terraform, clés SSH) et ce qui se perd si elle disparaît.
- Expliquer les flux autorisés, les accès refusés et l’emplacement de chaque donnée durable : par exemple, qui peut atteindre le port 5432, et qui peut ouvrir une session SSH.
- Pour chaque alternative écartée, indiquer le coût en ressources, le point de panne et la méthode de reconstruction à vérifier ; si l’argument ne tient pas, le noter comme question ouverte.
- Les décisions du registre sont « retenu, non vérifié » : écrire pour chacune le contrôle qui la ferait passer à « vérifié ».
- Expliquer comment un ticket identifié, son titre, son état et sa relecture dans PostgreSQL seront contrôlés plus tard, sans inventer de sortie ou de capture.

**Revue contradictoire, sans création de ressource :** rechercher un flux sans destination, un stockage sans propriétaire, un point de panne sans méthode de reconstruction ou une exposition incompatible avec l’absence d’authentification. Signaler l’écart et expliquer la limite restante ; un changement d’architecture se propose avec sa raison avant d’être inscrit au registre.

**Erreurs fréquentes :** Assimiler namespace, réseau conteneur et isolation de machines ; oublier où vivent les données.

**Démarche en cas d’écart :** Si le schéma paraît répondre au besoin mais qu’un accès reste inexplicable, distinguer flux manquant, dépendance oubliée et document qui ne dit pas tout. Suivre une requête et demander où vit sa donnée durable avant de proposer un composant de plus.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Quel compromis changerait si la charge ou l’exigence de reprise augmentait ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-02) ou demander le niveau d’aide souhaité. L’architecture retenue est la référence ; ce qui s’évalue, c’est ta justification et ce que tu en as vérifié.

[← Exercice précédent](01-application.md) · [Retour au parcours](README.md) · [Exercice suivant →](03-linux-reseau.md)
