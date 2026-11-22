# ADR-05 — K3s, copie d'essai, Prometheus/Grafana et k6

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
`srv-k3s` est un nœud unique pour la supervision et une copie d'essai. Le service principal reste sous Compose sur `srv-app` ; l'usage des mêmes images n'efface pas les différences d'orchestrateur.

## Décision
- K3s mono-nœud, Traefik sous HTTPS, SELinux Enforcing et firewalld vérifiés. Namespaces `monitoring` et `essai`, chacun avec ResourceQuota et LimitRange.
- Dans `essai`, déployer les trois mêmes **digests GHCR** avec une base PostgreSQL de test indépendante et sans credentials ni volume du principal.
- Prometheus scrape `srv-app` (métriques applicatives filtrées, node exporter) et la copie d'essai. Valeurs initiales : 15 s de scrape, 15 jours et plafond 5 Go sous réserve du stockage réel.
- Grafana Alerting envoie **deux alertes par e-mail SMTP** : indisponibilité du service principal et ancienneté de la dernière sauvegarde. Vérifier la réception réelle.
- k6 exécuté sur `srv-admin` vers `essai` **uniquement** ; définir p95, taux d'erreurs et seuils à partir d'une mesure de référence.

## Alternatives étudiées
- Cluster haute disponibilité : hors périmètre.
- Tirs k6 sur la base principale : refusés.
- Loki/centralisation complète des logs : option future fondée sur un besoin mesuré.

## Vérification de réception prévue
- K3s/Traefik, DNS et métriques opérationnels en conservant SELinux et firewalld.
- Deux alertes reçues par e-mail lors de tests contrôlés ; tir k6 visible dans Grafana, sans dégrader `monitoring` ni le service principal.
- Dimensionnement indicatif `srv-k3s` : 4 vCPU/6 Go, à confirmer avant provisionnement.

## Risques et retour arrière
Un nœud K3s n'est pas HA ; la cohabitation d'`essai` et `monitoring` nécessite quotas, surveillance du disque et retour arrière de la copie.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
