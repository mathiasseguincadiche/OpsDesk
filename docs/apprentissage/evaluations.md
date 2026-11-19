# Cinq évaluations transversales

Mise à jour : 18 novembre 2026, pour la version 2 d'OpsDesk.

Les exercices apprennent un outil à la fois. Les évaluations vérifient qu'on sait **les enchaîner** pour répondre à un besoin réel, comme en poste. Il y en a une par pilier ; chacune mobilise plusieurs exercices et se mène sur un scénario complet, du besoin à la preuve.

## Règles communes

- **Quand** : après les exercices concernés, jamais avant.
- **Où** : sur la cible indiquée ; toute action perturbatrice se fait sur la copie d'essai, ou sur `srv-app` dans une fenêtre annoncée, après une sauvegarde.
- **Aide** : déclarée avec son niveau, de A0 à A3 (voir [le parcours](README.md#preuve-et-progression-personnelles)).
- **Preuve** : sorties réelles datées, liens vers les commits et les exécutions de CI, chronométrages. Une sortie type n'est jamais une preuve.
- **Conclusion** : réussie, réussie avec aide, ou à retravailler, avec ce qui a manqué. Pas de note chiffrée. Le niveau L3 demande en plus une vérification séparée (exercice 13).

**État au 18 novembre 2026** : aucune évaluation menée.

<a id="evaluation-1"></a>

## Évaluation 1 — Construire : accueillir un nouveau venu

**Exercices mobilisés** : 01, 02, 03.

**Scénario.** Une personne arrive dans l'équipe. En 30 minutes, tu lui expliques OpsDesk et son infrastructure, puis tu lui ouvres un accès d'administration à `srv-admin`, sans mot de passe et sans affaiblir aucune protection.

**À démontrer.**

1. Le trajet d'une demande, du navigateur à la base, sur le schéma d'architecture, et ce que fait chaque composant.
2. Trois décisions du registre défendues avec leurs quatre réponses (besoin, alternative, panne, contrôle).
3. Un compte nominatif créé sur `srv-admin`, avec sa clé, son empreinte d'hôte vérifiée, et des droits justifiés.
4. Un refus attendu, prouvé : ce compte ne peut pas se connecter par mot de passe.

**Critères de réussite.** Explication juste sans notes ; accès fonctionnel par clé ; SELinux `Enforcing` et firewalld actif à la fin ; aucun secret transmis par un canal non protégé.

<a id="evaluation-2"></a>

## Évaluation 2 — Automatiser : reconstruire `srv-app` de zéro

**Exercices mobilisés** : 04, 05, 06, 11.

**Scénario.** Simuler la perte de `srv-app` sur une cible jetable explicitement isolée. Après vérification d’une sauvegarde restaurable, du plan et accord ciblé, reconstruire une VM de test entièrement par Terraform, Ansible, le rôle de déploiement puis la restauration. Ne jamais détruire la VM de service, le state partagé ou l’unique sauvegarde pour cette évaluation. Aucune configuration manuelle sur la cible de reconstruction.

**À démontrer.**

1. Le plan Terraform avant destruction et avant recréation, lu et commenté.
2. La VM de test recréée, configurée et servant OpsDesk, sans configuration manuelle.
3. Les données restaurées : le ticket témoin relu dans l'interface.
4. La durée totale, de la destruction au ticket relu.

**Critères de réussite.** Aucune configuration manuelle sur la cible de reconstruction ; second passage Ansible à `changed=0` ; second plan Terraform à « No changes » ; durée et fenêtre de perte observées, comparées aux objectifs RTO/RPO.

<a id="evaluation-3"></a>

## Évaluation 3 — Livrer : une modification, du commit au service

**Exercices mobilisés** : 06, 07, 08, 10.

**Scénario.** Une petite modification de l'application (par exemple, un libellé de l'interface) doit partir en service. Elle passe par une pull request, la CI, la copie d'essai dans K3s, puis le service réel, avec un retour arrière exercé.

**À démontrer.**

1. La pull request testée, puis fusionnée ; l'image publiée avec son digest.
2. La nouvelle version vérifiée d'abord sur la copie d'essai.
3. Le déploiement sur `srv-app` par le rôle Ansible, avec une sonde continue et l'indisponibilité mesurée.
4. Le digest de l'image qui tourne identique à celui publié par la CI.
5. Un retour arrière vers la version précédente, puis le retour à la nouvelle.

**Critères de réussite.** Aucune image construite à la main ; aucun accès SSH à `srv-app` nécessaire pour livrer, en dehors du rôle Ansible ; chaque étape reliée à son commit et à son exécution de CI.

<a id="evaluation-4"></a>

## Évaluation 4 — Observer : de l'alerte au post-mortem

**Exercices mobilisés** : 09, 12.

**Scénario.** Une autre personne provoque une panne sur la copie d'essai, sans te prévenir. Tu dois être alerté par ta supervision, puis diagnostiquer et rétablir.

**À démontrer.**

1. L'alerte reçue : laquelle, à quelle heure, combien de temps après le début de la panne.
2. Le diagnostic en sept temps, avec son journal d'incident.
3. Le rétablissement, recontrôlé jusqu'au parcours d'un utilisateur.
4. Un post-mortem d'une page, sans reproche, avec au moins une amélioration de la supervision.

**Critères de réussite.** Panne détectée par la supervision et non par hasard, ou absence de détection expliquée et corrigée ; cause démontrée par un test qui en écarte une autre ; une seule correction à la fois.

<a id="evaluation-5"></a>

## Évaluation 5 — Maintenir : une maintenance sous contrainte

**Exercices mobilisés** : 10, 11.

**Scénario.** Il faut appliquer les mises à jour de Rocky Linux à `srv-app`, avec redémarrage, avec un objectif de moins de 5 minutes d'indisponibilité et de zéro perte de données, à vérifier et non garanti à l'avance. Le critère d'abandon est fixé avant de commencer.

**À démontrer.**

1. La fiche d'intervention, écrite et datée avant l'intervention.
2. Une sauvegarde faite juste avant, copiée hors de la VM, empreinte vérifiée.
3. L'intervention, avec une sonde continue depuis `srv-admin`.
4. Les contrôles après : version, sondes, ticket témoin, courbes de supervision avant et après.
5. Un compte rendu de cinq lignes.

**Critères de réussite.** Indisponibilité mesurée et sous la limite, ou abandon déclenché par le critère écrit et retour à l'état initial prouvé ; ticket témoin intact ; système à jour.

## Historique

Les évaluations de la version 1 et leurs essais datés sont conservés dans [le registre historique](../evaluations.md).
