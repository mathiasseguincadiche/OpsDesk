# OpsDesk — comprendre l’architecture cible

> Architecture **proposée** et non déployée.

## Responsabilité de chaque composant

| Brique | Pourquoi elle existe | Ce qu’elle ne remplace pas |
| --- | --- | --- |
| Application de tickets | Règles métier et HTTP | Persistance des données |
| PostgreSQL | Données durables, transactions, migrations | Tests fonctionnels |
| Docker Compose | Démarrage local coordonné | Kubernetes |
| GitHub Actions | Répète tests et construction d’images | Tests d’exploitation |
| GHCR / Trivy | Stockage d’images versionnées / analyse de vulnérabilités | Politique complète de sécurité |
| Terraform | Déclare les ressources AWS à créer | Configuration détaillée de Rocky Linux |
| Ansible | Configure et durcit l’OS | Création des ressources cloud |
| K3s | Déploie et maintient les conteneurs du labo | Fiabilité intrinsèque de l’application |
| Prometheus / Grafana | Mesure et rend visibles les problèmes | Analyse complète des journaux |
| k6 | Mesure sous charge simulée | Preuve d’aptitude à la production |

## Trois étapes, une seule application

1. **Machine locale / Compose :** rapidité d’itération et compréhension des volumes, réseaux, variables et journaux.
2. **VM Rocky Linux sur AWS :** reconstruire l’environnement, vérifier SSH/réseau/pare-feu, comprendre l’Infrastructure as Code.
3. **K3s de laboratoire :** déploiement déclaratif, sondes de santé, secrets, stockage, supervision et incident.

Le passage à la phase suivante ne doit pas casser le scénario métier validé précédemment.

## Questions de conception encore ouvertes

- Quel framework est le plus lisible pour une application CRUD minimale ?
- Quel mécanisme de migration PostgreSQL permet de suivre les changements ?
- Quelle convention de version assure le lien code → tests → image ?
- Où sont stockés les secrets sans les committer ?
- Quelle mesure donne un signal d’incident utile, et quel seuil est défendable ?
- Comment réduire les dépenses AWS et supprimer proprement le labo ?

Consigner chaque réponse sous la forme **besoin → options → décision → compromis**. Ne pas ajouter de composant simplement parce qu’il est populaire.

## Cas de panne à investiguer

- **Base indisponible :** démontrer comment séparer erreur applicative et panne de connexion PostgreSQL.
- **Mauvaise version :** retrouver le commit, reconnaître un mauvais déploiement, restaurer la version précédente.
- **Latence élevée :** confronter métriques, requêtes, journaux et saturation avant d’augmenter les ressources.

Chaque cas produira ultérieurement un compte rendu daté, avec sorties de commande réellement observées.