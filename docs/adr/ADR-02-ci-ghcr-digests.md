# ADR-02 — Livraison reproductible par images signées par leur digest

**Statut : validé en conception (Architecture V3).** Le déploiement complet reste à réaliser.

## Décision
Les pipelines CI qualifient les versions, publient les images dans un registre privé et les désignent par des digests immuables. Les environnements consomment les mêmes références, sans reconstruire leurs images indépendamment.

## Justification
Les digests apportent une meilleure traçabilité des mises en service et facilitent le retour arrière contrôlé.

## Sécurité
Les consommateurs utilisent des permissions minimales, les identifiants ne sont jamais commis et aucune connexion entrante depuis la CI n'est requise dans le laboratoire privé.

La CI publique ne pilote pas directement Fedora. Les images qualifiées sont promues par digest après validation de la copie d’essai et approbation ; le rollback doit respecter les migrations.

## Vérification prévue
Contrôler l'identité des images, les preuves CI, l'installation d'une version précise et le retour arrière.

**Périmètre public :** la distribution des identifiants et les procédures d'accès au registre restent personnelles.
