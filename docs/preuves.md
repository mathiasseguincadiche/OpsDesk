# Lire une preuve et ses limites

## Preuve applicative courante

Le [rapport des tests actuels](../evidence/v44/application-tests.json) et son journal enregistrent 26 tests réussis sur la source montée en lecture seule, avec PostgreSQL réel. La plupart des cas utilisent une table TEMP ; un ticket fictif par passage est committé puis relu par des connexions distinctes et conservé. Le premier passage défavorable reste archivé séparément. Aucune image reconstruite, aucun service redéployé, aucune reprise ou opération InfraOps personnelle n’est exécutée.

## Smoke historique conservé

[Le smoke HTTP](../evidence/business-smoke.json) rapporte son heure UTC, la version servie, l’environnement d’accès local, chaque requête et son statut. Le fichier courant est daté du 3 novembre 2026 à 13:40:23 UTC ; il conserve un parcours de préparation historique comprenant :

- liveness, readiness et version ;
- affichage du formulaire HTML ; création/liste/lecture d’un ticket PostgreSQL ;
- transitions en cours/clôturé et refus de réouverture ;
- refus d’entrée invalide et de ticket absent ;
- soumission UI, contenu HTML échappé et refus sans CSRF ;
- métrique DB disponible.

La preuve déclare `uncommitted-v42`. Elle ne fournit pas un faux SHA, un digest GHCR, un test de persistance après redémarrage ou une restauration. Le champ `persisted_ticket_id` désigne le ticket enregistré et relu pendant le test, pas une preuve de résilience à une destruction.

## Avancement et contrôle : deux informations distinctes

L’avancement répond à « qu’est-ce qui existe ? » : prévu, en cours, réalisé/implémenté ou abandonné. Le contrôle répond à « qu’a-t-on établi ? » : vérifié, échec constaté ou non vérifié. Ainsi, un playbook écrit peut être **réalisé — non vérifié** ; un contrôle exécuté peut être **réalisé — échec constaté**. Les résultats détaillés gardent PASS, FAIL, PARTIEL ou NON EXÉCUTÉ. Le mot « exécuté » décrit une action effectuée, jamais sa réussite implicite. Un abandon indique sa raison et sa date lorsqu’elles sont connues.

Une preuve vaut pour les fichiers, versions, cible, méthode et critères qu’elle identifie. Si cet ensemble change, le contrôle de la nouvelle révision redevient non vérifié ; l’ancien rapport reste intact comme observation historique. Une correction ne supprime pas l’échec initial : lier la nouvelle validation. Un changement uniquement rédactionnel n’invalide pas automatiquement un résultat applicatif portant sur un code et un environnement inchangés ; il exige cependant son propre contrôle documentaire.

Une déclaration sans pièce consultable se note « déclaré par l’apprenant — non vérifié ». Elle n’est ni rejetée ni convertie en preuve. Les niveaux L0–L3 décrivent une progression personnelle et restent distincts de ces deux axes ; aucune migration documentaire ne les remplit.

**Exemple fictif :** un déploiement K3s a été contrôlé sur une VM et un digest précis. Changer le digest, le stockage ou les sondes ne transfère pas le PASS à la nouvelle cible. Conserver la preuve initiale, marquer le nouveau périmètre non vérifié et choisir les contrôles concernés avant de conclure.

Un « vérifié » indique toujours date, version ou hash, cible, commande/méthode, attendu, observé et limites. Si une pièce manque, préciser le manque plutôt que reconstruire une sortie probable.

## Registre à tenir

| Champ | Attendu |
|---|---|
| Besoin métier | Effet attendu pour le collaborateur ou l’équipe IT |
| Cible | Machine, runtime, namespace/volume et limites de l’isolement |
| Version | Commit réel, image/digest si disponible ; sinon état de travail déclaré |
| Pré-check | Ressources, droits, état initial et retour possible |
| Exécution | Commande ou job exact réellement lancé |
| Résultat | PASS/FAIL/PARTIEL/NON EXÉCUTÉ, observation et critère |
| Diagnostic | Échec observé, cause établie ou hypothèse encore ouverte |
| Traçabilité | Date UTC et fichier/log nettoyé ; aucune donnée secrète |

## Rejouer sans gonfler les statuts

**ACTIF — exécutable depuis les sources disponibles, sous prérequis ; NON EXÉCUTÉ par cette mission documentaire.** Les tests unitaires purs sont présents. Depuis la racine OpsDesk, sur le poste personnel avec Python disponible, sous son utilisateur ordinaire et sans DB ni installation supplémentaire, leur lancement est :

```sh
python3 -m unittest discover -s tests/unit -v
```

La preuve historique utilisait Python 3.14.10 ; relever sa propre version avant comparaison. Attendu : sept tests de règles sans échec, puis un code de sortie 0. En cas d’import introuvable ou de résultat différent, conserver l’erreur, le chemin de lancement et le commit ; lire le test et son import avant toute installation. La commande n’appelle ni DB ni service, mais Python peut créer un cache `__pycache__` dans le répertoire utilisateur du dépôt.

**ACTIF — travail personnel à réaliser : identifier et recevoir une instance avant le smoke.** `scripts/smoke.py` est présent ; il ne prépare ni n’installe le service. Le [contrat, section 20](contrat-applicatif.md#20-commandes-de-vérification) fournit le contexte du contrôle HTTP, après préparation de l’instance, des secrets et de la DB. La cible de référence `127.0.0.1:18081` désigne la boucle locale de la machine qui lance le client ; sur l’hôte, elle ne désigne pas automatiquement la VM. Le smoke crée deux tickets fictifs et ne les efface pas. Contrôler l’identité du service avec `/version`, les données autorisées et le port avant toute écriture.

Archiver uniquement la sortie réellement obtenue, avec version, environnement et date ; ne pas conserver PASS après une régression. La présence de ces consignes n’est pas un nouveau résultat.

## Ce qui appartient aux exercices personnels

Connexion développeur/CI → image → cible, image immuable publiée, reconstruction, idempotence de la configuration Linux Ansible, déploiement K3s, alerte, maintenance et restauration restent des évaluations personnelles distinctes. Les reprises locales historiques existent ; elles ne valident pas celles de l’apprenant. Les quinze cellules du portfolio sont suivies par projet ; [la grille OpsDesk](parcours-apprentissage.md#cinq-piliers--réception-séparée) ne devient pas verte parce qu’un seul smoke passe.

## Compléments exécutés le 3 novembre

- [Navigateur Chrome/Playwright](../evidence/browser.json) : affichage de la liste de tickets sur la boucle locale, aucune erreur JavaScript observée.
- [Contrat Terraform et rendu Ansible](../evidence/automation-contract.json) : état et JSON locaux, deux passages sans changement ; aucun provisioning. [Échec initial Ansible conservé](../evidence/automation-first-attempt.json).
- [Rendu Kustomize hors ligne](../evidence/k8s-static.json) : treize objets assemblés ; aucune API de cluster contactée.
- [Rapport de vulnérabilités](../evidence/vulnerability-scan.json) : vérifier son statut et l’image analysée ; sa seule présence ne signifie pas PASS.

[Évaluations détaillées](evaluations.md) · [Contrat, choix et limites](infrastructure.md).

## Reprise historique la plus récente

Le [rapport historique de reprise](../evidence/recovery.json) est daté du 3 novembre à 13:52:06 UTC : cible 18088 et 10,969 s. Le rapport précédent 10,769 s est conservé à part. Ces observations du même hôte ne sont pas rejouées depuis, ne constituent pas un PRA physique ou un SLO, et n’attribuent aucune compétence personnelle.
