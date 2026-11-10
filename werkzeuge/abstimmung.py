# Abstimmung aller Pakete (10.11.2026): P0 Design → P1 Für andere buchen v2 → P2 Nachtrag 5 → P3 Nachtrag 6 v2 → P4 Grundriss-Laden v2.
# Wendet die Blöcke der Reihe nach auf den Export 10.11. 08:13 („echt“) an. Jeder Block muss mit seinem „Vorher“ genau auf den Stand
# davor passen. Erzeugt P4 v2 (= Grundriss-Laden v1 + L5) und prüft den Endzustand über alle Pakete hinweg.
# Aufruf: python3 -I werkzeuge/abstimmung.py -> arbeit/2026-11-10_Abgestimmt/ABSTIMMUNG_pruefung.txt, P4_GrundrissLaden_v2/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

R = A.REPO
Z = os.path.join(R, "arbeit/2026-11-10_Abgestimmt")
f = A.lade_desktop_1011_echt()
pj = json.load(open(os.path.join(A.ENTPACKT, "desktop_2026-11-10_echt", "Properties.json"), encoding="utf-8-sig"))
assert pj["Name"] == "Tischbuchung" and pj["DocumentAppType"] == "DesktopOrTablet", "falscher Export"
ist = f.props
fehler, log = [], []


def de(k, v):
    return A.to_de(v, kommentare=(k == "App.Formulas"))


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


def lade(p):
    return json.load(open(os.path.join(R, p), encoding="utf-8"))


P0 = lade("arbeit/2026-11-10_Abgestimmt/P0_Design/bloecke.json")
P1 = lade("arbeit/2026-11-10_Abgestimmt/P1_FuerAndere_v2/bloecke.json")
P2 = lade("arbeit/2026-10-08_Nachtrag5/bloecke.json")
P3 = lade("arbeit/2026-11-10_Abgestimmt/P3_Nachtrag6_v2/bloecke.json")
G1 = lade("arbeit/2026-10-13_GrundrissLaden/bloecke.json")
MUT = os.environ.get("ABST_MUT")   # nur für werkzeuge/abstimmung_mutation.py
if MUT:
    exec(open(os.path.join(R, "werkzeuge", "abstimmung_mutation.py"), encoding="utf-8").read().split("#MUT " + MUT + "\n")[1].split("#ENDE")[0])

stand = dict(ist)
steuer = set(f.typ)
wer = {}          # Property -> Pakete, die sie ändern
neue_namen = {}   # neues Steuerelement -> Paket


stufe1 = {}


def anwenden(pid, bl, neue=()):
    for n in neue:
        if n in steuer:
            fehler.append(f"{pid}: neues Steuerelement {n} gibt es schon ({neue_namen.get(n, 'Export')})")
        steuer.add(n)
        neue_namen[n] = pid
    passt = 0
    for b in bl:
        k = f"{b['control']}.{b['prop']}"
        alt = stand.get(k)
        if b.get("gegen", "").startswith("Stufe"):
            # zweite Stufe (L3): Diff gegen Stufe 1, vorher_de bleibt das Original für den Rückfall-Anhang
            if alt is None or de(k, alt) != stufe1.get(k):
                fehler.append(f"{pid} {k}: Stufe 1 ist nicht der Stand davor")
            else:
                passt += 1
        elif b["vorher_de"] is None:
            if alt is not None:
                fehler.append(f"{pid} {k}: als neu/Standard geliefert, hat aber schon eine Formel")
        elif alt is None or de(k, alt) != b["vorher_de"]:
            fehler.append(f"{pid} {k}: Vorher passt nicht auf den Stand davor")
        else:
            passt += 1
        if b["control"] not in steuer:
            fehler.append(f"{pid} {k}: Steuerelement fehlt")
        stand[k] = b["neu"]
        stufe1[k] = b["de"]
        wer.setdefault(k, []).append(pid)
    log.append(f"{pid}: {len(bl)} Properties, davon {passt} mit Vorher (alle passen genau), {len(bl) - passt} neu/bisher Standard, "
               f"{len(neue)} neue Steuerelemente")


anwenden("P0", P0["app"])
anwenden("P1", P1["app"], P1["neue"])
anwenden("P2", P2["app"])
anwenden("P3", P3["app"], P3["neue"])

# --- P4 v2: Grundriss-Laden v1 + L5 --------------------------------------------------------------------------------
# Befund: Nach L3 liefert Gallery1 Datensätze aus TischeLokal ({ID, Titel, Geschoss, Gesperrt}). btnHitArea setzt
# varSelectedTisch = ThisItem (dieser Typ), „Neu buchen“ (P3) setzt varSelectedTisch = LookUp(Tische, …) (voller Listentyp).
# Zwei Record-Typen in einer Variable (Regel 4). L5: „Neu buchen“ liest aus derselben Quelle wie Gallery1.
k5 = "btnNeuBuchenHeute.OnSelect"
alt5 = stand[k5]
assert alt5.count("LookUp(Tische, Titel = ThisItem.Tisch.Value)") == 1
neu5 = alt5.replace("LookUp(Tische, Titel = ThisItem.Tisch.Value)", "LookUp(TischeLokal, Titel = ThisItem.Tisch.Value)")
P4 = [dict(b) for b in G1["app"]]
for b in P4:
    b.setdefault("art", "ersetzen")
l5 = dict(schritt="L5", titel="„Neu buchen“ liest den Tisch aus TischeLokal (gleicher Typ wie die Grundriss-Kachel)",
          control="btnNeuBuchenHeute", prop="OnSelect", neu=neu5, de=A.to_de(neu5), vorher_de=A.to_de(alt5),
          gegen="Nachtrag 6 v2", diff=diff(A.to_de(alt5), A.to_de(neu5)), art="ersetzen",
          pfad=P3["app"][[x["prop"] for x in P3["app"] if x["control"] == "btnNeuBuchenHeute"].index("OnSelect")]["pfad"])
if not globals().get("OHNE_L5"):
    P4.append(l5)
# Stufe 1 → Endfassung App.Formulas: die zweite Stufe vergleicht gegen Stufe 1 (wie in v1)
anwenden("P4", P4)
os.makedirs(os.path.join(Z, "P4_GrundrissLaden_v2"), exist_ok=True)
if not MUT:
  json.dump(dict(app=P4), open(os.path.join(Z, "P4_GrundrissLaden_v2", "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

end = stand
geaendert = list(wer)

# --- Prüfungen am Endzustand ---------------------------------------------------------------------------------------
formeln = set(re.findall(r"(?m)^\s*([A-Za-zÄÖÜäöü_][\wÄÖÜäöü]*)\s*=(?!=)", A.ausserhalb_strings(end["App.Formulas"])))
gesetzt = {m.group(1) for v in end.values() for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v)}
gesetzt |= {m.group(1) for v in end.values() for m in re.finditer(r"\bAs\s+((?:var|col)\w+)", v)}
for k in geaendert:
    v = end[k]
    km = k == "App.Formulas"
    o = A.ausserhalb_strings(v)
    if not A.klammern_ok(v) or A.from_de(A.to_de(v, kommentare=km), kommentare=km) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for x in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if x not in gesetzt and x not in formeln:
            fehler.append(f"{k}: Variable {x} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr|rec|txt|ico|img|Timer|Gallery|Label|Rectangle|Circle)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in steuer:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")

# Positionen: nach L1 aus OnStart raus, als benannte Formeln da; niemand setzt sie mehr per ClearCollect
for n in ["colTischPositionen", "colTischPositionenUG"]:
    if n not in formeln:
        fehler.append(f"{n}: keine benannte Formel")
    for k, v in end.items():
        if re.search(rf"(ClearCollect|Collect|Clear)\(\s*{n}\b", v):
            fehler.append(f"{k}: füllt {n} noch als Sammlung")

# varSelectedTisch: ein Record-Typ (Quelle wie Gallery1)
quelle = re.match(r"\s*Filter\(\s*(\w+)\s*,", end["Gallery1.Items"]).group(1)
setzer = {}
for k, v in end.items():
    for m in re.finditer(r"Set\(varSelectedTisch, *([^;]*?)\)(?=;|\s*$|\s*\n)", v):
        setzer.setdefault(m.group(1).strip(), []).append(k)
for w, ks in setzer.items():
    ok = w in ("Blank()", "varNeuBuchenTisch") or (w == "ThisItem" and all(f.pfad(k.split(".")[0]).find("Gallery1") >= 0 for k in ks))
    if not ok:
        fehler.append(f"varSelectedTisch wird in {ks} mit {w} gesetzt (anderer Typ?)")
nbt = re.findall(r"Set\(varNeuBuchenTisch, *LookUp\((\w+),", "".join(end.values()))
if nbt != [quelle]:
    fehler.append(f"varNeuBuchenTisch liest aus {nbt}, Gallery1 aus {quelle}")
if quelle == "TischeLokal":
    felder = set(re.findall(r"\{([^}]*)\}", re.search(r"TischeLokal = ForAll\(Tische As T, (\{[^}]*\})", end["App.Formulas"]).group(1))[0].replace(" ", "").split(","))
    felder = {x.split(":")[0] for x in felder}
    for k, v in end.items():
        c = k.split(".")[0]
        lesen = set(re.findall(r"varSelectedTisch\.(\w+)", v)) | set(re.findall(r"varNeuBuchenTisch\.(\w+)", v))
        if c in f.typ and "Gallery1" in f.pfad(c) and c != "Gallery1":
            lesen |= set(re.findall(r"ThisItem\.(\w+)", v))
        if lesen - felder:
            fehler.append(f"{k}: liest {sorted(lesen - felder)}, TischeLokal hat nur {sorted(felder)}")

# Jeder Öffner des Buchungsdialogs setzt alles zurück, was die Pakete brauchen
PFLICHT = ["Reset(tglFuerAndere)", "Reset(txtGastName)", "Set(varFbTrotzdem, false)", "Set(varEndeOverride", "Reset(dpDatum)", "Reset(ddEnde)"]
oeffner = sorted(k for k, v in end.items() if re.search(r"Set\(varZeigeDialog, *true", v))
for k in oeffner:
    for p_ in PFLICHT:
        if p_ not in end[k]:
            fehler.append(f"{k}: öffnet den Buchungsdialog ohne {p_}")
    if end[k].index("Set(varEndeOverride") > end[k].index("Reset(ddEnde)"):
        fehler.append(f"{k}: Ende-Vorgabe nach Reset(ddEnde)")
oeffner_panel = sorted(k for k, v in end.items() if re.search(r"Set\(varZeigeTischBuchungForm, *true", v))
for k in oeffner_panel:
    for p_ in ["Reset(tglFuerAnderePanel)", "Reset(txtGastNamePanel)", "Set(varFbTrotzdem, false)"]:
        if p_ not in end[k]:
            fehler.append(f"{k}: öffnet das Panel ohne {p_}")

# Schreibstellen: Zweifach-Sperre; Ladezeile überall gleich
schreib = sorted(k for k, v in end.items() if re.search(r"(Patch|Remove|RemoveIf)\(\s*Tischbuchungen", A.ausserhalb_strings(v)))
for k in schreib:
    v = end[k]
    if "!varIsLoading" not in v or "varSperreBis" not in v:
        fehler.append(f"{k}: Schreibstelle ohne Zweifach-Sperre")
def ladezeilen(v):
    i = 0
    while True:
        i = v.find("With({neu: ForAll(Filter(Tischbuchungen, (Endzeit > varAnsichtsDatum", i)
        if i < 0:
            return
        tiefe, j, instr = 0, i, False
        while j < len(v):
            c = v[j]
            if c == '"':
                instr = not instr
            elif not instr and c == "(":
                tiefe += 1
            elif not instr and c == ")":
                tiefe -= 1
                if tiefe == 0:
                    break
            j += 1
        yield v[i:j + 1]
        i = j


ladez = {}
for k, v in end.items():
    for t in ladezeilen(v):
        t = re.sub(r'Notify\("[^"]*"', 'Notify("…"', t)
        t = t.replace('; Notify("…", NotificationType.Success)', "")   # Aktualisieren-Knöpfe melden zusätzlich Erfolg
        ladez.setdefault(t, []).append(k)
if len(ladez) != 1:
    fehler.append(f"Ladezeile in {len(ladez)} Fassungen")
nlade = sum(len(x) for x in ladez.values())
for k in schreib:
    if not any(k in x for x in ladez.values()):
        fehler.append(f"{k}: Schreibstelle ohne Ladezeile")
if not end["App.OnStart"].rstrip().endswith(")") or "colGrundriss" not in end["App.OnStart"].split("Set(varJetztTakt")[0][-3000:]:
    pass
# Ladezeile vor dem letzten Stempel am Ende von OnStart (usenonblockingonstartrule)
on = end["App.OnStart"]
if on.rfind("ClearCollect(colGrundriss") < 0 or on.rfind("ClearCollect(colGrundriss") > on.rfind("Set(varJetztTakt"):
    fehler.append("App.OnStart: varJetztTakt nicht zuletzt nach der Ladezeile")

# Freigabe-Regel: überall dieselbe Grenze (Coalesce(varFreigabeMinuten, 30))
for k, v in end.items():
    for m in re.finditer(r"varFreigabeMinuten, *(\d+)", v):
        if m.group(1) != "30":
            fehler.append(f"{k}: Freigabe-Grenze {m.group(1)}")

# GastName: wo aus Sammlungen gelesen, muss jede Füllung der Sammlung ihn tragen (je ClearCollect-Aufruf geprüft)
def aufruf(v, i):
    tiefe, j, instr = 0, i, False
    while j < len(v):
        c = v[j]
        if c == '"':
            instr = not instr
        elif not instr and c == "(":
            tiefe += 1
        elif not instr and c == ")":
            tiefe -= 1
            if tiefe == 0:
                return v[i:j + 1]
        j += 1
    return v[i:]


fuellung = {}
for k, v in end.items():
    for m in re.finditer(r"ClearCollect\(\s*(col\w+)\b", v):
        fuellung.setdefault(m.group(1), []).append((k, aufruf(v, m.start())))
gast_sammlungen = set()
for k, v in end.items():
    for m in re.finditer(r"RemoveIf\(\s*(col\w+)\b", v):
        if "GastName" in aufruf(v, m.start()):
            gast_sammlungen.add(m.group(1))
    for m in re.finditer(r"LookUp\(\s*(col\w+)\b", v):
        if "GastName" in aufruf(v, m.start()):
            gast_sammlungen.add(m.group(1))
for c in sorted(gast_sammlungen):
    for k, t in fuellung.get(c, []):
        if "GastName" not in t:
            fehler.append(f"{k}: {c} wird ohne GastName gefüllt, aber mit GastName gelesen")

# Gewählte Buchung (Popup, Verwalten, Check-in) liest GastName: jeder Setzer liefert einen Listendatensatz von Tischbuchungen
voll = dict(ist); voll.update(end)
for k, v in voll.items():
    for m in re.finditer(r"Set\((varSelectedBuchung\w*|varCheckinBuchung), *(LookUp\(\w+|[^,;()]+(?:\(\))?)", v):
        w = m.group(2).strip()
        c = k.split(".")[0]
        gal = next((g for g in ["galTischbuchungenHeute", "galAlleTischbuchungen"] if c in f.typ and g in f.pfad(c)), None)
        ok = w in ("Blank()", "LookUp(Tischbuchungen", "varCheckinBuchung") or (
            w == "ThisItem" and gal is not None and re.search(r"Filter\(\s*Tischbuchungen", voll[gal + ".Items"]))
        if not ok:
            fehler.append(f"{k}: setzt {m.group(1)} mit {w} (kein Datensatz aus Tischbuchungen, GastName fehlt evtl.)")

# Panel-Auswahl: gelesene Felder stehen im Datensatz von ddTischePanel.Items
it = end["ddTischePanel.Items"]
satz = set(re.findall(r"\n\s*(\w+): ", it[it.find("TischeLokal As Ti"):] if "TischeLokal As Ti" in it else it))
for k, v in end.items():
    lesen = set(re.findall(r"ddTischePanel\.Selected\.(\w+)", v))
    if lesen - satz:
        fehler.append(f"{k}: liest ddTischePanel.Selected.{sorted(lesen - satz)}, nicht in Items")

mehrfach = {k: v for k, v in wer.items() if len(v) > 1}

# Check-in-Fenster: Bestandsaufnahme (Josias hat am 25.10. Teile auf 60 Min gestellt)
fenster = {}
for k, v in end.items():
    if "colCheckinFrage" in v or "btnEinchecken" in k or k == "Timer1.OnTimerEnd":
        for m in re.finditer(r"Startzeit <= DateAdd\(Now\(\), (\d+), TimeUnit\.Minutes\)|DateAdd\(varCheckinStart, -(\d+)", v):
            fenster.setdefault(k, set()).add(m.group(1) or m.group(2))

z = ["Abstimmung der Pakete, Grundlage Export 10.11. 08:13 („echt“, App „Tischbuchung“, Desktop).",
     "Reihenfolge: P0 Design → P1 Für andere buchen v2 → P2 Nachtrag 5 → P3 Nachtrag 6 v2 → P4 Grundriss-Laden v2 (= v1 + L5).", ""]
z += log
z += ["", f"Zusammen: {len(geaendert)} verschiedene Properties, {sum(len(v) for v in wer.values())} Blöcke, {len(neue_namen)} neue Steuerelemente: "
      + ", ".join(f"{n} ({p})" for n, p in neue_namen.items()),
      "Properties, die mehr als ein Paket ändert (jeweils auf dem Stand des vorigen aufgebaut, Vorher geprüft):"]
z += [f"  {k}: {' → '.join(v)}" for k, v in mehrfach.items()]
z += ["", "Endzustand:",
      f"  Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden: alle {len(geaendert)} geänderten Properties.",
      f"  Öffner Buchungsdialog ({', '.join(oeffner)}): setzen Gast-Schalter, Gastname, „Trotzdem“, Ende-Vorgabe, Datum und Ende zurück.",
      f"  Öffner Panel ({', '.join(oeffner_panel)}): setzen Gast-Schalter, Gastname und „Trotzdem“ zurück.",
      f"  Schreibstellen ({len(schreib)}): alle mit Zweifach-Sperre und Ladezeile. Ladezeile {nlade}× in einer Fassung (Aktualisieren-Knöpfe zusätzlich mit Erfolgsmeldung).",
      f"  varSelectedTisch: Setzer {sorted(setzer)}; Gallery1 und „Neu buchen“ lesen beide aus {quelle}.",
      f"  GastName in jeder Füllung von {', '.join(sorted(gast_sammlungen))} (dort mit GastName gelesen).",
      "  Gewählte Buchung (varSelectedBuchung, …Tab, varCheckinBuchung): jeder Setzer liefert einen Datensatz aus Tischbuchungen (mit GastName).",
      "  Positionen: benannte Formeln, keine Sammlung mehr. Freigabe-Grenze überall 30 Min (Coalesce).",
      "", "Check-in-Fenster (Bestand, nicht geändert):"]
z += [f"  {k}: {', '.join(sorted(v))} Min" for k, v in sorted(fenster.items())]
z += [""] + (["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"])
if not MUT:
    open(os.path.join(Z, "ABSTIMMUNG_pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
    json.dump({k: end[k] for k in geaendert}, open(os.path.join(Z, "endstand.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if not MUT:
    print("\n".join(z))
if MUT:
    print("MUTATION", MUT, "erkannt" if fehler else "NICHT erkannt", fehler[:2])
sys.exit(1 if fehler else 0)
