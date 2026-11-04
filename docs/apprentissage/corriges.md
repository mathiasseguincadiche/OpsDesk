# Repères de correction — à consulter après une première tentative

Ces repères séparés ne sont pas une infrastructure complète. Demander un indice, une explication limitée ou une revue ciblée selon le besoin. Une réponse différente peut être pertinente si elle satisfait le contrat et les vérifications. Tous les résultats personnels restent NON EXÉCUTÉS / NON ÉVALUÉS.


<a id="exercice-01"></a>
<a id="exercice-01"></a>

## Exercice 01 — Comprendre l’application

**Attendus à argumenter.** Un contrat applicatif décrit ce que le logiciel exige et garantit ; il ne choisit pas ton infrastructure. Un parcours utilisateur relie une entrée HTTP à une donnée persistante. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Un schéma fonctionnel personnel, la liste des données durables et les questions posées à l’équipe applicative.

**Vérification raisonnée.** Suivre une action utilisateur et nommer chaque composant qui peut la bloquer. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Confondre le laboratoire de Codex avec une architecture personnelle déjà choisie. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-02"></a>
<a id="exercice-02"></a>

## Exercice 02 — Concevoir l’architecture

**Attendus à argumenter.** L’architecture traduit un besoin en ressources, flux et frontières de confiance. Un dessin doit expliquer les accès et la persistance, pas seulement aligner des logos. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Schéma technique personnel modifiable, choix argumentés et alternatives raisonnables.

**Vérification raisonnée.** Partir du symptôme utilisateur et traverser client, point d’entrée, application puis stockage. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Assimiler namespace, réseau conteneur et isolation de machines ; oublier où vivent les données. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-03"></a>
<a id="exercice-03"></a>

## Exercice 03 — Préparer Linux et le réseau

**Attendus à argumenter.** Linux porte des processus, fichiers et services avec des droits. DNS résout un nom ; une route choisit un trajet ; un port écoute ; le pare-feu autorise un flux. Ces contrôles répondent à des questions différentes. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Identité de cible, carte de flux, accès vérifiés et diagnostic d’un défaut borné.

**Vérification raisonnée.** Observer utilisateur, processus/service, résolution, trajet, écoute puis autorisation ; changer une chose après confirmation. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Désactiver SELinux/le pare-feu en bloc ; utiliser root partout ; diagnostiquer une route avec un test DNS seulement. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-04"></a>
<a id="exercice-04"></a>

## Exercice 04 — Provisionner avec Terraform

**Attendus à argumenter.** Terraform compare la configuration au state et à l’état distant pour calculer un plan. Le state contient des identités et parfois des secrets ; un fichier terraform_data local ne crée pas une VM. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Code personnel, plan expliqué, état protégé et ressources observées correspondant au plan.

**Vérification raisonnée.** Localiser l’erreur entre syntaxe, provider/authentification, droits, quota ou dérive ; ne pas supprimer le state comme premier réflexe. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Confondre validation syntaxique et ressource créée ; versionner le state ; forcer un apply sur la mauvaise cible. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-05"></a>
<a id="exercice-05"></a>

## Exercice 05 — Configurer avec Ansible

**Attendus à argumenter.** Ansible applique des tâches à un inventaire. Un module convergent décrit un état ; l’idempotence se vérifie par une seconde passe et par l’état effectif, pas par un commentaire. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Première/seconde sorties expurgées, tâches expliquées et contrôle du service/paramètre effectivement configuré.

**Vérification raisonnée.** Lire le premier hôte/tâche/code en défaut ; vérifier accès, chemin, variable, module et privilège avant correction ciblée. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Utiliser shell pour chaque action ; confondre changed=0 avec service fonctionnel ; laisser une variable sensible dans un log. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-06"></a>
<a id="exercice-06"></a>

## Exercice 06 — Conteneuriser

**Attendus à argumenter.** Une image fige le programme et ses dépendances ; un conteneur est un processus qui l’utilise. Réseau, volumes, paramètres et secrets déterminent son fonctionnement. L’image n’est pas une sauvegarde de la base. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Recette personnelle, image identifiable, configuration privée et parcours métier vérifié.

**Vérification raisonnée.** Séparer erreur de build, commande de lancement, droits, DNS, connexion DB et schéma ; regarder le premier message utile. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Inclure secrets/données dans l’image ; utiliser latest sans identité ; croire qu’un conteneur démarré prouve le métier. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-07"></a>
<a id="exercice-07"></a>

## Exercice 07 — Orchestrer avec Kubernetes/K3s

**Attendus à argumenter.** Un Deployment pilote des réplicas ; un Service sélectionne des Pods ; readiness décide du trafic et liveness d’un redémarrage. Une donnée durable exige un choix explicite de stockage et de reprise. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Workloads/flux expliqués, version servie et parcours métier ; rollout et diagnostic sur une cible nommée.

**Vérification raisonnée.** Examiner événements, état du Pod, logs et sélecteurs/endpoints avant de relancer ; revalider la donnée utile. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Confondre port applicatif, Service et exposition ; probe qui dépend de la DB et redémarre tout ; PVC pris pour sauvegarde. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-08"></a>
<a id="exercice-08"></a>

## Exercice 08 — Construire la CI/CD

**Attendus à argumenter.** La CI formalise des contrôles déjà compris ; la livraison déplace un artefact identifié vers une cible autorisée. Une preuve doit appartenir au commit/run courant, pas être un ancien PASS joint au hasard. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Jobs personnels expliqués, échec discriminant diagnostiqué, même artefact testé livré et contrôle métier après livraison.

**Vérification raisonnée.** Nommer job, étape, commande, message, hypothèse et test final ; distinguer refus d’accès, variable absente, test métier et mauvais artefact. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Déployer depuis un runner public en supposant un accès au KVM local ; secrets dans les logs ; ancien JSON PASS présenté comme preuve du run. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-09"></a>
<a id="exercice-09"></a>

## Exercice 09 — Superviser

**Attendus à argumenter.** Une métrique est une mesure, un journal explique un événement et une alerte signale un besoin d’action. La disponibilité d’un processus ne garantit pas le succès d’un parcours métier. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Signal choisi pour le métier, alerte constatée, logs corrélés et retour observé ; pas seulement une capture de tableau vide.

**Vérification raisonnée.** Formuler le symptôme, comparer métriques/logs/événements et contrôler la dépendance suspecte sans multiplier les modifications. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Compter uniquement HTTP200 ; alerte sans destinataire ; générer un identifiant de ticket comme label à forte cardinalité. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-10"></a>
<a id="exercice-10"></a>

## Exercice 10 — Exploiter et maintenir

**Attendus à argumenter.** Day-2 désigne les opérations après la première installation : mises à jour, dérive, accès, capacité et qualité des données. Une maintenance possède un état initial, un risque, un retour et un contrôle métier. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Fiche avant/action/après, risque justifié, version et vérifications ; aide reçue déclarée.

**Vérification raisonnée.** Comparer le premier écart à l’état de référence, isoler une cause et confirmer le retour avec le parcours témoin. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Mettre tout à jour pour rendre un scan vert ; confondre retour d’image et retour de schéma ; changer plusieurs couches d’un coup. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-11"></a>
<a id="exercice-11"></a>

## Exercice 11 — Sauvegarder et restaurer

**Attendus à argumenter.** Une sauvegarde doit permettre une restauration utile. Pour OpsDesk, les tickets résident dans PostgreSQL ; aucune pièce jointe ni média utilisateur n’est géré. Le dump, le schéma et les versions doivent être cohérents ; les paramètres et secrets nécessaires à la reconstruction sont conservés séparément et protégés. Âge de capture, perte réellement observée et durée de reprise sont des mesures distinctes. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Intégrité contrôlée, mêmes références métier et mesures expliquées ; source préservée et limites explicites.

**Vérification raisonnée.** Identifier version, archive, clé, espace, accès, ordre de restauration PostgreSQL et de reconstruction de la configuration et référence attendue ; arrêter sur cible ou archive ambiguë. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Stocker clé et archive au même endroit en parlant de hors-site ; oublier la configuration et les versions nécessaires pour relire la DB ; prétendre cohérence sous écritures continues non testée. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-12"></a>
<a id="exercice-12"></a>

## Exercice 12 — Diagnostiquer et rétablir

**Attendus à argumenter.** Diagnostiquer consiste à éliminer des hypothèses avec des vérifications discriminantes. Rétablir exige un contrôle utilisateur après la correction ; une commande sans erreur n’est pas la fin de l’incident. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Symptôme, preuves, cause confirmée ou inconnue, correction, résultat métier et retour documentés.

**Vérification raisonnée.** Utiliser symptôme→couche→faits→hypothèse→test→correction→contrôle ; demander une aide précise si une donnée manque. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Réinstaller avant de lire les logs ; provoquer une panne hors périmètre ; appeler cause racine la première hypothèse plausible. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.


<a id="exercice-13"></a>
<a id="exercice-13"></a>

## Exercice 13 — Démontrer son autonomie

**Attendus à argumenter.** L’autonomie se constate sur une tâche nouvelle : comprendre le besoin, adapter une méthode, vérifier et expliquer. Un pipeline vert ou un fichier généré par Codex ne donne pas un niveau personnel. Pour OpsDesk, la preuve utile porte sur un ticket identifié, son titre et son état. Démonstration personnelle sur un cas proche nouveau, diagnostic et justification ; conclusion qualitative argumentée.

**Vérification raisonnée.** Décrire le blocage et les observations avant de demander une correction ; conserver ce qui a fonctionné et revoir une hypothèse à la fois. Une cause reste hypothétique tant que le contrôle ne l’a pas discriminée. Une autre architecture est recevable si elle respecte le contrat, les droits, la persistance et les critères.

**Points à refuser.** Recopier une référence puis revendiquer L3 ; cacher l’aide reçue ; inventer une note de certification. Un fichier de référence ou un PASS Codex n’établit ni exécution ni autonomie personnelles.

**Après la tentative.** Demander d’expliquer une décision, de montrer le test final et de proposer l’adaptation à un cas proche. Si nécessaire, donner une correction ciblée, puis laisser Mathias refaire le contrôle. Aucune configuration Terraform/Ansible/Docker/K3s/CI complète n’est fournie par ce repère.

**Conclusion qualitative à renseigner après l’épreuve :** Autonome sur l’exercice évalué ; Réussite avec assistance ; ou Compétence à retravailler. Justifier compréhension, méthode, qualité, vérification, diagnostic, sécurité, explication et aide utilisée ; aucun score de certification.
