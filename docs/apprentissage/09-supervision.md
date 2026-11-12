# 09 — Superviser

**Projet : OpsDesk · Pilier : Observer/diagnostiquer · Accompagnement : guidé.** Exercice préparé ; réalisation et vérification personnelles NON EXÉCUTÉES ; autonomie NON ÉVALUÉE.

Révision documentaire : 2026-11-04. Les [règles communes et exigences conservées](README.md#cadre-commun-des-exercices) complètent cette fiche.

## Situation et résultat à obtenir

Quand un utilisateur ne peut plus enregistrer un ticket, un processus vivant ne suffit pas à rassurer l’équipe. La supervision doit rendre visible le besoin touché et donner une première piste de diagnostic.

Utilise les signaux applicatifs fournis et un contrôle de ticket. Relie une alerte à l’indisponibilité réelle du besoin, puis explique le retour attendu.

**Livrable attendu :** Signal choisi pour le métier, alerte constatée, logs corrélés et retour observé ; pas seulement une capture de tableau vide. Le résultat est à produire, pas déjà obtenu.

## Comprendre avant de choisir

Une métrique est une mesure, un journal explique un événement et une alerte signale un besoin d’action. La disponibilité d’un processus ne garantit pas le succès d’un parcours métier.

Une métrique mesure une grandeur à un instant ou sur un intervalle ; un journal relate un événement ; une alerte associe une condition à une action et à un destinataire. Prometheus collecte les échantillons ; Grafana présente des requêtes et leurs résultats. Un panneau vide peut venir de la collecte, de la requête ou de la fenêtre de temps.

Choisir unités, labels et portée avant un seuil. Les compteurs applicatifs par worker ne représentent pas automatiquement un total durable du service ; un redémarrage peut les réinitialiser. Un identifiant de ticket en label multiplie les séries inutilement. Relier un signal technique au contrôle métier aide à distinguer dépendance non prête et panne utilisateur réelle.

**Question :** `/metrics` répond mais le panneau ne montre aucun échantillon. Quel fait vérifier d’abord pour départager une cible jamais collectée et une requête qui filtre toutes les séries ?

## Préparer la bonne cible

Parcours applicatif et points de santé compris ; cible et version identifiées, collecte proposée. Vérifier les outils réellement installés et les accès autorisés. Ne pas définir une alerte à partir d’un compteur dont le sens ou la portée reste inconnu.

Le poste de contrôle prévu est Fedora 45. Choisir une collecte et une visualisation proportionnées au laboratoire déjà qualifié, sans créer une VM par outil. Identifier source de métriques, collecteur, destinataire d’alerte autorisé, réseau et limites de ressources. Les métriques d’une application ne signifient pas que Prometheus ou Grafana est installé. Consulter le [guide Fedora/KVM/Rocky et ses limites de compatibilité](../laboratoire-fedora-kvm-rocky.md). Les essais historiques Ubuntu/WSL de Codex restent distincts ; aucune vérification matérielle n’est revendiquée ici.

Prévoir Prometheus pour la collecte et Grafana pour une vue utile. k6 reste un essai de charge personnel, borné sur une cible locale autorisée : choisir débit/concurrence, durée, seuil d’arrêt et mesure de latence/erreurs avant exécution. Ne pas charger une cible publique ou le PC sans limite. La VM invitée cible reste Rocky Linux 10.2 ; sa qualification est à vérifier avant cet exercice.

Avant une modification, compléter les [précontrôles communs](README.md#avant-une-action) et vérifier le retour prévu. Identifier séparément le poste de contrôle, la cible et leurs accès ; aucun outil ou service n’est supposé déjà prêt.

## Réaliser soi-même et demander un indice

1. Choisir un besoin utilisateur, un signal et ses limites ; noter unité, source, fréquence et coût de collecte.
2. Écrire une collecte, une vue et une règle proportionnées ; identifier le destinataire autorisé et le retour attendu. Préparer le contrôle métier en parallèle.
3. Rapprocher métriques, journaux et alerte sur un cas réversible autorisé. Pour k6, proposer d’abord cible locale, débit/concurrence, durée et seuil d’arrêt ; ne pas déduire une capacité d’une capture isolée.

Conserver ta première proposition avant la revue. Les indices se lisent à la demande, du moins direct au plus ciblé.

<details>
<summary>Indice 1 — orientation</summary>

Formuler le symptôme, comparer métriques/logs/événements et contrôler la dépendance suspecte sans multiplier les modifications.

</details>

<details>
<summary>Indice 2 — mécanisme</summary>

Contrôler l’état de la cible de collecte et la présence d’échantillons bruts avant le panneau. Pour une alerte absente, distinguer condition non atteinte, délai d’évaluation et destinataire non configuré.

</details>

<details>
<summary>Indice 3 — correction ciblée après tentative</summary>

Présenter ta tentative, l’attendu, l’observé et le premier écart. Demander l’analyse du seul point bloquant ; tu modifies ensuite ta solution, tu retestes et tu expliques la correction. Une explication limitée peut être demandée avant l’action ; aucun fichier InfraOps définitif n’est fourni à recopier. Consigner le niveau d’aide reçu.

</details>

## Vérifier, puis diagnostiquer

- Distinguer une mesure du processus, une dépendance prête et un contrôle du besoin utilisateur ; vérifier les unités, la portée et les labels.
- Montrer collecte, visualisation utile, règle et destinataire autorisé ; un tableau sans données ou un /metrics isolé n’est pas une supervision reçue.
- Sur un cas réversible autorisé, rapprocher signal, alerte, journaux et retour à l’état attendu ; consigner aussi les faux positifs ou contrôles non exécutés.
- Revalider un ticket identifié, son titre, son état et sa relecture dans PostgreSQL, lorsque le service est disponible dans le périmètre du module ; si son installation n’est pas encore l’objet de l’étape, indiquer ce contrôle métier NON EXÉCUTÉ.

**Cas négatif de lecture :** une série absente n’est pas automatiquement une valeur zéro. Expliquer quelle conclusion serait trompeuse et quel contrôle de collecte la réfuterait. Une panne volontaire ou une charge réelle n’est pas nécessaire à cette lecture.

**Erreurs fréquentes :** Compter uniquement HTTP200 ; alerte sans destinataire ; générer un identifiant de ticket comme label à forte cardinalité.

**Démarche en cas d’écart :** Si un tableau est vide, distinguer absence d’échantillons, mauvaise requête et fenêtre de temps. Vérifier la cible collectée avant le panneau. Si aucune alerte n’arrive, distinguer règle non déclenchée et routage non configuré avant de provoquer une panne.

Séparer attendu et observé ; une cause reste hypothétique tant qu’un contrôle ne l’a pas confirmée. Utiliser le [fil de diagnostic commun](README.md#vérifier-et-diagnostiquer).

## Expliquer et capitaliser

Conserver le livrable annoncé, les observations et les [métadonnées de preuve](README.md#preuve-et-progression-personnelles), expurgées de secrets. Expliquer le besoin couvert, la décision prise, le contrôle qui la soutient et ce qui reste non vérifié. Séparer programme fourni, logiciel tiers, référence Codex et travail personnel.

**Réutilisation :** Quel indicateur garde son sens quand on change le nombre de réplicas ou redémarre le processus ? Relier ta réponse à un autre projet sans en recopier une solution complète.

Le résultat technique, sa compréhension, un diagnostic représentatif et ton explication s’évaluent séparément. Aucun niveau personnel n’est attribué par cette fiche.

## Corrigé après tentative

Après une première tentative, consulter [les repères de correction](corriges.md#exercice-09--superviser) ou demander le niveau d’aide souhaité. La référence historique Codex n’est pas la réponse obligatoire à reproduire.

[← Exercice précédent](08-cicd.md) · [Retour au parcours](README.md) · [Exercice suivant →](10-maintenance.md)
