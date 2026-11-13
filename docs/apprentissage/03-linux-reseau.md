# 03 — Préparer Linux et le réseau

**Projet : OpsDesk · Pilier : Construire · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Une VM joignable et identifiable évite d’installer un service au mauvais endroit. Le support doit distinguer un nom introuvable, un trajet absent, un port fermé et un droit refusé.

Sur ton laboratoire identifié, vérifie séparément nom, route, écoute et droits. Prépare un compte ordinaire et l’accès requis au service ; garde les protections actives.

**Livrable attendu :** Identité de cible, carte de flux, accès vérifiés et diagnostic d’un défaut borné. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Linux porte des processus, fichiers et services avec des droits. DNS résout un nom ; une route choisit un trajet ; un port écoute ; le pare-feu autorise un flux. Ces contrôles répondent à des questions différentes.

Le nom d’hôte décrit une identité ; DNS traduit un nom en adresse ; la table de routage choisit un chemin ; un processus écoute sur une adresse et un port ; le pare-feu filtre des flux. Un succès à une couche n’atteste pas la suivante. SSH ajoute la vérification de l’identité du serveur et de l’utilisateur distant.

Les permissions Linux déterminent quel utilisateur peut lire un fichier ou agir sur un service. SELinux et firewalld apportent des contrôles distincts : observer un refus précis permet de chercher la règle concernée. Les désactiver globalement masque le problème et augmente le périmètre exposé.

**Question :** une connexion par adresse IP réussit, mais le nom ne fonctionne pas. Quel contrôle de résolution permettrait de départager une mauvaise entrée locale et une réponse DNS inattendue ?

## Préparer la bonne cible

Architecture retenue, relue et justifiée à l’exercice 02 ; accès autorisé au PC et résultats du pré-check hôte. Vérifier la disponibilité officielle de Rocky Linux 10.2 et son média avant d’en planifier l’installation. Aucun outil de virtualisation ni VM n’est considéré prêt sans contrôle.

Le pré-check de l’hôte Fedora 45 se fait sur le PC personnel, pas dans WSL ni dans une VM. La première VM, `srv-admin`, est la seule créée à la main (les deux autres le sont depuis elle à l’exercice 04) : cette VM cible Rocky Linux 10.2 est préparée personnellement sous KVM/QEMU/libvirt uniquement après qualification du média et des prérequis. Identifier ensuite séparément l’hôte, la VM, son utilisateur, son réseau et son stockage. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Suivre les pré-checks du guide sur le PC Fedora réel ; conserver les versions, ressources et points non vérifiés avant toute installation.
2. Préparer personnellement `srv-admin`, la première VM, après validation du média, puis relier son accès à l’hôte et noter ce qu’il faudra copier hors de la VM ; relever hôte, invité, utilisateur, adresse, routes, stockage et protections.
3. Vérifier séparément résolution, trajet, écoute, SSH et droits ; expliquer un refus attendu sans changer plusieurs couches ensemble.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Observer utilisateur, processus/service, résolution, trajet, écoute puis autorisation ; changer une chose après confirmation.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Comparer l’adresse obtenue pour le nom à l’adresse réellement portée par la VM. Une erreur d’authentification SSH suppose déjà qu’un serveur répond ; elle n’a pas le même sens qu’un délai de connexion.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Confirmer l’identité et la version de l’hôte puis de l’invité ; relever CPU, mémoire, disque et outils effectivement disponibles.
- Distinguer réseau prévu, route, résolution, écoute et autorisation : un résultat positif de l’un ne valide pas les autres.
- Vérifier SSH, utilisateur et permissions attendues ; relever les états de SELinux et firewalld sans les désactiver.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Test négatif sûr à proposer :** vérifier, sans modifier les droits, qu’un compte ordinaire ne peut pas écrire dans un emplacement système qui doit rester protégé. Justifier le refus attendu ; ne pas écrire ni effacer un fichier système.

**Erreurs fréquentes :** Désactiver SELinux/le pare-feu en bloc ; utiliser root partout ; diagnostiquer une route avec un test DNS seulement.

**Démarche en cas d’écart :** Si SSH échoue, distinguer route ou nom incorrect, absence d’écoute et refus d’authentification. Contrôler successivement identité, trajet, écoute puis droits ; un accès par IP mais pas par nom oriente vers la résolution, sans la prouver à lui seul.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Comment montrer qu’un refus vient des droits et non du réseau ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-03--préparer-linux-et-le-réseau) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](02-architecture.md) · [Retour au parcours](README.md) · [Exercice suivant →](04-terraform.md)
