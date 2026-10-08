# Nachtrag 3 (08.10.2026): Refresh im Zweig "nichts gebucht" der beiden Speichern-Knöpfe entfernen (Performance).
# Erzeugt die Varianten für Gesamtplan G6 und Paket F F4 aus deren Blöcken, ändert sonst nichts.
# Aufruf: python3 -I werkzeuge/nachtrag3.py -> arbeit/2026-10-08_Nachtrag3/NACHTRAG_3_Speichern_ohne_Refresh.md
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag3")
os.makedirs(ZIEL, exist_ok=True)
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))
F = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF/paket_f_bloecke.json"), encoding="utf-8"))

ALT = "        NotificationType.Warning\n      );\n      Refresh(Tischbuchungen),\n      Set(varSerienID, Text(GUID()));\n"
NEU = "        NotificationType.Warning\n      ),\n      Set(varSerienID, Text(GUID()));\n"
NACHLESE = "      Refresh(Tischbuchungen);\n      ClearCollect(colNeuNachlese, "
SPERRE = "If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),"

fehler, bloecke = [], []
for quelle, D, schritt in [("Gesamtplan", G, "G6"), ("Paket F", F, "F4")]:
    for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
        s = next(x for x in D["app"] if x["control"] == c and x["prop"] == "OnSelect")
        f = s["neu"]
        if f.count(ALT) != 1:
            fehler.append(f"{schritt} {c}: Anker nicht genau einmal ({f.count(ALT)})")
            continue
        n = f.replace(ALT, NEU)
        if n.count("Refresh(Tischbuchungen)") != 1 or NACHLESE not in n:
            fehler.append(f"{schritt} {c}: Refresh vor der Nachlese fehlt oder doppelt")
        if not n.startswith(SPERRE) or "ClearCollect(colGrundriss" not in n:
            fehler.append(f"{schritt} {c}: Sperre oder Ladezeile fehlt")
        if not A.klammern_ok(n) or A.from_de(A.to_de(n)) != n:
            fehler.append(f"{schritt} {c}: Klammern/Rückübersetzung")
        if len(f) - len(n) != len(ALT) - len(NEU):
            fehler.append(f"{schritt} {c}: mehr als die eine Stelle geändert")
        bloecke.append(dict(schritt=schritt, quelle=quelle, control=c, pfad=s["pfad"], de=A.to_de(n)))

pruef = [f"{len(bloecke)} Properties (G6 und F4, je btnSpeichern + btnSpeichernTischePanel).",
         "Je Block geprüft: genau eine Stelle geändert (Refresh im Zweig „nichts gebucht“ weg), Refresh vor der Nachlese bleibt (genau 1 Refresh), Zweifach-Sperre und Ladezeile vorhanden, Klammern, Rückübersetzung."]
pruef += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]

TEXT = open(os.path.join(A.REPO, "werkzeuge/nachtrag3_text.md"), encoding="utf-8").read().strip()
out = [TEXT, ""]
for sid in ["G6", "F4"]:
    out += [f"## Blöcke für {sid} (statt der {sid}-Blöcke in " + ("`GESAMTPLAN.md`" if sid == "G6" else "`UEBERGABE_PaketF.md`") + ")", ""]
    for b in [x for x in bloecke if x["schritt"] == sid]:
        out += [f"**`{b['control']}.OnSelect`** · Ort: `{b['pfad']}` · **ganze Property ersetzen**", "", "```", b["de"], "```", ""]
out += ["## Maschinelle Prüfung", "", "```", "\n".join(pruef), "```", ""]
p = os.path.join(ZIEL, "NACHTRAG_3_Speichern_ohne_Refresh.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print("\n".join(pruef))
print(p)
sys.exit(1 if fehler else 0)
