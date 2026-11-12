# Sécurité applicative, périmètre local et provenance

## Modèle retenu

**OpsDesk n’authentifie pas ses utilisateurs.** Tout visiteur du laboratoire peut lire et modifier les tickets fictifs. La session Flask ne sert qu’à signer le jeton CSRF des formulaires. Ce choix est explicite pour conserver un premier support métier limité ; aucune autorisation d’accès partagé ou Internet n’est donnée.

Une authentification minimale a été évaluée : elle ajouterait identités, mots de passe et cycle de session au premier parcours. Elle n’est pas ajoutée sous la forme d’un jeton partagé présenté comme un contrôle utilisateur. Si le besoin évolue, une modification applicative distincte et testée sera nécessaire.

## Contrôles applicatifs actuels

Corps HTTP limité à 16 Kio, validations de types/longueurs et du texte Unicode stockable, SQL paramétré, contraintes métier PostgreSQL, échappement Jinja, en-têtes de protection, mutations API exclusivement JSON et CSRF des formulaires. Une entrée CSRF non ASCII est refusée avec 400. `TRUSTED_HOSTS` limite par défaut les hôtes HTTP à localhost/127.0.0.1 ; son erreur est rendue sans modèle Jinja pour éviter un 500 avant l’adaptateur d’URL.

Les tests utilisent des cas négatifs réels dans la source applicative actuelle ; l’erreur DB est simulée dans un cas de test, pas provoquée dans le service source. Voir le [contrat](contrat-applicatif.md) et la [preuve actuelle](../evidence/qualification/application-tests.json).

## Secrets et droits attendus

Le code reçoit les chemins `DB_PASSWORD_FILE` et `SESSION_SECRET_FILE`, jamais leurs valeurs en ligne de commande. Ils sont privés et exclus de Git. Le rôle PostgreSQL est configurable par `DB_USER` ; seuls lecture/insertion/mise à jour et usage de séquence sont requis par l’application. L’apprenant préparera la base, les accès, les droits et leur stockage.

Les anciennes références utilisaient trois fichiers sous `secrets/`. La confidentialité réelle du montage Windows/WSL ne découle pas d’un simple chmod intentionnel ; elle n’est pas qualifiée par ce contrôle applicatif. Aucun identifiant réel n’est révoqué ou modifié ici.

## Alertes conservées

Le [rapport d’image historique](../evidence/vulnerability-scan.json) reste FAIL : 185 occurrences dont 45 HIGH, sans correction disponible indiquée pour ces HIGH à l’heure de ce scan. Ces nombres sont des occurrences paquet/avis, pas des exploits démontrés. Le retrait passé de pip/setuptools de l’image finale et le smoke réussi ne donnent pas un feu vert global. Le tri applicatif actuel du programme et ses réserves sont distincts de ce rapport historique.

Le choix/durcissement de l’image finale, TLS, flux, système, supervision et rotation d’infrastructure seront réalisés par l’apprenant. Les protections applicatives ne remplacent pas ces décisions.

## Provenance et licences

Le code de démonstration est fourni ; il ne doit pas être présenté comme un produit ITSM développé personnellement par l’apprenant. Les [origines et références](provenance.md) séparent application, composants tiers, références assistées et réalisations personnelles futures. Le code propre utilise [MIT](../LICENSE) ; les dépendances gardent leurs licences respectives.
