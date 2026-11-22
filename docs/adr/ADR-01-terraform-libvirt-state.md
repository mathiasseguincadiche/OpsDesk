# ADR-01 — Provisionnement local et état Terraform

**Statut : validé en conception (Architecture V2).** La réalisation dans le laboratoire reste à qualifier.

## Décision
L'hôte de virtualisation exécute directement Terraform et le provider adapté. L'administration des machines reste séparée du provisionnement de l'hyperviseur. L'état de l'infrastructure, potentiellement sensible, est conservé hors du dépôt public et protégé.

## Justification
Ce découplage évite de donner à une machine virtuelle les privilèges de l'hyperviseur et limite les dépendances circulaires au démarrage.

## Alternatives
Un pilotage de l'hyperviseur depuis une VM et un backend d'état distant ont été étudiés, mais ne sont pas nécessaires au laboratoire mono-opérateur.

## Vérification prévue
Création reproductible, plan sans dérive inexpliquée, contrôle des permissions et restauration de l'état à partir d'une sauvegarde protégée.

**Périmètre public :** les accès précis, la topologie interne, les chemins, les identités et la procédure de reprise sont conservés dans la documentation personnelle.
