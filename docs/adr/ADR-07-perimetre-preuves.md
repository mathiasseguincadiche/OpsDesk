# ADR-07 — Périmètre de validation et publication maîtrisée

**Statut : validé en conception (Architecture V3).**

## Décision
L'architecture cible est distincte du socle applicatif déjà testé. Les fonctionnalités d'infrastructure ne sont considérées comme réalisées que lorsqu'une preuve de déploiement, de sécurité et de restauration est disponible.

## Répartition documentaire
GitHub public contient le code, les contrats applicatifs, le schéma global, les principes de conception et les preuves non sensibles. Le dossier personnel Notion conserve le schéma détaillé, les paramètres réseau, les procédures d'administration et le plan d'exploitation complet.

## Vérification prévue
Qualifier successivement la conformité des configurations, la reproductibilité, la restauration et la supervision. Publier seulement des captures et des traces assainies.

## Limites
Les sources d'une version antérieure peuvent subsister dans l'historique Git et les anciennes PR ; les modifications de la branche principale ne les effacent pas.
