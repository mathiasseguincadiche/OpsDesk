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
