# 04 — Terraform : provider, ressources, state et cycle de vie

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 04, accessible sur invitation. Schéma : [le cycle Terraform](../diagrams/pedagogique-terraform.svg).

**Objectif.** Créer des machines virtuelles à partir de code, lire un plan avant de l'appliquer, et protéger le fichier d'état.

**Durée estimée** : 3 à 4 heures. **Prérequis** : `srv-admin` joignable (exercice 03) et sa liaison `qemu+ssh` vers libvirt de l'hôte (section 6.3 du [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md)). **État** : prévu, non vérifié.

## Pourquoi

Des machines créées à la main ne se refont pas à l'identique. Terraform remplace les clics par un fichier lisible et versionné, qui recrée les mêmes machines autant de fois que nécessaire.

## L'essentiel à comprendre

- Terraform compare trois choses : **ce que tu veux** (le code), **ce qu'il croit gérer** (le state) et **ce qui existe vraiment**. Le plan est la différence.
- On lit toujours le plan avant `apply` : `+` crée, `~` modifie sur place, `-/+` détruit puis recrée (risque de perte de données selon le cycle de vie et le stockage du disque ; vérifier le plan).
- Un second `plan` à `No changes` indique qu'aucun écart géré n'est détecté ; il ne prouve pas la disponibilité du service ni l'absence d'écarts non suivis.
- Le state ne va jamais dans Git et doit être copié hors de `srv-admin` : sans lui, Terraform peut proposer de recréer des ressources existantes. Ne pas appliquer un tel plan ; rechercher et vérifier l'état approprié.
- Le fournisseur `dmacvicar/libvirt` change beaucoup entre 0.8 et 0.9 : on fixe une version et on lit la documentation de cette version.
- Décision à prendre et à inscrire au registre avant de coder : image cloud et cloud-init, ou ISO et Kickstart.

## Cas voisin : un plan annonce un remplacement inattendu

**Exemple illustratif, non appliqué.** Sur une infrastructure de test sans données, un simple changement de paramètre produit `-/+` au lieu de `~`. Le symbole indique que Terraform prévoit **détruire puis recréer** la ressource ; il ne dit pas si un disque associé ou des données survivront.

**Démarche.** Avant `apply`, identifier la ressource, le champ déclencheur et le fournisseur/version concernés ; lire les conséquences sur les dépendances et le stockage ; comparer avec le besoin initial ; décider de corriger le code ou de préparer une migration séparée. Un second `plan` sans changement vérifie la convergence des ressources suivies, pas la disponibilité de l'application. Ce cas enseigne la lecture du plan sans fournir les fichiers des VM OpsDesk.

## Ce qu'il faut obtenir

| VM | vCPU | Mémoire | Disques | Adresse |
| --- | --- | --- | --- | --- |
| `srv-app` | 2 | 4 Go | 20 Go système + 10 Go de données | 192.168.150.10 |
| `srv-k3s` | 2 | 6 Go | 30 Go système | 192.168.150.20 |

Les deux sur `opsdesk-lan`, joignables en SSH depuis `srv-admin` par clé, compte `mathias`. `srv-admin` n'est pas gérée par Terraform.

Avant toute application : identifier dossier, backend/state, workspace et cible libvirt ; protéger une copie du state. Enregistrer avec `terraform plan -out=tfplan`, relire avec `terraform show tfplan`, puis appliquer le plan approuvé avec `terraform apply tfplan` seulement s'il reste valide. Le plan peut contenir des secrets : ne pas le versionner.

**Livrable** : le code (sans state), le plan commenté ligne par ligne, la sortie de l'`apply`, un second `plan` à « No changes », la preuve SSH des deux VM, et l'emplacement de la copie du state.

## Vérifications

| Ce que tu vérifies | Commande | Résultat attendu |
| --- | --- | --- |
| Les VM existent | `virsh … list --all` | `srv-app` et `srv-k3s`, `running` |
| Terraform les connaît | `terraform state list` | Aucune ressource pour `srv-admin` |
| Code et réalité concordent | `terraform plan` | `No changes.` |
| VM joignables | `ssh mathias@192.168.150.10 hostname`, puis `.20` | `srv-app`, puis `srv-k3s` |
| Disque de données | `lsblk` sur `srv-app` | Un second disque de 10 Go |
| State protégé | `git status` ; copie hors VM | Aucun `.tfstate` suivi ; une copie datée |

## Pièges fréquents

Appliquer un plan qui annonce un remplacement sans l'avoir compris ; lancer `terraform` depuis le mauvais dossier ; lever un verrou avec `force-unlock` pendant qu'une autre exécution tourne ; lire la documentation d'une autre version du fournisseur.

Suite : [exercice 05](05-ansible.md).
