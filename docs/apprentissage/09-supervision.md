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
- nginx bloque `/metrics` sur l’entrée utilisateur. La cible initiale autorise le port 8000 depuis `srv-k3s` seulement. Dans cet exercice, réduis cette surface : réserve une entrée privée aux seules métriques, sans routes métier, restreins sa source à la supervision, et referme le port direct de l’API. Vérifie un scrape réussi, le refus d’une route métier sur l’entrée de métriques et le refus des sources non autorisées. Justifie les règles réellement appliquées par Docker ; mettre à jour le registre et les schémas après validation.
- Si `srv-k3s` tombe, la supervision tombe avec.
- **SLI** : mesure d'un comportement du service (par exemple la proportion de requêtes valides réussies). **SLO** : objectif chiffré pour cet indicateur sur une fenêtre définie. Une sonde verte ou une cible `up` ne constitue pas, seule, un SLI de disponibilité utilisateur ; un SLO de laboratoire n'est pas un SLA contractuel.

## Cas voisin : une cible Prometheus est UP, mais l'utilisateur échoue

**Situation fictive, non mesurée.** Prometheus parvient à lire `/metrics` sur une API dont une route métier renvoie des erreurs. `up = 1` signifie que le scrape a réussi ; cela ne suffit pas à dire que les utilisateurs peuvent créer et relire leurs tickets.

**Méthode.** Choisir d'abord la question à répondre (proportion d'erreurs, latence, disponibilité de la base), puis la métrique, la fenêtre temporelle et le trafic à inclure. Un compteur brut cumule des événements : un débit exige un calcul sur une fenêtre. Une alerte doit être déclenchée **et observée revenir à la normale**, sur une copie isolée, avant de servir de preuve. Sans série mesurée, aucune valeur de SLI/SLO ne doit être inventée.

## Ce qu'il faut obtenir

1. `node_exporter` sur `srv-app` et `srv-k3s`, port 9100 ouvert à `srv-k3s` seulement.
2. Prometheus dans K3s, quatre cibles à `up = 1` : l'API du service réel, celle de la copie, les deux `node_exporter`.
3. Deux alertes : base indisponible depuis 1 minute ; erreurs 5xx en hausse.
4. Un tableau de bord Grafana : requêtes par seconde, part des erreurs, latence au 95ᵉ centile, état de la base.
5. Les deux alertes testées sur la copie d'essai : panne, `pending`, `firing`, retour à la normale, heures notées.
6. Un essai de charge limité avec k6, depuis `srv-admin`, sur la copie d'essai uniquement. Avant de lancer, définir un scénario de lecture, sa charge, sa durée et son arrêt de sécurité ; choisir un objectif de taux de succès et de latence p95, justifier les seuils et relever débit, CPU/RAM et saturation. Exclure les requêtes hors périmètre (p. ex. refus d'accès volontaires) selon une règle écrite ; si aucun trafic n'est observé, ne pas inventer de ratio. Comparer les résultats aux objectifs, émettre une hypothèse et expliquer le prochain contrôle. Un essai court ne prouve pas une disponibilité mensuelle.

**Livrable** : configuration, règles, tableau de bord exporté, capture des cibles, heures des tests d'alerte, tests k6 interprétés et preuves du filtrage des métriques.

## Vérifications

| Ce que tu vérifies | Où | Résultat attendu |
| --- | --- | --- |
| Cibles lues | Prometheus, Status → Targets | Quatre `UP` |
| Règles chargées | Prometheus, Alerts | Deux règles, `inactive` en temps normal |
| Alerte « base » | Base de la copie arrêtée | `firing` après 1 minute, puis retour à `inactive` |
| Alerte « 5xx » | Panne provoquant des 5xx sur la copie | `firing`, puis retour |
| Objectifs et charge | Mesures k6 et Grafana | Scénario, fenêtre, seuils, résultats et limites consignés ; pas d'objectif déclaré atteint sans mesure |
| Service réel épargné | Ses panneaux pendant les tests | Aucune erreur |
| Entrée privée réservée aux métriques | Test depuis la supervision et une source non autorisée ; test d’une route métier | Scrape réussi ; accès non autorisés et routes métier refusés ; API directe non publiée |

## Pièges fréquents

Cible `DOWN` (adresse de collecte, filtrage des sources, endpoint des métriques ou passage par le proxy utilisateur) ; compteur affiché sans `rate` ; alerte dont le `for` dépasse la durée de la panne ; historique perdu faute de stockage persistant pour Prometheus.

Suite : [exercice 10](10-maintenance.md).
