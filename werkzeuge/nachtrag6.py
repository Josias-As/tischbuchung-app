# Nachtrag 6 (12.10.2026): Verfallene Buchung im Dashboard – kein Check-in-Dialog mehr, dafür „Neu buchen“.
# Grundlage: Export 08.10. 14:26 (PCAppfertig) + Nachtrag 5. Diff je Property gegen den Export (Nachtrag 5 ändert keine dieser Properties).
# Aufruf: python3 -I werkzeuge/nachtrag6.py -> arbeit/2026-10-12_Nachtrag6/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_fertig()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-12_Nachtrag6")
os.makedirs(ZIEL, exist_ok=True)
N5 = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag5/bloecke.json"), encoding="utf-8"))
stand = dict(ist)
for b in N5["app"]:
    stand[f"{b['control']}.{b['prop']}"] = b["neu"]

TAKT = "Coalesce(varJetztTakt, Now())"
G = f"DateAdd({TAKT}, -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes)"
VERFALLEN = f"!ThisItem.CheckedIn && ThisItem.Startzeit <= {G} && ThisItem.Erstellt <= {G}"
# gleiche Regel wie lblStatusHeute nach Nachtrag 5 N4 (S3b)
s3b = stand["lblStatusHeute.Text"]
assert f"ThisItem.Startzeit <= {G} && ThisItem.Erstellt <= {G}" in s3b, "Regel weicht von S3b ab"
NAECHSTER = f"30 * RoundUp((Hour({TAKT}) * 60 + Minute({TAKT})) / 30, 0)"
NEU_SICHTBAR = (f"varAnsichtsDatum = Today() && {VERFALLEN} &&\n"
                f"Hour(ThisItem.Endzeit) * 60 + Minute(ThisItem.Endzeit) > {NAECHSTER}")

final, herkunft, NEUE = {}, {}, {}

# --- R1 Karte: Check-in-Dialog nur, wenn es etwas zu tun gibt ----------------------------------------------------------
final["btnEincheckenHeute.DisplayMode"] = (f"If(\n  ThisItem.Endzeit <= {TAKT} || ({VERFALLEN}),\n"
                                           "  DisplayMode.Disabled,\n  DisplayMode.Edit\n)")
final["btnEincheckenHeute.DisabledFill"] = "Color.Transparent"
final["btnEincheckenHeute.DisabledBorderColor"] = "Color.Transparent"
for k in ["btnEincheckenHeute.DisplayMode", "btnEincheckenHeute.DisabledFill", "btnEincheckenHeute.DisabledBorderColor"]:
    herkunft[k] = "R1"

# --- R2 Knopf „Neu buchen“ in der Karte -------------------------------------------------------------------------------
NEUE["btnNeuBuchenHeute"] = ("Button (Einfügen → Schaltfläche, klassisch)", "galTischbuchungenHeute",
                             "in die **erste Zeile** von `galTischbuchungenHeute` einfügen (Galerie markieren, Stift-Symbol der Vorlage, dann Einfügen)")
alt = ist["btnHitArea.OnSelect"]
start = alt.index("Set(varSelectedTisch, ThisItem);")
ende = alt.index("Set(varTagSo, false)") + len("Set(varTagSo, false)")
oeffnen = alt[start:ende]
assert oeffnen.count("Reset(ddEnde);") == 1 and "Set(varZeigeDialog, true);" in oeffnen
oeffnen = oeffnen.replace("Set(varSelectedTisch, ThisItem);", "Set(varSelectedTisch, varNeuBuchenTisch);")
oeffnen = oeffnen.replace("Reset(dpDatum);", 'Set(varEndeOverride, Text(ThisItem.Endzeit, "hh:mm"));\n      Reset(dpDatum);')
oeffnen = "\n".join(z[2:] if z.startswith("      ") else z for z in oeffnen.split("\n"))
neu_onselect = ("If(\n  !varIsLoading,\n"
                "  Set(varNeuBuchenTisch, LookUp(Tische, Titel = ThisItem.Tisch.Value));\n"
                "  If(\n    IsBlank(varNeuBuchenTisch.ID),\n"
                '    Notify("Diesen Tisch gibt es nicht mehr.", NotificationType.Warning),\n'
                "    varNeuBuchenTisch.Gesperrt,\n"
                '    Notify("Dieser Tisch ist zurzeit gesperrt.", NotificationType.Warning),\n'
                "    " + oeffnen + "\n  )\n)")
for k, v in {
    "btnNeuBuchenHeute.Text": '"Neu buchen"',
    "btnNeuBuchenHeute.X": "lblStatusHeute.X",
    "btnNeuBuchenHeute.Y": "lblStatusHeute.Y + 5",
    "btnNeuBuchenHeute.Width": "120",
    "btnNeuBuchenHeute.Height": "30",
    "btnNeuBuchenHeute.Size": "11",
    "btnNeuBuchenHeute.Fill": 'ColorValue("#171496")',
    "btnNeuBuchenHeute.Color": "Color.White",
    "btnNeuBuchenHeute.HoverFill": "ColorFade(Self.Fill, -20%)",
    "btnNeuBuchenHeute.PressedFill": "ColorFade(Self.Fill, -30%)",
    "btnNeuBuchenHeute.PressedColor": "Color.White",
    "btnNeuBuchenHeute.BorderThickness": "0",
    "btnNeuBuchenHeute.RadiusTopLeft": "8", "btnNeuBuchenHeute.RadiusTopRight": "8",
    "btnNeuBuchenHeute.RadiusBottomLeft": "8", "btnNeuBuchenHeute.RadiusBottomRight": "8",
    "btnNeuBuchenHeute.Visible": NEU_SICHTBAR,
    "btnNeuBuchenHeute.DisplayMode": "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
    "btnNeuBuchenHeute.AccessibleLabel": '"Tisch " & ThisItem.Tisch.Value & " neu buchen"',
    "btnNeuBuchenHeute.OnSelect": neu_onselect,
}.items():
    final[k] = v
    herkunft[k] = "R2"
final["lblStatusHeute.Visible"] = "!btnNeuBuchenHeute.Visible"
herkunft["lblStatusHeute.Visible"] = "R2"

# --- R3 Kachel-Dialog: Ende-Vorgabe aus „Neu buchen“ nicht stehen lassen -------------------------------------------------
k = "btnHitArea.OnSelect"
assert ist[k].count("Set(varSelectedTisch, ThisItem);") == 1
final[k] = ist[k].replace("Set(varSelectedTisch, ThisItem);", 'Set(varSelectedTisch, ThisItem);\n      Set(varEndeOverride, "");')
herkunft[k] = "R3"

# --- Prüfungen ---------------------------------------------------------------------------------------------------------
fehler = []
end = dict(stand); end.update(final)
gesetzt = {m.group(1) for v in end.values() for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v)}
STEUER = set(f.typ) | set(NEUE)
for k, v in final.items():
    o = A.ausserhalb_strings(v)
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for x in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if x not in gesetzt:
            fehler.append(f"{k}: Variable {x} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr|rec|Timer)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in STEUER:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")
    if re.search(r"(Patch|Remove|Collect)\(\s*Tischbuchungen", o):
        fehler.append(f"{k}: schreibt (Nachtrag 6 soll nicht schreiben)")
    if o.count("Tischbuchungen") > A.ausserhalb_strings(ist.get(k, "")).count("Tischbuchungen"):
        fehler.append(f"{k}: neue Abfrage auf Tischbuchungen")
# „Neu buchen“ öffnet den Dialog genau wie die Kachel (gleiche Rücksetzungen), nur Tisch und Ende-Vorgabe anders
ref = ist["btnHitArea.OnSelect"]
for anw in re.findall(r"(?:Set|Reset)\([^;]*?\)(?=;|\n|$)", ref[start:ende]):
    if anw.startswith("Set(varSelectedTisch"):
        continue
    if anw not in final["btnNeuBuchenHeute.OnSelect"]:
        fehler.append(f"Neu buchen: fehlt gegenüber der Kachel: {anw}")
# Rücksetzen der Ende-Vorgabe vor Reset(ddEnde) an beiden Öffnern
for k in ["btnHitArea.OnSelect", "btnNeuBuchenHeute.OnSelect"]:
    v = final[k]
    if not (v.index("Set(varEndeOverride") < v.index("Reset(ddEnde)")):
        fehler.append(f"{k}: Ende-Vorgabe nach Reset(ddEnde)")
if final["btnHitArea.OnSelect"].replace('\n      Set(varEndeOverride, "");', "") != ist["btnHitArea.OnSelect"]:
    fehler.append("btnHitArea.OnSelect: mehr geändert als die Rücksetzung")
# Wer öffnet den Buchungsdialog? Jeder Öffner muss die Ende-Vorgabe setzen
oeffner = [k for k, v in end.items() if re.search(r"Set\(varZeigeDialog, *true", v)]
for k in oeffner:
    if "Set(varEndeOverride" not in end[k]:
        fehler.append(f"{k}: öffnet den Buchungsdialog ohne Ende-Vorgabe")
# Freigabe-Regel identisch zur Statusanzeige (S3b)
for k in ["btnEincheckenHeute.DisplayMode", "btnNeuBuchenHeute.Visible"]:
    if f"ThisItem.Startzeit <= {G} && ThisItem.Erstellt <= {G}" not in final[k]:
        fehler.append(f"{k}: andere Verfallsregel als die Statusanzeige")


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


SCHRITTE = [
    ("R1", "Karte öffnet bei verfallener oder beendeter Buchung keinen Check-in-Dialog", ["btnEincheckenHeute.DisplayMode", "btnEincheckenHeute.DisabledFill", "btnEincheckenHeute.DisabledBorderColor"]),
    ("R2", "Knopf „Neu buchen“ (neu)", [k for k in final if k.startswith("btnNeuBuchenHeute.")] + ["lblStatusHeute.Visible"]),
    ("R3", "Kachel-Dialog: Ende-Vorgabe zurücksetzen", ["btnHitArea.OnSelect"]),
]
zug = [k for _, _, ks in SCHRITTE for k in ks]
if sorted(zug) != sorted(final) or len(zug) != len(set(zug)):
    fehler.append("Schritte decken nicht genau alle Properties ab")
out = []
for sid, t, ks in SCHRITTE:
    for k in ks:
        c, p = k.split(".", 1)
        v0 = ist.get(k)
        out.append(dict(schritt=sid, titel=t, control=c, prop=p, neu=final[k], de=A.to_de(final[k]), herkunft=herkunft[k],
                        vorher_de=A.to_de(v0) if v0 is not None else None,
                        diff=diff(A.to_de(v0), A.to_de(final[k])) if v0 is not None else None,
                        art="neu" if v0 is None else "ersetzen",
                        pfad=f.pfad(c) if c in f.typ else f"(neu) {f.pfad('galTischbuchungenHeute')} > {c}"))
json.dump(dict(app=out, neue=NEUE, oeffner=oeffner), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, 1 neues Steuerelement (btnNeuBuchenHeute). Grundlage: Export 08.10. 14:26 + Nachtrag 5.",
     "Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, keine neue Abfrage und kein Schreiben auf Tischbuchungen (nur „Neu buchen“ liest einmal Tische).",
     "„Neu buchen“ öffnet den Buchungsdialog mit denselben Rücksetzungen wie die Kachel (btnHitArea), nur Tisch und Ende-Vorgabe anders.",
     f"Öffner des Buchungsdialogs: {', '.join(oeffner)}; jeder setzt die Ende-Vorgabe vor Reset(ddEnde).",
     "Verfallsregel in Karte und Knopf zeichengleich mit lblStatusHeute (S3b über Nachtrag 5 N4)."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
