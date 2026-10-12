# Erzeugt arbeit/2026-10-12_Nachtrag6/NACHTRAG_6.md aus bloecke.json + werkzeuge/nachtrag6_text.md.
# Aufruf: python3 -I werkzeuge/nachtrag6.py && python3 -I werkzeuge/doc_nachtrag6.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

Z = os.path.join(A.REPO, "arbeit/2026-10-12_Nachtrag6")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/nachtrag6_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}

out = [T["kopf"], "", T["kurzfassung"], "", "## Schritte (Reihenfolge R1 → R3)", ""]
akt = None
for s in D["app"]:
    if s["schritt"] != akt:
        akt = s["schritt"]
        out += [f"### {s['schritt']} {s['titel']}", "", T[akt], ""]
    out += [f"#### `{s['control']}.{s['prop']}`", "",
            f"Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**"), ""]
    if s["diff"]:
        out += ["Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", ""]
    out += ["Vollständiger Block:", "", "```", s["de"], "```", ""]
out += [T["unsicher"], "", T["rueckfall"], ""]
out += ["## Anhang A: Fassungen im Export 08.10. 14:26 (Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']})", "", "```", s["vorher_de"], "```", ""]
out += ["`lblStatusHeute.Visible` ist im Export nicht gesetzt (Standard `true`).", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", ""]
p = os.path.join(Z, "NACHTRAG_6.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
