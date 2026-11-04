# Cinq évaluations OpsDesk — preuves techniques et autonomie

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

**Périmètre du 3 novembre 2026 : laboratoire local Ubuntu/WSL.** La chaîne InfraOps complète sur K3s reste partielle. Les essais exécutés par Codex sont des preuves du laboratoire ; ils n’attribuent pas à Mathias une exécution personnelle ou une maîtrise L3.

L0 = connu ; L1 = implémenté/contrôlé statiquement ; L2 = exécuté ; L3 = vérifié **et expliqué personnellement**. Aucun L3 n’est attribué ici. Le [registre JSON](../evidence/evaluations.json) reprend ces cinq évaluations pour la vue à quinze cellules du portfolio.

| Pilier | Verdict sur le besoin complet | Sous-preuve réelle | Manque bloquant |
|---|---|---|---|
| 1. Construire | PARTIEL | Compose, PostgreSQL, scénario HTTP et navigateur | VM cible et chemin K3s non qualifiés ; panne réseau non exécutée |
| 2. Automatiser | PARTIEL | Contrat Terraform et rendu Ansible répétés sans changement | Aucun provisioning/reconstruction ou configuration Rocky |
| 3. Faciliter la livraison | PARTIEL | Image et tests locaux ; workflow candidat | Publication/promotion/rollback et autonomie développeur en CI non démontrés |
| 4. Observer/diagnostiquer | PARTIEL | live/ready/version/metrics, refus HTTP attendus ; diagnostic d’un échec Ansible | Alerte réelle de service et incident de cluster non exécutés |
| 5. Maintenir/rétablir | NON EXÉCUTÉ dans ce registre | Procédure et critères décrits | Maintenance et restauration indépendante des tickets à prouver |

## 1. Construire : retrouver le ticket à travers les composants

**Pourquoi.** Le collaborateur doit pouvoir ouvrir puis retrouver sa demande ; l’équipe IT doit lire son état. La réception doit suivre l’utilisateur jusqu’aux données, pas seulement constater qu’un conteneur tourne.

**Code fourni / rôle InfraOps.** `app/opsdesk/` fournit les règles et pages du démonstrateur ; `compose.yaml`, `Dockerfile`, `db/001-initial.sql`, `scripts/prepare-local.sh` et `k8s/` définissent l’exécution, les droits et les dépendances. L’architecture sur [le schéma technique](diagrams/architecture-technique.svg) montre navigateur → port local → app → DNS `db` → PostgreSQL → volume.

**Pré-check.** Identifier le projet `v42opsdesk`, le port local 18081, le réseau et le volume ; vérifier ressources et absence d’accès public. Données fictives et secrets privés uniquement. La preuve initiale ne qualifie ni Fedora ni une VM Rocky. Ne pas employer le contexte Kubernetes existant.

**Exécution réelle.** `docker compose up --build --detach --wait`, puis `python3 scripts/smoke.py --base-url http://127.0.0.1:18081` ont exercé la cible Compose. Le [rapport du 2 novembre 22:06:49 UTC](../evidence/business-smoke.json) vérifie création/relecture/transitions et 400/404/409 attendus ; [Chrome/Playwright](../evidence/browser.json) a affiché la liste le 3 novembre 03:41:03 UTC. `kubectl kustomize k8s` a seulement [rendu les objets hors ligne](../evidence/k8s-static.json).

**Attendu / observé.** Le ticket témoin est relu dans PostgreSQL et sa transition interdite est refusée. Effet utilisateur positif localement. Un volume persistant pendant cette requête ne démontre pas une reprise après perte de machine.

**Diagnostic.** Les refus métier sont des résultats attendus ; aucune panne DNS/port/service n’a été injectée. Une readiness rouge devrait conduire à examiner DNS `db`, port, rôle et schéma avant d’accuser le réseau ; cette procédure n’est pas une panne observée.

**Verdict et suite.** PARTIEL, niveau technique local L2. Qualifier une cible dédiée, le stockage et les secrets, exécuter K3s, diagnostiquer un défaut borné et refaire le ticket. **Explication personnelle Mathias : NON EXÉCUTÉE** ; expliquer les flux, la différence live/ready et la séparation image/volume.

## 2. Automatiser : rendre une configuration répétable sans fausse infrastructure

**Pourquoi.** L’opérateur doit retrouver une configuration compréhensible et détecter une dérive. Une reconstruction réelle demande ensuite une cible et des ressources explicitement gérées.

**Fichiers / responsabilité.** `infra/terraform/main.tf` stocke le contrat non secret ; `infra/ansible/render.yml` le rend en JSON local ; `infra/verify.py` contrôle les sorties et le second passage. Aucune modification du code métier et aucun provisioning VM n’interviennent. [Guide et choix](infrastructure.md).

**Pré-check.** Répertoire du dépôt autorisé, Terraform 1.15.8 et Ansible core 2.20.1 observés, absence de secret dans le contrat, état/plans ignorés par Git, temporaires sous `/tmp`. Aucun paquet, service, pare-feu ou cloud ne sera modifié.

**Exécution réelle.** `python3 infra/verify.py` lance init/validate/plan/apply, répète apply/plan, refuse `bind_address=0.0.0.0`, puis lance syntax-check et deux rendus Ansible. [La preuve du 3 novembre 13:37:46 UTC](../evidence/automation-contract.json) porte sur ce contrat uniquement.

**Attendu / observé.** Deuxième apply `0 added, 0 changed, 0 destroyed` ; deuxième plan code 0 ; deuxième rendu `changed=0 unreachable=0 failed=0`. Le bind public est refusé au plan. Aucun endpoint réseau n’est créé par `terraform_data`.

**Échec et diagnostic observés.** Le premier rendu a échoué avant génération : Ansible ne pouvait pas créer son temporaire par défaut sous le HOME. `ANSIBLE_LOCAL_TEMP` n’avait pas déplacé le temporaire de la cible locale. L’inventaire fixe maintenant `ansible_remote_tmp` sous `/tmp` ; la revalidation passe. [Premier essai conservé](../evidence/automation-first-attempt.json).

**Verdict et suite.** PARTIEL, sous-exercice local L2 ; provisioning/reconstruction Rocky NON EXÉCUTÉS. Qualifier KVM/VM, fournisseur/état et configuration Linux avant de revendiquer l’automatisation de l’infrastructure. **Explication personnelle Mathias : NON EXÉCUTÉE** ; expliquer ce que Terraform gère vraiment, l’état et le second passage.

## 3. Faciliter la livraison : relier le changement au ticket servi

**Pourquoi.** Une équipe de développement fictive doit livrer une petite évolution sans obtenir des droits administrateur sur l’hôte ; le support doit reconnaître la bonne version et conserver ses tickets.

**Fichiers / responsabilité.** Le développeur modifie l’application et ses tests. InfraOps fournit le `Dockerfile`, la configuration et les garde-fous. [Le chemin développeur](livraison.md) décrit les contrôles. Les éventuels jobs CI doivent être lus avec leur vraie exécution ; un fichier workflow n’est pas un résultat distant.

**Pré-check.** Différence relue, tests positifs/négatifs, image saine identifiée, secret exclu du build, cible isolée, sauvegarde avant migration de schéma. Aucun accès runner → laboratoire ni publication de registre n’est supposé.

**Exécution réelle.** Sept tests unitaires ont été exécutés localement. Le smoke et le navigateur contrôlent l’application en service. La version initiale est `0.1.0`, révision déclarée `uncommitted-v42` : ce n’est pas un SHA publié. Le contrôle structurel et les runs CI nouvellement publiés doivent être ajoutés avec leurs références effectives.

**Attendu / observé.** L’image démarre avec PostgreSQL et sert le parcours positif et les refus attendus. La relation commit → image immuable → cible → ticket n’est pas entièrement établie par ce succès local. Le [scan d’image disponible](../evidence/vulnerability-scan.json) est un résultat de sécurité distinct à lire ; aucun feu vert production n’en est déduit.

**Échec / diagnostic.** Les tests de règles refusent les transitions invalides. Aucun mauvais artefact n’a été promu puis diagnostiqué dans cette cellule ; la chaîne CI et ses blocages restent à constater, sans supprimer un contrôle pour la rendre verte.

**Verdict et suite.** PARTIEL, local L2 / chaîne distante à qualifier. Faire passer les jobs, contrôler le commit et l’image réellement servis, promouvoir la même image puis revenir à l’image saine avec relecture du ticket. **Explication personnelle Mathias : NON EXÉCUTÉE** ; expliquer image/tag/digest, permissions CI et rollback de code versus données.

## 4. Observer et diagnostiquer : comprendre l’effet utilisateur

**Pourquoi.** Un processus peut répondre alors que le ticket ne peut plus être enregistré. Le support doit être averti et l’opérateur doit localiser le problème avec des indices concordants.

**Fichiers / responsabilité.** L’application expose live/ready/version/metrics ; le [runbook Day-2](exploitation-day2.md) ordonne les contrôles et la lecture des logs. Les compteurs appartiennent à un worker et redémarrent avec lui ; ils ne constituent pas une collecte Prometheus/Grafana durable.

**Pré-check.** Définir un symptôme, les endpoints, la fenêtre, les journaux nettoyés et les critères de retour. Les contrôles en lecture sont distincts d’une panne volontaire, qui nécessite une cible isolée et la confirmation ciblée prévue.

**Exécution réelle.** Le smoke lit live, ready et metrics ; `opsdesk_database_up 1` a été observé pendant le parcours. Les codes 400/404/409 attendus sont conservés. Le diagnostic Ansible du pilier 2 apporte une méthode de tri, pas une alerte applicative ni un incident de cluster.

**Attendu / observé.** L’opérateur dispose de signaux locaux et de journaux ; aucun routage d’alerte, temps de détection, SLO ou panne de Pod n’est qualifié. Les éventuelles preuves de sonde ultérieures doivent être lues dans leur périmètre et ne valent pas une notification externe.

**Verdict et suite.** PARTIEL, signaux locaux L2. Définir une alerte utile, constater sa détection, corréler journaux/événements/métriques et rejouer le ticket après correction autorisée. **Explication personnelle Mathias : NON EXÉCUTÉE** ; expliquer le lien symptôme → hypothèse → observation → cause établie.

## 5. Maintenir et rétablir : conserver les tickets après intervention

**Pourquoi.** L’équipe IT doit retrouver demandes et statuts après une maintenance ou une reprise ; un redéploiement du code ne récupère pas une base perdue.

**Fichiers / responsabilité.** [Le runbook Day-2](exploitation-day2.md) décrit préparation, maintenance, sauvegarde et contrôle métier. Le volume et les rôles DB appartiennent à l’environnement ; le code métier ne constitue pas une stratégie de continuité.

**Pré-check à exécuter.** Nommer source/volume et **nouvelle cible de restauration**, versions PostgreSQL/app, capacité, archive, droits, état initial et possibilité de retour. Ne jamais supprimer ou écraser la base source pour obtenir une preuve. Toute intervention perturbatrice attend son périmètre et sa confirmation ciblée.

**Résultat attendu.** Sauvegarde cohérente, restauration sur une cible indépendante, ticket témoin relu avec son statut et contrôles applicatifs passés ; maintenance vérifiée avant/après. Renseigner horodatages, pertes observées et limites de stockage.

**Observation actuelle.** Aucune restauration ou maintenance n’est attestée par les preuves citées dans cette version du registre. Le smoke relit un ticket pendant une session normale ; il ne prouve pas une reprise. Commande de restauration effectivement exécutée : **NON EXÉCUTÉE** dans cette cellule. Cause d’incident : aucune panne provoquée ou observée à attribuer.

**Verdict et suite.** NON EXÉCUTÉ. Exécuter la sauvegarde/restauration bornée puis enrichir cette cellule avec la vraie preuve, sans réécrire l’état initial. **Explication personnelle Mathias : NON EXÉCUTÉE** ; expliquer volume/sauvegarde/restauration, contrôle métier et limitations d’une copie sur le même hôte.
