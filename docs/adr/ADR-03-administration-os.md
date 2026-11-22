# ADR-03 — SSH cloisonné, durcissement Rocky, SELinux et firewalld

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
Le laboratoire sépare l'hyperviseur, le pilotage et l'application. `srv-admin` concentre des privilèges d'administration et `srv-app` contient les données et secrets : une seule identité SSH partagée serait un risque de mouvement latéral.

## Décision
- Clés ed25519 distinctes par fonction : Fedora → `srv-admin`, Ansible depuis `srv-admin` → deux VM, et expédition de sauvegarde `srv-app` → compte restreint Fedora. Aucune clé `qemu+ssh` vers libvirt depuis `srv-admin`.
- Comptes dédiés, `sudo` explicitement borné et audité. Refuser root SSH et les mots de passe **après** validation d'un chemin de récupération par clé/console.
- Sur les trois VM, maintenir SELinux Enforcing, firewalld et chrony. Diagnostiquer les AVC et corriger les contextes plutôt que désactiver SELinux. Sur K3s, tester l'intégration `k3s-selinux`.
- Aucun humain dans le groupe `docker` sur `srv-app` ; actions Docker administratives via élévation contrôlée ou unités systemd. Vérifier UID/GID, droits de secrets, limites et rotation des journaux.

## Alternatives étudiées
- Clé unique pour tous les services : non retenue.
- Désactivation de SELinux/firewalld en cas d'échec : refusée.
- Administration libvirt depuis `srv-admin` : supprimée par ADR-01.

## Vérification de réception prévue
- `getenforce=Enforcing`, comptes vérifiés, refus SSH root/mot de passe, aucune appartenance humaine au groupe docker.
- Deuxième passage Ansible sans erreur ni changements inexpliqués, validation du fonctionnement réel des services et de leurs contextes SELinux.

## Risques et retour arrière
Conserver l'accès console libvirt pour récupérer une machine verrouillée. Ne jamais appliquer simultanément un durcissement SSH et la suppression du seul accès fonctionnel.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
