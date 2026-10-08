# Erzeugt arbeit/2026-10-08_Gesamtplan/GESAMTPLAN.md aus gesamtplan_bloecke.json + werkzeuge/gesamtplan_text.md.
# Aufruf: python3 -I werkzeuge/gesamtplan.py && python3 -I werkzeuge/doc_gesamtplan.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan")
D = json.load(open(os.path.join(ZIEL, "gesamtplan_bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/gesamtplan_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); T[k] = []
    elif k:
        T[k].append(z)
T = {x: "\n".join(v).strip() for x, v in T.items()}

schritte = []
for s in D["app"]:
    if not schritte or schritte[-1][0] != s["schritt"]:
        schritte.append((s["schritt"], s["phase"], s["titel"], []))
    schritte[-1][3].append(s)

out = [T["kopf"], "", T["kurzfassung"], "", T["nutzung"], "", T["entscheidungen"], "", T["phase0"], ""]
# Übersicht
out += ["## Übersicht aller App-Schritte", "", "| Schritt | Phase | Was | Properties | neu anzulegen |", "|---|---|---|---|---|"]
for sid, ph, titel, ss in schritte:
    neu = sorted({s["control"] for s in ss if s["neues_steuerelement"]})
    out.append(f"| {sid} | {ph} | {titel} | {len(ss)} | {', '.join('`'+n+'`' for n in neu) or '–'} |")
out.append("")


def block(s):
    key = f"{s['control']}.{s['prop']}"
    z = [f"**`{key}`** · Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**")
         + (" · Herkunft: " + ", ".join(s["herkunft"]) if s["herkunft"] else "")]
    if s["prop"] == "Items.Value":
        z.append("(rechts im Eigenschaftenbereich „Wert“ auswählen, kein Formelfeld)")
    z += ["", "```", s["de"], "```", ""]
    return z


aktuelle_phase = None
for sid, ph, titel, ss in schritte:
    if ph != aktuelle_phase:
        aktuelle_phase = ph
        if f"phase {ph}" in T:
            out += [T[f"phase {ph}"], ""]
        if ph == 2:
            out += [T["GF"], ""]
    out += [f"### {sid} {titel}", ""]
    if sid in T:
        out += [T[sid], ""]
    neu = []
    for s in ss:
        if s["neues_steuerelement"] and s["control"] not in neu:
            neu.append(s["control"])
    if neu:
        out += ["Neue Steuerelemente (zuerst anlegen, Name exakt so): " + ", ".join(f"`{n}` ({D['neue_steuerelemente'][n][0]}, {D['neue_steuerelemente'][n][2]})" for n in neu), ""]
    for s in ss:
        out += block(s)
    if sid == "G8":
        out += [T["GR"], ""]

out += [T["phase 8"], "", T["GH"], ""]
for s in D["handy"]:
    key = f"{s['control']}.{s['prop']}"
    out += [f"**Handy-App `{key}`** · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**"), "", "```", s["de"], "```", ""]
out += [T["phase 9"], "", T["spaeter"], "", T["unsicher"], "", T["testbogen"], ""]

out += ["## Anhang A: Originale für den Rückfall (Export 07.10.)", "",
        "Properties, die es vorher nicht gab: leeren bzw. auf Standard setzen. Neue Steuerelemente: löschen.", ""]
for s in D["app"]:
    if s["orig_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** (Schritt {s['schritt']})", "", "```", s["orig_de"], "```", ""]
for s in D["handy"]:
    if s["orig_de"] is not None:
        out += [f"**Handy-App `{s['control']}.{s['prop']}`**", "", "```", s["orig_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(ZIEL, "pruefung.txt"), encoding="utf-8").read().strip(), "```", ""]
p = os.path.join(ZIEL, "GESAMTPLAN.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
