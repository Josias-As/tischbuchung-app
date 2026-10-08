# Erzeugt arbeit/2026-10-08_GrundrissSperre/GRUNDRISS_SPERRE.md aus bloecke.json.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A
Z = os.path.join(A.REPO, "arbeit/2026-10-08_GrundrissSperre")
D = json.load(open(os.path.join(Z, "bloecke.json"), encoding="utf-8"))
T = open(os.path.join(A.REPO, "werkzeuge/grundriss_sperre_text.md"), encoding="utf-8").read().strip()
out = [T, "", "## Blöcke", ""]
akt = None
for s in D["app"]:
    if s["schritt"] != akt:
        akt = s["schritt"]
        out += [f"### {s['schritt']} {s['titel']}", ""]
        if akt == "S4":
            out += ["**Neu anlegen, Namen exakt so:**",
                    "1. `conGrundriss` in der Strukturansicht markieren → Einfügen → Schaltfläche (klassisch) → umbenennen in **`btnGrundrissSperre`**.",
                    "2. `conGrundriss` wieder markieren → Einfügen → Schaltfläche (klassisch) → umbenennen in **`btnGrundrissAktualisieren`**.",
                    "3. **Prüfen in der Strukturansicht:** Beide liegen **in** `conGrundriss`, `btnGrundrissAktualisieren` ganz oben, `btnGrundrissSperre` direkt darunter. Sonst `btnGrundrissAktualisieren` → … → Neu anordnen → Ganz nach vorne.", ""]
    out += [f"#### `{s['control']}.{s['prop']}`", "", f"Ort: `{s['pfad']}` · " + ("**neu setzen**" if s["art"] == "neu" else "**ganze Property ersetzen**"), ""]
    if s["diff"]:
        out += ["Änderung gegenüber dem Stand nach Paket F2.1:", "", "```diff", s["diff"], "```", ""]
    out += ["```", s["de"], "```", ""]
out += ["## Anhang A: Fassungen vor dieser Änderung (Stand nach Paket F2.1, für den Rückfall)", ""]
for s in D["app"]:
    if s["vorher_de"] is not None:
        out += [f"**`{s['control']}.{s['prop']}`** ({s['schritt']}, vorher aus {s['quelle_vorher']})", "", "```", s["vorher_de"], "```", ""]
V = D["variante_streng"]
out += ["## Anhang B: Variante „streng“ für `tmrAktualisieren.OnTimerEnd` (ohne Check-in-Erinnerung)", "",
        "Nur einsetzen, wenn der Timer **gar keine** Abfrage machen soll. Ersetzt den S3-Block für `OnTimerEnd`. Die Check-in-Frage kommt dann nur beim App-Start.", "",
        "Änderung gegenüber S3:", "", "```diff", V["diff"], "```", "", "```", V["de"], "```", ""]
out += ["## Anhang C: Maschinelle Prüfung", "", "```", open(os.path.join(Z, "pruefung.txt"), encoding="utf-8").read().strip(), "```", ""]
p = os.path.join(Z, "GRUNDRISS_SPERRE.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p)
