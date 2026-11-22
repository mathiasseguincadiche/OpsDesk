# 02 — Architecture et décisions techniques

> Énoncé de référence, lisible sans Notion. Le cours complet (explications, exemple travaillé, indices) est dans la fiche Notion de l'exercice 02, accessible sur invitation.

**Objectif.** Défendre une décision d'architecture : le besoin qu'elle couvre, ce qu'on a écarté, ce qui se passe quand elle lâche, et comment on la vérifiera.

**Durée estimée** : 2 à 3 heures. **Prérequis** : exercice 01 ; le [registre des décisions](../architecture.md#décisions-retenues) ouvert. **État** : prévu, non vérifié.

## Pourquoi

Un choix qu'on ne sait pas expliquer ne se défend pas en entretien, et ne se corrige pas le jour où le contexte change. Un défaut coûte peu sur un dessin, beaucoup une fois les serveurs construits.

## L'essentiel à comprendre

- L'architecture est déjà décidée : trois serveurs Rocky Linux (`srv-admin`, `srv-app`, `srv-k3s`), Docker Engine et Compose sur `srv-app`, une sauvegarde copiée hors des serveurs, K3s pour une copie d'essai.
- Une décision se défend avec quatre réponses : **besoin et raison du choix, alternative et compromis, point de panne et condition de réexamen, contrôle**. Pour les décisions structurantes, expliquer quand une autre approche deviendrait préférable.
- Un schéma est juste quand chaque flux a une origine et une destination, chaque donnée durable un emplacement, chaque port ouvert une raison.
- Une décision « retenue » n'est pas « vérifiée » : rien n'est encore construit.
- Une raison manquante s'écrit comme question ouverte ; on ne l'invente pas.

## Cas voisin : comparer deux emplacements de journaux

**Exemple de décision fictive, non appliquée à OpsDesk.** Un service d'essai peut garder ses journaux uniquement dans un conteneur, ou les envoyer vers une collecte externe. La première option est simple et peu coûteuse, mais peut perdre l'historique lors d'une suppression ; la seconde facilite la recherche entre plusieurs instances, au prix d'une dépendance et d'un stockage supplémentaires.

**Méthode.** Formule le besoin (« retrouver un incident après recréation »), les alternatives, la conséquence d'une panne du collecteur et un contrôle mesurable (retrouver un identifiant de requête après recréation). Si tu ne connais ni le volume de logs ni la durée de conservation nécessaire, indique cette incertitude plutôt que d'inventer un SLO. Pour OpsDesk, les décisions à défendre restent celles de l'énoncé et du registre.

## Ce qu'il faut obtenir

1. **Un tableau de cinq décisions**, avec les quatre réponses : trois serveurs Rocky Linux ; Docker Compose sur le serveur plutôt que Kubernetes ou Podman ; l'administration de Docker par `sudo` plutôt que par le groupe `docker` ; la sauvegarde `pg_dump` copiée hors des serveurs ; K3s pour une copie d'essai seulement.
2. **Les flux redessinés de mémoire**, puis comparés au [schéma](../diagrams/architecture.svg) : requête d'utilisateur, connexion SSH de l'administrateur, sauvegarde nocturne, restauration.
3. **Une revue contradictoire** : au moins trois points qui ne tiennent pas ou qui manquent, chacun avec sa raison.

## Vérifications

| Ce que tu vérifies | Comment |
| --- | --- |
| Chaque décision a ses quatre réponses | Aucune case vide ; une incertitude porte « question ouverte » |
| Chaque flux a une origine, une destination et un port | Comparaison avec le schéma, différences expliquées |
| Chaque port ouvert de `srv-app` a une raison | 22, 8080, 8000 et 9100 |
| Chaque donnée durable a un emplacement et une copie | Base, sauvegardes, état Terraform, clés SSH |
| Les contrôles sont réalisables | Une commande ou une observation précise, pas « ça marche » |

## Un exemple de revue, déjà mené

Le flux Prometheus → `srv-app:8000` est cohérent sur le papier (nginx bloque `/metrics`, le port 8000 est ouvert à `srv-k3s` seulement). Il impose de publier le port 8000 dans le fichier Compose de production, et il ouvre toute l'API à `srv-k3s`, pas seulement `/metrics` : une limite de la cible initiale, à traiter et à vérifier à l'exercice 09 ; les schémas et le registre évolueront après preuve.

## Pièges fréquents

Recopier la raison du registre mot pour mot ; confondre volume et sauvegarde ; croire qu'un K3s à un seul nœud rend le service hautement disponible ; corriger un défaut en silence ; écrire « vérifié » pour une décision retenue.

Suite : [exercice 03](03-linux-reseau.md).
