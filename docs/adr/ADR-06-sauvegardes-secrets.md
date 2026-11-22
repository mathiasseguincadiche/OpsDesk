# ADR-06 — Ansible Vault, réception restreinte et sauvegardes Borg chiffrées

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
Le test de pg_dump/pg_restore sur runner prouve la restauration du socle, pas la protection contre perte de VM, ransomware ou panne de disque hôte. Un accès SSH à un compte personnel Fedora depuis `srv-app` est inacceptable.

## Décision
- Chiffrer les secrets versionnés avec **Ansible Vault**. Mot de passe de Vault et clés de récupération **hors Git et séparés des sauvegardes** ; utiliser *_FILE, droits/UID/GID et labels SELinux et `no_log` là où requis.
- Sauvegarde PostgreSQL `pg_dump -Fc` chaque jour à 02:00 dans le fuseau explicitement retenu ; sept points quotidiens comme rétention initiale, suivi de fraîcheur.
- Depuis `srv-app`, une clé de transfert ne peut que déposer dans `/var/backups/opsdesk/incoming` sur Fedora, sans shell interactif, lecture, suppression ni traversée du répertoire. La commande forcée SSH doit être **testée** ; ne pas combiner aveuglément `nologin` et `rrsync`.
- Un service distinct sur Fedora vérifie les dépôts et les archive dans **Borg chiffré sur disque externe** ; les droits de la VM ne permettent ni de modifier ni de supprimer ces archives. Sauvegarder aussi un état Terraform sensible chiffré et les manifestes nécessaires à la reconstruction.
- Objectifs **RPO au plus 24 h** et **RTO inférieur à 30 min** ; mesurer réellement ces temps lors d'une restauration depuis copie externe.

## Alternatives étudiées
- `~/sauvegardes` avec l'utilisateur personnel Fedora : refusé.
- Rsync vers le même disque sans seconde copie chiffrée : insuffisant.
- Gestionnaire de secrets additionnel : complexité non requise initialement.

## Vérification de réception prévue
- Refus de shell, suppression ou accès hors répertoire par l'identité backup.
- Borg chiffré sur support indépendant et déchiffrable avec clés récupérables ; restauration isolée PostgreSQL et vérification d'un ticket témoin.
- Test de restauration d'une copie du state, délai RPO/RTO mesuré et alerte si la sauvegarde vieillit.

## Risques et retour arrière
Le disque externe doit être réellement indépendant de l'hôte pour parer sa panne ; une copie reliée en permanence ne garantit pas l'immuabilité. Ne jamais effacer la base active pour un essai de reprise.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
