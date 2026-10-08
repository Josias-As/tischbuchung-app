# Erzeugt arbeit/2026-10-08_Nachtrag5/NACHTRAG_5.md aus bloecke.json + werkzeuge/nachtrag5_text.md.
# Aufruf: python3 -I werkzeuge/nachtrag5.py && python3 -I werkzeuge/doc_nachtrag5.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

Z = os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag5")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/nachtrag5_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}

out = [T["kopf"], "", T["kurzfassung"], "", T["abgleich"], "", "## 2. Schritte (Reihenfolge N1 → N7)", ""]
akt = None
for s in D["app"]:
    if s["schritt"] != akt:
        if akt:
            out += [T[akt], ""]
        akt = s["schritt"]
        out += [f"### {s['schritt']} {s['titel']}", ""]
    out += [f"#### `{s['control']}.{s['prop']}`", "",
            f"Ort: `{s['pfad']}` · **ganze Property ersetzen** · Herkunft: {s['herkunft']}", "",
            "Änderung gegenüber dem Export 08.10. 14:26 (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", "",
            "Vollständiger Block zum Einfügen:", "", "```", s["de"], "```", ""]
out += [T[akt], ""]
out += [T["testbogen"], "", T["unsicher"], "", T["rueckfall"], ""]
out += ["## Anhang A: Fassungen im Export 08.10. 14:26 (Rückfall)", ""]
for s in D["app"]:
    out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']})", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", ""]
p = os.path.join(Z, "NACHTRAG_5.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
