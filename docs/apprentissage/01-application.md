# 01 — Comprendre OpsDesk : HTTP, API et PostgreSQL

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 01, accessible sur invitation.

**Objectif.** Raconter le trajet d'une demande dans OpsDesk, du navigateur jusqu'à la base, et dire quel composant regarder quand quelque chose ne répond pas.

**Durée estimée** : 1 h 30 à 2 heures. **Prérequis** : aucun ; de quoi dessiner. Docker facultatif. **État** : prévu, non vérifié.

## Pourquoi

Faire tourner un service sans perdre ses données suppose de savoir ce qui se passe à l'intérieur. Sans cela, à la première panne, on redémarre tout au hasard.

## L'essentiel à comprendre

- La pile `compose.yaml` déclare trois services : `frontend` (nginx/React, port 8080), `backend` (FastAPI, port 8000) et `db` (PostgreSQL, port interne 5432, non publié). Les images applicatives s'appellent `opsdesk-frontend` et `opsdesk-api` ; un nom d'image n'est pas un nom de service. Les noms DNS internes utilisés par Compose sont ceux des services.
- Dans le parcours utilisateur, le navigateur parle à nginx ; nginx relaie `/api` vers l'API ; seule l'API accède à la base. Dans la pile de référence, l'accès direct à l'API sur `127.0.0.1:8000` est réservé aux essais et au diagnostic local.
- L'API vérifie **qui** demande (jeton JWT, valable 12 heures par défaut) et **s'il en a le droit** (rôle `user`, `agent` ou `admin`), puis applique les règles du ticket.
- Un ticket passe par Ouvert → En cours → Résolu → Clôturé ; les sauts interdits sont refusés (`409`), et seul le support prend un ticket en charge.
- `/health/live` dit que le processus répond ; `/health/ready` dit qu'il joint la base (`503` sinon).
- Un ticket survit à un redémarrage parce qu'il est écrit dans PostgreSQL, sur un volume.

Le schéma de référence est [l'architecture](../diagrams/architecture.svg) ; les détails sont dans la [référence technique](../reference-technique.md).

Pour approfondir sans résoudre ton exercice de création et prise en charge : [diagramme de séquence d'une simple consultation](../diagrams/sequence-consultation.svg), à ouvrir en grand.

## Comprendre le mécanisme et ses limites

**Exemple de raisonnement (sans solution de l'exercice).** Si la page d'accueil s'affiche mais qu'une demande ne peut pas être enregistrée, l'interface n'est pas forcément en cause : nginx peut servir les fichiers statiques alors que l'API ou PostgreSQL sont indisponibles. Commence par identifier précisément l'action qui échoue et la réponse HTTP, puis compare la sonde de vie et la sonde de disponibilité. **Limite :** une sonde positive ne prouve pas qu'un ticket peut être créé ; seule une vérification métier contrôlée le confirme.

## Ce qu'il faut obtenir

Marie (collaboratrice) crée le ticket « Mon poste ne se connecte plus au VPN » ; Karim (support) le prend en charge.

1. **Un schéma** du trajet de ces deux actions : chaque composant traversé, la méthode et l'adresse HTTP, le code de réponse attendu.
2. **La liste des données durables** : ce qui doit exister après un redémarrage complet.
3. **Deux garanties** apportées par l'application, et **deux limites**.
4. **Trois questions** à poser avant d'héberger ce service.

## Vérifications

| Ce que tu vérifies | Réponse attendue |
| --- | --- |
| Le navigateur parle-t-il à l'API ou à la base ? | Non, dans le parcours utilisateur : `frontend`, port 8080 |
| Qui vérifie le jeton et le rôle ? | `backend`, pas nginx |
| Où le ticket est-il écrit ? | Dans PostgreSQL, sur un volume |
| Que reçoit Marie si elle tente la prise en charge ? | Un refus `403` |
| Facultatif, pile locale : `curl -i http://127.0.0.1:8080/health/ready` | `200` et `"database":"up"` |

## Codes à savoir lire

| Code | Sens |
| --- | --- |
| `401` | Pas de jeton, ou jeton expiré |
| `403` | Compte connu, rôle insuffisant |
| `409` | Transition de statut interdite |
| `503` | L'API tourne mais ne joint pas la base |
| `502` / `504` (nginx) | nginx ne joint pas l'API ou dépasse un délai |

## Ce que tu dois savoir expliquer

Le trajet d'une création de ticket ; la différence entre `401` et `403` ; pourquoi le ticket survit au redémarrage de l'API et ce qui le ferait disparaître ; la différence entre `/health/live` et `/health/ready` ; ce qu'une réponse `200` ne garantit pas.

Suite : [exercice 02](02-architecture.md).
