# Erzeugt arbeit/2026-10-26_FuerAndere/UEBERGABE_FuerAndere.md aus bloecke.json + werkzeuge/fuer_andere_text.md.
# Aufruf: python3 -I werkzeuge/fuer_andere.py && python3 -I werkzeuge/doc_fuer_andere.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

Z = os.path.join(A.REPO, "arbeit/2026-10-26_FuerAndere")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/fuer_andere_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}
pp = os.path.join(Z, "pruefung_fuer_andere.md")
geprueft = os.path.exists(pp)
T["kopf"] = T["kopf"].replace("PRUEFSTATUS", "Unabhängig geprüft, Befunde in Abschnitt 6" if geprueft else "**Noch nicht unabhängig geprüft**")
T["pruefung_unabh"] = T["pruefung_unabh"].replace("PRUEFUNG_PLATZHALTER", open(pp, encoding="utf-8").read().strip() if geprueft else "Läuft noch.")
schritt_von = {}
for s in D["app"]:
    schritt_von.setdefault(s["control"], s["schritt"])
T["ablauf"] = T["ablauf"].replace("NEUE_TABELLE", "\n".join(f"| `{n}` | {t} | `{e}` | {schritt_von[n]} |" for n, (t, e) in D["neue"].items()))

out = [T["kopf"], "", T["kurzfassung"], "", T["ablauf"], "", "## 2. Schritte", ""]
akt = None
for sid in ["S2", "S3", "S4", "S5", "S6", "S7", "S8"]:
    bl = [s for s in D["app"] if s["schritt"] == sid]
    out += [f"### {sid} {bl[0]['titel']}", "", T[sid], ""]
    neu = [s for s in bl if s["art"] == "neu" and s["control"] in D["neue"]]
    for c in dict.fromkeys(s["control"] for s in neu):
        ps = [s for s in neu if s["control"] == c]
        kurz = [s for s in ps if "\n" not in s["de"] and len(s["de"]) <= 80]
        lang = [s for s in ps if s not in kurz]
        out += [f"#### `{c}` (neu, {D['neue'][c][0]}, in `{D['neue'][c][1]}`)", "", "| Property | Wert |", "|---|---|"]
        out += [f"| `{s['prop']}` | `{s['de'].replace('|', '¦')}` |" for s in kurz]
        out.append("")
        for s in lang:
            out += [f"`{c}.{s['prop']}`:", "", "```", s["de"], "```", ""]
    for s in [s for s in bl if s["art"] == "neu" and s["control"] not in D["neue"]]:
        out += [f"#### `{s['control']}.{s['prop']}`", "", f"Ort: `{s['pfad']}` · **neu setzen** (im Export nicht gesetzt, Standardwert)", "",
                "Vollständiger Block:", "", "```", s["de"], "```", ""]
    for s in [s for s in bl if s["art"] == "ersetzen"]:
        out += [f"#### `{s['control']}.{s['prop']}`", "", f"Ort: `{s['pfad']}` · **ganze Property ersetzen**", "",
                "Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", "",
                "Vollständiger Block:", "", "```", s["de"], "```", ""]
out += [T["tests"], "", T["rueckfall"], "", T["unsicher"], "", T["pruefung_unabh"], ""]
out += ["## Anhang A: Originale aus dem Export 25.10. 20:09 (Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`**", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "Mutationstest: 8 von 8 absichtlich eingebauten Fehlern erkannt (GastName nicht gespeichert, Altbestand verändert, Panel liest Dialog-Schalter, "
        "Verlängern ohne Bestätigung, unbekannter Knopf im Select, Variable ohne Präfix, Trotzdem blendet selbst aus, Altbestand-Breite fehlt).", ""]
p = os.path.join(Z, "UEBERGABE_FuerAndere.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
