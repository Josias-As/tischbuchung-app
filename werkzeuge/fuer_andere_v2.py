# „Für andere buchen“ + weicher Hinweis, Fassung 2 (10.11.2026): Design aus Referenz-Steuerelementen der App übernommen.
# (Fassung 1 vom 26.10.: werkzeuge/fuer_andere.py, bleibt erhalten.)
# Grundlage: Desktop-Export 25.10. 20:09 (quellen/2026-10-25_Desktop/). Entscheidungen Josias 26.10.: 1 A, 2 a, 3 ja, 4 ja, 6 ok.
# Aufruf: python3 -I werkzeuge/fuer_andere_v2.py -> arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_1011_echt()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2")
os.makedirs(ZIEL, exist_ok=True)
fehler, notiz = [], []
final, herkunft = {}, {}
# Rohwerte aller Steuerelemente (auch Standard-Properties, die in f.props fehlen können)
import glob as _g
roh = {}
for _fn in _g.glob(os.path.join(A.ENTPACKT, "desktop_2026-11-10_echt", "Controls", "*.json")):
    def _w(n):
        for r in n.get("Rules", []):
            roh[f"{n['Name']}.{r['Property']}"] = r["InvariantScript"].strip()
        for c in n.get("Children", []):
            _w(c)
    _w(json.load(open(_fn, encoding="utf-8-sig"))["TopParent"])


def stil(ref, props, name):
    """Stil-Properties eines vorhandenen Steuerelements auf ein neues übertragen (Design aus der App, nicht aus dem Kopf)."""
    out = {}
    for p in props:
        w = roh.get(f"{ref}.{p}")
        if w is None:
            fehler.append(f"Referenz {ref}.{p} fehlt im Export")
        else:
            out[f"{name}.{p}"] = w.replace("btnSpeichern", name) if "Self" not in w else w
    return out


STIL_KNOPF = ["Fill", "Color", "BorderColor", "BorderThickness", "DisabledBorderColor", "Font", "FontWeight", "HoverBorderColor", "HoverColor", "HoverFill",
              "PressedBorderColor", "PressedColor", "PressedFill", "RadiusTopLeft", "RadiusTopRight", "RadiusBottomLeft", "RadiusBottomRight", "Size", "Height"]
STIL_EINGABE = ["Fill", "Color", "BorderColor", "BorderThickness", "Font", "Size", "Height"]
STIL_SCHALTER = ["BorderColor", "Font", "Size", "TrueFill", "Color"]
STIL_DIALOG = ["Fill", "RadiusTopLeft", "RadiusTopRight", "RadiusBottomLeft", "RadiusBottomRight", "DropShadow"]
REFERENZ = {"knopf_primaer": "btnSpeichern", "knopf_sekundaer": "btnAbbrechen", "eingabe": "ddStart", "schalter": "tglTagMo", "dialog": "conDetailsPopup",
            "overlay": "conLadeOverlay", "titel": "lblTischeBuchenPanel"}
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
    v = ersetze(v, "ClearCollect(colNeuIch, Filter(Tischbuchungen, Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));",
                "ClearCollect(colNeuIch, ForAll(Filter(Tischbuchungen, Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart) As B, "
                "{ID: B.ID, Startzeit: B.Startzeit, Endzeit: B.Endzeit, CheckedIn: B.CheckedIn, Erstellt: B.Erstellt, GastName: B.GastName}));", k)
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
    v = ersetze(v, "ClearCollect(colVerlIch, Filter(Tischbuchungen, Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));",
                "ClearCollect(colVerlIch, ForAll(Filter(Tischbuchungen, Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt) As B, "
                "{ID: B.ID, Startzeit: B.Startzeit, Endzeit: B.Endzeit, CheckedIn: B.CheckedIn, Erstellt: B.Erstellt, GastName: B.GastName}));", k)
    v = ersetze(v, '      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch),\n'
                   '      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht.", NotificationType.Warning),\n', "", k)
    v = ersetze(v, "),\n      IfError(\n        Patch(Tischbuchungen, varVerlBuchung, {Endzeit: varVerlEndeNeu}),",
                "),\n"
                '      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt,\n'
                f'      Set(varFbQuelle, "{quelle}");\n'
                '      Set(varFbText, "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");\n'
                '      Set(varFbZeige, true),\n'
                "      IfError(\n        Patch(Tischbuchungen, varVerlBuchung, {Endzeit: varVerlEndeNeu}),", k)
    v = ersetze(v, "  Set(varAusgewaehltePlusDauer, Blank());\n", "  If(!varFbZeige, Set(varAusgewaehltePlusDauer, Blank()));\n", k)
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
final["lblPerson.Size"] = "If(IsBlank(varSelectedBuchung.GastName), 13, 11)"
final["lblPerson.Height"] = "If(IsBlank(varSelectedBuchung.GastName), 40, 46)"
final["lblZeit2.Y"] = "If(IsBlank(varSelectedBuchung.GastName), 100, 118)"
o = ist["lblZeitHeute.Text"]
final["lblZeitHeute.Text"] = gast("ThisItem", o, o + ' & Char(10) & "für " & ThisItem.GastName')
final["lblZeitHeute.Height"] = "If(IsBlank(ThisItem.GastName), Self.Size * 1.8, Self.Size * 3.6)"
o = ist["lblRaumZeit.Text"]
final["lblRaumZeit.Text"] = gast("ThisItem", o, o + ' & Char(10) & "für " & ThisItem.GastName')
final["lblRaumZeit.Height"] = "If(IsBlank(ThisItem.GastName), Self.Size * 1.8, Self.Size * 3.6)"
final["lblTischHeute.Y"] = "If(IsBlank(ThisItem.GastName), 27, 21)"
final["lblTischName.Y"] = "If(IsBlank(ThisItem.GastName), 27, 21)"
o = ist["lblZeit3.Text"]
final["lblZeit3.Text"] = gast("varSelectedBuchung", o, o + ' & Char(10) & "für " & varSelectedBuchung.GastName')
final["lblZeit3.Size"] = "If(IsBlank(varSelectedBuchung.GastName), 13, 10)"
final["lblZeit3.Width"] = "If(IsBlank(varSelectedBuchung.GastName), 150, btnPlus1Std.X - Self.X - 1)"
final["lblZeit3.Height"] = "If(IsBlank(varSelectedBuchung.GastName), 40, 50)"
o = ist["lblTitel3_1.Text"]
final["lblTitel3_1.Text"] = gast("varSelectedBuchungTab", o, '"Tisch " & varSelectedBuchungTab.Tisch.Value & "  ·  für " & varSelectedBuchungTab.GastName')
final["lblTitel3_1.Size"] = "If(IsBlank(varSelectedBuchungTab.GastName), 18, 15)"
final["lblTitel3_1.Width"] = "If(IsBlank(varSelectedBuchungTab.GastName), 400, Parent.Width - 24)"
for k in ["lblPerson.Text", "lblPerson.Width", "lblPerson.Size", "lblPerson.Height", "lblZeit2.Y", "lblZeitHeute.Text", "lblZeitHeute.Height", "lblRaumZeit.Text", "lblRaumZeit.Height",
          "lblZeit3.Text", "lblZeit3.Size", "lblZeit3.Width", "lblZeit3.Height", "lblTitel3_1.Text", "lblTitel3_1.Size", "lblTitel3_1.Width",
          "lblTischHeute.Y", "lblTischName.Y"]:
    herkunft[k] = "S8"

# --- S3/S4 Schalter und Namensfeld ------------------------------------------------------------------------------------
# Raster der Eingaben im Dialog: 40 hoch, Reihen bei Y 122 und 186 (ddStart, ddEnde). Der Schalter (28 hoch wie die Wochentage) sitzt mittig in der Reihe.
def schalter(name, x, y_reihe):
    d = stil(REFERENZ["schalter"], STIL_SCHALTER, name)
    d.update({f"{name}.X": x, f"{name}.Y": f"{y_reihe} + 6", f"{name}.Width": "165", f"{name}.Height": "28",
              f"{name}.Default": "false", f"{name}.FalseText": '"Für mich"', f"{name}.TrueText": '"Für andere"',
              f"{name}.AccessibleLabel": '"Für jemand anderen buchen"'})
    return d


def namensfeld(name, tgl, x, y, w):
    d = stil(REFERENZ["eingabe"], STIL_EINGABE, name)
    d.update({f"{name}.X": x, f"{name}.Y": y, f"{name}.Width": w,
              f"{name}.Default": '""', f"{name}.HintText": '"Name (Pflicht)"', f"{name}.MaxLength": "100",
              f"{name}.Visible": f"{tgl}.Value", f"{name}.AccessibleLabel": '"Name der Person, für die gebucht wird"'})
    return d


for k, v in schalter("tglFuerAndere", "270", "122").items():
    final[k] = v; herkunft[k] = "S3"
for k, v in namensfeld("txtGastName", "tglFuerAndere", "270", "186", "165").items():
    final[k] = v; herkunft[k] = "S3"
NEU["tglFuerAndere"] = ("Umschalter (klassisch, „Umschalten“)", "conBuchungDialog")
NEU["txtGastName"] = ("Texteingabe (klassisch)", "conBuchungDialog")
PANEL_REIHE = "tglTagFr_1.Y + tglTagFr_1.Height + 20"
for k, v in schalter("tglFuerAnderePanel", "ddTischePanel.X", PANEL_REIHE).items():
    final[k] = v; herkunft[k] = "S4"
final["tglFuerAnderePanel.Y"] = f"({PANEL_REIHE}) + 6"
for k, v in namensfeld("txtGastNamePanel", "tglFuerAnderePanel", "ddTischePanel.X + 175", PANEL_REIHE, "ddTischePanel.Width - 175").items():
    final[k] = v; herkunft[k] = "S4"
NEU["tglFuerAnderePanel"] = ("Umschalter (klassisch, „Umschalten“)", "conTischBuchungenPanel")
NEU["txtGastNamePanel"] = ("Texteingabe (klassisch)", "conTischBuchungenPanel")
k = "btnSpeichernTischePanel.Y"
if ist[k] != "tglTagFr_1.Y + tglTagFr_1.Height + 20":
    fehler.append(f"{k} anders als erwartet")
final[k] = f"({PANEL_REIHE}) + 40 + 20"
herkunft[k] = "S4"

# --- S2 Hinweisdialog direkt in Screen1 -------------------------------------------------------------------------------
NEU["btnFbHintergrund"] = ("Schaltfläche (klassisch)", "Screen1")
NEU["conFbHinweis"] = ("Container (Layout → Container, nicht horizontal/vertikal)", "Screen1")
NEU["lblFbTitel"] = ("Textbeschriftung", "conFbHinweis")
NEU["lblFbHinweis"] = ("Textbeschriftung", "conFbHinweis")
NEU["btnFbAbbrechen"] = ("Schaltfläche (klassisch)", "conFbHinweis")
NEU["btnFbTrotzdem"] = ("Schaltfläche (klassisch)", "conFbHinweis")
OV = roh["conLadeOverlay.Fill"]
dlg = {
    "btnFbHintergrund.X": "0", "btnFbHintergrund.Y": "0", "btnFbHintergrund.Width": "Parent.Width", "btnFbHintergrund.Height": "Parent.Height",
    "btnFbHintergrund.Text": '""', "btnFbHintergrund.Fill": OV, "btnFbHintergrund.HoverFill": OV, "btnFbHintergrund.PressedFill": OV,
    "btnFbHintergrund.BorderThickness": "0", "btnFbHintergrund.FocusedBorderThickness": "0",
    "btnFbHintergrund.RadiusTopLeft": "0", "btnFbHintergrund.RadiusTopRight": "0", "btnFbHintergrund.RadiusBottomLeft": "0", "btnFbHintergrund.RadiusBottomRight": "0",
    "btnFbHintergrund.TabIndex": "-1", "btnFbHintergrund.Visible": "varFbZeige", "btnFbHintergrund.OnSelect": "false",
    "btnFbHintergrund.AccessibleLabel": '"Hinweis offen"',
    "conFbHinweis.Width": "580", "conFbHinweis.Height": "280",
    "conFbHinweis.X": "(Parent.Width - Self.Width) / 2", "conFbHinweis.Y": "(Parent.Height - Self.Height) / 2", "conFbHinweis.Visible": "varFbZeige",
    "lblFbTitel.X": "20", "lblFbTitel.Y": "20", "lblFbTitel.Width": "Parent.Width - 40", "lblFbTitel.Height": "40",
    "lblFbTitel.Text": '"Zur selben Zeit schon gebucht"', "lblFbTitel.Font": "Font.'Open Sans'", "lblFbTitel.Size": roh["lblTischeBuchenPanel.Size"],
    "lblFbTitel.FontWeight": roh["lblTischeBuchenPanel.FontWeight"], "lblFbTitel.Color": roh["lblTischeBuchenPanel.Color"],
    "lblFbHinweis.X": "20", "lblFbHinweis.Y": "70", "lblFbHinweis.Width": "Parent.Width - 40", "lblFbHinweis.Height": "Parent.Height - 150",
    "lblFbHinweis.Text": f'varFbText & Char(10) & Char(10) & "{KONTAKT}"',
    "lblFbHinweis.Font": "Font.'Open Sans'", "lblFbHinweis.Size": "13", "lblFbHinweis.Color": roh["Label2.Color"],
    "lblFbHinweis.VerticalAlign": "VerticalAlign.Top",
    "btnFbAbbrechen.X": "20", "btnFbAbbrechen.Y": "Parent.Height - 60", "btnFbAbbrechen.Width": "(Parent.Width - 60) / 2",
    "btnFbAbbrechen.Text": '"Abbrechen"', "btnFbAbbrechen.AccessibleLabel": '"Abbrechen, nichts buchen"',
    "btnFbAbbrechen.OnSelect": "Set(varFbZeige, false);\nSet(varFbTrotzdem, false)",
    "btnFbTrotzdem.X": "Parent.Width - Self.Width - 20", "btnFbTrotzdem.Y": "btnFbAbbrechen.Y", "btnFbTrotzdem.Width": "btnFbAbbrechen.Width",
    "btnFbTrotzdem.Text": 'If(varFbQuelle = "verl" || varFbQuelle = "verltab", "Trotzdem verlängern", "Trotzdem buchen")',
    "btnFbTrotzdem.DisplayMode": "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
    "btnFbTrotzdem.AccessibleLabel": "Self.Text",
    "btnFbTrotzdem.OnSelect": ("If(\n  !varIsLoading && varFbZeige,\n  Set(varFbTrotzdem, true);\n  Set(varSperreBis, Blank());\n"
                               '  Switch(\n    varFbQuelle,\n    "panel", Select(btnSpeichernTischePanel),\n    "verl", Select(btnVerlängern),\n'
                               '    "verltab", Select(btnVerlängern_1),\n    Select(btnSpeichern)\n  )\n)'),
}
dlg.update(stil(REFERENZ["dialog"], STIL_DIALOG, "conFbHinweis"))
dlg.update(stil(REFERENZ["knopf_sekundaer"], STIL_KNOPF, "btnFbAbbrechen"))
dlg.update(stil(REFERENZ["knopf_primaer"], STIL_KNOPF, "btnFbTrotzdem"))
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
    if re.search(r'DropColumns\([^;]*"', v) or re.search(r"\bFilter\(Tischbuchungen,[^)]*GastName", v):
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
               '      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht.", NotificationType.Warning),',
               "  Set(varAusgewaehltePlusDauer, Blank());"}
    for z in weg:
        if z not in erlaubt and "Gebucht: " not in z and "RemoveIf(colVerlIch" not in z and "ClearCollect(colNeuIch" not in z and "ClearCollect(colVerlIch" not in z:
            fehler.append(f"{k}: Zeile unerwartet weg: {z.strip()[:60]}")
# Dialog und Panel gleich behandelt
a = final["btnSpeichern.OnSelect"].replace("tglFuerAndere", "T").replace("txtGastName", "X").replace('"dialog"', "Q")
b = final["btnSpeichernTischePanel.OnSelect"].replace("tglFuerAnderePanel", "T").replace("txtGastNamePanel", "X").replace('"panel"', "Q")
da = [z for z in difflib.ndiff(ist["btnSpeichern.OnSelect"].split("\n"), a.split("\n")) if z[:1] in "+-"]
db = [z for z in difflib.ndiff(ist["btnSpeichernTischePanel.OnSelect"].split("\n"), b.split("\n")) if z[:1] in "+-"]
if da != db:
    fehler.append("Dialog und Panel unterschiedlich geändert")
for ctrl in ["btnVerlängern", "btnVerlängern_1"]:
    v = final[f"{ctrl}.OnSelect"]
    if "!IsEmpty(colVerlIch) && !varFbBestaetigt" not in v or not (v.index("!IsEmpty(colVerlKonflikt)") < v.index("!IsEmpty(colVerlIch) && !varFbBestaetigt")):
        fehler.append(f"{ctrl}: Hinweis vor der Tischkonflikt-Prüfung")
    if "If(!varFbZeige, Set(varAusgewaehltePlusDauer, Blank()))" not in v:
        fehler.append(f"{ctrl}: Dauer wird trotz offenem Hinweis gelöscht")
for ctrl, col in [("btnSpeichern", "colNeuIch"), ("btnSpeichernTischePanel", "colNeuIch"), ("btnVerlängern", "colVerlIch"), ("btnVerlängern_1", "colVerlIch")]:
    if f"ClearCollect({col}, ForAll(" not in final[f"{ctrl}.OnSelect"] or "GastName: B.GastName" not in final[f"{ctrl}.OnSelect"]:
        fehler.append(f"{ctrl}: {col} ohne Projektion mit GastName")
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
# Layout: Textbreite je Zeichenart (Open Sans, Punkt -> Pixel 1,333, wie handy_tisch_zeigen.py), Zeilenhöhe 1,2 x Größe
def textpx(text, size):
    em = 0
    for ch in text:
        if ch.isdigit(): em += 0.572
        elif ch == " ": em += 0.26
        elif ch in ":.·,–-": em += 0.3
        elif ch in "il": em += 0.26
        elif ch in "mw": em += 0.85
        elif ch.isupper(): em += 0.68
        else: em += 0.55
    return em * 1.05 * size * 1.333


def zeilen(text, size, breite):
    import math
    return sum(max(1, math.ceil(textpx(t, size) / breite)) for t in text.split("\n"))


ZEILE = lambda size: size * 1.333 * 1.2
NAME, BUCHER = "Max Mustermann", "gebucht von Josias Semeraf"


def gw(k):
    """Wert im Gast-Zweig von If(IsBlank(…GastName), alt, gast) bzw. feste Zahl."""
    m = re.fullmatch(r"If\(IsBlank\([\w.]+\), [^,]+, (\d+)\)", final[k]) or re.fullmatch(r"(\d+)", final[k])
    return int(m.group(1)) if m else None


BW = int(final["conFbHinweis.Width"]); BS = int(final["btnFbTrotzdem.Size"])
pruef = [  # (wo, Text, Größe, verfügbare Breite)
    ("tglFuerAndere Text", "Für andere", int(final["tglFuerAndere.Size"]), int(final["tglFuerAndere.Width"]) - 55),
    ("btnFbTrotzdem", "Trotzdem verlängern", BS, (BW - 60) / 2 - 20),
    ("btnFbAbbrechen", "Abbrechen", int(final["btnFbAbbrechen.Size"]), (BW - 60) / 2 - 20),
    ("lblPerson Zeile 2", BUCHER, gw("lblPerson.Size"), 256 - 25 - 6 - 10),
    ("lblZeit3 Zeile 2 (bis btnPlus1Std X 175)", "für " + NAME, gw("lblZeit3.Size"), 175 - 12 - 1 - 10),
    ("lblZeitHeute Zeile 1 (bis lblStatusHeute X 270)", "08:00 – 12:00", 12, 270 - 100 - 12),
    ("lblZeitHeute Zeile 2", "für " + NAME, 12, 470 - 173 - 12),
    ("lblRaumZeit Zeile 2 (bis chkAuswahl)", "für " + NAME, 12, (600 - 75 - 60) - 100 - 12),
    ("lblTitel3_1 Gast", "Tisch UG Desk 14  ·  für " + NAME, gw("lblTitel3_1.Size"), 550 - 24 - 10),
]
for wo, t, size, w in pruef:
    px = textpx(t, size)
    notiz.append(f"Textbreite {wo}: „{t}“ ca. {px:.0f} von {w:.0f}")
    if px > w:
        fehler.append(f"{wo}: „{t}“ ca. {px:.0f} > {w:.0f}")
hoehen = [  # (wo, Zeilen, Größe, Höhe)
    ("lblPerson (Gast)", 2, gw("lblPerson.Size"), gw("lblPerson.Height")), ("lblZeit3 (Gast)", 2, gw("lblZeit3.Size"), gw("lblZeit3.Height")),
    ("lblZeitHeute (Gast)", 2, 12, 12 * 3.6),
]
for wo, n, size, h in hoehen:
    bedarf = n * ZEILE(size) + (0 if "Zeit" in wo and "lblZeit3" not in wo else 10)
    notiz.append(f"Höhe {wo}: {n} Zeilen ca. {bedarf:.0f} von {h:.0f}")
    if bedarf > h + 1:
        fehler.append(f"{wo}: {bedarf:.0f} > {h}")
for wo, unten, grenze in [("Popup lblPerson bis lblZeit2", 71 + gw("lblPerson.Height"), gw("lblZeit2.Y")), ("Popup lblZeit2 Textmitte", 118 + 20 + ZEILE(13) / 2, 154),
                          ("Verwalten lblZeit3 bis Knöpfe", 50 + gw("lblZeit3.Height"), 100), ("Karte lblZeitHeute 2 Zeilen (Gast, Titel bei Y 21, Kartenunterkante 94, 8 Rand)", 21 + 14 * 1.8 + 2 * ZEILE(12), 94 - 8)]:
    notiz.append(f"Lage {wo}: {unten:.0f} ≤ {grenze}")
    if unten > grenze:
        fehler.append(f"Lage {wo}: {unten:.0f} > {grenze}")
lang = max(['"An 10 von 11 Terminen hast du zu dieser Zeit schon einen Tisch gebucht. Trotzdem einen weiteren Tisch buchen?"',
            '"Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?"'], key=len).strip('"') + "\n\n" + KONTAKT
n = zeilen(lang, 13, BW - 40 - 10)
notiz.append(f"Höhe lblFbHinweis: längster Text {n} Zeilen ca. {n * ZEILE(13) + 10:.0f} von {280 - 100}")
if n * ZEILE(13) + 10 > 280 - 100:
    fehler.append("lblFbHinweis zu niedrig")
# Altbestand-Werte der neu gesetzten oder geänderten Maße (Standard aus den Rohdaten)
import glob as _g
roh = {}
for fn in _g.glob(os.path.join(A.ENTPACKT, "desktop_2026-11-10_echt", "Controls", "*.json")):
    def _walk(n):
        for r in n.get("Rules", []):
            roh[f"{n['Name']}.{r['Property']}"] = r["InvariantScript"]
        for c in n.get("Children", []):
            _walk(c)
    _walk(json.load(open(fn, encoding="utf-8-sig"))["TopParent"])
for k in ["lblPerson.Width", "lblPerson.Size", "lblPerson.Height", "lblZeit2.Y", "lblZeit3.Size", "lblZeit3.Width", "lblZeit3.Height", "lblTitel3_1.Size",
          "lblTitel3_1.Width", "lblZeitHeute.Height", "lblRaumZeit.Height"]:
    alt = ist.get(k, roh.get(k))
    if alt is None or f"GastName), {alt}," not in final[k]:
        fehler.append(f"{k}: Altbestand-Wert {alt} fehlt")
    notiz.append(f"{k}: Altbestand {alt}" + ("" if k in ist else " (Standard, im Export nicht gesetzt)"))
ALT_STANDARD = {k: roh.get(k) for k in final if k not in ist and k.split(".")[0] in f.typ}
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
json.dump(dict(app=out, neue={k: list(v) for k, v in NEU.items()}, standard=ALT_STANDARD), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
geaendert = sorted(k for k in final if k in ist)
std = sorted(k for k in final if k not in ist and k.split(".")[0] in f.typ)
z = [f"Für andere buchen: {len(out)} Properties: {len(geaendert)} bestehende ersetzt, {len(std)} an bestehenden Steuerelementen neu gesetzt (bisher Standard), "
     f"{len(out) - len(geaendert) - len(std)} an {len(NEU)} neuen Steuerelementen. Grundlage: Export 10.11. 08:13 (echt, zeichengleich mit 25.10.).",
     "Bisher Standard: " + ", ".join(f"{k} ({ALT_STANDARD.get(k)})" for k in std),
     "Geänderte bestehende Properties: " + ", ".join(geaendert)] + notiz
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
