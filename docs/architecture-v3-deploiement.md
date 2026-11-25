# OpsDesk — Architecture V3 : plan public de réalisation

**Conception validée le 25 novembre 2026 ; laboratoire non qualifié.** Remplace le [plan V2 historique](architecture-v2-deploiement.md).

| Phase | Objectif | Contrôle attendu |
| --- | --- | --- |
| 0 — Fedora | Préparer KVM/libvirt, Git, outils et stockage | Versions, accès libvirt, capacité |
| 1 — Fondamentaux | Première installation manuelle de srv-ops, réseau, SSH | Diagnostic, inventaire et compréhension des ressources |
| 2 — Provisionnement | Terraform : reprise ou recréation contrôlée de srv-ops avant service, puis srv-app et srv-k3s ; cloud-init, outputs filtrés | Plan relu, apply, absence de dérive, SSH |
| 3 — Configuration | Ansible depuis Fedora, durcissement et rôles | Refus/accès, SELinux, second passage changed=0 |
| 4 — Service | Compose serveur HTTPS, migrations, persistance | Parcours métier, TLS, isolation API/DB |
| 5 — Observabilité | Compose sur srv-ops, métriques et alertes | Collecte restreinte, deux e-mails reçus |
| 6 — Livraison | CI, GHCR privé, images par digest | Artefact qualifié, promotion et rollback |
| 7 — Kubernetes | Copie d’essai et données distinctes | Probes, quotas, TLS |
| 8 — Performance | k6 borné depuis Fedora vers srv-k3s | p95, débit, erreurs, ressources, arrêt |
| 9 — Exploitation | Maintenance, rollback, Borg | Restauration isolée, RPO/RTO |
| 10 — Autonomie | Reconstruction contrôlée d’une VM existante et incident inédit | Preuves datées, justification et contrôle séparé |

## Chaîne de contrôle

Préparer Fedora → Terraform init/validate/plan → revue → apply approuvé → cloud-init minimal et SSH prêt → outputs non sensibles filtrés et inventaire généré hors Git → Ansible (syntaxe, cibles, configuration, vérification) → déploiement et preuves. Les deux outils restent rejouables séparément, sans provisioner local-exec obligatoire. State, plans, clés et inventaire réel privés. Vérifier les clés hôtes SSH par une source de confiance.

## Conditions de passage

Le laboratoire lui-même sert à apprendre : aucune quatrième VM n’est prévue. La première VM, srv-ops, est créée manuellement pour comprendre KVM, le réseau et SSH ; avant d’y installer la supervision, inventorier ses ressources puis choisir une reprise Terraform supportée ou une recréation contrôlée de cette même VM, sans doublon ni suppression du réseau partagé. Préférer une recréation à ce stade si la reprise est incertaine. Pour l’exercice de reconstruction, privilégier srv-k3s : plan ciblé relu, données d’essai identifiées, sauvegardes et procédure de reprise vérifiées, arrêt annoncé dans le laboratoire. Ne pas toucher aux autres VM, au réseau partagé ni au principal. Les opérations destructives nécessitent une décision explicite. Sauvegarde restaurable avant tout changement risqué ; distinguer rollback d’image et compatibilité des migrations. Limiter k6 et arrêter si l’hôte ou le principal se dégrade.

Quatre épreuves : configuration idempotente ; reconstruction contrôlée de srv-k3s (ou d’une autre VM existante si justifiée) ; restauration indépendante avec ticket témoin et RPO/RTO ; supervision, notifications et charge isolée. L’autonomie exige un cas inédit et un contrôle séparé.

[ADR](adr/README.md) · [Flux](architecture-v3-flux.md) · [État](../STATUS.md)
