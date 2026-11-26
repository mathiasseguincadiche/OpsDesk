# ADR-05 — Kubernetes : copie d’essai et supervision

**Statut : validé en conception (Architecture V3 corrigée le 26 novembre 2026).** Rétablit le périmètre V2 de K3s ; laboratoire non déployé.

## Décision
Le principal reste sous Compose sur srv-app. K3s sur srv-k3s héberge la copie d’essai (données et secrets distincts) ainsi que Prometheus et Grafana, dans des namespaces distincts. Grafana Alerting envoie des e-mails. srv-admin porte kubectl, Helm, les outils de diagnostic et k6. Les tests de charge sont bornés et ciblent exclusivement la copie d’essai. Pas de VM supplémentaire, de Blackbox Exporter ni de supervision sous Compose.

## Justification
Pratiquer l’orchestration Kubernetes pour l’application d’essai et la supervision, sans ajouter de technologie. Une panne complète de K3s peut rendre la supervision indisponible ; ce compromis pédagogique est accepté. Les trois VM partagent l’hyperviseur : aucune haute disponibilité.

## Vérification
Collecte filtrée, deux e-mails reçus, accès Grafana privé, persistance des métriques, ressources bornées et absence d’impact mesurée sur le principal. Lors d’un incident K3s, diagnostiquer depuis srv-admin et vérifier le service principal séparément.

Les paramètres précis restent privés.
