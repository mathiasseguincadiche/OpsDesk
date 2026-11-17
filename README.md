# OpsDesk

**Projet personnel InfraOps · Automatisation d’infrastructure et exploitation d’un service de tickets IT**

OpsDesk permet à un collaborateur de créer une demande et au support de la suivre jusqu’à sa clôture. Le programme Flask/PostgreSQL et ses tests sont fournis : mon travail porte sur la conception du laboratoire, l’automatisation de son déploiement, la livraison et l’exploitation du service.

**Contribution actuelle :** architecture locale retenue, décisions techniques documentées, contrat applicatif et parcours de qualification structurés. Les configurations Terraform, Ansible, Podman, K3s et CI/CD restent à écrire et à démontrer personnellement.

[Architecture](docs/architecture.md) · [Préparer les outils](docs/laboratoire-fedora-kvm-rocky.md) · [13 exercices](docs/apprentissage/README.md) · [État et preuves](STATUS.md) · [Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223)

![Présentation d’OpsDesk : service de tickets et trois phases du parcours cible](docs/diagrams/presentation.svg)

## Le service à déployer

![Capture de l’interface OpsDesk lors de l’essai historique](evidence/interface.png)

*Interface observée lors de l’essai historique. Le rendu actuel reste à requalifier.*

L’application expose des pages HTML, une API JSON et des points de contrôle de santé et de métriques. PostgreSQL conserve les demandes et leurs statuts. Le [contrat applicatif](docs/contrat-applicatif.md) précise les interfaces, dépendances et limites.

## L’architecture retenue

| Environnement cible | Responsabilité |
| --- | --- |
| Hôte Fedora 45 / KVM-libvirt | Héberger les VM et les sauvegardes hors VM |
| `srv-admin` — Rocky Linux 10.2 | Provisionner et configurer avec Terraform, Ansible, Git et SSH ; lancer les tests k6 |
| `srv-app` — Rocky Linux 10.2 | Faire fonctionner OpsDesk et PostgreSQL 17 avec Podman rootless, Quadlet et systemd |
| `srv-k3s` — Rocky Linux 10.2 | Orchestrer une copie d’essai indépendante et héberger Prometheus/Grafana |

Le service principal reste sur `srv-app`. K3s ne pilote pas ses conteneurs Podman. La copie d’essai et sa base sont distinctes ; le cluster à un seul nœud ne fournit pas de haute disponibilité.

[Schéma technique et décisions](docs/architecture.md) · [Sources Draw.io et matrice des flux](docs/diagrams/README.md)

## Trois phases, un seul service

| Phase | Résultat attendu (non encore démontré) | Outils principaux |
| --- | --- | --- |
| 1 — Préparer et automatiser | Créer les VM et déployer le service | Linux, Terraform, Ansible, Podman |
| 2 — Livrer et conserver | Livrer une image identifiée et restaurer les données | GitHub Actions, GHCR, Trivy, pg_dump, rsync |
| 3 — Orchestrer et maintenir | Observer la disponibilité, diagnostiquer et maintenir | K3s, Prometheus, Grafana, k6 |

Le [parcours de pratique](docs/apprentissage/README.md) suit son propre ordre pédagogique, distinct des phases.

## État du projet

| Élément | Avancement | Contrôle |
| --- | --- | --- |
| Application fournie | Réalisé | [26 tests réussis](evidence/qualification/application-tests.json), 3 nov. 2026 ; essai de développement ponctuel |
| Analyse de sécurité de l’image historique | Réalisé | Échec : 185 occurrences dont 45 HIGH ; [triage](docs/triage-securite.md) |
| Infrastructure personnelle et CI/CD | Prévu | Non vérifié : aucune VM, aucun déploiement ni pipeline personnel démontré |

Les preuves historiques ne qualifient pas Fedora/Rocky, le laboratoire cible ou une compétence personnelle. Le service n’a pas d’authentification : données fictives, laboratoire uniquement, aucune exposition Internet ni production.

[État daté](STATUS.md) · [Méthode de preuve](docs/preuves.md) · [Provenance des contributions](docs/provenance.md)

## Commencer

1. **Sans installation :** lire le contrat et [l’exercice 01](docs/apprentissage/01-application.md), puis dessiner le trajet d’un ticket.
2. Relire et justifier l’architecture dans [l’exercice 02](docs/apprentissage/02-architecture.md).
3. [Préparer les outils et le laboratoire](docs/laboratoire-fedora-kvm-rocky.md) avant la pratique Linux, réseau et automatisation.

## Explorer le dépôt

| Espace | Contenu |
| --- | --- |
| [app/](app/) · [db/](db/) | Programme fourni et schéma SQL |
| [tests/](tests/) · [scripts/](scripts/) | Tests et contrôle métier fournis |
| [docs/](docs/README.md) | Documentation et parcours actif |
| [evidence/](evidence/) | Rapports et observations, avec leur périmètre |
| [Références historiques](docs/historique.md) | Anciennes recettes, distinctes du laboratoire actuel |

[Feuille de route](ROADMAP.md) · [Licence MIT](LICENSE)
