# OpsDesk

**InfraOps · Infrastructure as Code · Livraison et exploitation**

Un service de tickets IT pour apprendre à rendre une application déployable, observable et restaurable. Le programme Flask/PostgreSQL est fourni ; le projet porte sur son infrastructure.

**Contribution actuelle :** conception du laboratoire local, choix d’architecture documentés et parcours de qualification. **Infrastructure à réaliser :** Terraform, Ansible, Podman, CI/CD et K3s.

[Architecture](docs/architecture.md) · [Démonstration](docs/demonstration.md) · [Documentation](docs/README.md) · [État et preuves](STATUS.md)

![OpsDesk — service de tickets et trois phases InfraOps cibles](docs/diagrams/presentation.svg)

## Construire, livrer, exploiter

| Responsabilité | Mise en pratique prévue |
| --- | --- |
| **Préparer et automatiser** | Créer les VM Rocky avec Terraform/libvirt, les configurer avec Ansible, déployer avec Podman/Quadlet |
| **Livrer et conserver** | Versionner et tester une image OCI avec GitHub Actions, GHCR et Trivy ; sauvegarder et restaurer PostgreSQL |
| **Orchestrer et maintenir** | Déployer une copie d’essai sur K3s, observer avec Prometheus/Grafana, éprouver avec k6 |

L’architecture distingue trois VM : `srv-admin` pilote, `srv-app` héberge le service principal, `srv-k3s` héberge la copie d’essai et la supervision. K3s ne pilote pas Podman ; le cluster mono-nœud n’est pas hautement disponible.

[Architecture technique et décisions](docs/architecture.md) · [Flux réseau et sources Draw.io](docs/diagrams/README.md)

## Le service

![Interface historique d’OpsDesk : formulaire et liste des tickets fictifs](evidence/interface.png)

*Capture historique du 3 novembre 2026 — [observation navigateur](evidence/browser.json). Le rendu actuel reste à requalifier.*

Créer, suivre et clôturer un ticket ; vérifier sa persistance dans PostgreSQL. Le [contrat applicatif](docs/contrat-applicatif.md) documente les routes HTTP, la santé du service et ses métriques.

## État et preuves

| Périmètre | Résultat |
| --- | --- |
| Application fournie | [26 tests réussis](evidence/qualification/application-tests.json), 3 nov. 2026 ; développement ponctuel |
| Image historique | [Scan en échec](docs/triage-securite.md), 185 occurrences dont 45 HIGH |
| Infrastructure personnelle | Prévue ; aucun déploiement ni pipeline vérifié |

L’application est un démonstrateur sans authentification, réservé aux données fictives et au laboratoire privé. Les preuves historiques ne qualifient ni Fedora/Rocky ni les compétences personnelles.

[État détaillé](STATUS.md) · [Provenance](docs/provenance.md) · [Feuille de route](ROADMAP.md)

## Explorer

| Pour | Consulter |
| --- | --- |
| Comprendre et pratiquer | [13 exercices](docs/apprentissage/README.md) · [Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) |
| Préparer le laboratoire | [Installation des outils](docs/laboratoire-fedora-kvm-rocky.md) |
| Examiner le code et les tests fournis | [app/](app/) · [db/](db/) · [tests/](tests/) · [scripts/](scripts/) |
| Consulter les preuves et l’historique | [evidence/](evidence/) · [Références historiques](docs/historique.md) |

Première séance sans installation : lire [l’exercice 01](docs/apprentissage/01-application.md), puis [l’architecture](docs/apprentissage/02-architecture.md).

Licence : [MIT](LICENSE) — les composants tiers conservent leurs propres licences.
