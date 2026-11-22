# OpsDesk — Architecture V2 : plan de déploiement (phases 0 à 6)

**Accepté en conception le 22 novembre 2026. Infrastructure non déployée sur Fedora/Rocky.** Ce plan succède au plan historique « infrastructure V1 » du rapport Gemini. Il ne modifie pas la version de l'application OpsDesk V2.

[Registre des ADR](adr/README.md) · [Matrice des flux](architecture-v2-flux.md) · [ROADMAP](../ROADMAP.md) · [État des contrôles](../STATUS.md)

## Hypothèses d'implantation à vérifier

- **Hôte :** Fedora 45, KVM/libvirt ; mesurer les ressources disponibles avant de créer les VM.
- **Dimensionnement provisoire :** `srv-admin` 2 vCPU / 2 Go ; `srv-app` 2 vCPU / 4 Go plus disque de données séparé de 10 Go ; `srv-k3s` 4 vCPU / 6 Go, stockage à mesurer pour K3s et Prometheus. Ces valeurs ne sont pas des garanties de performance.
- **Réseau :** NAT `opsdesk-lan` /24, Fedora `.1`, `srv-admin` `.5`, `srv-app` `.10`, `srv-k3s` `.20`.
- **Produit :** application V2, trois images GHCR privées (API, frontend, PostgreSQL), digests immuables, CI applicative et Trivy existants conservés.
- **Sécurité :** TLS pour tous les accès navigateur serveur, Vault pour les secrets, Borg chiffré sur disque externe et destination de réception avec compte SSH restreint.
- **Continuité :** sept archives quotidiennes initiales à 02:00 (fuseau du timer explicitement défini), objectifs RPO ≤24 h / RTO <30 minutes **non encore prouvés**.
- **Interdiction générale :** la validation de la conception n'autorise ni `terraform apply` sur le poste, ni `destroy`, ni reformatage, ni migrations de données existantes, ni ouverture de ports, ni dépense cloud.

## Phase 0 — Préparer les fondations Fedora

**Livrables :** réseau NAT libvirt, stockage séparé, image cloud Rocky vérifiée, Terraform/provider libvirt local, protection du `terraform.tfstate`, conventions de variables/secrets et compte de réception de sauvegardes.

**Gate 0 :** réseau et résolution vérifiés, capacité hôte mesurée, image Rocky contrôlée, state exclu de Git, accès de récupération validé et restauration d'une copie chiffrée du state testable. Ne pas modifier les VM existantes sans périmètre validé.

**Preuves attendues :** commandes libvirt, manifestes de ressources, rapport de sécurité de l'état. **Statut initial : prévu / non vérifié.**

## Phase 1 — Créer `srv-admin` avec Terraform sur Fedora

**Livrables :** VM Rocky à `.5`, cloud-init, identité SSH dédiée, Ansible, Git, k6, inventaire. Aucune clé libvirt hébergée dans `srv-admin`.

**Gate 1 :** plan Terraform sans dérive inexpliquée après création, SSH par clé opérationnel, compte root/mot de passe refusés une fois la récupération assurée, SELinux Enforcing, firewalld/chrony actifs et outils disponibles. **Statut : prévu / non vérifié.**

## Phase 2 — Provisionner et durcir `srv-app` / `srv-k3s`

**Livrables :** VM Rocky `.10` et `.20`, disque de données distinct sur `srv-app`, comptes Ansible, DNS, accès SSH, durcissement OS, configurations SELinux/firewalld et ressources systèmes.

**Gate 2 :** communications permises et refusées vérifiées depuis plusieurs origines, droits et volumes contrôlés, second passage Ansible `failed=0` et sans changement inattendu, tests de récupération console disponibles. **Statut : prévu / non vérifié.**

## Phase 3 — Livrer l'application via GHCR et HTTPS

**Livrables :** pipeline de publication distinct des tests, trois images GHCR privées et manifeste de digests, Compose de **serveur** distinct de `compose.yaml` local, déploiement Vault avec fichiers secrets, CA/certificat de laboratoire, frontend HTTPS et migrations Alembic contrôlées.

**Gate 3 :** les trois digests déployés correspondent au manifeste ; navigateur reconnaît le certificat et envoie un cookie `Secure` ; connexion, ticket et déconnexion fonctionnent ; ports API :8000 et PostgreSQL :5432 restent inaccessibles depuis l'hôte ; métriques seulement sur chemin dédié autorisé. Ne jamais migrer une base existante sans sauvegarde/audit. **Statut : prévu / non vérifié.**

## Phase 4 — Sauvegardes, Borg et preuve de reprise

**Livrables :** timer systemd `pg_dump -Fc`, sept sauvegardes quotidiennes, compte de transfert incapable de supprimer les anciennes copies, dépôt hôte de réception, archive Borg **sur disque externe chiffré**, state Terraform récupérable et dispositif de protection des clés.

**Gate 4 :** le compte de réception ne peut ouvrir de shell, lire d'autres répertoires ou détruire des sauvegardes ; copie externe récupérée et déchiffrée ; `pg_restore` dans une base **isolée**, ticket témoin et Alembic contrôlés, RPO/RTO mesurés et comparés aux objectifs. Tester aussi le cas du disque indisponible. **Statut : prévu / non vérifié.**

## Phase 5 — Installer K3s, observabilité et copie d'essai

**Livrables :** K3s mono-nœud sur `srv-k3s`, Traefik HTTPS, namespaces `monitoring` et `essai`, ResourceQuota/LimitRange, trois images par digests sur copie **indépendante**, Prometheus avec scrape 15 s, rétention cible 15 j / 5 Go, Grafana Alerting via SMTP et scénarios k6.

**Gate 5 :** CoreDNS, ingress, métriques et quotas fonctionnent sous SELinux Enforcing/firewalld ; deux alertes se déclenchent et sont reçues par e-mail ; k6 ne cible **que** la copie et ne dégrade ni le principal ni `monitoring`. **Statut : prévu / non vérifié.**

## Phase 6 — Quatre épreuves de qualification finale

| Épreuve | Opération sur cible contrôlée | Résultat à démontrer |
| --- | --- | --- |
| 1. Conformité et idempotence | Second `terraform plan`, deuxième passage Ansible, SELinux et scans de ports positifs/négatifs | Pas de dérive, permissions correctes, refus réseau effectifs |
| 2. Reconstruction | Recréer une **cible jetable**, sans toucher au disque PostgreSQL actif | Infra/services recréés aux mêmes digests sans correctifs SSH manuels |
| 3. Reprise | Restaurer une sauvegarde Borg externe dans une base séparée | Tickets et schéma retrouvés, RPO et RTO **mesurés** |
| 4. Observabilité et charge | Test k6 sur `essai` et deux scénarios d'alertes maîtrisés | Métriques, seuils et notifications reçues sans dégradation du principal |

**Gate 6 :** les quatre épreuves disposent d'une preuve datée et vérifiable. Pas de suppression volontaire d'une base contenant des données à conserver. **Statut : prévu / non vérifié.**

## Règle de passage entre les phases

1. Produire du code Terraform/Ansible/K3s limité à une phase et les tests statiques correspondants, par PR séparée.
2. Relancer la CI sur le bon commit ; distinguer les vérifications de fichiers des essais de terrain.
3. Avant chaque commande à impact, vérifier la cible et obtenir une autorisation distincte.
4. Exécuter sur Fedora/Rocky, documenter commande, date, commit, cible, sortie, négatifs et limites.
5. Consigner dans `evidence/infrastructure/` et **STATUS** uniquement les contrôles effectivement réalisés ; laisser la phase non vérifiée en cas d'échec.
6. Mettre à jour ensemble les schémas Draw.io et SVG dans une PR graphique distincte avec inspection du rendu.

**Cette PR documentaire n'exécute aucun provisioning et ne certifie aucune des phases 0 à 6.**
