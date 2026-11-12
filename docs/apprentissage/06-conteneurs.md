# 06 — Conteneuriser

**Projet : OpsDesk · Pilier : Faciliter la livraison · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Le même programme doit pouvoir être livré avec ses dépendances tout en conservant les tickets. Conteneuriser permet de séparer l’artefact applicatif, sa configuration d’exécution et les données durables.

Conteneurise le programme fourni ; montre quelle version répond et relis un ticket après le remplacement applicatif prévu, avec stockage conservé.

**Livrable attendu :** Recette personnelle, image identifiable, configuration privée et parcours métier vérifié. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Une image fige le programme et ses dépendances ; un conteneur est un processus qui l’utilise. Réseau, volumes, paramètres et secrets déterminent son fonctionnement. L’image n’est pas une sauvegarde de la base.

L’image contient le programme et ses dépendances ; un conteneur en est une exécution avec ses propres paramètres. Un **tag** est un nom qui peut pointer vers un autre contenu ; le **digest** identifie le contenu de l’image. Un port écouté dans le conteneur n’est pas automatiquement accessible sur la VM ou le PC.

Le volume conserve des données en dehors du cycle de vie du processus. Il doit être relié au bon service et posséder des droits adaptés ; sa simple existence ne prouve pas qu’il contient la bonne base. Les secrets sont fournis à l’exécution et restent hors de l’image, du dépôt et des journaux. Refaire l’image ne restaure pas PostgreSQL.

**Question :** si l’application change mais pas le volume PostgreSQL, quelles identités et quel ticket permettront de vérifier la livraison et la persistance séparément ?

## Préparer la bonne cible

Contrat applicatif compris, VM et accès qualifiés ; stratégie de stockage et de secrets proposée. Vérifier la compatibilité et la disponibilité du moteur choisi avant son installation. Aucun Dockerfile ou Compose historique n’est obligatoire.

Le poste de contrôle prévu est Fedora 45. Le moteur de conteneurs est préparé personnellement dans la VM Rocky Linux 10.2 qualifiée ; ne pas confondre un moteur Windows/WSL historique avec celui de la VM. Relever moteur, version, utilisateur, chemins persistants et ports réellement choisis. La recette du conteneur est à écrire à partir du contrat applicatif. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Le moteur étudié dans ce projet est Docker dans la VM ; vérifier sa version et son accès avant de proposer Dockerfile/Compose. Le service sans authentification reste un démonstrateur privé de laboratoire.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. À partir du contrat, lister sources nécessaires au build, commande d’exécution, dépendances, variables, secrets et données à exclure de l’image.
2. Écrire personnellement ta recette et ta configuration d’exécution ; nommer les réseaux, ports et stockages avec leur cible réelle.
3. Construire puis identifier ton image ; contrôler l’application et une donnée témoin. Préparer un remplacement applicatif borné en conservant les données et les moyens de retour.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Séparer erreur de build, commande de lancement, droits, DNS, connexion DB et schéma ; regarder le premier message utile.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Pour un échec de démarrage, séparer build et runtime, puis lire commande, paramètres et premier message utile. Pour une connexion DB refusée, comparer nom/adresse, écoute et droits avant de toucher au stockage.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Relier code/commit, version de l’application et image réellement exécutée ; distinguer tag et digest.
- Vérifier séparément écoute, disponibilité des dépendances, paramètres privés et parcours utilisateur.
- Contrôler la donnée témoin après le remplacement applicatif prévu, avec stockage préservé et sans supprimer un volume existant.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Test négatif borné à préparer :** faire refuser une entrée métier invalide sur les données fictives de la cible autorisée, puis vérifier qu’aucun ticket invalide n’a été ajouté. Un test qui efface un volume n’est pas nécessaire.

**Erreurs fréquentes :** Inclure secrets/données dans l’image ; utiliser latest sans identité ; croire qu’un conteneur démarré prouve le métier.

**Démarche en cas d’écart :** Si le conteneur est vivant mais le service inutilisable, distinguer port non écouté, dépendance non prête et mauvais paramètre. Lire les journaux du seul composant concerné et tester le chemin de dépendance ; ne pas supprimer les données pour obtenir un redémarrage propre.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

**Réutilisation :** Comment donner au développeur un test reproductible sans lui donner les droits administrateur de l’hôte ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-06--conteneuriser) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](05-ansible.md) · [Retour au parcours](README.md) · [Exercice suivant →](07-k3s.md)
