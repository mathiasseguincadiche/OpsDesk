import pathlib, xml.etree.ElementTree as ET, subprocess, shutil, html, json, tempfile, os
from urllib.parse import quote
p=pathlib.Path("docs/diagrams")
out=pathlib.Path("/tmp/recette-schemas")
out.mkdir(exist_ok=True)
chrome=shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
assert chrome, "Navigateur indisponible"
sources=sorted(p.glob("*.drawio"))
assert len(sources)==13 and len(list(p.glob("*.svg")))==13
for src in sources:
    root=ET.parse(src).getroot()
    cells=list(root.iter("mxCell"))
    ids=[c.attrib["id"] for c in cells if "id" in c.attrib]
    assert len(ids)==len(set(ids)), src
    for c in cells:
        for k in ("parent","source","target"):
            assert k not in c.attrib or c.attrib[k] in ids,(src,k,c.attrib.get(k))
    svg=src.with_suffix(".svg")
    r=ET.parse(svg).getroot()
    _,_,w,h=map(float,r.attrib["viewBox"].split())
    assert w>0 and h>0
    width=375 if "mobile" in src.stem else (950 if src.stem in ("architecture","presentation") else 700)
    height=int(h*width/w+0.9999)
    for mode,color in (("clair","#ffffff"),("sombre","#0d1117")):
        page=out/(src.stem+"-"+mode+".html")
        dst=page.with_suffix(".png")
        page.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:'+color+'}img{display:block;width:'+str(width)+'px;height:auto}</style><img src="'+svg.resolve().as_uri()+'">',encoding="utf-8")
        subprocess.run([chrome,"--headless","--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--hide-scrollbars","--window-size="+str(width)+","+str(height),"--screenshot="+str(dst),page.as_uri()],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        page.unlink()
    print(src.stem, len(cells), "cellules", width, "x", height, "px, 2 rendus")
