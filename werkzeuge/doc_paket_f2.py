# Erzeugt arbeit/2026-10-08_PaketF2_1/UEBERGABE_PaketF2_1.md aus paket_f2_bloecke.json + werkzeuge/paket_f2_text.md.
# Aufruf: python3 -I werkzeuge/paket_f2.py && python3 -I werkzeuge/doc_paket_f2.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2_1")
D = json.load(open(os.path.join(ZIEL, "paket_f2_bloecke.json"), encoding="utf-8"))
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/paket_f2_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}

LADE = "Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss`"
NEU = {
    "App.OnStart": "3 Variablen vorbelegt (`varFreigabeMinuten`, `varCheckinGefragtID`, `varAuscheckFrageID`), Check-in-Frage vor der Ladezeile, " + LADE,
    "btnStornieren.OnSelect": "direkt und sicher: Sperre, frisch lesen, nur eigene, IfError, Nachlese, Meldung, " + LADE,
    "btnStornieren.DisplayMode": "neu: grau während des Speicherns",
    "btnStornieren_1.OnSelect": "wie `btnStornieren`, für den Tab",
    "btnStornieren_1.DisplayMode": "neu: grau während des Speicherns",
    "btnStornierenKlein.OnSelect": "Sperre dazu, " + LADE + ". Ablauf und Abfragen wie heute",
    "btnStornierenKlein.DisplayMode": "neu: grau während des Speicherns",
    "btnHitArea.OnSelect": "Buchungen des Tisches holen, verfallene entfernen, dann Dialog oder Popup",
    "ddStockwerk.OnChange": LADE, "dpAnsichtsDatum.OnChange": LADE, "Icon1_1.OnSelect": LADE, "Icon1.OnSelect": LADE,
    "Image6.OnSelect": LADE, "btnHitArea_1.OnSelect": LADE,
    "btnSpeichern.OnSelect": "Grenze, verfallene aus Vorprüfung und Nachlese entfernen, Minuten in der Meldung, " + LADE + ". Nachtrag 4 bleibt",
    "btnSpeichernTischePanel.OnSelect": "wie `btnSpeichern`",
    "btnTischHinzufügen.OnSelect": "eine Zeile: Grenze beim Öffnen setzen",
    "ddTischePanel.Items": "Feld `Aktiv`, nur aktive Buchungen zählen",
    "btn5Std.DisplayMode": "Kollisionsprüfung nur mit aktiven Buchungen", "btn5Std.Fill": "Kollisionsprüfung nur mit aktiven Buchungen",
    "btn9Std.DisplayMode": "Kollisionsprüfung nur mit aktiven Buchungen", "btn9Std.Fill": "Kollisionsprüfung nur mit aktiven Buchungen",
    "btnVerwalten.OnSelect": "nächste Buchung am Tisch ohne verfallene (Collection statt direkter Abfrage)",
    "btnVerwalten_2.OnSelect": "wie `btnVerwalten`, für den Tab",
    "btnVerlängern.OnSelect": "Grenze, Kollision ohne verfallene, neu „zwei Tische“, eigene verfallene → Meldung, " + LADE,
    "btnVerlängern_1.OnSelect": "wie `btnVerlängern`, für den Tab",
    "btnEinchecken.OnSelect": "ersetzt G5: Fenster bis Frist, Prüfung „schon vergeben“ vor und nach dem Check-in, Auschecken = Ende jetzt mit zweitem Tippen, " + LADE,
    "btnEinchecken.DisplayMode": "aus G5: grau während des Speicherns",
    "btnEinchecken.Text": "„Wirklich auschecken?“ nach dem ersten Tippen",
    "btnEincheckenHeute.OnSelect": "setzt die Auscheck-Frage beim Öffnen zurück",
    "lblStatusHeute.Text": "neu „Verfallen“", "lblStatusHeute.Color": "grau bei „Verfallen“",
    "tmrAktualisieren.Duration": "neu (wie G8)", "tmrAktualisieren.Repeat": "neu (wie G8)", "tmrAktualisieren.AutoStart": "neu (wie G8)",
    "tmrAktualisieren.Visible": "neu (wie G8)",
    "tmrAktualisieren.OnTimerEnd": "neu: G8 ohne `varZeigeStornoFrage`, " + LADE + ", Check-in-Erinnerung mit lokaler Vorprüfung",
}
for s in D["app"]:
    assert f"{s['control']}.{s['prop']}" in NEU, s["control"] + "." + s["prop"]

schritte = []
for s in D["app"]:
    if not schritte or schritte[-1][0] != s["schritt"]:
        schritte.append((s["schritt"], s["titel"], []))
    schritte[-1][2].append(s)

out = [T["kopf"], "", T["kurzfassung"], "", T["ausgangslage"], ""]
out += ["## 2. Einfügeliste (D): jede Property genau einmal", "",
        "Reihenfolge: **Vorab-Test (Abschnitt 3) → F1 → F2 → … → F8**. „Im Studio jetzt“ ist die Fassung, gegen die der Diff rechnet.", "",
        "| Schritt | Property | im Studio jetzt | was neu ist |", "|---|---|---|---|"]
for s in D["app"]:
    out.append(f"| {s['schritt']} | `{s['control']}.{s['prop']}` | {s['quelle_vorher'] or '– (neu)'} | {NEU[s['control'] + '.' + s['prop']]} |")
out += ["", "**Nicht mehr einfügen:** G4 (ganz), G5 (steckt in F7), G8 (steckt in F8), Paket F Fassung 1, Nachtrag 3 und 4 (stecken in F4).", ""]
out += [T["vorabtest"], "", "## 4. Schritte", ""]
for sid, titel, ss in schritte:
    out += [f"### {sid} {titel}", "", T[sid], ""]
    neu = [s["control"] for s in ss if s["neues_steuerelement"]]
    if neu:
        n = neu[0]
        out += [f"Neues Steuerelement (zuerst anlegen, Name exakt so): `{n}` ({D['neue_steuerelemente'][n][0]}, {D['neue_steuerelemente'][n][2]})", ""]
    for s in ss:
        key = f"{s['control']}.{s['prop']}"
        out += [f"#### `{key}`", "", f"Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**")
                + (f" · im Studio jetzt: {s['quelle_vorher']}" if s["quelle_vorher"] else ""), ""]
        if s["diff"]:
            out += ["Änderungen gegenüber dem Studio (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", ""]
        out += ["Vollständiger Block zum Einfügen:", "", "```", s["de"], "```", ""]
    out += [f"**Rückfall {sid}:** die Fassungen aus Anhang A wieder einsetzen" + (", neues Steuerelement löschen." if neu else ".") + " Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.", ""]
out += [T["rueckfall"], "", T["fragen"], "", T["testbogen"], "", T["unsicher"], ""]
out += ["## Anhang A: Fassungen im Studio vor diesem Paket (Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']}, {s['quelle_vorher']})", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Prüfung", "", "Maschinell (`werkzeuge/paket_f2.py`):", "", "```", open(os.path.join(ZIEL, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "Unabhängige Prüfung: siehe `../2026-10-08_PaketF2/pruefung_paket_f2.md` (Fassung 2; Fassung 2.1 ändert nur die DropColumns-Schreibweise).", "",
        "Bewusst ohne Freigabe-Regel:", ""] + [f"- `{k}`: {v}" for k, v in D["ausgenommen"].items()] + [""]
g8 = next(s for s in G["app"] if s["control"] == "tmrAktualisieren" and s["prop"] == "OnTimerEnd")["neu"]
alt = " && !varZeigeCheckin && !varZeigeStornoFrage,"
assert g8.count(alt) == 1
g8 = g8.replace(alt, " && !varZeigeCheckin,")
assert A.klammern_ok(g8) and A.from_de(A.to_de(g8)) == g8
out += [T["anhangc"], "", "**`tmrAktualisieren.OnTimerEnd`** (nur ohne Paket F)", "", "```", A.to_de(g8), "```", ""]
out += [T["anhangd"], ""]
for n in D["notfassung"]:
    out += [f"#### `{n['control']}.OnSelect` (Notweg)", "", "Änderungen gegenüber dem Studio:", "", "```diff", n["diff"], "```", "", "Vollständiger Block:", "", "```", n["de"], "```", ""]
p = os.path.join(ZIEL, "UEBERGABE_PaketF2_1.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
