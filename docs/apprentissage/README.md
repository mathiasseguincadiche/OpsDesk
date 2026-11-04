# Parcours personnel OpsDesk — V4.4

**Codex fournit l’application et les tests ; Mathias construit et exploite son infrastructure.** Accompagnement guidé. Le cadre technique commun reste Linux/Rocky, réseau, Terraform, Ansible, conteneurs, K3s adapté, CI/CD, supervision, sécurité, Day-2 et reprise. Aucun exercice n’est déclaré exécuté et aucun niveau personnel n’est renseigné.

Commencer par [le contrat applicatif](../contrat-applicatif.md), puis suivre cet ordre. Les anciens fichiers InfraOps Codex sont conservés comme références à examiner après sa propre tentative.

## Laboratoire et plateforme de travail

L’hôte prévu est **Fedora 45**, avec KVM/QEMU et libvirt ; le système invité cible est **Rocky Linux 10.2**. Cette cible reste prévue tant que les pré-checks et compatibilités exactes du [guide de laboratoire](../laboratoire-fedora-kvm-rocky.md) ne sont pas vérifiés. Les outils de contrôle Terraform/Ansible sont distingués des services exécutés dans la VM. Les exercices 01 et 02 ne demandent ni VM ni installation. Les ressources restent à dimensionner d’après les mesures du PC, sans multiplier les VM.

**GitHub est l’unique plateforme active du projet.** GitLab reste en l’état ; ses références historiques sont facultatives. Aucune synchronisation ni double gestion quotidienne n’est demandée. AWS et les variantes cloud restent des objectifs distincts à justifier et à autoriser, pas un prérequis du laboratoire local.

Docker, GitHub Actions/GHCR et Trivy sont reliés aux modules 06/08 ; Prometheus/Grafana et un test k6 borné au module 09. Les outils sont à vérifier, préparer et pratiquer personnellement.

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

Les [corrigés](corriges.md) sont séparés de la première lecture. Les [cinq évaluations](evaluations.md) mobilisent les acquis ; l’épreuve13 demande une tâche nouvelle. Les opérations sensibles exigent cible, pré-check et accord adapté. Le CV ne se modifie pas automatiquement.
