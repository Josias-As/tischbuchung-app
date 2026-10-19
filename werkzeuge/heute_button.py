# Knopf „Heute“ (19.10.2026): setzt das Ansichtsdatum (Dashboard-Liste, Grundriss, Vorgabe in Dialog/Panel) mit einem Klick auf heute.
# Grundlage: Desktop-Export 19.10. 10:35 (quellen/2026-10-19_HeuteButton/). Ein neues Steuerelement, sonst keine Änderung.
# Aufruf: python3 -I werkzeuge/heute_button.py -> arbeit/2026-10-19_HeuteButton/
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_1910()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-19_HeuteButton")
os.makedirs(ZIEL, exist_ok=True)
fehler, notiz = [], []
NAME = "btnHeuteDatum"

# OnSelect = dpAnsichtsDatum.OnChange, nur die erste Anweisung ersetzt (Ladezeile bleibt zeichengleich)
oc = ist["dpAnsichtsDatum.OnChange"]
ERSTE = "Set(varAnsichtsDatum, dpAnsichtsDatum.SelectedDate);\n"
if not oc.startswith(ERSTE):
    fehler.append("dpAnsichtsDatum.OnChange beginnt anders als erwartet")
rest = oc[len(ERSTE):]
lade = ist["App.OnStart"][ist["App.OnStart"].index("Set(varFreigabeGrenze, DateAdd(Now(), -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes));\nWith({neu"):]
lade = lade[:lade.index("\n", lade.index("With({neu"))]
if rest.strip() != lade.strip().rstrip(";"):   # in OnStart folgt noch eine Anweisung, daher dort mit ;
    fehler.append("Ladezeile in dpAnsichtsDatum.OnChange weicht von App.OnStart ab")
FREI = "!varIsLoading && !varZeigeDialog && !varZeigeVerwalten && !varZeigeCheckin"
onselect = ("If(\n  " + FREI + ",\n"
            "  Set(varAnsichtsDatum, Today());\n"
            "  Reset(dpAnsichtsDatum);\n"
            "  Set(varZeigeDetails, false);\n"
            + "\n".join("  " + z for z in rest.strip().split("\n")) + "\n)")
T = "Coalesce(varJetztTakt, Now())"
HEUTE = f"Date(Year({T}), Month({T}), Day({T}))"

neu = {
    "Text": '"Heute"',
    "X": "Image4.X + Image4.Width + 5",
    "Y": "dpAnsichtsDatum.Y + (dpAnsichtsDatum.Height - Self.Height) / 2",
    "Width": "90",
    "Height": "32",
    "Font": "Font.'Open Sans'",
    "Size": "12",
    "FontWeight": "FontWeight.Semibold",
    "Fill": 'ColorValue("#171496")',
    "Color": "RGBA(255, 255, 255, 1)",
    "HoverFill": "ColorFade(Self.Fill, -20%)",
    "HoverColor": "RGBA(255, 255, 255, 1)",
    "PressedFill": "ColorFade(Self.Fill, -30%)",
    "PressedColor": "RGBA(255, 255, 255, 1)",
    "BorderThickness": "0",
    "DisabledFill": 'ColorFade(ColorValue("#171496"), 50%)',
    "DisabledColor": "RGBA(255, 255, 255, 1)",
    "RadiusTopLeft": "10", "RadiusTopRight": "10", "RadiusBottomLeft": "10", "RadiusBottomRight": "10",
    "Visible": f"varAnsichtsDatum <> {HEUTE}",
    "DisplayMode": f"If({FREI}, DisplayMode.Edit, DisplayMode.Disabled)",
    "AccessibleLabel": '"Datum auf heute zurücksetzen"',
    "OnSelect": onselect,
}

# --- Prüfungen -------------------------------------------------------------------------------------------------------
if NAME in f.typ:
    fehler.append(f"{NAME} gibt es schon")
gesetzt = {m.group(1) for v in ist.values() for m in re.finditer(r"Set\(\s*(var\w+)", v)}
for p, v in neu.items():
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{p}: Klammern/Rückübersetzung")
    o = A.ausserhalb_strings(v)
    if "//" in o:
        fehler.append(f"{p}: Kommentar")
    for x in set(re.findall(r"\b(var\w+)", o)):
        if x not in gesetzt:
            fehler.append(f"{p}: {x} wird nirgends gesetzt")
    for c in set(re.findall(r"\b([A-Za-zÄÖÜäöü]\w*)\.(?:X|Y|Width|Height|SelectedDate)\b", o)) - {"Self", "Parent"}:
        if c not in f.typ:
            fehler.append(f"{p}: Steuerelement {c} fehlt")
        elif f.eltern.get(c) != "conDashboard":
            fehler.append(f"{p}: {c} liegt nicht in conDashboard")
onselect = neu["OnSelect"]   # Prüfungen immer am auszuliefernden Text
if onselect.count("ClearCollect(colGrundriss") != 1 or "Set(varGrundrissStand, Now())" not in onselect or rest.strip() not in onselect.replace("\n  ", "\n"):
    fehler.append("OnSelect: Ladezeile/Stempel fehlt")
if re.search(r"(Patch|Remove|Collect)\(\s*Tischbuchungen", onselect):
    fehler.append("OnSelect schreibt")
if neu["DisplayMode"].count(FREI) != 1 or onselect.count(FREI) != 1:
    fehler.append("Freigabe-Bedingung nicht in DisplayMode und OnSelect gleich")
# Wer liest varAnsichtsDatum? -> alles, was der Knopf mit umstellt
leser = sorted(k for k, v in ist.items() if "varAnsichtsDatum" in A.ausserhalb_strings(v) and not re.search(r"Set\(varAnsichtsDatum", v))
notiz.append("varAnsichtsDatum lesen (stellen sich mit um): " + ", ".join(leser))
for k in ("dpDatum.DefaultDate", "dpDatumTischePanel.DefaultDate", "galTischbuchungenHeute.Items", "Label16.Text"):
    if k not in leser:
        fehler.append(f"{k} liest varAnsichtsDatum nicht (Annahme falsch)")
schreiber = sorted(k for k, v in ist.items() if re.search(r"Set\(varAnsichtsDatum|Reset\(dpAnsichtsDatum", v))
notiz.append("varAnsichtsDatum/dpAnsichtsDatum schreiben bisher: " + ", ".join(schreiber))
if ist.get("dpAnsichtsDatum.DefaultDate") is not None:
    fehler.append("dpAnsichtsDatum.DefaultDate ist gesetzt -> Reset ergibt nicht heute")
notiz.append("dpAnsichtsDatum.DefaultDate nicht gesetzt (Standard Today()) -> Reset(dpAnsichtsDatum) zeigt heute")
# Lage: rechts von Image4, oberhalb von lblMyPersonalDesk (Y 75), innerhalb von conDashboard (Breite 470)
y0 = 24 + (51 - 32) / 2
if not (int(ist["dpAnsichtsDatum.Y"]) == 24 and int(ist["dpAnsichtsDatum.Height"]) == 51 and int(ist["lblMyPersonalDesk.Y"]) == 75):
    fehler.append("Lagewerte im Export anders als angenommen")
if y0 + 32 > 75:
    fehler.append("Knopf überlappt lblMyPersonalDesk")
notiz.append(f"Lage: Y {y0:g}–{y0 + 32:g} (lblMyPersonalDesk ab 75), X = Image4.X + Image4.Width + 5 = 85 + Image4.Width + 5 (Image4.Width im Export Standard, nicht gesetzt)")
if 85 + 150 + 5 + 90 > int(ist["conDashboard.Width"]):
    fehler.append("Knopf ragt aus conDashboard (bei Image4.Width bis 150)")


def lum(r, g, b):
    def k(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * k(r) + 0.7152 * k(g) + 0.0722 * k(b)


m = re.fullmatch(r'ColorValue\("#([0-9A-Fa-f]{6})"\)', neu["Fill"])
rgb = tuple(int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4)) if m else tuple(int(x) for x in re.findall(r"\d+", neu["Fill"])[:3])
if neu["Color"] != "RGBA(255, 255, 255, 1)":
    fehler.append("Kontrastprüfung erwartet weiße Schrift")
k1 = (lum(255, 255, 255) + 0.05) / (lum(*rgb) + 0.05)
notiz.append(f"Kontrast Weiß auf Fill {rgb}: {k1:.1f}:1")
if k1 < 4.5:
    fehler.append("Kontrast zu gering")
notiz.append("Textbreite „Heute“ bei Größe 12 halbfett ca. 45 (geschätzt) < 90")

out = [dict(control=NAME, prop=p, neu=v, de=A.to_de(v)) for p, v in neu.items()]
json.dump(dict(app=out, onchange_vorher_de=A.to_de(oc)), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"Knopf {NAME}: {len(out)} Properties, 1 neues Steuerelement in conDashboard. Grundlage: Export 19.10. 10:35."] + notiz
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
