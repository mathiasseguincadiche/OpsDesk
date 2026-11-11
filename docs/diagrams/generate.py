"""Generate matching editable draw.io and standalone SVG documentation diagrams."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parent
NAVY='#17385f'; BLUE='#17659b'; INK='#20334d'; TEAL='#e6f4f5'; BORDER='#a6bdcf'; ORANGE='#fff3db'

def generate(name,title,width,height,nodes,edges,description):
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(description)}</desc>',f'<rect width="{width}" height="{height}" fill="#f7fafc"/>','<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#39688a"/></marker></defs>',f'<text x="40" y="46" font-family="Arial,sans-serif" font-size="26" font-weight="700" fill="{NAVY}">{escape(title)}</text>']
    mxfile=ET.Element('mxfile',host='app.diagrams.net');diagram=ET.SubElement(mxfile,'diagram',id=name,name=title);model=ET.SubElement(diagram,'mxGraphModel',dx=str(width),dy=str(height),grid='1',gridSize='10',page='1',pageWidth=str(width),pageHeight=str(height),background='#f7fafc');root=ET.SubElement(model,'root');ET.SubElement(root,'mxCell',id='0');ET.SubElement(root,'mxCell',id='1',parent='0')
    title_cell=ET.SubElement(root,'mxCell',id='title',value=title,style=f'text;html=0;align=left;verticalAlign=middle;whiteSpace=wrap;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize=26;fontStyle=1;fontColor={NAVY};',vertex='1',parent='1');ET.SubElement(title_cell,'mxGeometry',x='40',y='20',width=str(width-80),height='40',attrib={'as':'geometry'})
    lookup={n['id']:n for n in nodes}
    for n in nodes:
        x,y,w,h=n['x'],n['y'],n['w'],n['h'];lines=n['lines'];fill=n.get('fill','#fff');dash=n.get('dash',False);container=n.get('container',False)
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{n.get("stroke",BORDER)}" stroke-width="{1.5 if container else 2}"'+(' stroke-dasharray="8 6"' if dash else '')+'/>')
        style=f'rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={n.get("stroke",BORDER)};fontColor={INK};fontFamily=Arial;fontSize={16 if container else 18};strokeWidth={1.5 if container else 2};'+('dashed=1;' if dash else '')+('verticalAlign=top;align=left;spacingTop=12;spacingLeft=16;' if container else 'align=center;')
        cell=ET.SubElement(root,'mxCell',id=n['id'],value='<b>'+escape(lines[0])+'</b>'+''.join('<br>'+escape(t) for t in lines[1:]),style=style,vertex='1',parent='1');ET.SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
        start=y+27 if container else y+(h-len(lines)*25)/2+18
        for i,line in enumerate(lines):
            svg.append(f'<text x="{x+(16 if container else w/2)}" y="{start+i*25}" text-anchor="{"start" if container else "middle"}" font-family="Arial,sans-serif" font-size="{16 if container else 18}" font-weight="{700 if i==0 else 400}" fill="{INK}">{escape(line)}</text>')
    for index,e in enumerate(edges):
        source,target=lookup[e['from']],lookup[e['to']];points=e.get('points')
        if not points:
            points=[(source['x']+source['w'],source['y']+source['h']/2),(target['x'],target['y']+target['h']/2)]
        pts=' '.join(f'{x},{y}' for x,y in points);svg.append(f'<polyline points="{pts}" fill="none" stroke="#39688a" stroke-width="2.2" marker-end="url(#arrow)"'+(' stroke-dasharray="6 5"' if e.get('dash') else '')+'/>')
        if e.get('label'):
            lx,ly=e.get('label_at',((points[0][0]+points[-1][0])/2,(points[0][1]+points[-1][1])/2-12));text=e['label'];bw=len(text)*8+14
            svg.append(f'<rect x="{lx-bw/2}" y="{ly-17}" width="{bw}" height="24" rx="4" fill="#f7fafc"/><text x="{lx}" y="{ly}" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" fill="{INK}">{escape(text)}</text>')
        anchors=f'exitX={(points[0][0]-source["x"])/source["w"]};exitY={(points[0][1]-source["y"])/source["h"]};entryX={(points[-1][0]-target["x"])/target["w"]};entryY={(points[-1][1]-target["y"])/target["h"]};exitPerimeter=0;entryPerimeter=0;'
        cell=ET.SubElement(root,'mxCell',id='edge'+str(index),value=e.get('label',''),style='edgeStyle=none;rounded=0;html=1;endArrow=block;endFill=1;fontFamily=Arial;fontSize=15;strokeColor=#39688a;labelBackgroundColor=#f7fafc;'+anchors+('dashed=1;' if e.get('dash') else ''),edge='1',parent='1',source=e['from'],target=e['to']);geo=ET.SubElement(cell,'mxGeometry',relative='1',attrib={'as':'geometry'});arr=ET.SubElement(geo,'Array',attrib={'as':'points'})
        for x,y in points[1:-1]:ET.SubElement(arr,'mxPoint',x=str(x),y=str(y))
        if e.get('label'):
            midpoint=((points[0][0]+points[-1][0])/2,(points[0][1]+points[-1][1])/2)
            ET.SubElement(geo,'mxPoint',x=str(lx-midpoint[0]),y=str(ly-midpoint[1]-5),attrib={'as':'offset'})
    svg.append('</svg>');(OUT/(name+'.svg')).write_text('\n'.join(svg)+'\n',encoding='utf8');ET.indent(mxfile,space='  ');ET.ElementTree(mxfile).write(OUT/(name+'.drawio'),encoding='utf-8',xml_declaration=True)

presentation=[
 {'id':'user','x':50,'y':120,'w':230,'h':120,'lines':['Collaborateur / équipe IT','Ouvrir une demande','Prendre en charge · clôturer'],'fill':'#fff'},
 {'id':'app','x':415,'y':105,'w':320,'h':150,'lines':['OpsDesk','Interface web + API','Démonstrateur métier fourni','Version locale 0.1.0'],'fill':TEAL},
 {'id':'db','x':865,'y':120,'w':280,'h':120,'lines':['PostgreSQL','Tickets et statuts','Données fictives persistantes'],'fill':'#fff'},
 {'id':'role','x':50,'y':315,'w':1095,'h':115,'lines':['Contributions et responsabilité personnelle','Codex : application, tests et contrat · Mathias : infrastructure, livraison et exploitation','Les preuves Codex ne valident aucun niveau personnel de Mathias.'],'fill':'#e9eff8'},
 {'id':'phase1','x':50,'y':495,'w':330,'h':145,'lines':['1. Recevoir l’application','Pages, API, règles et PostgreSQL','Tests applicatifs Codex : PASS','Contrat et preuves distinctes'],'fill':TEAL},
 {'id':'phase2','x':430,'y':495,'w':330,'h':145,'lines':['2. Construire personnellement','Linux · réseau · Terraform · Ansible','Énoncés et aides progressives','À FAIRE PAR MATHIAS'],'fill':ORANGE,'dash':True},
 {'id':'phase3','x':810,'y':495,'w':335,'h':145,'lines':['3. Livrer et exploiter','K3s · CI · signaux · diagnostic','Maintenance et reprise','À FAIRE PAR MATHIAS'],'fill':ORANGE,'dash':True},
]
generate('presentation','OpsDesk — un service utile, une progression InfraOps',1200,690,presentation,[{'from':'user','to':'app','label':'HTTP local'},{'from':'app','to':'db','label':'SQL'}],description='Vue pédagogique du service OpsDesk : application et base fournies ; infrastructure, livraison et exploitation personnelles à réaliser.')
technical=[
 {'id':'host','x':330,'y':85,'w':900,'h':580,'lines':['RÉFÉRENCE DEV CODEX V4.2 : Ubuntu / WSL2 · Compose'],'fill':'#eef3f9','container':True},
 {'id':'network','x':365,'y':205,'w':820,'h':190,'lines':['Réseau Docker v42opsdesk_net — DNS interne db'],'fill':'#f8fbfe','container':True},
 {'id':'browser','x':35,'y':250,'w':245,'h':115,'lines':['Navigateur du laboratoire','127.0.0.1:18081','Aucun accès public prévu'],'fill':'#fff'},
 {'id':'app','x':405,'y':255,'w':290,'h':115,'lines':['app :8000 · UID 10001','Gunicorn + Flask','live · ready · version · metrics'],'fill':TEAL},
 {'id':'db','x':875,'y':255,'w':265,'h':115,'lines':['db :5432','PostgreSQL 17.11','Rôle app : opsdesk_app'],'fill':'#fff'},
 {'id':'secrets','x':400,'y':460,'w':300,'h':115,'lines':['Secrets locaux hors Git','Mot de passe DB applicatif','Secret session / propriétaire'],'fill':'#fff'},
 {'id':'volume','x':865,'y':460,'w':300,'h':115,'lines':['Volume v42opsdesk_pgdata','Fichiers PostgreSQL','Un volume ≠ une sauvegarde'],'fill':'#fff'},
 {'id':'future','x':45,'y':720,'w':1175,'h':100,'lines':['EXERCICES PERSONNELS — À CONCEVOIR ET RÉALISER PAR MATHIAS','Rocky/KVM · K3s · CI distante · Prometheus/Grafana · reprise contrôlée'],'fill':ORANGE,'dash':True},
]
edges=[
 {'from':'browser','to':'app','label':'HTTP local','label_at':(342,292)},
 {'from':'app','to':'db','label':'DNS db / TCP 5432','label_at':(785,295)},
 {'from':'secrets','to':'app','points':[(550,460),(550,370)],'dash':True,'label':'fichiers montés','label_at':(550,420)},
 {'from':'db','to':'volume','points':[(1007,370),(1007,460)],'label':'écritures durables','label_at':(1055,425)},
]
generate('architecture-technique','OpsDesk — chemin réseau, données et frontières du lab',1280,860,technical,edges,description='Architecture historique du laboratoire de développement Codex sous Ubuntu/WSL2 et Docker Compose ; laboratoire personnel Fedora/KVM/Rocky non encore exécuté.')
print('Generated two editable draw.io files and two matching SVG files.')
