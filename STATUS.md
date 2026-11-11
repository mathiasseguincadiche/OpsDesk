# OpsDesk — réception applicative et progression personnelle

**Preuves applicatives V4.4 du 3 novembre 2026 ; révision documentaire du 4 novembre 2026.** Les sources applicatives sont testées dans un processus de développement ponctuel, sur le PostgreSQL existant. Aucun service n’a été redéployé, aucune image reconstruite et aucun exercice InfraOps personnel exécuté.

## Références GitHub contrôlées

Le contrôle du 4 novembre 2026 constate la PR [#1](https://github.com/mathiasseguincadiche/OpsDesk/pull/1) fusionnée à 02:11:40 UTC (`16b63546`) et la PR [#2](https://github.com/mathiasseguincadiche/OpsDesk/pull/2) fusionnée à 14:33:12 UTC. La PR [#3](https://github.com/mathiasseguincadiche/OpsDesk/pull/3) a été fusionnée le 4 novembre 2026 à 18:38:48 UTC ; la PR [#4](https://github.com/mathiasseguincadiche/OpsDesk/pull/4) a ensuite été fusionnée le 4 novembre à 21:28:52 UTC, portant `main` au commit `05caa712e28ffac4af1239c9e0d3b4175129ec1f` (contrôlé le 10 novembre 2026). Les audits précédents restent des observations datées de leur propre révision. Ces fusions documentent l’intégration des sources ; elles ne sont pas des preuves de CI ou d’infrastructure exécutée. GitHub reste la seule plateforme active ; GitLab est historique.

**Recentrage du parcours — 10 novembre 2026 :** la [PR #5](https://github.com/mathiasseguincadiche/OpsDesk/pull/5) a été fusionnée, avec `4c8444ec11bba406c2e7f4cfb67b993a304131aa` comme référence documentaire contrôlée après cette intégration. Elle organise le projet fil rouge unique et ses supports ; elle ne constitue pas une exécution du laboratoire personnel. Les preuves applicatives et les observations historiques conservent leurs dates propres.

**Finition éditoriale V11 (PR #6) :** lisibilité de l’accueil GitHub/Notion et mise en avant des procédures pour environnements neufs ou déjà équipés. Cette finition ne modifie ni l’application, ni la sécurité, ni les preuves techniques et ne prétend pas avoir exécuté Terraform, Ansible, K3s, CI ou une restauration personnelle.

## Portée de cette révision documentaire

**Documentation : réalisée — vérifiée par les contrôles documentaires décrits dans [l’audit V5](docs/audit-documentaire-v5.md), selon leur périmètre. Infrastructure personnelle : prévue — non vérifiée.** Le parcours et le logiciel restent V4.4 ; V5 désigne la charte. Une procédure écrite, une preuve ancienne et un niveau personnel sont trois objets distincts. Aucun test applicatif, scan, VM ou CI n’est rejoué par cette mise à jour. Les résultats ci-dessous appartiennent aux essais datés ; une modification de leur périmètre impose une nouvelle réception.

## Application

| Contrôle | Résultat et source | Portée |
|---|---|---|
| Règles, routes, formulaires et SQL réel de la source actuelle | [Rapport courant V4.4](evidence/v44/application-tests.json) et journal voisin | Lire le statut, la date, le nombre de tests et les hashes ; la plupart des écritures sont en table TEMP |
| Persistance réelle | Cas de test dédié : ticket fictif committé puis relu par des connexions distinctes | Le ticket témoin est conservé ; aucune donnée existante supprimée ou remplacée |
| Host autorisé/refusé et CSRF non ASCII | Cas positifs/négatifs dans la même suite | Réponse 400 contrôlée ; ni authentification ni sécurité réseau complète |
| Schéma et paramètres | [Contrat à 30 rubriques](docs/contrat-applicatif.md), `db/schema.sql` | Le rôle/base/droits/stockage restent à préparer par Mathias |
| Authentification | Absente, déclarée explicitement | Local fictif uniquement |
| Réception visuelle | [Capture et rapport V4.2](evidence/browser.json) | Historique, ne certifie pas chaque source V4.4 montée pour les tests |

Le premier passage V4.4 a découvert un refus Host qui tentait de rendre un modèle avant création de l’adaptateur d’URL, ainsi qu’une erreur de scénario du test réutilisant un en-tête Location absent après PATCH. [Rapport initial défavorable conservé](evidence/v44/application-tests-first-attempt.json). La source et le scénario ont été corrigés puis la suite rejouée ; le rapport courant porte son propre statut.

## Antériorités Codex V4.2

Le [smoke HTTP historique](evidence/business-smoke.json) a été actualisé le 3 novembre à 13:40 UTC. Le [dernier essai de reprise historique](evidence/recovery.json) est daté à 13:52:06 UTC, cible 18088, durée 10,969 s et ticket témoin identique. Une reprise précédente 10,769 s reste conservée séparément. Ces mesures n’ont pas été rejouées sous V4.4 et ne constituent ni SLO de production ni exercice personnel.

Les contrats Terraform/Ansible locaux et le rendu K3s étaient des essais Codex. Ils n’ont provisionné aucune VM/cloud et n’ont qualifié aucun cluster. Les anciens pipelines locaux ne sont pas exécutés ni corrigés automatiquement. Le candidat OpsDesk comporte encore le défaut `ci-business.json`/`business-smoke.json`, à étudier dans un exercice de diagnostic.

Le [scan complet historique](evidence/vulnerability-scan.json) reste FAIL, avec 185 occurrences dont 45 HIGH dans ce rapport. Le retrait d’outils d’installation de l’image n’autorise pas à annoncer une sécurité globale validée. Les nouveaux résultats de tri de sécurité du programme sont une pièce distincte.

## Mathias : pratique et autonomie

Les cinq responsabilités restent à réaliser personnellement : infrastructure/réseau, automatisation, déploiement/CI, supervision/diagnostic, maintenance/reprise. **Aucune preuve ou niveau L0/L1/L2/L3 personnel n’est attribué par les tests de Codex.** L2 exige une réalisation personnelle ; L3 une adaptation et un diagnostic autonomes sur une tâche nouvelle.

[Parcours](docs/parcours-apprentissage.md) · [Provenance](docs/provenance.md) · [Contrat](docs/contrat-applicatif.md). Le CV et la lettre de motivation sont gérés séparément ; aucune compétence personnelle n’est ajoutée sur la seule base des essais Codex ou d’une mise à jour documentaire.
