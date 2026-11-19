"""Compositions génériques V25. Exemples fictifs, indépendants d'OpsDesk."""
from pathlib import Path
import sys
from systeme_graphique import *

def sequence(dossier):
    d=Diagramme("sequence-requete", 760, 600)
    d.forme("fond",0,0,760,600,"",style_canevas(),calque="fond")
    titre(d,"Le trajet d'une requête HTTP","Exemple fictif : quatre composants et deux issues possibles.")
    statut(d,"principe",552,24,184,("principe","Schéma de principe"))
    xs=[95,285,475,665]
    for x,(i,f,ic,nom,detail) in zip(xs,[("client",ACCES,"navigateur","Client","navigateur"),("proxy",ACCES,"reseau","Proxy","point d'entrée"),("app",TRAITEMENT,"api","Service","API"),("db",DONNEES,"base","Base","données")]):
        composant(d,i,x-78,88,156,60,f,ic,"",nom,detail)
        d.trait_libre(i+"-vie",x,148,x,530,f"endArrow=none;strokeColor={RULE};strokeWidth=1.5;dashed=1;dashPattern=2 4;")
    def message(i,a,b,y,texte,retour=False):
        xa,xb=xs[a],xs[b]; sens=1 if xb>xa else -1
        st=style_flux("applicatif",ortho=False)+("dashed=1;dashPattern=4 3;strokeWidth=1.25;" if retour else "")
        d.trait_libre("m"+str(i),xa+sens*4,y,xb-sens*4,y,st,calque="flux")
        d.forme("txt"+str(i),min(xa,xb)+8,y-32,abs(xb-xa)-16,28,texte,style_texte("flux",SLATE,"center"),calque="annotations")
    message(1,0,1,206,"1 · GET /items")
    message(2,1,2,254,"2 · relaie la requête")
    message(3,2,3,302,"3 · envoie la requête SQL")
    message(4,3,2,350,"4 · lignes retournées",True)
    message(5,2,1,398,"5 · 200 + JSON",True)
    message(6,1,0,446,"6 · réponse au client",True)
    d.forme("limite",24,548,712,38,"Si la base ne répond pas, le service doit signaler l'échec : le code exact dépend de son contrat. Pointillés courts = réponses, pas statut d'avancement.",style_texte("note",INK),calque="annotations")
    return d.enregistrer(dossier)

def diagnostic(dossier):
    d=Diagramme("diagnostic-service",760,700)
    d.forme("fond",0,0,760,700,"",style_canevas(),calque="fond")
    titre(d,"Diagnostiquer un service indisponible","Hypothèses à vérifier, pas des causes déjà démontrées.")
    statut(d,"principe",552,24,184,("principe","Schéma de principe"))
    composant(d,"signal",104,88,320,60,SECURITE,"alerte","","Reproduire le symptôme","heure, cible, version")
    for i,q,y,f,c,detail in [
        ("q1","L'entrée<br>répond ?",176,INFRA,"Accès / réseau","nom, port, TLS, proxy"),
        ("q2","Le processus<br>répond ?",320,TRAITEMENT,"Service","état, journaux, sonde"),
        ("q3","Les dépendances<br>sont prêtes ?",464,DONNEES,"Dépendances","base, chemin réseau, droits")
    ]:
        d.forme(i,184,y,160,108,q,style_losange(TRAITEMENT))
        composant(d,"c"+i,448,y+20,288,68,f,"mesures","","Hypothèse : "+c,detail)
        d.lien("non"+i,i,"c"+i,"non",style_flux("applicatif")+"exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
    d.lien("debut","signal","q1","",style_flux("applicatif")+"exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    composant(d,"metier",104,608,320,60,ACCES,"valide","","Tester le parcours métier","une correction, puis recontrôle")
    for a,b in [("q1","q2"),("q2","q3"),("q3","metier")]:
        d.lien("oui"+a,a,b,"oui",style_flux("applicatif")+"exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    d.forme("rappel",448,608,288,60,"Ne pas redémarrer au hasard. Un signal oriente une investigation.",style_texte("note",INK),calque="annotations")
    return d.enregistrer(dossier)

if __name__=="__main__":
    p=Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=True)
    for fn in (sequence,diagnostic): print(fn(p))
