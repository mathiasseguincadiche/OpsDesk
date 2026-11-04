# CI : commandes, résultats et échecs

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

Le workflow GitHub vérifie un laboratoire éphémère sur ubuntu24.04 ; aucun accès au KVM de Mathias ni déploiement public. La pipeline GitLab miroir contrôle la source et les règles métier sans exiger de Docker privilégié. Les résultats distants doivent être lus après publication ; des fichiers présents ne sont pas une exécution.

| Étape / pourquoi | Déclencheur et dépendance | Commande / entrées | Sortie et critère | Échec / suite |
|---|---|---|---|---|
| Structural gate : refuser source invalide | Push branche/PR/manual après checkout | `python3 scripts/check.py` | Python/JSON/XML, deux couples diagrammes, motifs simples de secret | Lire errors, corriger puis reproduire ; ce n’est pas un scanner complet |
| Unité : règles de ticket | Gate réussi | `python3 -m unittest discover -s tests/unit -v` | 7 tests avec sous-cas, aucun DB | Statut/validation invalide : modifier règle ou test justifié |
| Lab métier : démontrer persistance/API | Unité réussie, secrets éphémères générés | `bash scripts/prepare-local.sh`, Compose build/up, `python3 scripts/smoke.py` | Ticket créé/lu/mis à jour, santé/version/métriques, refus négatifs | Logs service, DNS/DB/probes/version ; aucune suppression de volume pour passer |
| Reprise : vérifier données utiles | Lab sain et port libre | venv outil PyYAML puis `scripts/recovery_lab.py --port 18086` | Nouvelle cible, même ticket via HTTP | Étape/log privé du job, préserver source et rediagnostiquer |
| Preuves : relier au commit | Toujours, même en échec | JSON commit/run puis upload evidence/*.json | Artefact14jours sans secrets/dumps/.local | Pas d’artefact n’est pas une réussite ; relire journaux |
| GitLab verify-source | Commit de branche | `scripts/check.py` et unittest | Gate statique et métier pur | Même reproduction locale |

Références exactes : `.github/workflows/verify.yml` (référence locale V4.2), `.gitlab-ci.yml` (référence locale V4.2). Checkout et upload sont figés par SHA amont vérifié. Permissions GitHub contents:read seulement, aucun secret cloud ou registre. L’image contient version et révision ; les premières preuves locales indiquent honnêtement une révision non publiée. Les essais distants portent leur vrai commit CI.

La sonde locale `scripts/probe.py` retourne0 sur readiness saine et1 sur un port inutilisé (`evidence/probe-checks.json`). C’est un échec contrôlé de sonde, pas une panne injectée ni une fausse pipeline distante cassée/réparée. Le scan Trivy local conserve séparément ses résultats et vulnérabilités résiduelles ; cette CI ne prétend pas donner une certification de sécurité ou de mise en production.

Publication registre/GHCR, promotion, K3s, alerte routée et rollback de cluster restent à relier à des cibles/identités autorisées. Aucun job textuel ne simule un déploiement.
