# Registre public des décisions — OpsDesk Architecture V3

**Sept décisions validées en conception.** Elles décrivent les choix d'ingénierie et leurs compromis sans révéler les paramètres précis du laboratoire.

| Décision | Sujet |
| --- | --- |
| [ADR-01](ADR-01-terraform-libvirt-state.md) | Provisionnement local et état Terraform protégé |
| [ADR-02](ADR-02-ci-ghcr-digests.md) | CI, registre privé et livraison immuable |
| [ADR-03](ADR-03-administration-os.md) | Administration cloisonnée et durcissement Linux |
| [ADR-04](ADR-04-reseau-tls.md) | Réseau privé, HTTPS et isolation des services |
| [ADR-05](ADR-05-k3s-observabilite.md) | Kubernetes : copie d’essai et supervision |
| [ADR-06](ADR-06-sauvegardes-secrets.md) | Secrets, sauvegardes et restauration |
| [ADR-07](ADR-07-perimetre-preuves.md) | Frontières de validation et publication responsable |

## Compléments publics

- [Schéma global V3](../diagrams/architecture-globale-v3.svg) et [source Draw.io](../diagrams/architecture-globale-v3.drawio).
- [Principes de flux](../architecture-v3-flux.md) : frontières et politiques générales.
- [Phases 0 à 10](../architecture-v3-deploiement.md) : enchaînement et preuves sans procédures sensibles.
- [Statut des réalisations](../../STATUS.md).

## Répartition des informations

GitHub publie le code applicatif, les preuves expurgées, les principes des ADR et la **vue globale**. Le détail d'exploitation, le schéma technique personnel, les adresses et règles réseau, les sauvegardes et les inventaires sont conservés séparément dans un espace Notion personnel **sans lien public**.

Une architecture validée en conception n'est pas un laboratoire déployé ou audité.
