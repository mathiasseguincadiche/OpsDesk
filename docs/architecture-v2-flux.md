# OpsDesk — Architecture V2 : matrice des flux

**Statut : validée en conception ; règles réseau non appliquées aux VM.** Les ports de cette matrice sont des **flux cibles** et ne décrivent pas les ports effectivement ouverts aujourd'hui.

## Réseau et identités

| Cible | IP réservée | Fonction |
| --- | --- | --- |
| Fedora 45 (hôte) | `192.168.150.1` | Terraform local, KVM/libvirt, réception contrôlée et Borg sur disque externe |
| `srv-admin` (Rocky) | `192.168.150.5` | Ansible, Git, k6, bastion SSH |
| `srv-app` (Rocky) | `192.168.150.10` | Compose de production : React/Nginx, FastAPI, PostgreSQL |
| `srv-k3s` (Rocky) | `192.168.150.20` | K3s mono-nœud, Prometheus, Grafana et copie d'essai |

Réseau NAT privé libvirt **opsdesk-lan : `192.168.150.0/24`**. Réservations IP et DNS internes à vérifier ; pas de redirection entrante depuis Internet. Les noms de service en `opsdesk.lan`, les SAN TLS et le plan DNS seront testés ensemble.

## Flux autorisés par l'architecture

| Source | Destination | Port / protocole cible | Objet / contrôle obligatoire |
| --- | --- | --- | --- |
| Fedora (Terraform) | libvirt local | `qemu:///system` | Provisionnement via hôte, pas de `qemu+ssh` depuis `srv-admin` |
| Fedora | `srv-admin` | TCP 22 SSH | Clé de pilotage dédiée, root et mot de passe refusés |
| `srv-admin` | `srv-app`, `srv-k3s` | TCP 22 SSH | Ansible, identité dédiée, `sudo` borné |
| Navigateur de l'hôte Fedora | `srv-app` | TCP 443 HTTPS | Connexion, tickets, cookies Secure, CA locale reconnue |
| `srv-admin` | `srv-app` | TCP 443 HTTPS | Contrôle du service principal ; aucun besoin d'atteindre :8000 |
| `srv-admin` (k6) | Traefik sur `srv-k3s` | TCP 443 HTTPS | **Essai uniquement** : aucune charge k6 sur `srv-app` |
| Fedora (navigateur) | Grafana via `srv-admin` → `srv-k3s` | Tunnel SSH (TCP 22) | Port Grafana :3000 non publié au LAN ; accès local par tunnel |
| Prometheus (`srv-k3s`) | Passerelle métriques `srv-app` | TCP 9180 HTTP interne filtré **proposé** | Uniquement `/metrics` ; pas de publication globale FastAPI :8000 |
| Prometheus (`srv-k3s`) | node_exporter sur `srv-app` | TCP 9100 HTTP interne filtré | Autoriser seulement la source `.20` ; tester les refus |
| Frontend Nginx (réseau Compose) | API (réseau Compose) | TCP 8000 HTTP interne | Routes `/api` et sondes ; pas de port hôte |
| API (réseau Compose) | PostgreSQL (réseau Compose) | TCP 5432 PostgreSQL interne | Jamais publié sur l'IP de la VM |
| Compte de transfert `srv-app` | Réception dédiée Fedora | TCP 22 SSH restreint | Dépôt uniquement, sans shell ni suppression ni accès au compte personnel |
| `srv-app` / `srv-k3s` | `ghcr.io` | TCP 443 HTTPS **sortant** | Tirer les **trois images par digest** avec droit de lecture seul |
| `srv-admin` | GitHub et dépôts nécessaires | TCP 443 HTTPS sortant | Récupérer le dépôt, paquets et artefacts ; pas de connexion entrante GitHub Actions |
| Grafana Alerting (`srv-k3s`) | Relais SMTP | SMTP sur port/TLS du fournisseur choisi | Deux alertes et accusé réel de réception e-mail ; aucune donnée de connexion dans Git |

**K3s mono-nœud :** ne pas recopier aveuglément les ports destinés à un cluster multi-nœuds. Les éventuels flux kubelet, CNI, CIDR des pods et services seront établis à partir de la version et de la configuration effectivement déployées, puis testés sous SELinux Enforcing et firewalld.

## Flux interdits et tests négatifs

| Source non autorisée | Cible | Résultat à prouver |
| --- | --- | --- |
| Fedora ou `srv-admin` | `srv-app:8000` et `srv-app:5432` | Ports non joignables, y compris après publication Docker/Compose |
| Fedora ou `srv-admin` | `srv-app:9100` et `srv-app:9180` | Refus, tandis que Prometheus `.20` peut collecter les métriques prévues |
| Internet | Les trois VM | Pas de NAT entrant ou de redirection exposant les VM |
| Copie d'essai K3s | PostgreSQL principal | Aucune route ni aucun secret permettant d'atteindre la base réelle |
| Compte de sauvegarde | Shell Fedora, répertoires personnels, anciennes archives | Refus d'ouverture de shell, de lecture, de suppression et d'évasion du dépôt |
| Client LAN quelconque | Grafana :3000 ou FastAPI :8000 | Aucun accès direct |

## Principes de qualification

Un port **fermé dans une configuration** n'est pas nécessairement **inaccessible sur le réseau** : Docker peut modifier le chemin de filtrage. Vérifier depuis plusieurs origines avec `curl`, `nmap`, inspection des règles nftables et diagnostics SELinux. Distinguer l'application locale `127.0.0.1:8080` du futur serveur HTTPS :443. Conserver les essais réussis et refus attendus dans `evidence/infrastructure/` uniquement après exécution réelle.

[Sept ADR](adr/README.md) · [ADR-04 Réseau/TLS](adr/ADR-04-reseau-tls.md) · [Plan de déploiement V2](architecture-v2-deploiement.md) · [STATUS](../STATUS.md)
