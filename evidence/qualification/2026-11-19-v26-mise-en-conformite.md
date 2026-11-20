# Mise en conformité V26 — preuves datées

Base de revue : `d2a8e9e204b1bb797c26b1e1c927b9ec4fe166b1`. Date locale : 19 novembre 2026 (les logs sont en UTC, le 20 novembre).

## Recette applicative

[Run 44645263160](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645263160) — succès, commit d'application `1a3d60decebf1c26a70c275be90ab876ee353bcd`. Runner Ubuntu isolé ; ni Rocky ni K3s.

- [Backend](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645263160/job/135986093052) : Ruff réussi ; 28 tests réussis sur SQLite et 28 sur PostgreSQL 17 (1 avertissement dans chaque suite).
- [Frontend](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645263160/job/135986093026) : installation verrouillée, typage et build réussis.
- [Compose](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645263160/job/135986092616) : smoke ALL GOOD, tests d'isolation, reprise API et PostgreSQL et persistance du ticket après recréation.

Ces résultats précèdent la mise à jour des paquets des images. Ils ne lui sont pas transférables.

## Recette graphique

[Run 44645955660](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645955660) — 15 sources / 15 exports, 30 rendus en clair/sombre ; deux exports natifs Draw.io 32.7.4. Minimum déclaré estimé : séquence 12 px en grand, diagnostic 11,04 px à 700 px, architecture détaillée 11 px en grand. Les 13 compositions historiques sont préservées. Une finition des annotations et des flux a été identifiée après examen des deux nouvelles vues ; nouvelle recette à consigner. Consultation interactive GitHub/Notion à vérifier.

## Premier scan v2

[Job 135988455140](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44645955660/job/135988455140), Trivy 0.74.0, base d'avis téléchargée le 20/11/2026 UTC. Périmètre : images API et frontend du commit `5cd4562ac4740dd8d9df62dbaf457d9b66be974a`, scan de secrets du contenu actif (hors legacy et .git).

| Cible | CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN | Secrets détectés |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| API | 0 | 53 | 112 | 68 | 7 | 0 |
| Frontend | 1 | 56 | 83 | 96 | 2 | 0 |
| Sources actives | — | — | — | — | — | 0 |

Occurrences, pas nombre de CVE distinctes. Critique observée : `CVE-2026-111497` sur `brotli-libs 1.2.0-r0`, correctif indiqué `1.2.1-r0`. Le job réussi signifie que le scan s'est exécuté, non que la sécurité est validée. La mise à jour des paquets des deux bases vise les correctifs disponibles ; les vulnérabilités non corrigées demandent triage et limites d'exposition. L'image tierce PostgreSQL et l'historique Git ne sont pas couverts par ce premier scan.

Aucune réalisation personnelle ni niveau d'autonomie validé. La recette ponctuelle ne constitue pas le pipeline de livraison de l'exercice 08.

## Recette de finition et second scan

[Run 44646629874](https://github.com/mathiasseguincadiche/OpsDesk/actions/runs/44646629874) — six jobs réussis ; code testé `a2d89673980c39abe906e96d78fd88a78b75e7a7`, exports finaux `5032700eedcfd21952cb8eb52894b97f8cc650c1`. Ruff, 28 tests SQLite, 28 tests PostgreSQL 17 (un avertissement par suite), frontend typage/build, smoke ALL GOOD, reprise API/base, persistance après recréation des trois conteneurs. Runner Ubuntu jetable, pas de laboratoire Rocky. 15 paires Draw.io/SVG, 30 rendus navigateur, finitions des deux nouvelles vues inspectées. Recette native d'export Draw.io réussie ; interaction Notion/GitHub et appareils réels non testés.

Le job sécurité a construit ses propres images ; ne pas confondre ces digests avec les images du job Compose.

| Image scannée | CRITICAL | HIGH | MEDIUM | LOW | UNKNOWN |
| --- | ---: | ---: | ---: | ---: | ---: |
| API | 0 | 52 | 111 | 68 | 7 |
| Frontend | 0 | 0 | 0 | 0 | 0 |
| PostgreSQL 17-alpine (nouveau périmètre) | 1 | 26 | 40 | 3 | 1 |

Digests du job sécurité : API `sha256:92e7cc9ee918ad172be1f4593cd2b618dace6d33e3d22bbd69dd1f3a906567cb`, frontend `sha256:88f55860ba3854dbbe27e1eab0f3798a3c1578fa91fb38108f93e36eff51b423`, PostgreSQL `sha256:526f86d93c6ea08fd3f1fe5605650cacc781b2c6013169a0ad8f42c7d3d84f32`.

L'occurrence critique brotli du frontend n'est plus signalée. PostgreSQL : occurrence critique CVE-2025-68121 (bibliothèque standard Go 1.24.6) ; identifier le binaire réel et la version officielle corrigée. Aucun secret détecté dans le périmètre actif. La qualification sécurité est en échec sur le critère d'absence de vulnérabilités graves non traitées ; [suivi #51](https://github.com/mathiasseguincadiche/OpsDesk/issues/51). Ne pas exposer le laboratoire.
