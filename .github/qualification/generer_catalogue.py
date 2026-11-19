"""Catalogue V25 et bibliothèque de composants : utilise les jetons du kit."""
from pathlib import Path
import sys
from systeme_graphique import *

def catalogue(p):
    W,H=1200,980
    d=Diagramme("catalogue",W,H)
    d.forme("canevas",0,0,W,H,"",style_canevas(),calque="fond")
    titre(d,"Système graphique V25","Composants, icônes, formes et conventions à réutiliser selon le sujet.")
    def en_tete(ident,y,texte):
        d.forme(ident,32,y,1136,24,texte,style_texte("categorie",MUTED),calque="annotations")
    en_tete("t-familles",96,"FAMILLES · LA COULEUR EST DOUBLÉE D'UN LIBELLÉ")
    icones=["navigateur","api","base","script","mesures","sauvegarde","bouclier","serveur"]
    for i,(f,ic) in enumerate(zip(FAMILLES,icones)):
        composant(d,f"famille-{i}",32+(i%4)*288,124+(i//4)*76,272,64,f,ic,f.nom,f.trait,f"texte {f.texte}")
    en_tete("t-icones",292,"ICÔNES · TRAIT 1,75 · GRILLE 24")
    for i,nom in enumerate(NOMS_ICONES):
        x,y=32+(i%11)*104,324+(i//11)*76
        d.forme("icone-"+nom,x+36,y,28,28,"",icone_style(nom,SLATE))
        d.forme("icone-"+nom+"-nom",x,y+32,100,22,nom.replace("_"," "),style_texte("note",MUTED,"center"),calque="annotations")
    y=560
    en_tete("t-formes",y,"FORMES · CHAQUE FORME A UNE FONCTION")
    d.forme("forme-zone",32,y+32,240,120,"ZONE · VRAIE FRONTIÈRE",style_zone(),calque="frontieres")
    machine(d,"forme-machine",288,y+32,240,120,"Machine","nom · adresse")
    d.forme("forme-regroupement",544,y+32,200,120,"REGROUPEMENT PÉDAGOGIQUE",style_regroupement(),calque="frontieres")
    d.forme("forme-cylindre",760,y+32,120,96,"<b>Base</b><br>données",style_cylindre(DONNEES))
    d.forme("forme-document",896,y+32,128,96,"<b>Fichier</b><br>configuration",style_document(AUTOMATISATION))
    d.forme("forme-decision",1040,y+32,128,96,"Décision ?",style_losange(TRAITEMENT))
    y=736
    en_tete("t-flux",y,"FLUX · COULEUR = NATURE · TRAIT = AVANCEMENT")
    for i,(cat,(nom,_)) in enumerate(FLUX.items()):
        x=32+i*288
        d.trait_libre("flux-"+cat+"-r",x,y+44,x+80,y+44,style_flux(cat,ortho=False))
        d.trait_libre("flux-"+cat+"-p",x,y+72,x+80,y+72,style_flux(cat,prevu=True,ortho=False))
        d.forme("flux-"+cat+"-nom",x+92,y+34,190,52,f"<b>{nom}</b><br>plein : réalisé<br>pointillé : prévu",style_texte("note",INK),calque="annotations")
    y=860
    en_tete("t-statuts",y,"STATUTS · SYMBOLE ET MOT, JAMAIS SEULEMENT LA COULEUR")
    for i,etat in enumerate([("verifie","Vérifié · date"),("realise","Réalisé · non vérifié"),("prevu","Prévu"),("echec","Échec constaté"),("principe","Schéma de principe")]):
        statut(d,"statut-"+etat[0],32+i*232,y+32,216,etat)
    return d.enregistrer(p)

def bibliotheque_drawio(p):
    entrees=[]
    def entree(t,l,h,fn):
        d=Diagramme("entree",l,h);fn(d);entrees.append((t,d,l,h))
    for f,ic in zip(FAMILLES,["navigateur","api","base","script","mesures","sauvegarde","bouclier","serveur"]):
        entree(f"Composant · {f.nom}",216,64,lambda d,f=f,ic=ic:composant(d,"c",0,0,216,64,f,ic,"catégorie","Nom","détail"))
    entree("Machine",320,200,lambda d:machine(d,"m",0,0,320,200,"srv-nom","adresse · rôle"))
    entree("Machine prévue",320,200,lambda d:machine(d,"m",0,0,320,200,"srv-nom","adresse · rôle",prevu=True))
    entree("Zone (frontière)",400,240,lambda d:d.forme("z",0,0,400,240,"ZONE",style_zone()))
    entree("Regroupement pédagogique",400,200,lambda d:d.forme("r",0,0,400,200,"REGROUPEMENT",style_regroupement()))
    entree("Base de données",140,100,lambda d:d.forme("b",0,0,140,100,"<b>Base</b>",style_cylindre(DONNEES)))
    entree("Fichier",200,120,lambda d:d.forme("f",0,0,200,120,"<b>fichier.ext</b>",style_document(AUTOMATISATION)))
    entree("Décision",140,100,lambda d:d.forme("q",0,0,140,100,"Question ?",style_losange(TRAITEMENT)))
    for etat in [("verifie","Vérifié · date"),("realise","Réalisé"),("prevu","Prévu"),("echec","Échec constaté"),("principe","Schéma de principe")]:
        entree(f"Statut · {etat[1]}",200,24,lambda d,etat=etat:statut(d,"s",0,0,200,etat))
    for nom in NOMS_ICONES:
        entree(f"Icône · {nom}",24,24,lambda d,nom=nom:d.forme("i",0,0,24,24,"",icone_style(nom,SLATE)))
    return bibliotheque(entrees,p/"bibliotheque-v25.xml")

if __name__=="__main__":
    p=Path(sys.argv[1] if len(sys.argv)>1 else "03_MODELES/schemas")
    p.mkdir(parents=True,exist_ok=True)
    print(catalogue(p));print(bibliotheque_drawio(p))
