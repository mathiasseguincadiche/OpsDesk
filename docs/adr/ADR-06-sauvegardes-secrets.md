# ADR-06 — Secrets protégés, sauvegardes externes et restauration

**Statut : validé en conception (Architecture V3).**

## Décision
Les secrets sont gérés hors du code public avec chiffrement et droits restreints. Les données applicatives sont sauvegardées automatiquement, transmises à un point de réception à privilèges réduits et recopiées vers un support externe chiffré indépendant.

## Justification
Le chiffrement, le cloisonnement des identités de transfert et l'indépendance des copies réduisent l'impact d'une panne ou d'une compromission de la machine applicative.

Protéger aussi le state Terraform, les identités de récupération et la CA interne. Une sauvegarde restaurable précède tout changement risqué.

## Vérification prévue
Tester la restauration sur environnement isolé, les refus d'opérations non autorisées et les temps effectivement mesurés de reprise.

**Périmètre public :** les identités de transfert, commandes forcées, chemins, rétentions exactes, horaires, clés et procédures de reprise restent privés.
