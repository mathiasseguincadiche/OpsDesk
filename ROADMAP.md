# OpsDesk — plan de réalisation et critères de sortie

Chaque étape suit : **pourquoi → précontrôle → construction → validation → panne simulée → explication**.

## 0. Cadrer le service

- [ ] Définir trois usages : ouvrir, consulter, clôturer un ticket.
- [ ] Choisir la pile applicative la plus simple à maintenir ; argumenter le choix.
- [ ] Dessiner le schéma PostgreSQL et identifier les données **fictives**.
- [ ] Définir une API minimale et des erreurs prévisibles.

**Validation :** quelqu’un d’autre comprend les besoins en une minute. **À expliquer :** pourquoi une base relationnelle pour les tickets ?

## 1. Application et livraison locale — commencer ici

- [ ] Écrire le CRUD minimal et des tests métier (cas nominal et entrée invalide).
- [ ] Démarrer PostgreSQL + application avec Compose, healthchecks et données persistantes.
- [ ] Tester création → modification → redémarrage → relecture.
- [ ] Produire une image versionnée reliée à un commit.
- [ ] Construire une vraie CI : tests, image, analyse Trivy, publication GHCR conditionnée à la réussite et aux permissions minimales.
- [ ] Forcer volontairement un test en échec et vérifier que la CI le signale.

**Sortie :** une personne peut suivre les instructions sur sa machine, rejouer le scénario et identifier l’image exacte.

## 2. Provisionnement et sécurisation

- [ ] Définir budget AWS, région, réseau, secrets, droits IAM et procédure de destruction.
- [ ] Écrire Terraform : `fmt`, `validate`, `plan`, revue, puis `apply` autorisé.
- [ ] Configurer Rocky Linux avec Ansible (comptes, SSH, SELinux, firewalld, packages et logs).
- [ ] Tester un deuxième passage Ansible sans changement indésirable.
- [ ] Déployer l’application et vérifier accès, sécurité, journalisation.
- [ ] Reconstruire le laboratoire et supprimer les ressources payantes.

**Sortie :** environnement traçable et reconstructible. **À expliquer :** Terraform crée les ressources ; Ansible configure l’OS.

## 3. Exploitation et incident

- [ ] Adapter l’application au déploiement K3s, gestion des secrets et stockage compris.
- [ ] Définir sondes readiness/liveness, ressources et procédure de rollback.
- [ ] Collecter disponibilité, latence et erreurs dans Prometheus/Grafana.
- [ ] Créer une alerte déclenchable et un scénario de dépannage avec journaux.
- [ ] Exécuter un test k6 avec seuils et interpréter les résultats.
- [ ] Documenter un échec, son diagnostic et le retour à un fonctionnement normal.

**Sortie :** mini-démonstration « incident → signal → investigation → réparation » avec mesures datées.

## Avant toute diffusion comme projet achevé

- [ ] Code réel disponible et instructions reproductibles.
- [ ] Tests et pipeline accessibles ; captures/logs nettoyés de secrets.
- [ ] Au moins un incident documenté avec sa cause.
- [ ] `STATUS.md` à jour avec commit, date et preuves.
- [ ] Présentation honnête des limites, coûts et décisions.

Les liens vers les dépôts pourront ensuite être ajoutés au CV, mais aucun état technique n’est anticipé.