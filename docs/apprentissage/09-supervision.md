# 09 — Superviser avec Prometheus et Grafana : mesures et alertes

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 09, accessible sur invitation. Schéma : [qui mesure quoi, et d'où viennent les alertes](../diagrams/pedagogique-supervision.svg).

**Objectif.** Superviser OpsDesk avec Prometheus et Grafana, mettre en place deux alertes testées, et partir d'une courbe pour formuler puis vérifier une hypothèse.

**Durée estimée** : 5 à 7 heures. **Prérequis** : OpsDesk sur `srv-app` (exercice 06), K3s et la copie d'essai (exercice 07). **État** : prévu, non vérifié.

## Pourquoi

Sans supervision, on apprend une panne par les utilisateurs, sans savoir depuis quand ni où. L'application expose ses mesures sur `/metrics` justement pour cela.

## L'essentiel à comprendre

- Prometheus **va chercher** les mesures toutes les 15 secondes et les garde 15 jours ; Grafana les dessine ; une alerte est une règle évaluée sur ces mesures. Aucune n'envoie de message : elles se lisent dans Prometheus et Grafana ([registre](../architecture.md#décisions-retenues)).
- Mesures exposées par l'API : `opsdesk_http_requests_total` (méthode, route, statut), `opsdesk_http_request_duration_seconds` (histogramme), `opsdesk_database_up`, `opsdesk_tickets` (statut, priorité), `opsdesk_users`, `opsdesk_logins_total`, `opsdesk_ticket_transitions_total`.
- Un compteur se lit avec `rate(…[5m])` ; une jauge se lit telle quelle ; une latence au 95ᵉ centile se calcule avec `histogram_quantile`.
- Le `for` d'une alerte évite les fausses alertes : la condition doit tenir pendant toute la durée.
- nginx bloque `/metrics` : Prometheus lit l'API directement sur le port 8000, ouvert à `srv-k3s` seulement.
- Si `srv-k3s` tombe, la supervision tombe avec.

## Ce qu'il faut obtenir

1. `node_exporter` sur `srv-app` et `srv-k3s`, port 9100 ouvert à `srv-k3s` seulement.
2. Prometheus dans K3s, quatre cibles à `up = 1` : l'API du service réel, celle de la copie, les deux `node_exporter`.
3. Deux alertes : base indisponible depuis 1 minute ; erreurs 5xx en hausse.
4. Un tableau de bord Grafana : requêtes par seconde, part des erreurs, latence au 95ᵉ centile, état de la base.
5. Les deux alertes testées sur la copie d'essai : panne, `pending`, `firing`, retour à la normale, heures notées.
6. Un essai de charge limité avec k6, depuis `srv-admin`, sur la copie d'essai uniquement.

**Livrable** : configuration, règles, tableau de bord exporté, capture des cibles, et les heures des tests d'alerte.

## Vérifications

| Ce que tu vérifies | Où | Résultat attendu |
| --- | --- | --- |
| Cibles lues | Prometheus, Status → Targets | Quatre `UP` |
| Règles chargées | Prometheus, Alerts | Deux règles, `inactive` en temps normal |
| Alerte « base » | Base de la copie arrêtée | `firing` après 1 minute, puis retour à `inactive` |
| Alerte « 5xx » | Panne provoquant des 5xx sur la copie | `firing`, puis retour |
| Service réel épargné | Ses panneaux pendant les tests | Aucune erreur |

## Pièges fréquents

Cible `DOWN` (port 8000 non publié, pare-feu, ou passage par nginx) ; compteur affiché sans `rate` ; alerte dont le `for` dépasse la durée de la panne ; historique perdu faute de stockage persistant pour Prometheus.

Suite : [exercice 10](10-maintenance.md).
