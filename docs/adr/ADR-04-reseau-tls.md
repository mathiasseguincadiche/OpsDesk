# ADR-04 — Réseau privé, HTTPS, frontières et ports

**Statut :** accepté en conception pour **OpsDesk Architecture V2** le 22 novembre 2026. **Exécution sur Fedora/Rocky : prévue, non vérifiée.**

> Un ADR décrit une décision, pas un résultat de déploiement. Les contrôles réalisés sont uniquement ceux étayés par [STATUS](../../STATUS.md).

## Contexte
L'ancien schéma montrait HTTP :8080 en accès navigateur et la possibilité d'exposer FastAPI :8000 pour les métriques. L'application utilise des cookies Secure en production : l'accès navigateur doit être HTTPS dès la mise en service serveur.

## Décision
- Conserver le NAT `opsdesk-lan` (`192.168.150.0/24`) : Fedora .1, `srv-admin` .5, `srv-app` .10, `srv-k3s` .20 ; réservations IP, DNS et synchronisation du temps vérifiés.
- HTTPS sur Nginx de `srv-app` et Traefik de la copie K3s dès la phase 3/5. CA locale dédiée, noms SAN corrects, confiance installée sur les navigateurs du laboratoire.
- PostgreSQL :5432 et API :8000 restent confinés aux réseaux conteneurs, **sans publication sur la VM**. Une passerelle dédiée peut exposer uniquement `/metrics` à Prometheus depuis .20, sur port de travail proposé :9180, sous filtrage effectif.
- Node exporter :9100 limité à .20 ; Grafana accédé par tunnel SSH via `srv-admin` sans publier :3000 ; n'ouvrir que les ports K3s réellement nécessaires au nœud unique.
- Vérifier les règles Docker, firewalld et nftables par tests réseau positifs et négatifs depuis plusieurs machines.

## Alternatives étudiées
- HTTP seul sur le LAN : conservé pour la démonstration locale 127.0.0.1, non retenu pour le déploiement serveur.
- Ouverture de :8000 uniquement pour `/metrics` : exposerait toutes les autres routes API, refusé.
- mTLS entre tous les conteneurs : non nécessaire au laboratoire initial.

## Vérification de réception prévue
- Connexion navigateur HTTPS et cookie Secure ; connexion/ticket/déconnexion fonctionnels.
- Depuis Fedora et `srv-admin`, API :8000 et DB :5432 refusés ; métriques :9180/:9100 refusées hors de la source .20 ; inspection de DNS, certificats, pare-feu et ingress.
- Aucun accès entrant public ou accès direct Grafana :3000.

## Risques et retour arrière
Les ports et noms sont des valeurs de conception à éprouver, pas des ports déjà ouverts. Ne pas supposer que firewalld bloque tous les ports publiés par Docker.

## Références et dépendances
[Registre des sept ADR](README.md) · [Matrice des flux V2](../architecture-v2-flux.md) · [Déploiement par phases 0 à 6](../architecture-v2-deploiement.md) · [État réel](../../STATUS.md)
