# OpsDesk — apprendre et comprendre

Ce dépôt est un laboratoire **guidé**, pas un catalogue de commandes à copier-coller.

## La méthode des sept questions

Pour chaque tâche, produire des réponses courtes et concrètes :

1. **Quel problème ?** Expliquer ce qui dysfonctionnerait sans cette étape.
2. **Quels prérequis ?** Outils, versions, permissions, ressources et coûts.
3. **Quel mécanisme ?** Décrire les échanges et les responsabilités, sans jargon inutile.
4. **Comment faire le minimum ?** Un seul changement observable.
5. **Comment prouver ?** Commande exacte, résultat attendu, résultat obtenu.
6. **Comment diagnostiquer ?** Provoquer une panne sans risque et identifier son symptôme.
7. **Qu’ai-je compris ?** Expliquer à voix haute la logique et ses limites.

## Petit lexique

- **Image Docker :** modèle d’exécution versionné ; un conteneur est une instance démarrée de cette image.
- **Volume :** emplacement de données indépendant du cycle de vie d’un conteneur.
- **CI :** contrôles automatiques à chaque changement, dont il faut lire les vrais résultats.
- **IaC :** description versionnée des ressources désirées ; comparer le plan avant d’agir.
- **Idempotence :** relancer la configuration ne doit pas entraîner de changements inutiles.
- **Readiness :** indique si l’application peut recevoir du trafic ; **liveness** indique si elle doit être redémarrée.
- **Observabilité :** indices permettant d’expliquer un fonctionnement ou un incident.

## Exercices graduels

- **Débutant :** expliquer pourquoi les tickets survivent au redémarrage d’un conteneur mais pas à l’effacement de son volume.
- **Livraison :** suivre un commit jusqu’aux tests puis jusqu’au tag d’image GHCR.
- **Infrastructure :** expliquer précisément ce que crée Terraform et ce que configure Ansible.
- **Exploitation :** tracer un incident depuis l’alerte jusqu’à la cause, puis vérifier la reprise.
- **Retour d’expérience :** noter un choix initial incorrect et pourquoi la correction est meilleure.

Écrire pour chaque exercice : **hypothèse, manipulation, observation, explication, limite**. Les 16 modules détaillés d’OpsDesk peuvent être approfondis dans Notion ; GitHub garde le code et les preuves.