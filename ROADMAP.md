# Feuille de route technique — OpsDesk

**Périmètre :** application de tickets et infrastructure Linux nécessaire à son exploitation. Cette feuille de route décrit des livrables techniques, **pas** un programme de formation ni des exercices. Les objectifs futurs sont indiqués **prévus / non vérifiés** ; voir [STATUS.md](STATUS.md).

La version 2 fournit FastAPI, React/nginx et PostgreSQL, avec des images non-root, des sondes et une pile Compose locale. La cible serveur retenue est Docker Engine et Compose sur Rocky Linux, administrée depuis `srv-admin` et configurée par Ansible ; K3s est réservé à une copie d'essai, sans remplacement silencieux de cette cible. Voir [architecture](docs/architecture.md).

## Livrables par phase

| Phase | Livrable technique | Vérification attendue | État |
| --- | --- | --- | --- |
| Socle applicatif | API, interface, base, conteneurs et tests | Tests, smoke, persistance, version, ports | Réalisé ; [preuves datées](STATUS.md) |
| 1 — Infrastructure | Trois VM Rocky sur Fedora/KVM, réseau privé, stockage et comptes | Identité des cibles, réseau, accès et protection vérifiés | Prévu, non vérifié |
| 1 — Provisionnement | Déclaration Terraform des VM et de leur réseau | Plan expliqué, application contrôlée, seconde passe sans dérive | Prévu, non vérifié |
| 1 — Configuration | Rôles Ansible et service Docker Compose sur `srv-app` | Idempotence, droits, SELinux, pare-feu, santé et ticket témoin | Prévu, non vérifié |
| 2 — Livraison | Tests CI, scan Trivy et deux images immuables publiées dans GHCR | Provenance des digests, contrôle avant installation | Prévu, non vérifié |
| 2 — Continuité | Sauvegardes hors VM, restauration isolée et retour arrière | Données relues, RPO/RTO observés sur cible connue | Prévu, non vérifié |
| 3 — Observabilité | Métriques Prometheus, vues Grafana et alertes justifiées | Collecte, déclenchement et réception des alertes | Prévu, non vérifié |
| 3 — Orchestration | Copie d'essai OpsDesk sur K3s | Déploiement, disponibilité, stockage et diagnostic | Prévu, non vérifié |
| 3 — Exploitation | Maintenance, mise à jour, diagnostic et reprise | Procédure reproductible, indisponibilité mesurée, preuve métier | Prévu, non vérifié |

## Décisions et contraintes

- **Laboratoire cible :** Fedora 45 / KVM / libvirt avec `srv-admin`, `srv-app`, `srv-k3s` sous Rocky Linux 10.2 ; sans haute disponibilité.
- **Exposition :** laboratoire privé et données fictives ; aucune mise en ligne publique sans nouvelle étude de sécurité.
- **Déploiement :** le serveur principal utilise Compose ; K3s reste une copie d'essai.
- **Changements à risque :** toute destruction, exposition réseau, utilisation d'une ressource payante ou restauration de données exige une analyse et une autorisation explicites.
- **Sources de vérité :** le [registre des décisions](docs/architecture.md#décisions-retenues) décrit les choix ; [STATUS.md](STATUS.md) décrit les observations ; [evidence/](evidence/) conserve les preuves réelles.

Les cours, préparations personnelles et évaluations sont maintenus **hors du dépôt produit**, dans le centre de formation Notion.

[Contrat applicatif](docs/contrat-applicatif.md) · [Architecture](docs/architecture.md) · [État](STATUS.md)
