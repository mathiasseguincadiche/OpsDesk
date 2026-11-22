# ADR-07 — Périmètre Architecture V2 et validation par preuves

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
Le rapport initial appelait la cible « Infrastructure V1 ». Cette architecture **remplace l'ancienne cible** : l'utilisateur l'a validée sous le nom « Architecture V2 ». L'application OpsDesk V2 est déjà testée ; les VM restent à créer.

## Décision
- Distinguer strictement **Application OpsDesk V2** (socle existant) de **Architecture OpsDesk V2** (choix adoptés) et des **phases 0 à 6** (travaux non encore vérifiés sur Fedora/Rocky).
- Chaque phase est un lot avec livrables, contrôle positif, contrôle négatif, conditions de refus et preuve datée. CI documentaire/applicative ≠ recette de déploiement réel.
- Épreuves finales : (1) conformité et idempotence, (2) reconstruction jetable, (3) restauration externe et mesure RPO/RTO, (4) supervision/charge/alertes.
- GitHub conserve code, architecture, IaC, runbooks et preuves ; Notion conserve cours, exercices, corrigés, évaluations et **Installation des outils**. Sources des schémas en Draw.io + exports SVG synchronisés.
- Les durcissements indispensables (TLS, contrôle d'images, gestion de secrets, sauvegardes chiffrées) ne sont pas repoussés à une hypothétique V3.

## Alternatives étudiées
- Déployer toutes les briques d'un coup : refusé pour conserver une causalité claire.
- Déclarer une phase réalisée à partir d'un plan, d'un schéma ou de la réussite d'une PR : refusé.

## Vérification de réception prévue
- Dossiers et ADR liés aux contrôles du plan et à la matrice des flux.
- Quatre épreuves finales validées sur l'environnement réel avec SHA, date, cible, commande, résultat et limite.
- Aucun résultat personnel inventé ni duplication des contenus pédagogiques dans GitHub.

## Risques et retour arrière
L'accord de conception autorise une PR documentaire, **pas** un terraform apply ni une opération destructive. Une nouvelle décision majeure donnera lieu à une nouvelle version d'ADR et conservera les preuves antérieures.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
