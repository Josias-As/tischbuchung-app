# Erzeugt arbeit/2026-10-08_PaketF2_1/AENDERUNGEN_F2_zu_F2_1.md: nur die geänderten Blöcke, Diff gegen Fassung 2 und gegen das Studio.
import difflib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

alt = {f"{s['control']}.{s['prop']}": s for s in json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2/paket_f2_bloecke.json"), encoding="utf-8"))["app"]}
neu_d = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2_1/paket_f2_bloecke.json"), encoding="utf-8"))
neu = {f"{s['control']}.{s['prop']}": s for s in neu_d["app"]}
assert set(alt) == set(neu)
geaendert = [k for k in neu if alt[k]["neu"] != neu[k]["neu"]]
for k in geaendert:
    a, n = alt[k]["neu"], neu[k]["neu"]
    assert a.replace('), "Erstellt")', "), Erstellt)") == n, k
d = lambda x, y: "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=0))[2:])
out = ["# Paket F: Änderungen von Fassung 2 zu Fassung 2.1 (08.10.2026)", "",
       "**Anlass (belegt):** App-Prüfung nach F1: „Die Funktion ‚DropColumns‘ weist ungültige Argumente auf. Erwarteter Name des Bezeichners“.",
       "",
       "**Änderung:** In der Ladezeile `DropColumns(…; Erstellt)` statt `DropColumns(…; \"Erstellt\")`. Sonst ändert sich **nichts** (maschinell geprüft: alte und neue Fassung unterscheiden sich in jedem Block nur an dieser Stelle).",
       "",
       f"**Betroffen:** {len(geaendert)} von {len(neu)} Properties. Die übrigen {len(neu) - len(geaendert)} sind unverändert.",
       "",
       "**Andere Stellen geprüft:** `AddColumns`, `RenameColumns` und `ShowColumns` kommen weder im Export noch im Gesamtplan, in Paket F2 oder im Handy-Plan vor.",
       "",
       "`SortByColumns(…; \"Startzeit\")` mit Text steht schon im veröffentlichten Export (`galAlleTischbuchungen`, `Label4`/`Label5`, Handy `galMeine`/`galHeute`) und läuft dort (**belegt**). Deshalb bleibt es so.",
       "",
       "Der Generator meldet ab jetzt jeden Spaltennamen als Text in `Add/Drop/Rename/ShowColumns` als Fehler. Gegenprobe gemacht: Die alte Schreibweise wird erkannt.",
       "",
       "**So einfügen:**",
       "- **F1 neu einfügen** mit dem Block unten. Danach OnStart ausführen und die App-Prüfung ansehen.",
       "- Ist `Erstellt` **an anderer Stelle** rot (nicht in `DropColumns`), sofort melden. Das ist dann U1 (Spaltenname), siehe Vorab-Test.",
       "- Für F2 bis F8 die Blöcke aus `UEBERGABE_PaketF2_1.md` nehmen oder die Blöcke hier. Sie sind identisch.",
       "",
       "Die Diffs gegen den Stand im Studio stehen in `UEBERGABE_PaketF2_1.md`.",
       "", "## Geänderte Blöcke", ""]
for k in geaendert:
    s = neu[k]
    out += [f"### {s['schritt']} `{k}`", "", "Änderung gegenüber Fassung 2:", "", "```diff", d(alt[k]["de"], s["de"]), "```", "",
            "Vollständiger Block (Fassung 2.1):", "", "```", s["de"], "```", ""]
p = os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2_1/AENDERUNGEN_F2_zu_F2_1.md")
open(p, "w", encoding="utf-8").write("\n".join(out))
print(p, len(geaendert), "geänderte Properties:", ", ".join(geaendert))
