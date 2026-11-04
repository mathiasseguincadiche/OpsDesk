# Apprendre OpsDesk par des résultats observables

## Parcours actif et laboratoire personnel

Commencer par [l’exercice personnel V4.4 n° 1 — comprendre l’application](apprentissage/01-application.md) et [le contrat applicatif](contrat-applicatif.md). Les [13 exercices prioritaires](apprentissage/README.md) sont distincts des supports théoriques et preuves historiques conservés. Les corrigés se consultent après une tentative ; les cinq évaluations personnelles sont dans `docs/apprentissage/evaluations.md`.

Le laboratoire prévu est **Fedora 45 hôte → KVM/QEMU/libvirt → Rocky Linux 10.2 invité**. Les exercices 01/02 se font en lecture et dessin ; pour la préparation technique, lire [le guide de laboratoire et ses contrôles](laboratoire-fedora-kvm-rocky.md). Aucune compatibilité, installation ou VM personnelle n’est validée par les essais historiques Ubuntu/WSL de Codex. Une version ou un contrôle non vérifié reste signalé ; aucune substitution silencieuse de Rocky Linux n’est autorisée.

GitHub est l’unique plateforme active de ce parcours. GitLab est laissé en l’état ; ses anciennes références sont historiques et facultatives, sans synchronisation ni second flux quotidien.

**V4.4 : premier projet accompagné.** Mathias écrit et réalise lui-même ses configurations ; Codex explique, propose des indices puis examine sa tentative. Le Notion OpsDesk existant garde sa fonction pédagogique et son historique. Ce dépôt fournit les sources et les preuves ; il ne crée pas un deuxième parent Notion ni une duplication littérale des leçons.

## Ordre de progression V4.4

Application → architecture personnelle → Linux/réseau → Terraform → Ansible → conteneurisation → K3s → CI/CD → supervision → Day-2 → sauvegarde/restauration → diagnostic/rétablissement → épreuve nouvelle d’autonomie. Les contenus utiles sont conservés ; ce parcours ne force pas 13 pages exactement. Les énoncés complets, indices et corrigés séparés sont préparés avec le parcours Notion ; les anciennes solutions sont des références à consulter après la première tentative, pas des réponses imposées.

L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. **Aucun niveau n’est attribué par les tests de Codex.** Le premier exercice porte sur les besoins techniques d’OpsDesk et un schéma proposé personnellement.

## Méthode progressive conservée

Pour chaque tâche : **problème → prérequis → mécanisme → minimum utile → test → diagnostic → explication personnelle**. Progresser de « je reconnais les composants » à « j’exécute guidé », puis « j’interprète », « je diagnostique » et enfin « je reproduis et j’explique ». Un fichier écrit ou un job vert ne suffit pas à valider la dernière étape.

## Exercices à partir du service actuel

1. Ouvrir un ticket dans l’UI, le retrouver par l’API et expliquer pourquoi il est dans PostgreSQL.
2. Comparer `/health/live`, `/health/ready`, `/version` et `/metrics` ; décrire les limites de chaque signal.
3. Envoyer une entrée trop courte et une transition interdite ; expliquer pourquoi les refus attendus sont des tests réussis.
4. Dessiner le trajet navigateur → port local → app → DNS `db` → PostgreSQL → volume.
5. Lire un échec réel, formuler une hypothèse, vérifier une seule chose à la fois et conserver l’observation.
6. Préparer les exercices de livraison, maintenance et restauration ; ne les compter que lorsqu’ils ont été exécutés sur une cible identifiée.

## Cinq piliers — réception séparée

| Pilier | Preuve directrice OpsDesk | État personnel Mathias |
|---|---|---|
| Construire | Chemin réseau jusqu’au service tickets sur la cible retenue ; K3s lors du module dédié et après qualification | **NON EXÉCUTÉ personnellement** dans les preuves suivies ; niveau non évalué |
| Automatiser | Terraform/Ansible reconstruisent l’environnement autorisé | **NON EXÉCUTÉ personnellement** ; les anciens rendus locaux sont ceux de Codex |
| Faciliter la livraison | CI d’image et vérification d’un ticket sans SSH administrateur développeur | **NON EXÉCUTÉ personnellement** ; construire ses jobs à partir d’une procédure comprise |
| Observer/diagnostiquer | Alerte applicative et panne analysée | **NON EXÉCUTÉ personnellement** ; signaux/alerte/diagnostic à proposer et vérifier |
| Maintenir/rétablir | Maintenance Day-2 et reprise des tickets | **NON EXÉCUTÉ personnellement** ; les reprises historiques Codex restent distinctes |

Pour chaque ligne, renseigner : pourquoi, fichiers, pré-check, commande/version réelle, contrôle positif et négatif, diagnostic, preuve datée et explication personnelle. Ne pas annoncer « cinq piliers vérifiés » avec la seule tranche HTTP locale.

## Glossaire ciblé

- **Image** : artefact d’exécution ; un tag précis n’est pas nécessairement immuable, un digest identifie le contenu.
- **Volume** : données séparées du cycle de vie du conteneur ; pas une sauvegarde.
- **CI** : contrôles répétés sur un changement ; lire les étapes et leurs échecs.
- **Idempotence** : répétition sans changement indésirable, à constater sur une seconde exécution.
- **Readiness** : dépendances nécessaires disponibles ; pas une preuve exhaustive du parcours utilisateur.
- **Observabilité** : indices pour comprendre un état ; une métrique n’est ni un log ni une alerte.
- **Rollback** : retour d’une version applicative ; distinct d’une restauration de données.

## Conservation des supports antérieurs

Les premiers guides de conception portaient déjà sur les trois phases, les secrets, la persistance, la CI et le diagnostic. Ces connaissances restent présentes dans [architecture](architecture.md), [démarrage](demarrage.md), [livraison](livraison.md) et [Day-2](exploitation-day2.md). Les anciennes assertions « aucune application » ne décrivent plus cette révision ; les originaux sont conservés dans la sauvegarde d’audit et l’historique du dépôt.

Les [cinq évaluations personnelles V4.4](apprentissage/evaluations.md) fixent les contrôles à produire. Les [anciennes évaluations Codex](evaluations.md) conservent leurs essais datés et indiquent besoins, pré-checks, commandes réelles, erreurs, preuves et suites. Le [guide infrastructure](infrastructure.md) explique la différence entre contrat local testé et infrastructure réellement provisionnée.
