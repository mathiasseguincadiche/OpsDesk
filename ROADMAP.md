# Feuille de route technique — OpsDesk Architecture V3

**Conception validée le 25 novembre 2026 ; infrastructure non réalisée et non vérifiée.** Application V2 inchangée ; preuves dans [STATUS](STATUS.md).

| Phase | Livraison attendue | Contrôle de passage |
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

Chaque phase d’infrastructure est prévue, non vérifiée. Le parcours utilise exclusivement Fedora et les trois VM prévues. srv-ops sert aux fondamentaux avant sa prise en charge par Terraform ; ne pas la dupliquer ni supprimer le réseau partagé. Pour la reconstruction, privilégier srv-k3s après contrôle des dépendances, du plan et des sauvegardes. Une sauvegarde initiale et un test de restauration précèdent toute modification risquée, sans attendre la phase 9. La première installation utilise des images identifiées ; les nouvelles versions sont ensuite testées sur K3s avant promotion. La CI actuelle qualifie le socle, sans publication ni déploiement. Aucun runner permanent lié au dépôt public sur Fedora. Les exercices, installations, corrigés et preuves personnelles restent dans Notion. Les solutions sont construites progressivement par l’apprenant.

[Plan V3](docs/architecture-v3-deploiement.md) · [ADR](docs/adr/README.md) · [Flux](docs/architecture-v3-flux.md) · [État](STATUS.md)
