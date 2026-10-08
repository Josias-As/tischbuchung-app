# Nachtrag 4 (08.10.2026): Nachlese der Speichern-Knöpfe ohne Refresh (Performance, zählt bei jeder Buchung).
# Baut auf Nachtrag 3 auf (Refresh im Zweig "nichts gebucht" schon weg) und erzeugt G6- und F4-Blöcke.
# Idee: Die Nachlese ist eine eigene, pro Klick eindeutige Abfrage (untere Grenze um die Sekunden seit Mitternacht
# erweitert). Ein Zwischenspeicher der Vorprüfung kann sie deshalb nicht beantworten (wie L2: eindeutige URL).
# Eigene Zeilen zählt sie über SerienID, gleichzeitige fremde Buchungen über die Überlappung, wie bisher.
# Aufruf: python3 -I werkzeuge/nachtrag3.py && python3 -I werkzeuge/nachtrag4.py
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag4")
os.makedirs(ZIEL, exist_ok=True)
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))
F = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF/paket_f_bloecke.json"), encoding="utf-8"))

# Nachtrag 3 (identisch zu werkzeuge/nachtrag3.py)
N3_ALT = "        NotificationType.Warning\n      );\n      Refresh(Tischbuchungen),\n      Set(varSerienID, Text(GUID()));\n"
N3_NEU = "        NotificationType.Warning\n      ),\n      Set(varSerienID, Text(GUID()));\n"
# Nachtrag 4
VORPRUEF = "ClearCollect(colNeuBelegt, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));"
N4_ALT = ("      Refresh(Tischbuchungen);\n"
          "      ClearCollect(colNeuNachlese, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n")
N4_NEU = ("      Set(varNeuNachVon, DateAdd(varNeuSpanStart, -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1), TimeUnit.Seconds));\n"
          "      ClearCollect(colNeuNachlese, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));\n")
SPERRE = "If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),"
LADE = "ClearCollect(colGrundriss"

fehler, bloecke = [], []
for quelle, D, schritt in [("Gesamtplan", G, "G6"), ("Paket F", F, "F4")]:
    for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
        s = next(x for x in D["app"] if x["control"] == c and x["prop"] == "OnSelect")
        f = s["neu"]
        for alt, name in [(N3_ALT, "Nachtrag 3"), (N4_ALT, "Nachtrag 4"), (VORPRUEF, "Vorprüfung")]:
            if f.count(alt) != 1:
                fehler.append(f"{schritt} {c}: Anker {name} nicht genau einmal ({f.count(alt)})")
        if fehler:
            continue
        n = f.replace(N3_ALT, N3_NEU).replace(N4_ALT, N4_NEU)
        if "Refresh(Tischbuchungen)" in n:
            fehler.append(f"{schritt} {c}: Refresh übrig")
        if len(f) - len(n) != (len(N3_ALT) - len(N3_NEU)) + (len(N4_ALT) - len(N4_NEU)):
            fehler.append(f"{schritt} {c}: mehr als die zwei Stellen geändert")
        # Nachlese muss anders geformt sein als die Vorprüfung, nach dem Patch kommen und varNeuNachVon vorher setzen
        nach = re.search(r"ClearCollect\(colNeuNachlese, Filter\(Tischbuchungen, ([^\n]*)\)\);", n)
        vor = re.search(r"ClearCollect\(colNeuBelegt, Filter\(Tischbuchungen, ([^\n]*)\)\);", n)
        if not nach or not vor or nach.group(1) == vor.group(1):
            fehler.append(f"{schritt} {c}: Nachlese gleich geformt wie die Vorprüfung")
        if not (n.index("Set(varNeuNachVon") < n.index("ClearCollect(colNeuNachlese") and n.index("IfError(\n        Patch(") < n.index("Set(varNeuNachVon")):
            fehler.append(f"{schritt} {c}: Reihenfolge Patch → Grenze → Nachlese stimmt nicht")
        if "With(" in nach.group(1):
            fehler.append(f"{schritt} {c}: With-Lokale im Server-Prädikat")
        # Auswertung unverändert: zählt eigene Zeilen über SerienID, Konflikt über Überlappung
        for muss in ["Set(varNeuAnzahl, CountRows(Filter(colNeuNachlese, SerienID = varSerienID)));",
                     "M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit"]:
            if muss not in n:
                fehler.append(f"{schritt} {c}: Auswertung verändert ({muss[:40]})")
        if not n.startswith(SPERRE) or LADE not in n:
            fehler.append(f"{schritt} {c}: Sperre oder Ladezeile fehlt")
        if not A.klammern_ok(n) or A.from_de(A.to_de(n)) != n:
            fehler.append(f"{schritt} {c}: Klammern/Rückübersetzung")
        if schritt == "F4" and "RemoveIf(colNeuNachlese, SerienID <> varSerienID && " not in n:
            fehler.append(f"{schritt} {c}: Freigabe-Regel in der Nachlese fehlt")
        bloecke.append(dict(schritt=schritt, quelle=quelle, control=c, pfad=s["pfad"], de=A.to_de(n), neu=n))

pruef = [f"{len(bloecke)} Properties (G6 und F4, je btnSpeichern + btnSpeichernTischePanel), Grundlage: Gesamtplan bzw. Paket F + Nachtrag 3.",
         "Je Block geprüft: genau zwei Stellen geändert (Nachtrag 3 + Nachlese), kein Refresh(Tischbuchungen) mehr, Nachlese anders geformt als die Vorprüfung, "
         "Reihenfolge Patch → varNeuNachVon → Nachlese, keine With-Lokale im Server-Prädikat, Auswertung (SerienID-Zählung, Überlappung) unverändert, "
         "Zweifach-Sperre und Ladezeile vorhanden, in F4 die Freigabe-Regel in der Nachlese, Klammern, Rückübersetzung."]
pruef += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
json.dump(bloecke, open(os.path.join(ZIEL, "nachtrag4_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

TEXT = open(os.path.join(A.REPO, "werkzeuge/nachtrag4_text.md"), encoding="utf-8").read().strip()
out = [TEXT, ""]
for sid in ["G6", "F4"]:
    out += [f"## Blöcke für {sid} (statt " + ("G6 in `GESAMTPLAN.md` bzw. Nachtrag 3)" if sid == "G6" else "F4 in `UEBERGABE_PaketF.md` bzw. Nachtrag 3)"), ""]
    for b in [x for x in bloecke if x["schritt"] == sid]:
        out += [f"**`{b['control']}.OnSelect`** · Ort: `{b['pfad']}` · **ganze Property ersetzen**", "", "```", b["de"], "```", ""]
out += ["## Maschinelle Prüfung", "", "```", "\n".join(pruef), "```", ""]
p = os.path.join(ZIEL, "NACHTRAG_4_Nachlese_ohne_Refresh.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(pruef))
print(p)
sys.exit(1 if fehler else 0)
