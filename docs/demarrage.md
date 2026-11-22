# Démarrer OpsDesk en local

Ce guide lance OpsDesk sur un poste, en conteneurs, pour l'essayer ou le développer. Mise à jour : 18 novembre 2026, pour la version 2.0.0. Le déploiement sur serveur (Docker Engine et Compose sur Rocky Linux) est un jalon futur décrit dans la [feuille de route](../ROADMAP.md).

## Ce qu'il faut

| Outil | Vérification | Remarque |
| --- | --- | --- |
| Git | `git --version` | Pour récupérer le dépôt |
| Docker Engine avec le plugin Compose | `docker compose version` | Les essais consignés ont été faits avec Docker 29.8 et Compose 5.5.1 sous Ubuntu WSL2. L'ancienne commande `docker-compose` (Compose v1, en Python) n'est plus maintenue |
| Python 3 | `python3 --version` | Seulement pour le test de bout en bout |
| `curl` | `curl --version` | Pour contrôler la disponibilité depuis le poste |
| Les ports locaux 8080 et 8000 libres (Linux) | `ss -lnt \| grep -E ':(8080\|8000)[[:space:]]'` | Aucune ligne attendue ; adapter le contrôle au système hôte |

## Comprendre les trois niveaux de contrôle

Le démarrage Compose ci-dessous concerne la **démonstration locale**, pas la réception du laboratoire Rocky. Vérifier successivement : **(1)** que les conteneurs démarrent, **(2)** que `/health/ready` voit PostgreSQL, **(3)** que le parcours de ticket fonctionne avec le smoke. Le dernier test crée un ticket fictif persistant : ne pas l'exécuter sur une base réelle ou partagée. Si un niveau échoue, consulter [le diagnostic](#en-cas-de-problème) avant de redémarrer ou supprimer quoi que ce soit.

## 1. Récupérer le dépôt

```bash
git clone https://github.com/mathiasseguincadiche/OpsDesk.git && cd OpsDesk
```

## 2. Démarrer

```bash
docker compose up -d --build
```

Sur un dépôt fraîchement cloné, aucun fichier `.env` n'est nécessaire. La première construction peut prendre quelques minutes. La base démarre d'abord ; l'API attend qu'elle soit saine, puis l'interface attend l'API.

## 3. Vérifier

```bash
docker compose ps
```

Les trois services (`db`, `backend`, `frontend`) doivent afficher `healthy` une fois le démarrage terminé. La sonde Docker de l'API vérifie la vie du processus, pas sa disponibilité métier ; la requête suivante complète ce contrôle.

```bash
curl -i http://127.0.0.1:8080/health/ready
```

Attendu : `200` et `"database":"up"`. Puis le test de bout en bout, qui rejoue un parcours complet à travers nginx :

```bash
python3 scripts/smoke.py http://127.0.0.1:8080
```

Attendu : une ligne `OK` par contrôle, puis `ALL GOOD`. Le test crée un ticket fictif et ne l'efface pas.

Ouvrir enfin **http://localhost:8080** et cliquer sur un compte de démonstration pour se connecter.

## Ce qui tourne

| Service | Rôle | Accès depuis le poste |
| --- | --- | --- |
| `frontend` | nginx et l'interface React | `http://localhost:8080` |
| `backend` | API FastAPI | `http://127.0.0.1:8000`, limité au poste (documentation : `/api/docs`) |
| `db` | PostgreSQL 17 | Non publié |

Les ports 8080 et 8000 de cette pile sont liés à `127.0.0.1`. Depuis une autre machine, la connexion doit échouer ; vérifier également les adresses de publication avec `docker compose ps`. Ne pas élargir cette exposition pour des comptes et données de démonstration. Le déploiement réseau sur `srv-app` relève d'une configuration d'infrastructure distincte.

Les données sont dans un volume nommé : elles survivent à l'arrêt et à la recréation des conteneurs.

## Arrêter

```bash
docker compose down
```

Les conteneurs sont supprimés, le volume de la base est conservé. **`docker compose down -v` supprime aussi le volume, donc tous les tickets** : à réserver à une remise à zéro voulue.

## Configuration facultative

Pour modifier un port ou une option, créer `.env` à partir de `.env.example` uniquement si aucun `.env` n'existe déjà. Les valeurs existantes sont conservées ; ne pas recréer le volume pour changer un mot de passe. Le Compose de référence utilise des valeurs publiques de démonstration et le mode `development`. Sur un serveur, utiliser une configuration de déploiement dédiée avec `ENVIRONMENT=production` et des secrets distincts (voir [référence technique](reference-technique.md#déployer-avec-docker-compose-sur-un-serveur)).

## En cas de problème

| Ce que tu vois | Cause probable | Que faire |
| --- | --- | --- |
| `address already in use` sur 8080 ou 8000 | Un autre service occupe le port | Identifier ce service avant de l'arrêter ; ou adapter `HTTP_PORT` / `API_PORT` dans `.env`, puis les URL de contrôle |
| `backend` jamais `healthy` | L'API n'arrive pas à démarrer (souvent la base ou un secret) | `docker compose logs backend` |
| L'API refuse les secrets | Un `.env` ou des variables existantes activent le mode `production` sans secrets valides | Pour la démonstration locale, utiliser `development` ; pour un serveur, corriger les secrets. Ne pas modifier ni supprimer les données existantes. |
| `502` ou `504` sur l’interface | nginx ne joint pas l’API ou n’obtient pas de réponse à temps | `docker compose ps`, puis les journaux de `backend` et `frontend` |
| Connexion refusée avec le mot de passe administrateur modifié | Le premier administrateur n'est créé qu'une fois, sur une base vide | Le mot de passe de `.env` ne s'applique qu'au premier démarrage |
| Pas de données de démonstration | Elles ne sont créées que si la base est vide, et si `SEED_DEMO_DATA=true` | Normal sur une base déjà utilisée |

## Développer sans conteneur

Pour modifier le code avec rechargement automatique (API sur SQLite, interface avec Vite) : voir la section [Développer sans conteneur](reference-technique.md#développer-sans-conteneur) de la référence technique.

## Et ensuite

- Comprendre les trois services : [contrat applicatif](contrat-applicatif.md) et [architecture](architecture.md).
- Exploiter le service : [exploitation courante](exploitation-day2.md).
- Préparer le déploiement serveur : [feuille de route](../ROADMAP.md) et [référence technique](reference-technique.md).
