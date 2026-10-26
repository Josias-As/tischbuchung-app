# „Für andere buchen“ + weicher Hinweis bei zweitem Tisch zur selben Zeit (26.10.2026).
# Grundlage: Desktop-Export 25.10. 20:09 (quellen/2026-10-25_Desktop/). Entscheidungen Josias 26.10.: 1 A, 2 a, 3 ja, 4 ja, 6 ok.
# Aufruf: python3 -I werkzeuge/fuer_andere.py -> arbeit/2026-10-26_FuerAndere/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_2510()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-26_FuerAndere")
os.makedirs(ZIEL, exist_ok=True)
fehler, notiz = [], []
final, herkunft = {}, {}
NEU = {}   # neue Steuerelemente: Name -> (Typ, Eltern, Hinweis)


def ersetze(text, alt, neu, wo):
    n = text.count(alt)
    if n != 1:
        fehler.append(f"{wo}: Anker {n}x statt 1x: {alt[:70]!r}")
        return text
    return text.replace(alt, neu)


LADE = "ClearCollect(colGrundriss, DropColumns(Filter(neu, Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze), Erstellt)); Set(varGrundrissStand, Now())"
KONTAKT = "Fragen: Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT)."

# --- S5 Speichern (Dialog und Panel) ---------------------------------------------------------------------------------
for k, tgl, txt, quelle in [("btnSpeichern.OnSelect", "tglFuerAndere", "txtGastName", "dialog"),
                            ("btnSpeichernTischePanel.OnSelect", "tglFuerAnderePanel", "txtGastNamePanel", "panel")]:
    v = ist[k]
    v = ersetze(v, "Set(varIsLoading, true);\n",
                "Set(varIsLoading, true);\n"
                "  Set(varFbBestaetigt, varFbTrotzdem);\n"
                "  Set(varFbTrotzdem, false);\n"
                "  Set(varFbZeige, false);\n"
                f"  Set(varFbFuerAndere, {tgl}.Value);\n"
                f"  Set(varFbGast, If({tgl}.Value, Trim({txt}.Text), Blank()));\n", k)
    v = ersetze(v, 'IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID),\n    Notify("Bitte einen Tisch auswählen.", NotificationType.Warning),\n',
                'IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID),\n    Notify("Bitte einen Tisch auswählen.", NotificationType.Warning),\n'
                '    varFbFuerAndere && IsBlank(varFbGast),\n'
                '    Notify("Bitte den Namen der Person eingeben, für die du buchst.", NotificationType.Warning),\n', k)
    v = ersetze(v, "RemoveIf(colNeuIch, !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);",
                "RemoveIf(colNeuIch, varFbFuerAndere || !IsBlank(GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));", k)
    v = ersetze(v, "            !IsBlank(LookUp(colNeuIch, Startzeit < T.Ende && Endzeit > T.Start).ID),",
                "            !varFbBestaetigt && !IsBlank(LookUp(colNeuIch, Startzeit < T.Ende && Endzeit > T.Start).ID),", k)
    v = ersetze(v, "If(\n      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt,",
                "If(\n      varNeuIchBelegt > 0,\n"
                f'      Set(varFbQuelle, "{quelle}");\n'
                '      Set(varFbText, If(varNeuGesamt = 1, "Du hast zu dieser Zeit schon einen Tisch gebucht.", '
                '"An " & varNeuIchBelegt & " von " & varNeuGesamt & " Terminen hast du zu dieser Zeit schon einen Tisch gebucht.") & '
                '" Trotzdem einen weiteren Tisch buchen?");\n'
                "      Set(varFbZeige, true),\n"
                "      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt,", k)
    v = ersetze(v, "              SerienID: varSerienID\n", "              SerienID: varSerienID,\n              GastName: varFbGast\n", k)
    v = ersetze(v, '"Gebucht: " & varNeuTischTitel & ", "', '"Gebucht: " & varNeuTischTitel & If(IsBlank(varFbGast), "", " für " & varFbGast) & ", "', k)
    final[k] = v
    herkunft[k] = "S5"

# --- S6 Verlängern (Dashboard und Tab) --------------------------------------------------------------------------------
for k, quelle in [("btnVerlängern.OnSelect", "verl"), ("btnVerlängern_1.OnSelect", "verltab")]:
    v = ist[k]
    v = ersetze(v, "Set(varIsLoading, true);\n",
                "Set(varIsLoading, true);\n  Set(varFbBestaetigt, varFbTrotzdem);\n  Set(varFbTrotzdem, false);\n  Set(varFbZeige, false);\n", k)
    v = ersetze(v, "RemoveIf(colVerlIch, ID = varVerlBuchung.ID || (",
                "RemoveIf(colVerlIch, ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (", k)
    v = ersetze(v, '      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch),\n'
                   '      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht.", NotificationType.Warning),\n',
                '      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt,\n'
                f'      Set(varFbQuelle, "{quelle}");\n'
                '      Set(varFbText, "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");\n'
                '      Set(varFbZeige, true),\n', k)
    final[k] = v
    herkunft[k] = "S6"

# --- S7 Öffner setzen Schalter, Name und Bestätigung zurück ------------------------------------------------------------
k = "btnHitArea.OnSelect"
final[k] = ersetze(ist[k], "      Reset(dpDatum);\n",
                   "      Reset(tglFuerAndere);\n      Reset(txtGastName);\n      Set(varFbTrotzdem, false);\n      Reset(dpDatum);\n", k)
herkunft[k] = "S7"
k = "btnTischHinzufügen.OnSelect"
if not ist[k].endswith("Reset(dpWiederholenBis_1)"):
    fehler.append(f"{k}: Ende anders als erwartet")
final[k] = ist[k] + ";\nReset(tglFuerAnderePanel);\nReset(txtGastNamePanel);\nSet(varFbTrotzdem, false)"
herkunft[k] = "S7"

# --- S8 Anzeige: Altbestand (GastName leer) bleibt zeichengleich -----------------------------------------------------
def gast(rec, orig, neu_ausdruck):
    return f"If(\n  IsBlank({rec}.GastName),\n  {orig},\n  {neu_ausdruck}\n)"


o = ist["lblPerson.Text"]
final["lblPerson.Text"] = gast("varSelectedBuchung", o, 'varSelectedBuchung.GastName & Char(10) & "gebucht von " & varSelectedBuchung.Person.DisplayName')
final["lblPerson.Width"] = "If(IsBlank(varSelectedBuchung.GastName), 150, Image7.X - Self.X - 6)"
final["lblZeit2.Y"] = "If(IsBlank(varSelectedBuchung.GastName), 100, 112)"
o = ist["lblZeitHeute.Text"]
final["lblZeitHeute.Text"] = gast("ThisItem", o, o + ' & "  ·  für " & ThisItem.GastName')
o = ist["lblRaumZeit.Text"]
final["lblRaumZeit.Text"] = gast("ThisItem", o, o + ' & "  ·  für " & ThisItem.GastName')
o = ist["lblZeit3.Text"]
final["lblZeit3.Text"] = gast("varSelectedBuchung", o, o + ' & Char(10) & "für " & varSelectedBuchung.GastName')
o = ist["lblTitel3_1.Text"]
final["lblTitel3_1.Text"] = gast("varSelectedBuchungTab", o, o + ' & "  ·  für " & varSelectedBuchungTab.GastName')
final["lblTitel3_1.Width"] = "If(IsBlank(varSelectedBuchungTab.GastName), 400, Parent.Width - 24)"
for k in ["lblPerson.Text", "lblPerson.Width", "lblZeit2.Y", "lblZeitHeute.Text", "lblRaumZeit.Text", "lblZeit3.Text", "lblTitel3_1.Text", "lblTitel3_1.Width"]:
    herkunft[k] = "S8"

# --- S3/S4 Schalter und Namensfeld ------------------------------------------------------------------------------------
def schalter(name, x, y):
    return {
        f"{name}.X": x, f"{name}.Y": y, f"{name}.Width": "165", f"{name}.Height": "40",
        f"{name}.Default": "false",
        f"{name}.FalseText": '"Für mich"', f"{name}.TrueText": '"Für andere"',
        f"{name}.TrueFill": 'ColorValue("#00A96B")', f"{name}.BorderColor": "RGBA(32, 54, 71, 1)",
        f"{name}.Font": "Font.'Open Sans'", f"{name}.Size": "13",
        f"{name}.AccessibleLabel": '"Für jemand anderen buchen"',
    }


def namensfeld(name, tgl, x, y, w):
    return {
        f"{name}.X": x, f"{name}.Y": y, f"{name}.Width": w, f"{name}.Height": "40",
        f"{name}.Default": '""', f"{name}.HintText": '"Name (Pflicht)"', f"{name}.MaxLength": "100",
        f"{name}.Visible": f"{tgl}.Value", f"{name}.BorderColor": "RGBA(32, 54, 71, 1)",
        f"{name}.Font": "Font.'Open Sans'", f"{name}.Size": "13",
        f"{name}.AccessibleLabel": '"Name der Person, für die gebucht wird"',
    }


for k, v in schalter("tglFuerAndere", "270", "122").items():
    final[k] = v; herkunft[k] = "S3"
for k, v in namensfeld("txtGastName", "tglFuerAndere", "270", "186", "165").items():
    final[k] = v; herkunft[k] = "S3"
NEU["tglFuerAndere"] = ("Umschalter (klassisch, „Umschalten“)", "conBuchungDialog")
NEU["txtGastName"] = ("Texteingabe (klassisch)", "conBuchungDialog")
for k, v in schalter("tglFuerAnderePanel", "ddTischePanel.X", "tglTagFr_1.Y + tglTagFr_1.Height + 20").items():
    final[k] = v; herkunft[k] = "S4"
for k, v in namensfeld("txtGastNamePanel", "tglFuerAnderePanel", "ddTischePanel.X + 175", "tglFuerAnderePanel.Y", "ddTischePanel.Width - 175").items():
    final[k] = v; herkunft[k] = "S4"
NEU["tglFuerAnderePanel"] = ("Umschalter (klassisch, „Umschalten“)", "conTischBuchungenPanel")
NEU["txtGastNamePanel"] = ("Texteingabe (klassisch)", "conTischBuchungenPanel")
k = "btnSpeichernTischePanel.Y"
if ist[k] != "tglTagFr_1.Y + tglTagFr_1.Height + 20":
    fehler.append(f"{k} anders als erwartet")
final[k] = "tglFuerAnderePanel.Y + tglFuerAnderePanel.Height + 20"
herkunft[k] = "S4"

# --- S2 Hinweisdialog direkt in Screen1 -------------------------------------------------------------------------------
NEU["btnFbHintergrund"] = ("Schaltfläche (klassisch)", "Screen1")
NEU["conFbHinweis"] = ("Container (Layout → Container, nicht horizontal/vertikal)", "Screen1")
NEU["lblFbHinweis"] = ("Textbeschriftung", "conFbHinweis")
NEU["btnFbAbbrechen"] = ("Schaltfläche (klassisch)", "conFbHinweis")
NEU["btnFbTrotzdem"] = ("Schaltfläche (klassisch)", "conFbHinweis")
dlg = {
    "btnFbHintergrund.X": "0", "btnFbHintergrund.Y": "0", "btnFbHintergrund.Width": "Parent.Width", "btnFbHintergrund.Height": "Parent.Height",
    "btnFbHintergrund.Text": '""', "btnFbHintergrund.Fill": "RGBA(0, 0, 0, 0.35)", "btnFbHintergrund.HoverFill": "RGBA(0, 0, 0, 0.35)",
    "btnFbHintergrund.PressedFill": "RGBA(0, 0, 0, 0.35)", "btnFbHintergrund.BorderThickness": "0", "btnFbHintergrund.FocusedBorderThickness": "0",
    "btnFbHintergrund.RadiusTopLeft": "0", "btnFbHintergrund.RadiusTopRight": "0", "btnFbHintergrund.RadiusBottomLeft": "0", "btnFbHintergrund.RadiusBottomRight": "0",
    "btnFbHintergrund.TabIndex": "-1", "btnFbHintergrund.Visible": "varFbZeige", "btnFbHintergrund.OnSelect": "false",
    "btnFbHintergrund.AccessibleLabel": '"Hinweis offen"',
    "conFbHinweis.Width": "440", "conFbHinweis.Height": "230",
    "conFbHinweis.X": "(Parent.Width - Self.Width) / 2", "conFbHinweis.Y": "(Parent.Height - Self.Height) / 2",
    "conFbHinweis.Fill": "Color.White", "conFbHinweis.RadiusTopLeft": "16", "conFbHinweis.RadiusTopRight": "16",
    "conFbHinweis.RadiusBottomLeft": "16", "conFbHinweis.RadiusBottomRight": "16", "conFbHinweis.Visible": "varFbZeige",
    "lblFbHinweis.X": "20", "lblFbHinweis.Y": "20", "lblFbHinweis.Width": "Parent.Width - 40", "lblFbHinweis.Height": "130",
    "lblFbHinweis.Text": f'varFbText & Char(10) & Char(10) & "{KONTAKT}"',
    "lblFbHinweis.Font": "Font.'Open Sans'", "lblFbHinweis.Size": "13", "lblFbHinweis.Color": "RGBA(50, 49, 48, 1)",
    "lblFbHinweis.VerticalAlign": "VerticalAlign.Top",
    "btnFbAbbrechen.X": "20", "btnFbAbbrechen.Y": "Parent.Height - 60", "btnFbAbbrechen.Width": "(Parent.Width - 60) / 2", "btnFbAbbrechen.Height": "40",
    "btnFbAbbrechen.Text": '"Abbrechen"', "btnFbAbbrechen.Font": "Font.'Open Sans'", "btnFbAbbrechen.Size": "15",
    "btnFbAbbrechen.Fill": "Color.Black", "btnFbAbbrechen.Color": "RGBA(255, 255, 255, 1)",
    "btnFbAbbrechen.HoverFill": "ColorFade(Self.Fill, 30%)", "btnFbAbbrechen.PressedFill": "ColorFade(Color.Black, 30%)", "btnFbAbbrechen.PressedColor": "Color.White",
    "btnFbAbbrechen.AccessibleLabel": '"Abbrechen, nichts buchen"',
    "btnFbAbbrechen.OnSelect": "Set(varFbZeige, false);\nSet(varFbTrotzdem, false)",
    "btnFbTrotzdem.X": "Parent.Width - Self.Width - 20", "btnFbTrotzdem.Y": "btnFbAbbrechen.Y", "btnFbTrotzdem.Width": "btnFbAbbrechen.Width", "btnFbTrotzdem.Height": "40",
    "btnFbTrotzdem.Text": 'If(varFbQuelle = "verl" || varFbQuelle = "verltab", "Trotzdem verlängern", "Trotzdem buchen")',
    "btnFbTrotzdem.Font": "Font.'Open Sans'", "btnFbTrotzdem.Size": "15",
    "btnFbTrotzdem.Fill": 'ColorValue("#171496")', "btnFbTrotzdem.Color": "RGBA(255, 255, 255, 1)",
    "btnFbTrotzdem.HoverFill": "ColorFade(Self.Fill, -20%)", "btnFbTrotzdem.PressedFill": "ColorFade(Self.Fill, -20%)", "btnFbTrotzdem.PressedColor": "Color.White",
    "btnFbTrotzdem.DisplayMode": "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
    "btnFbTrotzdem.AccessibleLabel": "Self.Text",
    "btnFbTrotzdem.OnSelect": ("If(\n  !varIsLoading && varFbZeige,\n  Set(varFbTrotzdem, true);\n  Set(varSperreBis, Blank());\n"
                               '  Switch(\n    varFbQuelle,\n    "panel", Select(btnSpeichernTischePanel),\n    "verl", Select(btnVerlängern),\n'
                               '    "verltab", Select(btnVerlängern_1),\n    Select(btnSpeichern)\n  )\n)'),
}
for k, v in dlg.items():
    final[k] = v; herkunft[k] = "S2"

# --- Prüfungen -----------------------------------------------------------------------------------------------------------
STEUER = set(f.typ) | set(NEU)
end = dict(ist); end.update(final)
gesetzt = {m.group(1) for v in end.values() for m in re.finditer(r"Set\(\s*(var\w+)", v)}
for k, v in final.items():
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    o = A.ausserhalb_strings(v)
    if "//" in o:
        fehler.append(f"{k}: Kommentar")
    for x in set(re.findall(r"\b(var\w+)", o)):
        if x not in gesetzt:
            fehler.append(f"{k}: {x} wird nirgends gesetzt")
    for c in set(re.findall(r"\b([A-Za-zÄÖÜäöü_]\w*)\.(?:X|Y|Width|Height|Value|Text|Selected|SelectedDate)\b", o)) - {"Self", "Parent", "ThisItem", "T", "F", "B", "D", "N", "M", "X", "Ti", "Z", "Tisch", "Geschoss", "Person"}:
        if c not in STEUER and not c.startswith("var"):
            fehler.append(f"{k}: Steuerelement {c} unbekannt")
    for c in re.findall(r"(?:Select|Reset)\((\w+)\)", o):
        if c not in STEUER:
            fehler.append(f"{k}: {c} unbekannt")
    if re.search(r"(?<![\w.])GastName\b|\.GastName\b", o) and not re.search(r"\b(ThisItem|varSelectedBuchung|varSelectedBuchungTab|varVerlBuchung)\.GastName|GastName: varFbGast|IsBlank\(GastName\)", o):
        fehler.append(f"{k}: GastName ohne Bezug")
    if re.search(r'DropColumns\([^;]*"', v) or re.search(r"\bFilter\(Tischbuchungen[^;]*GastName", v):
        fehler.append(f"{k}: GastName im Server-Filter (nicht delegierbar)")
# neue Variablen alle mit Präfix varFb, keine neuen Variablen ohne Präfix
alt_vars = {m.group(1) for v in ist.values() for m in re.finditer(r"Set\(\s*(var\w+)", v)}
neu_vars = gesetzt - alt_vars
if any(not x.startswith("varFb") for x in neu_vars):
    fehler.append(f"neue Variablen ohne Präfix: {neu_vars}")
notiz.append("neue Variablen: " + ", ".join(sorted(neu_vars)))
# Schreibstellen: Sperre, Ladezeile, IfError und varIsLoading-Rücksetzung unverändert vorhanden
for k in ["btnSpeichern.OnSelect", "btnSpeichernTischePanel.OnSelect", "btnVerlängern.OnSelect", "btnVerlängern_1.OnSelect"]:
    for s in [LADE, "Set(varIsLoading, false)", "IfError(", "!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis)"]:
        if final[k].count(s) != ist[k].count(s):
            fehler.append(f"{k}: {s[:30]} verändert")
    # alles außer den Einfügungen bleibt gleich: entferne neue Zeilen und vergleiche zeilenweise Anzahl gemeinsamer Zeilen
    alt_z, neu_z = ist[k].split("\n"), final[k].split("\n")
    weg = [z for z in alt_z if z not in neu_z]
    erlaubt = {"      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt,", "              SerienID: varSerienID",
               "    RemoveIf(colNeuIch, !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);",
               "            !IsBlank(LookUp(colNeuIch, Startzeit < T.Ende && Endzeit > T.Start).ID),",
               "      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch),",
               '      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht.", NotificationType.Warning),'}
    for z in weg:
        if z not in erlaubt and "Gebucht: " not in z and "RemoveIf(colVerlIch" not in z:
            fehler.append(f"{k}: Zeile unerwartet weg: {z.strip()[:60]}")
# Dialog und Panel gleich behandelt
a = final["btnSpeichern.OnSelect"].replace("tglFuerAndere", "T").replace("txtGastName", "X").replace('"dialog"', "Q")
b = final["btnSpeichernTischePanel.OnSelect"].replace("tglFuerAnderePanel", "T").replace("txtGastNamePanel", "X").replace('"panel"', "Q")
da = [z for z in difflib.ndiff(ist["btnSpeichern.OnSelect"].split("\n"), a.split("\n")) if z[:1] in "+-"]
db = [z for z in difflib.ndiff(ist["btnSpeichernTischePanel.OnSelect"].split("\n"), b.split("\n")) if z[:1] in "+-"]
if da != db:
    fehler.append("Dialog und Panel unterschiedlich geändert")
# Altbestand: Originaltext steckt unverändert im Zweig IsBlank(GastName)
for k in ["lblPerson.Text", "lblZeitHeute.Text", "lblRaumZeit.Text", "lblZeit3.Text", "lblTitel3_1.Text"]:
    if f",\n  {ist[k]},\n" not in final[k] or not final[k].startswith("If(\n  IsBlank("):
        fehler.append(f"{k}: Altbestand nicht zeichengleich")
for k, alt in [("lblPerson.Width", "150"), ("lblZeit2.Y", "100"), ("lblTitel3_1.Width", "400")]:
    if f"GastName), {alt}," not in final[k]:
        fehler.append(f"{k}: Altbestand-Wert {alt} fehlt")
# Hinweisdialog: Trotzdem läuft nur über vorhandene Speichern-/Verlängern-Knöpfe, jede Quelle hat einen Zweig
for q, ctrl in [("dialog", "btnSpeichern"), ("panel", "btnSpeichernTischePanel"), ("verl", "btnVerlängern"), ("verltab", "btnVerlängern_1")]:
    if f'Set(varFbQuelle, "{q}")' not in final[f"{ctrl}.OnSelect"]:
        fehler.append(f"{ctrl}: setzt Quelle {q} nicht")
    if f"Select({ctrl})" not in final["btnFbTrotzdem.OnSelect"]:
        fehler.append(f"Trotzdem ruft {ctrl} nicht auf")
for ctrl in ["btnSpeichern", "btnSpeichernTischePanel", "btnVerlängern", "btnVerlängern_1"]:
    v = final[f"{ctrl}.OnSelect"]
    if v.index("Set(varFbTrotzdem, false)") > v.index("Set(varIsLoading, true)") + 200:
        fehler.append(f"{ctrl}: Bestätigung wird nicht am Anfang verbraucht")
if "Set(varFbZeige, false)" in final["btnFbTrotzdem.OnSelect"]:
    fehler.append("Trotzdem blendet den Hinweis selbst aus (Doppelklick träfe den Dialog darunter)")
for ctrl in ["btnSpeichern", "btnSpeichernTischePanel", "btnVerlängern", "btnVerlängern_1"]:
    v = final[f"{ctrl}.OnSelect"]
    if not (v.index("Set(varIsLoading, true)") < v.index("Set(varFbZeige, false)") < v.index("Set(varFbZeige, true)")):
        fehler.append(f"{ctrl}: Hinweis wird nicht am Anfang ausgeblendet")
for ctrl in ["btnSpeichern", "btnSpeichernTischePanel"]:
    if final[f"{ctrl}.OnSelect"].count("GastName: varFbGast") != 1:
        fehler.append(f"{ctrl}: GastName wird nicht gespeichert")
for ctrl in ["btnVerlängern", "btnVerlängern_1"]:
    if "!IsEmpty(colVerlIch) && !varFbBestaetigt" not in final[f"{ctrl}.OnSelect"]:
        fehler.append(f"{ctrl}: Bestätigung wird nicht beachtet")
# Layout (Schätzung Textbreite: Größe * 0,56 je Zeichen)
def breite(t, size):
    return len(t) * size * 0.56
for t, s, w, wo in [("Für andere", 13, 165 - 60, "Schalter"), ("Für mich", 13, 165 - 60, "Schalter"), ("Trotzdem verlängern", 15, (440 - 60) / 2 - 12, "btnFbTrotzdem"),
                    ("Abbrechen", 15, (440 - 60) / 2 - 12, "btnFbAbbrechen"), ("gebucht von Josias Semeraf", 13, 256 - 25 - 6 - 10, "lblPerson"),
                    ("für Max Mustermann", 13, 150 - 10, "lblZeit3"), ("08:00 – 12:00  ·  für Max Mustermann", 12, 470 - 173 - 12, "lblZeitHeute")]:
    if breite(t, s) > w:
        fehler.append(f"{wo}: „{t}“ ca. {breite(t, s):.0f} > {w:.0f}")
    notiz.append(f"Textbreite {wo}: „{t}“ ca. {breite(t, s):.0f} von {w:.0f}")
# Lage Panel: Schalterzeile und Speichern innerhalb 678 (conDashboard bei 768 Höhe)
y_fr = 320 + 50 / 2 - 28 / 2 + 4 * (28 + 10)
y_row = y_fr + 28 + 20
y_btn = y_row + 40 + 20
notiz.append(f"Panel: Zeile „Für andere“ Y {y_row:g}–{y_row + 40:g}, Speichern Y {y_btn:g}–{y_btn + 40:g}, Panelhöhe bei 768 = 678")
if y_btn + 40 > 678:
    fehler.append("Panel: Speichern ragt heraus")
notiz.append("Dialog: Schalter X 270–435, Y 122–162, Namensfeld Y 186–226; frei zwischen Image2 (bis 245) und Eingaben (ab 448); Wochentage erst ab Y 290")

# --- Ausgabe ----------------------------------------------------------------------------------------------------------------
def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


SCHRITTE = [
    ("S2", "Hinweisdialog anlegen (direkt in Screen1)"),
    ("S3", "Buchungsdialog: Schalter und Namensfeld"),
    ("S4", "Panel: Schalter und Namensfeld, Speichern rückt nach unten"),
    ("S5", "Speichern: Gast, weicher Hinweis, GastName"),
    ("S6", "Verlängern: Gast-Buchungen zählen nicht, weicher Hinweis"),
    ("S7", "Öffner setzen Schalter und Name zurück"),
    ("S8", "Anzeige: Gastname und „gebucht von“"),
]
out = []
for sid, titel in SCHRITTE:
    for k in [k for k in final if herkunft[k] == sid]:
        c, p = k.split(".", 1)
        v0 = ist.get(k)
        out.append(dict(schritt=sid, titel=titel, control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        vorher_de=A.to_de(v0) if v0 is not None else None,
                        diff=diff(A.to_de(v0), A.to_de(final[k])) if v0 is not None else None,
                        art="neu" if v0 is None else "ersetzen",
                        pfad=f.pfad(c) if c in f.typ else f"(neu) {NEU[c][1]} > {c}"))
if sorted(k for k in final) != sorted(f"{o['control']}.{o['prop']}" for o in out):
    fehler.append("Schritte decken nicht alle Properties ab")
json.dump(dict(app=out, neue={k: list(v) for k, v in NEU.items()}), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
geaendert = sorted(k for k in final if k in ist)
z = [f"Für andere buchen: {len(out)} Properties ({len(geaendert)} bestehende geändert, {len(out) - len(geaendert)} an {len(NEU)} neuen Steuerelementen). Grundlage: Export 25.10. 20:09.",
     "Geänderte bestehende Properties: " + ", ".join(geaendert)] + notiz
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
