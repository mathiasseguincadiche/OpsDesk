# ADR-01 — Terraform sur Fedora, libvirt et état protégé

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
Le premier plan hébergeait Terraform sur `srv-admin`, avec un bootstrap externe et une clé `qemu+ssh` donnant accès à libvirt sur Fedora. Cela créait une dépendance circulaire et multipliait les accès sensibles.

## Décision
- Terraform et le provider libvirt s'exécutent exclusivement sur l'hôte Fedora 45 via `qemu:///system`, avec des permissions contrôlées.
- Terraform décrit le réseau `opsdesk-lan` et les trois VM Rocky (`srv-admin` .5, `srv-app` .10, `srv-k3s` .20), cloud-init, disques système et volumes de données séparés.
- `srv-admin` héberge Ansible, Git et k6, sans clé libvirt ni moteur Terraform nécessaire.
- Le `terraform.tfstate`, les plans susceptibles de contenir des secrets et les fichiers de variables sensibles sont exclus de Git. Un seul opérateur modifie le state à la fois ; copie chiffrée externe et restauration de copie obligatoires.

## Alternatives étudiées
- Terraform dans `srv-admin` via `qemu+ssh` : écarté pour éviter le bootstrap circulaire et l'accès à l'hyperviseur dans une VM.
- Backend Terraform distant : complexité injustifiée pour un laboratoire à opérateur unique ; à réexaminer en cas d'équipe.

## Vérification de réception prévue
- Plan et `apply` contrôlés ; second `terraform plan` sans dérive ; vérification des IP et disques ; restauration du state depuis une copie chiffrée, sur environnement isolé.
- Prouver qu'une recréation de VM ne détruit jamais un volume de données conservé.

## Risques et retour arrière
Les privilèges libvirt restent élevés ; toute destruction, modification du réseau ou réinitialisation de disque exige un accord séparé. Retour arrière par sauvegarde du state et réconciliation, jamais `destroy` aveugle.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
