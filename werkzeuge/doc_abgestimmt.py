# Erzeugt die Dokumente der abgestimmten Pakete (10.11.2026) aus den Blöcken + werkzeuge/abgestimmt_text.md
# (P4 nutzt zusätzlich werkzeuge/grundriss_laden_text.md, unverändert):
#   arbeit/2026-11-10_Abgestimmt/EINSETZPLAN.md, P0_Design/UEBERGABE_P0_Design.md, P1_FuerAndere_v2/UEBERGABE_FuerAndere_v2.md,
#   P3_Nachtrag6_v2/UEBERGABE_Nachtrag6_v2.md, P4_GrundrissLaden_v2/UEBERGABE_GrundrissLaden_v2.md
# Aufruf: python3 -I werkzeuge/abstimmung.py && python3 -I werkzeuge/abstimmung_mutation.py && python3 -I werkzeuge/doc_abgestimmt.py
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

R = A.REPO
Z = os.path.join(R, "arbeit/2026-11-10_Abgestimmt")


def texte(p):
    T, k = {}, None
    for z in open(os.path.join(R, p), encoding="utf-8").read().split("\n"):
        if z.startswith("@@ "):
            k = z[3:].strip(); T[k] = []
        elif k:
            T[k].append(z)
    return {x: "\n".join(v).strip() for x, v in T.items()}


T = texte("werkzeuge/abgestimmt_text.md")
G = texte("werkzeuge/grundriss_laden_text.md")


def lade(p):
    return json.load(open(os.path.join(R, p), encoding="utf-8"))


PAKETE = [
    ("P0", "Design-Korrektur", lade("arbeit/2026-11-10_Abgestimmt/P0_Design/bloecke.json"), "P0_Design/UEBERGABE_P0_Design.md", "maschinell"),
    ("P1", "Für andere buchen v2", lade("arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2/bloecke.json"), "P1_FuerAndere_v2/UEBERGABE_FuerAndere_v2.md",
     "Logik unabhängig (Fassung 1), Stil maschinell"),
    ("P2", "Nachtrag 5", lade("arbeit/2026-10-08_Nachtrag5/bloecke.json"), "../2026-10-08_Nachtrag5/NACHTRAG_5.md", "unabhängig (08.10.)"),
    ("P3", "Nachtrag 6 v2", lade("arbeit/2026-11-10_Abgestimmt/P3_Nachtrag6_v2/bloecke.json"), "P3_Nachtrag6_v2/UEBERGABE_Nachtrag6_v2.md", "maschinell"),
    ("P4", "Grundriss-Laden v2", lade("arbeit/2026-11-10_Abgestimmt/P4_GrundrissLaden_v2/bloecke.json"), "P4_GrundrissLaden_v2/UEBERGABE_GrundrissLaden_v2.md", "maschinell"),
]
INHALT = {"P0": "„Tisch Buchen“ blau, „Heute“ gedrückt lesbar", "P1": "Für andere buchen, weicher Hinweis „Trotzdem“, Gastname in der Anzeige",
          "P2": "Stornieren mit Bestätigung, Nachholen S3b/F5/G25, Raumcode-Abfragen weg, Erinnerung per E-Mail, Tab lädt nur offen",
          "P3": "Verfallene Karte gesperrt, Knopf „Neu buchen“", "P4": "Positionen als benannte Formeln, Tische einmal laden, L5 Typ-Abgleich"}
EXPORT = "Export 10.11. 08:13"

# Basis je Block: wer hat die Property zuletzt vor diesem Block geändert?
zuletzt, basis = {}, {}
for pid, name, D, _, _ in PAKETE:
    for i, b in enumerate(D["app"]):
        k = f"{b['control']}.{b['prop']}"
        basis[(pid, i)] = zuletzt.get(k, EXPORT)
        zuletzt[k] = f"{pid} ({name})" if not (pid == "P4" and b["schritt"] == "L2") else "Stufe 1 (L2)"


def bloecke(pid, D, sids, txt):
    out = []
    neue = D.get("neue", {})
    std = D.get("standard", {})
    idx = {id(b): i for i, b in enumerate(D["app"])}
    for sid in sids:
        bl = [b for b in D["app"] if b["schritt"] == sid]
        out += [f"### {sid} {bl[0]['titel']}", "", txt[sid], ""]
        neu = [b for b in bl if b.get("art") == "neu" and b["control"] in neue]
        for c in dict.fromkeys(b["control"] for b in neu):
            ps = [b for b in neu if b["control"] == c]
            kurz = [b for b in ps if "\n" not in b["de"] and len(b["de"]) <= 80]
            lang = [b for b in ps if b not in kurz]
            info = neue[c]
            out += [f"#### `{c}` (neu, {info[0]}, in `{info[1]}`)", ""]
            if len(info) > 2:
                out += [f"Anlegen: {info[2]}.", ""]
            out += ["| Property | Wert |", "|---|---|"]
            out += [f"| `{b['prop']}` | `{b['de'].replace('|', '¦')}` |" for b in kurz]
            out.append("")
            for b in lang:
                out += [f"`{c}.{b['prop']}`:", "", "```", b["de"], "```", ""]
        for b in [b for b in bl if b.get("art") == "neu" and b["control"] not in neue]:
            s = std.get(f"{b['control']}.{b['prop']}", "Standard")
            out += [f"#### `{b['control']}.{b['prop']}`", "", f"Ort: `{b['pfad']}` · **neu setzen** (bisher nicht gesetzt, Standard `{s}`, Rückfall: `{s}`)", "",
                    "Vollständiger Block:", "", "```", b["de"], "```", ""]
        for b in [b for b in bl if b.get("art", "ersetzen") == "ersetzen"]:
            gg = basis[(pid, idx[id(b)])]
            zusatz = " (Stufe 1)" if b["schritt"] == "L2" else (" (Endfassung)" if gg.startswith("Stufe") else "")
            out += [f"#### `{b['control']}.{b['prop']}`{zusatz}", "", f"Ort: `{b['pfad'].replace('(neu) ', '')}` · **ganze Property ersetzen**", "",
                    f"Änderung gegenüber {gg} (`-` alt, `+` neu):", "", "```diff", b["diff"], "```", "", "Vollständiger Block:", "", "```", b["de"], "```", ""]
    return out


def anhang(pid, D, titel):
    out = [f"## Anhang A: {titel}", ""]
    gesehen = set()
    for b in D["app"]:
        k = f"{b['control']}.{b['prop']}"
        if b["vorher_de"] is None or k in gesehen:
            continue
        gesehen.add(k)
        out += [f"**`{k}`**", "", "```", b["vorher_de"], "```", ""]
    return out


def lies(p):
    return open(os.path.join(R, p), encoding="utf-8").read().strip()


def schreibe(rel, out):
    p = os.path.join(Z, rel)
    open(p, "w", encoding="utf-8").write("\n".join(out))
    print(p, sum(1 for _ in open(p, encoding="utf-8")), "Zeilen")


PK = {pid: (name, D) for pid, name, D, _, _ in PAKETE}
ABST = lies("arbeit/2026-11-10_Abgestimmt/ABSTIMMUNG_pruefung.txt")
MUT = lies("arbeit/2026-11-10_Abgestimmt/ABSTIMMUNG_mutation.txt")
assert ABST.endswith("Prüfung: 0 Fehler"), "Abstimmung hat Fehler"
mut_zahl = MUT.split("\n")[-1]
assert mut_zahl.startswith("11 von 11"), mut_zahl
anhang_b = lambda eigene: ["## Anhang B: Maschinelle Prüfung", "", "Paket allein:", "", "```", eigene, "```", "",
                           "Alle Pakete zusammen (`werkzeuge/abstimmung.py`):", "", "```", ABST, "```", ""]

# --- P0 ------------------------------------------------------------------------------------------------------------
D = PK["P0"][1]
schreibe("P0_Design/UEBERGABE_P0_Design.md",
         [T["P0.kopf"], "", T["P0.kurzfassung"], "", "## 1. Schritt", ""] + bloecke("P0", D, ["P0"], {"P0": T["P0.P0"]})
         + [T["P0.rueckfall"], ""] + anhang("P0", D, "Originale aus dem Export 10.11. 08:13 (Rückfall)")
         + anhang_b(lies("arbeit/2026-11-10_Abgestimmt/P0_Design/pruefung.txt")))

# --- P1 ------------------------------------------------------------------------------------------------------------
D = PK["P1"][1]
schritt_von = {}
for b in D["app"]:
    schritt_von.setdefault(b["control"], b["schritt"])
abl = T["P1.ablauf"].replace("NEUE_TABELLE", "\n".join(f"| `{n}` | {t[0]} | `{t[1]}` | {schritt_von[n]} |" for n, t in D["neue"].items()))
schreibe("P1_FuerAndere_v2/UEBERGABE_FuerAndere_v2.md",
         [T["P1.kopf"], "", T["P1.kurzfassung"], "", abl, "", "## 2. Schritte", ""]
         + bloecke("P1", D, ["S2", "S3", "S4", "S5", "S6", "S7", "S8"], {s: T["P1." + s] for s in ["S2", "S3", "S4", "S5", "S6", "S7", "S8"]})
         + [T["P1.tests"], "", T["P1.rueckfall"], "", T["P1.unsicher"], "", T["P1.pruefung"], ""]
         + anhang("P1", D, "Originale aus dem Export 10.11. 08:13 (Rückfall)")
         + anhang_b(lies("arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2/pruefung.txt")))

# --- P3 ------------------------------------------------------------------------------------------------------------
D = PK["P3"][1]
schreibe("P3_Nachtrag6_v2/UEBERGABE_Nachtrag6_v2.md",
         [T["P3.kopf"], "", T["P3.kurzfassung"], "", "## Schritte (Reihenfolge R1 → R2 → R3)", ""]
         + bloecke("P3", D, ["R1", "R2", "R3"], {s: T["P3." + s] for s in ["R1", "R2", "R3"]})
         + [T["P3.unsicher"], "", T["P3.rueckfall"], ""]
         + anhang("P3", D, "Stand vor P3 (Export 10.11. 08:13, `btnHitArea.OnSelect` nach P1) – Rückfall")
         + anhang_b(lies("arbeit/2026-11-10_Abgestimmt/P3_Nachtrag6_v2/pruefung.txt")))

# --- P4 ------------------------------------------------------------------------------------------------------------
D = PK["P4"][1]
urs = G["ursache"]
alt_typ = "`varSelectedTisch` und `varDetailsTisch` werden nur aus `ThisItem` der Galerie oder mit `Blank()` gefüllt (belegt). Es gibt also nur einen Datensatz-Typ."
assert urs.count(alt_typ) == 1
urs = urs.replace(alt_typ, "`varSelectedTisch` und `varDetailsTisch` wurden im Export 13.10. nur aus `ThisItem` der Galerie oder mit `Blank()` gefüllt (belegt). "
                  "**Seit P3 füllt auch „Neu buchen“ `varSelectedTisch`, deshalb L5.** Danach gibt es wieder nur einen Datensatz-Typ (maschinell geprüft).")
tst = G["tests"]
assert tst.count("| L3 | Tische lokal | Tests 4–8 |") == 1
tst = tst.replace("| L3 | Tische lokal | Tests 4–8 |", "| L3 + L5 | Tische lokal, Neu buchen | Tests 4–8, L5-Test |")
uns = G["unsicher"] + "\n" + T["P4.unsicher_neu"]
txt = {s: G[s] for s in ["K1", "L1", "L2", "L3", "L4"]}
txt["L5"] = T["P4.L5"]
schreibe("P4_GrundrissLaden_v2/UEBERGABE_GrundrissLaden_v2.md",
         [T["P4.kopf"], "", T["P4.kurzfassung"], "", urs, "", T["P4.einfuegen"], "", "## 3. Schritte", ""]
         + bloecke("P4", D, ["K1", "L1", "L2", "L3", "L5", "L4"], txt)
         + [tst, "", G["rueckfall"], "", uns, "", G["pruefung_unabh"], ""]
         + anhang("P4", D, "Originale (Rückfall)") + ["Die Originale stammen aus dem Export 10.11. 08:13 (= Export 13.10. an diesen Stellen), "
                                                      "`btnNeuBuchenHeute.OnSelect` aus P3. Deutsche Schreibweise.", ""]
         + anhang_b(lies("arbeit/2026-10-13_GrundrissLaden/pruefung.txt")))

# --- Einsetzplan ---------------------------------------------------------------------------------------------------
zeilen = []
props_ges = set()
for pid, name, D, doc, gepr in PAKETE:
    n_neu = len(D.get("neue", {}))
    keys = {f"{b['control']}.{b['prop']}" for b in D["app"]}
    props_ges |= keys
    zeilen.append(f"| **{pid}** {name} | {INHALT[pid]} | {len(D['app'])} | {n_neu} | [`{os.path.basename(doc)}`]({doc}) | {gepr} |")
mutliste = "; ".join(z.split(" ", 2)[2].split(" ")[0] for z in MUT.split("\n")[:-1])
mutnamen = {"ohne_L5": "L5 fehlt", "neu_buchen_ohne_gastreset": "„Neu buchen“ ohne Gast-Rücksetzung", "n5_vorher_anders": "Vorher eines N5-Blocks passt nicht",
            "speichern_ohne_sperre": "Speichern ohne Sperre", "colneuich_ohne_gastname": "`colNeuIch` ohne GastName",
            "ladezeile_abweichend": "Ladezeile an einer Stelle anders", "panel_feld_fehlt": "Panel liest ein Feld, das die Liste nicht hat",
            "doppelter_name": "doppelter Steuerelement-Name", "positionen_noch_sammlung": "Positionen noch als Sammlung in OnStart",
            "freigabe_60": "Freigabe-Grenze 60 statt 30", "buchung_aus_sammlung": "gewählte Buchung aus einer Sammlung ohne GastName"}
mutliste = ", ".join(mutnamen[z.split()[1]] for z in MUT.split("\n")[:-1]) + f". Ergebnis: {mut_zahl}"
kurz = T["E.kurzfassung"].replace("PAKET_TABELLE", "\n".join(zeilen)).replace("ZAHL_PROPS", str(len(props_ges)))
dok = ["## 2. Dokumente zum Einfügen", "",
       "| Paket | Dokument | Ordner |", "|---|---|---|"]
for pid, name, D, doc, _ in PAKETE:
    dok.append(f"| {pid} {name} | [`{os.path.basename(doc)}`]({doc}) | `{os.path.dirname(doc) or '.'}` |")
dok += ["", "- **P2 Nachtrag 5:** Dokument vom 08.10. unverändert. Nur sein Abschnitt 3 (Testbogen) ist ersetzt durch Abschnitt 3 hier.",
        "- **Ältere Fassungen** (Für andere buchen v1, Nachtrag 6 v1, Grundriss-Laden v1) **nicht mehr einfügen.** Sie bleiben zum Nachlesen erhalten.",
        "- Design-Prüfung und Skizzen: [`DESIGN_PRUEFUNG.md`](DESIGN_PRUEFUNG.md), Ordner `design/`."]
schreibe("EINSETZPLAN.md",
         [T["E.kopf"].replace("MUTZAHL", mut_zahl), "", kurz, "", T["E.reihenfolge"], ""] + dok + ["", T["E.tests"], "", T["E.rueckfall"], "", T["E.offen"], "",
          T["E.maschinell"].replace("MUTLISTE", mutliste), "", "```", ABST, "```", ""])
