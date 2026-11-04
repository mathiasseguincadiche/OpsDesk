# OpsDesk — triage de sécurité applicative V4.4

**Verdict global conservé : FAIL. Triage contextualisé : PARTIEL. Aucune autorisation d’exposition Internet ni acceptation du risque.** Ce document distingue l’application fournie par Codex et la sécurité de l’infrastructure que Mathias construira personnellement.

## Source et fraîcheur

Le [rapport Trivy conservé](../evidence/vulnerability-scan.json) a été produit avec Trivy 0.74.0 sur `v42opsdesk-app:0.1.0-local`, image `sha256:2fa15b716fd4f4df2d286f412cca1b3b323cc484677a0ac3866a8fecced5ac95`. Sa date est `2026-11-03T13:48:01.065269+00:00`. La base explicitement utilisée a été mise à jour le 3 novembre 2026 à 07:14 UTC et téléchargée à 13:36 UTC. Le cache par défaut plus ancien affiché par une commande générale de version n’est pas le cache utilisé ici.

Ce triage ne relance pas un scan et ne reconstruit pas l’image. Les sources applicatives V4.4 ont leurs tests distincts ; l’ancien scan ne prouve pas une nouvelle image déployée. Le [JSON de qualification](../evidence/v44/security-triage.json) conserve empreinte SHA-256, identité d’image, métriques et réserves.

## Lire les chiffres sans les gonfler

| Mesure | Résultat |
|---|---:|
| Occurrences paquet/avis | 185 |
| Identifiants d’avis uniques | 85 |
| HIGH / MEDIUM / LOW / UNKNOWN | 45 /72 /61 /7 |
| CRITICAL | 0 |
| Occurrences HIGH/CRITICAL avec version corrective renseignée dans ce scan | 0 |
| Classe OS / classe langage | 185 /0 |

Les 185 occurrences ne signifient pas 185 failles différentes exploitables. Un même avis peut affecter plusieurs sous-paquets d’un composant ; par exemple CVE-2026-76642 apparaît neuf fois. Les 85 identifiants ne sont pas non plus un décompte de failles certifié : les alias CVE/GHSA ne sont pas exhaustivement normalisés. Aucun constat n’est supprimé comme doublon artificiel.

## Qualification des risques

| Groupe | Constat et portée | Décision |
|---|---|---|
| Bibliothèques et utilitaires Debian | Tous les constats enregistrés appartiennent au système de l’image. Leur présence est attestée ; leur exploitation depuis le parcours métier n’est pas démontrée. | Garder les 45 HIGH ouverts ; examiner support et correctifs officiels avant tout usage partagé ou public. |
| Exemple util-linux / mount | Le [suivi Debian CVE-2026-76642](https://security-tracker.debian.org/tracker/CVE-2026-76642) indique la version trixie de l’image affectée. Les routes métier fournies n’appellent pas volontairement un helper mount ; cette lecture du code n’est pas un test d’intrusion. | Ne pas assimiler absence d’appel prévu à innocuité globale. Aucun changement OS/permissions n’est fait ici. |
| Code applicatif Python | Aucun constat de classe langage dans ce rapport ; contrôles d’entrées et d’accès documentés par les tests applicatifs. | Un PASS de test ou l’absence de finding Python ne constitue pas une certification de sécurité. |
| Identités et données de développement | Données fictives, secrets exclus des preuves, accès de développement limité au laboratoire. | Contrôler les secrets et les journaux ; aucune identité réelle n’est révoquée ou remplacée ici. |

OpsDesk reste un démonstrateur fictif sans authentification utilisateur ; son usage de développement et ses hôtes autorisés doivent rester explicites. Les protections testées côté application ne remplacent pas la conception des accès, du transport et des permissions de la future infrastructure.

## Corrections et réserves

Le retrait historique des outils d’installation inutiles a déjà réduit l’image runtime ; le rapport défavorable antérieur est conservé. Zéro correctif HIGH/CRITICAL renseigné pour ces occurrences OS signifie seulement que la base de ce scan n’en fournit pas pour la version détectée. Cela ne démontre ni l’absence de risque ni l’absence d’une correction dans toute autre branche de distribution.

La suite doit examiner les avis fournisseurs, la compatibilité d’une image corrigée et la régression applicative. Aucune migration arbitraire vers une distribution instable, désactivation de scan, suppression de rapport ou règle d’ignorance globale n’est livrée. La sélection et le durcissement d’infrastructure restent des exercices personnels de Mathias, avec leurs preuves futures. Les réglages loopback et les tests fictifs n’autorisent aucune exposition publique.
