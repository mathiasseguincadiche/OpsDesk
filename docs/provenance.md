# Provenance des éléments du dépôt

Ce document dit d'où vient chaque partie du dépôt, et ce qui revient à la réalisation personnelle. Mise à jour : 18 novembre 2026.

## Qui a fait quoi

| Ensemble | Origine | Statut |
| --- | --- | --- |
| Application v2 : `backend/`, `frontend/`, tests, Dockerfiles, `compose.yaml`, `scripts/smoke.py` | Produits avec l'aide d'un assistant d'IA, à partir d'une première version elle-même générée par IA | Fournis : support de l'apprentissage, pas une réalisation personnelle à mettre au CV comme développement |
| Composants tiers : Python, FastAPI, SQLAlchemy, psycopg, React, Vite, Tailwind CSS, Recharts, nginx, PostgreSQL | Projets libres, sous leurs propres licences | La licence MIT du dépôt ne les remplace pas |
| Documentation produit : README, architecture, référence technique, contrat applicatif | Rédigée avec l'aide d'un assistant d'IA, relue contre le code | Décisions validées par le propriétaire du projet |
| Schémas v2 (`docs/diagrams/`) | Dessinés pour le projet avec Draw.io, sans logo de produit | Sources `.drawio` et exports SVG versionnés |
| Infrastructure : laboratoire, Terraform, Ansible, fichier Compose de production, CI, K3s, supervision, sauvegarde | **À concevoir, écrire, exécuter et expliquer soi-même** | Réalisation personnelle, à prouver exercice par exercice ; rien n'est réalisé à ce jour |
| Données de démonstration | Fictives : noms, adresses et tickets inventés | Aucune donnée réelle |

### Illustration de couverture GitHub

La bannière `docs/images/opsdesk-hero.svg` est une identité graphique
éditoriale créée avec assistance IA pour faciliter la lecture. Elle ne
représente ni une VM réellement créée ni le fonctionnement vérifié
de l'architecture. Les diagrammes techniques conservent leurs
sources `.drawio` et leurs exports SVG.

## La version 1

La version 1 (application Flask, sans authentification), ses tests, ses preuves datées, ses schémas et ses documents d'infrastructure sont conservés dans [`legacy/`](../legacy/) :

- [`legacy/evidence/`](../legacy/evidence/) : rapports bruts du 3 novembre 2026 ;
- [`legacy/diagrams/`](../legacy/diagrams/README.md) : schémas v1 et provenance de leurs logos (simple-icons, sous licences CC0, CC BY 3.0 et CC BY-SA 4.0 selon le logo) ;
- [`legacy/docs/`](../legacy/docs/README.md) : CI, infrastructure, livraison, triage de sécurité et versions de la v1.

Les fichiers d'infrastructure de la v1 (Dockerfile, Terraform et Ansible locaux, manifestes Kubernetes, CI) ne sont plus dans le dépôt depuis le 4 novembre 2026 ; ils n'ont jamais créé de machine, de cluster ni de ressource cloud.

## Une source de vérité par sujet

| Question | Source de vérité | Quand la mettre à jour |
| --- | --- | --- |
| Découvrir le projet | [README](../README.md) et [index documentaire](README.md) | Quand le périmètre ou l'état change |
| Comprendre un choix | [Registre des décisions](architecture.md#décisions-retenues) | Après une vraie décision ; une raison inconnue n'est pas inventée |
| Héberger ou exploiter l'application | [Contrat applicatif](contrat-applicatif.md) et [référence technique](reference-technique.md) | À chaque évolution de l'API ou de la configuration |
| Formation personnelle | [Centre Notion](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) | Hors du dépôt public ; cours, exercices et évaluations dans Notion |
| Savoir ce qui est fait et vérifié | [STATUS.md](../STATUS.md) | À chaque nouveau contrôle, daté |
| Lire une preuve | [Preuves](preuves.md) | Quand la méthode change |
| Agir en incident | [Reprise](reprise.md#triage-court-avant-une-reprise-personnelle) | Après chaque évolution effective de procédure |

Avant de déplacer un fichier, recenser ses liens entrants.

## Vocabulaire

- **Hôte** : le poste Fedora. **Invité** : une des trois VM Rocky Linux (`srv-admin`, `srv-app`, `srv-k3s`).
- **Application** : le programme fourni. **Infrastructure personnelle** : ce que l'on construit soi-même. **Référence historique** : un essai daté de la version 1.
- **Réalisé** : l'élément existe. **Vérifié** : un contrôle daté et traçable l'a confirmé. **L3** : une tâche nouvelle réussie et vérifiée séparément.
