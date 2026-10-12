# Erzeugt arbeit/2026-10-12_TischZeigen2/HANDY_TISCH_ZEIGEN.md aus bloecke.json + werkzeuge/handy_tisch_zeigen_text.md.
# Aufruf: python3 -I werkzeuge/tisch_zeigen_v2.py && python3 -I werkzeuge/handy_tisch_zeigen.py && python3 -I werkzeuge/doc_handy_tisch_zeigen.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

Z = os.path.join(A.REPO, "arbeit/2026-10-12_TischZeigen2")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/handy_tisch_zeigen_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}
out = [T["kopf"], "", T["kurzfassung"], "", T["vorbereitung"], "", "## 2. Schritte", ""]
out += ["**Neue Steuerelemente:**", "", "| Name | Typ | liegt in | Schritt |", "|---|---|---|---|"]
out += [f"| `{n}` | {v['typ']} | `{v['ort']}` | {v['schritt']} |" for n, v in D["neue"].items()] + [""]
akt = None
for s in D["app"]:
    if s["schritt"] != akt:
        akt = s["schritt"]
        out += [f"### {s['schritt']} {s['titel']}", "", T[akt], ""]
    out += [f"#### `{s['control']}.{s['prop']}`", "", f"Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**"), ""]
    if s["diff"]:
        out += ["Änderung gegenüber dem Handy-Export 12.10. 12:05 (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", ""]
    out += ["```", s["de"], "```", ""]
out += [T["test"], "", T["unsicher"], "", T["rueckfall"], "", T["neu"], ""]
out += ["## Anhang A: Fassungen im Handy-Export 12.10. 12:05 (Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']})", "", "```", s["vorher_de"], "```", ""]
out += ["`App.Formulas` ist im Export leer.", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "```", open(os.path.join(Z, "pruefung_tabelle.txt"), encoding="utf-8").read().strip(), "```", ""]
p = os.path.join(Z, "HANDY_TISCH_ZEIGEN.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
