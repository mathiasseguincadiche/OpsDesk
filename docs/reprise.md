# Reprise : retrouver les tickets après une panne

Ce document dit comment décider d'une reprise, et comment la mener sans aggraver la situation. Mise à jour : 18 novembre 2026, pour la version 2.0.0.

**État** : le dispositif de sauvegarde et la restauration de la base d'OpsDesk sont **prévus, non réalisés** ([exercice 11](apprentissage/11-sauvegarde-reprise.md)). La méthode ci-dessous a été démontrée sur une base de démonstration le 18 novembre 2026, pas encore sur OpsDesk.

## Triage court avant une reprise personnelle

Symptômes d'entrée : tickets inaccessibles, lecture ou écriture refusée, `/health/ready` en `503`, ou données attendues absentes.

1. **Identifier.** La machine, la version (`/version`), le point d'entrée et un ticket témoin connu. Noter l'heure, le symptôme et l'impact. Si la cible est ambiguë, s'arrêter avant toute modification.
2. **Observer sans rien changer.** Les trois sondes, l'état des services, les journaux de l'API et de la base, l'espace disque. `/metrics` peut répondre `200` alors que la base est arrêtée : c'est `opsdesk_database_up` qu'il faut lire.
3. **Séparer les causes.** Accès (réseau, pare-feu), application, connexion à la base, données. La plupart des pannes se corrigent **sans restauration** : redémarrer la base, remettre un secret, rouvrir un port. Ne jamais réinitialiser un stockage pour tester une hypothèse.
4. **Décider d'une restauration** seulement si les données sont perdues ou corrompues. Vérifier alors : la copie à utiliser (date, empreinte), une destination séparée, et que la base actuelle, même abîmée, est conservée.
5. **Contrôler après.** Connexion, lecture et écriture d'un ticket, ticket témoin relu. Noter la fenêtre de perte et le temps écoulé, puis les comparer aux objectifs RPO et RTO fixés avant l’incident.

**Passer le relais.** Si la cause reste inconnue après une vérification qui tranche, si des données risquent d'être perdues, ou si un secret apparaît : arrêter toute modification et consigner les faits. Le propriétaire du laboratoire décide de la suite. Aucune astreinte ni contact externe n'est prévu par ce projet.

## Restaurer la base

Principe retenu au [registre](architecture.md#décisions-retenues), détaillé dans l'[exercice 11](apprentissage/11-sauvegarde-reprise.md) :

1. Prendre la copie `pg_dump` la plus récente sur l'hôte, et vérifier son empreinte `sha256`.
2. Vérifier qu'elle est lisible : `pg_restore --list`.
3. La restaurer dans une **base vide**, sur une cible séparée de la base actuelle, avec `pg_restore --no-owner`, en utilisant les outils de PostgreSQL 17.
4. Faire pointer l'API vers cette base, puis contrôler `/health/ready` et relire le ticket témoin dans l'interface.
5. Seulement ensuite, décider du sort de l'ancienne base.

Une restauration remet les données au point de la dernière sauvegarde exploitable. L'objectif RPO de 24 heures n'est atteint que si une sauvegarde récente a réussi et est exploitable ; une copie manquée ou corrompue peut accroître la perte. Mesurer l'âge du point de restauration au moment de la panne et les données manquantes, puis comparer au RPO. Avant de modifier la cible, confirmer explicitement l'identité de la base, son caractère isolé, la version des outils, l'intégrité de l'archive et le retour arrière. Redéployer une image ne restaure jamais un ticket.

## Ce qui a été démontré

Le 18 novembre 2026, sur le poste de développement, avec deux conteneurs PostgreSQL 17.12 jetables : une base de 501 lignes sauvegardée par `pg_dump`, son empreinte relevée, restaurée par `pg_restore` dans une base vide d'un autre serveur, la ligne témoin retrouvée, la source intacte, le tout en 0,49 seconde. Les sorties sont reproduites dans la fiche Notion de l'exercice 11. Cette démonstration valide la méthode, pas la reprise d'OpsDesk.

## Historique de la version 1

Le 3 novembre 2026, un script de la version 1 a restauré la base dans une application et des volumes neufs, et relu un ticket à l'identique : 10,769 s puis 10,969 s. Les rapports sont conservés dans [`legacy/evidence/recovery-history-20261103T135154Z.json`](../legacy/evidence/recovery-history-20261103T135154Z.json) et [`legacy/evidence/recovery.json`](../legacy/evidence/recovery.json). Ils concernent la v1 et ne valent pas pour la v2.
