# Parcours personnel OpsDesk — V4.4

**Codex fournit l’application et les tests ; Mathias construit et exploite son infrastructure.** Accompagnement guidé. Le cadre technique commun reste Linux/Rocky, réseau, Terraform, Ansible, conteneurs, K3s adapté, CI/CD, supervision, sécurité, Day-2 et reprise. Aucun exercice n’est déclaré exécuté et aucun niveau personnel n’est renseigné.

Commencer par [l’exercice 01](01-application.md) et [le contrat applicatif](../contrat-applicatif.md), puis suivre cet ordre. Les anciennes configurations InfraOps Codex sont des références historiques à examiner après sa propre tentative lorsqu’elles sont accessibles : leur disponibilité hors du dépôt courant reste NON VÉRIFIÉE.

## Laboratoire et plateforme de travail

L’hôte prévu est **Fedora 45**, avec KVM/QEMU et libvirt ; le système invité cible est **Rocky Linux 10.2**. Cette cible reste prévue tant que les pré-checks et compatibilités exactes du [guide de laboratoire](../laboratoire-fedora-kvm-rocky.md) ne sont pas vérifiés. Les outils de contrôle Terraform/Ansible sont distingués des services exécutés dans la VM. Les exercices 01 et 02 ne demandent ni VM ni installation. Les ressources restent à dimensionner d’après les mesures du PC, sans multiplier les VM.

**GitHub est l’unique plateforme active du projet.** GitLab reste en l’état ; ses références historiques sont facultatives. Aucune synchronisation ni double gestion quotidienne n’est demandée. AWS et les variantes cloud restent des objectifs distincts à justifier et à autoriser, pas un prérequis du laboratoire local.

Docker, GitHub Actions/GHCR et Trivy sont reliés aux exercices 06/08 ; Prometheus/Grafana et un test k6 borné à l’exercice 09. Les outils sont à vérifier, préparer et pratiquer personnellement.

| Ordre | Exercice | Responsabilité |
|---|---|---|
| 01 | [01 — Comprendre l’application](01-application.md) | Construire |
| 02 | [02 — Concevoir l’architecture](02-architecture.md) | Construire |
| 03 | [03 — Préparer Linux et le réseau](03-linux-reseau.md) | Construire |
| 04 | [04 — Provisionner avec Terraform](04-terraform.md) | Automatiser |
| 05 | [05 — Configurer avec Ansible](05-ansible.md) | Automatiser |
| 06 | [06 — Conteneuriser](06-conteneurs.md) | Faciliter la livraison |
| 07 | [07 — Orchestrer avec Kubernetes/K3s](07-k3s.md) | Faciliter la livraison |
| 08 | [08 — Construire la CI/CD](08-cicd.md) | Faciliter la livraison |
| 09 | [09 — Superviser](09-supervision.md) | Observer/diagnostiquer |
| 10 | [10 — Exploiter et maintenir](10-maintenance.md) | Maintenir/rétablir |
| 11 | [11 — Sauvegarder et restaurer](11-sauvegarde-reprise.md) | Maintenir/rétablir |
| 12 | [12 — Diagnostiquer et rétablir](12-diagnostic.md) | Observer/diagnostiquer |
| 13 | [13 — Démontrer son autonomie](13-autonomie.md) | Transverse |

Les [corrigés](corriges.md) sont séparés de la première lecture. Les [cinq évaluations](evaluations.md) mobilisent les acquis ; l’exercice 13 demande une tâche nouvelle. Les opérations sensibles exigent cible, pré-check et accord adapté. Le CV ne se modifie pas automatiquement.

<a id="cadre-commun-des-exercices"></a>

## Cadre commun des exercices

Les fiches regroupent l’ancienne trame de 18 rubriques en sept temps de lecture. Les principes communs sont expliqués une fois ici ; les besoins, notions, consignes, critères, erreurs et situations de diagnostic restent propres à chaque exercice. Un schéma de lecture n’impose pas de restaurer une base pendant un exercice d’architecture.

Le besoin métier commun est de créer, retrouver et faire avancer des tickets IT fictifs. Un ticket identifié, son titre et son état doivent rester contrôlables. Le contrat décrit ce que le programme exige et garantit ; il ne choisit pas une infrastructure à recopier. Codex fournit le programme et les tests ; Mathias propose ses choix, écrit ses configurations, exécute ses contrôles et explique ses résultats.

L’application ne possède pas d’authentification utilisateur : laboratoire local, données fictives et absence d’exposition Internet restent des contraintes. La protection CSRF ne constitue pas un compte utilisateur. PostgreSQL doit conserver les données ; santé du processus, disponibilité de la base, identité de version et parcours métier se vérifient séparément. Les 26 tests applicatifs historiques Codex ne prouvent ni ton laboratoire ni ta sécurité globale ; le triage historique reste FAIL dans son contexte.

Les **13 exercices V4.4** donnent l’ordre personnel. Les **16 modules historiques** sont des ressources théoriques, accessibles depuis le [parcours Notion](https://app.notion.com/p/3fc65721fa1881f7b4d2f248aafeed23), sans second ordre obligatoire. Les **trois phases** racontent l’évolution d’un seul service dans un seul dépôt. Les **cinq évaluations** vérifient les responsabilités de façon transversale, séparément du statut des exercices. OpsDesk, BankFlow et LogiTrack restent trois projets indépendants : aide guidée ici, puis aide progressivement réduite dans les autres parcours, sans les modifier pendant cette mission.

<a id="avant-une-action"></a>

### Avant une action

Pour 01/02, préparer uniquement lecture, questions et dessin : ni VM, ni service, ni installation. À partir de 03, commencer par le [guide de laboratoire et ses pré-checks](../laboratoire-fedora-kvm-rocky.md). Aucune compatibilité exacte, ressource matérielle ou installation n’est présumée reçue.

Avant une commande personnelle, noter son besoin, la machine visée (hôte, VM, conteneur ou runner), l’utilisateur, le répertoire de lancement, les versions, les prérequis et l’état initial. Identifier paramètres à choisir, droits, effet, fichiers ou ressources touchés, résultat attendu et contrôle. Prévoir où lire les erreurs, quelle observation ferait arrêter et quel retour est possible. Distinguer explication conceptuelle et bloc réellement prêt à copier ; un nom de commande dans une leçon n’est pas une procédure exécutable.

Une action sur un cloud payant, une exposition Internet, un réseau sensible, un incident provoqué ou une suppression exige l’accord ciblé prévu. Ne pas supprimer une VM, un volume, un state ou l’unique archive pour fabriquer une preuve. Préférer un constat en lecture seule et une copie de laboratoire ; garder les protections actives. Les anciens guides de commandes sont historiques quand leurs fichiers requis sont absents.

<a id="verifier-et-diagnostiquer"></a>

### Vérifier et diagnostiquer

Écrire l’attendu avant d’observer le résultat réel. Distinguer contrôle de syntaxe, contrôle d’identité de cible, état technique et effet utilisateur. Prévoir un contrôle positif et un refus attendu sûr, proportionnés au sujet ; un exercice de lecture peut utiliser un contre-exemple documentaire. Le contrôle métier sur un ticket est différé et marqué NON EXÉCUTÉ tant que le service n’est pas disponible dans le périmètre personnel.

En cas d’écart, garder le fil : **symptôme → observation → hypothèses → test discriminant → cause confirmée ou inconnue → correction justifiée → validation finale**. Noter le premier fait utile, les versions et l’heure ; conserver les messages expurgés. Changer un seul point justifié puis recontrôler le besoin. Un exemple fictif ou un PASS Codex ne remplace pas une observation personnelle.

L’aide se demande au niveau utile : indice 1 pour orienter l’observation ; indice 2 pour expliquer le mécanisme ; indice 3 après présentation de la tentative pour analyser le point bloquant. Les volets restent fermés à la première lecture. Une explication de syntaxe ou un extrait fictif minimal est recevable ; la conception et les fichiers finaux restent personnels. Une difficulté normale appelle une prochaine action, pas un verdict définitif.

<a id="preuve-et-progression-personnelles"></a>

### Preuve et progression personnelles

Conserver la première tentative, puis le livrable et le contrôle final. Pour chaque preuve réellement obtenue, renseigner date, cible/environnement, version ou commit, méthode/action personnelle, attendu/observé, résultat, difficulté, hypothèses, correction, test final, limites et aide reçue. Retirer secrets, cookies, jetons, données privées et state. Un lien de suivi indique où travailler ; il ne valide pas le travail.

Utiliser la base [Suivi des réalisations — OpsDesk](https://app.notion.com/p/f6cbd99a06334863a17a0b53521b813d) : une entrée par exercice, les évaluations distinctes, l’historique conservé. Une tâche créée reste À faire sans date de vérification, preuve, résultat ou niveau anticipé. Renseigner les observations après la séance réelle.

**PRÉVU**, **EN COURS**, **IMPLÉMENTÉ/RÉALISÉ**, **EXÉCUTÉ** et **VÉRIFIÉ** décrivent des états distincts. Un état VÉRIFIÉ exige une méthode, une version/référence, une cible, une date et un résultat traçables. Pour un contrôle : **PASS**, **FAIL**, **PARTIEL**, **NON EXÉCUTÉ**. Utiliser **NON VÉRIFIÉ** lorsque la portée du contrôle n’est pas établie.

**L0** = découverte ; **L1** = compréhension ; **L2** = réalisation personnelle ; **L3** = autonomie vérifiée sur une adaptation ou un diagnostic nouveau avec aide limitée. Le résultat technique, la compréhension, le diagnostic et l’explication se vérifient séparément. Un exercice terminé avec assistance peut relever de L2 ; il n’attribue pas automatiquement L3. Aucun niveau, acquis CV ou résultat personnel n’est prérempli par la documentation.

### Conservation des 18 exigences

| Ancienne rubrique | Emplacement après regroupement |
|---|---|
| 1. Situation professionnelle | Situation et résultat à obtenir, propre à la fiche |
| 2. Objectif pédagogique | Titre, résultat observable, consignes et questions ; responsabilité en tête de fiche |
| 3. Besoin applicatif | Besoin commun ci-dessus, appliqué à la situation de chaque fiche |
| 4. Concepts à comprendre | Comprendre avant de choisir, notions et cas propres à la fiche |
| 5. Prérequis | Préparer la bonne cible |
| 6. Environnement et matériel | Préparer la bonne cible et guide de laboratoire référencé |
| 7. Travail personnel | Réaliser soi-même, avec micro-jalons et décisions propres au sujet |
| 8. Contraintes | Cadre commun et Avant une action ; limites spécifiques dans la fiche |
| 9. Indices progressifs | Trois volets distincts de la fiche, du moins direct au plus ciblé |
| 10. Vérifications à effectuer | Vérifier, puis diagnostiquer, critères propres conservés |
| 11. Résultat attendu | Livrable annoncé dès la situation |
| 12. Erreurs fréquentes | Erreurs propres dans Vérifier, puis diagnostiquer |
| 13. Démarche de diagnostic | Cas propre à la fiche et fil commun ci-dessus |
| 14. Preuves à conserver | Livrable propre, Expliquer et capitaliser, métadonnées communes |
| 15. Synthèse | Expliquer besoin, choix, contrôle et limites |
| 16. Réutilisation des acquis | Question de réutilisation propre à chaque fiche |
| 17. Validation et autonomie | Critères propres et niveaux communs ci-dessus ; cinq évaluations séparées |
| 18. Corrigé séparé | Corrigé après tentative, lien propre à chaque exercice |

Révision documentaire : 2026-11-04. Contrôles de cette réorganisation : structure et cohérence documentaires ; aucune réalisation InfraOps personnelle, aucun test utilisateur réel ni rendu Notion/mobile n’est établi par cette fiche.
