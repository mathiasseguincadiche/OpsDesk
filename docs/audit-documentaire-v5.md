# OpsDesk — application ciblée de la charte documentaire V5

Révision : 4 novembre 2026. Responsable de validation : Mathias. Rédaction et contrôles : Codex, même IA ; aucune revue humaine ou indépendante n’est simulée. Cette passe documentaire ne réalise pas les exercices InfraOps à la place de l’apprenant.

## Couverture et état de référence

Base distante relue : `main` au commit `886918115e4321c89c0923e4ea95286c50e2e506`, arbre `4f043cd6235dc0f6d99b6b19328c92fc90e6c506`. La PR [#3](https://github.com/mathiasseguincadiche/OpsDesk/pull/3) est fusionnée depuis le 4 novembre à 18:38:48 UTC. Son [audit V4](audit-finalisation-v44.md) est conservé comme réception historique ; il ne décrit pas l’état de cette nouvelle revue.

Les 85 fichiers de l’arbre ont été inventoriés : 84 textes ont été comparés par hash Git au snapshot local, zéro divergence avant intervention ; le binaire `evidence/interface.png` est recensé mais non téléchargé ni relu. L’authentification locale du clone n’est pas utilisée : lecture/publication par le connecteur GitHub, en conservant le vrai parent distant et tous les fichiers hors périmètre.

Le corpus V5 fourni comprend 15 fichiers : 12 modules, compilation, index et introduction. Les fichiers sont copiés et hachés dans le dossier de travail ; comparaison V4/V5 automatisée de l’intégralité des modules et relecture ciblée de leurs nouveautés, avec les règles inchangées du corpus V4 déjà appliquées. Il ne s’agit pas d’une nouvelle lecture linéaire intégrale de chaque module V5. Les 12 modules individuels sont retrouvés octet pour octet dans la compilation ; cette dernière n’est pas un deuxième ensemble d’exigences. Les prompts restent un référentiel de qualité désigné par l’utilisateur, sans étendre les autorisations opérationnelles.

Relecture ciblée : neuf Markdown existants modifiés ci-dessous ; `business.py`, `web.py`, `schema.sql`, générateur de schémas, preuves et tests concernés par lecture statique ; sept pages Notion existantes. La vérification automatique parcourt les liens/ancres/fences de tous les Markdown. Les autres fichiers sont contrôlés pour leur intégrité ; ils ne constituent pas une nouvelle revue de code exhaustive. Les 13 exercices déjà validés restent en place, avec leur cadre commun renforcé. Les 16 ressources, cinq évaluations, 18 tâches historiques et archives ne sont pas réécrits. Aucune propriété ou ligne de la base Notion n’est modifiée par cette passe.

## Verdict par dimension

| Dimension | Verdict et portée |
|---|---|
| Exactitude des changements | Prêt sur les éléments relus : fusion #3, API actuelle, origine des SVG et fichiers réellement présents |
| Structure/navigation | Prêt pour les ajouts contrôlés ; aucun déplacement ni nouvelle base ; liens et ancres vérifiés par le contrôle livré |
| Pédagogie | Prêt avec réserves : preuves, décisions et triage explicités ; aucune séance utilisateur réelle menée |
| Preuves et statuts | Prêt documentaire : avancement/contrôle/niveau personnel distincts ; contrôle technique personnel non évalué |
| Rédaction | Prêt sur les ajouts relus ; vocabulaire commun, conventions existantes conservées |
| Sécurité | Prêt avec réserves pour le diff documentaire ; sécurité de l’application et de l’infrastructure non reçue, triage historique FAIL conservé |
| Présentation/accessibilité | Non évaluée sur les interfaces natives pendant cette passe ; XML analysé et réserves précédentes conservées |

L’exercice 01 reste accessible sans installation ni VM. Les représentations SVG existent, mais la réception d’un véritable export par Draw.io reste incomplète. Ces verdicts ne sont ni une note globale, ni une certification de production.

## Écarts confirmés et corrections

| Priorité | Emplacement précis | Constat, conséquence et correction | Contrôle |
|---|---|---|---|
| P0 | Accueil Notion, premier encadré ; STATUS, Références GitHub | #3 restait présentée en brouillon dans Notion ; STATUS s’arrêtait à #2. Les dates et le main de référence sont actualisés | GitHub PR/branche relus ; sept pages relues après écriture |
| P1 | Preuves, Avancement et contrôle ; cadre commun des exercices ; Notion 00/08 | La validité d’une preuve lors d’un changement n’était pas assez explicite. Deux axes et règles de renouvellement ajoutés, sans renommer les champs de la base | Comparaison des paragraphes ; absence de mutation de la base |
| P1 | Contrat, §3 et §14 | Paramètres API, erreurs et valeurs par défaut incomplets ; conservation locale d’un ancien script affirmée sans contrôle. Référence issue du code ajoutée ; ancien script signalé absent et conservation hors dépôt non vérifiée | AST des routes, JSON fictifs analysés, source et schéma relus |
| P1 | Architecture, registre et origine des schémas ; Notion 01/10 | Raisons anciennes et décisions personnelles pouvaient être confondues ; les SVG pouvaient passer pour des exports par éditeur. Provenance et limites rendues explicites | Lecture du mandat, du générateur et des XML ; aucun schéma modifié |
| P1 | Reprise, triage court ; démarrage, état d’essai ; Notion 06 | Le lecteur en incident rencontrait surtout une recette historique non exécutable. Triage court, arrêt avant mutation et relais au propriétaire ajoutés | Relecture de la séquence ; procédure personnelle non exécutée |
| P2 | Provenance, maintenance et fiche de reprise ; Notion 07/08/10 | Rôles documentaires, termes et reprise dispersés. Liens, responsabilités, conduite face à un secret et fiche de reprise ajoutés | Liens/ancres et non-régression ; aucun incident de secret déclaré sans constat |

Les alternatives anciennes SPA/Flask ou SQLite/PostgreSQL sont qualifiées de comparaisons pédagogiques ; elles ne sont pas attribuées à une étude personnelle de Mathias. La raison détaillée du choix des distributions reste non documentée dans les sources de cette passe. Aucun ADR n’est rempli avec une justification inventée.

## Matrice des modules V5

| Module | Application et état |
|---|---|
| 00 | Appliqué : statuts sur deux axes, preuve versionnée, origine des déclarations, limites, intégrité et autorisations. Preuve personnelle toujours non préremplie |
| 01 | Appliqué : rôles et sources de vérité dans provenance, registre court dans architecture ; aucune arborescence Diátaxis imposée |
| 02 | Appliqué : attribution et état conservés dans README ; pas de nouveau badge, licence ou politique inventés |
| 03 | Appliqué au cadre commun : explication progressive de la preuve et questions de décision ; aucune solution InfraOps finale. Fiche d’appropriation autonome non créée, car non demandée et besoin déjà couvert par 01/02 |
| 04 | Appliqué à la référence API et aux précautions des commandes ; exemples explicitement fictifs. Exécution et validation de toutes les options des anciens guides : non vérifiées |
| 05 | Appliqué : état d’essai des procédures, conditions d’arrêt, point de non-retour, retour non essayé et triage court. Réception pratique : non vérifiée |
| 06 | Partiel : paires réelles conservées, origine séparée du SVG déclarée ; réouverture et véritable export par éditeur non vérifiés |
| 07 | Appliqué : audit préalable, couverture précise, écarts sourcés, intégrité et verdict par dimension ; pas d’audit de code global revendiqué |
| 08 | Partiel : seuils WCAG 2.2 distingués d’une conformité globale ; aucun changement graphique fondé sur une mesure isolée |
| 09 | Appliqué : termes fixes, langue française, avancement/contrôle et raisons inconnues explicites ; anciens contenus historiques conservés |
| 10 | Partiel : chemins de lecture et triage renforcés ; usage réel, clavier, mobile/sombre non vérifiés |
| 11 | Appliqué : audit ciblé, corrections ordinaires autorisées, fiche de reprise, contrôles et proposition de revue sans fusion |

Le logiciel et le parcours restent V4.4. V5 qualifie la charte documentaire. Aucun module n’est un prétexte pour fabriquer un fichier technique, une compétence ou une nouvelle politique. Le corpus source n’est pas modifié par cette intervention.

## Contrôles reproductibles et limites

Le dossier de revue livre `check_documentation.py`, l’inventaire de référence et les sorties JSON. Depuis le dossier où les artefacts ont été extraits, avec un checkout OpsDesk à la révision proposée, Python standard suffit :

```sh
python3 check_documentation.py --repo chemin/vers/OpsDesk --inventory github-source-tree.json
```

`chemin/vers/OpsDesk` est un chemin à adapter au checkout, pas une commande de clonage. Cette commande lit les Markdown, AST Python, XML et hashes, puis écrit son résultat JSON sur la sortie standard. Elle n’importe ni ne démarre l’application ; aucun service, privilège, installation, VM ou cloud nécessaire. Les commandes effectivement exécutées par Codex utilisent `work/v5/check_documentation.py`, `--repo work/OpsDesk` et `--inventory work/v5/github-source-tree.json` ; leurs sorties exactes sont dans le dossier de revue. Le script local de contrôle n’est pas ajouté aux scripts opérationnels du dépôt.

La première passe a relevé deux liens vers ce rapport encore absent ; sa création résout ces deux écarts. La passe de réception est rejouée après production du rapport. Les contrôles portent sur existence des destinations, ancres, fences, 30 rubriques conservées du contrat, deux objets JSON fictifs, routes API lues par AST, XML et frontière du diff. Une analyse syntaxique ne prouve pas que le service répond.

La comparaison des hashes du rapport applicatif ancien retrouve dix fichiers présents identiques et un chemin historique absent (`db/001-initial.sql`). Aucun fichier présent de ce périmètre ne diffère ; cela conserve l’attribution de la preuve ancienne, sans recevoir l’environnement ni relancer les 26 tests. Le scan historique reste FAIL, 185 occurrences dont 45 HIGH, sur l’image et la date de son rapport ; aucune nouvelle image personnelle n’est analysée.

| Contrôle | Résultat / limite |
|---|---|
| Corpus V5 accessible, hashes et modules dans compilation | PASS structurel, 15 sources et 12 modules retrouvés ; lecture comparative ciblée, pas seconde série d’exigences |
| Référence distante et intégrité avant correction | PASS : 84 textes identiques à main ; image binaire seulement recensée |
| Liens/ancres/fences et contrat | Résultat exact de la passe finale livré dans checks.json ; aucun PASS anticipé à la place d’une sortie |
| Non-régression opérationnelle | Diff limité aux Markdown ; fichiers applicatifs, scripts, dépendances, diagrammes, laboratoire et preuves techniques conservés |
| Sept pages Notion | Réponses d’écriture sans avertissement et relecture pour la réception ; pages/bases enfants conservées |
| Tests applicatifs, scans nouveaux, Terraform/Ansible/K3s, CI, restauration | NON EXÉCUTÉS pendant cette mission documentaire |
| Interfaces Notion/GitHub natives, mobile/sombre/clavier | NON VÉRIFIÉES ; texte des connecteurs et contrôles statiques seulement |
| Export Draw.io et réouverture | NON VÉRIFIÉS ; générateur analysé sans exécution ni conversion |
| Liens externes | PARTIEL : identités GitHub/Notion ciblées et références W3C consultées ; pas de contrôle exhaustif des anciens liens externes |

Les critères de contraste [1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) et [1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) ont été relus dans les explications officielles W3C : 4,5:1 pour le texte normal, 3:1 pour le grand texte et les parties graphiques nécessaires à la compréhension, sans arrondir le seuil. Le rapport précédent mesure des bordures pâles sous 3:1 ; leur nécessité pour comprendre le schéma doit être examinée avant de conclure à une non-conformité. Les textes et les flux ne reposent pas uniquement sur ces bordures. Cette passe n’établit aucune conformité WCAG globale et ne réécrit pas rétrospectivement le rapport précédent.

## Pages Notion mises à jour

- [Accueil](https://app.notion.com/p/3fc65721fa1881ad8325c8c4619c7223) : fusion #3 et portée V5.
- [00 — Parcours pédagogique](https://app.notion.com/p/3fc65721fa1881f7b4d2f248aafeed23) : règles communes de preuve et procédures.
- [01 — Architecture](https://app.notion.com/p/3fc65721fa18813488a5d4052fe90c76) : décisions personnelles et provenance des schémas.
- [06 — Runbook](https://app.notion.com/p/3fc65721fa1881f6ac84f48db75a0634) : triage avant modification et conditions d’arrêt.
- [07 — Sécurité](https://app.notion.com/p/3fc65721fa188145b029c7780c0768b9) : conduite face à un secret, sans inventer d’incident.
- [08 — Glossaire](https://app.notion.com/p/3fc65721fa18819cba26e66c4f6bd226) : vocabulaire fixe du suivi.
- [10 — Revue GitHub](https://app.notion.com/p/3fc65721fa1881099b7aec8afb260661) : critères V5, référence API et reprise.

Les modifications ciblent des paragraphes ou insèrent une section dans les pages existantes ; aucun remplacement global, suppression d’archive, nouvelle page mère ou nouvelle base. Les snapshots et opérations exactes sont livrés pour revue et retour différentiel éventuel, après comparaison de l’état courant afin de préserver les modifications ultérieures de Mathias.

## Fichiers modifiés et prochaine action

`README.md`, `STATUS.md`, `docs/apprentissage/README.md`, `docs/architecture.md`, `docs/contrat-applicatif.md`, `docs/demarrage.md`, `docs/preuves.md`, `docs/provenance.md`, `docs/reprise.md` et ce rapport. Les annexes de validation et le script documentaire restent dans le dossier de revue, hors fichiers opérationnels du dépôt.

Pour la reprise personnelle : ouvrir l’exercice 01 et le contrat, reformuler fonctions et limites, tracer les flux et poser ses questions sans VM ni installation. Pour la revue documentaire : examiner la nouvelle PR en brouillon et les réserves ; aucune fusion ni publication publique automatique. Le lien de la PR et le commit final sont ajoutés à la fiche de livraison et à l’accueil Notion après leur création réelle.
