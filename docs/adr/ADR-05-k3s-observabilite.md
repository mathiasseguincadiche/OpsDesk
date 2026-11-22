# ADR-05 — Kubernetes d'essai et observabilité séparée

**Statut : validé en conception (Architecture V2).**

## Décision
Le service principal reste déployé sous Compose ; une plateforme Kubernetes d'essai indépendante accueille une copie isolée et les outils d'observabilité. Les essais de performance se déroulent sur cette copie, jamais sur les données principales.

## Justification
Cette séparation rend possible l'apprentissage de Kubernetes, des métriques et des alertes sans imposer son orchestration au service principal.

## Vérification prévue
Valider la séparation des données, les ressources et quotas, la collecte restreinte, la réception des alertes et l'absence d'impact des essais sur le service principal.

**Périmètre public :** les noms d'espaces, destinations de métriques, seuils et destinations d'alertes détaillées restent dans le dossier personnel.
