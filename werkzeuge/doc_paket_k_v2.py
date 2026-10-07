# Erzeugt UEBERGABE_PaketK_v2.md aus bloecke.json (vorher paket_k_v2.py laufen lassen).
# Aufruf: python3 -I werkzeuge/doc_paket_k_v2.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

ZIEL = os.path.join(A.REPO, "arbeit/2026-10-07_PaketK_v2")
S = json.load(open(os.path.join(ZIEL, "bloecke.json"), encoding="utf-8"))
TEXT = open(os.path.join(A.REPO, "werkzeuge/paket_k_v2_text.md"), encoding="utf-8").read()

# Abschnitte aus dem Begleittext: "@@ <Schlüssel>" leitet einen Abschnitt ein.
abschnitte = {}
schluessel = None
for zeile in TEXT.split("\n"):
    if zeile.startswith("@@ "):
        schluessel = zeile[3:].strip()
        abschnitte[schluessel] = []
    elif schluessel:
        abschnitte[schluessel].append(zeile)
abschnitte = {k: "\n".join(v).strip() for k, v in abschnitte.items()}
pv2 = os.path.join(ZIEL, "pruefung_v2.md")
abschnitte["pruefung"] = abschnitte["pruefung"].replace(
    "__PRUEFUNG_V2__", open(pv2, encoding="utf-8").read().strip() if os.path.exists(pv2) else "Noch ausstehend.")

schritte = []
for s in S:
    if not schritte or schritte[-1][0] != s["nr"]:
        schritte.append((s["nr"], []))
    schritte[-1][1].append(s)

TEILE = {"0": "Teil 0: Vorbereitung (zuerst)", "A": "Teil A: Verwalten-Dialoge (Verlängern, Stornieren, Einchecken)",
         "B": "Teil B: Neue Buchung speichern", "C": "Teil C: Tischauswahl im Tische-Panel", "D": "Teil D: Kleinigkeiten"}

out = [abschnitte["kopf"], "", abschnitte["kurzfassung"], "", "## 1. Übersicht", "",
       "| Schritt | Steuerelement.Property | Was | Behebt |", "|---|---|---|---|"]
behebt = json.loads(abschnitte["behebt"])
for nr, ss in schritte:
    props = ", ".join(f"`{s['control']}.{s['prop']}`" for s in ss)
    out.append(f"| {nr} | {props} | {ss[0]['titel']} | {behebt.get(nr, '')} |")
out += ["", abschnitte["entscheidungen"], "", abschnitte["ablauf"], ""]

teil = None
for nr, ss in schritte:
    if ss[0]["teil"] != teil:
        teil = ss[0]["teil"]
        out += [f"## {TEILE[teil]}", ""]
        if f"teil {teil}" in abschnitte:
            out += [abschnitte[f"teil {teil}"], ""]
    out += [f"### {nr} " + ", ".join(f"`{s['control']}.{s['prop']}`" for s in ss), ""]
    if nr in abschnitte:
        out += [abschnitte[nr], ""]
    for s in ss:
        key = f"{s['control']}.{s['prop']}"
        out.append(f"Ort: `{s['pfad']}`")
        out.append("")
        if s["art"] == "neu":
            out.append(f"**`{key}` gibt es heute nicht (Standard). Neu setzen auf:**")
        else:
            n_alt = len(s["orig_de"].split("\n"))
            geaendert = sum(1 for z in s["diff"].split("\n") if z[:1] in "+-" and not z.startswith(("+++", "---")))
            if geaendert and geaendert < n_alt:
                out += [f"Änderung an `{key}` (rot = weg, grün = neu, Rest unverändert):", "```diff", s["diff"], "```"]
            else:
                out.append(f"`{key}` wird komplett neu geschrieben (Original in Anhang 1).")
            out.append("")
            out.append(f"**Einfügen: ganze Property `{key}` ersetzen durch**")
        out += ["", "```", s["de"], "```", ""]
    if f"test {nr}" in abschnitte:
        out += [abschnitte[f"test {nr}"], ""]

for k in ["rueckfall", "unsicher", "testbogen", "pruefung", "spaeter", "regeln"]:
    out += [abschnitte[k], ""]

out += ["## Anhang 1: Originale (Rückfall, aus dem Export vom 07.10.)", ""]
for s in S:
    key = f"{s['control']}.{s['prop']}"
    if s["orig_de"] is None:
        out += [f"### `{key}`", "", "Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).", ""]
    else:
        out += [f"### `{key}`", "", "```", s["orig_de"], "```", ""]

out += ["## Anhang 2: Maschinelle Prüfung", "", "```", open(os.path.join(ZIEL, "pruefung.txt"), encoding="utf-8").read().strip(), "```", ""]

pfad = os.path.join(ZIEL, "UEBERGABE_PaketK_v2.md")
open(pfad, "w", encoding="utf-8").write("\n".join(out))
print(pfad, len("\n".join(out)), "Zeichen")
