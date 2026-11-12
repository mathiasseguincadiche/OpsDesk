# Feuille de route d’OpsDesk

OpsDesk est le projet fil rouge unique du parcours. L’application est fournie ; l’infrastructure et son exploitation sont à construire, exercice après exercice. Aucun exercice d’infrastructure n’est réalisé à ce jour : tous les éléments ci-dessous sont au statut **Prévu**, et leur contrôle est **Non vérifié**. L’[état détaillé](STATUS.md) donne les preuves existantes.

## Étapes

| N° | Étape | Exercice |
| --- | --- | --- |
| 1 | Comprendre l’application et lire son contrat | [01](docs/apprentissage/01-application.md) |
| 2 | Concevoir l’architecture et justifier ressources, flux, accès et stockage | [02](docs/apprentissage/02-architecture.md) |
| 3 | Préparer Linux, Rocky Linux et le réseau du laboratoire | [03](docs/apprentissage/03-linux-reseau.md) |
| 4 | Écrire le Terraform, lire le plan, vérifier les ressources créées | [04](docs/apprentissage/04-terraform.md) |
| 5 | Écrire l’Ansible, contrôler les changements puis la seconde passe | [05](docs/apprentissage/05-ansible.md) |
| 6 | Conteneuriser l’application ; choisir volumes, réseaux et secrets ; vérifier un ticket | [06](docs/apprentissage/06-conteneurs.md) |
| 7 | Pratiquer K3s : ressources, sondes, stockage, mise à jour et diagnostic | [07](docs/apprentissage/07-k3s.md) |
| 8 | Construire la CI/CD à partir d’une livraison manuelle comprise | [08](docs/apprentissage/08-cicd.md) |
| 9 | Choisir des signaux utiles, construire la supervision, vérifier une alerte | [09](docs/apprentissage/09-supervision.md) |
| 10 | Préparer une maintenance et contrôler le service avant et après | [10](docs/apprentissage/10-maintenance.md) |
| 11 | Concevoir une sauvegarde et une restauration isolée ; vérifier les tickets | [11](docs/apprentissage/11-sauvegarde-reprise.md) |
| 12 | Diagnostiquer un cas nouveau et rétablir le service | [12](docs/apprentissage/12-diagnostic.md) |
| 13 | Refaire une tâche nouvelle et expliquer ses choix avec une aide limitée | [13](docs/apprentissage/13-autonomie.md) |

## Principes

- Le laboratoire prévu est **Fedora 45 (hôte) → KVM, QEMU, libvirt → Rocky Linux 10.2 (invité)**. Les exercices 1 et 2 se font en lecture et en dessin ; la préparation technique suit le [guide du laboratoire](docs/laboratoire-fedora-kvm-rocky.md). Une version non vérifiée reste signalée, et Rocky Linux n’est pas remplacé en silence.
- L’architecture retenue (deux serveurs Rocky Linux, réseau `opsdesk-lan`, Podman, sauvegarde, supervision) est dans le [registre des décisions](docs/architecture.md#décisions-retenues) et sur le [schéma technique](docs/diagrams/architecture-technique.svg).
- Les corrigés se lisent après une première tentative. Les anciennes solutions sont des références datées, pas des fichiers à recopier ([provenance](docs/provenance.md)).
- Toute ressource payante, exposition réelle, destruction ou nettoyage demande son périmètre et un accord préalable.
- GitHub est l’unique plateforme active. GitLab reste en l’état, à titre historique.
- AWS est facultatif et dépend d’un budget et d’une autorisation.

[Parcours](docs/parcours-apprentissage.md) · [Contrat applicatif](docs/contrat-applicatif.md) · [État](STATUS.md)
