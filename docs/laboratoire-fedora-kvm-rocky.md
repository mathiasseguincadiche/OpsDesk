# Préparer le laboratoire Fedora 45 → KVM/libvirt → Rocky Linux 10.2

**Document préparatoire V4.4 — 4 novembre 2026.** Les procédures ci-dessous sont à réaliser personnellement par Mathias, sur son PC identifié. Elles n’ont pas été exécutées sur Fedora ou dans une VM par Codex. Le contenu existant des projets reste conservé ; ce guide remplace les anciennes étapes de démarrage basées sur des ZIP, un script de publication ou le laboratoire WSL.

L’objectif est une première VM utilisable et comprise, puis les exercices du projet. La lecture du guide n’attribue aucun résultat personnel, niveau L0–L3 ou autonomie. Aucun Terraform, playbook Ansible, Dockerfile, fichier Quadlet, manifeste K3s ou pipeline complet n’est fourni ici.

## 1. Identifier les rôles avant de lancer une commande

- **Fedora 45 / GNOME 51 est l’hôte physique.** Il porte le bureau, KVM, QEMU, libvirt, virt-manager et les outils de contrôle choisis.
- **Rocky Linux 10.2 est l’invité.** Chaque VM possède son propre système, disque virtuel, utilisateur, réseau et services. Les composants applicatifs du projet y seront préparés lors des exercices correspondants.
- **KVM** donne au noyau Linux l’accélération de virtualisation matérielle. **QEMU** exécute la VM et présente son matériel virtuel. **libvirt** fournit une API et gère les ressources ; **virt-manager** est son interface graphique. Un outil présent ne prouve pas que toute cette chaîne fonctionne.
- **WSL et les conteneurs historiques de Codex sont des essais antérieurs distincts.** Un résultat Ubuntu/WSL ne valide pas Fedora 45, Rocky Linux 10.2, un réseau KVM ou les compétences de Mathias.

Fedora 45 a été annoncé officiellement le 3 novembre 2026 ; GNOME 51 est publié depuis septembre. Rocky Linux 10.2 et son ISO minimal sont disponibles. Cela confirme des versions distribuées, pas leur installation sur ton PC. [Fedora 45](https://fedoramagazine.org/announcing-fedora-linux-45/), [GNOME 51](https://release.gnome.org/51/), [Rocky Linux 10.2](https://rockylinux.org/news/rocky-linux-10-2-ga-release).

**Un poste = une cible de commande.** `127.0.0.1` sur Fedora désigne Fedora ; la même adresse dans Rocky désigne la VM ; celle de WSL désigne encore un autre contexte. Une application liée à la boucle locale de la VM ne devient pas accessible depuis le navigateur Fedora. Plus tard, tu choisiras et justifieras un accès hôte→IP privée de VM avec une écoute et des règles limitées, ou un tunnel SSH. Aucun port n’est ouvert automatiquement par ce guide.

## 2. Pré-check de l’hôte Fedora — observation avant installation

Ouvre un terminal **sur le bureau Fedora du PC**, relève la date et nomme la machine. Exécute les contrôles un par un, lis leur résultat et garde une synthèse expurgée. Le tableau donne des résultats **attendus**, jamais des sorties réellement observées ici.

Les commandes libvirt/QEMU des lignes H07–H11 ne se lancent qu’après avoir vérifié leur présence en H05. Si la cible est Ubuntu/WSL, un conteneur ou une machine non identifiée, ne transforme pas ses résultats en pré-check Fedora.

| Contrôle et objectif | Commande sur Fedora | Résultat attendu | Interprétation accessible | Réaction si échec | État ici |
|---|---|---|---|---|---|
| H01 — Identifier distribution, noyau et architecture | `cat /etc/os-release` ; `uname -m` ; `uname -r` | Fedora 45, architecture correspondant au média choisi, noyau relevé | L’identité du système décide de la procédure applicable ; relever la version réelle, même différente de la cible | Conserver le constat ; résoudre la différence de cible avant une installation | NON EXÉCUTÉ |
| H02 — Identifier le bureau et le contexte physique | `gnome-shell --version` ; `systemd-detect-virt` | Génération GNOME 51 ; contexte physique attendu | GNOME n’est pas l’hyperviseur. Un contexte de virtualisation signalé peut nécessiter une analyse de virtualisation imbriquée | Ne pas changer de distribution ou de BIOS automatiquement ; identifier la vraie machine | NON EXÉCUTÉ |
| H03 — Vérifier CPU et virtualisation matérielle | `LC_ALL=C lscpu` ; `lsmod` ; `stat /dev/kvm` | CPU et fonctions de virtualisation visibles ; module KVM correspondant ; périphérique KVM accessible selon la politique locale | Le CPU physique, les options du firmware et l’accès au périphérique sont trois conditions différentes | Examiner firmware, modules et droits. Ne pas rendre `/dev/kvm` accessible à tous avec un chmod global | NON EXÉCUTÉ |
| H04 — Vérifier le niveau CPU nécessaire à Rocky 10 | `/lib64/ld-linux-x86-64.so.2 --help` | `x86-64-v3` marqué pris en charge/recherché sur x86_64 | Rocky 10 x86_64 exige ce niveau d’instructions ; le test devra être refait dans la VM | Si v3 n’est pas exposé, expliquer le blocage ; aucune substitution silencieuse vers Rocky 9/10.1 | NON EXÉCUTÉ |
| H05 — Distinguer paquets présents et outils disponibles | `rpm -q qemu-kvm libvirt-daemon-kvm libvirt-client virt-manager virt-install` ; `command -v virsh` ; `command -v virt-host-validate` ; `command -v qemu-system-x86_64` | Versions des paquets effectivement installés ; chemins des exécutables | « Not installed » est un manque identifié, pas une autorisation d’installer toute une pile. Un paquet disponible n’est pas un outil déjà installé | Relever uniquement les éléments absents puis examiner la transaction adaptée à Fedora 45 | NON EXÉCUTÉ |
| H06 — Identifier version DNF et paquets proposés | `dnf --version` ; si DNF5 : `dnf5 group info virtualization` et `dnf5 info --available qemu-kvm libvirt-daemon-kvm libvirt-client virt-manager virt-install` | Version du gestionnaire et paquets issus des dépôts Fedora attendus | DNF5 sépare groupes et environnements ; ne pas recopier une ancienne syntaxe sans vérifier l’aide | Si groupe absent, lire les paquets individuels et les dépôts ; ne pas activer un dépôt tiers au hasard | NON EXÉCUTÉ |
| H07 — Identifier l’organisation des services libvirt | `systemctl list-unit-files 'virtqemud*' 'virtnetworkd*' 'virtstoraged*' 'libvirtd*'` ; `systemctl status virtqemud.socket` | Unités réellement présentes et mode actif compréhensible | Un socket actif peut démarrer le démon à la demande. Un service inactif n’est pas forcément un défaut si son socket fonctionne | Lire le journal et le mode installé. Ne pas activer à la fois une pile modulaire et une pile libvirtd concurrente | NON EXÉCUTÉ |
| H08 — Tester la connexion de gestion autorisée | `id` ; `virsh --readonly --connect qemu:///system list --all` ; `virsh --readonly --connect qemu:///system version` | Accès autorisé à la connexion système, liste éventuellement vide | Une liste vide est normale avant création ; « permission denied » et « socket absent » ne se corrigent pas de la même façon | Contrôler authentification/polkit, unités et URI. Les droits de gestion libvirt sont puissants ; pas de contournement global | NON EXÉCUTÉ |
| H09 — Vérifier que KVM peut accueillir l’invité | `virt-host-validate qemu` ; `virsh --readonly --connect qemu:///system domcapabilities --virttype kvm --arch x86_64` | Prérequis KVM satisfaits et capacités de VM disponibles | Lire chaque PASS/WARN/FAIL ; un avertissement IOMMU pour du passthrough PCI n’est pas la même chose qu’un échec d’accélération KVM | Corriger uniquement un prérequis nécessaire. Ne pas activer passthrough, migration ou virtualisation imbriquée sans besoin | NON EXÉCUTÉ |
| H10 — Contrôler CPU et mémoire disponibles | `lscpu` ; `free -h` ; `vmstat 1 5` | Ressources disponibles compatibles avec la VM proposée, pression mémoire raisonnable | Le total RAM n’est pas la mémoire libre ; le swap ne remplace pas une réserve pour le bureau | Réduire le nombre de VM simultanées ou leur taille ; ne pas modifier la mémoire de services existants à l’aveugle | NON EXÉCUTÉ |
| H11 — Identifier stockage et espace réellement disponibles | `lsblk -f` ; `df -hT` ; `virsh --readonly --connect qemu:///system pool-list --all` ; puis `virsh --readonly --connect qemu:///system pool-dumpxml NOM_POOL_IDENTIFIE` | Pool, chemin et système de fichiers connus ; capacité libre et marge pour images, VM et logs | Un disque qcow2 peut croître jusqu’à sa capacité virtuelle. Les volumes et chemins par défaut ne sont pas supposés présents | Ne pas partitionner/formater. Choisir un stockage existant autorisé ou présenter le manque avant création | NON EXÉCUTÉ |
| H12 — Identifier réseau et collisions potentielles | `ip -brief address` ; `ip route` ; `nmcli connection show --active` ; `virsh --readonly --connect qemu:///system net-list --all` | Réseaux hôte/VPN/libvirt connus, aucune plage choisie en conflit | Un réseau nommé default n’est ni garanti présent ni garanti dans sa configuration d’origine | Lire `virsh --readonly --connect qemu:///system net-dumpxml NOM_RESEAU_IDENTIFIE`, justifier le profil ; ne pas modifier le réseau principal du PC | NON EXÉCUTÉ |
| H13 — Vérifier protections et zones effectives | `getenforce` ; `sestatus` ; `systemctl is-active firewalld` ; `sudo firewall-cmd --get-active-zones` | SELinux Enforcing et pare-feu actif dans la politique attendue | Les zones et interfaces sont plus utiles qu’une simple liste de ports sans contexte | Comprendre l’état et les règles ; ne pas désactiver globalement SELinux ou firewalld | NON EXÉCUTÉ |
| H14 — Diagnostiquer un refus après une tentative précise | `journalctl -b -u virtqemud --no-pager -n 50` ; `sudo ausearch -m AVC,USER_AVC -ts recent` | Événement lié à l’heure, au chemin et au processus concernés | Un refus SELinux doit être relié à un objet précis ; aucun AVC trouvé ne prouve à lui seul que tout fonctionne | Lire droits/contexte avec `ls -ldZ CHEMIN_IDENTIFIÉ`, puis comparer au contexte prévu ; pas de politique générée aveuglément | NON EXÉCUTÉ |

Les noms `NOM_POOL_IDENTIFIE`, `NOM_RESEAU_IDENTIFIE` et `CHEMIN_IDENTIFIÉ` sont des valeurs à relever et remplacer, pas des noms imposés. Les commandes après « puis » sont conditionnées au résultat précédent. Si `ausearch`, `nmcli`, `vmstat` ou un autre outil manque, noter le manque et rechercher son paquet ; ne pas inventer son résultat.

Les paquets Fedora 45 `qemu-kvm`, `libvirt-daemon-kvm`, `virt-manager` et `virt-install` existent dans les catalogues officiels. Après le pré-check seulement, examiner avec DNF les paquets absents et la transaction proposée, puis installer personnellement les éléments utiles. Exemple limité : si seul virt-manager manque, la commande à étudier est `sudo dnf install virt-manager`, pas une réinstallation de tout le groupe. Aucun ajout au groupe libvirt, activation de socket ou installation n’est exécuté par Codex. [Catalogues QEMU](https://packages.fedoraproject.org/pkgs/qemu/qemu-kvm/), [libvirt](https://packages.fedoraproject.org/pkgs/libvirt/libvirt-daemon-kvm/), [virt-manager](https://packages.fedoraproject.org/pkgs/virt-manager/virt-manager/), [DNF5](https://dnf5.readthedocs.io/en/stable/commands/group.8.html).

Les libvirt récents proposent des démons modulaires ; le mode installé doit être découvert avant une correction. Sur une pile modulaire dont les unités existent, `virtqemud.socket` concerne QEMU, `virtnetworkd.socket` les réseaux et `virtstoraged.socket` le stockage. Une activation éventuelle sera une action personnelle expliquée et ciblée après observation ; ce guide n’impose aucune migration d’un hôte déjà configuré. [Démons libvirt](https://www.libvirt.org/daemons.html), [connexion après installation](https://libvirt.org/kbase/failed_connection_after_install.html).

## 3. Proportionner le laboratoire et comprendre ses limites

L’observation CIM du PC sous Windows indique **Ryzen 7 7700, 8 cœurs et 16 threads et 48 Gio de RAM**. Elle ne prouve ni l’installation Fedora, ni l’accélération KVM sous Fedora. Les capacités de virtualisation signalées sous Windows/Hyper-V ne doivent pas être interprétées comme un test CPU négatif pour le futur hôte. L’espace NTFS observé n’est pas l’espace alloué au stockage Fedora.

**Proposition de départ à vérifier sur l’hôte : une seule VM Rocky Linux 10.2, 2 vCPU, 4 Gio RAM et 30 Gio de disque virtuel qcow2 à allocation progressive.** Il s’agit d’une hypothèse de dimensionnement, pas d’un minimum certifié. Laisser une marge pour Fedora, les autres usages, les caches d’images, les mises à jour et la croissance des données. Contrôler le chemin du pool avant de choisir le disque.

Une deuxième VM ne se justifie que lorsqu’un exercice demande deux cibles distinctes : promotion, reconstruction ou reprise en conservant la source. Les trois projets ne demandent pas trois laboratoires complets allumés simultanément. Pour K3s, prévoir plus tard son propre besoin : le minimum officiel du serveur, deux cœurs et 2 Go RAM, exclut la charge applicative. Mesurer aussi PostgreSQL, l’application et la supervision avant de choisir les ressources ; aucun cluster n’est présumé installé. [Exigences K3s](https://docs.k3s.io/installation/requirements).

| Profil réseau à comprendre | Usage possible | Limite et décision attendue |
|---|---|---|
| NAT libvirt | Accès sortant pour paquets et registres, accès privé hôte↔VM selon le réseau observé | Ne signifie pas isolement absolu : la VM peut joindre des réseaux externes. Vérifier les routes et conflits VPN ; aucun transfert de port public n’est nécessaire |
| Réseau isolé | Échanges entre cibles d’un exercice contrôlé sans routage sortant prévu | Les téléchargements et DNS publics ne seront pas automatiquement disponibles ; prévoir la préparation puis les contrôles attendus |
| Bridge vers le LAN | Besoin explicite d’une présence de la VM sur le réseau physique | Impact sur le réseau réel et exposition accrue ; ce choix n’est pas nécessaire au premier exercice et ne sera pas appliqué automatiquement |

Le profil sera choisi d’après le besoin, les réseaux déjà présents et les règles du PC. Aucun sous-réseau, bridge permanent ou configuration complète n’est imposé. [Réseaux libvirt](https://libvirt.org/formatnetwork.html).

Un **instantané** facilite un retour d’état dans certaines conditions ; il peut dépendre du disque d’origine. Il ne remplace pas une sauvegarde indépendante ni la cohérence PostgreSQL/médias. Une sauvegarde présente ne prouve pas une restauration, et une VM restaurée ne prouve pas le parcours métier. La reconstruction devra être démontrée sans supprimer la source existante. [Sauvegarde disque libvirt](https://www.libvirt.org/kbase/live_full_disk_backup.html).

## 4. Choisir et vérifier le média Rocky Linux 10.2

Pour une installation minimale x86_64, l’index officiel contient **`Rocky-10.2-x86_64-minimal.iso`** ainsi que son `.CHECKSUM` et sa signature `.CHECKSUM.asc`. Choisir ce nom exact dans le répertoire 10.2, avec la clé publique Rocky 10 liée par la page officielle. Ne pas utiliser un alias latest pour prouver une version figée. [Répertoire officiel des médias 10.2](https://download.rockylinux.org/pub/rocky/10.2/isos/x86_64/), [identité des clés](https://rockylinux.org/resources/gpg-key-info).

Télécharge personnellement le média et les petits fichiers de vérification dans un nouveau dossier identifié. Après avoir contrôlé la présence de `sha256sum`, `gpg` et `gpgv`, lis la clé publique et compare **l’empreinte complète**, pas seulement un nom d’utilisateur :

```sh
gpg --show-keys --with-fingerprint RPM-GPG-KEY-Rocky-10
```

L’empreinte publiée de la clé 10 est `FC226859C0860BF0DDB95B085B106C736FEDFC85`. Un nom « Rocky » affiché ne suffit pas à l’identifier. Pour vérifier la signature dans une clé publique dédiée, sans importer la clé dans ton trousseau habituel :

```sh
gpg --batch --dearmor --output rocky10-verification.gpg RPM-GPG-KEY-Rocky-10
gpgv --keyring ./rocky10-verification.gpg Rocky-10.2-x86_64-minimal.iso.CHECKSUM.asc Rocky-10.2-x86_64-minimal.iso.CHECKSUM
sha256sum --check Rocky-10.2-x86_64-minimal.iso.CHECKSUM
```

Exécute chaque commande seulement si la précédente a réussi. Le fichier `rocky10-verification.gpg` doit être nouveau : ne remplace pas un trousseau existant. Le contrôle attendu est d’abord une signature valide de la clé identifiée, puis le nom exact de l’ISO avec le résultat `OK`. En cas d’empreinte ou de somme différente, conserver l’écart et ne pas démarrer l’installation ; rechercher un téléchargement incomplet, une mauvaise version ou une mauvaise source. Ne pas supprimer le contrôle pour avancer.

**Portée du contrôle Codex :** seules les métadonnées publiques de la version 10.2 ont été téléchargées et la signature du CHECKSUM vérifiée avec gpgv. Le média utilisateur n’a pas été téléchargé, son intégrité n’a pas été vérifiée et aucune VM n’a été créée. Mathias doit donc exécuter ses propres contrôles du média. Le guide d’installation générique Rocky consulté contient encore un exemple 10.1 ; il explique la méthode mais ne change pas notre cible 10.2. [Méthode officielle d’installation](https://docs.rockylinux.org/guides/installation/).

## 5. Préparer personnellement une première VM dans virt-manager

Cette procédure prépare le support de travail. Elle ne réalise pas l’architecture OpsDesk complète. Avant chaque validation, lire le récapitulatif et conserver ses choix :

1. **Choisir la connexion.** Ouvrir virt-manager et identifier la connexion QEMU/KVM système contrôlée en H08. Si les VM attendues sont absentes, vérifier `qemu:///system` contre `qemu:///session` ; ne pas les recréer pour contourner une mauvaise connexion.
2. **Créer une nouvelle VM de laboratoire.** Donner un nom personnel explicite et vérifier qu’aucune ressource existante n’a ce nom. Sélectionner le média 10.2 dont l’intégrité vient d’être contrôlée. Si la détection du système ne connaît pas le libellé10.2, relever ce point et vérifier les capacités/osinfo ; ne pas annoncer une version 9 ou 10.1 à la place.
3. **Affecter les ressources.** Examiner l’hypothèse 2 vCPU/4 Gio/30 Gio, les ressources libres mesurées et l’espace du pool choisi. La taille virtuelle du disque ne dispense pas de surveiller sa croissance physique. Ne choisir aucun disque physique existant à écraser.
4. **Personnaliser avant de commencer.** Vérifier accélération KVM, CPU virtuel, disque, carte réseau et firmware proposés. Un modèle générique trop ancien peut masquer x86-64-v3. Comparer `host-model` et `host-passthrough` à partir des capacités observées ; justifier le choix et refaire le test CPU dans l’invité. Le passthrough peut limiter la portabilité vers un autre CPU. [Capacités CPU libvirt](https://www.libvirt.org/formatdomaincaps.html).
5. **Choisir le réseau.** Utiliser le profil privé/NAT existant identifié et adapté à la phase de préparation, ou présenter un autre choix motivé. Relever le nom du réseau et la méthode d’adressage. Le nom de l’interface dans Rocky et l’adresse attribuée seront observés, pas devinés.
6. **Installer Rocky Linux 10.2.** Choisir une installation serveur minimale pour éviter une charge graphique inutile. Vérifier dans l’installateur que le disque sélectionné est le **nouveau disque virtuel de cette VM**. Les réglages de langue, fuseau, nom d’hôte et stockage doivent être relus ; la procédure ne modifie pas les partitions du PC.
7. **Créer un utilisateur ordinaire.** Choisir une identité personnelle avec les droits d’administration utiles. Conserver les identifiants hors Git et hors preuves publiques. Revoir un besoin sudo ne signifie pas travailler en root en permanence.
8. **Contrôler la première session.** Démarrer la VM et exécuter l’inventaire invité ci-dessous. Garder une console disponible avant d’adapter SSH ou le réseau. Vérifier les services réellement présents avant une activation.
9. **Mettre à jour et qualifier.** Dans cette VM nouvellement identifiée, examiner les mises à jour et la transaction DNF, puis les appliquer personnellement à un moment choisi. Noter versions avant/après et éventuel besoin de redémarrage. Refaire les contrôles de l’invité après le redémarrage. Ne pas prétendre qu’un noyau cité dans une note de sortie est le noyau corrigé installé.

La configuration de la VM reste un choix personnel à expliquer. Ce guide ne fournit pas un XML libvirt final, un Kickstart complet ou une ressource Terraform à recopier.

## 6. Contrôler l’invité et préparer l’accès sans contourner les protections

Après connexion à la console de **cette VM Rocky**, contrôler d’abord son identité. Les commandes de gestion d’hyperviseur restent sur Fedora ; celles du tableau suivant sont pour Rocky :

| Objectif | Commandes dans Rocky | Attendu et lecture du résultat | Si le résultat diffère |
|---|---|---|---|
| Identité et CPU invité | `cat /etc/os-release` ; `uname -m` ; `uname -r` ; `lscpu` ; `/lib64/ld-linux-x86-64.so.2 --help` | Rocky Linux 10.2 et x86-64-v3 exposé ; noter le noyau réel | Revoir le modèle CPU/capacités en conservant la VM ; ne pas changer silencieusement la distribution |
| Compte, sudo, heure | `id` ; `sudo -l` ; `timedatectl status` | Compte ordinaire, droits compris, heure cohérente | Corriger le besoin précis depuis une console autorisée ; ne pas publier les identifiants |
| Réseau réellement attribué | `ip -brief address` ; `ip route` ; `nmcli device status` | Interface, adresse et route conformes au profil choisi | Séparer lien, DHCP/adresse, routage et pare-feu. Ne pas supposer `eth0`, `ens3` ou une adresse fixe |
| Résolution de noms | `getent ahosts download.rockylinux.org` | Résolution fonctionnelle si le profil doit joindre les dépôts publics | Si réseau isolé sans DNS public prévu, noter « non applicable ». Sinon distinguer défaut DNS et route ; ne pas utiliser ping comme seul diagnostic |
| Outils et dépôts | `rpm -q openssh-server firewalld policycoreutils python3` ; `dnf --version` ; `dnf repolist` ; `python3 --version` | Paquets/versions/dépôts réellement présents | Les paquets manquants sont à examiner. Le Python système 3.12 ne vaut pas qualification d’OpsDesk testé sous 3.14 |
| Service SSH | `systemctl list-unit-files 'sshd*'` ; `systemctl status sshd` ; `sudo sshd -t` ; `ss -lnt` | Service/unité identifié, configuration valide, écoute attendue | Contrôler paquet, configuration puis service. Une écoute sans droit réseau ne démontre pas l’accès hôte→VM |
| Sécurité et ressources | `getenforce` ; `sestatus` ; `systemctl is-active firewalld` ; `sudo firewall-cmd --get-active-zones` ; `free -h` ; `df -hT` | Protections actives et marge cohérente avec la VM | Diagnostiquer zone/flux, permissions/contexte ou saturation au lieu de désactiver les protections |

Si SSH n’est pas installé, aucune sortie de `sshd -t` n’est attendue : examiner le paquet nécessaire avant la suite. Avant la première connexion depuis Fedora, relever **dans la console de la VM** l’empreinte de sa clé d’hôte publique, par exemple `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` si cette clé existe. La comparer au message affiché lors de la connexion à l’IP relevée. En cas d’empreinte changée, vérifier qu’il s’agit bien de la cible reconstruite ; ne pas supprimer automatiquement les anciennes entrées de confiance.

L’accès par clé personnelle et les règles permettant SSH seront proposés et réalisés par Mathias sur la VM identifiée, en gardant la console et une session de secours jusqu’à revalidation. Aucun secret existant n’est remplacé ; la clé privée n’est jamais ajoutée au dépôt ni aux preuves.

Pour un refus, suivre l’ordre **symptôme → observation → hypothèses → test discriminant → cause connue ou encore inconnue → correction ciblée → validation**. Un `ls -ldZ` permet de voir droits et contexte ; `ausearch` retrouve un AVC récent ; `audit2why` peut aider à l’expliquer s’il est présent. Utiliser une règle de contexte attendue et le mécanisme `restorecon` adapté au seul chemin identifié ; ne pas générer une politique d’autorisation globale à partir de tous les refus. Pour firewalld, relever zone/interface/source/port avant de proposer une règle minimale. [SELinux dans Rocky](https://docs.rockylinux.org/guides/security/learning_selinux/).

Pour vérifier les mises à jour dans la VM identifiée, `dnf check-update` renvoie 0 si aucune mise à jour n’est proposée, 100 si des mises à jour sont disponibles, et un autre code à interpréter en cas d’erreur. Lire ensuite la transaction de `sudo dnf upgrade` avant de la confirmer ; cette opération personnelle ne doit viser que la VM choisie. Le code 100 de la consultation n’est pas un échec d’installation. [Référence DNF](https://dnf.readthedocs.io/en/latest/command_ref.html#check-update-command).

Depuis Fedora, après vérification de l’empreinte et de l’adresse, la connexion s’étudie sous la forme `ssh UTILISATEUR@IP_VM_RELEVEE` : remplacer ces deux repères par le compte et l’adresse réellement observés. Un refus de connexion, un nom non résolu et un refus d’authentification sont trois symptômes différents.

## 7. Vérifier la compatibilité au moment du module concerné

Ce tableau conserve les technologies choisies. Il ne transforme pas une disponibilité documentaire en logiciel déjà installé ou en compatibilité entièrement testée.

| Composant | Fait documentaire vérifié au 4 novembre 2026 | Contrôle personnel et limite |
|---|---|---|
| Fedora 45/KVM/QEMU/libvirt | Paquets officiels Fedora 45 disponibles ; libvirt propose les sockets modulaires | Relever versions RPM, mode des unités, accès autorisé, capacités et test invité. Combinaison complète **NON EXÉCUTÉE** ici |
| Rocky Linux 10.2 | Média exact disponible ; baseline Rocky 10 x86-64-v3 ; noyau de la famille 6.12 | Contrôler signature, somme du propre ISO, CPU invité, noyau et mises à jour. Aucun résultat Windows/WSL transféré |
| Docker Engine — OpsDesk/BankFlow | Docker documente RHEL 10 et CentOS Stream 10 ; sa page précise que les dérivés ne sont pas vérifiés par Docker | Compatibilité exacte Rocky Linux 10.2 **PARTIELLE**. Contrôler dépôt/versions, conflits éventuels dont podman-docker, réseau, SELinux, DB et parcours métier avant de recevoir le module. Ne pas remplacer Docker par Podman à l’insu de Mathias. [Plateformes](https://docs.docker.com/engine/install/), [RHEL](https://docs.docker.com/engine/install/rhel/) |
| Podman — LogiTrack | Podman 5.8.2 est publié dans Rocky Linux 10.2 ; documentation rootless correspondante disponible | Vérifier `podman --version`, `podman info`, identité sans sudo, `/etc/subuid`/`subgid`, cgroups et stockage local. Les conteneurs root et utilisateur sont distincts. Aucun alias docker=podman. [Manuel5.8.2](https://docs.podman.io/en/v5.8.2/markdown/podman.1.html) |
| Terraform | CLI Linux proposée officiellement ; provider KVM `dmacvicar/libvirt` communautaire ; la branche 0.9 est une réécriture de 0.8 | Choisir/verrouiller CLI et provider, lire leur schéma et le plan. `terraform_data` historique ne provisionne aucune VM. Aucun apply exécuté et aucun HCL final livré. [CLI](https://developer.hashicorp.com/terraform/install), [provider](https://github.com/dmacvicar/terraform-provider-libvirt) |
| Ansible | Fedora 45 utilise Python 3.15. La matrice core 2.21 ne couvre que Python contrôleur 3.12–3.14 ; la série 2.22 couvre contrôleur 3.13–3.15 et cibles 3.9–3.15 | Vérifier `python3 --version`, `ansible --version`, `rpm -q ansible-core` et le dépôt du paquet choisi. Les index Fedora consultés distinguent des builds bêtas et les canaux stable/testing ; leurs instantanés diffèrent. Vérifier le paquet réellement proposé et ne pas présumer une version finale déjà stable, ni activer testing automatiquement. Choisir une combinaison publiée et prise en charge, ou un environnement de contrôle Python compatible, puis qualifier collections/SSH/idempotence ; aucune compatibilité locale présumée. [Paquet Fedora](https://packages.fedoraproject.org/pkgs/ansible-core/ansible-core/), [matrice 2.22](https://docs.ansible.com/projects/ansible-core/2.22/reference_appendices/release_and_maintenance.html) |
| K3s | Exigences RHEL 10 documentées, dont `kernel-modules-extra` ; ressources minimales hors charges applicatives ; politiques SELinux nécessaires | Choisir une version, vérifier modules/noyau, politique et ports du mode réseau retenu. Les exemples de politique el9 et anciens correctifs RHEL < 8.4 ne sont pas automatiquement des étapes Rocky Linux 10.2. Conserver firewalld avec des règles ciblées ; aucun cluster présumé. Compatibilité exacte **PARTIELLE**, installation **NON EXÉCUTÉE**. [Prérequis](https://docs.k3s.io/installation/requirements), [SELinux](https://docs.k3s.io/advanced) |
| BorgBackup | Paquet 1.4.5 disponible dans EPEL 10.2 et méthode d’installation documentée | Vérifier dépôt choisi, version et compatibilité des archives. Le dépôt EPEL n’est pas supposé activé. Créer sauvegarde et reprise sera un exercice de Mathias, pas une commande de préparation générale. [Paquet](https://packages.fedoraproject.org/pkgs/borgbackup/borgbackup/), [amont](https://borgbackup.readthedocs.io/en/stable/installation.html) |
| Application/Python/PostgreSQL | Contrats V4.4 : OpsDesk testé Python 3.14.10 ; BankFlow 3.12.16 ; InvenTree 1.7.0 sur 3.14.10 ; PostgreSQL 17.11 utilisé dans ces essais | La disponibilité Python 3.12/3.14 ou PostgreSQL 18 dans Rocky ne prouve pas la réception de l’application sur ces combinaisons. Conserver les versions du contrat ou faire qualifier explicitement un changement ; pas d’upgrade majeur DB implicite |

Une réserve spécifique est conservée pour K3s : dans [l’installateur amont inspecté à un commit figé](https://github.com/k3s-io/k3s/blob/2b723db54007ab1509fc86ee2712ecc93cc49843/install.sh#L621), Rocky 10.2 passe dans la sélection par défaut `el9` pour la politique SELinux. C’est une lecture de source, pas une preuve d’incompatibilité du paquet ni un test d’installation. Avant d’exécuter ce module, vérifier la version choisie et une politique effectivement applicable à Rocky 10.2 ; à défaut, reporter cette installation en NON EXÉCUTÉ plutôt que désactiver SELinux ou remplacer la distribution.

La qualification InvenTree 1.7.0 couvre huit tests backend/HTTP Django et les contrôles de quantités ; le rendu JavaScript complet reste non qualifié. L’instance historique 1.6.3 n’est pas une preuve de réception 1.7.0. Les verdicts sécurité FAIL conservés ne sont pas transformés en PASS par le changement de VM ou de documentation.

## 8. Recevoir le laboratoire avec des preuves interprétées

Remplis personnellement une ligne de preuve pour chacun des contrôles utiles : date, cible, version, commande réellement exécutée, résultat attendu, résultat observé, interprétation, correction éventuelle, dernier contrôle, assistance et limite. Ne remplis pas PASS par anticipation et ne déplace aucun statut Notion pour la seule lecture d’une fiche.

| Contrôle de réception | Ce qu’il doit démontrer | Résultat personnel à renseigner |
|---|---|---|
| Identité | Hôte Fedora 45 et invité Rocky Linux 10.2 correctement distingués ; VM et utilisateur nommés | NON EXÉCUTÉ |
| Accélération et CPU | KVM utilisable ; CPU virtuel réellement compatible avec x86-64-v3 | NON EXÉCUTÉ |
| Démarrage | Premier démarrage puis redémarrage personnel de la nouvelle VM à un moment choisi ; accès retrouvé sans modifier une source existante | NON EXÉCUTÉ |
| Réseau | Adresse, route et flux hôte↔VM conformes au réseau choisi ; DNS seulement lorsqu’il est attendu | NON EXÉCUTÉ |
| SSH et droits | Empreinte de cible contrôlée ; utilisateur prévu connecté depuis Fedora ; sudo justifié | NON EXÉCUTÉ |
| Sécurité | SELinux et pare-feu actifs ; règles adaptées au seul besoin, refus interprétés si rencontrés | NON EXÉCUTÉ |
| Ressources | RAM, stockage et charge suffisants pour ce qui est effectivement lancé ; marge notée | NON EXÉCUTÉ |
| Versions | Outils installés et applicatifs prévus relevés séparément ; compatibilités restantes déclarées | NON EXÉCUTÉ |
| Reconstruction | Méthode documentée puis reproduite, lorsqu’autorisé, sur une seconde cible distincte, avec source conservée ; mêmes contrôles d’accès et de système | NON EXÉCUTÉ |
| Réception métier | Plus tard seulement : service et données fictives du projet contrôlés selon son contrat, au-delà d’un HTTP 200 ou d’un processus vivant | NON EXÉCUTÉ |

Un état reproductible commence par tes notes du média, versions, paramètres de VM, réseau, utilisateur, paquets et contrôles. Certains journaux de l’installateur et fichiers Kickstart peuvent contenir des secrets ou hashes de mots de passe : conserver le nécessaire en privé, ne pas les publier bruts. L’automatisation complète de cette reconstruction viendra dans tes modules Terraform/Ansible.

Si la seconde cible n’a pas été créée et testée, le statut reconstruction reste **NON EXÉCUTÉ** ; la procédure peut être prête sans que le laboratoire soit totalement reçu. Ne pas supprimer la première VM, ses disques ou ses sauvegardes pour fabriquer une preuve.

## 9. Utiliser les dépôts et commencer le parcours

Les dépôts vérifiés sont [OpsDesk](https://github.com/mathiasseguincadiche/OpsDesk), [BankFlow](https://github.com/mathiasseguincadiche/BankFlow) et [LogiTrack](https://github.com/mathiasseguincadiche/LogiTrack). Ils restent indépendants ; ce guide commun porte uniquement sur la préparation hôte/VM, sans architecture applicative multi-dépôts.

GitHub est la plateforme principale : utilise le dépôt réel indiqué dans l’accueil Notion ou le README du projet, après vérification de son URL, de la branche et de la révision. **Un seul dépôt principal par projet.** Aucun ancien ZIP, script de publication ou commande créant un nouveau dépôt public n’est requis. `git --version` permet de vérifier Git ; GitHub CLI n’est pas un prérequis automatique. Une URL SSH demande une clé déjà configurée ; HTTPS suit la méthode d’authentification choisie, jamais un mot de passe/token stocké dans une URL.

GitLab reste entièrement en l’état pendant cette mission. Aucun miroir ni synchronisation n’est créé. Les anciens supports GitLab sont des références historiques facultatives ; la chaîne active étudiée dans cette préparation est GitHub Actions.

Tu peux commencer **OpsDesk — Exercice personnel V4.4 n°1 : comprendre l’application** avant toute création de VM : ouvrir [l’énoncé actif](apprentissage/01-application.md), lire [le contrat](contrat-applicatif.md), identifier le trajet d’une demande et les données durables, puis formuler tes questions. Le schéma cible personnel appartient à l’étape d’architecture suivante. Les seize supports théoriques OpsDesk sont des ressources ; les treize exercices V4.4 sont l’ordre de travail prioritaire. Le corrigé se consulte après une tentative.

AWS et les objectifs cloud utiles sont conservés séparément. Ils ne sont pas des prérequis cachés aux premiers exercices KVM. Toute ressource payante ou exposition réelle demandera un besoin et une décision explicites ; ce guide n’en crée aucune.

## 10. Statut documentaire et prochaines actions

La procédure et les compatibilités documentaires sont préparées ; les contrôles du PC Fedora et de la première VM restent **NON EXÉCUTÉS**. La seule vérification technique de cette préparation concerne la signature de métadonnées publiques Rocky Linux 10.2, dans un contexte Codex distinct.

Pour la séance de préparation, Mathias identifiera d’abord Fedora et les ressources, exécutera les pré-checks et expliquera les écarts avant toute modification. Codex pourra relire les observations et aider au blocage précis. Ensuite seulement, Mathias créera personnellement la VM et en apportera les preuves. La présence de ce document, d’un fichier de configuration ou d’une application fournie ne valide aucune compétence personnelle.
