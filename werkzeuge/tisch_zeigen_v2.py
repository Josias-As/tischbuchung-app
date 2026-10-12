# Tisch zeigen v2 (12.10.2026): Gegenprüfung der Handy-Chat-Tabelle (tabelle_handy_de.txt) und Bilder.
# Quelle: Desktop-Export 12.10. 11:52 (Grundrissemachen) + echte SharePoint-Reihenfolge (tische_reihenfolge_2026-10-12.json).
# Aufruf: python3 -I werkzeuge/tisch_zeigen_v2.py -> arbeit/2026-10-12_TischZeigen2/
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A
from PIL import Image, ImageDraw

d = A.lade_desktop_1210b()
P = os.path.join(A.REPO, "quellen/2026-10-12_TischZeigen/paket")
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-12_TischZeigen2")
os.makedirs(ZIEL, exist_ok=True)
o, fo = d.props["App.OnStart"], d.props["App.Formulas"]


def konst(n):
    return int(re.search(rf"\b{n}\s*=\s*(\d+)\s*;", fo).group(1))


def tabelle(name):
    i = o.index("ClearCollect(\n  " + name + ","); j = o.index(");", i)
    t = re.findall(r'\{Tisch: "([^"]+)",\s*X: (\d+),\s*Y: (\d+),\s*Ausrichtung: "(\w+)"\}', o[i:j])
    assert len(t) == o[i:j].count("{Tisch:")
    return {m[0]: (int(m[1]), int(m[2]), m[3]) for m in t}


SREF = min(881 / 1920, 678 / 1080)
assert "BasisSkalierungReferenz = Min(881 / BasisBreite, 678 / BasisHoehe);" in fo and d.props["Gallery1.TemplateSize"] == "1"
G = {"OG": {"Horizontal": (konst("BasisKachelbreiteQuer"), konst("BasisKachelhoeheQuer")), "Vertikal": (konst("BasisKachelbreiteHoch"), konst("BasisKachelhoeheHoch"))},
     "UG": {"Horizontal": (konst("BasisKachelbreiteQuerUG"), konst("BasisKachelhoeheQuerUG")), "Vertikal": (konst("BasisKachelbreiteHochUG"), konst("BasisKachelhoeheHochUG"))}}
BIG = (konst("BasisKachelbreiteBigTableUG"), konst("BasisKachelhoeheQuerUG"))
pos = {"OG": tabelle("colTischPositionen"), "UG": tabelle("colTischPositionenUG")}
reihe = json.load(open(os.path.join(P, "tische_reihenfolge_2026-10-12.json"), encoding="utf-8-sig"))
CROP = (60, 200, 1860, 920); CW, CH = 1800, 720
fehler, eigene = [], {}
for g in ("OG", "UG"):
    ids = [t for _, t, gg in sorted(reihe) if gg == g]
    if sorted(ids) != sorted(pos[g]):
        fehler.append(f"{g}: Reihenfolge-Datei und Positionstabelle haben andere Tische: {set(ids) ^ set(pos[g])}")
    for n, t in enumerate(ids):
        if t not in pos[g]:
            continue
        x, y, a = pos[g][t]
        w, h = BIG if t == "Big Table" else G[g][a]
        if t.startswith("Quiet Desk"):
            w, h = w - 10, h - 7
        y = y + n / SREF
        x, y = x - CROP[0], y - CROP[1]
        eigene[t] = dict(Geschoss=g, X=(CH - y - h) / CH, Y=x / CW, B=h / CH, H=w / CW)
# Tabelle des Handy-Chats lesen (deutsche Schreibweise)
txt = open(os.path.join(P, "tabelle_handy_de.txt"), encoding="utf-8-sig").read()
en = A.from_de(txt.strip())
assert A.klammern_ok(en)
zeilen = re.findall(r'\{Tisch: "([^"]+)", Geschoss: "(\w+)", X: ([\d.]+), Y: ([\d.]+), B: ([\d.]+), H: ([\d.]+)\}', en)
assert len(zeilen) == en.count("{Tisch:"), "Tabelle nicht vollständig gelesen"
hc = {z[0]: dict(Geschoss=z[1], X=float(z[2]), Y=float(z[3]), B=float(z[4]), H=float(z[5])) for z in zeilen}
abw = []
for t in sorted(set(hc) | set(eigene)):
    if t not in hc or t not in eigene:
        fehler.append(f"{t}: nur in {'Handy-Chat' if t in hc else 'Nachrechnung'}"); continue
    for k in ("X", "Y", "B", "H"):
        if abs(hc[t][k] - eigene[t][k]) > 0.0006:
            abw.append(f"{t}.{k}: Handy-Chat {hc[t][k]} / nachgerechnet {eigene[t][k]:.4f}")
    if hc[t]["Geschoss"] != eigene[t]["Geschoss"]:
        fehler.append(f"{t}: Geschoss")
fehler += abw
# Bilder: Rechtecke der Handy-Chat-Tabelle auf deren Bilder legen (Sichtprüfung) + Seitenverhältnis
for g in ("OG", "UG"):
    im = Image.open(os.path.join(P, f"handy_plan_{g}.jpg")).convert("RGB")
    W, H = im.size
    if (W, H) != (720, 1800):
        fehler.append(f"handy_plan_{g}.jpg: Größe {W}x{H} statt 720x1800")
    dr = ImageDraw.Draw(im)
    for t, p in hc.items():
        if p["Geschoss"] == g:
            dr.rectangle([p["X"] * W, p["Y"] * H, (p["X"] + p["B"]) * W, (p["Y"] + p["H"]) * H], outline=(255, 120, 0), width=5)
    im.resize((W // 2, H // 2)).save(os.path.join(ZIEL, f"pruef_overlay_{g}.png"))
json.dump(dict(handy_chat=hc, nachgerechnet=eigene), open(os.path.join(ZIEL, "tabelle_gegenpruefung.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"Tische: Handy-Chat {len(hc)}, nachgerechnet {len(eigene)} (Desktop-Export 12.10. 11:52, Reihenfolge per REST).",
     "Vergleich je Wert mit Toleranz 0,0006 (Rundung auf 4 Stellen)."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Gegenprüfung: 0 Abweichungen"]
open(os.path.join(ZIEL, "pruefung_tabelle.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
