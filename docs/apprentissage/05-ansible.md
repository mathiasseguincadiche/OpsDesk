# 05 — Configurer avec Ansible

**Projet : OpsDesk · Pilier : Automatiser · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Une VM créée doit recevoir un état cohérent et vérifiable. Automatiser sa configuration permet de répéter la préparation et d’identifier ce qui change réellement, au lieu de rejouer des commandes sans contrôle.

Configure la cible choisie, rejoue le playbook et explique une tâche non convergente. Un rendu JSON localhost historique ne remplit pas cette évaluation.

**Livrable attendu :** Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Ansible applique des tâches à un inventaire. Un module convergent décrit un état ; l’idempotence se vérifie par une seconde passe et par l’état effectif, pas par un commentaire.

L’**inventaire** associe des noms aux machines et à leurs paramètres de connexion. Le contrôleur Ansible rejoint la VM par **SSH** ; la plupart des modules usuels y nécessitent un Python compatible. Un **module** exprime une opération et son résultat ; un playbook organise les tâches. L’élévation `become` donne les droits requis à certaines tâches : elle ne remplace pas le choix d’un compte distant ordinaire.

Un résultat `changed` signifie que la tâche déclare avoir modifié l’état, selon la logique du module. Un **handler** est une tâche déclenchée par notification après un changement, par exemple pour prendre en compte une configuration ; il ne doit pas provoquer un redémarrage à chaque passe sans besoin. La seconde passe aide à vérifier la convergence. Même `changed=0` peut accompagner un mauvais service, une mauvaise cible ou un contrôle incomplet : observer l’état obtenu et son effet utile reste nécessaire.

**Question :** une première passe copie un fichier et notifie un handler ; la seconde ne change rien. Quelles observations prouvent que le bon fichier a été pris en compte par le bon service sur la bonne VM ?

Référence : [handlers Ansible](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_handlers.html). Les prérequis des modules choisis se lisent dans leur documentation de version.

## Préparer la bonne cible

Cible VM et propriétaire de ressources identifiés aux exercices 03/04 ; accès SSH vérifié avec le compte ordinaire prévu. Vérifier la version d’Ansible sur le contrôleur et les prérequis Python des modules sur l’invité. Ne pas supposer un inventaire correct parce qu’un nom répond au ping ICMP.

Ansible est piloté depuis le poste Fedora 45 vers la VM Rocky Linux 10.2 identifiée. Vérifier inventaire, résolution, SSH, utilisateur distant, Python requis par les modules et élévation ciblée avant une tâche mutatrice. Les paquets, services et protections sont ceux de la VM cible, pas ceux du poste de contrôle. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Construire ton inventaire et prouver l’identité SSH/Python de la cible avant toute tâche mutatrice ; préciser quelles tâches exigent become.
2. Écrire une configuration limitée avec les modules adaptés, des variables séparées et un handler seulement si nécessaire ; prévoir le contrôle indépendant de l’état voulu.
3. Comparer les deux passes, examiner chaque changement restant et contrôler le service ou paramètre. Ne pas masquer une divergence par un résultat changed artificiellement forcé.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Lire le premier hôte/tâche/code en défaut ; vérifier accès, chemin, variable, module et privilège avant correction ciblée.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Lire le nom d’hôte et la première tâche en échec. Distinguer connexion SSH, interpréteur distant, privilège et état du service ; pour une divergence, examiner la condition réelle du module et la notification du handler.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Vérifier l’inventaire et l’identité SSH réelle de la VM avant les changements ; un test Ansible de connexion vérifie aussi son prérequis Python.
- Comparer première et seconde passes ; expliquer chaque changement restant sans masquer un échec avec une condition arbitraire.
- Contrôler le paramètre ou service réellement configuré et son effet utile ; changed=0 seul ne démontre pas le fonctionnement.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Cas de lecture fictif :** une passe finit avec `changed=0`, mais la VM visée dans l’inventaire n’est pas celle du schéma. Quel contrôle d’identité invalide la conclusion ? Un refus de privilège prévu se teste seulement sur une tâche de lecture adaptée, sans modifier un service.

**Erreurs fréquentes :** Utiliser shell pour chaque action ; confondre changed=0 avec service fonctionnel ; laisser une variable sensible dans un log.

**Démarche en cas d’écart :** Si Ansible échoue, distinguer accès SSH, Python distant et élévation. Si une seconde passe change encore, lire la tâche concernée et son état attendu ; corriger la cause puis vérifier le service, sans rendre silencieusement la tâche inconditionnelle.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Quelle partie de ta configuration peut être réutilisée sans copier les secrets ni les adresses ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-05--configurer-avec-ansible) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](04-terraform.md) · [Retour au parcours](README.md) · [Exercice suivant →](06-conteneurs.md)
