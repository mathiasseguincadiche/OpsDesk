# ADR-02 — Livraison GHCR privée, trois images et digests immuables

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
Le dépôt dispose déjà de CI applicative, documentaire et Trivy, mais pas d'une chaîne de livraison vers les trois VM. Le réseau NAT ne doit recevoir aucune connexion entrante de GitHub Actions.

## Décision
- GitHub Actions construit et publie sur GHCR **privé** les trois images : API, frontend et PostgreSQL dérivée. Ne pas reconstruire indépendamment sur chaque VM.
- Tag lisible lié au SHA Git et, si justifié, version sémantique ; les déploiements utilisent exclusivement `image@sha256:...`, pas `latest`.
- Un manifeste de livraison versionné associe SHA, les trois digests, résultats CI et date. Ansible initie l'installation ; `srv-app` et K3s téléchargent les images en HTTPS **sortant**.
- Credentials GHCR lecture seule, distincts de l'écriture CI, distribués hors Git par Vault ; imagePullSecret K3s à durée et droits contrôlés.

## Alternatives étudiées
- Build local par VM : dérive et absence de traçabilité.
- GHCR public : facilite les pulls mais ne correspond pas au choix de confidentialité.
- Déploiement GitHub Actions par SSH entrant : incompatible avec le LAN NAT.

## Vérification de réception prévue
- Publier les trois digests après tests et contrôle HIGH/CRITICAL ; déployer une même version sur Compose et sur la copie K3s ; vérifier les références réelles.
- Tester une mise à jour puis un retour arrière vers un manifeste connu, sous réserve de compatibilité du schéma Alembic.

## Risques et retour arrière
Les packages privés nécessitent un cycle de rotation des jetons. La promotion est bloquée si la CI échoue ; un scan vert n'est pas une homologation de l'ensemble de l'infrastructure.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
