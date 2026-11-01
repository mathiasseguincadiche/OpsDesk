# OpsDesk — démarrage de l’apprentissage

> Guide de **préparation**, pas tutoriel d’exécution déjà validé. Les véritables commandes applicatives seront ajoutées après création et test du code.

## Environnement envisagé

- Poste de développement : **Fedora**.
- VM cible : **Rocky Linux**.
- Laboratoire : **KVM** si nécessaire.
- Phase 1 : Docker et Docker Compose, Git, éditeur de code.
- Phase 2 : Terraform, Ansible, compte AWS avec budget et droits limités.
- Phase 3 : K3s, Prometheus/Grafana, k6.

## Précontrôles sans modification de la machine

```bash
git --version
docker --version
docker compose version
```

Si une commande répond « not found », s’arrêter, identifier la distribution et utiliser la documentation officielle de l’outil. Ne pas lancer l’installation ou le cloud « pour voir ».

## Première séance concrète

1. Définir les champs d’un ticket et le sens de chaque statut.
2. Choisir une pile applicative **simple** et expliquer le choix dans `docs/architecture.md`.
3. Créer un test d’ouverture de ticket, puis un test d’entrée invalide.
4. Développer le service minimal, brancher PostgreSQL, vérifier les résultats.
5. Ajouter Compose et tester persistance + redémarrage.
6. Consigner les commandes et les sorties réellement obtenues dans ce guide, sans coller de secrets.

En cas d’échec : noter l’erreur exacte, vérifier versions, ports et journaux, changer une seule hypothèse à la fois. **Ne pas supprimer de volumes sans vérifier les données qu’ils contiennent.**