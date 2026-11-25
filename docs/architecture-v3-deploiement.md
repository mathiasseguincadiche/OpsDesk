# OpsDesk — Architecture V3 : plan public de réalisation

**Conception validée le 25 novembre 2026 ; laboratoire non qualifié.** Remplace le [plan V2 historique](architecture-v2-deploiement.md).

| Phase | Objectif | Contrôle attendu |
| --- | --- | --- |
| 0 — Fedora | Préparer KVM/libvirt, Git, outils et stockage | Versions, accès libvirt, capacité |
| 1 — Fondamentaux | VM pédagogique temporaire, réseau, SSH | Diagnostic et suppression hors cible |
| 2 — Provisionnement | Terraform, trois VM, cloud-init, outputs filtrés | Plan, apply, absence de dérive, SSH |
| 3 — Configuration | Ansible depuis Fedora, durcissement et rôles | Refus/accès, SELinux, second passage changed=0 |
| 4 — Service | Compose serveur HTTPS, migrations, persistance | Parcours métier, TLS, isolation API/DB |
| 5 — Observabilité | Compose sur srv-ops, métriques et alertes | Collecte restreinte, deux e-mails reçus |
| 6 — Livraison | CI, GHCR privé, images par digest | Artefact qualifié, promotion et rollback |
| 7 — Kubernetes | Copie d’essai et données distinctes | Probes, quotas, TLS |
| 8 — Performance | k6 borné depuis Fedora, VM temporaire optionnelle | p95, débit, erreurs, ressources, arrêt |
| 9 — Exploitation | Maintenance, rollback, Borg | Restauration isolée, RPO/RTO |
| 10 — Autonomie | Reconstruction jetable et incident inédit | Preuves datées, justification et contrôle séparé |

## Chaîne de contrôle

Préparer Fedora → Terraform init/validate/plan → revue → apply approuvé → cloud-init minimal et SSH prêt → outputs non sensibles filtrés et inventaire généré hors Git → Ansible (syntaxe, cibles, configuration, vérification) → déploiement et preuves. Les deux outils restent rejouables séparément, sans provisioner local-exec obligatoire. State, plans, clés et inventaire réel privés. Vérifier les clés hôtes SSH par une source de confiance.

## Conditions de passage

La VM manuelle est temporaire et hors cible Terraform. Pas de destruction du service pour un exercice. Les opérations destructives exigent revue et autorisation. Sauvegarde restaurable avant tout changement risqué ; distinguer rollback d’image et compatibilité des migrations. Limiter k6 et arrêter si l’hôte ou le principal se dégrade.

Quatre épreuves : configuration idempotente ; reconstruction jetable ; restauration indépendante avec ticket témoin et RPO/RTO ; supervision, notifications et charge isolée. L’autonomie exige un cas inédit et un contrôle séparé.

[ADR](adr/README.md) · [Flux](architecture-v3-flux.md) · [État](../STATUS.md)
