# 04 — Provisionner avec Terraform

**Projet : OpsDesk · Pilier : Automatiser · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Créer une VM à la main ne fournit pas encore une méthode reproductible. Terraform permet de décrire les ressources, de prévoir leurs changements et de relier leur identité réelle à une configuration versionnée.

Écris les ressources du laboratoire autorisé et explique chaque différence du plan. Montre que le state correspond à la bonne cible avant ton apply.

**Livrable attendu :** Code personnel, plan expliqué, état protégé et ressources observées correspondant au plan. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Terraform compare la configuration au state et à l’état distant pour calculer un plan. Le state contient des identités et parfois des secrets ; un fichier terraform_data local ne crée pas une VM.

Le **provider** est le composant qui traduit les ressources Terraform en appels à l’API choisie, ici celle du laboratoire libvirt. Sa version et ses ressources disponibles doivent correspondre à ta documentation. Trois objets restent distincts : la configuration décrit l’état souhaité ; le **state** associe les adresses Terraform aux identifiants gérés ; la ressource réelle est la VM ou le volume observé dans libvirt. Le state ne remplace pas la vérification de la cible et peut contenir des secrets.

**Lire le cycle avant de l’utiliser — repères conceptuels, pas un bloc de commandes prêt à lancer :** `init` prépare backend et providers et écrit des fichiers locaux ; `fmt` met en forme les fichiers et peut les modifier ; `validate` vérifie la cohérence de la configuration sans prouver l’accès à libvirt ; `plan` calcule les changements à partir des informations disponibles et peut interroger l’API ; `apply` exécute les changements acceptés et modifie les ressources. Un plan correct à un instant peut devenir périmé si l’environnement change. Aucun de ces mots n’autorise ici un apply, un import ou une destruction.

**Lecture fictive, sans exécution :** un plan annonce une création de VM et le remplacement d’un volume existant. Quelle ressource contient les tickets ? Quelles identités, quel backend/workspace et quelle URI libvirt dois-tu vérifier avant de décider ? Une seule ressource `terraform_data` n’appelle pas libvirt pour créer une VM.

Références : [cycle Terraform](https://developer.hashicorp.com/terraform/intro/core-workflow), [init](https://developer.hashicorp.com/terraform/cli/commands/init), [fmt](https://developer.hashicorp.com/terraform/cli/commands/fmt), [validate](https://developer.hashicorp.com/terraform/cli/commands/validate), [plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [apply](https://developer.hashicorp.com/terraform/cli/commands/apply). Lire la documentation correspondant à la version personnellement retenue.

## Préparer la bonne cible

Accès libvirt et laboratoire identifiés à l’exercice 03 ; versions de Terraform et du fournisseur vérifiées dans le guide. Distinguer ressource existante, ressource d’essai à créer et ressource déjà gérée. Pas de configuration complète fournie à recopier.

Le poste de contrôle prévu est Fedora 45 ; les ressources à gérer sont des ressources KVM/libvirt identifiées du laboratoire. Terraform et la version du fournisseur libvirt choisi doivent être vérifiés séparément. La VM Rocky Linux 10.2 est la cible ; une VM créée manuellement n’appartient pas automatiquement au state Terraform. Ne pas adopter, remplacer ou supprimer une ressource existante par supposition. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Établir le propriétaire des ressources existantes et la cible autorisée ; choisir et justifier provider, version, backend et protection du state.
2. Écrire ta première configuration limitée, puis définir tes contrôles de forme, validation et lecture du plan. Expliquer chaque création, modification ou remplacement avant toute action.
3. Après autorisation et réalisation personnelle, rapprocher l’identifiant libvirt observé de celui géré par Terraform ; refaire un plan et expliquer toute dérive.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Localiser l’erreur entre syntaxe, provider/authentification, droits, quota ou dérive ; ne pas supprimer le state comme premier réflexe.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Distinguer un défaut de syntaxe d’un échec d’accès au provider, puis une mauvaise association d’identité. Comparer URI, backend/workspace et identifiant réel avant d’envisager une correction du state.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Expliquer le fournisseur, sa version, l’URI libvirt et les ressources visées ; chaque différence du plan doit correspondre au laboratoire autorisé.
- Après son intervention personnelle, rapprocher l’identifiant réel de la ressource et son état du plan lu ; un terraform_data local ne vaut pas création de VM.
- Rejouer le plan sans changement voulu, interpréter le résultat et protéger le state ; ne pas publier un state pour prouver la réussite.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Contrôle négatif sans mutation de ressource :** sur une copie de travail, proposer une configuration volontairement incohérente à faire rejeter par la validation. Expliquer pourquoi ce refus ne prouve ni la disponibilité du provider ni la sécurité d’un plan ; ne lancer aucun apply sur cet exemple.

**Erreurs fréquentes :** Confondre validation syntaxique et ressource créée ; versionner le state ; forcer un apply sur la mauvaise cible.

**Démarche en cas d’écart :** Si le plan ne vise pas la VM attendue, distinguer mauvais workspace/backend, mauvais URI libvirt et ressource non gérée. Lire la cible et les identifiants avant toute correction ; ne pas effacer le state, importer ou détruire une VM pour faire disparaître l’écart.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#verifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

**Réutilisation :** Comment reprendre le même besoin dans un second environnement sans partager les identités de ressources ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-04) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](03-linux-reseau.md) · [Retour au parcours](README.md) · [Exercice suivant →](05-ansible.md)
