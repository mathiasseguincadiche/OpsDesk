# OpsDesk — Architecture V3 : principes publics des flux

**Cible corrigée et validée en conception le 26 novembre 2026 ; laboratoire non déployé.** La matrice exacte, les adresses, identités et règles de filtrage restent privées dans Notion.

| Émetteur | Destination | Usage et contrainte |
| --- | --- | --- |
| Fedora / Terraform | Libvirt local | Réseau, volumes et VM ; aucun accès hyperviseur invité |
| Fedora / Ansible | Trois VM | SSH direct, comptes et droits minimaux, clés hôtes contrôlées |
| Fedora / navigateur | Principal et essai | HTTPS avec validation TLS |
| srv-admin / kubectl, Helm | K3s | API authentifiée, accès limité |
| srv-admin / k6 | Copie d’essai | HTTPS, cible autorisée, débit et durée bornés |
| srv-k3s / Prometheus | Exporteurs et métriques autorisés | Collecte filtrée, métriques séparées des routes métier |
| Fedora | Grafana sous K3s | Tunnel SSH direct puis port-forward local, authentification |
| srv-k3s / Grafana Alerting | Relais SMTP autorisé | E-mail, TLS, secrets protégés |
| Frontend | API | Réseau interne |
| API | PostgreSQL | Réseau interne, aucun port DB publié |
| VM | GHCR privé et dépôts OS | Sortant, authentifié selon besoin |
| srv-app | Fedora | Transfert restreint des exports, Borg externe |

Les deux bases, secrets et volumes sont distincts. La supervision partage K3s avec la copie d’essai dans des namespaces séparés : une panne complète du cluster peut la rendre indisponible. Tester les flux autorisés et refusés, notamment le filtrage Docker/firewalld. Aucun accès entrant public ou depuis la CI.

[ADR](adr/README.md) · [Plan](architecture-v3-deploiement.md) · [Vue globale](diagrams/architecture-globale-v3.svg)
