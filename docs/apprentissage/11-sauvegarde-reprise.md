# 11 — Sauvegarder et restaurer

**Projet : OpsDesk · Pilier : Maintenir/rétablir · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

L’équipe doit retrouver les tickets après une perte ou une erreur. Créer une archive n’apporte cette garantie que si sa restauration indépendante rend les mêmes références métier accessibles.

Définis ce qui doit être retrouvé pour un ticket témoin, puis écris et pratique ta sauvegarde/restauration sur une cible distincte. Le script historique reste un corrigé après tentative.

**Livrable attendu :** Intégrité contrôlée, mêmes références métier et mesures expliquées ; source préservée et limites explicites. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Une sauvegarde doit permettre une restauration utile. Un dump, ses médias, la configuration nécessaire et les identités doivent être cohérents. Âge de capture, perte réellement observée et durée de reprise sont des mesures distinctes.

Une **sauvegarde** conserve une copie récupérable selon une stratégie ; une **restauration** remet ses données sur une cible et vérifie leur utilité. Un **snapshot** capture un état selon le mécanisme de stockage et peut dépendre du support d’origine : il n’est pas automatiquement une copie indépendante et cohérente de PostgreSQL. Un **rollback d’image** change le programme ; une **reconstruction** recrée l’environnement à partir de sources et paramètres identifiés. Ces mécanismes peuvent se compléter, mais ne prouvent pas la même chose.

Pour le service actuel, les données métier sont dans PostgreSQL ; configuration et secrets nécessaires doivent pouvoir être reconstitués de façon sûre. OpsDesk ne gère pas de pièces jointes ni de médias utilisateur : ne pas inventer un jeu de fichiers à sauvegarder. Si un futur périmètre en ajoute, sa cohérence devra être traitée explicitement.

Le **RPO** est l’objectif de perte de données admissible exprimée dans le temps ; le **RTO** est l’objectif de délai de reprise. Pour les comparer à l’observé, dater le point de capture, les écritures témoins et le début/fin du scénario. Retrouver un ticket connu prouve une référence ; cela ne mesure pas toutes les écritures perdues. Définir les bornes et rapporter les mesures réelles sans inventer de panne : une reprise d’exercice chronométrée reste différente d’une panne physique.

**Question :** une archive est valide mais sa clé n’est disponible que sur la machine supposée perdue. Quelle dépendance empêche la reprise ? Une seconde VM sur le même disque protège-t-elle d’une panne du PC ?

Référence : [sauvegarde logique et restauration PostgreSQL](https://www.postgresql.org/docs/current/backup-dump.html). Vérifier versions serveur/outils, contenu et droits avant de rédiger ta procédure ; aucun dump ni restore n’est lancé par cette fiche.

## Préparer la bonne cible

Données témoins connues et état métier vérifié, source identifiée, destination distincte et clé privée disponibles selon la stratégie proposée. Vérifier l’espace et les droits avant l’archivage, puis les prérequis de reconstruction avant la reprise.

Sauvegarde : `pg_dump` au format custom sur `srv-app`, copie par `rsync` hors de la VM. Reprise : `srv-admin` refait `srv-app`, `pg_restore` remet la base, puis `/health/ready` et un ticket témoin sont contrôlés. Distinguer trois pertes : une VM applicative, `srv-admin` (état Terraform et clés SSH, à copier hors de la VM) et le PC lui-même. Identifier la VM source et une cible de reprise distincte, créée seulement lorsqu’elle est utile et selon les ressources vérifiées du PC Fedora 45/KVM. Ne pas restaurer sur la source. Relever version applicative, base, médias éventuels, configuration privée, emplacement d’archive et clés nécessaires. Un second disque virtuel, ou le dossier `~/sauvegardes` de l’hôte, est sur le même PC : ce n’est pas une sauvegarde hors site. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Identifier les références métier, versions, configuration et secrets nécessaires ; proposer cohérence, destination indépendante, chiffrement, disponibilité des clés et rétention.
2. Écrire tes précontrôles d’espace, droits, intégrité et compatibilité ; nommer sans ambiguïté source, archive et destination de reprise. Définir les bornes RPO/RTO et critères d’arrêt.
3. Après préparation et autorisation, restaurer personnellement sur une cible isolée distincte, sans effacer la source ; relire les mêmes tickets et expliquer perte observée, durée et limites.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Identifier version, archive, clé, espace, accès, ordre DB/médias et référence attendue ; arrêter sur cible ou archive ambiguë.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Avant d’accuser l’archive, comparer point de capture, version, rôle SQL, base cible et référence du ticket. L’intégrité d’un fichier ne prouve pas que le service a relu les données restaurées.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Vérifier que l’archive, ses versions, ses données et sa clé permettent la reconstruction ; contrôler intégrité et cohérence, sans écraser une archive existante.
- Restaurer sur une cible distincte et vérifier l’accès au service ainsi que les mêmes références métier ; une archive créée n’est pas une preuve de reprise.
- Mesurer les bornes de capture, la perte de données et la durée de retour utiles ; distinguer RPO/RTO visés et réellement observés.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Contrôle négatif sûr :** sur les métadonnées d’une copie de l’archive, détecter une version ou une destination incompatible et s’arrêter avant restauration. Ne pas corrompre l’unique archive, supprimer la source ou provoquer une perte pour mesurer la reprise.

**Erreurs fréquentes :** Stocker clé et archive au même endroit en parlant de hors-site ; oublier la configuration et les accès nécessaires ; prétendre une cohérence sous écritures continues non testée.

**Démarche en cas d’écart :** Si le service restauré démarre mais qu’un ticket manque, départager mauvais point de capture, mauvaise base cible et données incomplètes. Comparer référence, version et intégrité sur la cible de reprise ; conserver la source et la dernière archive connue.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Quelle preuve démontrerait une reprise utile après perte de la machine plutôt qu’un simple remplacement de conteneur ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-11--sauvegarder-et-restaurer) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](10-maintenance.md) · [Retour au parcours](README.md) · [Exercice suivant →](12-diagnostic.md)
