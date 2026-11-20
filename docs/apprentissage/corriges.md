# Repères de correction — à lire après ta tentative

Mise à jour : 18 novembre 2026, pour la version 2 d'OpsDesk. Les énoncés sont dans [le parcours](README.md) ; la même page existe dans le centre de formation Notion.

## Comment utiliser ces repères

- **Après ta tentative, jamais avant.** Compare ta réponse, puis corrige-la toi-même et refais le contrôle.
- **Ce ne sont pas des solutions à recopier.** Aucun fichier Terraform, Ansible, Compose de production, Kubernetes ou CI complet n'est fourni : ton infrastructure reste ton travail.
- **Une autre réponse peut être juste** si elle respecte le registre des décisions, protège les données et passe les vérifications de la fiche.
- **Pour chaque exercice** : les réponses attendues aux questions de la partie 8 de la fiche, ce que contient une bonne solution, et les points à refuser dans un rendu.

<a id="exercice-01"></a>

## Exercice 01 — Comprendre OpsDesk

**Réponses attendues.**

- *Le trajet d'une création.* Le navigateur envoie `POST /api/tickets` à nginx (port 8080) ; nginx relaie à l'API ; l'API lit le jeton (qui ?), le rôle (a-t-il le droit ?), valide le titre et la description, écrit le ticket et son premier événement d'historique dans PostgreSQL, puis répond `201` avec le ticket en JSON.
- *`401` ou `403`.* `401` : l'API ne sait pas qui demande (pas de jeton, jeton expiré ou invalide). `403` : elle le sait, mais ce compte n'a pas le droit.
- *Pourquoi le ticket survit.* Il est écrit dans PostgreSQL, dont les fichiers sont sur un volume, séparé du conteneur. Il disparaît si le volume est supprimé ou le disque perdu sans sauvegarde.
- *`/health/live` ou `/health/ready`.* Le premier dit que le processus répond, sans interroger la base ; le second dit qu'il joint la base (`503` sinon).
- *Si la base est arrêtée.* `/health/ready` (503, `"database":"down"`), l'état du conteneur de la base, puis les journaux de l'API et de la base.
- *Ce qu'un `200` ne garantit pas.* Ni la persistance, ni une sauvegarde restaurable, ni la sécurité face à Internet, ni la tenue sous charge.

**Une bonne solution contient** un schéma où dans le parcours utilisateur, le navigateur passe par `frontend` ; la prise en charge par `POST /api/tickets/{id}/status` vers `in_progress` ; le `403` de Marie si elle tente la prise en charge ; comme données durables, les comptes, les tickets, les commentaires et l'historique (pas les jetons, qui ne sont pas stockés).

**Points à refuser.** Une flèche du navigateur vers la base ; « nginx vérifie le mot de passe » ; « le jeton est stocké en base » ; une limite qui n'en est pas une (« l'application est lente ») sans mesure.

<a id="exercice-02"></a>

## Exercice 02 — Architecture et décisions

**Réponses attendues.**

- *Trois serveurs.* Séparer piloter (`srv-admin`), servir (`srv-app`) et expérimenter et superviser (`srv-k3s`) : les outils d'infrastructure ont un lieu nommé et reconstructible, et les essais K3s ne menacent pas le service. Coût : 12 Go de mémoire pris à l'hôte, trois machines à maintenir.
- *Docker Compose sur le serveur.* Un seul fichier versionné décrit toute la pile ; c'est l'outil le plus répandu pour un service sur une machine. Il ne répartit rien entre plusieurs machines : c'est ce qu'apporte Kubernetes, pratiqué à part sur `srv-k3s`. Podman et Quadlet ont été écartés le 18 novembre 2026, au profit d'outils plus généralistes.
- *Le groupe `docker`.* Il vaut root : qui parle au démon peut monter `/` dans un conteneur. On administre donc par `sudo`, tracé dans le journal.
- *Si `srv-app` disparaît.* Le service s'arrête ; les données écrites depuis la dernière sauvegarde exploitable risquent d'être perdues (objectif de 24 heures seulement si une copie récente a effectivement réussi) ; le reste se reconstruit par Terraform et Ansible. *Si le PC hôte disparaît*, tout est perdu, sauvegardes comprises : aucune copie hors du PC n'est prévue.
- *Pourquoi K3s.* Pour apprendre Kubernetes sans risque pour le service réel ; un seul nœud n'apporte aucune haute disponibilité.

**Une bonne revue contradictoire relève au moins** : le stockage de la base « à revoir » (droits et contexte SELinux, y compris l’UID du conteneur) ; l'absence de copie hors du PC ; la copie du state Terraform et des clés hors de `srv-admin`, qui contient des secrets à chiffrer ; le port 8000 ouvert à `srv-k3s` pour toute l'API ; la supervision qui tombe avec `srv-k3s`.

**Points à refuser.** Une alternative inventée, sans lien avec le registre ; « vérifié » pour une décision non construite ; un défaut corrigé sans être écrit comme question ouverte ; la confusion entre volume et sauvegarde.

<a id="exercice-03"></a>

## Exercice 03 — Rocky Linux, VM, réseau et SSH

**Réponses attendues.**

- *VM ou conteneur.* Une VM a son propre noyau et simule une machine entière ; un conteneur partage le noyau de l'hôte et isole un processus.
- *Pourquoi un `ping` ne suffit pas.* ICMP et TCP 22 sont deux flux différents, filtrés séparément.
- *Les quatre messages.* `timed out` : aucune réponse (VM éteinte, mauvaise adresse). `No route to host` : souvent un rejet du pare-feu. `refused` : la machine répond, rien n'écoute sur le port. `Permission denied` : le serveur répond, l'authentification échoue.
- *L'empreinte.* Elle prouve qu'on parle au bon serveur ; une empreinte changée signale une VM recréée ou une interception.
- *Pourquoi garder SELinux et le pare-feu.* Les désactiver masque la cause et laisse le serveur exposé ; on corrige la règle précise.

**Une bonne solution contient** le tableau des six questions avec de vraies sorties datées ; la configuration SSH dans un fichier de `/etc/ssh/sshd_config.d/`, validée par `sshd -t` ; les deux refus prouvés ; un diagnostic où la panne provoquée est retrouvée par la méthode, pas devinée.

**Points à refuser.** SELinux en `Permissive` « temporairement » ; `PermitRootLogin yes` ; une connexion qui ne marche que par mot de passe ; une ancienne empreinte effacée sans vérification.

<a id="exercice-04"></a>

## Exercice 04 — Terraform

**Réponses attendues.**

- *Les trois choses comparées.* Le code, le state, et ce qui existe réellement dans libvirt.
- *`+`, `~`, `-/+`.* Créer ; modifier sur place ; détruire puis recréer (une VM perd alors son disque).
- *Le state.* Hors de Git car il contient identifiants et parfois secrets ; copie protégée hors de `srv-admin`. En cas de perte, ne pas appliquer un plan de recréation avant d'avoir examiné et retrouvé l'état approprié.
- *Une modification à la main.* Le plan suivant montre une dérive et propose de revenir à ce que dit le code.
- *Terraform et Ansible.* Terraform crée les machines (disques, réseau, ressources) ; Ansible configure l'intérieur.

**Une bonne solution contient** une version du fournisseur fixée ; une seule description réutilisée pour les deux VM ; le disque de données de 10 Go sur `srv-app` seulement ; aucune ressource pour `srv-admin` ; un second plan à « No changes » ; la décision image cloud ou ISO écrite au registre.

**Points à refuser.** Un `.tfstate` dans le dépôt ; un `apply` dont le plan annonçait un remplacement non expliqué ; `srv-admin` importée dans le state ; un mot de passe en clair dans le code.

<a id="exercice-05"></a>

## Exercice 05 — Ansible

**Réponses attendues.**

- *Playbook ou liste de commandes.* Le playbook décrit l'état voulu, se relit, se versionne, et se rejoue sans dégâts.
- *`ok`, `changed`, `failed`.* Déjà conforme ; corrigé ; échec.
- *Pourquoi `changed=0` ne suffit pas.* Il dit qu'il n'y a plus rien à corriger, pas que le service fonctionne : on vérifie sur le serveur.
- *Sur une VM neuve.* Toutes les tâches répondent `changed` au premier passage, puis `ok` au second.

**Une bonne solution contient** une tâche par point de l'état voulu, avec les modules dédiés (`dnf` avec `state: absent` puis `present`, `yum_repository` ou le fichier `.repo` officiel avec sa clé, `systemd_service` avec `enabled` et `state`, `file`, `ansible.posix.firewalld` avec `permanent` et `immediate`) ; aucun `shell` pour installer ; aucun `user` ajouté au groupe `docker` ; un second passage à `changed=0`.

**Points à refuser.** `shell` partout ; `changed` à chaque passage laissé tel quel ; un mot de passe dans l'inventaire ; `firewalld` arrêté pour ouvrir le port ; le script `get.docker.com` lancé par `curl | sh` ; `mathias` ajouté au groupe `docker` « pour éviter `sudo` ».

<a id="exercice-06"></a>

## Exercice 06 — Docker Engine et Compose

**Réponses attendues.**

- *Image, conteneur, volume.* Le programme figé ; son exécution, jetable ; le stockage qui survit au conteneur.
- *Qui fait quoi.* Le fichier décrit ; `docker compose` le transmet au démon ; le démon crée réseaux, volumes et conteneurs ; systemd ne démarre que le démon.
- *Au reboot.* systemd lance `docker` parce qu'il est activé ; Docker relance les conteneurs `unless-stopped`, sauf ceux arrêtés à la main.
- *Un mot de passe sans fichier.* Un fichier sur le serveur, monté par le bloc `secrets:` de Compose dans `/run/secrets/`, lu par la variable `*_FILE` ; il doit rester lisible par l'utilisateur du conteneur.
- *Port publié et firewalld.* Docker écrit ses propres règles : la zone du serveur ne dit pas à elle seule qui joint un port publié. La preuve se fait depuis une autre machine.
- *`healthy` ne suffit pas.* La sonde de l'API vise `/health/live` : l'API reste saine sans base. La preuve est un ticket créé puis relu.
- *Volume et sauvegarde.* Le volume survit au conteneur, pas à sa suppression ni à la perte du disque.

**Une bonne solution contient** des images référencées par digest ; deux réseaux, la base absente de celui de nginx ; l'API joignable sous le nom `backend` ; une sonde et `restart: unless-stopped` par service ; la rotation des journaux ; trois secrets en fichiers ; le port 8080 publié sur l'adresse de `srv-app` et le port 8000 accessible à `srv-k3s` seule, prouvé depuis les autres machines ; `selinux-enabled` dans `daemon.json` et `container_t` constaté ; la décision sur le stockage écrite et justifiée ; un rôle Ansible avec `community.docker.docker_compose_v2`, idempotent, qui ne recrée rien au second passage.

**Complément DNS/TLS.** Le nom doit être résolu par le DNS du laboratoire ; le certificat présenté doit être approuvé, correspondre au nom et permettre une requête vérifiée sans `-k` ; un certificat non approuvé doit être refusé.

**Points à refuser.** Un secret écrit dans le fichier Compose ou un template ; des images en `:latest` ; la base publiée sur un port de l'hôte ; le socket Docker monté dans un conteneur ; SELinux désactivé ou `--privileged` pour « faire marcher » un montage ; un service qui ne revient pas après un reboot ; `docker compose down -v` sur le service réel.

<a id="exercice-07"></a>

## Exercice 07 — K3s

**Réponses attendues.**

- *Lancer ou déclarer.* On décrit l'état voulu ; le cluster agit en permanence pour le rejoindre.
- *Deployment, Service, Ingress.* Garde N pods ; nom stable vers les pods prêts, choisis par leurs étiquettes ; entrée HTTP depuis l'extérieur.
- *Readiness ou liveness.* La première retire du trafic, la seconde redémarre. `/health/ready` en liveness ferait redémarrer l'API en boucle à chaque panne de la base.
- *Deux API, une seule base.* L'API ne garde rien en mémoire et partage le même `JWT_SECRET` ; deux PostgreSQL sur le même stockage le corrompraient.
- *Un seul nœud.* Si `srv-k3s` tombe, tout tombe.

**Réponses attendues aux quatre expériences.** Pod de l'API supprimé : recréé en quelques secondes, erreurs `502` ou `503` pendant ce temps. Base arrêtée : l'API sort des endpoints mais ne redémarre pas (si les sondes sont justes). Pod de la base supprimé : le ticket est relu, grâce au PVC. Deux pods d'API : la session reste valide d'un pod à l'autre, grâce au jeton signé par un secret commun.

**Points à refuser.** Les valeurs du Secret dans le dépôt ; une sonde unique pour les deux rôles ; « K3s rend OpsDesk hautement disponible ».

<a id="exercice-08"></a>

## Exercice 08 — CI/CD

**Réponses attendues.**

- *Ce que prouve une CI verte.* Les tests écrits passent, les images se construisent, la politique de scan est satisfaite pour les vulnérabilités détectées à cette date (exceptions tracées), une image identifiée est publiée. Elle ne prouve pas que cette image tourne quelque part.
- *Pourquoi la CI ne déploie pas.* Ses machines ne joignent pas le réseau privé, et le déploiement reste une décision humaine, depuis `srv-admin`.
- *Tag ou digest.* Le tag peut bouger ; on déploie par digest. Même un tag de commit reste modifiable sauf politique d’immuabilité imposée et vérifiée.
- *PostgreSQL en CI.* Certains défauts (verrous, types) n'apparaissent pas sur SQLite.
- *Trivy trouve une vulnérabilité grave.* On corrige (image de base plus récente) ; sinon on accepte par écrit, avec une raison et une date de réexamen.

**Une bonne solution contient** des tests sur pull request sans publication ; `needs:` entre tests et images ; `permissions` minimales, `packages: write` seulement pour publier ; deux tags (version et commit) ; une règle Trivy écrite ; le rôle Ansible paramétré par la version ; les digests comparés ; l’enchaînement contrôlé et ses tests d’échec.

**Points à refuser.** Un jeton personnel au lieu du `GITHUB_TOKEN` ; un seuil Trivy abaissé sans trace ; un déploiement sur `latest` ; une capture d'un ancien run présentée comme preuve.

<a id="exercice-09"></a>

## Exercice 09 — Supervision

**Réponses attendues.**

- *Compteur, jauge, histogramme.* `opsdesk_http_requests_total` ne fait qu'augmenter ; `opsdesk_database_up` vaut 1 ou 0 ; `opsdesk_http_request_duration_seconds` range les durées par tranches.
- *Pourquoi `rate`.* Un compteur brut ne dit que le total depuis le démarrage, et repart à zéro au redémarrage ; `rate` donne une vitesse et gère ces remises à zéro.
- *Le `for`.* La condition doit tenir pendant toute la durée : un à-coup ne déclenche rien.
- *L'API arrêtée.* La mesure `up` de sa cible passe à 0 ; l'alerte « base » ne se déclenche pas, car `/metrics` ne répond plus du tout. Il manque donc une alerte sur `up`, à proposer.
- *`srv-k3s` tombe.* La supervision tombe avec : personne n'est prévenu.

**Une bonne solution contient** quatre cibles `UP` ; une alerte « base » fondée sur `opsdesk_database_up` égale à 0 avec un `for` d'une minute ; une alerte 5xx fondée sur la vitesse des requêtes dont le statut commence par 5 ; une latence au 95ᵉ centile par `histogram_quantile` ; les heures de `pending`, `firing` et retour, pour chaque alerte ; le service réel épargné pendant les tests.

**Points à refuser.** Un compteur affiché sans `rate` ; une alerte jamais vue à `firing` ; une étiquette par ticket ou par utilisateur (trop de séries) ; k6 lancé sur le service réel.

<a id="exercice-10"></a>

## Exercice 10 — Maintenance

**Réponses attendues.**

- *Avant.* État de départ, sauvegarde, étapes, retour arrière, critère d'abandon. On décide du critère avant, parce qu'en pleine intervention on veut toujours « encore un essai ».
- *Retour arrière ou restauration.* Le premier redéploie l'image précédente sans toucher aux données ; la seconde remet les données d'une sauvegarde.
- *Pourquoi des `502` ou `504`.* Pendant une indisponibilité de l’API, nginx ne la joint plus ou atteint un délai. Mesure historique : environ 2 secondes lors d’une recréation ; ne pas la généraliser.
- *Ce qui casse le retour arrière.* Une nouvelle version qui modifie le schéma de la base : l'ancienne image ne sait plus le lire.
- *La sonde ailleurs.* Une sonde sur le serveur qu'on redémarre s'arrête avec lui.

**Une bonne solution contient** deux fiches d'intervention écrites avant ; une sonde horodatée depuis `srv-admin` ; une indisponibilité chiffrée ; la version et le digest identiques à ceux de départ après le retour arrière ; le ticket témoin relu ; un compte rendu court.

**Points à refuser.** Une fiche écrite après coup ; « le service a l'air de remarcher » ; un retour arrière jamais exercé.

<a id="exercice-11"></a>

## Exercice 11 — Sauvegarde et restauration

**Réponses attendues.**

- *Volume et sauvegarde.* Le volume ne protège ni d'une suppression, ni d'une erreur, ni de la perte du disque ou de la VM.
- *`pg_dump` plutôt qu'une copie de fichiers.* Il lit la base dans une transaction : copie cohérente, sans arrêt. Une copie à chaud des fichiers peut être incohérente.
- *RPO et RTO.* Objectifs de perte maximale et de délai maximal de reprise. On mesure la fenêtre de perte et le délai de rétablissement, puis on les compare aux objectifs ; une sauvegarde quotidienne réussie vise une perte de 24 h au maximum.
- *Ce que le dispositif ne couvre pas.* La perte du PC hôte (aucune copie ailleurs), une corruption non détectée avant la rotation des 7 copies, une suppression de données remarquée plus de 7 jours après.
- *Pourquoi une cible séparée.* Pour ne jamais risquer la base en service, et pour prouver qu'on sait repartir de zéro.

**Une bonne solution contient** un service et un minuteur systemd du système, avec `Persistent=true`, qui lance `pg_dump` dans le conteneur de la base (`docker compose exec -T`) ; un script qui s'arrête à la première erreur ; une rotation à 7 copies ; une clé SSH limitée au seul dépôt des copies ; des empreintes comparées ; un procès-verbal de restauration chronométré avec le ticket témoin relu dans l'interface.

**Points à refuser.** Des sauvegardes laissées seulement sur `srv-app` ; un test de restauration sur la base en service ; une sauvegarde « réussie » de 0 octet ; une clé SSH qui ouvre tout l'hôte.

<a id="exercice-12"></a>

## Exercice 12 — Diagnostic

**Réponses attendues.**

- *Pourquoi les faits avant les hypothèses.* Sinon on cherche à confirmer sa première idée et on oublie les autres.
- *Ce que désignent les sondes.* `/healthz` en échec : nginx ou l'accès réseau. `/health/live` en échec : l'API. `/health/ready` en `503` : la base ou le chemin vers elle.
- *Mitigation ou cause racine.* La première rétablit vite (un retour arrière) ; la seconde, corrigée, empêche le retour de la panne.
- *Sans reproche.* Une panne est presque toujours une suite de failles du système et des procédures ; chercher un coupable fait cacher les erreurs.

**Les six cartes d'incident, pour comparer après coup.**

| Carte | Signature | Ce qui la confirme | Correction |
| --- | --- | --- | --- |
| Mot de passe de la base | `503` sur `/health/ready`, base en marche | Journaux de l'API : échec d'authentification PostgreSQL | Remettre le bon secret, redémarrer l'API |
| Nom de l'API | Interface affichée, `502` sur `/api` | `/health/live` de l'API répond en direct, pas via nginx | Rétablir le nom `backend` |
| Secret des jetons | Tous les utilisateurs renvoyés vers la connexion (`401`) | Les nouvelles connexions fonctionnent | Rien à corriger si le changement était voulu ; sinon remettre l'ancien secret |
| Pare-feu | Délai ou rejet depuis l'hôte, service sain sur le serveur | `curl` local réussi, distant en échec ; examiner les règles Docker et le pare-feu | Rétablir uniquement l’accès autorisé, puis vérifier le refus des autres sources |
| Redémarrage | Plus rien après un reboot | `systemctl is-enabled docker` à `disabled` | Réactiver le service `docker`, par le playbook |
| Version | L'API ne démarre pas | `docker compose ps -a` et `docker compose logs backend` : image introuvable (`manifest unknown`) | Remettre un digest existant, de préférence par le rôle |

**Points à refuser.** Un redémarrage général avant tout relevé ; « cause racine » écrite pour la première hypothèse plausible ; un post-mortem qui désigne une personne.

<a id="exercice-13"></a>

## Exercice 13 — Autonomie

Pas de corrigé : chaque tâche a plusieurs bonnes réponses. Ce qui s'évalue, c'est la démarche.

**Une fiche de cas solide** a ses dix rubriques remplies pendant le travail ; des faits relevés avant l'action ; une option écartée avec sa raison ; une preuve avant et après ; une limite réelle ; l'aide déclarée avec son niveau ; une auto-évaluation prudente.

**Conclusion à écrire après la vérification séparée** : autonome sur la tâche évaluée (L3) ; réussite avec aide (L2, aide déclarée) ; ou compétence à retravailler, avec ce qui a manqué. Aucune note chiffrée.

**Points à refuser.** Une tâche déjà faite présentée comme nouvelle ; une aide cachée ; L3 sans vérification séparée.
