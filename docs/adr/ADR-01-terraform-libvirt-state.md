# ADR-01 — Provisionnement local et état Terraform

**Statut : validé en conception (Architecture V3).** La réalisation dans le laboratoire reste à qualifier.

## Décision
L'hôte de virtualisation exécute directement Terraform et le provider adapté. Ansible s’exécute aussi sur Fedora, dans un environnement Python isolé ; les cycles restent distincts. Cloud-init amorce les VM (compte, clé publique, nom, prérequis minimaux). Des outputs filtrés génèrent l’inventaire hors Git ; attendre cloud-init et SSH avant Ansible. Aucune VM ne reçoit l’accès à libvirt. L'état de l'infrastructure, potentiellement sensible, est conservé hors du dépôt public et protégé.

La cible comporte exactement trois VM. Pour apprendre les bases, srv-admin est d’abord créée manuellement puis intégrée à Terraform par une méthode supportée et vérifiée ou recréée avant l’installation de la supervision. Inventorier les ressources existantes, protéger le state et ne pas créer de doublon ni détruire le réseau partagé.

## Justification
Ce découplage évite de donner à une machine virtuelle les privilèges de l'hyperviseur et limite les dépendances circulaires au démarrage.

## Alternatives
Un pilotage de l'hyperviseur depuis une VM et un backend d'état distant ont été étudiés, mais ne sont pas nécessaires au laboratoire mono-opérateur.

## Vérification prévue
Création reproductible, plan sans dérive inexpliquée, contrôle des permissions et restauration de l'état à partir d'une sauvegarde protégée.

**Périmètre public :** les accès précis, la topologie interne, les chemins, les identités et la procédure de reprise sont conservés dans la documentation personnelle.
