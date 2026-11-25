# ADR-05 — Kubernetes d’essai et observabilité indépendante

**Statut : validé en conception (Architecture V3).** Remplace la cohabitation V2.

## Décision
Le principal reste sous Compose sur srv-app. K3s sur srv-k3s héberge uniquement la copie d’essai, avec données et secrets distincts. Prometheus, Grafana et Blackbox Exporter vivent sur srv-ops sous Compose. Grafana Alerting envoie des e-mails. k6 s’exécute à la demande depuis Fedora avec limites et arrêt de sécurité. Les exercices de performance utilisent uniquement Fedora et srv-k3s ; aucune VM de charge supplémentaire n’est prévue.

## Justification
Une panne K3s ne doit pas supprimer la supervision. Les trois VM partagent toutefois l’hyperviseur : aucune haute disponibilité. Le générateur de charge peut affecter les ressources communes.

## Vérification
Collecte filtrée, sondes HTTPS, deux e-mails reçus, panne K3s visible depuis srv-ops, métriques persistantes, ressources bornées et absence d’impact mesurée sur le principal. Aucun accès Grafana public.

Les paramètres précis restent privés.
