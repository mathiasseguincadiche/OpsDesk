# Feuille de route technique — OpsDesk Architecture V2

**Statut : conception Architecture V2 validée le 22 novembre 2026 ; implémentation infrastructure non vérifiée.** Le socle **Application OpsDesk V2** existe et a été testé ; aucun résultat des runners ne vaut déploiement Fedora/KVM/Rocky.

Le plan de référence détaillé est [Architecture V2 — phases 0 à 6](docs/architecture-v2-deploiement.md), avec [sept ADR](docs/adr/README.md), [matrice réseau](docs/architecture-v2-flux.md) et [STATUS](STATUS.md) pour les preuves réellement disponibles.

## Jalons d'implémentation

| Phase | Livraison technique attendue | Contrôle de passage | Statut |
| --- | --- | --- | --- |
| Application V2 (socle) | API, frontend, PostgreSQL, images, Alembic et CI | Voir les preuves existantes | Réalisé et testé en CI dans les limites de STATUS |
| 0 — Fedora | Réseau NAT libvirt, image cloud, Terraform, state et stockage protégés | Réseau, droits et capacité hôte vérifiés | Prévu, non vérifié |
| 1 — Administration | `srv-admin`, Ansible, Git, SSH, k6 depuis Terraform sur Fedora | Idempotence, accès SSH et sécurité du pilote | Prévu, non vérifié |
| 2 — Serveurs | `srv-app` et `srv-k3s` Rocky, Ansible, SELinux/firewalld, disque séparé | Second passage Ansible, ports autorisés/refusés | Prévu, non vérifié |
| 3 — Service | GHCR **privé**, trois images **par digest**, Compose serveur, TLS, Vault, Alembic | HTTPS réel, tickets, isolation DB/API et persistance | Prévu, non vérifié |
| 4 — Reprise | Dumps 02:00, réception SSH limitée, Borg externe chiffré, state, 7 copies | Restauration isolée, ticket témoin et RPO/RTO mesurés | Prévu, non vérifié |
| 5 — Supervision | K3s mono-nœud, copie d'essai, Prometheus, Grafana SMTP, k6 | Deux e-mails reçus, mesures/quotas et charge isolée | Prévu, non vérifié |
| 6 — Qualification | Idempotence, reconstruction jetable, reprise externe, charge/alertes | Quatre épreuves étayées par preuves datées | Prévu, non vérifié |

## Garanties de réalisation

- **Une seule cible principale :** Docker Engine + Compose sur `srv-app`. K3s héberge uniquement une copie d'essai séparée et la supervision.
- **Pas de double travail :** conserver les CI et les images applicatives déjà en place ; développer seulement les livraisons et déploiements non réalisés.
- **Sécurité dès la première mise en service serveur :** TLS navigateur, secrets Vault, GHCR privé, digests, port API/DB non exposé, sauvegarde chiffrée externe.
- **Reproductibilité :** Terraform depuis Fedora, Ansible depuis `srv-admin`, changements par PR et essais réels à chaque phase.
- **Aucune preuve inventée :** un plan ou une PR verte n'équivalent pas à la qualification sur Rocky.
- **Précaution :** aucune création/destruction de VM, migration de données existantes, modification réseau ou opération payante sans autorisation spécifique.

Les cours, corrections, évaluations et l'installation des outils demeurent dans **Notion**, distincts des livrables GitHub.

[Architecture V2](docs/adr/README.md) · [Flux](docs/architecture-v2-flux.md) · [Plan phases 0 à 6](docs/architecture-v2-deploiement.md) · [État](STATUS.md)
