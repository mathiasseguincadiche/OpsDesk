# Infrastructure : contrat local et candidat K3s

> **HISTORIQUE — référence non exécutable depuis le dépôt courant.** Au contrôle de `main` du 4 novembre 2026 (`51e1a489`), `infra/terraform/`, `infra/ansible/`, `infra/verify.py`, `infra/verify_k8s.py` et `k8s/` sont absents. Les blocs de commandes conservent les anciennes instructions pour comprendre l’essai Ubuntu/WSL ; ils ne sont pas prêts à copier et ne lancent pas le laboratoire personnel. Les versions et résultats qui suivent sont historiques. [Parcours actif](apprentissage/README.md) · [Pré-checks Fedora/KVM/Rocky](laboratoire-fedora-kvm-rocky.md).

## Référence historique — laboratoire de développement

Les procédures et résultats ci-dessous datent des essais historiques ; ils ne sont pas relancés. Les configurations et opérations InfraOps sont à réaliser personnellement ([contrat applicatif](contrat-applicatif.md), [provenance](provenance.md)). Les niveaux techniques de ce texte suivent un ancien barème et ne sont pas les niveaux personnels du [parcours](parcours-apprentissage.md). Les preuves de reprise récentes sont datées dans [STATUS](../STATUS.md).

## Ce qui a été exécuté, et à quoi cela sert

Avant de créer une machine, il faut s’accorder sur la cible : service, port, dépendance et exposition. `infra/terraform/main.tf` formalise ce **contrat non secret** avec la ressource intégrée `terraform_data`. Cette ressource conserve des données dans l’état Terraform ; elle ne crée ni VM, ni conteneur, ni réseau. [Référence HashiCorp](https://developer.hashicorp.com/terraform/language/resources/terraform-data).

`infra/ansible/render.yml` lit le résultat et produit `.local/ansible/opsdesk-contract.json`. Ansible utilise une connexion locale, sans élévation de privilèges, et ne change aucun paquet, service ou fichier système. Le fichier de modèle ne contient pas de secret. Un second passage sans changement vérifie l’idempotence de **ce rendu** ; il ne prouve pas la configuration ou la reconstruction d’un serveur Rocky. [Référence du module template](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html).

| Besoin métier / contrainte | Choix | Alternative écartée pour cette tranche | Test et portée |
|---|---|---|---|
| Partager une configuration lisible sans exposer le service | Contrat typé, boucle locale obligatoire | Provisionner un cloud sans budget ni accord | Bind public refusé au plan ; aucune ressource réseau créée |
| Répéter la configuration sans dérive | Modèle Ansible, JSON validé, seconde passe | Modifier directement un fichier sans critère | Deuxième rendu `changed=0` ; uniquement le fichier local |
| Apprendre state/plan/apply | Backend local ignoré de Git, aucun secret dans le contrat | Fausse VM ou fournisseur `null` présenté comme un provisionnement | Deuxième apply et plan sans changement ; aucune VM |
| Préparer le cluster sans toucher un contexte existant | Manifests et rendu Kustomize hors ligne | Déployer dans le contexte par défaut non qualifié | Treize objets rendus ; aucune preuve d’admission ou d’exécution |

## Ancienne procédure de contrat — lecture après tentative

Pré-check : poste de travail autorisé, Terraform ≥1.6 et <2, Ansible core, Python 3 et répertoire du dépôt accessible en écriture. La preuve actuelle utilise Terraform **1.15.8** et Ansible core **2.20.1** sur Ubuntu/WSL. Aucune connexion réseau de provisionnement n’est nécessaire ; le fournisseur Terraform est intégré.

Commande historique depuis la racine du laboratoire Ubuntu/WSL, sans élévation ; elle écrivait états, plans, logs et JSON locaux. Script absent du dépôt courant :

```bash
python3 infra/verify.py
```

Le script historique lançait `fmt`, `init`, `validate`, `plan`, `apply`, un deuxième `apply`, un deuxième `plan`, un cas négatif puis le contrôle de syntaxe et les deux rendus Ansible. Il conserve états/plans/logs dans `.local/terraform/`, les rendus dans `.local/ansible/`, et une synthèse non secrète dans [automation-contract.json](../evidence/automation-contract.json).

Critères : second apply `0 added, 0 changed, 0 destroyed` ; second plan code 0 ; second rendu `changed=0 unreachable=0 failed=0` ; une tentative `bind_address=0.0.0.0` doit être refusée au plan. Une variable refusée constitue un contrôle réussi, pas une exposition réseau.

L’état local et le répertoire `.terraform` ne sont pas publiés. Ils ne contiennent ici que le contrat non secret ; ne pas y ajouter de mot de passe. Les droits du montage NTFS/WSL ne qualifient pas des ACL Linux pour de vrais secrets. Un futur backend distant exigera contrôle d’accès, chiffrement, verrouillage, versionnement et une procédure de reprise adaptés.

## Diagnostic observé : Ansible ne peut pas créer son répertoire temporaire

Le premier rendu a échoué avant toute génération : `localhost unreachable=1`, le répertoire temporaire par défaut sous le HOME n’étant pas accessible à l’exécution. Définir `ANSIBLE_LOCAL_TEMP` ne change que le temporaire du contrôleur. L’inventaire de référence définissait **`ansible_remote_tmp` vers un répertoire dédié sous `/tmp`** pour cette connexion locale. La seconde exécution passe sans modification du HOME ni service hôte.

[Échec initial conservé](../evidence/automation-first-attempt.json) · [Revalidation et limites](../evidence/automation-contract.json).

## Ce que le candidat K3s contient

Les ressources historiques de `k8s/` ont été **rapportées IMPLÉMENTÉES et rendues hors ligne ; NON EXÉCUTÉES sur cluster**. Le dossier est absent du dépôt courant ; la disponibilité de ses originaux hors dépôt est NON VÉRIFIÉE à ce jour. Aucun manifeste ne publie de NodePort, LoadBalancer ou Ingress. L’application sans authentification est destinée à un accès local temporaire sur un laboratoire dédié.

| Fichier | Rôle et prérequis |
|---|---|
| `kustomization.yaml` | Assemble namespace et treize objets ; ne contacte aucun cluster lors du rendu |
| `namespace.yaml` | Namespace isolé et politique Pod Security `restricted` versionnée ; vérifier sa compatibilité avec la version réelle du cluster |
| `init-configmap.json` | SQL d’initialisation identique à `db/001-initial.sql` ; aucun mot de passe en clair |
| `runtime.yaml` | Un PostgreSQL StatefulSet/PVC, une Deployment app, deux Services internes et un compte runtime sans jeton monté |
| `policies.yaml` | Refus par défaut, flux app → DB, DNS et smoke → app ; dépend d’un CNI appliquant réellement NetworkPolicy |
| `delivery-rbac.yaml` | Identité de livraison limitée à l’app et aux lectures du namespace ; aucun droit d’écriture des Secrets, du StatefulSet ou des PVC |

L’application et PostgreSQL s’exécutent sous identités numériques non root avec capacités supprimées, seccomp et élévation de privilèges interdite. La racine est en lecture seule ; les chemins temporaires et les données ont des volumes distincts. Le stockage et l’UID PostgreSQL doivent être éprouvés sur le CSI réellement utilisé. [Référence des contextes de sécurité Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/).

Les images locales/taguées sont des candidats. Avant toute livraison, importer l’image construite et vérifiée ou remplacer son nom par un digest réellement accessible. La révision de travail de la première preuve ne devient pas un commit de livraison par ce remplacement.

## Ancien rendu hors cluster — lecture après tentative

Commande historique depuis la racine du laboratoire Ubuntu/WSL ; elle régénérait un fichier puis rendait les manifests sans contacter de cluster. Script et sources absents du dépôt courant :

```bash
python3 infra/verify_k8s.py
```

La preuve [k8s-static.json](../evidence/k8s-static.json) a été produite avec kubectl **1.36.2** / Kustomize **5.8.1**. Le YAML est lisible et les identités d’objets sont uniques. Ce contrôle n’inclut pas la validation du schéma par l’API, l’admission, le pull des images, la création des volumes ou l’application des politiques réseau.

Ce script régénère `k8s/init-configmap.json` à partir du fichier canonique `db/001-initial.sql`, rend les objets avec `kubectl kustomize k8s` et contrôle leurs identités/namespace. Il requiert PyYAML (fourni avec l’environnement Ansible de l’essai). Si le SQL change, relire la différence et le nouveau rendu. Éviter deux schémas DB divergents entre Compose et K3s.

## Pré-check obligatoire avant une future application

1. Nommer explicitement le cluster et la machine autorisés ; ne jamais employer par réflexe le contexte courant.
2. Contrôler version K3s/Kubernetes, nœuds, capacité, CNI/NetworkPolicy, StorageClass et droits du namespace. Aucun de ces résultats n’est acquis ici.
3. Fixer les images par contenu vérifié ; relire les ressources et la version Pod Security. Contrôler que les secrets n’existent que sur le laboratoire privé.
4. Préparer personnellement les fichiers secrets nécessaires à la cible, vérifier leur existence et leurs droits sans les imprimer ; aucune génération préalable n’est présumée. La base reçoit `db_owner_password` et `db_app_password` ; l’app reçoit uniquement `db_app_password` et `session_secret`.
5. Relire la différence et qualifier séparément le plan de sauvegarde/retour arrière. Une PVC n’est pas une sauvegarde ; la suppression du namespace/PVC est une destruction, hors du parcours normal.
6. Une fois le laboratoire autorisé, appliquer, attendre DB et app, contrôler live/ready/version, puis ouvrir/lire un ticket et vérifier les refus attendus. Capturer les sorties réelles avant tout statut VÉRIFIÉ.

Pour consulter sans ambiguïté une **future** cible, toutes les commandes doivent porter son nom, par exemple `kubectl --context="$LAB_CONTEXT" -n opsdesk-lab get pods`. Ce guide ne choisit pas la valeur de `LAB_CONTEXT` et ne déclenche aucune écriture distante.

## Livrer, diagnostiquer et revenir en arrière sur cette future cible

- Différencier processus app vivant et DB prête : startup/liveness portent sur `/health/live`, readiness sur `/health/ready`.
- Relier la version servie à l’image du Pod, puis au commit et au résultat de la chaîne de livraison.
- En cas de `ImagePullBackOff`, lire événements et nom/digest/permission de registre avant de changer un tag. En cas de `Pending`, vérifier d’abord PVC, capacité et admission ; en cas de readiness rouge, vérifier app → DNS `db` → port 5432 → rôle/schéma.
- Préparer v1 → v2 → retour à la même image v1, avec un ticket témoin conservé. Le rollback applicatif ne revient pas sur le schéma ni sur les écritures DB.
- Toute panne volontaire ou maintenance perturbatrice nécessite une cible isolée nommée, un état initial récupérable et la confirmation ciblée prévue par le mandat.

Ces exercices de cluster sont **NON EXÉCUTÉS**. Le [registre des cinq piliers](evaluations.md) conserve cette limite, même si le contrat Terraform/Ansible et le rendu Kustomize passent.
