# Politique de sécurité d'OpsDesk

OpsDesk est un **projet de laboratoire**. La configuration de démonstration utilise des comptes et des valeurs par défaut fictifs ; elle n'est pas une configuration de production. **Ne pas exposer ce service sur Internet sans conception, durcissement, qualification et contrôles supplémentaires.**

## Portée

- Application v2 : API FastAPI, interface React/nginx, PostgreSQL et conteneurs.
- Laboratoire privé prévu : Fedora, Rocky Linux, Terraform, Ansible, Docker Compose et K3s isolé.
- Les futures infrastructures, alertes, sauvegardes et restaurations **ne sont pas présumées réalisées**.

La prise en charge des correctifs dépend de l'état du projet et des mainteneurs. Aucune garantie de support de production, de délai de correction ou de disponibilité ne peut être donnée.

## Signaler une vulnérabilité sans divulgation publique

1. Depuis l'onglet **Security** du dépôt, utiliser **Report a vulnerability** / le signalement privé **si cette fonction est activée**.
2. Si cette fonction n'est pas disponible, ne pas déposer d'exploit, de mot de passe, de jeton, de données personnelles ou de détails directement exploitables dans une issue publique. Demander d'abord au mainteneur la mise à disposition d'un canal privé via les moyens de contact de son profil.
3. Décrire dans un canal adapté le commit, le composant, l'environnement, la gravité, les conditions de reproduction et les résultats expurgés.
4. Attendre l'analyse avant toute divulgation ; ne pas attaquer ni scanner des services tiers.

Ce document **n'active pas** à lui seul le signalement privé dans les paramètres GitHub.

## Risques connus et dépendances

La [synthèse des risques techniques](docs/securite.md), le [statut vérifié](STATUS.md) et le [suivi des scans d'images](https://github.com/mathiasseguincadiche/OpsDesk/issues/51) détaillent les constats datés. Un scan terminé, même avec des alertes connues, n'est **pas** une homologation de sécurité. Les chiffres et versions de vulnérabilités doivent être relus dans leur rapport source avant communication.

Les mises à jour de dépendances doivent passer par une PR, avec vérifications et analyse des impacts. Aucune fusion ou mise en production automatique n'est autorisée par cette politique.

## Mesures minimales pour le laboratoire

- Employer des données fictives ; protéger les secrets et les states Terraform hors Git.
- Garder SELinux et le pare-feu actifs et contrôler les ports publiés, notamment Docker.
- Vérifier l'identité des images, les permissions, les volumes, les versions et les sauvegardes.
- Ne pas confondre `/health/live`, `/health/ready`, `/metrics` et la disponibilité métier.
- Tester sauvegarde, restauration et retour arrière sur une cible isolée avant de les déclarer fiables.

Références : [contrat applicatif](docs/contrat-applicatif.md) · [exploitation](docs/exploitation-day2.md) · [preuves](docs/preuves.md).
