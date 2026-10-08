# Erzeugt arbeit/2026-10-08_Handy/UMBAUPLAN_Handy.md aus handy_bloecke.json + werkzeuge/handy_plan_text.md.
# Aufruf: python3 -I werkzeuge/handy_plan.py && python3 -I werkzeuge/doc_handy_plan.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Handy_v2")
D = json.load(open(os.path.join(ZIEL, "handy_bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/handy_plan_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}
schritte = []
for s in D["app"]:
    if not schritte or schritte[-1][0] != s["schritt"]:
        schritte.append((s["schritt"], s["titel"], []))
    schritte[-1][2].append(s)
out = [T["kopf"], "", T["start"], "", T["kurzfassung"], "", T["stand"], "", T["regeln"], "", T["nutzung"], "",
       "## 5. Schritte", "", "| Schritt | Was | Properties |", "|---|---|---|", "| H0 | Vorab-Test „Erstellt“ | – (2 Test-Steuerelemente, danach löschen) |"]
out += [f"| {sid} | {t} | " + ", ".join(f"`{s['control']}.{s['prop']}`" for s in ss) + " |" for sid, t, ss in schritte]
out += ["", "### H0 Vorab-Test „Erstellt“", "", T["H0"], ""]
for sid, t, ss in schritte:
    out += [f"### {sid} {t}", "", T[sid], ""]
    for s in ss:
        out += [f"#### `{s['control']}.{s['prop']}`", "", f"Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**"), ""]
        if s["diff"]:
            out += ["Änderungen gegenüber dem Export 08.10. (`-` alt, `+` neu):", "", "```diff", s["diff"], "```", ""]
        out += ["Vollständiger Block:", "", "```", s["de"], "```", ""]
    out += [f"**Rückfall {sid}:** Fassung aus Anhang A wieder einsetzen" + (" (`ddStart.Default` leeren)." if sid == "H7" else "."), ""]
out += [T["offen"], "", T["testbogen"], "", "## Anhang A: Fassungen im Export 08.10. (Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']})", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(ZIEL, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "Bewusst ohne Freigabe-Regel:", ""] + [f"- `{a}`: {b}" for a, b in D["ausgenommen"].items()] + [""]
p = os.path.join(ZIEL, "UMBAUPLAN_Handy_v2.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
