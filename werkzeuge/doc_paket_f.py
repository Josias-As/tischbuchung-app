# Erzeugt arbeit/2026-10-08_PaketF/UEBERGABE_PaketF.md aus paket_f_bloecke.json + werkzeuge/paket_f_text.md.
# Aufruf: python3 -I werkzeuge/paket_f.py && python3 -I werkzeuge/doc_paket_f.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_PaketF")
D = json.load(open(os.path.join(ZIEL, "paket_f_bloecke.json"), encoding="utf-8"))
T, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/paket_f_text.md"), encoding="utf-8").read().split("\n"):
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

out = [T["kopf"], "", T["kurzfassung"], "", T["regel"], "", T["varianten"], "", T["nutzung"], ""]
out += ["## 4. Schritte", "", "| Schritt | Was | Properties | neu anzulegen |", "|---|---|---|---|"]
for sid, titel, ss in schritte:
    neu = sorted({s["control"] for s in ss if s["neues_steuerelement"]})
    out.append(f"| {sid} | {titel} | {len(ss)} | {', '.join('`'+n+'`' for n in neu) or '–'} |")
out.append("")
for sid, titel, ss in schritte:
    out += [f"### {sid} {titel}", "", T[sid], ""]
    neu = []
    for s in ss:
        if s["neues_steuerelement"] and s["control"] not in neu:
            neu.append(s["control"])
    if neu:
        out += ["Neues Steuerelement (zuerst anlegen, Name exakt so): " + ", ".join(f"`{n}` ({D['neue_steuerelemente'][n][0]}, {D['neue_steuerelemente'][n][2]})" for n in neu), ""]
    for s in ss:
        key = f"{s['control']}.{s['prop']}"
        z = f"**`{key}`** · Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**")
        if s["quelle_vorher"]:
            z += f" · vorher: {s['quelle_vorher']}"
        out += [z, "", "```", s["de"], "```", ""]
    out += [f"**Rückfall {sid}:** Fassungen aus Anhang A wieder einsetzen" + (", neues Steuerelement löschen." if neu else "."), ""]
out += [T["handy"], "", T["testbogen"], "", T["texte"], "", T["unsicher"], "", T["spaeter"], ""]
out += ["## Anhang A: Fassungen vor Paket F (für den Rückfall)", "",
        "Je Property die Fassung, die nach dem Gesamtplan gilt (bzw. aus dem Export, wenn der Gesamtplan sie nicht ändert).", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** (Schritt {s['schritt']}, {s['quelle_vorher']})", "", "```", s["vorher_de"], "```", ""]
out += ["## Anhang B: Maschinelle Prüfung", "", "```", open(os.path.join(ZIEL, "pruefung.txt"), encoding="utf-8").read().strip(), "```", "",
        "Bewusst ohne Freigabe-Regel:", ""] + [f"- `{k}`: {v}" for k, v in D["ausgenommen"].items()] + [""]
p = os.path.join(ZIEL, "UEBERGABE_PaketF.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")
