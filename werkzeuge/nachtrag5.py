# Nachtrag 5 (08.10.2026): Storno-Bestätigung per zweitem Tippen + Korrekturen aus dem Abgleich mit dem Export 08.10. 14:26.
# Grundlage ist der Export (= Studio-Stand), nicht ein Plan. Diff je Property gegen den Export.
# Aufruf: python3 -I werkzeuge/nachtrag5.py -> arbeit/2026-10-08_Nachtrag5/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_fertig()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag5")
os.makedirs(ZIEL, exist_ok=True)
GS = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_GrundrissSperre/bloecke.json"), encoding="utf-8"))
F21 = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2_1/paket_f2_bloecke.json"), encoding="utf-8"))
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))

LOCK = "!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis)"
final, herkunft = {}, {}


def ersetze(k, alt, neu, anzahl=1):
    v = final.get(k, ist[k])
    assert v.count(alt) == anzahl, (k, alt[:60], v.count(alt))
    final[k] = v.replace(alt, neu)


# --- N1 Storno-Bestätigung (Einzel: Dashboard + Tab) -----------------------------------------------------------------
KOPF = LOCK + ",\n  Set(varIsLoading, true);\n"
for knopf, sel in [("btnStornieren", "varSelectedBuchung"), ("btnStornieren_1", "varSelectedBuchungTab")]:
    k = f"{knopf}.OnSelect"
    v = ist[k]
    assert v.startswith("If(\n  " + KOPF) and v.endswith("\n  Set(varIsLoading, false)\n)"), k
    rumpf = v[len("If(\n  " + LOCK + ",\n"):-len("\n)")]
    rumpf_neu = "\n".join("  " + z if z else z for z in rumpf.split("\n"))
    final[k] = ("If(\n  " + LOCK + ",\n"
                f"  If(\n    !(varStornoFrageID > 0 && varStornoFrageID = {sel}.ID),\n"
                f"    Set(varStornoFrageID, {sel}.ID);\n"
                "    Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));\n"
                '    Notify("Wirklich stornieren? Zum Bestätigen auf „Ja, stornieren“ tippen.", NotificationType.Information),\n'
                "    Set(varStornoFrageID, 0);\n"
                + rumpf_neu + "\n  )\n)")
    final[f"{knopf}.Text"] = f'If(varStornoFrageID > 0 && varStornoFrageID = {sel}.ID, "Ja, stornieren", "Stornieren")'
    herkunft[k] = herkunft[f"{knopf}.Text"] = "N1"

# --- N2 Storno-Bestätigung (Mehrfach) --------------------------------------------------------------------------------
AUSWAHL = 'Concat(colAusgewaehlteBuchungen, Text(ID), ",")'
k = "btnStornierenKlein.OnSelect"
v = ist[k]
assert v.startswith("If(\n  " + KOPF) and v.endswith("\n  Set(varIsLoading, false)\n)"), k
rumpf = v[len("If(\n  " + LOCK + ",\n"):-len("\n)")]
rumpf_neu = "\n".join("  " + z if z else z for z in rumpf.split("\n"))
final[k] = ("If(\n  " + LOCK + ",\n"
            f"  If(\n    CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl <> {AUSWAHL},\n"
            f"    Set(varStornoFrageAuswahl, {AUSWAHL});\n"
            "    Set(varSperreBis, DateAdd(Now(), 1, TimeUnit.Seconds));\n"
            '    Notify("Wirklich " & CountRows(colAusgewaehlteBuchungen) & If(CountRows(colAusgewaehlteBuchungen) = 1, " Buchung", " Buchungen") & " stornieren? Zum Bestätigen noch einmal tippen.", NotificationType.Information),\n'
            '    Set(varStornoFrageAuswahl, "");\n'
            + rumpf_neu + "\n  )\n)")
final["btnStornierenKlein.Text"] = (f'If(CountRows(colAusgewaehlteBuchungen) > 0 && varStornoFrageAuswahl = {AUSWAHL}, '
                                    '"Ja, " & CountRows(colAusgewaehlteBuchungen) & " stornieren", "Stornieren")')
herkunft[k] = herkunft["btnStornierenKlein.Text"] = "N2"

# --- N3 Frage beim Öffnen der Verwalten-Dialoge zurücksetzen ---------------------------------------------------------
k = "btnVerwalten.OnSelect"
assert ist[k].startswith("Set(varSelectedBuchung, ThisItem);\n")
final[k] = "Set(varStornoFrageID, 0);\n" + ist[k]
k = "btnVerwalten_2.OnSelect"
assert ist[k].startswith("If(\n  varAuswahlModusAktiv,\n")
final[k] = 'Set(varStornoFrageID, 0);\nSet(varStornoFrageAuswahl, "");\n' + ist[k]
herkunft["btnVerwalten.OnSelect"] = herkunft["btnVerwalten_2.OnSelect"] = "N3"

# --- N4 Fehlende Teile aus früheren Paketen (Export weicht vom eingefügt gemeldeten Stand ab) -------------------------
for s in GS["app"]:
    if s["schritt"] == "S3b":
        k = f"{s['control']}.{s['prop']}"
        final[k] = s["neu"]; herkunft[k] = "N4 (= Grundriss-Sperre S3b)"
for s in F21["app"]:
    if s["control"] == "btn5Std" and s["prop"] == "Fill":
        final["btn5Std.Fill"] = s["neu"]; herkunft["btn5Std.Fill"] = "N4 (= Paket F2.1 F5)"
for s in G["app"]:
    if s["control"] == "recBuchungDanach1" and s["prop"] == "Visible":
        final["recBuchungDanach1.Visible"] = s["neu"]; herkunft["recBuchungDanach1.Visible"] = "N4 (= Gesamtplan G25)"

# --- N5 Raumcode: die letzten Abfragen beim Start (gemessen) hinter die Raumbestätigung stellen ------------------------
for k in ["recBuchungDavor1.X", "recBuchungDavor1.Width", "recBuchungDanach1.X", "recBuchungDanach1.Width"]:
    v = ist[k]
    assert "Raumbuchungen" in v and not v.startswith("If(")
    eingerueckt = "\n".join("  " + z if z else z for z in v.split("\n"))
    final[k] = "If(\n  varZeigeRaumBestätigung,\n" + eingerueckt + ",\n  0\n)"
    herkunft[k] = "N5"

# --- Prüfungen ---------------------------------------------------------------------------------------------------------
fehler = []
end = dict(ist); end.update(final)
gesetzt = set()
for v in end.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
for k, v in final.items():
    o = A.ausserhalb_strings(v)
    if not A.klammern_ok(v) or A.from_de(A.to_de(v)) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for x in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if x not in gesetzt:
            fehler.append(f"{k}: Variable {x} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr|rec)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in f.typ:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")
    if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", o) and LOCK not in v:
        fehler.append(f"{k}: Schreibstelle ohne Sperre")
    if "ClearCollect(colGrundriss" in v and "Set(varGrundrissStand, Now())" not in v:
        fehler.append(f"{k}: Ladezeile ohne Stempel")
    if re.search(r"(Drop|Add|Rename|Show)Columns\([^)]*\"", o):
        fehler.append(f"{k}: Spaltenname als Text")
# Storno: Frage schreibt nichts, Bestätigung = unveränderter Rumpf (nur eingerückt)
for knopf in ["btnStornieren", "btnStornieren_1", "btnStornierenKlein"]:
    v = final[f"{knopf}.OnSelect"]
    frage = v.split("NotificationType.Information),")[0]
    if re.search(r"Remove\(|Patch\(|Tischbuchungen|varIsLoading, true", frage.split(LOCK, 1)[1]):
        fehler.append(f"{knopf}: Frage-Zweig schreibt oder fragt ab")
    if "DateAdd(Now(), 1, TimeUnit.Seconds)" not in frage:
        fehler.append(f"{knopf}: Frage-Zweig ohne 1-s-Sperre")
    rest = v.split("NotificationType.Information),\n", 1)[1]
    rest = rest.split("\n", 1)[1]  # Rücksetzen der Frage
    rest = "\n".join(z[2:] if z.startswith("  ") else z for z in rest[:-len("\n  )\n)")].split("\n"))
    orig = ist[f"{knopf}.OnSelect"][len("If(\n  " + LOCK + ",\n"):-len("\n)")]
    if rest != orig:
        fehler.append(f"{knopf}: Bestätigungs-Zweig weicht vom Export ab")
for k in ["btnVerwalten.OnSelect", "btnVerwalten_2.OnSelect"]:
    if final[k].split("\n", 2 if "_2" in k else 1)[-1] != ist[k]:
        fehler.append(f"{k}: mehr geändert als das Rücksetzen")
# Bestätigung setzt die Frage zurück, bevor geschrieben wird
for knopf, var in [("btnStornieren", "Set(varStornoFrageID, 0);"), ("btnStornieren_1", "Set(varStornoFrageID, 0);"), ("btnStornierenKlein", 'Set(varStornoFrageAuswahl, "");')]:
    v = final[f"{knopf}.OnSelect"]
    if v.index(var) > v.index("Remove("):
        fehler.append(f"{knopf}: Frage wird erst nach dem Schreiben zurückgesetzt")
# Raumcode: keine ungeschützte Abfrage auf Raumbuchungen/Räume mehr außerhalb von Verhaltensformeln
for k, v in end.items():
    c, p = k.split(".", 1)
    if p.startswith("On"):
        continue
    if re.search(r"\b(Raumbuchungen|Räume)\b", A.ausserhalb_strings(v)):
        gate = (re.match(r"\s*If\(\s*varZeigeRaum(Bestätigung|BuchungForm)\s*,", v) or v.startswith("varZeigeRaumBestätigung && ")
                or f.eltern.get(c) == "galRäume")
        if not gate:
            fehler.append(f"{k}: Raum-Abfrage ohne Bedingung")


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


SCHRITTE = [
    ("N1", "Stornieren mit Bestätigung: Dashboard und Tab", ["btnStornieren.OnSelect", "btnStornieren.Text", "btnStornieren_1.OnSelect", "btnStornieren_1.Text"]),
    ("N2", "Mehrfach-Stornieren mit Bestätigung", ["btnStornierenKlein.OnSelect", "btnStornierenKlein.Text"]),
    ("N3", "Frage beim Öffnen zurücksetzen", ["btnVerwalten.OnSelect", "btnVerwalten_2.OnSelect"]),
    ("N4", "Nachholen: im Export fehlende Teile (S3b, F5, G25)", ["lblStatusHeute.Text", "lblStatusHeute.Color", "btn5Std.Fill", "recBuchungDanach1.Visible"]),
    ("N5", "Raumcode: letzte Startabfragen abschalten", ["recBuchungDavor1.X", "recBuchungDavor1.Width", "recBuchungDanach1.X", "recBuchungDanach1.Width"]),
]
zug = [k for _, _, ks in SCHRITTE for k in ks]
if sorted(zug) != sorted(final) or len(zug) != len(set(zug)):
    fehler.append("Schritte decken nicht genau alle Properties ab")
out = []
for sid, t, ks in SCHRITTE:
    for k in ks:
        c, p = k.split(".", 1)
        out.append(dict(schritt=sid, titel=t, control=c, prop=p, neu=final[k], de=A.to_de(final[k]), herkunft=herkunft[k],
                        vorher_de=A.to_de(ist[k]), diff=diff(A.to_de(ist[k]), A.to_de(final[k])), pfad=f.pfad(c)))
json.dump(dict(app=out), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, kein neues Steuerelement. Grundlage: Export 08.10. 14:26 (PCAppfertig).",
     "Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, Schreibstellen mit Sperre, Ladezeile mit Stempel, Spaltennamen als Bezeichner.",
     "Storno: Frage-Zweig schreibt und fragt nicht ab, setzt 1-s-Sperre; Bestätigungs-Zweig = Export-Fassung unverändert (nur eingerückt); Frage wird vor dem Schreiben zurückgesetzt.",
     "Öffnen: an btnVerwalten/btnVerwalten_2 nur das Rücksetzen vorangestellt.",
     "Raumcode: danach keine Raum-Abfrage außerhalb von Verhaltensformeln ohne Bedingung."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
