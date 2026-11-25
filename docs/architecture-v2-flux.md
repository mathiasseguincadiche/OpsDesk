# OpsDesk — Architecture V2 : principes des flux publics

> **Archive V2 — remplacée le 25 novembre 2026.** [Référence active](architecture-v3-flux.md). Les informations ci-dessous ne décrivent plus la cible.

**Statut : validée en conception ; infrastructure du laboratoire non déployée.**

Cette version publique décrit les **frontières fonctionnelles**, non les règles d'accès détaillées. La matrice complète, le plan d'adressage, les identités, les ports d'exploitation et les contrôles négatifs exacts sont dans le dossier technique personnel.

## Réseau et responsabilités

L'hôte de virtualisation provisionne un réseau de laboratoire privé. Une machine assure l'administration, une seconde porte le service applicatif sous Compose et une troisième héberge une copie d'essai ainsi que la supervision.

## Flux fonctionnels

| Émetteur | Destination logique | Usage | Contrainte |
| --- | --- | --- | --- |
| Hôte | Machines virtuelles | Provisionnement | Commandes limitées à l'hyperviseur |
| Administration | Machines gérées | Configuration et déploiement | Comptes dédiés, droits minimaux |
| Navigateur | Frontend | Utilisation du service | HTTPS |
| Frontend | API | Requêtes métier | Réseau applicatif interne |
| API | Base de données | Accès aux données | Non exposé aux postes utilisateurs |
| Applications | Registre privé | Téléchargement des images | Sortant et authentifié |
| Supervision | Exporteurs autorisés | Mesures et alertes | Collecte filtrée |
| Tests | Copie d'essai | Essais de performance | Données indépendantes |
| Application | Réception de sauvegardes | Protection des données | Compte non destructif |

## Refus attendus

Les interfaces internes de données et de supervision ne sont pas accessibles directement aux utilisateurs. Le laboratoire n'accepte pas de connexion publique entrante vers les machines virtuelles. La copie d'essai ne partage ni données réelles ni accès administratifs avec le service principal.

## Qualification

Les refus comme les autorisations devront être testés, avec des preuves expurgées avant publication. **Ce tableau ne constitue pas une configuration de pare-feu utilisable directement.**

[Registre public des décisions](adr/README.md) · [Architecture globale](diagrams/architecture-globale.png) · [État réel](../STATUS.md)
