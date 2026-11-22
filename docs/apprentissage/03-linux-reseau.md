# 03 — Rocky Linux, machines virtuelles, réseau et SSH

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 03, accessible sur invitation. Schéma : [les six questions d'un accès SSH](../diagrams/pedagogique-acces-ssh.svg).

**Objectif.** Créer la première machine virtuelle, `srv-admin`, et savoir trouver pourquoi une connexion SSH échoue, couche par couche, sans désactiver aucune protection.

**Durée estimée** : 3 à 4 heures. **Prérequis** : PC Fedora avec la virtualisation vérifiée (section 2 du [guide du laboratoire](../laboratoire-fedora-kvm-rocky.md)), exercice 02. **État** : prévu, non vérifié.

## Pourquoi

Tout le reste du projet passe par SSH : Terraform et Ansible partent de `srv-admin`. Désactiver le pare-feu ou SELinux « pour voir » fait passer la connexion, mais laisse la cause inconnue et le serveur moins protégé.

## L'essentiel à comprendre

- Une connexion SSH qui échoue se diagnostique en **six questions, dans l'ordre** : le nom, la route, le service (port 22), le pare-feu, l'identité du serveur (empreinte), le compte.
- Le message dit déjà beaucoup : `Connection timed out` (aucune réponse), `No route to host` (souvent un rejet du pare-feu), `Connection refused` (rien n'écoute), `Permission denied` (authentification).
- Un `ping` réussi ne prouve rien sur SSH : ICMP et TCP sont filtrés séparément.
- On vérifie l'empreinte de la clé d'hôte à la première connexion, depuis la console de la VM.
- SELinux reste en mode `Enforcing`, firewalld reste actif : on cherche la règle précise.

## Cas voisin : une connexion réussit par adresse, pas par nom

**Situation illustrative, non observée sur les VM.** Une machine de test répond à `ssh utilisateur@192.0.2.10`, mais `ssh utilisateur@serveur.test` échoue. Une hypothèse est la résolution du nom ; elle doit être confrontée à l'adresse réellement obtenue avant de modifier SSH. Si le nom désigne déjà la bonne adresse, chercher ailleurs : routage, écoute, filtrage ou identité.

**Ce que montre chaque preuve.** Une résolution correcte ne garantit pas la route ; un `ping` positif ne garantit pas TCP/22 ; un port TCP joignable ne valide pas la clé d'hôte ni le compte. Relève les messages avant toute action, puis change **une seule couche**. Les adresses ci-dessus sont réservées à la documentation : elles ne désignent aucune VM du laboratoire.

## Ce qu'il faut obtenir

1. Un réseau virtuel NAT `opsdesk-lan` en 192.168.150.0/24 sur l'hôte.
2. La VM `srv-admin` : Rocky Linux 10.2 minimal, 1 vCPU, 2 Go, 20 Go, à l'adresse 192.168.150.5, créée à la main (sections 4 à 6 du guide).
3. Le compte `mathias`, avec `sudo`.
4. `ssh mathias@192.168.150.5` depuis Fedora, par clé, sans mot de passe.
5. Connexion par mot de passe et connexion directe de `root` refusées.
6. SELinux `Enforcing`, firewalld actif.

**Livrable** : le tableau des six questions rempli avec tes commandes et tes sorties datées, la preuve des deux refus, et le diagnostic d'une panne simple provoquée sur ta VM.

## Vérifications

| Ce que tu vérifies | Commande | Résultat attendu |
| --- | --- | --- |
| Bonne VM | `cat /etc/os-release` ; `hostnamectl` | Rocky Linux 10.2 ; `srv-admin` |
| Adresse et route | `ip -brief address` ; `ip route` | 192.168.150.5/24 ; route par défaut |
| SSH écoute | `ss -lnt` | `LISTEN` sur le port 22 |
| Connexion par clé | `ssh mathias@192.168.150.5 hostname` | `srv-admin`, sans mot de passe |
| Mot de passe refusé | `ssh -o PubkeyAuthentication=no mathias@192.168.150.5` | `Permission denied`, sans demande de mot de passe |
| Protections actives | `getenforce` ; `systemctl is-active firewalld` | `Enforcing` ; `active` |

## Pièges fréquents

Modifier `sshd` sans `sshd -t` ni console ouverte ; effacer une ancienne empreinte sans comprendre pourquoi elle a changé ; changer plusieurs couches à la fois ; conclure « route absente » sur la seule foi de `No route to host`.

Suite : [exercice 04](04-terraform.md).
