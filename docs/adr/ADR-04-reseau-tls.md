# ADR-04 — Réseau privé, HTTPS et isolation des services

**Statut : validé en conception (Architecture V2).**

## Décision
Les machines du laboratoire appartiennent à un réseau privé. Les accès utilisateur au service cible passent par HTTPS ; les interfaces de données et d'administration ne sont pas exposées directement. Les accès de supervision sont limités aux consommateurs attendus.

## Justification
La séparation des frontières réseau réduit la surface d'exposition. TLS protège le trafic utilisateur tandis que les contrôles réseau limitent les mouvements latéraux.

## Vérification prévue
Tests d'accès positifs et négatifs, vérification des certificats, du routage, des résolutions internes et des règles de filtrage.

**Périmètre public :** adressage, plans de ports, origines autorisées, noms DNS et règles détaillées figurent uniquement dans la documentation personnelle.
