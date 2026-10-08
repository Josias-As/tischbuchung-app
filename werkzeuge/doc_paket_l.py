# Erzeugt FEHLER_UMBAUPLAN_STIL_PaketL.md aus paket_l_bloecke.json + paket_l_text.md.
# Aufruf: python3 -I werkzeuge/paket_l.py && python3 -I werkzeuge/doc_paket_l.py
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Kritische_Analyse")
S = json.load(open(os.path.join(ZIEL, "paket_l_bloecke.json"), encoding="utf-8"))
ab, k = {}, None
for z in open(os.path.join(A.REPO, "werkzeuge/paket_l_text.md"), encoding="utf-8").read().split("\n"):
    if z.startswith("@@ "):
        k = z[3:].strip(); ab[k] = []
    elif k:
        ab[k].append(z)
ab = {x: "\n".join(v).strip() for x, v in ab.items()}
out = [ab["kopf"], ""]
nr = None
for s in S:
    if s["nr"] != nr:
        if nr and f"test {nr}" in ab:
            out += [ab[f"test {nr}"], ""]
        nr = s["nr"]
        out += [f"### {nr} {s['titel']}", ""]
    key = f"{s['control']}.{s['prop']}"
    out += [f"**`{key}`** (Ort: `{s['pfad']}`) ersetzen durch:", "", "```", s["de"], "```", ""]
if f"test {nr}" in ab:
    out += [ab[f"test {nr}"], ""]
out += [ab["plaene"], "", ab["stil"], "", ab["verbesserungen"], "", "## Anhang: Originale (Rückfall)", ""]
for s in S:
    out += [f"**`{s['control']}.{s['prop']}`**", "", "```", s["orig_de"] or "(leer)", "```", ""]
a = A.lade_desktop()
ZP = ["Fill", "HoverFill", "PressedFill", "Color", "HoverColor", "PressedColor", "DisabledFill", "SelectionFill",
      "ChevronBackground", "ChevronHoverBackground", "TrueFill", "IconBackground", "BorderColor"]
out += ["## Anhang B: Zustände aller bedienbaren Steuerelemente (Export 07.10., vor Paket K/L)", "",
        "`·` = Standardwert. Erzeugt aus dem Export, nicht von Hand.", "",
        "| Steuerelement | Typ | Ort | " + " | ".join(ZP) + " |", "|" + "---|" * (len(ZP) + 3)]
for c in a.reihenfolge:
    t = a.typ[c].split("@")[0].replace("Classic/", "")
    if t in ("Button", "DropDown", "DatePicker", "Toggle", "CheckBox", "Icon") or a.props.get(c + ".OnSelect", "").strip():
        if t in ("Label", "Rectangle") and a.props.get(c + ".OnSelect", "").strip() == "Select(Parent)":
            continue
        zellen = []
        for p in ZP:
            v = a.props.get(f"{c}.{p}")
            zellen.append("·" if v is None else ("(Formel)" if "\n" in v or len(v) > 45 else "`" + A.to_de(v).replace("|", "\\|") + "`"))
        out.append(f"| `{c}` | {t} | {a.eltern.get(c, '')} | " + " | ".join(zellen) + " |")
p = os.path.join(ZIEL, "FEHLER_UMBAUPLAN_STIL_PaketL.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p)
