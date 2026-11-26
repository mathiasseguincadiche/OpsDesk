# ADR-03 — Administration cloisonnée et durcissement Linux

**Statut : validé en conception (Architecture V3).**

## Décision
Le contrôle Ansible est sur Fedora, séparé des workloads invités. SSH direct vers les trois VM, contrôle des clés hôtes, compte dédié, privilèges limités ; aucun bastion obligatoire. Git et Ansible Vault sont sur Fedora. srv-admin est dédié à l’administration et au diagnostic, à kubectl/Helm et à k6 ; il n’est pas un contrôleur Ansible. Les systèmes Linux sont gérés avec Ansible, des identités séparées, des privilèges minimaux et les mécanismes de sécurité natifs du système.

## Justification
Séparer administration et application limite les droits nécessaires à chaque fonction et favorise la reproductibilité du durcissement.

## Vérification prévue
Contrôler les accès autorisés et refusés, l'idempotence de la configuration, le maintien d'un accès de récupération et la supervision des changements.

**Périmètre public :** l'inventaire des comptes, les chemins d'administration, les clés, les règles pare-feu et les commandes de récupération sont conservés hors GitHub.
