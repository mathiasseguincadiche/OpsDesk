# Journal des changements du dépôt

Ce registre retrace les changements documentaires, structurels et techniques **vérifiables dans Git**. Une modification du dépôt n'est pas une preuve de déploiement dans le laboratoire. Pour la qualification réelle, lire [STATUS.md](STATUS.md).

## Non publié

- Correction du périmètre V3 (26 novembre) : retour à la supervision Kubernetes avec Prometheus/Grafana et copie d’essai sur srv-k3s ; srv-admin pour l’administration, kubectl/Helm et k6. Terraform, Ansible, Vault et Git sur Fedora. Les entrées V3 antérieures ci-dessous sont historiques. Aucun déploiement réel.

- Finitions V3 : cohérence de la sauvegarde d’essai, du statut de conception et des visuels publics ; source Draw.io de présentation et contrôles de rendu natif. Aucun changement de l’application ni de la topologie.

- Simplification du parcours V3 : apprentissage sur Fedora et les trois VM définitives, première installation manuelle de srv-admin avant sa prise en charge Terraform, charge depuis Fedora et reconstruction contrôlée de srv-k3s. Aucune VM supplémentaire prévue ni déployée.

- Architecture d’infrastructure V3 validée en conception : pilotage Fedora Terraform/Ansible, cloud-init, inventaire généré, supervision srv-admin, K3s d’essai et k6 borné. Application V2 inchangée ; aucune qualification réelle.

- Correction de l'image API : inclure Alembic et ses révisions dans le runtime non-root, avec test de migration et démarrage en mode production sur base PostgreSQL séparée.

- API Python 3.13 Alpine (construction et exécution) : tests conservés, scan Trivy à 0 HIGH/CRITICAL sur les images utilisées et politique CI de refus.
- Recette Chromium sur runner : connexion par cookie HttpOnly, contrôle CSRF, création de ticket, reconnexion après rechargement, déconnexion et affichage mobile.

- Authentification : compteur de tentatives HMAC partagé via PostgreSQL, refus HTTP 429 également en accès direct à l'API, inscriptions publiques interdites en production.

- Sécurité navigateur : session JWT en cookie HttpOnly, protection CSRF liée au jeton, mode Secure en production, suppression de l'ancien stockage local, conservation du Bearer pour les scripts.

- Image de démonstration PostgreSQL : dérivé minimal de `postgres:17-alpine`, substitution de `gosu` (Go vulnérable) par `su-exec` (outil C d'Alpine), avec scan comparatif et tests de restauration sur runner.

- Qualité fonctionnelle : contrôle automatisé de `pg_dump` / `pg_restore` en base séparée, puis reconnexion de l'API après redémarrage sur runner jetable.

- Audit sécurité des images : workflow Trivy API/frontend/PostgreSQL, rapports JSON et suivi de la gravité ; réglage de confiance des en-têtes de proxy Uvicorn limité à `127.0.0.1` par défaut.

- Séparation GitHub/Notion : cours et ressources personnelles transférés dans Notion, documentation publique recentrée sur le produit.
- Audit du 22 novembre : blocage des comptes de démonstration en production, révocation des anciens JWT après changement de mot de passe, limitation des rafales d'authentification Nginx, migration de l'alias TypeScript 7.
- Nouvelle CI applicative sur runner (API SQLite/PostgreSQL, build React, Compose, smoke) ; voir [les preuves](evidence/qualification/2026-11-22-audit-cicd.md). Aucune release ni aucun déploiement Rocky.

- Nouvelle présentation GitHub du README et illustration vectorielle de couverture.
- Contrôle automatique de la documentation, des liens et des paires Draw.io/SVG (sans exécution de l'infrastructure).
- Cadre de contribution, modèles d'issues/PR, politique de sécurité et charte GitHub.

## Application 2.0.0 — novembre 2026

- Application fournie FastAPI, React/nginx et PostgreSQL 17, avec rôles et tickets.
- Images locales de démonstration, Docker Compose et sondes de santé.
- Documentation de l'architecture, exercices et qualification datée en environnement de test.

Cette entrée décrit la **version applicative 2.0.0** telle que documentée et ne prétend pas qu'une release GitHub ou un déploiement Rocky a été publié. Les détails et les résultats sont dans [STATUS.md](STATUS.md) et les [preuves du socle](evidence/qualification/2026-11-19-v26-mise-en-conformite.md).

## Archives

La version 1 et ses documents historiques sont conservés dans [legacy/](legacy/).
