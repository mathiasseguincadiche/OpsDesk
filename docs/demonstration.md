# Présenter OpsDesk en 10 à 15 minutes

**Scénario oral proposé, non chronométré et non présenté comme une démonstration déjà réalisée par l’apprenant.** Les durées ci-dessous sont un découpage indicatif. Les tests de source et les observations du service historique ont des preuves séparées.

## Démonstration documentaire — disponible actuellement

1. Présenter le [schéma de présentation](diagrams/presentation.svg) et le besoin métier.
2. Examiner la [capture historique](../evidence/interface.png) et son [observation navigateur datée](../evidence/browser.json) : création et suivi de tickets, données fictives. La capture n'est pas une exécution actuelle.
3. Ouvrir le [rapport des 26 tests applicatifs](../evidence/qualification/application-tests.json), puis le [scan en échec](../evidence/vulnerability-scan.json). Expliquer leurs périmètres respectifs, pas une validation globale.
4. Présenter le [registre des choix](architecture.md#décisions-retenues) et les prochaines réalisations personnelles à démontrer dans le [parcours](apprentissage/README.md).

Aucun service n’a besoin d'être démarré pour cette revue. Aucune disponibilité 24 h/24 ni réception cloud/K3s n’est annoncée.

## Démonstration vivante — à préparer sur la cible personnelle

Le scénario ci-dessous exige un laboratoire reçu et des preuves personnelles. Il n'est pas une procédure aujourd'hui exécutable.

| Temps indicatif | Action | Ce que le lecteur doit comprendre |
|---|---|---|
| 0–2 min | Montrer le schéma de présentation et la page tickets | Le problème métier et le rôle InfraOps, distinct du code métier fourni |
| 2–5 min | Créer une demande, la prendre en charge puis la clôturer | Un service utile et des données, pas un simple endpoint de santé |
| 5–7 min | Lire `/version`, live et ready ; expliquer `db:5432` | Version réellement servie, réseau, différence processus/dépendance |
| 7–9 min | Rejouer le smoke et commenter un 400/409 attendu | Un échec de validation peut être un garde-fou correct |
| 9–11 min | Montrer les métriques et logs sans secrets | Observer le service ; endpoint métriques ≠ alerte opérationnelle |
| 11–13 min | Montrer le registre et les étapes Terraform/Ansible/K3s | Distinguer exécuté, vérifié, candidat et non exécuté |
| 13–15 min | Répondre aux questions et annoncer la prochaine preuve | La maîtrise se construit par tests, diagnostic et reprise |

Ne pas improviser une panne devant le recruteur. Une démonstration d’incident doit avoir été répétée sur la cible isolée, être récupérable et disposer de ses pré-checks. Présenter seulement son scénario tant qu’elle n’est pas exécutée.

Avant une démonstration vivante, vérifier l’existence de sa propre cible locale et sa version ; les anciennes commandes Compose sont [historiques et non exécutables depuis le dépôt courant](demarrage.md). Sans cible personnelle reçue, présenter le contrat, les schémas historiques et les preuves historiques.

## Questions d’entretien utiles

- Pourquoi la DB est-elle séparée de l’image de l’application ?
- Qu’arrive-t-il si live passe mais ready échoue ?
- Pourquoi un rollback de l’image ne restaure-t-il pas les tickets ?
- Comment relier ce qui est servi à un commit et à une image précise ?
- Comment passer de la conception à une infrastructure reproductible ? Expliquer le choix des ressources, les paramètres, les droits, les contrôles et la méthode de reprise.

[État réel](../STATUS.md) · [Architecture](architecture.md) · [Preuves](preuves.md)
