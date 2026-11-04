# Provenance et séparation des responsabilités — OpsDesk

| Ensemble | Origine constatée | Usage V4.4 |
|---|---|---|
| Application `app/`, schéma `db/schema.sql`, tests et contrat | Fournis par Codex pour une équipe de développement fictive | Support applicatif de laboratoire |
| Python, Flask/Jinja, psycopg, Gunicorn et PostgreSQL | Composants tiers, licences propres conservées | Dépendances du support ; la licence MIT du dépôt ne les remplace pas |
| Anciennes recettes conteneurs, Terraform, Ansible, K3s, CI et reprise | Générées et partiellement essayées par Codex sous V4.2 | Références historiques, à comparer après une tentative personnelle |
| Énoncés, indices, corrigés séparés et évaluations | Préparation pédagogique Codex | Aide progressive, aucun niveau personnel attribué |
| Infrastructure cible et opérations personnelles | À concevoir, écrire, exécuter et expliquer par Mathias | Réalisation personnelle à prouver |

## Chemins historiques identifiés et disponibilité actuelle

Les chemins suivants décrivent l’antériorité locale V4.2 rapportée dans les notes et preuves. Au contrôle de `main` `51e1a489` le 4 novembre 2026, ces configurations et scripts InfraOps sont absents du dépôt ; les JSON sous `evidence/` y restent disponibles. La conservation de leurs originaux dans un autre espace local est **NON VÉRIFIÉE** dans cette passe. Ils ne sont pas des solutions personnelles réalisées :

- Conteneurs : `Dockerfile`, `.dockerignore`, `compose.yaml`, `scripts/prepare-local.sh`.
- Administration DB : `db/001-initial.sql`, qui mélange schéma et création/droits du rôle.
- Terraform/Ansible : `infra/terraform/main.tf`, `infra/ansible/`, `infra/verify.py`.
- K3s : `k8s/` et `infra/verify_k8s.py`, rendus hors cluster seulement.
- CI : `.github/workflows/verify.yml`, `.gitlab-ci.yml`, candidats non exécutés à distance.
- Exploitation : `scripts/probe.py`, `scripts/recovery_lab.py`, contrôles et preuves sous `evidence/`.

La présente passe documentaire ne supprime, déplace, corrige ni exécute aucun de ces éléments. Elle conserve les chemins rapportés et les preuves présentes ; elle ne recrée pas les configurations absentes. Les configurations Terraform ne créaient que des contrats locaux ; les rendus Ansible écrivaient des fichiers localhost ; aucun provisioning Rocky/KVM/cloud ou cluster K3s n’était reçu.

## Usage pédagogique honnête

Les anciens guides techniques sont balisés comme références Codex, avec contexte historique. Ils peuvent aider après la première tentative, mais Mathias décide de son architecture et écrit ses propres fichiers. Les résultats V4.2 ne renseignent pas son niveau : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée sur une tâche nouvelle.

Le défaut `ci-business.json`/`business-smoke.json` du candidat CI est documenté pour son diagnostic personnel, sans reconstruction du pipeline par Codex. Les preuves de reprise sont historiques et n’imposent pas leurs durées comme objectifs de production.

## Maintenir les documents sans entretenir plusieurs copies

La charte documentaire V5 est le référentiel de cette passe ; le logiciel et le parcours personnel gardent leur version V4.4. Mathias valide les décisions et fournit les résultats personnels ; Codex prépare les corrections documentaires dans une PR dédiée. Le même outil a rédigé et contrôlé cette passe : cela ne constitue pas une revue indépendante humaine.

| Question du lecteur / rôle principal | Source de vérité et déclencheur de mise à jour |
|---|---|
| Découvrir le projet | [README](../README.md), à modifier lorsque périmètre ou état change |
| Apprendre et comprendre | [Exercices](apprentissage/README.md) et Notion ; actualiser les liens et notions dans le même changement, sans dupliquer le README |
| Connaître l’interface, les champs et contraintes | [Contrat](contrat-applicatif.md), confronté à business.py/web.py et schema.sql ; chaque évolution de l’API entraîne sa relecture |
| Expliquer un choix durable | [Registre des décisions](architecture.md#décisions-durables-et-décisions-encore-personnelles), enrichi après une vraie décision ; ne pas inventer les raisons manquantes |
| Constater un résultat | [STATUS](../STATUS.md) et [preuves](preuves.md), avec date, version, méthode et portée ; retirer une présentation « actuelle » devenue périmée, conserver le rapport historique |
| Agir en incident | [Triage](reprise.md#triage-court-avant-une-reprise-personnelle), puis procédure personnelle qualifiée ; exercices et explications restent séparés |

Ces rôles distinguent explication, apprentissage, référence et guide pratique ; ils ne créent pas quatre arborescences supplémentaires. Avant un déplacement, recenser les liens entrants. Les versions de distribution/outils, compatibilités, captures et interfaces vieillissent : les recontrôler dans leurs sources officielles avant pratique ; ne pas transformer une date de rédaction en date de réception.

**Vocabulaire retenu :** hôte = Fedora prévu ; invité = VM Rocky prévue ; application = programme fourni ; infrastructure personnelle = solution de Mathias ; référence historique = essai Codex daté. « Réalisé/implémenté » décrit la présence ; « vérifié » décrit un contrôle traçable ; « PASS » le résultat de ce contrôle ; « autonomie L3 » une adaptation ou un diagnostic personnel nouveau. Réutiliser ces termes dans les pages sans renommer massivement les propriétés Notion.

## Fiche de reprise documentaire — état au 4 novembre 2026

- **Mission :** appliquer les apports utiles V5 à la documentation OpsDesk existante ; autorisation de correction GitHub/Notion et PR en brouillon, sans merge ni réalisation InfraOps.
- **Base relue :** main `886918115e4321c89c0923e4ea95286c50e2e506`, après fusion de #3 à 18:38:48 UTC. Cette fiche devra être confrontée au vrai main lors de la reprise suivante.
- **Décisions conservées :** un dépôt/service, GitHub actif, parcours personnel V4.4, exercice 01 sans VM ; [registre](architecture.md#décisions-durables-et-décisions-encore-personnelles).
- **Documents préparés :** règles de preuve, API, décisions, triage et maintenance ; [audit V5](audit-documentaire-v5.md) pour les contrôles exacts et leurs limites. La présence de ces documents ne vaut pas leur validation humaine.
- **État technique :** aucun nouveau test, déploiement, scan ou essai personnel ; les rapports applicatifs Codex restent ceux de leur version et environnement.
- **À confirmer par la pratique :** laboratoire et versions, choix personnels, restauration, CI et autonomie. Leurs niveaux/preuves ne sont pas préremplis.
- **Première action suivante :** relire cette fiche et la PR de la passe V5, contrôler branche/commit/statut, puis démarrer ou poursuivre l’exercice 01 avec sa propre reformulation. Une fusion exige une décision ciblée distincte.
