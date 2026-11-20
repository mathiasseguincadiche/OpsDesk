"""Schémas d'OpsDesk, construits avec le système graphique de la collection V24.

Usage, depuis la racine du dépôt :
    python docs/diagrams/outils/generer_schemas.py docs/diagrams
puis exporter chaque source en SVG avec Draw.io (commande dans docs/diagrams/README.md).

Les faits représentés viennent du dépôt : compose.yaml, frontend/nginx.conf.template,
backend/app, docs/architecture.md (registre des décisions), docs/apprentissage/.
Les vues pédagogiques sont conçues pour 760 px (fiches Notion d'environ 700 px).
"""
import sys
from pathlib import Path

from systeme_graphique import (
    ACCES, AUTOMATISATION, CANVAS, CARD, DONNEES, FAMILLES, FLUX, HEADER, INFRA, INK, MUTED, NEUTRE,
    NOMS_ICONES, OBSERVABILITE, RESILIENCE, RULE, SECURITE, SLATE, TRAITEMENT, ZONE, Diagramme,
    bibliotheque, composant, icone_style, legende, machine, pastille, police, statut, style_canevas,
    style_carte, style_cylindre, style_document, style_flux, style_losange, style_machine,
    style_regroupement, style_texte, style_zone, titre,
)

MONO = "font-family:Courier New,monospace;font-size:12px"


def html_code(lignes):
    return "<br>".join(f'<span style="{MONO};color:{INK}">{l}</span>' for l in lignes)


# --------------------------------------------------------------------------- #
# 1. Présentation : infographie éditoriale                                     #
# --------------------------------------------------------------------------- #

def presentation(dossier):
    d = Diagramme("presentation", 1000, 640)
    d.forme("canevas", 0, 0, 1000, 640, "", style_canevas(), calque="fond")
    titre(d, "OpsDesk", "Une application de tickets de support informatique, et le projet DevOps qui la rend exploitable")

    # Acteurs (source : schemas.py, rôles user / agent / admin)
    acteurs = [("collaborateur", "utilisateur", "Collaborateur", "signale un incident, suit sa demande"),
               ("support", "utilisateur", "Support", "prend en charge, résout, commente"),
               ("administrateur", "administrateur", "Administrateur", "gère les comptes et les rôles")]
    d.forme("acteurs-titre", 32, 96, 220, 20, "QUI L'UTILISE", style_texte("categorie", MUTED), calque="annotations")
    for i, (ident, ic, nom, det) in enumerate(acteurs):
        composant(d, ident, 32, 124 + i * 72, 232, 60, ACCES, ic, "", nom, det)

    # Point focal : l'application
    app = d.forme("application", 328, 104, 344, 236, "", f"rounded=1;arcSize=14;absoluteArcSize=1;fillColor={CARD};"
                  f"strokeColor={ACCES.trait};strokeWidth=2.25;shadow=0;", calque="composants")
    d.forme("application-icone", 24, 22, 36, 36, "", icone_style("navigateur", ACCES.trait), app)
    d.forme("application-nom", 72, 18, 250, 44,
            f'<span style="font-size:24px;font-weight:bold;color:{INK}">OpsDesk</span><br>'
            f'<span style="font-size:12px;color:{MUTED}">version 2 · interface web et API</span>',
            style_texte("detail", INK), app)
    d.forme("application-fonctions", 24, 76, 296, 40,
            "Créer et suivre des tickets, les commenter, garder l'historique de chaque changement, "
            "et voir l'activité sur un tableau de bord.", style_texte("detail", INK, valign="top"), app)
    # Cycle de vie (source : workflow.py)
    etats = ["Ouvert", "En cours", "Résolu", "Clôturé"]
    for i, e in enumerate(etats):
        pid = pastille(d, f"etat-{i}", 24 + i * 76, 136, 64, e, ACCES, plein=(i == 0), parent=app)
        if i:
            d.lien(f"etat-lien-{i}", f"etat-{i - 1}", pid, "", style_flux("applicatif", ortho=False) +
                   "strokeWidth=1.25;endSize=4;", calque="annotations")
    d.forme("application-cycle", 24, 166, 296, 18, "le cycle de vie d'un ticket, vérifié par l'API",
            style_texte("note", MUTED), app)
    statut(d, "application-statut", 24, 196, 232, ("verifie", "Réalisée · vérifiée en local"), parent=app)

    # Ce qu'elle garantit (source : deps.py, db, observability.py)
    d.forme("garanties-titre", 736, 96, 232, 20, "CE QU'ELLE GARANTIT", style_texte("categorie", MUTED), calque="annotations")
    composant(d, "garantie-acces", 736, 124, 232, 60, SECURITE, "cadenas", "", "Accès par rôle", "jeton signé, droits vérifiés")
    composant(d, "garantie-donnees", 736, 196, 232, 60, DONNEES, "base", "", "Données conservées", "PostgreSQL, sur un volume")
    composant(d, "garantie-signaux", 736, 268, 232, 60, OBSERVABILITE, "mesures", "", "Signaux d'exploitation", "sondes, métriques, journaux")
    # Flèches droites : chaque ancrage est calculé à la hauteur du centre de la carte reliée.
    for i, a in enumerate(["collaborateur", "support", "administrateur"]):
        ey = (124 + i * 72 + 30 - 104) / 236
        d.lien(f"usage-{i}", a, app, "", style_flux("applicatif", ortho=False) + f"exitX=1;exitY=0.5;entryX=0;entryY={ey:.4f};")
    for i, g in enumerate(["garantie-acces", "garantie-donnees", "garantie-signaux"]):
        ey = (124 + i * 72 + 30 - 104) / 236
        d.lien(f"garantie-{i}", app, g, "", style_flux("applicatif", ortho=False) + f"exitX=1;exitY={ey:.4f};entryX=0;entryY=0.5;"
               + "endArrow=oval;endFill=1;endSize=6;")

    # Ligne de temps du projet (source : ROADMAP.md, STATUS.md)
    d.forme("projet", 24, 368, 952, 248, "LE PROJET DEVOPS : RENDRE CE SERVICE EXPLOITABLE", style_regroupement(), calque="frontieres")
    y = 432
    d.trait_libre("ligne-temps", 72, y, 920, y, f"endArrow=block;endFill=1;strokeColor={RULE};strokeWidth=3;")
    jalons = [("depart", "Point de départ", "application et conteneurs testés en local", ["FastAPI", "React", "PostgreSQL"], True),
              ("phase1", "1 · Préparer et automatiser", "serveurs créés et configurés par du code", ["Terraform", "Ansible", "Docker Compose"], False),
              ("phase2", "2 · Livrer et conserver", "chaîne de livraison, sauvegarde testée", ["GitHub Actions", "Trivy", "pg_dump"], False),
              ("phase3", "3 · Orchestrer et observer", "copie d'essai, supervision, charge", ["K3s", "Prometheus", "Grafana"], False)]
    for i, (ident, nom, det, outils, fait) in enumerate(jalons):
        x = 72 + i * 228
        d.forme(f"{ident}-point", x - 9, y - 9, 18, 18, "", f"ellipse;fillColor={ACCES.trait if fait else CARD};"
                f"strokeColor={ACCES.trait if fait else SLATE};strokeWidth=2;", calque="composants")
        d.forme(f"{ident}-nom", x - 12, y + 18, 210, 20, nom, style_texte("composant", INK), calque="composants")
        d.forme(f"{ident}-detail", x - 12, y + 40, 210, 18, det, style_texte("detail", MUTED), calque="composants")
        cx, cy = x - 12, y + 66
        for j, o in enumerate(outils):
            w = 20 + int(len(o) * 6.8)
            if cx + w > x - 12 + 212:          # retour à la ligne : jamais de débordement sur la colonne voisine
                cx, cy = x - 12, cy + 30
            pastille(d, f"{ident}-outil-{j}", cx, cy, w, o, NEUTRE)
            cx += w + 6
        statut(d, f"{ident}-statut", x - 12, y + 136, 168 if fait else 96,
               ("verifie", "Réalisé · vérifié") if fait else ("prevu", "Prévu"))
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# 1 bis. Présentation à 760 px : la même infographie, pour une page Notion     #
# --------------------------------------------------------------------------- #

def presentation_notion(dossier):
    """Même contenu que la présentation, recomposé à 760 px : affichée dans environ 700 px, aucun texte sous 11 px."""
    W, H = 760, 688
    d = Diagramme("presentation-notion", W, H)
    d.forme("canevas", 0, 0, W, H, "", style_canevas(), calque="fond")
    titre(d, "OpsDesk", "Une application de tickets de support informatique, et le projet DevOps qui la rend exploitable",
          l=W - 64)

    COL, APP_X, APP_L = 184, 232, 296          # 24 + 184 + 24 + 296 + 24 + 184 + 24 = 760
    DROITE = APP_X + APP_L + 24
    d.forme("acteurs-titre", 24, 100, COL, 20, "QUI L'UTILISE", style_texte("categorie", MUTED), calque="annotations")
    for i, (ident, ic, nom, det) in enumerate([("collaborateur", "utilisateur", "Collaborateur", "signale, suit sa demande"),
                                                ("support", "utilisateur", "Support", "prend en charge, résout"),
                                                ("administrateur", "administrateur", "Administrateur", "gère comptes et rôles")]):
        composant(d, ident, 24, 128 + i * 72, COL, 60, ACCES, ic, "", nom, det)

    app = d.forme("application", APP_X, 108, APP_L, 236, "", f"rounded=1;arcSize=14;absoluteArcSize=1;fillColor={CARD};"
                  f"strokeColor={ACCES.trait};strokeWidth=2.25;shadow=0;", calque="composants")
    d.forme("application-icone", 16, 20, 32, 32, "", icone_style("navigateur", ACCES.trait), app)
    d.forme("application-nom", 60, 16, 224, 40, f'<span style="font-size:22px;font-weight:bold;color:{INK}">OpsDesk</span><br>'
            f'<span style="font-size:12px;color:{MUTED}">version 2 · interface web et API</span>', style_texte("detail", INK), app)
    d.forme("application-fonctions", 16, 68, 264, 52, "Créer et suivre des tickets, les commenter, garder l'historique "
            "de chaque changement, voir l'activité sur un tableau de bord.", style_texte("detail", INK, valign="top"), app)
    for i, e in enumerate(["Ouvert", "En cours", "Résolu", "Clôturé"]):
        pid = pastille(d, f"etat-{i}", 16 + i * 68, 132, 58, e, ACCES, plein=(i == 0), parent=app)
        if i:
            d.lien(f"etat-lien-{i}", f"etat-{i - 1}", pid, "", style_flux("applicatif", ortho=False) + "strokeWidth=1.25;endSize=4;",
                   calque="annotations")
    d.forme("application-cycle", 16, 162, 264, 18, "le cycle de vie d'un ticket, vérifié par l'API", style_texte("note", MUTED), app)
    statut(d, "application-statut", 16, 196, 232, ("verifie", "Réalisée · vérifiée en local"), parent=app)

    d.forme("garanties-titre", DROITE, 100, COL, 20, "CE QU'ELLE GARANTIT", style_texte("categorie", MUTED), calque="annotations")
    for i, (ident, f, ic, nom, det) in enumerate([("garantie-acces", SECURITE, "cadenas", "Accès par rôle", "jeton signé, droits"),
                                                   ("garantie-donnees", DONNEES, "base", "Données conservées", "PostgreSQL, volume"),
                                                   ("garantie-signaux", OBSERVABILITE, "mesures", "Signaux", "sondes, métriques")]):
        composant(d, ident, DROITE, 128 + i * 72, COL, 60, f, ic, "", nom, det)
    for i, a in enumerate(["collaborateur", "support", "administrateur"]):
        ey = (128 + i * 72 + 30 - 108) / 236
        d.lien(f"usage-{i}", a, app, "", style_flux("applicatif", ortho=False) + f"exitX=1;exitY=0.5;entryX=0;entryY={ey:.4f};")
    for i, g in enumerate(["garantie-acces", "garantie-donnees", "garantie-signaux"]):
        ey = (128 + i * 72 + 30 - 108) / 236
        d.lien(f"garantie-{i}", app, g, "", style_flux("applicatif", ortho=False) + f"exitX=1;exitY={ey:.4f};entryX=0;entryY=0.5;"
               + "endArrow=oval;endFill=1;endSize=6;")

    # Ligne de temps : quatre colonnes de 172 px ; noms et détails peuvent passer sur deux lignes.
    d.forme("projet", 24, 376, 712, 288, "LE PROJET DEVOPS : RENDRE CE SERVICE EXPLOITABLE", style_regroupement(), calque="frontieres")
    y, x0, pas = 440, 64, 172
    d.trait_libre("ligne-temps", x0, y, 712, y, f"endArrow=block;endFill=1;strokeColor={RULE};strokeWidth=3;")
    jalons = [("depart", "Point de départ", "application et conteneurs testés en local", ["FastAPI", "React", "PostgreSQL"], True),
              ("phase1", "1 · Préparer et automatiser", "serveurs créés et configurés par du code", ["Terraform", "Ansible", "Docker Compose"], False),
              ("phase2", "2 · Livrer et conserver", "chaîne de livraison, sauvegarde testée", ["GitHub Actions", "Trivy", "pg_dump"], False),
              ("phase3", "3 · Orchestrer et observer", "copie d'essai, supervision, charge", ["K3s", "Prometheus", "Grafana"], False)]
    for i, (ident, nom, det, outils, fait) in enumerate(jalons):
        x = x0 + i * pas
        cx0, larg = x - 12, pas - 16
        d.forme(f"{ident}-point", x - 9, y - 9, 18, 18, "", f"ellipse;fillColor={ACCES.trait if fait else CARD};"
                f"strokeColor={ACCES.trait if fait else SLATE};strokeWidth=2;", calque="composants")
        d.forme(f"{ident}-nom", cx0, y + 16, larg, 36, nom, style_texte("composant", INK, valign="top"), calque="composants")
        d.forme(f"{ident}-detail", cx0, y + 56, larg, 34, det, style_texte("detail", MUTED, valign="top"), calque="composants")
        cx, cy = cx0, y + 98
        for j, o in enumerate(outils):
            w = 20 + int(len(o) * 6.8)
            if cx + w > cx0 + larg:
                cx, cy = cx0, cy + 30
            pastille(d, f"{ident}-outil-{j}", cx, cy, w, o, NEUTRE)
            cx += w + 6
        statut(d, f"{ident}-statut", cx0, y + 168, 150 if fait else 96,
               ("verifie", "Réalisé · vérifié") if fait else ("prevu", "Prévu"))
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# 2. Architecture : vue de déploiement par zones                               #
# --------------------------------------------------------------------------- #

def architecture(dossier):
    W, H = 1200, 940
    d = Diagramme("architecture", W, H)
    d.forme("canevas", 0, 0, W, H, "", style_canevas(), calque="fond")
    titre(d, "Architecture de déploiement cible",
          "Où s'exécute chaque composant d'OpsDesk, et par quels flux ils communiquent. Sources : registre des décisions, compose.yaml, nginx.conf.template.")
    statut(d, "etat-cible", W - 32 - 392, 28, 392, ("prevu", "Infrastructure prévue · aucune machine n'est encore créée"))

    d.forme("a-retenir", 32, 100, 780, 64,
            "<b>À retenir.</b> Un seul point d'entrée pour les utilisateurs : nginx, port 8080. L'API et la base restent internes. "
            "Tout se pilote depuis srv-admin ; Prometheus lit les mesures depuis srv-k3s ; les sauvegardes quittent la VM.",
            style_texte("note", INK, valign="top"), calque="annotations")

    # Internet : GitHub (source : registre, décision « Livraison »)
    gh = d.forme("internet", 840, 92, 336, 88, "INTERNET", style_zone(prevu=True, teinte=CARD), calque="frontieres")
    composant(d, "ghcr", 864, 124, 288, 44, AUTOMATISATION, "depot", "", "GitHub · Actions et GHCR", "images publiées par la CI", prevu=True)

    # Hôte (source : guide du laboratoire)
    d.forme("hote", 24, 196, 1152, 664, "HÔTE FEDORA 45 · KVM / LIBVIRT", style_zone(prevu=True), calque="frontieres")
    composant(d, "navigateur", 40, 608, 160, 60, ACCES, "navigateur", "accès", "Navigateur", "poste hôte")
    composant(d, "sauvegardes", 40, 716, 160, 60, RESILIENCE, "sauvegarde", "hors VM", "~/sauvegardes", "copies datées", prevu=True)
    composant(d, "libvirt", 40, 268, 160, 60, INFRA, "serveur", "hyperviseur", "libvirt", "crée les VM", prevu=True)

    # Réseau (source : registre, décision « Réseau, accès et protections »)
    d.forme("reseau", 256, 236, 896, 600, "RÉSEAU NAT opsdesk-lan · 192.168.150.0/24 · SELinux Enforcing et firewalld sur chaque VM",
            style_zone(prevu=True, teinte="#E4EAF3"), calque="frontieres")

    # srv-admin
    adm = machine(d, "srv-admin", 280, 276, 360, 176, "srv-admin", "192.168.150.5 · pilotage", prevu=True)
    for i, (ident, ic, nom, det) in enumerate([("terraform", "fichier", "Terraform", "crée les VM"),
                                                ("ansible", "liste", "Ansible", "configure, déploie"),
                                                ("git", "depot", "Git", "code et playbooks"),
                                                ("k6", "mesures", "k6", "charge, copie seule")]):
        composant(d, ident, 16 + (i % 2) * 168, 52 + (i // 2) * 60, 160, 52, AUTOMATISATION, ic, "", nom, det,
                  prevu=True, parent=adm)

    # srv-k3s
    k3s = machine(d, "srv-k3s", 768, 276, 360, 176, "srv-k3s", "192.168.150.20 · K3s, un nœud", icone="grappe", prevu=True)
    for i, (ident, f, ic, nom, det) in enumerate([("copie", TRAITEMENT, "conteneur", "Copie d'essai", "mêmes images, base de test"),
                                                   ("traefik", ACCES, "reseau", "Traefik", "Ingress, port 80"),
                                                   ("grafana", OBSERVABILITE, "alerte", "Grafana", "tableaux de bord"),
                                                   ("prometheus", OBSERVABILITE, "mesures", "Prometheus", "15 s, 15 jours, 2 alertes")]):
        composant(d, ident, 16 + (i % 2) * 168, 52 + (i // 2) * 60, 160, 52, f, ic, "", nom, det, prevu=True, parent=k3s)

    # srv-app (source : compose.yaml, Dockerfiles, registre « Exécution » et « Administration de Docker par sudo »)
    app = machine(d, "srv-app", 280, 488, 848, 324, "srv-app",
                  "192.168.150.10 · 2 vCPU, 4 Go, disque de données 10 Go", prevu=True)
    run = d.forme("docker", 16, 48, 624, 260, "DOCKER ENGINE + COMPOSE · /opt/opsdesk",
                  style_zone(prevu=True, teinte="#F7F9FC"), parent=app, calque="frontieres")
    composant(d, "web", 24, 64, 176, 76, ACCES, "navigateur", "frontend", "nginx", "interface React<br>port 8080", parent=run)
    composant(d, "api", 236, 64, 176, 76, TRAITEMENT, "api", "backend", "FastAPI", "jeton, rôles<br>port 8000", parent=run)
    d.forme("db", 448, 52, 152, 100,
            f'<span style="font-size:11px;font-weight:bold;letter-spacing:0.6px;color:{DONNEES.texte}">DB</span><br>'
            f'<span style="font-size:14px;font-weight:bold">PostgreSQL 17</span><br>'
            f'<span style="font-size:12px;color:{MUTED}">port 5432, non publié</span>', style_cylindre(DONNEES), parent=run)
    composant(d, "volume", 448, 184, 152, 52, DONNEES, "volume", "", "Volume", "données de la base", parent=run)
    composant(d, "pg-dump", 24, 184, 176, 52, RESILIENCE, "horloge", "", "pg_dump", "minuteur 02:00 · 7 copies", prevu=True, parent=run)
    composant(d, "secrets", 236, 184, 176, 52, SECURITE, "cle", "", "Secrets en fichiers", "base, JWT, admin", prevu=True, parent=run)
    composant(d, "node-app", 664, 64, 168, 52, OBSERVABILITE, "mesures", "", "node_exporter", "système, port 9100", prevu=True, parent=app)
    d.forme("note-app", 664, 136, 168, 156,
            "Conteneurs sans root, relancés par Docker ; systemd démarre le démon. Aucun membre du groupe docker. Seul le port 8080 sert aux utilisateurs ; "
            "le port 8000 ne l'est qu'à srv-k3s, pour /metrics ; la base n'est jamais publiée.", style_texte("note", MUTED, valign="top"), parent=app, calque="annotations")

    # Flux applicatifs : testés en conteneurs locaux (source : compose.yaml, smoke.py)
    d.lien("flux-http", "navigateur", "web", "HTTP :8080", style_flux("applicatif", fort=True) +
           "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("flux-api", "web", "api", "/api", style_flux("applicatif", fort=True) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("flux-sql", "api", "db", "SQL", style_flux("applicatif", fort=True) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("flux-volume", "db", "volume", "", f"edgeStyle=none;endArrow=none;strokeColor={DONNEES.trait};strokeWidth=1.5;"
           "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")

    # Administration (prévue)
    d.lien("flux-ssh-app", "srv-admin", "srv-app", "SSH :22", style_flux("administration", prevu=True) +
           "exitX=0.5;exitY=1;entryX=0.2125;entryY=0;")
    d.lien("flux-ssh-k3s", "srv-admin", "srv-k3s", "SSH :22", style_flux("administration", prevu=True) +
           "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("flux-libvirt", "terraform", "libvirt", "qemu+ssh", style_flux("administration", prevu=True) +
           "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    d.lien("flux-images", "ghcr", "srv-k3s", "images HTTPS", style_flux("administration", prevu=True) +
           "exitX=0.5;exitY=1;entryX=0.75;entryY=0;")
    d.lien("flux-images-app", "ghcr", "srv-app", "", style_flux("administration", prevu=True) +
           "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(1164, 146), (1164, 650)])
    # Observabilité (prévue)
    # Prometheus (x 952-1112, y 388-440) ; api (x 532-708, haut y 600) ; node_exporter (x 944-1112, haut y 552)
    d.lien("flux-metrics", "prometheus", "api", "/metrics :8000", style_flux("observabilite", prevu=True) +
           "exitX=0.25;exitY=1;entryX=0.75;entryY=0;", points=[(992, 470), (760, 470), (760, 572), (664, 572)])
    d.lien("flux-node", "prometheus", "node-app", ":9100", style_flux("observabilite", prevu=True) +
           "exitX=0.8;exitY=1;entryX=0.8;entryY=0;")
    # Sauvegarde (prévue)
    # pg_dump (x 320-496, y 720-772) lit la base (x 744-896, y 588-688) en passant entre les deux rangées
    d.lien("flux-dump", "pg-dump", "db", "lit la base", style_flux("sauvegarde", prevu=True) +
           "exitX=0.5;exitY=0;entryX=0.2;entryY=1;", points=[(408, 702), (774, 702)])
    d.lien("flux-rsync", "pg-dump", "sauvegardes", "rsync · SSH", style_flux("sauvegarde", prevu=True) +
           "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")

    legende(d, 24, 876, [
        ("trait", "applicatif", False, "Applicatif · testé en conteneurs locaux"),
        ("trait", "administration", True, "Administration, déploiement"),
        ("trait", "observabilite", True, "Observabilité"),
        ("trait", "sauvegarde", True, "Sauvegarde"),
        ("forme", style_zone(prevu=True), "Pointillés : prévu"),
    ], l=1152)
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# 3. Pédagogique : le mécanisme d'Ansible                                      #
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# 7. Présentation pour téléphone : lecture verticale (~375 px)                 #
# --------------------------------------------------------------------------- #

def presentation_mobile(dossier):
    """Même contenu que la présentation, recomposé en une colonne : rien n'est réduit, tout est empilé."""
    W, H = 400, 1272          # hauteur = somme des blocs empilés (voir les y ci-dessous)
    d = Diagramme("presentation-mobile", W, H)
    d.forme("canevas", 0, 0, W, H, "", style_canevas(), calque="fond")
    d.forme("titre", 24, 24, 352, 30, "OpsDesk", style_texte("titre", INK), calque="annotations")
    d.forme("sous-titre", 24, 56, 352, 40, "Une application de tickets de support informatique, et le projet DevOps qui la rend exploitable.",
            style_texte("sous_titre", MUTED, valign="top"), calque="annotations")

    app = d.forme("application", 24, 112, 352, 216, "", f"rounded=1;arcSize=14;absoluteArcSize=1;fillColor={CARD};"
                  f"strokeColor={ACCES.trait};strokeWidth=2.25;", calque="composants")
    d.forme("application-icone", 20, 20, 32, 32, "", icone_style("navigateur", ACCES.trait), app)
    d.forme("application-nom", 64, 16, 272, 40, f'<span style="font-size:22px;font-weight:bold">OpsDesk</span><br>'
            f'<span style="font-size:12px;color:{MUTED}">version 2 · interface web et API</span>', style_texte("detail", INK), app)
    d.forme("application-fonctions", 20, 68, 312, 54, "Créer et suivre des tickets, les commenter, garder l'historique "
            "de chaque changement, voir l'activité sur un tableau de bord.", style_texte("detail", INK, valign="top"), app)
    for i, e in enumerate(["Ouvert", "En cours", "Résolu", "Clôturé"]):
        pid = pastille(d, f"etat-{i}", 20 + i * 80, 132, 68, e, ACCES, plein=(i == 0), parent=app)
        if i:
            d.lien(f"etat-lien-{i}", f"etat-{i - 1}", pid, "", style_flux("applicatif", ortho=False) + "strokeWidth=1.25;endSize=4;",
                   calque="annotations")
    statut(d, "application-statut", 20, 176, 232, ("verifie", "Réalisée · vérifiée en local"), parent=app)

    y = 352
    d.forme("acteurs-titre", 24, y, 352, 20, "QUI L'UTILISE", style_texte("categorie", MUTED), calque="annotations")
    for i, (ident, ic, nom, det) in enumerate([("collaborateur", "utilisateur", "Collaborateur", "signale, suit sa demande"),
                                                ("support", "utilisateur", "Support", "prend en charge, résout"),
                                                ("administrateur", "administrateur", "Administrateur", "gère les comptes")]):
        composant(d, ident, 24, y + 28 + i * 64, 352, 56, ACCES, ic, "", nom, det)
    y += 28 + 3 * 64 + 16
    d.forme("garanties-titre", 24, y, 352, 20, "CE QU'ELLE GARANTIT", style_texte("categorie", MUTED), calque="annotations")
    for i, (ident, f, ic, nom, det) in enumerate([("acces", SECURITE, "cadenas", "Accès par rôle", "jeton signé, droits vérifiés"),
                                                   ("donnees", DONNEES, "base", "Données conservées", "PostgreSQL, sur un volume"),
                                                   ("signaux", OBSERVABILITE, "mesures", "Signaux d'exploitation", "sondes, métriques, journaux")]):
        composant(d, ident, 24, y + 28 + i * 64, 352, 56, f, ic, "", nom, det)
    y += 28 + 3 * 64 + 16

    d.forme("projet", 24, y, 352, H - 24 - y, "LE PROJET DEVOPS", style_regroupement(), calque="frontieres")
    jalons = [("Point de départ", "application et conteneurs testés en local", "FastAPI · React · PostgreSQL", True),
              ("1 · Préparer et automatiser", "serveurs créés et configurés par du code", "Terraform · Ansible · Docker Compose", False),
              ("2 · Livrer et conserver", "chaîne de livraison, sauvegarde testée", "GitHub Actions · Trivy · pg_dump", False),
              ("3 · Orchestrer et observer", "copie d'essai, supervision, charge", "K3s · Prometheus · Grafana", False)]
    ligne_x, y0, pas = 56, y + 56, 96
    d.trait_libre("ligne-temps", ligne_x, y0, ligne_x, y0 + pas * 3 + 24, f"endArrow=block;endFill=1;strokeColor={RULE};strokeWidth=3;")
    for i, (nom, det, outils, fait) in enumerate(jalons):
        yy = y0 + i * pas
        d.forme(f"jalon-{i}-point", ligne_x - 9, yy - 9, 18, 18, "", f"ellipse;fillColor={ACCES.trait if fait else CARD};"
                f"strokeColor={ACCES.trait if fait else SLATE};strokeWidth=2;", calque="composants")
        d.forme(f"jalon-{i}-texte", ligne_x + 24, yy - 12, 276, 52,
                f'<span style="font-size:14px;font-weight:bold">{nom}</span><br><span style="font-size:12px;color:{MUTED}">{det}</span>'
                f'<br><span style="font-size:12px;color:{INK}">{outils}</span>', style_texte("detail", INK, valign="top"), calque="composants")
        statut(d, f"jalon-{i}-statut", ligne_x + 24, yy + 46, 132 if fait else 84,
               ("verifie", "Réalisé · vérifié") if fait else ("prevu", "Prévu"))
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Catalogue visuel et bibliothèque Draw.io                                     #
# --------------------------------------------------------------------------- #



# =========================================================================== #
# Vues conçues pour 760 px : fiches Notion (~700 px) et README                 #
# =========================================================================== #

L760 = 760


def _fond(nom, h, titre_txt, sous_titre, badge=None):
    d = Diagramme(nom, L760, h)
    d.forme("canevas", 0, 0, L760, h, "", style_canevas(), calque="fond")
    titre(d, titre_txt, sous_titre, l=L760 - 64 - (232 if badge else 0))
    if badge:
        statut(d, "statut-schema", L760 - 24 - 220, 28, 220, badge)
    return d


def carte_simple(d, ident, x, y, l, h, f, html, parent=None, fond=None, centre=False):
    """Carte sans icône : texte libre, aligné à gauche ou centré."""
    style = style_carte(f, fond=fond).replace("spacingLeft=46", "spacingLeft=12")
    if centre:
        style += "align=center;spacingLeft=8;spacingRight=8;"
    return d.forme(ident, x, y, l, h, html, style, parent)


def b(t, taille=14, couleur=INK):
    return f'<span style="font-size:{taille}px;font-weight:bold;color:{couleur}">{t}</span>'


def s(t, couleur=MUTED, taille=12):
    return f'<span style="font-size:{taille}px;color:{couleur}">{t}</span>'


def code(t, couleur=INK):
    return f'<span style="{MONO};color:{couleur}">{t}</span>'


# --------------------------------------------------------------------------- #
# Architecture, vue globale (760 px)                                           #
# --------------------------------------------------------------------------- #

def architecture_globale(dossier):
    """Vue d'ensemble : trois machines, l'environnement d'exécution, les quatre flux principaux.

    Sources : registre des décisions (machines, réseau, ports), compose.yaml (conteneurs), architecture.drawio (vue détaillée).
    """
    d = _fond("architecture-globale", 660, "Architecture d'OpsDesk : vue d'ensemble",
              "Trois machines sur un réseau privé ; un seul point d'entrée pour les utilisateurs.",
              ("prevu", "Infrastructure prévue"))
    d.forme("hote", 16, 100, 728, 476, "HÔTE FEDORA · KVM", style_zone(prevu=True), calque="frontieres")
    composant(d, "navigateur", 28, 258, 124, 56, ACCES, "navigateur", "", "Navigateur", "poste hôte")
    composant(d, "sauvegardes", 28, 422, 124, 56, RESILIENCE, "sauvegarde", "", "Copies", "hors VM", prevu=True)
    d.forme("reseau", 176, 138, 556, 426, "RÉSEAU opsdesk-lan", style_zone(prevu=True, teinte="#E4EAF3"), calque="frontieres")

    app = machine(d, "srv-app", 192, 176, 292, 372, "srv-app", "le service", prevu=True)
    d.forme("docker", 12, 46, 268, 270, "DOCKER ENGINE + COMPOSE", style_zone(prevu=True, teinte="#F7F9FC"), parent=app, calque="frontieres")
    composant(d, "web", 12, 38, 244, 52, ACCES, "navigateur", "", "nginx", "interface · port 8080", parent="docker")
    composant(d, "api", 12, 122, 244, 52, TRAITEMENT, "api", "", "API FastAPI", "jeton, rôles · port 8000", parent="docker")
    d.forme("db", 12, 196, 244, 64, f'{b("PostgreSQL 17")}<br>{s("port 5432, non publié")}', style_cylindre(DONNEES), parent="docker")
    d.forme("note-app", 12, 322, 268, 40, "Conteneurs sans root ; administration par sudo.", style_texte("note", MUTED, valign="top"),
            parent=app, calque="annotations")
    d.lien("flux-api", "web", "api", "/api", style_flux("applicatif", fort=True, ortho=False) + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.lien("flux-sql", "api", "db", "SQL", style_flux("applicatif", fort=True, ortho=False) + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")

    adm = machine(d, "srv-admin", 524, 176, 196, 132, "srv-admin", "pilote", prevu=True)
    for ident, x, y, l in (("Terraform", 12, 48, 92), ("Ansible", 110, 48, 74), ("Git", 12, 80, 52)):
        pastille(d, f"admin-{ident}", x, y, l, ident, AUTOMATISATION, parent=adm)
    k3s = machine(d, "srv-k3s", 524, 340, 196, 168, "srv-k3s", "supervision", icone="grappe", prevu=True)
    pastille(d, "k3s-copie", 12, 56, 112, "Copie d'essai", TRAITEMENT, parent=k3s)
    pastille(d, "k3s-prom", 12, 88, 104, "Prometheus", OBSERVABILITE, parent=k3s)
    pastille(d, "k3s-graf", 12, 120, 80, "Grafana", OBSERVABILITE, parent=k3s)

    # Ancrages : web y 270-322 (centre 296) ; api y 354-406 (380) ; db y 428-492 (460) ; srv-app y 176-548.
    d.lien("flux-http", "navigateur", "web", "HTTP :8080", style_flux("applicatif", fort=True, ortho=False) +
           "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", decalage=(0, -12))
    d.lien("flux-ssh", "srv-admin", "srv-app", "SSH", style_flux("administration", prevu=True, ortho=False) +
           f"exitX=0;exitY=0.5;entryX=1;entryY={(242 - 176) / 372:.4f};", decalage=(0, -12))
    d.lien("flux-metrics", "srv-k3s", "api", "/metrics", style_flux("observabilite", prevu=True, ortho=False) +
           f"exitX=0;exitY={(370 - 340) / 168:.4f};entryX=1;entryY=0.5;", decalage=(0, -12))
    d.lien("flux-backup", "db", "sauvegardes", "pg_dump", style_flux("sauvegarde", prevu=True, ortho=False) +
           "exitX=0;exitY=0.5;entryX=1;entryY=0.5;", decalage=(0, -12))
    legende(d, 16, 592, [("trait", "applicatif", False, "Applicatif · testé en local"),
                         ("trait", "administration", True, "Administration"),
                         ("trait", "observabilite", True, "Observabilité"),
                         ("trait", "sauvegarde", True, "Sauvegarde")], l=728)
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Ansible (exercice 05), 760 px                                                #
# --------------------------------------------------------------------------- #

def pedagogique_ansible(dossier):
    d = _fond("pedagogique-ansible", 720, "Comment Ansible rend un serveur conforme",
              "Il compare l'état voulu à l'état observé et ne change que ce qui manque.",
              ("principe", "Schéma de principe"))
    adm = machine(d, "srv-admin", 24, 96, 260, 328, "srv-admin", "pilotage")
    d.forme("etape-1", 12, 46, 236, 20, "① L'ÉTAT VOULU", style_texte("categorie", AUTOMATISATION.texte), adm)
    d.forme("inventaire", 12, 72, 236, 76, f'{b("inventory.ini", 12)} {s("· où agir")}<br>' +
            html_code(["[app]", "srv-app ansible_host=…10"]), style_document(AUTOMATISATION), adm)
    d.forme("playbook", 12, 160, 236, 152, f'{b("playbook.yml", 12)} {s("· quoi obtenir")}<br>' +
            html_code(["- docker-ce : present", "- docker : actif", "- 8080/tcp : ouvert"]) +
            f'<br><br>{s("Un résultat à obtenir,<br>pas une suite de commandes.")}', style_document(AUTOMATISATION), adm)

    app = machine(d, "srv-app", 340, 96, 396, 328, "srv-app", "Python exécute chaque tâche")
    d.forme("etape-2", 12, 46, 372, 20, "② POUR CHAQUE TÂCHE", style_texte("categorie", TRAITEMENT.texte), app)
    carte_simple(d, "observe", 12, 76, 120, 108, NEUTRE, f'{b("État observé", 12)}<br>{s("docker-ce : là", INK)}<br>'
                 f'{s("docker : arrêté", INK)}<br>{s("8080 : fermé", INK)}', parent=app)
    q = d.forme("conforme", 144, 82, 104, 96, "Conforme ?", style_losange(TRAITEMENT), app)
    ok = carte_simple(d, "ok", 288, 102, 96, 56, DONNEES, f'{b("ok", 14, DONNEES.texte)}<br>{s("rien ne change")}',
                      parent=app, fond=DONNEES.fond, centre=True)
    corr = carte_simple(d, "corrige", 140, 236, 112, 56, TRAITEMENT, f'{b("corrige")}<br>{s("démarre, ouvre")}',
                        parent=app, centre=True)
    ch = carte_simple(d, "changed", 288, 236, 96, 56, RESILIENCE, f'{b("changed", 14, RESILIENCE.texte)}<br>{s("a changé")}',
                      parent=app, fond=RESILIENCE.fond, centre=True)
    d.lien("compare", "observe", q, "", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("oui", q, ok, "oui", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", decalage=(0, -12))
    d.lien("non", q, corr, "non", style_flux("applicatif", ortho=False) + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.lien("puis", corr, ch, "", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.forme("aller-retour", 12, 204, 128, 108, "Envoyée par SSH, exécutée par Python, puis effacée. Aucun agent.",
            style_texte("note", MUTED, valign="top"), app, calque="annotations")
    # playbook : y absolu 256-408 ; srv-app : y 96-424
    d.lien("envoi", "playbook", "srv-app", "SSH · tâche", style_flux("administration", fort=True, ortho=False) +
           f"exitX=1;exitY={(296 - 256) / 152:.4f};entryX=0;entryY={(296 - 96) / 328:.4f};", decalage=(0, -12))
    d.lien("reponse", "srv-app", "playbook", "ok · changed", style_flux("administration", ortho=False) +
           f"exitX=0;exitY={(372 - 96) / 328:.4f};entryX=1;entryY={(372 - 256) / 152:.4f};", decalage=(0, -12))

    res = d.forme("resultat", 24, 448, 712, 248, "③ ON REJOUE POUR VÉRIFIER", style_regroupement(), calque="frontieres")
    p1 = d.forme("passage-1", 16, 44, 320, 76, f'{b("1er passage", 12)}<br>' + html_code(["ok=4  changed=2  failed=0"]) +
                 f'<br>{s("deux écarts corrigés")}', style_document(RESILIENCE), res)
    p2 = d.forme("passage-2", 376, 44, 320, 76, f'{b("2e passage, sans rien changer", 12)}<br>' + html_code(["ok=4  changed=0  failed=0"]) +
                 f'<br>{s("<b>idempotent</b> : plus rien à corriger", DONNEES.texte)}', style_document(DONNEES), res)
    d.lien("rejouer", p1, p2, "", style_flux("applicatif", fort=True, ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.forme("verifier", 16, 140, 680, 56,
            f'{b("Puis on vérifie sur le serveur", 13)}<br>' + code("docker --version · systemctl is-enabled docker · getent group docker"),
            style_texte("detail", INK, valign="top"), res, calque="annotations")
    d.forme("limite", 16, 212, 680, 60, "<b>Limite</b> : changed=0 dit qu'il n'y a plus rien à corriger, pas que le service fonctionne. "
            "Les compteurs incluent la collecte des faits.", style_texte("note", INK, valign="top"), res, calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 03 : diagnostiquer une connexion SSH (couloirs)                     #
# --------------------------------------------------------------------------- #

def pedagogique_acces_ssh(dossier):
    d = _fond("pedagogique-acces-ssh", 680, "Une connexion SSH échoue : six questions, dans l'ordre",
              "Chaque question se vérifie sur la machine indiquée ; on s'arrête à la première qui échoue.")
    poste = machine(d, "poste", 24, 96, 300, 560, "Poste Fedora", "le client", icone="poste")
    vm = machine(d, "vm", 436, 96, 300, 560, "VM Rocky", "le serveur, depuis sa console")
    etapes = [("poste", "Le nom donne-t-il la bonne adresse ?", "getent hosts srv-admin", "Name or service not known"),
              ("poste", "La route mène-t-elle à la VM ?", "ip route get 192.168.150.5", "route ou interface inattendue"),
              ("vm", "Le service écoute-t-il sur le port 22 ?", "ss -lnt", "Connection refused"),
              ("vm", "Le pare-feu laisse-t-il passer ?", "firewall-cmd --list-all", "No route to host"),
              ("vm", "Empreinte du serveur attendue ?", "ssh-keygen -lf clé_hôte.pub", "empreinte différente"),
              ("vm", "Le compte est-il accepté ?", "~/.ssh/authorized_keys", "Permission denied (publickey)")]
    prev = None
    for i, (cote, question, commande, echec) in enumerate(etapes):
        y = 140 + i * 84
        n = d.forme(f"etape-{i + 1}", 366, y + 20, 28, 28, str(i + 1),
                    f"ellipse;fillColor={SLATE};strokeColor=none;{police('composant', CARD, 'center')}", calque="composants")
        if prev:
            d.lien(f"suite-{i}", prev, n, "", f"edgeStyle=none;endArrow=block;endFill=1;endSize=5;strokeColor={RULE};strokeWidth=2;"
                   "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
        prev = n
        cadre = poste if cote == "poste" else vm
        cid = carte_simple(d, f"question-{i + 1}", 12, y - 96, 276, 68, INFRA if cote == "poste" else TRAITEMENT,
                           f'{b(question, 13)}<br>{code(commande)}<br>{s("indice : " + echec, SECURITE.texte)}', parent=cadre)
        d.lien(f"vers-{i + 1}", n, cid, "", f"edgeStyle=none;endArrow=none;strokeColor={RULE};strokeWidth=1.5;dashed=1;dashPattern=2 3;"
               + ("exitX=0;exitY=0.5;entryX=1;entryY=0.5;" if cote == "poste" else "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"))
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 04 : ce que Terraform compare (convergence puis cycle)              #
# --------------------------------------------------------------------------- #

def pedagogique_terraform(dossier):
    d = _fond("pedagogique-terraform", 640, "Ce que Terraform compare pour calculer un plan",
              "Trois sources, une différence ; on lit le plan avant de l'appliquer.", ("principe", "Schéma de principe"))
    d.forme("code", 24, 104, 216, 104, f'{b("main.tf", 13)} {s("· ce que tu veux")}<br>' +
            html_code(["2 VM : srv-app, srv-k3s", "versionné dans Git"]), style_document(AUTOMATISATION))
    d.forme("state", 272, 104, 216, 104, f'{b("terraform.tfstate", 13)}<br>{s("ce que Terraform croit gérer")}<br>' +
            html_code(["identifiants réels"]) + f'<br>{s("hors de Git, copié ailleurs", RESILIENCE.texte)}', style_document(RESILIENCE))
    composant(d, "reel", 512, 120, 208, 72, INFRA, "serveur", "libvirt", "Ce qui existe", "VM, disques, réseaux")
    plan = carte_simple(d, "plan", 200, 268, 360, 64, NEUTRE, f'{b("terraform plan", 15)}<br>{s("la différence entre les trois, sans rien modifier")}',
                        fond=CARD, centre=True)
    for src, x in (("code", 0.15), ("state", 0.5), ("reel", 0.85)):
        d.lien(f"vers-plan-{src}", src, plan, "", style_flux("administration", ortho=False) + f"exitX=0.5;exitY=1;entryX={x};entryY=0;")
    issues = [("creer", DONNEES, "+", "créer", "la ressource manque"),
              ("modifier", TRAITEMENT, "~", "modifier sur place", "l'identifiant reste"),
              ("remplacer", SECURITE, "-/+", "remplacer", "recréation : risque pour les données")]
    for i, (ident, f, sym, nom, det) in enumerate(issues):
        x = 24 + i * 244
        carte_simple(d, ident, x, 388, 220, 68, f, f'{b(sym, 18, f.texte)}&nbsp;&nbsp;{b(nom)}<br>{s(det)}', fond=f.fond)
        d.lien(f"issue-{ident}", plan, ident, "", style_flux("applicatif", ortho=False) + f"exitX={0.2 + i * 0.3};exitY=1;entryX=0.5;entryY=0;")
    apply_ = carte_simple(d, "apply", 200, 512, 360, 56, NEUTRE, f'{b("terraform apply", 15)}<br>{s("exécute le plan accepté, puis met le state à jour")}',
                          fond=CARD, centre=True)
    d.lien("lire", "modifier", apply_, "tu relis, puis tu acceptes", style_flux("applicatif", ortho=False) +
           "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.lien("cycle-reel", apply_, "reel", "", style_flux("administration", fort=True) + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
           points=[(742, 540), (742, 156)], decalage=(-34, 0))
    d.forme("sans-state", 24, 588, 712, 40, "<b>Sans state</b>, Terraform risque de proposer des recréations : ne pas appliquer sans examiner le plan. "
            "Un plan « No changes » indique qu’aucun écart géré n’est détecté.", style_texte("note", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 06 : de la définition Compose aux conteneurs (transformation)       #
# --------------------------------------------------------------------------- #

def pedagogique_compose(dossier):
    d = _fond("pedagogique-compose", 600, "De la définition Compose aux conteneurs",
              "docker compose lit le fichier, le démon Docker crée chaque objet, puis le maintient en marche.",
              ("principe", "Schéma de principe"))
    cols = [(24, "① CE QUE TU ÉCRIS", "compose.yaml", AUTOMATISATION),
            (280, "② CE QUE DOCKER CRÉE", "docker compose up -d", TRAITEMENT),
            (536, "③ CE QUI TOURNE", "projet opsdesk", DONNEES)]
    for x, t, sous, f in cols:
        d.forme(f"col-{x}", x, 100, 200, 20, t, style_texte("categorie", f.texte), calque="annotations")
        d.forme(f"col-{x}-s", x, 120, 216, 18, sous, style_texte("note", MUTED), calque="annotations")
    lignes = [("networks: backend", "opsdesk_backend", "réseau, DNS : db", "reseau", INFRA),
              ("volumes: db-data", "opsdesk_db-data", "données PostgreSQL", "volume", DONNEES),
              ("services: db", "opsdesk-db-1", "base", "base", DONNEES),
              ("services: backend", "opsdesk-backend-1", "API, port 8000", "api", TRAITEMENT),
              ("services: frontend", "opsdesk-frontend-1", "nginx, port 8080", "navigateur", ACCES)]
    for i, (cle, objet, res, ic, f) in enumerate(lignes):
        y = 152 + i * 64
        a = d.forme(f"fichier-{i}", 24, y, 200, 48, code(cle), style_document(AUTOMATISATION) + "verticalAlign=middle;spacingTop=0;")
        bb = carte_simple(d, f"objet-{i}", 280, y, 200, 48, TRAITEMENT, code(objet), centre=True)
        c = composant(d, f"ressource-{i}", 536, y, 200, 48, f, ic, "", res, "")
        d.lien(f"cree-{i}", a, bb, "", style_flux("administration", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        d.lien(f"tourne-{i}", bb, c, "", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.forme("cycle", 24, 480, 712, 96, "", style_regroupement(), calque="frontieres")
    for i, (t, det) in enumerate([("Au boot", "systemd démarre docker, qui relance les conteneurs unless-stopped"),
                                  ("S'il s'arrête", "relancé par sa politique ; un docker stop le laisse arrêté"),
                                  ("Journaux", "docker compose logs backend")]):
        d.forme(f"cycle-{i}", 40 + i * 236, 496, 220, 64, f'{b(t, 13)}<br>{s(det)}', style_texte("detail", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 07 : la boucle de contrôle de K3s                                   #
# --------------------------------------------------------------------------- #

def pedagogique_k3s(dossier):
    d = _fond("pedagogique-k3s", 600, "Ce que K3s fait de tes déclarations",
              "Le Deployment maintient le nombre de pods ; le Service n'envoie le trafic qu'aux pods prêts.",
              ("principe", "Schéma de principe"))
    d.forme("yaml", 24, 104, 196, 216, f'{b("api.yaml", 13)} {s("· ce que tu déclares")}<br>' +
            html_code(["kind: Deployment", "replicas: 2", "readinessProbe:", "  /health/ready", "---", "kind: Service", "selector: app=api"]),
            style_document(AUTOMATISATION))
    k = machine(d, "srv-k3s", 260, 96, 476, 380, "srv-k3s", "K3s, un nœud", icone="grappe")
    dep = carte_simple(d, "deployment", 16, 52, 300, 60, TRAITEMENT, f'{b("Deployment")}<br>{s("veut 2 pods, en compte 1, en crée un")}', parent=k)
    pa = composant(d, "pod-a", 16, 164, 140, 60, DONNEES, "conteneur", "", "Pod A", "prêt · 1/1", parent=k)
    pb = composant(d, "pod-b", 176, 164, 140, 60, NEUTRE, "conteneur", "", "Pod B", "0/1", prevu=True, parent=k)
    svc = carte_simple(d, "service", 16, 296, 300, 60, ACCES, f'{b("Service api")}<br>{s("endpoints : Pod A seulement")}', parent=k)
    ing = carte_simple(d, "ingress", 340, 296, 120, 60, ACCES, f'{b("Ingress")}<br>{s("Traefik")}', parent=k)
    d.lien("applique", "yaml", dep, "apply", style_flux("administration", ortho=False) +
           f"exitX=1;exitY={(178 - 104) / 216:.4f};entryX=0;entryY=0.5;", decalage=(0, -12))
    d.lien("cree-a", dep, pa, "", style_flux("administration", ortho=False) + f"exitX={86 / 300:.4f};exitY=1;entryX=0.5;entryY=0;")
    d.lien("cree-b", dep, pb, "", style_flux("administration", ortho=False) + f"exitX={246 / 300:.4f};exitY=1;entryX=0.5;entryY=0;")
    d.lien("entree", ing, svc, "", style_flux("applicatif", ortho=False) + "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
    d.lien("trafic", svc, pa, "trafic", style_flux("applicatif", fort=True, ortho=False) +
           f"exitX={86 / 300:.4f};exitY=0;entryX=0.5;entryY=1;", decalage=(0, 0))
    d.forme("exclu", 340, 156, 124, 76, "<b>Pas de trafic</b> vers Pod B tant que sa sonde échoue.",
            style_texte("note", SECURITE.texte, valign="middle"), parent=k, calque="annotations")
    d.forme("sondes", 24, 496, 712, 72,
            "<b>readinessProbe</b> (/health/ready) : prêt ou non à recevoir du trafic ; un échec retire le pod du Service, sans le redémarrer. "
            "<b>livenessProbe</b> (/health/live) : encore vivant ; un échec le redémarre.",
            style_texte("note", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 08 : du commit au service (couloirs, points de contrôle)            #
# --------------------------------------------------------------------------- #

def pedagogique_cicd(dossier):
    d = _fond("pedagogique-cicd", 620, "Du commit au service",
              "La CI prouve et publie ; le déploiement reste une décision humaine.",
              ("prevu", "Prévu · exercice 08"))
    gh = d.forme("github", 24, 96, 712, 256, "GITHUB ACTIONS · CONTRÔLES AUTOMATISÉS", style_zone(prevu=True, teinte=CARD), calque="frontieres")
    etapes = [("tests", TRAITEMENT, "liste", "Tests", "pytest sur PostgreSQL"),
              ("images", TRAITEMENT, "conteneur", "Images", "sur main seulement"),
              ("trivy", SECURITE, "bouclier", "Trivy", "vulnérabilités graves ?"),
              ("ghcr", AUTOMATISATION, "depot", "GHCR", "tag et digest")]
    for i, (ident, f, ic, nom, det) in enumerate(etapes):
        composant(d, ident, [16, 200, 384, 556][i], 48, 140, 60, f, ic, "", nom, det, prevu=True, parent=gh)
        if i:
            d.lien(f"suite-{i}", etapes[i - 1][0], ident, "", style_flux("administration", prevu=True, ortho=False) +
                   "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    carte_simple(d, "stop-tests", 6, 160, 160, 52, SECURITE, f'{b("échec : arrêt", 13, SECURITE.texte)}<br>{s("pas d\'image")}', parent=gh, fond=SECURITE.fond, centre=True)
    carte_simple(d, "stop-trivy", 374, 160, 160, 52, SECURITE, f'{b("grave : arrêt", 13, SECURITE.texte)}<br>{s("ou exception écrite")}', parent=gh, fond=SECURITE.fond, centre=True)
    d.forme("pr", 190, 156, 168, 60, "Une <b>pull request</b> s'arrête après les tests : testée, jamais publiée.",
            style_texte("note", MUTED, valign="middle"), parent=gh, calque="annotations")
    d.lien("ko-tests", "tests", "stop-tests", "rouge", style_flux("administration", prevu=True, ortho=False) + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.lien("ko-trivy", "trivy", "stop-trivy", "oui", style_flux("administration", prevu=True, ortho=False) + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    lab = d.forme("labo", 24, 384, 712, 168, "LABORATOIRE PRIVÉ · DÉCISION HUMAINE", style_zone(prevu=True), calque="frontieres")
    composant(d, "choix", 16, 48, 200, 64, AUTOMATISATION, "administrateur", "srv-admin", "Choisir une version", "dont la CI est verte", prevu=True, parent=lab)
    composant(d, "deploie", 256, 48, 184, 64, AUTOMATISATION, "liste", "Ansible", "Déployer", "digests et cible", prevu=True, parent=lab)
    composant(d, "app", 536, 48, 172, 64, ACCES, "serveur", "srv-app", "Tirer par digest", "puis /health/ready", prevu=True, parent=lab)
    d.lien("dec", "choix", "deploie", "", style_flux("administration", prevu=True, ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("dep", "deploie", "app", "SSH", style_flux("administration", prevu=True, ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", decalage=(0, -12))
    d.lien("pull", "ghcr", "app", "image", style_flux("administration", prevu=True, ortho=False) +
           f"exitX=0.5;exitY=1;entryX={(650 - 24 - 536) / 172:.4f};entryY=0;")
    d.forme("preuve", 24, 568, 712, 40, "<b>La preuve</b> : les digests des deux images déployées correspondent aux artefacts qualifiés et publiés par la CI.",
            style_texte("note", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 09 : de la mesure à l'alerte (collecte, puis machine à états)       #
# --------------------------------------------------------------------------- #

def pedagogique_supervision(dossier):
    d = _fond("pedagogique-supervision", 640, "De la mesure à l'alerte",
              "Prometheus va chercher les mesures ; une règle d'alerte passe par trois états.", ("principe", "Schéma de principe"))
    app = machine(d, "srv-app", 24, 96, 300, 176, "srv-app", "ce qui est mesuré")
    composant(d, "api", 12, 48, 276, 52, TRAITEMENT, "api", "", "API · /metrics :8000", "requêtes, latence, opsdesk_database_up", parent=app)
    composant(d, "node", 12, 112, 276, 52, OBSERVABILITE, "mesures", "", "node_exporter · :9100", "processeur, mémoire, disque", parent=app)
    k = machine(d, "srv-k3s", 436, 96, 300, 176, "srv-k3s", "ce qui mesure")
    composant(d, "prom", 12, 48, 276, 52, OBSERVABILITE, "mesures", "", "Prometheus", "lit chaque cible toutes les 15 s", parent=k)
    composant(d, "graf", 12, 112, 276, 52, OBSERVABILITE, "alerte", "", "Grafana", "tableaux de bord", parent=k)
    d.lien("lit-api", "prom", "api", "lit", style_flux("observabilite", ortho=False) + "exitX=0;exitY=0.5;entryX=1;entryY=0.5;", decalage=(0, -12))
    d.lien("lit-node", "prom", "node", "", style_flux("observabilite") + "exitX=0;exitY=0.8;entryX=1;entryY=0.5;")
    d.forme("regle", 24, 300, 712, 44, f'{b("La règle « base indisponible »", 13)}&nbsp;&nbsp;' + code("opsdesk_database_up == 0") + "&nbsp;&nbsp;" + s("pendant 1 minute (for: 1m)"),
            style_texte("detail", INK), calque="annotations")
    etats = [("inactive", NEUTRE, "Inactive", "la condition est fausse"),
             ("pending", RESILIENCE, "Pending", "vraie, depuis moins de 1 min"),
             ("firing", SECURITE, "Firing", "vraie depuis 1 min : l'alerte sonne")]
    for i, (ident, f, nom, det) in enumerate(etats):
        carte_simple(d, ident, 24 + i * 266, 380, 180, 80, f, f'{b(nom, 15, f.texte)}<br>{s(det)}', fond=f.fond, centre=True)
    d.lien("t1", "inactive", "pending", "devient vraie", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.35;entryX=0;entryY=0.35;", decalage=(0, -12))
    d.lien("t2", "pending", "firing", "reste vraie 1 min", style_flux("applicatif", ortho=False) + "exitX=1;exitY=0.35;entryX=0;entryY=0.35;", decalage=(0, -12))
    d.lien("t3", "pending", "inactive", "redevient fausse", style_flux("applicatif", ortho=False) + "exitX=0;exitY=0.75;entryX=1;entryY=0.75;", decalage=(0, 12))
    d.lien("t4", "firing", "inactive", "rétablie", style_flux("applicatif") + "exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=[(646, 500), (114, 500)])
    d.forme("note", 24, 532, 712, 80, "Si l'API elle-même ne répond plus, opsdesk_database_up n'existe plus : cette règle se tait. "
            "C'est la mesure « up » de la cible qui le montre. Ici, aucune alerte n'envoie de message : elles se lisent dans Prometheus et Grafana.",
            style_texte("note", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)


# --------------------------------------------------------------------------- #
# Exercice 11 : ce que l'on peut perdre, et le temps pour revenir (temps)      #
# --------------------------------------------------------------------------- #

def pedagogique_sauvegarde(dossier):
    d = _fond("pedagogique-sauvegarde", 600, "Ce que l'on peut perdre, et le temps pour revenir",
              "Les mesures de perte et de reprise se comparent aux objectifs RPO et RTO.",
              ("principe", "Heures d'exemple"))
    y = 176
    x0, x1 = 48, 712
    d.trait_libre("temps", x0, y, x1, y, f"endArrow=block;endFill=1;strokeColor={SLATE};strokeWidth=2.5;")

    def x_heure(h):
        return x0 + (x1 - x0 - 24) * (h - 0) / 18

    reperes = [(2, "02:00", "pg_dump", RESILIENCE), (14, "14:00", "panne", SECURITE), (16, "16:00", "service rétabli", DONNEES)]
    for i, (h, t, nom, f) in enumerate(reperes):
        x = x_heure(h)
        d.forme(f"repere-{i}", x - 8, y - 8, 16, 16, "", f"ellipse;fillColor={f.trait};strokeColor=none;", calque="composants")
        d.forme(f"repere-{i}-t", x - 60, y - 52, 120, 36, f'{b(t, 13)}<br>{s(nom, f.texte)}', style_texte("detail", INK, "center", valign="bottom"),
                calque="annotations")

    def accolade(ident, ha, hb, yy, texte, f):
        xa, xb = x_heure(ha), x_heure(hb)
        st = f"endArrow=none;strokeColor={f.trait};strokeWidth=2;"
        d.trait_libre(f"{ident}-h", xa, yy, xb, yy, st)
        d.trait_libre(f"{ident}-a", xa, yy - 8, xa, yy + 8, st)
        d.trait_libre(f"{ident}-b", xb, yy - 8, xb, yy + 8, st)
        d.forme(f"{ident}-t", xa, yy + 10, xb - xa, 36, texte, style_texte("detail", INK, "center", valign="top"), calque="annotations")

    accolade("rpo", 2, 14, 216, f'{b("Perte : 12 h", 13, SECURITE.texte)}<br>{s("fenêtre de perte à comparer au RPO")}', SECURITE)
    accolade("rto", 14, 16, 216, f'{b("Délai : 2 h", 13, DONNEES.texte)}<br>{s("à comparer au RTO")}', DONNEES)

    d.forme("restauration-titre", 24, 296, 712, 20, "LA RESTAURATION, DANS L'ORDRE", style_texte("categorie", MUTED), calque="annotations")
    etapes = [("copie", RESILIENCE, "sauvegarde", "La copie", "sur l'hôte, empreinte vérifiée"),
              ("cible", INFRA, "serveur", "Une cible vide", "jamais la base en service"),
              ("restore", DONNEES, "restauration", "pg_restore", "code de retour 0"),
              ("preuve", ACCES, "valide", "Ticket témoin", "relu dans l'interface")]
    for i, (ident, f, ic, nom, det) in enumerate(etapes):
        composant(d, ident, 24 + i * 180, 328, 164, 64, f, ic, "", nom, det)
        if i:
            d.lien(f"etape-{i}", etapes[i - 1][0], ident, "", style_flux("sauvegarde", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.forme("ou", 24, 416, 712, 20, "OÙ VIVENT LES COPIES", style_texte("categorie", MUTED), calque="annotations")
    composant(d, "sur-app", 24, 448, 260, 60, RESILIENCE, "horloge", "srv-app", "7 copies nocturnes", "minuteur 02:00, rotation")
    composant(d, "sur-hote", 476, 448, 260, 60, RESILIENCE, "sauvegarde", "hôte", "~/sauvegardes", "survit à la perte de la VM")
    d.lien("rsync", "sur-app", "sur-hote", "rsync · SSH", style_flux("sauvegarde", ortho=False) + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", decalage=(0, -12))
    d.forme("limite", 24, 528, 712, 48, "<b>Limite</b> : la copie sur l'hôte ne survit pas à la perte du PC lui-même. "
            "Une sauvegarde jamais restaurée n'est qu'un espoir.", style_texte("note", INK, valign="top"), calque="annotations")
    return d.enregistrer(dossier)



# --------------------------------------------------------------------------- #
# V26 — Deux vues complémentaires, sans résoudre les exercices personnels.   #
# --------------------------------------------------------------------------- #

def sequence_consultation(dossier):
    """Consultation d'un ticket existant, pas la solution à la création/prise en charge."""
    W, H = 920, 888
    d = Diagramme("sequence-consultation", W, H)
    d.forme("canevas", 0, 0, W, H, "", style_canevas(), calque="fond")
    titre(d, "Consulter un ticket : la requête de bout en bout",
          "Schéma de principe · pile locale de référence · utilisateur déjà connecté", l=W-64)
    x = [112, 344, 576, 808]
    acteurs = [("client", ACCES, "navigateur", "Navigateur", "interface React"),
               ("proxy", ACCES, "service", "nginx", "frontend · :8080"),
               ("api", TRAITEMENT, "api", "FastAPI", "backend · :8000"),
               ("db", DONNEES, "base", "PostgreSQL", "db · :5432")]
    for i, (ident, f, ic, nom, det) in enumerate(acteurs):
        composant(d, ident, x[i]-88, 92, 176, 64, f, ic, "", nom, det)
        d.trait_libre("vie-"+ident, x[i], 156, x[i], 732,
                    f"endArrow=none;dashed=1;dashPattern=3 5;strokeColor={RULE};strokeWidth=1.5;", calque="frontieres")
    zones = [("req", 176, 116, "01 · ACHEMINER LA REQUÊTE"),
             ("auth", 308, 160, "02 · AUTHENTIFIER LE COMPTE"),
             ("lecture", 484, 130, "03 · VÉRIFIER LA VISIBILITÉ ET LIRE"),
             ("retour", 630, 108, "04 · RETOURNER LA RÉPONSE")]
    for ident, y, h, label in zones:
        d.forme("zone-"+ident, 16, y, 888, h, "", style_regroupement(), calque="fond")
        d.forme("label-"+ident, 28, y+4, 420, 20, label, style_texte("categorie", MUTED), calque="annotations")
    for ident, i, y1, y2, f in [("p",1,228,710,ACCES),("a",2,270,668,TRAITEMENT),("d1",3,370,418,DONNEES),("d2",3,540,590,DONNEES)]:
        d.forme("act-"+ident, x[i]-5, y1, 10, y2-y1, "",
               f"rounded=0;fillColor={f.fond};strokeColor={f.trait};strokeWidth=1.25;", calque="composants")
    def message(ident, a, z, y, label, retour=False):
        xa, xb = x[a], x[z]
        sens = 1 if xb>xa else -1
        st = style_flux("applicatif", ortho=False)
        if retour:
            st += "dashed=1;dashPattern=4 4;endArrow=open;endFill=0;"
        d.trait_libre("flux-"+ident, xa+6*sens, y, xb-6*sens, y, st, calque="flux")
        d.forme("txt-"+ident, min(xa,xb)+10, y-29, abs(xb-xa)-20, 26,
                label, style_texte("detail", INK, "center"), calque="annotations")
    message("01",0,1,228,"1 · GET /api/tickets/{id}<br>Authorization: Bearer …")
    message("02",1,2,274,"2 · Relais HTTP vers backend")
    d.forme("jwt", 358, 330, 204, 42, "3 · Vérifie le JWT<br>signature, expiration, identifiant",
            style_texte("detail", TRAITEMENT.texte, "center"), calque="annotations")
    message("04",2,3,374,"4 · Charge le compte actif")
    message("05",3,2,418,"5 · Compte renvoyé",True)
    d.forme("visibilite", 358, 500, 204, 42, "6 · Filtre la visibilité<br>demandeur ou membre du support",
            style_texte("detail", TRAITEMENT.texte, "center"), calque="annotations")
    message("07",2,3,548,"7 · SELECT du ticket visible")
    message("08",3,2,590,"8 · Données + relations",True)
    message("09",2,1,668,"9 · HTTP 200 + JSON",True)
    message("10",1,0,710,"10 · Relais de la réponse",True)
    carte_simple(d,"ok",24,754,280,102,ACCES,
                 b("Résultat")+ "<br>"+s("React affiche le ticket ; nginx ne décide pas des droits."))
    carte_simple(d,"err1",320,754,280,102,SECURITE,
                 b("401 · Authentification")+ "<br>"+s("Jeton absent, invalide ou compte désactivé. Aucun ticket livré."))
    carte_simple(d,"err2",616,754,280,102,SECURITE,
                 b("404 · Visibilité")+ "<br>"+s("Ticket inexistant ou non visible pour ce compte."))
    return d.enregistrer(dossier)


def diagnostic_service(dossier):
    """Arbre de diagnostic : indices et vérifications, pas les cartes de panne."""
    d = _fond("diagnostic-service", 920, "Diagnostiquer OpsDesk par couches",
              "Observer avant de modifier · la première sonde en échec oriente, sans prouver la cause.")
    carte_simple(d,"depart",32,92,696,64,INFRA,
                 b("Un utilisateur ne peut plus accéder à ses tickets", 15)+"<br>"+s("Confirmer cible, version, heure, impact et périmètre ; reproduire sans changer le service."),fond=HEADER)
    tests = [
        ("nginx", "1 · /healthz", "HTTP 200 ?", "Accès ou nginx", "URL/DNS, route, port 8080, processus et journaux nginx.", ACCES),
        ("live", "2 · /health/live", "HTTP 200 ?", "API ou trajet proxy", "État du backend, DNS interne, journaux, délai 502/504.", TRAITEMENT),
        ("ready", "3 · /health/ready", "200 et database up ?", "Dépendance base", "Connexion DB, réseau, stockage, secret lisible sans affichage.", DONNEES),
        ("metier", "4 · Parcours métier", "Ticket accessible ?", "Règles ou droits", "401/403/404/409/422, compte, requête et request_id.", SECURITE),
    ]
    for i,(ident,nom,q,diag,detail,f) in enumerate(tests):
        y=184+i*132
        d.forme(ident,44,y,308,88,b(nom,15)+"<br>"+s(q,INK,13),style_losange(f),calque="composants")
        carte_simple(d,"cause-"+ident,428,y-2,300,92,f,b(diag)+"<br>"+s(detail),fond=f.fond)
        d.lien("non-"+ident,ident,"cause-"+ident,"Non",style_flux("applicatif",ortho=False)+"exitX=1;exitY=0.5;entryX=0;entryY=0.5;",decalage=(0,-12))
        prev="depart" if i==0 else tests[i-1][0]
        if i==0:
            d.lien("suite-"+ident,prev,ident,"",style_flux()+"exitX=0.24;exitY=1;entryX=0.5;entryY=0;")
        else:
            d.lien("suite-"+ident,prev,ident,"Oui",style_flux("applicatif",ortho=False)+"exitX=0.5;exitY=1;entryX=0.5;entryY=0;",decalage=(26,0))
    carte_simple(d,"vert",44,712,308,70,ACCES,b("Oui · vérifier l'intermittence")+"<br>"+s("Comparer métriques, journaux et heure du signal."),fond=ACCES.fond)
    d.lien("suite-vert","metier","vert","Oui",style_flux("applicatif",ortho=False)+"exitX=0.5;exitY=1;entryX=0.5;entryY=0;",decalage=(26,0))
    carte_simple(d,"regle",428,704,300,86,RESILIENCE,b("Avant toute correction")+"<br>"+s("Tester une hypothèse ; confirmer la cible et le retour arrière."),fond=RESILIENCE.fond)
    # Bus à droite des cartes : chaque piste rejoint le même contrôle avant action.
    bus_style = f"endArrow=none;strokeColor={SLATE};strokeWidth=1.5;"
    for i in range(4):
        yy=228+i*132
        d.trait_libre("bus-branche-"+str(i),728,yy,744,yy,bus_style,calque="flux")
    d.trait_libre("bus-vertical",744,228,744,747,bus_style,calque="flux")
    d.trait_libre("bus-regle",744,747,728,747,style_flux("applicatif",ortho=False),calque="flux")
    carte_simple(d,"fin",32,816,696,76,INFRA,b("Corriger une seule cause confirmée, puis recontrôler",15)+"<br>"+s("Sondes + parcours utilisateur + ticket témoin ; noter chronologie, impact et limites."),fond=HEADER)
    d.lien("fin-dessus","vert","fin","",style_flux("applicatif",ortho=False)+"exitX=0.5;exitY=1;entryX=0.24;entryY=0;")
    d.lien("fin-correction","regle","fin","",style_flux("applicatif",ortho=False)+"exitX=0.5;exitY=1;entryX=0.78;entryY=0;")
    return d.enregistrer(dossier)


CONSTRUCTIONS = (presentation, presentation_mobile, presentation_notion, architecture, architecture_globale, pedagogique_ansible,
                 pedagogique_acces_ssh, pedagogique_terraform, pedagogique_compose, pedagogique_k3s,
                 pedagogique_cicd, pedagogique_supervision, pedagogique_sauvegarde, sequence_consultation, diagnostic_service)

if __name__ == "__main__":
    sortie = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    sortie.mkdir(parents=True, exist_ok=True)
    for construire in CONSTRUCTIONS:
        print(construire(sortie))
