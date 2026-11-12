# Cinq évaluations personnelles

Toutes restent NON EXÉCUTÉES ; niveau NON ÉVALUÉ. Aucune preuve personnelle n’est renseignée. Les essais historiques sont historiques et séparés.

Ces évaluations sont transversales : elles ne constituent pas cinq exercices supplémentaires ni un second ordre de travail. Les exercices 01/02 restent sans VM ; les contrôles métier sur service déployé sont différés tant que leur cible n’est pas personnellement disponible. Renseigner alors NON EXÉCUTÉ pour cette partie, sans déclarer toute l’évaluation reçue. L’exercice 13 fournit un cas nouveau pour examiner les responsabilités et l’autonomie ; consulter les [règles de preuve et de niveau](README.md#preuve-et-progression-personnelles).


<a id="evaluation-1"></a>

<a id="evaluation-1"></a>

## Évaluation 1 — Construire

**Objectif/scénario :** démontrer construire pour des demandes IT créées, consultables et suivies sans perdre les tickets, à partir des exercices 1, 2, 3 et d’une variante nouvelle.

**Environnement/pré-check :** cible personnelle identifiée, version, accès, ressources, données fictives, état initial et retour ; aucun incident destructif sans accord ciblé.

**Action personnelle :** L’apprenant propose la méthode, écrit les configurations nécessaires, exécute et explique. Niveau d’aide initial : guidé.

**Contrôle :** Expliquer le besoin et justifier l’architecture retenue ; distinguer Fedora hôte et Rocky invité. Vérifier réseau/SSH/droits/protections sur la VM réelle, puis expliquer un refus attendu. La présence d’un dessin ou le démarrage d’une VM ne suffit pas. Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL.

**Résultat/preuve/niveau :** NON EXÉCUTÉ / aucune preuve personnelle / NON ÉVALUÉ. Après exécution : date, environnement, version/commit, action, résultat, difficulté, correction, test final, aide reçue.

**Correction/consolidation :** à définir sur la tentative réelle. Une réussite avec assistance est distincte d’une autonomie sur un cas nouveau.


<a id="evaluation-2"></a>

<a id="evaluation-2"></a>

## Évaluation 2 — Automatiser

**Objectif/scénario :** démontrer automatiser pour des demandes IT créées, consultables et suivies sans perdre les tickets, à partir des exercices 4, 5 et d’une variante nouvelle.

**Environnement/pré-check :** cible personnelle identifiée, version, accès, ressources, données fictives, état initial et retour ; aucun incident destructif sans accord ciblé.

**Action personnelle :** L’apprenant propose la méthode, écrit les configurations nécessaires, exécute et explique. Niveau d’aide initial : guidé.

**Contrôle :** Relier chaque objet Terraform à une ressource réellement gérée et à son state protégé ; expliquer le plan puis le résultat observé. Montrer une configuration Ansible sur la bonne VM, la seconde passe interprétée et le paramètre ou service effectivement conforme. Un contrat local terraform_data ou changed=0 seul ne valide pas l’automatisation. Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL.

**Résultat/preuve/niveau :** NON EXÉCUTÉ / aucune preuve personnelle / NON ÉVALUÉ. Après exécution : date, environnement, version/commit, action, résultat, difficulté, correction, test final, aide reçue.

**Correction/consolidation :** à définir sur la tentative réelle. Une réussite avec assistance est distincte d’une autonomie sur un cas nouveau.


<a id="evaluation-3"></a>

<a id="evaluation-3"></a>

## Évaluation 3 — Faciliter la livraison

**Objectif/scénario :** démontrer faciliter la livraison pour des demandes IT créées, consultables et suivies sans perdre les tickets, à partir des exercices 6, 7, 8 et d’une variante nouvelle.

**Environnement/pré-check :** cible personnelle identifiée, version, accès, ressources, données fictives, état initial et retour ; aucun incident destructif sans accord ciblé.

**Action personnelle :** L’apprenant propose la méthode, écrit les configurations nécessaires, exécute et explique. Niveau d’aide initial : guidé.

**Contrôle :** Relier commit, tests, run et artefact identifiable ; expliquer permissions et accès à la cible. Promouvoir le même artefact sans reconstruction cachée, contrôler la version servie et les données, puis démontrer un retour borné compatible avec le schéma. Un fichier CI présent ou un job textuel de succès ne prouve pas une livraison. Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL. GHCR et Trivy font partie des contrôles à préparer, sans publier automatiquement une image ou un dépôt.

**Résultat/preuve/niveau :** NON EXÉCUTÉ / aucune preuve personnelle / NON ÉVALUÉ. Après exécution : date, environnement, version/commit, action, résultat, difficulté, correction, test final, aide reçue.

**Correction/consolidation :** à définir sur la tentative réelle. Une réussite avec assistance est distincte d’une autonomie sur un cas nouveau.


<a id="evaluation-4"></a>

<a id="evaluation-4"></a>

## Évaluation 4 — Observer/diagnostiquer

**Objectif/scénario :** démontrer observer/diagnostiquer pour des demandes IT créées, consultables et suivies sans perdre les tickets, à partir des exercices 9, 12 et d’une variante nouvelle.

**Environnement/pré-check :** cible personnelle identifiée, version, accès, ressources, données fictives, état initial et retour ; aucun incident destructif sans accord ciblé.

**Action personnelle :** L’apprenant propose la méthode, écrit les configurations nécessaires, exécute et explique. Niveau d’aide initial : guidé.

**Contrôle :** Justifier un signal métier, montrer collecte/visualisation et règle avec destinataire autorisé ; distinguer défaut de collecte et défaut du service. Pour un symptôme borné, formuler deux hypothèses, exécuter un contrôle discriminant puis corréler métriques, journaux et résultat utilisateur. Aucune panne destructive n’est requise. Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL.

**Résultat/preuve/niveau :** NON EXÉCUTÉ / aucune preuve personnelle / NON ÉVALUÉ. Après exécution : date, environnement, version/commit, action, résultat, difficulté, correction, test final, aide reçue.

**Correction/consolidation :** à définir sur la tentative réelle. Une réussite avec assistance est distincte d’une autonomie sur un cas nouveau.


<a id="evaluation-5"></a>

<a id="evaluation-5"></a>

## Évaluation 5 — Maintenir/rétablir

**Objectif/scénario :** démontrer maintenir/rétablir pour des demandes IT créées, consultables et suivies sans perdre les tickets, à partir des exercices 10, 11 et d’une variante nouvelle.

**Environnement/pré-check :** cible personnelle identifiée, version, accès, ressources, données fictives, état initial et retour ; aucun incident destructif sans accord ciblé.

**Action personnelle :** L’apprenant propose la méthode, écrit les configurations nécessaires, exécute et explique. Niveau d’aide initial : guidé.

**Contrôle :** Préparer une maintenance limitée avec état initial, compatibilité et retour. Contrôler une archive cohérente puis restaurer sur une cible distincte ; retrouver les mêmes références métier et expliquer les mesures de perte/durée. Un backup créé, un conteneur redémarré ou un disque virtuel sur le même PC ne prouve pas à lui seul une reprise utile ou hors site. Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL.

**Résultat/preuve/niveau :** NON EXÉCUTÉ / aucune preuve personnelle / NON ÉVALUÉ. Après exécution : date, environnement, version/commit, action, résultat, difficulté, correction, test final, aide reçue.

**Correction/consolidation :** à définir sur la tentative réelle. Une réussite avec assistance est distincte d’une autonomie sur un cas nouveau.

[Retour au parcours](README.md) · [Épreuve nouvelle d’autonomie](13-autonomie.md) · [Repères après tentative](corriges.md)

Révision documentaire : 2026-11-04.
