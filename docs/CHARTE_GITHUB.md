# Charte universelle — GitHub pour projets InfraOps

[← Documentation OpsDesk](README.md) · [README du projet](../README.md) · [Contribuer](../CONTRIBUTING.md) · [État vérifié](../STATUS.md)

## 1. Mission et principes

Un dépôt GitHub est à la fois **une porte d'entrée lisible, un ouvrage d'ingénierie exploitable et un ensemble de preuves traçables**. Il ne sert pas à reproduire le cours personnel Notion. Un visiteur doit comprendre la finalité en dix secondes, essayer le service sans risque, identifier le périmètre de l'auteur, examiner les compromis et retrouver les preuves.

**Ne jamais sacrifier l'exactitude pour la présentation.** La structure dépend du domaine : réseau, sauvegarde, service conteneurisé ou laboratoire IaC peuvent partager une identité éditoriale sans utiliser les mêmes schémas ni les mêmes dossiers.

## 2. Identité et présentation du README

Ordre par défaut, adaptable au contexte :

1. **Signature visuelle** : visuel sobre, accessible, avec texte alternatif. Sa nature éditoriale ou technique est explicite.
2. **Accroche** : projet, métier, problème résolu et environnement en trois à cinq lignes.
3. **Accès immédiats** : découvrir, essayer, architecture, preuves, documentation.
4. **Aperçu vérifié** : vraie capture datée, environnement et données fictives si nécessaire.
5. **Démarrage rapide** : outils, commandes, résultat attendu, vérification, arrêt/retour arrière.
6. **Architecture** : petite vue de présentation et lien vers les détails.
7. **Périmètre et réalisations** : application fournie, contribution personnelle et objectifs futurs distincts.
8. **Documentation par besoin** : installer, comprendre, opérer, dépanner, auditer, reproduire.
9. **Contribution, sécurité, licence, provenance** : politiques et preuves.

Les tableaux servent à **comparer**, pas à remplir les blancs. Les badges de CI ne sont affichés qu'avec un workflow réel et un lien vers son état. Ne pas afficher un badge PASS, production, coverage ou « secure » sans contrôle correspondant.

### Design

- Identité cohérente : bleu nuit, bleu acier, orange discret pour OpsDesk. Autres projets : palette propre, mêmes conventions d'accessibilité.
- Titres courts, hiérarchie H1/H2/H3, paragraphes aérés, exemples de commandes réellement utiles.
- Captures adaptées aux thèmes clair/sombre par `<picture>` ; largeur responsive, légende et alt explicites.
- La couverture `docs/images/opsdesk-hero.svg` est une **illustration graphique** autonome : elle ne représente ni une architecture validée ni un résultat de déploiement.
- Un **schéma d'architecture ou pédagogique**, à la différence d'une simple bannière, possède une source `.drawio` et un export `.svg` cohérents, avec un titre, une légende, des flux exacts et les responsabilités. L'export SVG vient du schéma source.
- Éviter les animations gênantes, les emojis systématiques, les titres en majuscules, les graphiques décoratifs et les dépendances à un CDN tiers pour les visuels importants.
- Vérifier les rendus **GitHub Web clair/sombre et mobile** : le lint du SVG ne les démontre pas.

## Contrat de lecture avant publication

Une correction rédactionnelle doit résoudre une difficulté observée, pas allonger un fichier pour elle-même. Suivant le besoin, adopter l'ordre **question du lecteur → mécanisme → exemple distinct → limites → preuve ou vérification**. Une procédure conserve explicitement cible, prérequis, droits, risques, interprétation du résultat et retour arrière.

Tester au moins quatre parcours : **découverte** (finalité et périmètre), **apprentissage** (comprendre avant d'agir), **exploitation** (trouver rapidement un diagnostic) et **revue technique** (retrouver les choix et leurs compromis). Les fichiers GitHub doivent rester intelligibles sans accès au centre Notion ; les énoncés ne fournissent pas les solutions de l'infrastructure personnelle.

Une CI verte vérifie les contrats qu'elle exécute ; elle ne certifie ni la qualité pédagogique, ni un rendu GitHub mobile, ni une VM réellement déployée.

## 3. Architecture documentaire

| Besoin | Source de référence |
| --- | --- |
| Découvrir en deux minutes | `README.md` |
| Trouver un document | `docs/README.md` |
| Comprendre les responsabilités et les compromis | `docs/architecture.md`, contrat et ADR |
| Démarrer et préparer les outils | `docs/demarrage.md`, laboratoire, installation |
| Exploiter, diagnostiquer et rétablir | Référence technique, exploitation, reprise et runbooks |
| Comparer une intention à la réalité | `STATUS.md` + preuves datées dans `evidence/` |
| Suivre les travaux non réalisés | `ROADMAP.md` |
| Comprendre la provenance des éléments | `docs/provenance.md` |
| Apprendre pas à pas et noter ses résultats personnels | Centre de formation Notion, distinct du dépôt public |

Une source de vérité par information ; les autres pages pointent vers elle au lieu de recopier un tableau de statut vite obsolète.

La documentation **doit conserver** sa section d'installation et préparation de l'environnement, les commandes annotées, la validation, le diagnostic, la sécurité et le retour arrière. Un dépôt n'est pas professionnel parce qu'il contient beaucoup de fichiers.

## 4. Les sept gabarits

| Famille | Template versionné |
| --- | --- |
| README projet | [README-PROJET.md](templates/README-PROJET.md) |
| Architecture et décisions | [ARCHITECTURE-ADR.md](templates/ARCHITECTURE-ADR.md) |
| Guide d'exploitation | [RUNBOOK.md](templates/RUNBOOK.md) |
| Preuve de réalisation | [PREUVE.md](templates/PREUVE.md) |
| Pull request | [PR GitHub](../.github/pull_request_template.md) |
| Issue / anomalie | [Formulaire d'anomalie](../.github/ISSUE_TEMPLATE/bug.yml) et [documentation](../.github/ISSUE_TEMPLATE/docs.yml) |
| Version et release notes | [RELEASE-NOTES.md](templates/RELEASE-NOTES.md) |

Ces modèles sont des **points de départ**, pas des documents factuels ni des comptes rendus de tests exécutés.

## 5. Un document technique complet

Pour une opération : **pourquoi** → contexte et cible → **prérequis** → **inventaire de l'existant** → installation conditionnelle → procédure expliquée → validation → dépannage → rollback → preuve.

Chaque commande significative indique : hôte/conteneur concerné, effet attendu, droits, arguments essentiels, risques, contrôle du succès, écarts possibles. Un exemple voisin est distingué de l'exercice personnel. Ne pas retirer les étapes d'installation sous prétexte que l'auteur dispose déjà des outils.

Pour une architecture : **vue de présentation** et **vue technique** différentes ; composants, frontières, flux, ports, données, erreurs, dépendances, variantes, décisions et hypothèses explicites.

## 6. Niveau de preuve et périmètre de CI

| Niveau | Ce que cela établit |
| --- | --- |
| Document/source présent | Un fichier existe dans la révision étudiée |
| Validation statique | Structure, syntaxe, liens ou conventions contrôlés |
| Tests CI d'un composant | Un comportement a été testé sur un runner identifié |
| Déploiement sur cible | Version effectivement installée sur une machine identifiée |
| Service et données vérifiés | Scénario métier, persistance, permissions ou alerte réellement testés |
| Restauration / incident | Reprise et retour arrière mesurés et observés |

Une coche verte documentaire ne prouve pas un déploiement, ni l'autonomie de l'apprenant. Une capture d'écran doit indiquer version et environnement. Un rendu produit artificiellement n'est jamais une capture réelle.

Le workflow `Documentation quality (no deployment)` contrôle les liens, le SVG et les paires `.drawio` / `.svg`. Il ne remplace ni les tests applicatifs détaillés ni l'exercice personnel de CI/CD et publication GHCR.

## 7. Contributions et sécurité

- Une issue pour le besoin et sa reproduction ; une PR pour les changements et leurs risques.
- Permissions minimales, secrets absents du dépôt, dépendances suivies, pas d'auto-merge de vulnérabilités.
- Les modèles de contribution invitent à fournir les résultats réellement observés et les preuves, sans badge de compétence inventé.
- Une politique de sécurité ne certifie jamais qu'un laboratoire est prêt pour une exposition publique.
- Les notes privées Notion, niveaux personnels, mots de passe et captures non expurgées ne sont jamais copiés dans le portfolio.

## 8. Répartition des responsabilités dans l'atelier

| Agent | Contrôle GitHub |
| --- | --- |
| Chef des opérations | Cadrer la demande, les risques, la validation des PR |
| Architecte solutions | Conventions, arborescence, diagrammes, ADR |
| Rédacteur pédagogique | README, documentation, progression de lecture |
| Ingénieur DevOps | Scripts, tests, Git, CI/CD, reproductibilité et rollback |
| Sécurité | Secrets, exposition, dépendances, permissions, remédiations |
| Expert recherche | Versions réelles, documentation officielle et alternatives |
| Auditeur qualité | Vérification indépendante du diff, des liens, des preuves et des limites |

**La lecture n'autorise pas l'écriture.** Chaque changement proposé par OpenClaw devrait produire une PR avec diff, contrôles et approbation avant fusion. Ne pas autoriser les agents à pousser directement sur `main`.

## 9. Recette finale d'une refonte

- [ ] La page d'accueil est compréhensible sans défilement intensif.
- [ ] Les liens relatifs et les ancres utiles fonctionnent.
- [ ] Les fichiers source des schémas sont conservés avec leurs exports.
- [ ] Les captures et diagrammes sont lisibles en clair/sombre et sur téléphone.
- [ ] Les consignes d'installation et de diagnostic sont intactes.
- [ ] Les statuts et les preuves sont datés, périmétrés et cohérents.
- [ ] Le code utile n'a pas été déplacé inutilement.
- [ ] Les secrets/notes privées sont absents des changements.
- [ ] Les tests applicables sont passés sur la révision précise.
- [ ] Les limites de la CI, du rendu et des tests réels sont explicites.

**Une recette statique verte n'est pas une recette graphique native.** Contrôler le rendu GitHub séparément.