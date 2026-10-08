# Gesamtplan (08.10.2026): alle geplanten Änderungen als EIN Paket, jede Property genau einmal in ihrer Endfassung.
# Grundlage: Export 07.10. -> Paket K v2 -> Paket L -> Entscheidungen aus dem Interview (06:00, Freigabe, Gesperrt,
# Storno-Bestätigung, Timer, Andere Zeit buchen, Raumcode ruhig, Barrierefreiheit, Handy-App).
# Aufruf: python3 -I werkzeuge/gesamtplan.py  -> arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json + pruefung.txt
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
h = A.lade_handy()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan")
os.makedirs(ZIEL, exist_ok=True)
K = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-07_PaketK_v2/bloecke.json"), encoding="utf-8"))
L = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Kritische_Analyse/paket_l_bloecke.json"), encoding="utf-8"))

final, herkunft = {}, {}
for s in K:
    k = f"{s['control']}.{s['prop']}"
    final[k] = s["neu"]; herkunft.setdefault(k, []).append("K v2 " + s["nr"])
for s in L:
    k = f"{s['control']}.{s['prop']}"
    final[k] = s["neu"]; herkunft.setdefault(k, []).append("L " + s["nr"])

NEUE_STEUER = {}   # Name -> (Typ, Eltern, Einfügeanleitung)
NEUE_SPALTEN = {"Gesperrt"}
NEUE_VARS = {"varStornoQuelle", "varZeigeStornoFrage"}


def aktuell(k):
    return final[k] if k in final else a.props[k]


def aendere(k, alt, neu, tag, n=1):
    f = aktuell(k)
    assert f.count(alt) == n, (k, alt[:60], f.count(alt))
    final[k] = f.replace(alt, neu)
    herkunft.setdefault(k, []).append(tag)


def setze(k, wert, tag):
    final[k] = wert
    herkunft.setdefault(k, []).append(tag)


LADE = a.get("btnEinchecken", "OnSelect").split(";\n")[-1].strip()
BLAU = 'ColorValue("#171496")'

# --- 06:00: Startlisten ab 06:00, Vorschlag an anderen Tagen bleibt 08:00 -----------------------------------------
for c in ["ddStart", "ddStartTischePanel"]:
    aendere(f"{c}.Items", "30 * RoundUp(minutenJetzt / 30, 0),\n          8 * 60", "Max(6 * 60, 30 * RoundUp(minutenJetzt / 30, 0)),\n          6 * 60", "06:00")
    aendere(f"{c}.Default", "30 * RoundUp(minutenJetzt / 30, 0),", "Max(6 * 60, 30 * RoundUp(minutenJetzt / 30, 0)),", "06:00")
for c in ["btn5Std", "btn9Std"]:
    aendere(f"{c}.OnSelect", "30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60)",
            "Max(6 * 60, 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0)), 8 * 60)", "06:00")
    for p in ["DisplayMode", "Fill"]:
        k = f"{c}.{p}"
        f = aktuell(k)
        n = f.count("30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0)")
        assert n == 3, (k, n)
        f = f.replace("30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0)",
                      "Max(6 * 60, 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30, 0))")
        f = f.replace("dpDatumTischePanel.SelectedDate = Today()",
                      "dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt), Month(varPanelJetzt), Day(varPanelJetzt))")
        assert "Now()" not in f and "Today()" not in f, k
        setze(k, f, "06:00 + Öffnungszeitpunkt")

# --- Check-in-Hinweis in der Erfolgsmeldung (automatische Freigabe nach 30 Min) -------------------------------------
for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
    aendere(f"{c}.OnSelect", '" Uhr.", NotificationType.Success)',
            '" Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben.", NotificationType.Success)', "Check-in-Hinweis")

# --- P4 Gesperrt (Spalte in Tische) ------------------------------------------------------------------------------
for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
    aendere(f"{c}.OnSelect", "    IsEmpty(colNeuTermine),\n",
            '    !IsBlank(LookUp(Tische, ID = varNeuTischID && Gesperrt = true).ID),\n'
            '    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen.", NotificationType.Warning),\n'
            "    IsEmpty(colNeuTermine),\n", "P4 Gesperrt")
setze("btnHitArea.OnSelect",
      'If(\n  ThisItem.Gesperrt,\n  Notify("Dieser Tisch ist zurzeit gesperrt.", NotificationType.Warning),\n  '
      + aktuell("btnHitArea.OnSelect").replace("\n", "\n  ") + "\n)", "P4 Gesperrt")
aendere("ddTischePanel.Items", "                  Titel: Ti.Titel,\n", "                  Titel: Ti.Titel,\n                  Gesperrt: Ti.Gesperrt,\n", "P4 Gesperrt")
aendere("ddTischePanel.Items", '!("big table" in Lower(Titel)) && (Belegt = 0',
        '!Gesperrt && !("big table" in Lower(Titel)) && (Belegt = 0', "P4 Gesperrt")
setze("Rectangle1.Fill", 'If(\n  ThisItem.Gesperrt,\n  ColorValue("#A6A6A6"),\n  ' + a.get("Rectangle1", "Fill").replace("\n", "\n  ") + "\n)", "P4 Gesperrt")
setze("Circle1.Fill", 'If(\n  ThisItem.Gesperrt,\n  Color.White,\n  ' + a.get("Circle1", "Fill").replace("\n", "\n  ") + "\n)", "P4 Gesperrt")

# --- P6 Storno-Bestätigung -----------------------------------------------------------------------------------------
storno_dash, storno_tab, storno_klein = aktuell("btnStornieren.OnSelect"), aktuell("btnStornieren_1.OnSelect"), aktuell("btnStornierenKlein.OnSelect")
for f in (storno_dash, storno_tab, storno_klein):
    assert f.startswith("If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),")
setze("btnStornieren.OnSelect", 'Set(varStornoQuelle, "dash");\nSet(varZeigeStornoFrage, true)', "P6")
setze("btnStornieren_1.OnSelect", 'Set(varStornoQuelle, "tab");\nSet(varZeigeStornoFrage, true)', "P6")
setze("btnStornierenKlein.OnSelect", 'Set(varStornoQuelle, "klein");\nSet(varZeigeStornoFrage, true)', "P6")
ein = lambda t, n: "\n".join(" " * n + z if z.strip() else z for z in t.split("\n"))
NEUE_STEUER["conStornoFrage"] = ("Container (Einfügen → Layout → Container)", "Screen1", "auf oberster Ebene einfügen (nicht in einen anderen Container)")
NEUE_STEUER["lblStornoFrage"] = ("Label (Einfügen → Textbeschriftung)", "conStornoFrage", "in `conStornoFrage` einfügen")
NEUE_STEUER["btnStornoNein"] = ("Button (Einfügen → Schaltfläche, klassisch)", "conStornoFrage", "in `conStornoFrage` einfügen")
NEUE_STEUER["btnStornoJa"] = ("Button (Einfügen → Schaltfläche, klassisch)", "conStornoFrage", "in `conStornoFrage` einfügen")
for k, v in {
    "conStornoFrage.Visible": "varZeigeStornoFrage",
    "conStornoFrage.X": "(Parent.Width - Self.Width) / 2", "conStornoFrage.Y": "(Parent.Height - Self.Height) / 2",
    "conStornoFrage.Width": "420", "conStornoFrage.Height": "150", "conStornoFrage.Fill": "Color.White",
    "conStornoFrage.BorderColor": "RGBA(32, 54, 71, 1)", "conStornoFrage.BorderThickness": "1",
    "conStornoFrage.RadiusTopLeft": "16", "conStornoFrage.RadiusTopRight": "16",
    "conStornoFrage.RadiusBottomLeft": "16", "conStornoFrage.RadiusBottomRight": "16",
    "lblStornoFrage.Text": 'If(varStornoQuelle = "klein", "Wirklich " & CountRows(colAusgewaehlteBuchungen) & " Buchung(en) stornieren?", "Diese Buchung wirklich stornieren?")',
    "lblStornoFrage.X": "25", "lblStornoFrage.Y": "20", "lblStornoFrage.Width": "370", "lblStornoFrage.Height": "50",
    "lblStornoFrage.Size": "15", "lblStornoFrage.FontWeight": "FontWeight.Bold", "lblStornoFrage.Color": "RGBA(32, 54, 71, 1)",
    "btnStornoNein.Text": '"Nein"', "btnStornoNein.X": "25", "btnStornoNein.Y": "90", "btnStornoNein.Width": "170", "btnStornoNein.Height": "40",
    "btnStornoNein.Fill": "Color.Black", "btnStornoNein.Color": "Color.White", "btnStornoNein.HoverFill": "ColorFade(Self.Fill, 30%)",
    "btnStornoNein.PressedFill": "ColorFade(Color.Black, 30%)", "btnStornoNein.PressedColor": "Color.White",
    "btnStornoNein.OnSelect": "Set(varZeigeStornoFrage, false)",
    "btnStornoJa.Text": '"Ja, stornieren"', "btnStornoJa.X": "225", "btnStornoJa.Y": "90", "btnStornoJa.Width": "170", "btnStornoJa.Height": "40",
    "btnStornoJa.Fill": 'ColorValue("#EB3951")', "btnStornoJa.Color": "Color.White", "btnStornoJa.HoverFill": "ColorFade(Self.Fill, -20%)",
    "btnStornoJa.PressedFill": "ColorFade(Self.Fill, -30%)", "btnStornoJa.PressedColor": "Color.White",
    "btnStornoJa.DisplayMode": "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
    "btnStornoJa.OnSelect": 'Set(varZeigeStornoFrage, false);\nSwitch(\n  varStornoQuelle,\n  "dash",\n' + ein(storno_dash, 2)
                             + ',\n  "tab",\n' + ein(storno_tab, 2) + ',\n' + ein(storno_klein, 2) + "\n)",
}.items():
    setze(k, v, "P6 neu")

# --- P3 Timer -----------------------------------------------------------------------------------------------------
NEUE_STEUER["tmrAktualisieren"] = ("Timer (Einfügen → Eingabe → Timer)", "Screen1", "auf oberster Ebene einfügen")
still = LADE.replace('Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen.", NotificationType.Warning)', "false")
assert still != LADE
for k, v in {
    "tmrAktualisieren.Duration": "300000", "tmrAktualisieren.Repeat": "true", "tmrAktualisieren.AutoStart": "true",
    "tmrAktualisieren.Visible": "false",
    "tmrAktualisieren.OnTimerEnd": "If(\n  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab"
                                   " && !varZeigeVerwaltenKlein && !varZeigeCheckin && !varZeigeStornoFrage,\n"
                                   "  If(\n    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today(),\n"
                                   "    Set(varAnsichtsDatum, Today());\n    Reset(dpAnsichtsDatum)\n  );\n"
                                   "  Refresh(Tischbuchungen);\n  " + still + "\n)",
}.items():
    setze(k, v, "P3 neu")

# --- P1 Andere Zeit buchen ----------------------------------------------------------------------------------------
hit = aktuell("btnHitArea.OnSelect")
frei = hit.split("IsBlank(relevanteBuchung),", 1)[1].split(",\n        Set(varDetailsTisch", 1)[0].strip()
assert frei.startswith("Set(varSelectedTisch, ThisItem);") and frei.endswith("Set(varTagSo, false)"), frei[-80:]
frei = "\n".join(z.strip() for z in frei.split("\n")).replace("Set(varSelectedTisch, ThisItem);", "Set(varSelectedTisch, varDetailsTisch);", 1)
NEUE_STEUER["btnAndereZeit"] = ("Button (Einfügen → Schaltfläche, klassisch)", "conDetailsPopup", "in `conDetailsPopup` einfügen")
NEUE_STEUER["lblBelegtHeute"] = ("Label (Einfügen → Textbeschriftung)", "conBuchungDialog", "in `conBuchungDialog` einfügen")
assert a.get("conDetailsPopup", "Height") == "154" and a.get("Image7", "Height") == "154"
for k, v in {
    "conDetailsPopup.Height": "200", "Image7.Height": "Parent.Height",
    "btnAndereZeit.Text": '"Andere Zeit buchen"', "btnAndereZeit.X": "25", "btnAndereZeit.Y": "152",
    "btnAndereZeit.Width": "210", "btnAndereZeit.Height": "36", "btnAndereZeit.Size": "12",
    "btnAndereZeit.Fill": BLAU, "btnAndereZeit.Color": "Color.White", "btnAndereZeit.HoverFill": "ColorFade(Self.Fill, -20%)",
    "btnAndereZeit.PressedFill": "ColorFade(Self.Fill, -30%)", "btnAndereZeit.PressedColor": "Color.White",
    "btnAndereZeit.Visible": "!varDetailsTisch.Gesperrt",
    "btnAndereZeit.OnSelect": frei,
    "lblBelegtHeute.Text": 'With(\n  { belegt: SortByColumns(Filter(colGrundriss, TischName = varSelectedTisch.Titel && Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)), "Startzeit", SortOrder.Ascending) },\n  If(IsEmpty(belegt), "An diesem Tag noch frei.", "Belegt: " & Concat(belegt, Text(Startzeit, "hh:mm") & "–" & Text(Endzeit, "hh:mm"), ", "))\n)',
    "lblBelegtHeute.Visible": "varZeigeDialog && dpDatum.SelectedDate = varAnsichtsDatum",
    "lblBelegtHeute.X": "270", "lblBelegtHeute.Y": "110", "lblBelegtHeute.Width": "165", "lblBelegtHeute.Height": "150",
    "lblBelegtHeute.Size": "11", "lblBelegtHeute.VerticalAlign": "VerticalAlign.Top", "lblBelegtHeute.Color": "RGBA(32, 54, 71, 1)",
}.items():
    setze(k, v, "P1 neu")

# --- Raumcode ruhigstellen (nicht löschen) -------------------------------------------------------------------------
setze("galRäume.Items", "If(\n  varZeigeRaumBuchungForm,\n  " + a.get("galRäume", "Items").replace("\n", "\n  ") + "\n)", "Raum ruhig")
setze("galRaumbuchungenHeute.Items", "If(\n  varZeigeRaumBuchungForm,\n  " + a.get("galRaumbuchungenHeute", "Items") + "\n)", "Raum ruhig")
for c in ["recBuchungDavor1", "recBuchungDanach1"]:
    setze(f"{c}.Visible", "varZeigeRaumBestätigung && " + a.get(c, "Visible"), "Raum ruhig")
for c in ["Label4", "Label5"]:
    setze(f"{c}.Text", "If(\n  varZeigeRaumBestätigung,\n  " + a.get(c, "Text").replace("\n", "\n  ") + ',\n  ""\n)', "Raum ruhig")

# --- Barrierefreiheit (AccessibleLabel) ---------------------------------------------------------------------------
LABELS = {"Image6": "Aktualisieren", "dpDatumRaum": "Datum Raumbuchung", "ddBeginnRaumPanel": "Beginn Raumbuchung",
          "ddDauerRaumPanel": "Dauer Raumbuchung", "galRäume": "Räume", "Icon1": "Aktualisieren",
          "tglAuswahlModus": "Mehrfachauswahl ein oder aus", "galAlleTischbuchungen": "Meine Tischbuchungen",
          "dpAnsichtsDatum": "Angezeigtes Datum wählen", "Icon1_1": "Aktualisieren", "galTischbuchungenHeute": "Meine Buchungen am gewählten Tag",
          "galRaumbuchungenHeute": "Meine Raumbuchungen", "ddTischePanel": "Tisch", "dpDatumTischePanel": "Datum",
          "ddStartTischePanel": "Beginn", "ddEndTischePanel": "Ende", "tglTagMo_1": "Montag", "tglTagDi_1": "Dienstag",
          "dpWiederholenBis_1": "Wiederholen bis", "tglTagMi_1": "Mittwoch", "tglTagDo_1": "Donnerstag", "tglTagFr_1": "Freitag",
          "ddStockwerk": "Stockwerk", "imgGrundrissUG": "Grundriss Untergeschoss", "Gallery1": "Tische im Grundriss",
          "Rectangle6_2": "Trennlinie", "Image1_4": "Symbolbild", "Rectangle6_1": "Trennlinie", "dpDatum": "Datum",
          "ddStart": "Beginn", "ddEnde": "Ende", "tglTagMo": "Montag", "tglTagDi": "Dienstag", "tglTagMi": "Mittwoch",
          "tglTagDo": "Donnerstag", "tglTagFr": "Freitag", "dpWiederholenBis": "Wiederholen bis"}
assert len(LABELS) == 37
for c, t in LABELS.items():
    setze(f"{c}.AccessibleLabel", f'"{t}"', "Barrierefreiheit")

# --- Handy-App: 06:00 --------------------------------------------------------------------------------------------
HANDY = {}
hf = h.get("ddStart", "Items")
alt = "If(ddDatum.Selected.Tag = Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), 8 * 60)"
assert hf.count(alt) == 1
neu_ab = "If(ddDatum.Selected.Tag = Today(), Max(6 * 60, 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0)), 6 * 60)"
HANDY["ddStart.Items"] = hf.replace(alt, neu_ab)
assert "ddStart.Default" not in h.props
HANDY["ddStart.Default"] = ("If(\n  ddDatum.Selected.Tag = Today(),\n  With(\n    { ab: Max(6 * 60, 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0)) },\n"
                            '    Text(Time(RoundDown(ab / 60, 0), Mod(ab, 60), 0), "hh:mm")\n  ),\n  "08:00"\n)')

# --- Schritte (jede Property genau einmal) --------------------------------------------------------------------------
P = lambda *ks: list(ks)
SCHRITTE = [
    ("G1", 1, "Grundlage: Variablen beim App-Start", P("App.OnStart")),
    ("G2", 1, "Verwalten-Dialoge: Grenze beim Öffnen, Dauer-Knöpfe ohne Abfrage", P("btnVerwalten.OnSelect", "btnVerwalten_2.OnSelect",
        *[f"{c}.{p}" for c in ["btnPlus1Std", "btnPlus2Std", "btnPlus3Std", "btnPlus1Std_1", "btnPlus2Std_1", "btnPlus3Std_1",
                                "btnMinus1Std", "btnMinus2Std", "btnMinus3std"] for p in ["DisplayMode", "Fill"]])),
    ("G3", 1, "Verlängern/Verkürzen sicher", P("btnVerlängern.OnSelect", "btnVerlängern.DisplayMode", "btnVerlängern_1.OnSelect", "btnVerlängern_1.DisplayMode")),
    ("G4", 1, "Stornieren sicher, mit Bestätigung", P(*[k for k in final if k.split(".")[0] in ("conStornoFrage", "lblStornoFrage", "btnStornoNein", "btnStornoJa")],
        "btnStornieren.OnSelect", "btnStornieren.DisplayMode", "btnStornieren_1.OnSelect", "btnStornieren_1.DisplayMode", "btnStornierenKlein.OnSelect")),
    ("G5", 1, "Einchecken sicher", P("btnEinchecken.OnSelect", "btnEinchecken.DisplayMode")),
    ("G6", 1, "Neue Buchung speichern (Dialog und Panel)", P("btnSpeichern.OnSelect", "btnSpeichern.DisplayMode", "btnSpeichernTischePanel.OnSelect", "btnSpeichernTischePanel.DisplayMode")),
    ("G7", 1, "Dialoge öffnen mit frischen Eingaben, Startzeiten ab 06:00", P("btnHitArea.OnSelect", "btnTischHinzufügen.OnSelect",
        "ddStart.Items", "ddStart.Default", "ddStartTischePanel.Items", "ddStartTischePanel.Default")),
    ("G8", 2, "Automatisch aktualisieren (Timer)", P(*[k for k in final if k.startswith("tmrAktualisieren.")])),
    ("G9", 3, "Tischauswahl im Panel: nur freie Tische", P("ddTischePanel.Items", "ddTischePanel.Items.Value", "ddTischePanel.AllowEmptySelection", "ddTischePanel.Default")),
    ("G10", 3, "Knöpfe 5 Std / 9 Std", P(*[f"{c}.{p}" for c in ["btn5Std", "btn9Std"] for p in ["DisplayMode", "Fill", "OnSelect"]])),
    ("G11", 3, "Hinweistext Wiederholung im Panel", P("Label14.Text", "Label14.Color")),
    ("G12", 3, "Kleine Korrekturen", P("ddStockwerk.OnSelect", "Icon1.OnSelect", "Icon1_1.OnSelect", "Image6.OnSelect", "btnHitArea_1.OnSelect", "btnAbbrechenTischePanel.OnSelect")),
    ("G13", 4, "Grundriss: gesperrte Tische grau", P("Rectangle1.Fill", "Circle1.Fill")),
    ("G14", 4, "Grundriss: freie Zeit an belegten Tischen buchen", P("conDetailsPopup.Height", "Image7.Height",
        *[k for k in final if k.split(".")[0] in ("btnAndereZeit", "lblBelegtHeute")])),
    ("G15", 4, "Details-Popup: Status wie Kachel", P("lblStatus.Text", "lblStatus.Color")),
    ("G16", 4, "Dashboard-Liste nach Uhrzeit", P("galTischbuchungenHeute.Items", "conCheckinDialog.Y")),
    ("G17", 5, "Gedrückte Knöpfe lesbar", P(*[k for k in final if any(t.startswith("L L3") for t in herkunft[k]) and k.endswith(("PressedColor", "PressedFill")) and not k.startswith("btnSpeichern.PressedFill")])),
    ("G18", 5, "Aktiver Tab sichtbar", P("btnTabDashboard.Fill", "btnTabBuchungen.Fill")),
    ("G19", 5, "Profilfarbe fest", P("Circle2.Fill")),
    ("G20", 5, "Buchungsdialog im selben Design wie das Panel", P(*[k for k in final if any(t == "L L7" for t in herkunft[k])])),
    ("G21", 5, "Stornieren rot", P("btnStornieren.Fill", "btnStornieren_1.Fill", "btnStornierenKlein.Fill")),
    ("G22", 5, "Texte einheitlich Deutsch", P(*[k for k in final if any(t == "L L9" for t in herkunft[k])])),
    ("G23", 5, "Auswahl- und Trennlinienfarben", P(*[k for k in final if any(t == "L L10" for t in herkunft[k])])),
    ("G24", 5, "Einheitlicher Hover auf Klickflächen", P(*[k for k in final if any(t == "L L11" for t in herkunft[k])])),
    ("G25", 6, "Raumcode ruhigstellen (bleibt erhalten)", P(*[k for k in final if "Raum ruhig" in herkunft[k]])),
    ("G26", 7, "Barrierefreiheit: Beschriftungen", P(*[k for k in final if k.endswith(".AccessibleLabel")])),
]
fehler = []
zugeteilt = {}
for sid, ph, titel, keys in SCHRITTE:
    for k in keys:
        if k in zugeteilt:
            fehler.append(f"{k}: doppelt in {zugeteilt[k]} und {sid}")
        zugeteilt[k] = sid
for k in final:
    if k not in zugeteilt:
        fehler.append(f"{k}: keinem Schritt zugeteilt")
for k in zugeteilt:
    if k not in final:
        fehler.append(f"{k}: in Schritt, aber ohne Formel")

# --- Prüfungen -----------------------------------------------------------------------------------------------------
STEUER = set(a.typ) | set(NEUE_STEUER)
ALTE_VARS = set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", "\n".join(a.props.values())))
stand = dict(a.props); stand.update(final)
gesetzt = set()
for v in stand.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
for k, f in final.items():
    c = k.split(".")[0]
    if c not in STEUER:
        fehler.append(f"{k}: Steuerelement unbekannt")
    if not A.klammern_ok(f):
        fehler.append(f"{k}: Klammern")
    if A.from_de(A.to_de(f)) != f:
        fehler.append(f"{k}: Rückübersetzung")
    if "//" in A.ausserhalb_strings(f):
        fehler.append(f"{k}: Kommentar")
    ohne = A.ausserhalb_strings(f)
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", ohne)):
        if v not in gesetzt:
            fehler.append(f"{k}: Variable {v} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr)[A-ZÄÖÜa-zäöü0-9_]*)\.", ohne)):
        if n not in STEUER:
            fehler.append(f"{k}: unbekanntes Steuerelement {n}")
# Schreibstellen
schreib = [k for k, v in stand.items() if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", A.ausserhalb_strings(v))]
for k in schreib:
    v = stand[k]
    arme = [v] if k != "btnStornoJa.OnSelect" else [storno_dash, storno_tab, storno_klein]
    for arm in arme:
        if not arm.startswith("If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),") or LADE not in arm:
            fehler.append(f"{k}: Schreibstelle ohne Sperre oder Ladezeile")
for k in ["btnStornieren.OnSelect", "btnStornieren_1.OnSelect", "btnStornierenKlein.OnSelect"]:
    if "Remove(" in stand[k]:
        fehler.append(f"{k}: sollte nur noch fragen")
# Handy
for k, f in HANDY.items():
    if not A.klammern_ok(f) or A.from_de(A.to_de(f)) != f:
        fehler.append(f"Handy {k}: Klammern/Rückübersetzung")

out = []
for sid, ph, titel, keys in SCHRITTE:
    for k in keys:
        c, p = k.split(".", 1)
        out.append(dict(schritt=sid, phase=ph, titel=titel, control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        orig=a.props.get(k), orig_de=A.to_de(a.props[k]) if k in a.props else None,
                        art="neu" if k not in a.props else "ersetzen", herkunft=herkunft.get(k, []),
                        pfad=a.pfad(c) if c in a.typ else f"(neu) {NEUE_STEUER[c][1]} > {c}",
                        neues_steuerelement=NEUE_STEUER.get(c)))
handy = [dict(control=k.split(".")[0], prop=k.split(".", 1)[1], neu=v, de=A.to_de(v), orig=h.props.get(k),
              orig_de=A.to_de(h.props[k]) if k in h.props else None, art="neu" if k not in h.props else "ersetzen") for k, v in HANDY.items()]
json.dump(dict(app=out, handy=handy, neue_steuerelemente=NEUE_STEUER), open(os.path.join(ZIEL, "gesamtplan_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
zeilen = [f"{len(out)} Properties Desktop-App in {len(SCHRITTE)} Schritten, {len(handy)} Properties Handy-App, {len(NEUE_STEUER)} neue Steuerelemente.",
          f"Schreibstellen auf Tischbuchungen nach dem Plan: {len(schreib)} ({', '.join(sorted(schreib))}), alle mit Zweifach-Sperre und Ladezeile.",
          "Je Property geprüft: Klammern, Rückübersetzung deutsch->englisch, keine Kommentare, Steuerelemente bekannt oder neu angelegt, jede gelesene var/col wird irgendwo gesetzt.",
          "Jede Property kommt genau einmal vor."]
zeilen += ["FEHLER: " + f for f in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))
sys.exit(1 if fehler else 0)
