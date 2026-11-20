# Démarrer OpsDesk en local

Ce guide lance OpsDesk sur un poste, en conteneurs, pour l'essayer ou le développer. Mise à jour : 18 novembre 2026, pour la version 2.0.0. Le déploiement sur serveur (Docker Engine et Compose sur Rocky Linux) est l'objet de l'[exercice 06](apprentissage/06-conteneurs.md).

## Ce qu'il faut

| Outil | Vérification | Remarque |
| --- | --- | --- |
| Git | `git --version` | Pour récupérer le dépôt |
| Docker Engine avec le plugin Compose | `docker compose version` | Les essais consignés ont été faits avec Docker 29.8 et Compose 5.5.1 sous Ubuntu WSL2. L'ancienne commande `docker-compose` (Compose v1, en Python) n'est plus maintenue |
| Python 3 | `python3 --version` | Seulement pour le test de bout en bout |
| `curl` | `curl --version` | Pour contrôler la disponibilité depuis le poste |
| Les ports locaux 8080 et 8000 libres (Linux) | `ss -lnt \| grep -E ':(8080\|8000)[[:space:]]'` | Aucune ligne attendue ; adapter le contrôle au système hôte |

## 1. Récupérer le dépôt et préparer la configuration

```bash
git clone https://github.com/mathiasseguincadiche/OpsDesk.git && cd OpsDesk
```

```bash
if [ -e .env ] || [ -L .env ]; then
  printf 'Configuration existante conservée. Vérifiez-la avant de continuer.\n'
else
  (umask 077; set -C; cat .env.example > .env)
fi
```

Ouvrir `.env` et remplacer les trois valeurs `change-me` : mot de passe de la base, `JWT_SECRET` (32 caractères au moins, par exemple généré par `openssl rand -base64 48`), mot de passe du premier administrateur. Le fichier `.env` n'est jamais versionné.

## 2. Démarrer

```bash
docker compose up -d --build
```

La première fois, la construction des images prend quelques minutes. La base démarre d'abord ; l'API attend qu'elle soit saine, puis l'interface attend l'API.

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

Les ports 8080 et 8000 de cette pile sont liés à `127.0.0.1`. Depuis une autre machine, la connexion doit échouer ; vérifier également les adresses de publication avec `docker compose ps`. Ne pas élargir cette exposition pour des comptes et données de démonstration. Le déploiement réseau sur `srv-app` relève de l’exercice 06.

Les données sont dans un volume nommé : elles survivent à l'arrêt et à la recréation des conteneurs.

## Arrêter

```bash
docker compose down
```

Les conteneurs sont supprimés, le volume de la base est conservé. **`docker compose down -v` supprime aussi le volume, donc tous les tickets** : à réserver à une remise à zéro voulue.

## En cas de problème

| Ce que tu vois | Cause probable | Que faire |
| --- | --- | --- |
| `address already in use` sur 8080 ou 8000 | Un autre service occupe le port | Identifier ce service avant de l'arrêter ; ou adapter `HTTP_PORT` / `API_PORT` dans `.env`, puis les URL de contrôle |
| `backend` jamais `healthy` | L'API n'arrive pas à démarrer (souvent la base ou un secret) | `docker compose logs backend` |
| L'API démarre puis s'arrête, message sur `JWT_SECRET` | `ENVIRONMENT=production` exige un `JWT_SECRET` d'au moins 32 caractères | Corriger `.env`, puis `docker compose up -d` |
| `502` ou `504` sur l’interface | nginx ne joint pas l’API ou n’obtient pas de réponse à temps | `docker compose ps`, puis les journaux de `backend` et `frontend` |
| Connexion refusée avec le mot de passe administrateur modifié | Le premier administrateur n'est créé qu'une fois, sur une base vide | Le mot de passe de `.env` ne s'applique qu'au premier démarrage |
| Pas de données de démonstration | Elles ne sont créées que si la base est vide, et si `SEED_DEMO_DATA=true` | Normal sur une base déjà utilisée |

## Développer sans conteneur

Pour modifier le code avec rechargement automatique (API sur SQLite, interface avec Vite) : voir la section [Développer sans conteneur](reference-technique.md#développer-sans-conteneur) de la référence technique.

## Et ensuite

- Comprendre ce qui tourne : [exercice 01](apprentissage/01-application.md) et [contrat applicatif](contrat-applicatif.md).
- Exploiter le service : [exploitation courante](exploitation-day2.md).
- Construire l'infrastructure : [le parcours](apprentissage/README.md).
