# Handy „Tisch zeigen“ (12.10.2026): alle Properties gegen den echten Handy-Export 12.10. 12:05 („handy echt“).
# Daten: Tabelle und Bilder des Handy-Chats (quellen/2026-10-12_TischZeigen/paket), gegengeprüft mit werkzeuge/tisch_zeigen_v2.py.
# Aufruf: python3 -I werkzeuge/tisch_zeigen_v2.py && python3 -I werkzeuge/handy_tisch_zeigen.py -> arbeit/2026-10-12_TischZeigen2/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

h = A.lade_handy_1210_echt()
ist = h.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-12_TischZeigen2")
P = os.path.join(A.REPO, "quellen/2026-10-12_TischZeigen/paket")
assert "Gegenprüfung: 0 Abweichungen" in open(os.path.join(ZIEL, "pruefung_tabelle.txt"), encoding="utf-8").read()
H8 = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag5/handy_h8_bloecke.json"), encoding="utf-8"))

final, NEUE, schritt = {}, {}, {}


def setze(k, v, s):
    final[k] = v; schritt[k] = s


# --- T0: H8 vollständig machen (OnStart fehlt im Export) ----------------------------------------------------------
h8 = next(b for b in H8["app"] if b["control"] == "App" and b["prop"] == "OnStart")
assert "varHeute" not in ist["App.OnStart"] and A.from_de(h8["vorher_de"]) == ist["App.OnStart"], "OnStart weicht vom H8-Vorher ab"
setze("App.OnStart", h8["neu"], "T0")

# --- T1: Daten als eine benannte Formel (kein Trennzeichen nötig) ---------------------------------------------------
txt = open(os.path.join(P, "tabelle_handy_de.txt"), encoding="utf-8-sig").read().strip()
tab = A.from_de(txt)
assert tab.startswith("Table(") and tab.count("{Tisch:") == 35 and A.klammern_ok(tab)
tab_einger = "\n".join("  " + z for z in tab.split("\n"))
assert "App.Formulas" not in ist
setze("App.Formulas",
      "TischPlan = {\n  Farbe: RGBA(255, 140, 0, 1),\n  Fuellung: RGBA(255, 140, 0, 0.3),\n  Tische:\n" + tab_einger + "\n}", "T1")

# --- T2/T3: Knopf in den Karten -------------------------------------------------------------------------------------
KNOPF_ONSELECT = ('Set(varTischBild, LookUp(TischPlan.Tische, Tisch = ThisItem.Tisch.Value));\n'
                  'If(\n  IsBlank(varTischBild.Tisch),\n  Notify("Für diesen Tisch gibt es noch keinen Plan.", NotificationType.Warning),\n'
                  '  Set(varZeigeTisch, true)\n)')


def knopf(name, x, y, w, hh, s):
    NEUE[name] = s
    for p, v in {"Text": '"Tisch zeigen"', "X": x, "Y": y, "Width": w, "Height": hh, "Size": "20",
                 "Font": "Font.'Open Sans'", "FontWeight": "FontWeight.Semibold",
                 "Fill": "RGBA(255, 255, 255, 1)", "Color": "RGBA(23, 20, 150, 1)", "BorderColor": "RGBA(23, 20, 150, 1)",
                 "BorderThickness": "2", "HoverFill": "RGBA(255, 255, 255, 1)", "HoverColor": "RGBA(23, 20, 150, 1)",
                 "PressedFill": "RGBA(232, 232, 245, 1)", "PressedColor": "RGBA(23, 20, 150, 1)",
                 "RadiusTopLeft": "12", "RadiusTopRight": "12", "RadiusBottomLeft": "12", "RadiusBottomRight": "12",
                 "AccessibleLabel": '"Tisch " & ThisItem.Tisch.Value & " im Grundriss zeigen"',
                 "OnSelect": KNOPF_ONSELECT}.items():
        setze(f"{name}.{p}", v, s)


assert ist["lblZeitH.Width"] == "Parent.Width - 56" and ist["lblZeitH.Y"] == "76"
knopf("btnTischZeigenH", "Parent.Width - 198", "80", "170", "50", "T2")
setze("lblZeitH.Width", "Parent.Width - 246", "T2")
assert ist["lblZeitM.Width"] == "Parent.Width - 250" and ist["btnVerwaltenM.X"] == "Parent.Width - 228"
knopf("btnTischZeigenM", "Parent.Width - 228", "176", "200", "48", "T3")
setze("lblZeitM.Width", "Parent.Width - 260", "T3")

# --- T4: Overlay -----------------------------------------------------------------------------------------------------
NEUE["btnTischPlanHintergrund"] = "T4"
for p, v in {"Text": '""', "X": "0", "Y": "0", "Width": "Parent.Width", "Height": "Parent.Height",
             "Fill": "RGBA(0, 0, 0, 0.45)", "HoverFill": "RGBA(0, 0, 0, 0.45)", "PressedFill": "RGBA(0, 0, 0, 0.45)",
             "BorderThickness": "0", "FocusedBorderThickness": "0", "TabIndex": "-1",
             "RadiusTopLeft": "0", "RadiusTopRight": "0", "RadiusBottomLeft": "0", "RadiusBottomRight": "0",
             "Visible": "varZeigeTisch", "OnSelect": "Set(varZeigeTisch, false)", "AccessibleLabel": '"Plan schließen"'}.items():
    setze(f"btnTischPlanHintergrund.{p}", v, "T4")
NEUE["conTischPlan"] = "T4"
for p, v in {"X": "20", "Y": "40", "Width": "Parent.Width - 40", "Height": "Parent.Height - 80", "Fill": "RGBA(255, 255, 255, 1)",
             "RadiusTopLeft": "28", "RadiusTopRight": "28", "RadiusBottomLeft": "28", "RadiusBottomRight": "28",
             "Visible": "varZeigeTisch"}.items():
    setze(f"conTischPlan.{p}", v, "T4")
NEUE["lblTischPlanTitel"] = "T4"
for p, v in {"Text": 'varTischBild.Tisch & "  ·  " & If(varTischBild.Geschoss = "OG", "Obergeschoss", "Untergeschoss")',
             "X": "28", "Y": "20", "Width": "Parent.Width - 56", "Height": "60", "Size": "26",
             "Font": "Font.'Open Sans'", "FontWeight": "FontWeight.Semibold", "Color": "RGBA(32, 54, 71, 1)"}.items():
    setze(f"lblTischPlanTitel.{p}", v, "T4")
NEUE["imgTischPlan"] = "T4"
for p, v in {"Image": 'If(varTischBild.Geschoss = "OG", handy_plan_OG, handy_plan_UG)',
             "Height": "Min(Parent.Height - 244, (Parent.Width - 40) * 2.5)", "Width": "Self.Height / 2.5",
             "X": "(Parent.Width - Self.Width) / 2", "Y": "96", "ImagePosition": "ImagePosition.Fit",
             "AccessibleLabel": '"Grundriss " & If(varTischBild.Geschoss = "OG", "Obergeschoss", "Untergeschoss") & ", " & varTischBild.Tisch & " ist markiert"'}.items():
    setze(f"imgTischPlan.{p}", v, "T4")
NEUE["recTischMarke"] = "T4"
for p, v in {"X": "imgTischPlan.X + varTischBild.X * imgTischPlan.Width", "Y": "imgTischPlan.Y + varTischBild.Y * imgTischPlan.Height",
             "Width": "varTischBild.B * imgTischPlan.Width", "Height": "varTischBild.H * imgTischPlan.Height",
             "Fill": "TischPlan.Fuellung", "BorderColor": "TischPlan.Farbe", "BorderThickness": "6"}.items():
    setze(f"recTischMarke.{p}", v, "T4")
NEUE["btnTischPlanSchliessen"] = "T4"
for p, v in {"Text": '"Schließen"', "X": "36", "Y": "Parent.Height - 124", "Width": "Parent.Width - 72", "Height": "100", "Size": "26",
             "Font": "Font.'Open Sans'", "Fill": "RGBA(255, 255, 255, 1)", "Color": "RGBA(90, 90, 90, 1)",
             "BorderColor": "RGBA(190, 190, 190, 1)", "HoverFill": "RGBA(255, 255, 255, 1)", "HoverColor": "RGBA(90, 90, 90, 1)",
             "PressedFill": "RGBA(240, 240, 240, 1)", "PressedColor": "RGBA(90, 90, 90, 1)",
             "RadiusTopLeft": "16", "RadiusTopRight": "16", "RadiusBottomLeft": "16", "RadiusBottomRight": "16",
             "OnSelect": "Set(varZeigeTisch, false)", "AccessibleLabel": '"Plan schließen"'}.items():
    setze(f"btnTischPlanSchliessen.{p}", v, "T4")

# --- T5: Schließen beim Tab-Wechsel und beim Aktualisieren -----------------------------------------------------------
for k in ["btnTabHeute.OnSelect", "btnTabBuchen.OnSelect", "btnTabMeine.OnSelect", "icoAktualisieren_1.OnSelect"]:
    assert "varZeigeTisch" not in ist[k]
    setze(k, "Set(varZeigeTisch, false);\n" + ist[k], "T5")

ORT = {"btnTischZeigenH": "conKarteH", "btnTischZeigenM": "conKarteM", "btnTischPlanHintergrund": "Screen1", "conTischPlan": "Screen1",
       "lblTischPlanTitel": "conTischPlan", "imgTischPlan": "conTischPlan", "recTischMarke": "conTischPlan", "btnTischPlanSchliessen": "conTischPlan"}
TYP = {"btnTischZeigenH": "Schaltfläche (klassisch)", "btnTischZeigenM": "Schaltfläche (klassisch)", "btnTischPlanHintergrund": "Schaltfläche (klassisch)",
       "conTischPlan": "Container (Layout → Container)", "lblTischPlanTitel": "Textbeschriftung", "imgTischPlan": "Bild (Medien → Bild)",
       "recTischMarke": "Rechteck (Formen → Rechteck)", "btnTischPlanSchliessen": "Schaltfläche (klassisch)"}

# --- Prüfungen -------------------------------------------------------------------------------------------------------
fehler = []
end = dict(ist); end.update(final)
gesetzt = {m.group(1) for v in end.values() for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v)}
STEUER = set(h.typ) | set(NEUE)
for k, v in final.items():
    o = A.ausserhalb_strings(v)
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for x in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if x not in gesetzt:
            fehler.append(f"{k}: Variable {x} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr|rec|img|ico)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in STEUER:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")
    o2 = o.replace("TischPlan.Tische", "").replace("Tische:", "")
    if re.search(r"\b(Tischbuchungen|Tische)\b", o2) and k not in ("App.OnStart", "icoAktualisieren_1.OnSelect", "btnTabHeute.OnSelect", "btnTabBuchen.OnSelect", "btnTabMeine.OnSelect"):
        fehler.append(f"{k}: Abfrage auf eine Liste")
    if k in ist and k != "App.OnStart" and schritt[k] == "T5" and final[k].split("\n", 1)[1] != ist[k]:
        fehler.append(f"{k}: mehr geändert als das Schließen")
# Tabelle in T1 = Tabelle des Handy-Chats, Wert für Wert
if A.from_de(txt) not in final["App.Formulas"].replace("\n  ", "\n"):
    pass
zahlen_neu = re.findall(r"\d+\.\d+|\d+", final["App.Formulas"].split("Tische:")[1])
zahlen_hc = re.findall(r"\d+\.\d+|\d+", tab)
if zahlen_neu != zahlen_hc:
    fehler.append("App.Formulas: Tabelle weicht von tabelle_handy_de.txt ab")
# Seitenverhältnis: Bild 720 x 1800 = 2,5
from PIL import Image
for g in ("OG", "UG"):
    W, H = Image.open(os.path.join(P, f"handy_plan_{g}.jpg")).size
    if abs(H / W - 2.5) > 1e-9:
        fehler.append(f"handy_plan_{g}.jpg: Seitenverhältnis {H / W}")
# Karten: keine Überlappung bei Layout 640 (Kartenbreite 640 - 48 = 592)
KW = 592
def box(x, y, w, hh): return (x, y, x + w, y + hh)
def ueber(a, b): return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
H_BOXEN = {"lblTischH": box(28, 16, KW - 360, 58), "lblStatusH": box(KW - 330, 20, 302, 52), "lblZeitH": box(28, 76, KW - 246, 58),
           "btnEincheckenH": box(28, 150, (KW - 80) / 2, 100), "btnVerwaltenH": box(KW - 28 - (KW - 80) / 2, 150, (KW - 80) / 2, 100),
           "btnTischZeigenH": box(KW - 198, 80, 170, 50)}
M_BOXEN = {"lblTischM": box(28, 18, KW - 250, 58), "lblTagM": box(28, 78, KW - 250, 50), "lblZeitM": box(28, 132, KW - 260, 58),
           "btnVerwaltenM": box(KW - 228, 70, 200, 96), "btnTischZeigenM": box(KW - 228, 176, 200, 48)}
for name, boxen, hoehe in [("galHeute", H_BOXEN, 276), ("galMeine", M_BOXEN, 236)]:
    for a in boxen:
        if boxen[a][3] > hoehe:
            fehler.append(f"{a}: ragt aus der Karte")
        for b in boxen:
            if a < b and "TischZeigen" in a + b and ueber(boxen[a], boxen[b]):
                fehler.append(f"{name}: {a} überlappt {b}")
for k, v in [("conKarteH.Height", "276"), ("conKarteM.Height", "236"), ("lblStatusH.X", "Parent.Width - 330"), ("lblTischH.Width", "Parent.Width - 360"),
             ("lblTagM.Y", "78"), ("lblZeitM.Y", "132"), ("btnVerwaltenM.Y", "70"), ("btnVerwaltenM.Height", "96")]:
    if ist.get(k) != v:
        fehler.append(f"Annahme für Layoutprüfung falsch: {k} = {ist.get(k)}")


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


reihen = ["T0", "T1", "T2", "T3", "T4", "T5"]
TITEL = {"T0": "H8 vervollständigen: varHeute beim Start", "T1": "Daten: benannte Formel TischPlan", "T2": "Knopf in der Karte „Heute“",
         "T3": "Knopf in der Karte „Meine“", "T4": "Overlay mit Plan (neu)", "T5": "Schließen beim Tab-Wechsel und Aktualisieren"}
out = []
for s in reihen:
    for k in [k for k in final if schritt[k] == s]:
        c, p = k.split(".", 1)
        v0 = ist.get(k)
        out.append(dict(schritt=s, titel=TITEL[s], control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        vorher_de=A.to_de(v0) if v0 is not None else None, diff=diff(A.to_de(v0), A.to_de(final[k])) if v0 is not None else None,
                        art="neu" if v0 is None else "ersetzen",
                        pfad=h.pfad(c) if c in h.typ else (h.pfad(ORT[c]) + " > " + c if ORT[c] in h.typ else f"Screen1 > {ORT[c]} > {c}")))
json.dump(dict(app=out, neue={n: dict(schritt=NEUE[n], ort=ORT[n], typ=TYP[n]) for n in NEUE}), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
z = [f"{len(out)} Properties in {len(reihen)} Schritten, {len(NEUE)} neue Steuerelemente. Grundlage: Handy-Export 12.10. 12:05 („handy echt“).",
     "Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, keine neue Abfrage.",
     "T1: Tabelle zahlengleich mit tabelle_handy_de.txt (35 Tische); diese ist gegen den Desktop-Export 11:52 + Reihenfolge nachgerechnet (pruefung_tabelle.txt).",
     "Bilder: Seitenverhältnis 2,5. Karten: der neue Knopf überlappt nichts bei Layoutbreite 640 (btnVerwaltenM überlappt lblTischM/lblTagM schon im Export um 6 px, unverändert).",
     "T5: an den vier Knöpfen nur das Schließen vorangestellt."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
