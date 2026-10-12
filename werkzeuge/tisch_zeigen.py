# Tisch zeigen (Handy, 12.10.2026): Grundriss-Bilder mit eingezeichneten Tischen und Positionstabelle in Anteilen (0–1).
# Quelle: Desktop-Export 12.10. (colTischPositionen/colTischPositionenUG in App.OnStart, Kachelmaße in App.Formulas, Bilder in Assets).
# Aufruf: python3 -I werkzeuge/tisch_zeigen.py -> arbeit/2026-10-12_TischZeigen/
import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A
from PIL import Image, ImageDraw, ImageFont

f = A.lade_desktop_1210()
ROOT = os.path.join(A.ENTPACKT, "desktop_2026-10-12")
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-12_TischZeigen")
os.makedirs(ZIEL, exist_ok=True)
o = f.props["App.OnStart"]
fo = f.props["App.Formulas"]


def konst(name):
    m = re.search(rf"\b{name}\s*=\s*(\d+)\s*;", fo)
    assert m, name
    return int(m.group(1))


def tabelle(name):
    i = o.index("ClearCollect(\n  " + name + ",")
    j = o.index(");", i)
    t = [dict(Tisch=m[0], X=int(m[1]), Y=int(m[2]), Ausrichtung=m[3]) for m in
         re.findall(r'\{Tisch: "([^"]+)",\s*X: (\d+),\s*Y: (\d+),\s*Ausrichtung: "(\w+)"\}', o[i:j])]
    assert t and len(t) == o[i:j].count("{Tisch:"), name
    return t


# Belegt: Bild-Steuerelemente sind BasisBreite x BasisHoehe (1920 x 1080) * Skalierung, Bilder 1920 x 1080, ImagePosition.Fit
assert konst("BasisBreite") == 1920 and konst("BasisHoehe") == 1080
assert "BasisSkalierungReferenz = Min(881 / BasisBreite, 678 / BasisHoehe);" in fo
SREF = min(881 / 1920, 678 / 1080)
assert f.props["Gallery1.TemplateSize"] == "1"   # TemplatePadding 0 (Controls/4.json) -> Versatz je Eintrag 1 / SREF
GROESSE = {
    "OG": {"Horizontal": (konst("BasisKachelbreiteQuer"), konst("BasisKachelhoeheQuer")),
           "Vertikal": (konst("BasisKachelbreiteHoch"), konst("BasisKachelhoeheHoch"))},
    "UG": {"Horizontal": (konst("BasisKachelbreiteQuerUG"), konst("BasisKachelhoeheQuerUG")),
           "Vertikal": (konst("BasisKachelbreiteHochUG"), konst("BasisKachelhoeheHochUG"))},
}
BIG = (konst("BasisKachelbreiteBigTableUG"), konst("BasisKachelhoeheQuerUG"))
res = json.load(open(os.path.join(ROOT, "References/Resources.json"), encoding="utf-8-sig"))["Resources"]
BILD = {}
for g, ctrl in [("OG", "imgGrundrissOG"), ("UG", "imgGrundrissUG")]:
    name = f.props[f"{ctrl}.Image"].strip("'")
    r = next(x for x in res if x.get("Name") == name)
    BILD[g] = (name, os.path.join(ROOT, r["Path"].replace("\\", "/")))

CROP = (60, 200, 1860, 920)   # Gebäude in beiden Bildern, weißer Rand weg (geprüft am Bild)
CW, CH = CROP[2] - CROP[0], CROP[3] - CROP[1]


def kurz(t):
    return t.replace("OG Desk ", "").replace("UG Desk ", "").replace("Quiet Desk ", "Q").replace("Big Table", "Big Table")


try:
    FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except OSError:
    FONT = ImageFont.load_default()

daten, info = {}, {}
for g, tab in [("OG", tabelle("colTischPositionen")), ("UG", tabelle("colTischPositionenUG"))]:
    zeilen = []
    for n, t in enumerate(tab):
        w, h = BIG if t["Tisch"] == "Big Table" else GROESSE[g][t["Ausrichtung"]]
        if t["Tisch"].startswith("Quiet Desk"):
            w, h = w - 10, h - 7
        x, y = t["X"], t["Y"] + n / SREF          # Galerie-Versatz (Rectangle1.Y): Reihenfolge = Tabelle (geschlussfolgert)
        assert CROP[0] <= x and x + w <= CROP[2] and CROP[1] <= y and y + h <= CROP[3], t
        zeilen.append(dict(Tisch=t["Tisch"], Geschoss=g, px=(x - CROP[0], y - CROP[1], w, h)))
    # Bilder
    im = Image.open(BILD[g][1]).convert("RGBA")
    bg = Image.new("RGBA", im.size, "white")
    bg.alpha_composite(im)
    bild = bg.crop(CROP)
    d = ImageDraw.Draw(bild)
    for z in zeilen:
        x, y, w, h = z["px"]
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(60, 60, 60), width=3)
        tx = kurz(z["Tisch"])
        bb = d.textbbox((0, 0), tx, font=FONT)
        d.text((x + (w - (bb[2] - bb[0])) / 2, y + (h - (bb[3] - bb[1])) / 2 - bb[1]), tx, fill=(60, 60, 60), font=FONT)
    for lage, b in [("quer", bild), ("hoch", bild.rotate(-90, expand=True))]:
        rgb = b.convert("RGB")
        for q in (80, 70, 60):
            buf = io.BytesIO(); rgb.save(buf, "JPEG", quality=q, optimize=True)
            if buf.tell() <= 200_000:
                break
        p = os.path.join(ZIEL, f"tischplan_{g}_{lage}.jpg")
        open(p, "wb").write(buf.getvalue())
        info[f"{g}_{lage}"] = dict(datei=os.path.basename(p), groesse_px=rgb.size, kb=round(buf.tell() / 1024), qualitaet=q)
    daten[g] = zeilen

# Anteile: quer (x/W, y/H) und hoch (Bild 90° im Uhrzeigersinn gedreht: x' = H - y - h, y' = x)
zeilen = []
for g in ("OG", "UG"):
    for z in daten[g]:
        x, y, w, h = z["px"]
        zeilen.append(dict(Tisch=z["Tisch"], Geschoss=g,
                           quer=dict(X=round(x / CW, 4), Y=round(y / CH, 4), B=round(w / CW, 4), H=round(h / CH, 4)),
                           hoch=dict(X=round((CH - y - h) / CH, 4), Y=round(x / CW, 4), B=round(h / CH, 4), H=round(w / CW, 4))))
# Kontrolle: Hoch-Anteile auf das gedrehte Bild zurückgerechnet = gleiche Pixel
for z in zeilen:
    q, hq = z["quer"], z["hoch"]
    assert abs(hq["Y"] - q["X"]) < 1e-3 and abs(hq["X"] - (1 - q["Y"] - q["H"])) < 1e-3
json.dump(dict(crop=CROP, bild_quer=(CW, CH), bild_hoch=(CH, CW), sref=SREF, bilder=info, quelle={g: BILD[g][0] for g in BILD}, tische=zeilen),
          open(os.path.join(ZIEL, "tischplan_positionen.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def tabelle_fx(lage):
    teile = [f'{{Tisch: "{z["Tisch"]}", Geschoss: "{z["Geschoss"]}", X: {z[lage]["X"]}, Y: {z[lage]["Y"]}, B: {z[lage]["B"]}, H: {z[lage]["H"]}}}'
             for z in zeilen]
    return "Table(\n  " + ",\n  ".join(teile) + "\n)"


for lage in ("hoch", "quer"):
    fx = tabelle_fx(lage)
    assert A.klammern_ok(fx) and A.from_de(A.to_de(fx)) == fx
    open(os.path.join(ZIEL, f"tabelle_{lage}_de.txt"), "w", encoding="utf-8").write(A.to_de(fx) + "\n")
print(json.dumps(info, indent=1))
print(len(zeilen), "Tische")
