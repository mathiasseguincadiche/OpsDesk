"""Système graphique de la collection V24 : jetons, icônes et formes Draw.io.

Ce module ne dessine aucun schéma : il fournit le langage commun (couleurs,
typographie, icônes, composants, connecteurs, statuts, légende) que les
compositions de `generer_schemas_modeles.py` assemblent. La description
lisible du système est dans `MODELES/schemas/systeme-graphique.md`.
"""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------- #
# Jetons : couleurs                                                            #
# --------------------------------------------------------------------------- #

INK, MUTED, SLATE = "#1D293B", "#596A80", "#33445D"
RULE, CANVAS, CARD = "#C9D3E2", "#F6F8FC", "#FFFFFF"
HEADER, ZONE = "#E9EEF6", "#EEF2F8"


@dataclass(frozen=True)
class Famille:
    """Une famille de composants : un trait, un texte (contraste >= 4,5:1), un fond."""
    nom: str
    trait: str
    texte: str
    fond: str


ACCES = Famille("Accès et interface", "#2864F0", "#2459D6", "#EDF3FF")
TRAITEMENT = Famille("Traitement", "#7549D8", "#6D3FD0", "#F3EFFF")
DONNEES = Famille("Données", "#008D7B", "#007C6C", "#EAF8F3")
AUTOMATISATION = Famille("Automatisation", "#0E6E86", "#0E6E86", "#E7F5F9")
OBSERVABILITE = Famille("Observabilité", "#B4245B", "#B4245B", "#FDEFF4")
RESILIENCE = Famille("Résilience", "#C66A29", "#A85A22", "#FFF4EC")
SECURITE = Famille("Sécurité", "#B42318", "#B42318", "#FEF1EF")
INFRA = Famille("Infrastructure", SLATE, INK, HEADER)
NEUTRE = Famille("Neutre", MUTED, INK, CARD)

FAMILLES = [ACCES, TRAITEMENT, DONNEES, AUTOMATISATION, OBSERVABILITE, RESILIENCE, SECURITE, INFRA]

# Catégories de flux : la couleur dit la nature du flux ; le trait dit l'avancement.
FLUX = {
    "applicatif": ("Applicatif", SLATE),
    "administration": ("Administration et déploiement", AUTOMATISATION.trait),
    "observabilite": ("Observabilité", OBSERVABILITE.trait),
    "sauvegarde": ("Sauvegarde", RESILIENCE.trait),
}

# --------------------------------------------------------------------------- #
# Jetons : typographie et micro-design                                         #
# --------------------------------------------------------------------------- #

FONT = "Helvetica"          # rendu en Arial ou Helvetica selon le système, jamais intégrée
TYPO = {                    # taille en px, graisse
    "titre": (20, True), "sous_titre": (13, False),
    "zone": (12, True), "machine": (15, True), "composant": (14, True),
    "categorie": (12, True), "detail": (12, False), "flux": (12, True), "note": (12, False),
}
GRILLE = 8                  # toutes les positions et tailles sont des multiples de 8 (4 pour les détails)
MARGE_CANEVAS = 24
PADDING = 12                # marge intérieure d'un composant
ICONE = 24                  # icône dans un composant ; 32 pour un point focal
RAYON = {"composant": 8, "machine": 10, "zone": 14, "pastille": 12}
TRAIT = {"composant": 1.25, "machine": 1.5, "zone": 1, "flux": 1.75, "flux_fort": 2.25}
TIRETS_PREVU = "8 5"

# --------------------------------------------------------------------------- #
# Icônes : dessinées pour la collection, au trait, grille 24, un seul style    #
# --------------------------------------------------------------------------- #

_ICONES = {
    "utilisateur": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c0-3.9 3.1-6.5 7-6.5s7 2.6 7 6.5"/>',
    "administrateur": '<circle cx="10" cy="8" r="3.5"/><path d="M3.5 20c0-3.7 2.9-6.3 6.5-6.3 1.3 0 2.5.3 3.5.9"/>'
                      '<path d="M17.5 13.5l3 1.2v2.6c0 1.8-1.3 3-3 3.7-1.7-.7-3-1.9-3-3.7v-2.6z"/>',
    "navigateur": '<rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="M3 9h18"/><circle cx="6" cy="6.8" r=".6"/><circle cx="8.4" cy="6.8" r=".6"/>',
    "poste": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
    "serveur": '<rect x="4" y="3.5" width="16" height="7" rx="1.5"/><rect x="4" y="13.5" width="16" height="7" rx="1.5"/>'
               '<path d="M7.5 7h.01M7.5 17h.01M11 7h5M11 17h5"/>',
    "conteneur": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
    "service": '<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "grappe": '<circle cx="12" cy="5.5" r="2.5"/><circle cx="5.5" cy="17" r="2.5"/><circle cx="18.5" cy="17" r="2.5"/><path d="M10.8 7.7L6.7 14.8M13.2 7.7l4.1 7.1M8 17h8"/>',
    "reseau": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2V12M12 12l-5.4 5.4M12 12l5.4 5.4"/>',
    "pare_feu": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3 9.7h18M3 14.3h18M9 5v4.7M15 9.7v4.6M9 14.3V19"/>',
    "api": '<path d="M8 6l-5 6 5 6M16 6l5 6-5 6M13.5 4l-3 16"/>',
    "base": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13"/><path d="M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
    "volume": '<rect x="3" y="7" width="18" height="10" rx="2"/><path d="M7 12h6"/><circle cx="17" cy="12" r=".9"/>',
    "fichier": '<path d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5M9 12h6M9 15.5h6"/>',
    "liste": '<path d="M6 2.5h8l4.5 4.5v14.5H6z"/><path d="M14 2.5V7h4.5"/><path d="M8.5 12.5l1.2 1.2 2-2.2M8.5 17l1.2 1.2 2-2.2M13.5 13h2.5M13.5 17.5h2.5"/>',
    "script": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9.5l3 2.5-3 2.5M12 15h5"/>',
    "pipeline": '<circle cx="5" cy="12" r="2.2"/><circle cx="12" cy="12" r="2.2"/><circle cx="19" cy="12" r="2.2"/><path d="M7.2 12h2.6M14.2 12h2.6"/>',
    "cle": '<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M21 12v2.5"/>',
    "cadenas": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 018 0v3M12 15v2"/>',
    "bouclier": '<path d="M12 3l7.5 3v5.5c0 4.5-3.2 7.8-7.5 9.5-4.3-1.7-7.5-5-7.5-9.5V6z"/>',
    "mesures": '<path d="M4 4v16h16"/><path d="M7.5 15l3.5-4 3 2.5 4.5-6"/>',
    "journaux": '<path d="M5 6h14M5 10h14M5 14h9M5 18h11"/>',
    "alerte": '<path d="M12 3.5a5.5 5.5 0 00-5.5 5.5v4l-2 3h15l-2-3V9A5.5 5.5 0 0012 3.5zM10 19.5a2 2 0 004 0"/>',
    "sauvegarde": '<rect x="3.5" y="4" width="17" height="4.5" rx="1"/><path d="M5 8.5V20h14V8.5M12 11.5v5.5M9.5 14.5L12 17l2.5-2.5"/>',
    "restauration": '<path d="M4.5 12a7.5 7.5 0 107.5-7.5H8"/><path d="M10.5 1.8L7.8 4.5l2.7 2.7M12 8.5V12l2.5 1.8"/>',
    "depot": '<circle cx="6" cy="5.5" r="2.2"/><circle cx="6" cy="18.5" r="2.2"/><circle cx="18" cy="9" r="2.2"/><path d="M6 7.7v8.6M18 11.2c0 3.6-6 2.4-10.3 5.8"/>',
    "nuage": '<path d="M7 18.5a4.5 4.5 0 01-.6-9 6 6 0 0111.4 1.5 3.8 3.8 0 01-.8 7.5z"/>',
    "horloge": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
    "valide": '<circle cx="12" cy="12" r="8.5"/><path d="M8.2 12.3l2.5 2.5 5-5.3"/>',
    "echec": '<circle cx="12" cy="12" r="8.5"/><path d="M9 9l6 6M15 9l-6 6"/>',
    "decision": '<path d="M12 3l9 9-9 9-9-9z"/><path d="M12 8.5v4M12 15.5h.01"/>',
}


def icone_svg(nom: str, couleur: str, taille: int = 24) -> str:
    corps = _ICONES[nom]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{taille}" height="{taille}" viewBox="0 0 24 24" '
            f'fill="none" stroke="{couleur}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{corps}</svg>')


def icone_style(nom: str, couleur: str) -> str:
    """Style Draw.io d'une image d'icône (data URI sans « ;base64 », convention Draw.io)."""
    data = base64.b64encode(icone_svg(nom, couleur).encode()).decode()
    return f"shape=image;aspect=fixed;imageAspect=0;verticalLabelPosition=bottom;image=data:image/svg+xml,{data};"


NOMS_ICONES = list(_ICONES)

# --------------------------------------------------------------------------- #
# Diagramme : cellules nommées, calques                                        #
# --------------------------------------------------------------------------- #


def _txt(s: str) -> str:
    return escape(s, {'"': "&quot;"})


class Diagramme:
    """Un fichier .drawio : une page, des calques, des cellules aux identifiants explicites."""

    CALQUES = ("fond", "frontieres", "composants", "flux", "annotations")

    def __init__(self, nom: str, largeur: int, hauteur: int):
        self.nom, self.largeur, self.hauteur = nom, largeur, hauteur
        self.cellules: list[str] = []
        self.ids: set[str] = set()
        for calque in self.CALQUES:
            self.cellules.append(f'<mxCell id="calque-{calque}" value="{calque.capitalize()}" parent="0"/>')

    def _id(self, ident: str) -> str:
        base, n = ident, 2
        while ident in self.ids:
            ident, n = f"{base}-{n}", n + 1
        self.ids.add(ident)
        return ident

    def forme(self, ident, x, y, l, h, valeur="", style="", parent=None, calque="composants"):
        ident = self._id(ident)
        parent = parent or f"calque-{calque}"
        self.cellules.append(
            f'<mxCell id="{ident}" value="{_txt(valeur)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{l}" height="{h}" as="geometry"/></mxCell>')
        return ident

    def lien(self, ident, source, cible, valeur="", style="", points=(), calque="flux", decalage=None):
        ident = self._id(ident)
        pts = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points)
        geo = '<mxGeometry relative="1" as="geometry">'
        if pts:
            geo += f'<Array as="points">{pts}</Array>'
        if decalage:
            geo += f'<mxPoint x="{decalage[0]}" y="{decalage[1]}" as="offset"/>'
        geo += "</mxGeometry>"
        self.cellules.append(
            f'<mxCell id="{ident}" value="{_txt(valeur)}" style="{style}" edge="1" parent="calque-{calque}" '
            f'source="{source}" target="{cible}">{geo}</mxCell>')
        return ident

    def trait_libre(self, ident, x1, y1, x2, y2, style, calque="annotations"):
        """Segment sans forme d'origine ni d'arrivée (légende, ligne de temps, ligne de vie)."""
        ident = self._id(ident)
        self.cellules.append(
            f'<mxCell id="{ident}" value="" style="{style}" edge="1" parent="calque-{calque}">'
            f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/></mxGeometry></mxCell>')
        return ident

    def xml(self) -> str:
        corps = "".join(self.cellules)
        return (f'<mxGraphModel dx="{self.largeur}" dy="{self.hauteur}" grid="1" gridSize="{GRILLE}" guides="1" '
                f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.largeur}" '
                f'pageHeight="{self.hauteur}" background="none" math="0" shadow="0"><root><mxCell id="0"/>{corps}'
                f"</root></mxGraphModel>")

    def enregistrer(self, dossier: Path) -> Path:
        chemin = Path(dossier) / f"{self.nom}.drawio"
        chemin.write_text(f'<mxfile host="Collection V24" agent="systeme_graphique.py">'
                          f'<diagram id="{self.nom}" name="{self.nom}">{self.xml()}</diagram></mxfile>',
                          encoding="utf-8")
        return chemin

# --------------------------------------------------------------------------- #
# Styles                                                                       #
# --------------------------------------------------------------------------- #


def police(role: str, couleur: str = INK, align: str = "left") -> str:
    taille, gras = TYPO[role]
    return f"fontFamily={FONT};fontSize={taille};fontColor={couleur};align={align};{'fontStyle=1;' if gras else ''}"


def _tirets(prevu: bool) -> str:
    return f"dashed=1;dashPattern={TIRETS_PREVU};" if prevu else ""


def style_texte(role="note", couleur=MUTED, align="left", valign="middle") -> str:
    return (f"text;html=1;whiteSpace=wrap;strokeColor=none;fillColor=none;verticalAlign={valign};"
            f"spacing=0;{police(role, couleur, align)}")


def style_canevas() -> str:
    return f"rounded=1;arcSize=2;fillColor={CANVAS};strokeColor=none;"


def style_zone(prevu=False, teinte=ZONE) -> str:
    """Vraie frontière (hôte, réseau, zone de confiance) : teinte, trait fin, titre en capitales."""
    return (f"rounded=1;arcSize={RAYON['zone']};absoluteArcSize=1;html=1;whiteSpace=wrap;fillColor={teinte};"
            f"strokeColor={SLATE};strokeWidth={TRAIT['zone']};{_tirets(prevu)}verticalAlign=top;align=left;"
            f"spacingLeft=16;spacingTop=10;{police('zone', SLATE)}")


def style_regroupement() -> str:
    """Regroupement pédagogique, sans valeur technique : fond seul, sans trait."""
    return (f"rounded=1;arcSize=12;absoluteArcSize=1;html=1;whiteSpace=wrap;fillColor={ZONE};strokeColor=none;"
            f"verticalAlign=top;align=left;spacingLeft=16;spacingTop=12;{police('zone', MUTED)}")


def style_machine(prevu=False) -> str:
    """Machine ou VM : conteneur à bandeau d'en-tête (déplacer la machine déplace son contenu)."""
    return (f"swimlane;html=1;whiteSpace=wrap;startSize=36;rounded=1;arcSize={RAYON['machine']};absoluteArcSize=1;"
            f"fillColor={HEADER};swimlaneFillColor={CARD};strokeColor={SLATE};strokeWidth={TRAIT['machine']};"
            f"{_tirets(prevu)}align=left;spacingLeft=44;collapsible=0;container=1;{police('machine', INK)}")


def style_carte(f: Famille, prevu=False, fond=None) -> str:
    return (f"rounded=1;arcSize={RAYON['composant']};absoluteArcSize=1;html=1;whiteSpace=wrap;"
            f"fillColor={fond or CARD};strokeColor={f.trait};strokeWidth={TRAIT['composant']};{_tirets(prevu)}"
            f"align=left;verticalAlign=middle;spacingLeft={PADDING + ICONE + 10};spacingRight={PADDING};"
            f"{police('detail', INK)}")


def style_cylindre(f: Famille, prevu=False) -> str:
    return (f"shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=9;html=1;whiteSpace=wrap;fillColor={f.fond};"
            f"strokeColor={f.trait};strokeWidth={TRAIT['composant']};{_tirets(prevu)}{police('detail', INK, 'center')}")


def style_document(f: Famille, prevu=False) -> str:
    return (f"shape=note;size=14;html=1;whiteSpace=wrap;fillColor={CARD};strokeColor={f.trait};"
            f"strokeWidth={TRAIT['composant']};{_tirets(prevu)}align=left;verticalAlign=top;spacingLeft={PADDING};"
            f"spacingTop=10;spacingRight={PADDING};{police('detail', INK)}")


def style_pastille(f: Famille = NEUTRE, plein=False) -> str:
    fond = f.fond if plein else CARD
    return (f"rounded=1;arcSize=50;html=1;whiteSpace=wrap;fillColor={fond};strokeColor={f.trait};strokeWidth=1;"
            f"{police('categorie', f.texte, 'center')}")


def style_losange(f: Famille) -> str:
    return (f"rhombus;html=1;whiteSpace=wrap;fillColor={f.fond};strokeColor={f.trait};strokeWidth={TRAIT['composant']};"
            f"{police('detail', INK, 'center')}")


def style_flux(categorie="applicatif", prevu=False, fort=False, double=False, ortho=True) -> str:
    _, couleur = FLUX[categorie]
    largeur = TRAIT["flux_fort"] if fort else TRAIT["flux"]
    route = "edgeStyle=orthogonalEdgeStyle;rounded=1;" if ortho else "edgeStyle=none;"
    fleche = "startArrow=block;startFill=1;" if double else "startArrow=none;"
    return (f"{route}html=1;strokeColor={couleur};strokeWidth={largeur};{_tirets(prevu)}endArrow=block;endFill=1;"
            f"endSize=6;startSize=6;{fleche}jumpStyle=arc;jumpSize=8;labelBackgroundColor={CANVAS};"
            f"{police('flux', couleur, 'center')}")

# --------------------------------------------------------------------------- #
# Composants (assemblages réutilisables)                                       #
# --------------------------------------------------------------------------- #


def libelle(categorie: str, nom: str, detail: str = "", f: Famille = NEUTRE) -> str:
    t_cat, t_nom, t_det = TYPO["categorie"][0], TYPO["composant"][0], TYPO["detail"][0]
    html = ""
    if categorie:
        html += f'<span style="font-size:{t_cat}px;font-weight:bold;letter-spacing:0.6px;color:{f.texte}">{categorie.upper()}</span><br>'
    html += f'<span style="font-size:{t_nom}px;font-weight:bold;color:{INK}">{nom}</span>'
    if detail:
        html += f'<br><span style="font-size:{t_det}px;color:{MUTED}">{detail}</span>'
    return html


def composant(d: Diagramme, ident, x, y, l, h, f: Famille, icone, categorie, nom, detail="",
              prevu=False, parent=None, fond=None):
    """Carte : icône à gauche, catégorie, nom, détail. Taille libre, adaptée au contenu."""
    cid = d.forme(ident, x, y, l, h, libelle(categorie, nom, detail, f), style_carte(f, prevu, fond), parent)
    d.forme(f"{ident}-icone", PADDING, (h - ICONE) / 2, ICONE, ICONE, "", icone_style(icone, f.trait), cid)
    return cid


def machine(d: Diagramme, ident, x, y, l, h, nom, detail, icone="serveur", prevu=False, parent=None):
    titre = f'{nom}&nbsp;&nbsp;<span style="font-weight:normal;font-size:12px;color:{MUTED}">{detail}</span>'
    mid = d.forme(ident, x, y, l, h, titre, style_machine(prevu), parent, calque="frontieres")
    d.forme(f"{ident}-icone", 14, 8, 20, 20, "", icone_style(icone, SLATE), mid)
    return mid


def pastille(d: Diagramme, ident, x, y, l, texte, f: Famille = NEUTRE, plein=False, parent=None, h=24):
    return d.forme(ident, x, y, l, h, texte, style_pastille(f, plein), parent, calque="annotations")


def statut(d: Diagramme, ident, x, y, l, etat: str, parent=None):
    """Badge de statut, symbole dessiné + mot : la couleur n'est jamais seule porteuse du sens.

    Les symboles sont des formes, pas des caractères : un glyphe absent de la police s'afficherait mal.
    """
    genre, texte = etat
    f, plein = {"verifie": (DONNEES, True), "realise": (NEUTRE, False), "prevu": (NEUTRE, False),
                "echec": (SECURITE, True), "principe": (NEUTRE, False)}[genre]
    pid = d.forme(ident, x, y, l, 22, texte, style_pastille(f, plein) + "align=left;spacingLeft=24;",
                  parent, calque="annotations")
    if genre in ("verifie", "echec"):
        d.forme(f"{ident}-symbole", 6, 3, 16, 16, "", icone_style("valide" if genre == "verifie" else "echec", f.trait), pid)
    elif genre == "realise":
        d.forme(f"{ident}-symbole", 9, 7, 8, 8, "", f"ellipse;fillColor={SLATE};strokeColor=none;", pid)
    elif genre == "prevu":
        d.forme(f"{ident}-symbole", 8, 6, 10, 10, "", f"ellipse;fillColor=none;strokeColor={SLATE};strokeWidth=1.5;dashed=1;dashPattern=2 1.5;", pid)
    else:
        d.forme(f"{ident}-symbole", 7, 5, 12, 12, "", f"rhombus;fillColor=none;strokeColor={SLATE};strokeWidth=1.5;", pid)
    return pid


def titre(d: Diagramme, texte: str, sous_titre: str = "", x=MARGE_CANEVAS + 8, y=MARGE_CANEVAS, l=None):
    l = l or d.largeur - 2 * (MARGE_CANEVAS + 8)
    d.forme("titre", x, y, l, 28, texte, style_texte("titre", INK), calque="annotations")
    if sous_titre:
        d.forme("sous-titre", x, y + 30, l, 20, sous_titre, style_texte("sous_titre", MUTED), calque="annotations")


def legende(d: Diagramme, x, y, entrees, l=None):
    """Légende horizontale, limitée aux conventions réellement utilisées dans le schéma.

    entrees : liste de ("trait", categorie, prevu, texte) ou ("forme", style, texte) ou ("statut", etat, texte).
    """
    l = l or d.largeur - 2 * MARGE_CANEVAS
    d.forme("legende-fond", x, y, l, 44, "", f"rounded=1;arcSize=20;fillColor={CARD};strokeColor={RULE};", calque="annotations")
    cx = x + 16
    for i, e in enumerate(entrees):
        if e[0] == "trait":
            _, cat, prevu, texte = e
            d.trait_libre(f"legende-t{i}", cx, y + 22, cx + 34, y + 22, style_flux(cat, prevu, ortho=False))
            cx += 42
        elif e[0] == "forme":
            _, style, texte = e
            d.forme(f"legende-f{i}", cx, y + 12, 26, 20, "", style, calque="annotations")
            cx += 34
        else:
            _, etat, texte = e
            statut(d, f"legende-s{i}", cx, y + 11, 92, etat)
            cx += 100
            texte = texte or ""
        largeur = max(60, int(len(texte) * 6.4))
        d.forme(f"legende-x{i}", cx, y + 12, largeur, 20, texte, style_texte("note", INK), calque="annotations")
        cx += largeur + 22
    return cx


def bibliotheque(entrees: list[tuple[str, Diagramme, int, int]], chemin: Path) -> Path:
    """Bibliothèque Draw.io (Fichier > Bibliothèque > Ouvrir) : une entrée par composant."""
    items = [{"xml": d.xml(), "w": w, "h": h, "aspect": "fixed", "title": t} for t, d, w, h in entrees]
    chemin.write_text("<mxlibrary>" + json.dumps(items, ensure_ascii=False) + "</mxlibrary>", encoding="utf-8")
    return chemin
