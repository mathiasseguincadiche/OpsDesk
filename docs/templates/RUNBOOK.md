# Runbook — [opération ou incident]

**Portée :** [hôte, VM, service, version, responsabilité] · **État :** procédure à qualifier.

## 1. Quand utiliser cette procédure ?

[Symptômes, impact métier, objectif et conditions d'arrêt.]

## 2. Préparer la cible et les outils

- [ ] Identifier la bonne machine, le compte et le service.
- [ ] Inventorier les outils installés et leurs versions.
- [ ] Installer les composants manquants seulement si nécessaire, avec méthode de vérification.
- [ ] Vérifier l'état initial, les permissions, le pare-feu et SELinux.
- [ ] Prévoir sauvegarde, créneau d'intervention, conditions de rollback.

## 3. Diagnostiquer sans détruire

| Hypothèse | Commande / contrôle | Interprétation |
| --- | --- | --- |
| […] | […] | […] |

## 4. Exécuter une opération approuvée

```bash
# Exemple : indiquer précisément hôte, droits et effet réel.
[commande à adapter]
```

[Arguments, risques et résultats attendus, sans sortie fictivement « OK ».]

## 5. Vérifier fonctionnellement

- [ ] Le service répond sur la bonne version.
- [ ] Les données restent accessibles.
- [ ] Les sondes et journaux concordent.
- [ ] Le besoin métier est effectivement couvert.

## 6. Retour arrière et escalade

[Déclencheur, sauvegarde utilisée, effet sur la donnée et vérification après restauration.]

## 7. Compte rendu et preuve

- Date et cible : […]
- Commit, version, digest : […]
- Actions réellement exécutées : […]
- Résultats observés : Non exécuté
- Limites et suites : […]
