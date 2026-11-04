# Reprise minimale d’un ticket — essais historiques Codex

> **HISTORIQUE — référence Codex non exécutable depuis le dépôt courant.** Au contrôle de `main` du 4 novembre 2026 (`51e1a489`), `scripts/recovery_lab.py` et la configuration Compose sont absents. Les blocs de commandes conservent les anciennes instructions pour comprendre l’essai Ubuntu/WSL ; ils ne sont pas prêts à copier et ne lancent pas le laboratoire personnel. Les versions et résultats qui suivent sont historiques. [Parcours actif V4.4](apprentissage/README.md) · [Pré-checks Fedora/KVM/Rocky](laboratoire-fedora-kvm-rocky.md).

## Triage court avant une reprise personnelle

**Méthode documentaire réalisée — non vérifiée sur le laboratoire personnel.** Cette section aide à décider quoi observer ; elle ne rend pas la recette historique ci-dessous exécutable. Symptômes d’entrée : tickets inaccessibles, lecture/écriture refusée, readiness en échec ou données attendues absentes.

1. Identifier la machine, la version, le point d’entrée et le ticket témoin ; noter heure, symptôme et impact. Si l’identité est ambiguë, arrêter avant modification.
2. Lire les observations déjà accessibles : processus/ports, live/ready, réponse métier et journaux expurgés. Sans instance personnelle préparée, consigner l’impossibilité et revenir à l’exercice concerné, sans essayer le port historique au hasard.
3. Séparer défaut d’accès, application, connexion DB, schéma et stockage. `/metrics` HTTP 200 peut accompagner une DB indisponible : sa valeur est à lire dans le contrat. Choisir une vérification discriminante en lecture seule ; ne pas réinitialiser le stockage pour tester une hypothèse.
4. Si une restauration est justifiée, vérifier version de l’archive, destination indépendante, sauvegarde source et retour réellement essayé. Sans archive identifiée/restaurable ou sans accord pour une action risquée, arrêter et préparer le [protocole personnel](apprentissage/11-sauvegarde-reprise.md). Aucun point de non-retour n’est franchi par cette fiche.
5. Après une correction personnellement choisie et autorisée, contrôler accès, identité, lecture/écriture et ticket témoin ; consigner attendu/observé et durée/perte réellement mesurées. Une réponse 200 isolée ne suffit pas.

**Passer le relais :** Mathias est le responsable du laboratoire personnel. Si la cause reste inconnue après la vérification discriminante, si des données risquent d’être perdues ou si un secret apparaît, arrêter les mutations et lui soumettre les faits expurgés. Aucun service d’astreinte ni contact externe n’est défini ou sollicité par ce projet. Après incident, mettre à jour la procédure et conserver l’échec suivi de sa nouvelle validation.

## Référence historique Codex — cadre V4.4

Ce corps conserve les procédures et résultats préparés sous V4.2. Les configurations et opérations InfraOps appartiennent désormais au travail personnel de Mathias ; elles ne sont pas relancées par Codex. Consulter d’abord le [contrat applicatif](contrat-applicatif.md) et la [provenance](provenance.md). Les niveaux techniques anciens de ce texte ne sont pas les niveaux personnels V4.4 : L0 découverte, L1 compréhension, L2 réalisation personnelle, L3 autonomie vérifiée. Les preuves de reprise plus récentes sont datées dans [STATUS](../STATUS.md), sans modifier rétrospectivement cet essai.

Le 3 novembre 2026 à 13:48:10 UTC, `scripts/recovery_lab.py` a exporté PostgreSQL puis restauré les tickets dans une base et une application sur volumes/réseau neufs. Le ticket fermé a été relu via HTTP : ID, titre, description, priorité, statut et dates strictement identiques. La source 18081 est restée disponible, la cible 18086 distincte. Durée observée : 10,769 s, dans [le rapport historique conservé](../evidence/recovery-history-20261103T135154Z.json). Un essai ultérieur, le même jour à 13:52:06 UTC, utilise la cible 18088 et mesure 10,969 s dans [le dernier rapport V4.2](../evidence/recovery.json). Aucune de ces mesures n’est une réception personnelle ni un essai rejoué par cette mission documentaire.

Prérequis : laboratoire local OpsDesk sain, ticket référencé dans business-smoke.json, Docker autorisé, PyYAML 6.0.3 et port 18086 libre sur Ubuntu/WSL. La commande historique, depuis la racine du laboratoire, créait une nouvelle cible et des fichiers privés ; elle est non exécutable depuis le dépôt courant :

```bash
python3 scripts/recovery_lab.py --port 18086
```

Les notes historiques décrivent un refus des ports utilisés, un nom de cible aléatoire et l’absence de suppression de source ou de `down -v`. Le dump, les fichiers privés de cible et les secrets étaient placés sous `.local/` ; leur présence actuelle hors dépôt est NON VÉRIFIÉE. Le dump de cet exercice OpsDesk était signalé non chiffré ; il ne constitue pas une politique de sauvegarde exploitable. Prévoir chiffrement, destination indépendante, rétention, fraîcheur et identités protégées avant usage réel.

Un ticket comparé démontre ce contrôle précis ; il ne qualifie pas tous les volumes, les écritures concurrentes, une perte physique, K3s ni Rocky. Un redéploiement d’image seul n’aurait pas restauré un ticket perdu. Le rapport historique identifie l’image locale exacte par son ID et des droits applicatifs limités après restauration.
