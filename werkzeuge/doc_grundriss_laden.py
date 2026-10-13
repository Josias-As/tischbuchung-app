# Erzeugt arbeit/2026-10-13_GrundrissLaden/UEBERGABE_Grundriss_Laden_v1.md aus bloecke.json + werkzeuge/grundriss_laden_text.md.
# Aufruf: python3 -I werkzeuge/grundriss_laden.py && python3 -I werkzeuge/doc_grundriss_laden.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

Z = os.path.join(A.REPO, "arbeit/2026-10-13_GrundrissLaden")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/grundriss_laden_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}
pp = os.path.join(Z, "pruefung_grundriss_laden.md")
pruef = open(pp, encoding="utf-8").read().strip() if os.path.exists(pp) else "Noch nicht durchgeführt."
T["pruefung_unabh"] = T["pruefung_unabh"].replace("PRUEFUNG_PLATZHALTER", pruef)

out = [T["kopf"], "", T["kurzfassung"], "", T["ursache"], "", T["einfuegen"], "", "## 3. Schritte", ""]
akt = None
for s in D["app"]:
    if s["schritt"] != akt:
        akt = s["schritt"]
        out += [f"### {s['schritt']} {s['titel']}", "", T[akt], ""]
    out += [f"#### `{s['control']}.{s['prop']}`" + (" (Endfassung)" if s["gegen"] != "Export 13.10." else (" (Stufe 1)" if s["schritt"] == "L2" else "")), "",
            f"Ort: `{s['pfad']}` · **ganze Property ersetzen**", "",
            f"Änderung gegenüber {s['gegen']} (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", "",
            "Vollständiger Block:", "", "```", s["de"], "```", ""]
out += [T["tests"], "", T["rueckfall"], "", T["unsicher"], "", T["pruefung_unabh"], ""]
out += ["## Anhang A: Originale (Rückfall)", "", T["anhang_hinweis"], ""]
gesehen = set()
for s in D["app"]:
    key = f"{s['control']}.{s['prop']}"
    if key in gesehen:
        continue
    gesehen.add(key)
    out += [f"**`{key}`**", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "Mutationstest (13.10.): 6 von 6 absichtlich eingebauten Fehlern erkannt (Positionswert geändert, Feld `Gesperrt` fehlt, "
        "zusätzliche Anweisung in `App.OnStart`, `Gallery1.Items` liest weiter `Tische`, fehlendes `;` in `App.Formulas`, `TischNrOG` liest weiter `Tische`).", ""]
p = os.path.join(Z, "UEBERGABE_Grundriss_Laden_v1.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
