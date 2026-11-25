# OpsDesk — Architecture V3 : principes publics des flux

**Validée en conception ; non déployée.** Remplace les [flux V2 historiques](architecture-v2-flux.md). La matrice exacte, les adresses, identités et règles de filtrage restent privées dans Notion.

| Émetteur | Destination | Usage et contrainte |
| --- | --- | --- |
| Fedora / Terraform | Libvirt local | Réseau, volumes et VM ; aucun accès hyperviseur invité |
| Fedora / Ansible | Trois VM | SSH direct, comptes et droits minimaux, clés hôtes contrôlées |
| Fedora / navigateur | Principal et essai | HTTPS avec validation TLS |
| Fedora / kubectl, Helm | K3s | API authentifiée, accès limité |
| Fedora / k6 | Copie d’essai | HTTPS, cible autorisée, débit et durée bornés |
| srv-ops / Prometheus | Exporteurs et métriques VM | Collecte filtrée, métriques séparées des routes métier |
| srv-ops / Blackbox Exporter | HTTPS principal et essai | Sondes avec CA interne |
| Fedora | Grafana sur srv-ops | Tunnel SSH direct, écoute locale |
| srv-ops / Grafana Alerting | Relais SMTP autorisé | E-mail, TLS, secrets protégés |
| Frontend | API | Réseau interne |
| API | PostgreSQL | Réseau interne, aucun port DB publié |
| VM | GHCR privé et dépôts OS | Sortant, authentifié selon besoin |
| srv-app | Fedora | Transfert restreint des exports, Borg externe |

Les deux bases, secrets et volumes sont distincts. La supervision fonctionne hors K3s mais dépend de Fedora. Tester les flux autorisés et refusés, notamment le filtrage Docker/firewalld. Aucun accès entrant public ou depuis la CI.

[ADR](adr/README.md) · [Plan](architecture-v3-deploiement.md) · [Vue globale](diagrams/architecture-globale-v3.svg)
