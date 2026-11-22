# Registre des décisions — OpsDesk Architecture V2

**Architecture V2 : validée en conception le 22 novembre 2026.** L'ancienne cible était appelée « infrastructure V1 » ; cette nouvelle architecture la remplace. **Application OpsDesk V2** désigne le socle existant : la version applicative et la version d'architecture ne sont pas interchangeables.

| ADR | Choix validé |
| --- | --- |
| [ADR-01](ADR-01-terraform-libvirt-state.md) | Terraform sur Fedora, libvirt et état protégé |
| [ADR-02](ADR-02-ci-ghcr-digests.md) | Livraison GHCR privée, trois images et digests immuables |
| [ADR-03](ADR-03-administration-os.md) | SSH cloisonné, durcissement Rocky, SELinux et firewalld |
| [ADR-04](ADR-04-reseau-tls.md) | Réseau privé, HTTPS, frontières et ports |
| [ADR-05](ADR-05-k3s-observabilite.md) | K3s, copie d'essai, Prometheus/Grafana et k6 |
| [ADR-06](ADR-06-sauvegardes-secrets.md) | Ansible Vault, réception restreinte et sauvegardes Borg chiffrées |
| [ADR-07](ADR-07-perimetre-preuves.md) | Périmètre Architecture V2 et validation par preuves |

## Compléments nécessaires

- [Matrice des flux V2](../architecture-v2-flux.md) : adresses, ports, origines autorisées, refus obligatoires.
- [Plan de déploiement V2](../architecture-v2-deploiement.md) : phases 0 à 6 et quatre épreuves finales.
- [Architecture applicative](../architecture.md) : fonctionnement du service déjà testé et distinction entre application et infrastructure.
- [État vérifié](../../STATUS.md) : seul document qui précise ce qui a été exécuté réellement.
- [Schémas Draw.io/SVG](../diagrams/README.md) : les exports actuels décrivent l'ancienne cible ; une **mise à jour graphique en paire source/export** est nécessaire avant de les présenter comme Architecture V2.

## Frontières de responsabilité

GitHub héberge produit, code d'infrastructure, décisions, procédures et preuves. Notion conserve les cours, exercices, corrigés, évaluations et « Installation des outils ». Aucun nouveau contenu pédagogique n'est importé dans GitHub.

**Aucune phase d'infrastructure n'est réputée déployée par la seule acceptation de ces ADR.** Le déploiement, les opérations destructives et les changements réseau réclament des autorisations et preuves distinctes.
