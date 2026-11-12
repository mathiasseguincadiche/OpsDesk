# État d’OpsDesk

Dernière révision : 12 novembre 2026. Les preuves ci-dessous portent chacune leur date : aucun test, scan, machine virtuelle ou pipeline n’a été rejoué lors de cette révision.

**Avancement** : Prévu, En cours, Réalisé, Abandonné. **Contrôle** : Vérifié, Échec constaté, Non vérifié. Les deux informations sont distinctes : un élément réalisé peut rester non vérifié.

## Application

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Pages, API, statuts des tickets | Réalisé | Vérifié le 3 novembre 2026 : 26 tests réussis en 2,5 s | [Rapport](evidence/v44/application-tests.json) ; source montée en lecture seule dans un processus de développement ponctuel, PostgreSQL existant réutilisé |
| Persistance en base | Réalisé | Vérifié le 3 novembre 2026 : un ticket fictif validé puis relu par des connexions distinctes | Même rapport ; le ticket témoin est conservé, aucune donnée existante n’est modifiée |
| Hôte autorisé ou refusé, jeton CSRF non ASCII | Réalisé | Vérifié le 3 novembre 2026 : réponse 400 contrôlée | Même rapport ; ne démontre ni authentification ni sécurité réseau |
| Schéma SQL et paramètres | Réalisé | Vérifié par lecture, non exécuté sur une base neuve | [Contrat applicatif](docs/contrat-applicatif.md), `db/schema.sql` ; rôle, base et droits restent à préparer |
| Authentification des utilisateurs | Abandonné | — | [Sécurité](docs/securite.md) : évaluée puis non ajoutée ; données fictives, usage local uniquement |
| Rendu visuel de l’interface | Réalisé | Non vérifié sur la version actuelle | [Capture et rapport](evidence/browser.json) d’une version antérieure |

Le premier passage des tests a échoué sur deux points : un refus d’hôte qui tentait d’afficher une page avant la création de l’adaptateur d’URL, et une erreur de scénario sur un en-tête `Location`. Le [rapport initial](evidence/v44/application-tests-first-attempt.json) est conservé ; la source et le scénario ont été corrigés, puis la suite rejouée.

## Sécurité

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Analyse Trivy 0.74.0 de l’image `v42opsdesk-app:0.1.0-local` | Réalisé | Échec constaté le 3 novembre 2026 : 185 occurrences (45 HIGH, 72 MEDIUM, 61 LOW, 7 UNKNOWN), 85 CVE distinctes | [Rapport](evidence/vulnerability-scan.json) ; image historique, aucune vulnérabilité corrigeable de niveau HIGH ou CRITICAL |
| Tri des alertes | En cours | Non vérifié | [Triage](docs/triage-securite-v44.md) : qualification partielle, aucune acceptation de risque, aucune validation globale |

Le retrait des outils d’installation de l’image ne permet pas d’annoncer une sécurité validée.

## Infrastructure

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Smoke HTTP de l’essai historique | Réalisé | Vérifié le 3 novembre 2026 | [Rapport](evidence/business-smoke.json) ; Ubuntu/WSL2 avec Docker Compose, non rejoué depuis |
| Reprise après arrêt, essai historique | Réalisé | Vérifié le 3 novembre 2026 : 10,969 s, ticket témoin identique | [Rapport](evidence/recovery.json) ; ne constitue ni objectif de production ni exercice personnel |
| Conteneurs, Terraform, Ansible, K3s, CI | Prévu | Non vérifié | Les essais historiques n’ont créé aucune machine, aucun cloud ni cluster ; leurs fichiers ne sont pas dans le dépôt ([provenance](docs/provenance.md)) |
| Défaut `ci-business.json` / `business-smoke.json` du candidat CI | Prévu | Non vérifié | À diagnostiquer dans le parcours d’apprentissage |
| Laboratoire Fedora 45, KVM, Rocky Linux 10.2 | Prévu | Non vérifié | [Guide](docs/laboratoire-fedora-kvm-rocky.md) |

## Documentation

| Élément | Avancement | Contrôle | Preuve et portée |
| --- | --- | --- | --- |
| Schémas de présentation et technique | Réalisé | Vérifié en partie : export Draw.io, rouverture dans diagrams.net, thème sombre ; libellés trop petits à la largeur du README | [Fiche de contrôle](docs/diagrams/README.md#contrôles) |
| Affichage sur GitHub et Notion | Réalisé | Non vérifié à largeur étroite | — |

## Apprentissage

Aucun exercice d’infrastructure n’a été réalisé à ce jour. Les niveaux du [parcours](docs/parcours-apprentissage.md) (L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée) ne sont attribués par aucun test. Les [preuves](docs/preuves.md) décrivent la manière de les consigner.

Les pull requests fusionnées documentent l’historique des modifications ; elles ne prouvent ni exécution de la CI ni déploiement.
