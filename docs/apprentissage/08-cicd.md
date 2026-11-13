# 08 — Construire la CI/CD

**Projet : OpsDesk · Pilier : Faciliter la livraison · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

L’équipe doit pouvoir relier un changement à ses tests et à l’artefact livré. Une CI/CD utile automatise des contrôles compris et empêche de confondre une ancienne preuve avec le résultat du changement courant.

Construis une première chaîne GitHub Actions. Étudie le cas historique où le smoke écrit ci-business.json mais la reprise lit business-smoke.json : explique quel ticket est utilisé et comment prouver la correction, sans recopier le pipeline.

**Livrable attendu :** Jobs personnels expliqués, échec discriminant diagnostiqué, même artefact testé livré et contrôle métier après livraison. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

La CI formalise des contrôles déjà compris ; la livraison déplace un artefact identifié vers une cible autorisée. Une preuve doit appartenir au commit/run courant, pas être un ancien PASS joint au hasard.

Un **déclencheur** choisit quand le workflow commence. Un **job** regroupe des étapes exécutées sur un **runner** ; une **step** lance une commande ou une action. Des dépendances entre jobs imposent l’ordre utile, sans supposer qu’ils partagent la même machine ou le même répertoire. Les permissions du jeton, les secrets et l’accès réseau déterminent ce que chaque job peut faire.

Les tests, rapports et images ont des identités différentes. Un artefact de preuve doit citer commit, run et méthode ; l’image doit garder le même digest entre test et promotion. GHCR stocke l’image ; Trivy fournit un verdict de scan à interpréter, avec sa date et sa base de vulnérabilités. Le FAIL historique ne remplace pas le scan de ton nouvel artefact et un scan seul ne prouve pas la sécurité globale.

Un runner GitHub hébergé se trouve hors du PC : il ne rejoint pas par défaut ta VM privée KVM. L’accès à une cible doit être conçu, autorisé et contrôlé ; ne pas rendre l’application publique pour contourner cette frontière. La CI de tests peut être utile avant qu’une livraison distante soit possible.

**Investigation historique, sans recopier le workflow :** un smoke écrit `ci-business.json` et une reprise lit `business-smoke.json`. Identifier producteur, consommateur, ticket témoin, date et identité du run. Quelle assertion ferait échouer la chaîne si le consommateur utilise une ancienne preuve ? Le constat porte sur la référence historique, pas sur un workflow présent et exécuté dans main.

Références : [runners GitHub hébergés](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners) et [accès aux réseaux privés](https://docs.github.com/en/actions/concepts/runners/private-networking).

## Préparer la bonne cible

Procédure manuelle de test et de livraison comprise, artefact identifié et cible de validation autorisée. L’étude K3s est disponible ; une livraison conteneur sur la cible retenue reste possible si K3s n’a pas encore été qualifié. Ne pas contourner un blocage en prétendant un déploiement de cluster.

Ansible est lancé à la main depuis `srv-admin`, où le développeur se connecte en SSH : il choisit une version quand la CI est verte, `srv-app` tire l’image, puis `/health/ready` est contrôlé ; le retour arrière redéploie la version précédente. Les sources personnelles sont conservées dans le dépôt GitHub principal du projet. Identifier séparément le runner choisi et `srv-app`, VM Rocky Linux 10.2 cible sous KVM ; un runner hébergé n’accède pas implicitement au laboratoire local. La cible de livraison, son accès et ses permissions doivent être proposés et vérifiés avant tout déploiement. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL restent distincts ; aucune vérification matérielle n’est revendiquée ici.

La chaîne étudiée est GitHub Actions, avec GHCR pour un artefact identifié et Trivy pour conserver le verdict de scan. Définir permissions minimales, secrets, rétention des preuves et arrêt sur échec. Le diagnostic du contrat de preuve historique ci-business.json/business-smoke.json reste un cas à expliquer, pas un pipeline à recopier.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Dessiner ta chaîne de contrôles à partir de la procédure manuelle : déclencheur, jobs, étapes, entrées, sorties et conditions d’arrêt.
2. Choisir le runner, ses permissions et les accès possibles ; écrire ton workflow personnel sans créer de secret ni publier automatiquement une image.
3. Relier commit/run/rapports/digest ; expliquer le cas historique de preuve périmée. Préparer la promotion du même artefact seulement vers une cible accessible et autorisée, puis contrôler version et données.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Nommer job, étape, commande, message, hypothèse et test final ; distinguer refus d’accès, variable absente, test métier et mauvais artefact.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Pour une preuve absente ou périmée, comparer nom exact du fichier, répertoire de travail, producteur, transfert entre jobs et consommateur. Chercher la première étape qui accepte une preuve sans vérifier son identité.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Relier commit, run, jobs et artefact testé ; conserver le premier échec utile et vérifier que la preuve appartient au run courant.
- Promouvoir le même artefact vers la cible retenue, avec accès justifiés et accord d’environnement ; ne pas reconstruire sous le même tag entre test et livraison.
- Contrôler version et données après livraison et après le retour prévu ; un job de succès sans contrôle de la cible ne vaut pas déploiement.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Test négatif à concevoir :** sur des données de test, faire refuser une preuve dont le commit ou le ticket ne correspond pas au run courant. Aucun déploiement ni secret réel n’est nécessaire pour raisonner sur ce contrat ; garder le contrôle NON EXÉCUTÉ avant son essai personnel.

**Erreurs fréquentes :** Déployer depuis un runner public en supposant un accès au KVM local ; secrets dans les logs ; ancien JSON PASS présenté comme preuve du run.

**Démarche en cas d’écart :** Si le pipeline passe mais la cible affiche une autre version, distinguer artefact reconstruit, mauvais environnement et preuve périmée. Comparer commit/run/digest à l’identité servie ; corriger le point démontré et refaire le contrôle utilisateur.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence historique et travail personnel.

**Réutilisation :** Comment prouver qu’une promotion n’a pas reconstruit une image différente ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-08--construire-la-cicd) ou demander le niveau d’aide souhaité. La référence historique n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](07-k3s.md) · [Retour au parcours](README.md) · [Exercice suivant →](09-supervision.md)
