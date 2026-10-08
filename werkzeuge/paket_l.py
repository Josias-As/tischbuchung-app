# Paket L (08.10.2026): Fehler und Stimmigkeit, die Paket K v2 nicht abdeckt. Nur Properties, die K v2 NICHT ändert.
# Aufruf: python3 -I werkzeuge/paket_l.py  -> arbeit/2026-10-08_Kritische_Analyse/paket_l_bloecke.json + Prüfprotokoll
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Kritische_Analyse")
K = {f"{s['control']}.{s['prop']}" for s in json.load(open(os.path.join(A.REPO, "arbeit/2026-10-07_PaketK_v2/bloecke.json"), encoding="utf-8"))}
S = []


def schritt(nr, c, p, neu, titel, art="ersetzen"):
    S.append(dict(nr=nr, control=c, prop=p, neu=neu, titel=titel, art=art))


def ersetze(c, p, alt, neu, n=1):
    f = a.get(c, p)
    assert f.count(alt) == n, (c, p, f.count(alt))
    return f.replace(alt, neu)


BLAU, GRUEN, ROT = 'ColorValue("#171496")', 'ColorValue("#00A96B")', 'ColorValue("#EB3951")'

# L1 Startliste ohne 22:00 (sonst leere Endliste -> Buchung 22:00-00:00)
for c in ["ddStart", "ddStartTischePanel"]:
    schritt("L1", c, "Items", ersetze(c, "Items", "Sequence(RoundDown((minutenEnde - minutenStart) / 30, 0) + 1, 0)",
                                       "Sequence(Max(0, RoundDown((minutenEnde - minutenStart) / 30, 0)), 0)"),
            "Letzte Startzeit 21:30 statt 22:00")

# L2 Dashboard-Liste nach Uhrzeit, Check-in-Dialog an derselben Zeile
schritt("L2", "galTischbuchungenHeute", "Items",
        "SortByColumns(\n  " + a.get("galTischbuchungenHeute", "Items").replace("\n", "\n  ") + ",\n  \"Startzeit\",\n  SortOrder.Ascending\n)",
        "Eigene Buchungen des Tages nach Startzeit")
schritt("L2", "conCheckinDialog", "Y", ersetze("conCheckinDialog", "Y", "Filter(galTischbuchungenHeute.AllItems, ID < varSelectedBuchung.ID)",
        "Filter(galTischbuchungenHeute.AllItems, Startzeit < varSelectedBuchung.Startzeit || (Startzeit = varSelectedBuchung.Startzeit && ID < varSelectedBuchung.ID))"),
        "Dialog-Position passend zur neuen Sortierung")

# L3 Gedrückte Knöpfe: Schrift bleibt lesbar
for c in ["btnAbbrechen", "btnSchließen2", "btnSchließen3", "btnSchließen4", "btnSchließen4_1", "btnSchließenKlein"]:
    assert a.get(c, "PressedColor") in ("Self.Fill", "Color.Black")
    schritt("L3", c, "PressedColor", "Color.White", "Schrift beim Drücken weiß (vorher schwarz auf schwarz)")
    schritt("L3", c, "PressedFill", "ColorFade(Color.Black, 30%)", "Gedrückt: dunkelgrau statt schwarz")
schritt("L3", "btnSpeichern", "PressedColor", "Color.White", "Schrift beim Drücken weiß (vorher grün auf grün)")

# L4 Aktiver Tab sichtbar
for c, tab in [("btnTabDashboard", "dashboard"), ("btnTabBuchungen", "buchungen")]:
    schritt("L4", c, "Fill", f'If(varAktiverTab = "{tab}", {BLAU}, ColorFade({BLAU}, 35%))', "Aktiver Tab dunkel, inaktiver hell")

# L5 Profilfarbe pro Person fest statt bei jedem Start zufällig
farben = re.findall(r'ColorValue\("#[0-9A-Fa-f]{6}"\)', a.get("App", "OnStart").split("varProfilFarbe")[1].split("Set(varZoom")[0])
assert len(farben) == 8
schritt("L5", "Circle2", "Fill",
        "Switch(\n  Mod(Len(User().Email), 8) + 1,\n" + "".join(f"  {i}, {f},\n" for i, f in enumerate(farben[:7], 1)) + f"  {farben[7]}\n)",
        "Gleiche Farbe bei jedem Start (aus der Länge der E-Mail-Adresse)")

# L6 Details-Popup: Status passend zum Grundriss
schritt("L6", "lblStatus", "Text", 'If(varSelectedBuchung.CheckedIn, "Eingecheckt", "Gebucht")', "Status statt immer „Besetzt“")
schritt("L6", "lblStatus", "Color", 'If(varSelectedBuchung.CheckedIn, ColorValue("#EB3951"), ColorValue("#FFA500"))', "Farbe wie die Kachel (rot/orange)")

# L7 Einheitliche Bedienelemente: Buchungsdialog wie Panel (Markenblau, grüne Schalter)
for c in ["tglTagMo", "tglTagDi", "tglTagMi", "tglTagDo", "tglTagFr"]:
    schritt("L7", c, "TrueFill", 'ColorValue("#00A96B")', "Wochentag-Schalter grün wie im Panel")
for c in ["dpDatum", "dpWiederholenBis"]:
    schritt("L7", c, "IconBackground", BLAU, "Kalender-Symbol blau wie im Panel")
for c in ["ddStart", "ddEnde"]:
    schritt("L7", c, "ChevronBackground", BLAU, "Pfeil blau wie im Panel")
    schritt("L7", c, "HoverFill", "ColorFade(Self.Fill, -20%)", "Hover wie im Panel")
schritt("L7", "btnSpeichern", "Fill", BLAU, "Speichern blau wie alle anderen Speichern-Knöpfe")
schritt("L7", "btnSpeichern", "PressedFill", "ColorFade(Self.Fill, -20%)", "Gedrückt etwas dunkler")
schritt("L7", "tglAuswahlModus", "TrueFill", BLAU, "Auswahlmodus blau")

# L8 Stornieren als gefährliche Aktion erkennbar
for c in ["btnStornieren", "btnStornieren_1", "btnStornierenKlein"]:
    schritt("L8", c, "Fill", ROT, "Stornieren rot statt blau wie Speichern")

# L9 Texte: einheitlich Deutsch, gleiche Schreibweise
TEXTE = [("lblMyPersonalDesk", '"Meine Tischbuchungen"'), ("btnTischHinzufügen", '"Tisch buchen"'),
         ("lblTischeBuchenPanel", '"Tisch buchen"'), ("btnPlus1Std", '"+1 Std"'), ("btnPlus2Std", '"+2 Std"'),
         ("btnPlus3Std", '"+3 Std"'), ("btnPlus1Std_1", '"+1 Std"'), ("btnPlus2Std_1", '"+2 Std"'), ("btnPlus3Std_1", '"+3 Std"'),
         ("btnMinus1Std", '"−1 Std"'), ("btnMinus2Std", '"−2 Std"'), ("btnMinus3std", '"−3 Std"'),
         ("lblTischLeer", '"Keine Buchungen"'), ("lblTischLeer_1", '"Keine Buchungen"'),
         ("lblTitel3", 'If(IsBlank(varSelectedBuchung), "", varSelectedBuchung.Tisch.Value)'),
         ("lblTitel3_1", '"Verwalten: " & varSelectedBuchungTab.Tisch.Value'),
         ("lblTitel2", 'varSelectedBuchung.Tisch.Value'), ("lblTischHeute", 'ThisItem.Tisch.Value')]
for c, t in TEXTE:
    schritt("L9", c, "Text", t, "Text vereinheitlicht")

# L10 Auswahl- und Akzentfarben: Markenblau statt Standard-Graublau
schritt("L10", "Rectangle3_2", "Fill", BLAU, "Auswahlbalken im Buchungen-Tab blau wie im Dashboard")
for c in ["Rectangle5", "Rectangle6", "Rectangle6_1", "Rectangle6_2"]:
    assert a.get(c, "Fill") == "RGBA(100, 118, 132, 1)"
    schritt("L10", c, "Fill", BLAU, "Akzentbalken im Dialog blau")
for c in ["ddStockwerk", "ddTischePanel", "ddStartTischePanel", "ddEndTischePanel", "ddStart", "ddEnde"]:
    schritt("L10", c, "SelectionFill", BLAU, "Markierte Zeile in der Auswahlliste blau")
for c in ["ddTischePanel", "ddStartTischePanel", "ddEndTischePanel", "ddStart", "ddEnde"]:
    schritt("L10", c, "ChevronHoverBackground", "ColorFade(Self.ChevronBackground, -20%)", "Pfeil beim Hover dunkler statt graublau")

# L11 Unsichtbare Klickflächen: eine Hover-Stärke
for c in ["btnHitArea", "btnEincheckenHeute", "btnVerwalten", "btnVerwalten_2", "btnHitArea_1"]:
    schritt("L11", c, "HoverFill", "RGBA(0, 0, 0, 0.1)", "Einheitliche Hover-Abdunklung für Klickflächen")

# L12 Dialoge einheitlich weiß
for c in ["conVerwaltenDialog_1", "conVerwaltenKlein"]:
    schritt("L12", c, "Fill", "Color.White", "Dialog weiß wie alle anderen Dialoge")

# L13 Eingaben beim Öffnen zurücksetzen (Datum/Zeit blieben vom letzten Mal stehen)
schritt("L13", "btnHitArea", "OnSelect", ersetze("btnHitArea", "OnSelect",
        "      Set(varSelectedTisch, ThisItem);\n",
        "      Set(varSelectedTisch, ThisItem);\n      Reset(dpDatum);\n      Reset(ddStart);\n      Reset(ddEnde);\n      Reset(dpWiederholenBis);\n"),
        "Buchungsdialog öffnet immer mit dem Grundriss-Datum und frischen Zeiten")
KV2 = {f"{s['control']}.{s['prop']}": s for s in json.load(open(os.path.join(A.REPO, "arbeit/2026-10-07_PaketK_v2/bloecke.json"), encoding="utf-8"))}
f = KV2["btnTischHinzufügen.OnSelect"]["neu"]
assert f.rstrip().endswith('Set(varEndeOverridePanel, "")')
schritt("L13", "btnTischHinzufügen", "OnSelect",
        f.rstrip() + ";\nReset(ddStartTischePanel);\nReset(ddEndTischePanel);\nReset(dpWiederholenBis_1)",
        "Panel öffnet mit frischen Zeiten (baut auf Paket K v2 C2 auf)")
AUF_K = {"btnTischHinzufügen.OnSelect"}

# Prüfungen
fehler = []
for s in S:
    k = f"{s['control']}.{s['prop']}"
    if k in K and k not in AUF_K:
        fehler.append(f"{k}: wird schon von Paket K v2 geändert")
    if s["control"] not in a.typ:
        fehler.append(f"{k}: Steuerelement fehlt")
    if (k in a.props) != (s["art"] == "ersetzen"):
        fehler.append(f"{k}: art passt nicht (Property {'vorhanden' if k in a.props else 'fehlt'})")
    if not A.klammern_ok(s["neu"]):
        fehler.append(f"{k}: Klammern")
    de = A.to_de(s["neu"])
    if A.from_de(de) != s["neu"]:
        fehler.append(f"{k}: Rückübersetzung")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl)[A-ZÄÖÜa-zäöü0-9_]*)\.", A.ausserhalb_strings(s["neu"]))):
        if n not in a.typ:
            fehler.append(f"{k}: unbekanntes Steuerelement {n}")
    s["de"], s["orig"] = de, (KV2[k]["neu"] if k in AUF_K else a.props.get(k))
    s["orig_de"] = A.to_de(s["orig"]) if s["orig"] else None
    s["pfad"] = a.pfad(s["control"])
keys = [f"{s['control']}.{s['prop']}" for s in S]
fehler += [f"{k}: doppelt" for k in set(keys) if keys.count(k) > 1]
json.dump(S, open(os.path.join(ZIEL, "paket_l_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(S), "Properties,", len(set(s["nr"] for s in S)), "Schritte;", "keine Überschneidung mit Paket K v2" if not any("Paket K" in f for f in fehler) else "")
print("FEHLER:\n  " + "\n  ".join(fehler) if fehler else "Prüfung: 0 Fehler")
sys.exit(1 if fehler else 0)
