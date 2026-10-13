# Grundriss-Laden v1 (13.10.2026): Positionen als benannte Formeln, Tische einmal lokal laden.
# Grundlage: Desktop-Export 13.10. 09:59 (quellen/2026-10-13_Desktop/, = Analyse-Paket). Diff je Property gegen den Export.
# Aufruf: python3 -I werkzeuge/grundriss_laden.py -> arbeit/2026-10-13_GrundrissLaden/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

f = A.lade_desktop_1310()
ist = f.props
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-13_GrundrissLaden")
os.makedirs(ZIEL, exist_ok=True)
fehler, notiz = [], []

# props_de.json aus dem Analyse-Paket = dieser Export (bis auf bekannte Anführungszeichen-Reste des PowerShell-Lesers)
pj = json.load(open(os.path.join(A.REPO, "quellen/2026-10-13_Analyse/props_de.json"), encoding="utf-8-sig"))
def _pj(x):
    x = str(x).strip()
    return x[2:].rstrip().rstrip("'").strip() if x.startswith("'=") else x


abw = [k for k in pj if A.to_de(ist[k], True).strip() != _pj(pj[k])]
if set(pj) != set(ist) or abw:
    fehler.append(f"props_de.json weicht vom Export ab: {abw[:5]}")
notiz.append(f"props_de.json = Export 13.10. ({len(pj)} Properties, nach Abzug der Anführungszeichen-Reste 0 Abweichungen)")


def genau_einmal(text, anker, wo):
    n = text.count(anker)
    if n != 1:
        fehler.append(f"{wo}: Anker {n}x statt 1x: {anker[:60]!r}")
    return n == 1


# --- L1 App.OnStart: die zwei ClearCollect-Blöcke der Positionen entfernen -------------------------------------------------
os_alt = ist["App.OnStart"]
bloecke = {}
os_neu = os_alt
for name in ("colTischPositionen", "colTischPositionenUG"):
    anker = f"ClearCollect(\n  {name},\n"
    genau_einmal(os_alt, anker, "App.OnStart")
    i = os_neu.index(anker)
    j = os_neu.index("\n);\n", i) + len("\n);\n")
    bloecke[name] = os_neu[i:j]
    os_neu = os_neu[:i] + os_neu[j:]
if os_neu.rstrip().split("\n")[-1] != "Set(varJetztTakt, Now())":
    fehler.append("App.OnStart: varJetztTakt ist nicht mehr die letzte Anweisung")
if re.search(r"colTischPositionen", os_neu):
    fehler.append("App.OnStart: Positionen noch vorhanden")


def records(block):
    rs = re.findall(r'\{Tisch: "([^"]+)",\s*X: (\d+),\s*Y: (\d+),\s*Ausrichtung: "(\w+)"\}', block)
    if len(rs) != block.count("{Tisch:"):
        fehler.append("Positionsdatensatz nicht lesbar")
    return rs


pos_alt = {n: records(b) for n, b in bloecke.items()}

# --- L2 / L3 App.Formulas ----------------------------------------------------------------------------------------------------
fo_alt = ist["App.Formulas"]


def tabelle(name):
    b = bloecke[name]
    inhalt = b[b.index("\n", b.index(name)) + 1: b.rindex("\n);\n")]   # Datensätze, Zeilen wie im Export
    return f"{name} = Table(\n{inhalt}\n);"


KOPF_POS = ("// Grundriss-Laden 2026-10-13: Positionen als benannte Formeln statt ClearCollect in App.OnStart.\n"
            "// Werden berechnet, wenn eine Kachel sie braucht, also nie leer (keine Kacheln bei 0/0 beim Start). Werte unverändert aus App.OnStart.")
fo_stufe1 = fo_alt.rstrip("\n") + "\n" + KOPF_POS + "\n" + tabelle("colTischPositionen") + "\n" + tabelle("colTischPositionenUG")

NR_ALT = {g: f'Tisch{"Nr" + g} = With({{src: Filter(Tische, Geschoss.Value = "{g}")}}, ForAll(Sequence(CountRows(src)), {{Titel: Index(src, Value).Titel, Nr: Value}}));' for g in ("OG", "UG")}
NR_ALT = {g: v.replace(f"Tisch{'Nr' + g}", f"TischNr{g}") for g, v in NR_ALT.items()}
NR_NEU = {g: v.replace("Filter(Tische, ", "Filter(TischeLokal, ") for g, v in NR_ALT.items()}
LOKAL = ("// Grundriss-Laden 2026-10-13: alle Tische einmal lesen (ForAll = eine Abfrage, danach lokal). Gallery1, TischNrOG/UG und ddTischePanel lesen daraus.\n"
         "// Reihenfolge = Reihenfolge der Liste (nach ID), wie bisher beim Filtern auf Tische. Gesperrt gilt wie bisher ab App-Start.\n"
         "TischeLokal = ForAll(Tische As T, {ID: T.ID, Titel: T.Titel, Geschoss: T.Geschoss, Gesperrt: T.Gesperrt});")
fo_stufe2 = fo_stufe1
for g in ("OG", "UG"):
    genau_einmal(fo_alt, NR_ALT[g], "App.Formulas")
    fo_stufe2 = fo_stufe2.replace(NR_ALT[g], NR_NEU[g])
anker_nr = "// Grundriss-Fix 2026-09-30: laufende Nummer je Tisch"
genau_einmal(fo_alt, anker_nr, "App.Formulas")
fo_stufe2 = fo_stufe2.replace(anker_nr, LOKAL + "\n" + anker_nr)

# --- L3 Gallery1.Items, L4 ddTischePanel.Items -------------------------------------------------------------------------------
GAL_ALT = "Filter(Tische, Geschoss.Value = varAusgewaehltesStockwerk)"
if ist["Gallery1.Items"] != GAL_ALT:
    fehler.append("Gallery1.Items weicht vom erwarteten Export ab")
gal_neu = "Filter(TischeLokal, Geschoss.Value = varAusgewaehltesStockwerk)"
dd_alt = ist["ddTischePanel.Items"]
genau_einmal(dd_alt, "Tische As Ti,", "ddTischePanel.Items")
dd_neu = dd_alt.replace("Tische As Ti,", "TischeLokal As Ti,")

# --- K1 ddStockwerk.SelectionColor (Kleinigkeit, vor dem Go-Live möglich) ------------------------------------------------------
sc_alt = ist["ddStockwerk.SelectionColor"]
sc_neu = "RGBA(32, 54, 71, 1)"


def lum(r, g, b):
    def k(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * k(r) + 0.7152 * k(g) + 0.0722 * k(b)


def kontrast(a, b):
    la, lb = sorted((lum(*a), lum(*b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


sf = tuple(int(x) for x in re.findall(r"\d+", ist["ddStockwerk.SelectionFill"])[:3])
k_alt, k_neu = kontrast((255, 255, 255), sf), kontrast((32, 54, 71), sf)
notiz.append(f"ddStockwerk: Kontrast Schrift/Auswahl alt {k_alt:.2f}:1, neu {k_neu:.2f}:1 (WCAG AA verlangt 4,5:1)")
if not (k_alt < 4.5 <= k_neu):
    fehler.append("Kontrastrechnung passt nicht zur Aussage")
if sc_alt != "RGBA(255, 255, 255, 1)":
    fehler.append("ddStockwerk.SelectionColor weicht vom erwarteten Export ab")

# --- Prüfungen ------------------------------------------------------------------------------------------------------------------
final = {
    "App.OnStart": os_neu,
    "App.Formulas#1": fo_stufe1,
    "App.Formulas": fo_stufe2,
    "Gallery1.Items": gal_neu,
    "ddTischePanel.Items": dd_neu,
    "ddStockwerk.SelectionColor": sc_neu,
}
for k, v in final.items():
    kom = k.startswith("App.Formulas")
    if not A.klammern_ok(v) or A.from_de(A.to_de(v, kom), kom) != v:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    if not kom and "//" in A.ausserhalb_strings(v):
        fehler.append(f"{k}: Kommentar in Verhaltens-/Datenformel")


def definitionen(fo):
    """Namen der benannten Formeln (Zeilen 'Name = ...' auf oberster Ebene, ohne Kommentare)."""
    namen, tiefe = [], 0
    for z in fo.split("\n"):
        s = A.ausserhalb_strings(z.split("//")[0] if not z.lstrip().startswith("//") else "")
        m = re.match(r"^(\w+)\s*=", s)
        if tiefe == 0 and m:
            namen.append(m.group(1))
        tiefe += s.count("(") + s.count("{") + s.count("[") - s.count(")") - s.count("}") - s.count("]")
    return namen


for k in ("App.Formulas#1", "App.Formulas"):
    n = definitionen(final[k])
    if len(n) != len(set(n)):
        fehler.append(f"{k}: doppelte Namen")
    # jede Definition endet mit ';' (deutsch ';;'): Anzahl Definitionen = Anzahl Semikolons auf oberster Ebene
    s = "\n".join(z for z in A.ausserhalb_strings(final[k]).split("\n") if not z.lstrip().startswith("//"))
    tiefe, semis = 0, 0
    for ch in s:
        tiefe += ch in "({[" ; tiefe -= ch in ")}]"
        semis += ch == ";" and tiefe == 0
    if semis != len(n):
        fehler.append(f"{k}: {len(n)} Definitionen, aber {semis} Abschluss-Semikolons")
    notiz.append(f"{k}: {len(n)} benannte Formeln: {', '.join(n)}")
n_alt = definitionen(fo_alt)
n1, n2 = definitionen(fo_stufe1), definitionen(fo_stufe2)
if n1 != n_alt + ["colTischPositionen", "colTischPositionenUG"] or sorted(n2) != sorted(n1 + ["TischeLokal"]):
    fehler.append("App.Formulas: unerwartete Definitionen")
# Bestehender Text bleibt erhalten (Stufe 1 hängt nur an, Stufe 2 ändert nur TischNr und fügt TischeLokal ein)
if not fo_stufe1.startswith(fo_alt.rstrip("\n")):
    fehler.append("App.Formulas Stufe 1 ändert vorhandenen Text")
if fo_stufe2.replace(LOKAL + "\n", "").replace(NR_NEU["OG"], NR_ALT["OG"]).replace(NR_NEU["UG"], NR_ALT["UG"]) != fo_stufe1:
    fehler.append("App.Formulas Stufe 2 ändert mehr als TischNr/TischeLokal")
if os_neu != os_alt.replace(bloecke["colTischPositionen"], "").replace(bloecke["colTischPositionenUG"], ""):
    fehler.append("App.OnStart ändert mehr als die zwei Blöcke")

# Positionen: Werte 1:1 übernommen, Namen eindeutig, passen zur echten Tische-Liste (REST 12.10.)
for name in pos_alt:
    neu = records(re.search(rf"^{name} = Table\((.*?)\n\);", fo_stufe2, re.S | re.M).group(1))
    if neu != pos_alt[name]:
        fehler.append(f"{name}: Werte nicht 1:1")
alle = [r[0] for n in pos_alt for r in pos_alt[n]]
if len(alle) != len(set(alle)):
    fehler.append("Positionen: doppelter Tischname")
rest = json.load(open(os.path.join(A.REPO, "quellen/2026-10-12_TischZeigen/paket/tische_reihenfolge_2026-10-12.json"), encoding="utf-8"))
liste = {t[1]: t[2] for t in rest}
og = {r[0] for r in pos_alt["colTischPositionen"]}
ug = {r[0] for r in pos_alt["colTischPositionenUG"]}
if og != {t for t, g in liste.items() if g == "OG"} or ug != {t for t, g in liste.items() if g == "UG"}:
    fehler.append("Positionen passen nicht zur Tische-Liste vom 12.10.")
notiz.append(f"Positionen: OG {len(og)}, UG {len(ug)} (inkl. Big Table) = Tische-Liste 12.10. (REST, {len(liste)} Zeilen), Namen und Geschoss gleich")
# Nr je Tisch (Galerie-Versatz): Reihenfolge der Liste, bisher wie künftig gleich
for g in ("OG", "UG"):
    reihe = [t[1] for t in rest if t[2] == g]
    notiz.append(f"Nr {g} (Listenreihenfolge 12.10.): " + ", ".join(f"{i + 1}={t.replace(' Desk ', ' ')}" for i, t in enumerate(reihe)))

# Niemand sonst schreibt die Positionen (benannte Formeln sind schreibgeschützt), neue Namen frei
for k, v in ist.items():
    o = A.ausserhalb_strings(v)
    if k != "App.OnStart" and re.search(r"(Collect|ClearCollect|Clear|Remove|RemoveIf|Patch|UpdateIf)\(\s*colTischPositionen", o):
        fehler.append(f"{k} schreibt die Positionen")
    if re.search(r"\bTischeLokal\b", o):
        fehler.append(f"Name TischeLokal schon belegt ({k})")

# Felder: alles, was aus Kachel-Datensätzen gelesen wird, steckt in TischeLokal
FELDER = set(re.findall(r"(\w+): T\.\1\b", LOKAL))   # Felder, die TischeLokal wirklich liefert
gelesen = set()
for k, v in ist.items():
    o = A.ausserhalb_strings(v)
    c = k.split(".")[0]
    if c in ("Rectangle1", "Circle1", "Label1", "btnHitArea", "Gallery1"):
        gelesen |= set(re.findall(r"ThisItem\.(\w+)", o))
    gelesen |= set(re.findall(r"\b(?:varSelectedTisch|varDetailsTisch)\.(\w+)", o))
    if c == "ddTischePanel":
        gelesen |= set(re.findall(r"\bTi\.(\w+)", o))
if not gelesen <= FELDER:
    fehler.append(f"TischeLokal fehlt: {gelesen - FELDER}")
notiz.append(f"Gelesene Felder aus Kachel/Auswahl/Tischliste: {', '.join(sorted(gelesen))} (alle in TischeLokal)")
# varSelectedTisch/varDetailsTisch werden nur aus ThisItem (Gallery1) oder Blank() gefüllt -> ein Record-Typ
for k, v in ist.items():
    for m in re.finditer(r"Set\((varSelectedTisch|varDetailsTisch), ([^)]*\)?)", v):
        if m.group(2) not in ("ThisItem)", "Blank()"):
            fehler.append(f"{k}: {m.group(1)} aus anderer Quelle: {m.group(2)}")
    if re.search(r"Set\((varSelectedTisch|varDetailsTisch), ThisItem", v) and k.split(".")[0] != "btnHitArea":
        fehler.append(f"{k}: setzt Tisch aus einer anderen Galerie")
if f.eltern.get("btnHitArea") != "Gallery1":
    fehler.append("btnHitArea liegt nicht in Gallery1")

def ohne_kommentar(v):
    return "\n".join(z.split("//")[0] for z in A.ausserhalb_strings(v).split("\n"))


# Wer liest Tische direkt? vorher / nachher
end = dict(ist)
end.update({k: v for k, v in final.items() if "#" not in k})
vor = sorted(k for k, v in ist.items() if re.search(r"\bTische\b", ohne_kommentar(v)))
nach = sorted(k for k, v in end.items() if re.search(r"\bTische\b", ohne_kommentar(v)))
if nach != ["App.Formulas", "btnSpeichern.OnSelect", "btnSpeichernTischePanel.OnSelect"]:
    fehler.append(f"Tische direkt gelesen nachher: {nach}")
for k in ("btnSpeichern.OnSelect", "btnSpeichernTischePanel.OnSelect"):
    if "LookUp(Tische, ID = varNeuTischID && Gesperrt = true)" not in ist[k]:
        fehler.append(f"{k}: frische Gesperrt-Prüfung nicht gefunden")
notiz.append(f"Tische direkt gelesen vorher: {', '.join(vor)}")
notiz.append(f"Tische direkt gelesen nachher: {', '.join(nach)} (App.Formulas nur noch in TischeLokal, Speichern prüft Gesperrt weiter frisch am Server)")
if len(re.findall(r"\bTische\b", ohne_kommentar(fo_stufe2))) != 1:
    fehler.append("App.Formulas Stufe 2 liest Tische mehr als einmal")
# Kein ClearCollect einer Sammlung colTische o. Ä. (bewusst keine neue Sammlung)
if re.search(r"\bcolTische\b", "\n".join(end.values())):
    fehler.append("colTische kommt vor")

# Ladezeile unverändert in OnStart
lade = os_alt[os_alt.index("With({neu: ForAll(Filter(Tischbuchungen"):]
lade = lade[:lade.index("\n")]
if lade not in os_neu:
    fehler.append("L2-Ladezeile in OnStart verändert")


# --- Ausgabe -----------------------------------------------------------------------------------------------------------------------
def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


SCHRITTE = [
    ("K1", "Auswahlfarbe der Geschoss-Auswahl lesbar", [("ddStockwerk.SelectionColor", "ddStockwerk.SelectionColor", None)]),
    ("L1", "App.OnStart: Positionen herausnehmen", [("App.OnStart", "App.OnStart", None)]),
    ("L2", "App.Formulas Stufe 1: Positionen als benannte Formeln", [("App.Formulas#1", "App.Formulas", None)]),
    ("L3", "Stufe 2: Tische einmal lokal laden", [("App.Formulas", "App.Formulas", "App.Formulas#1"), ("Gallery1.Items", "Gallery1.Items", None)]),
    ("L4", "Kann: Tischliste im Panel liest dieselben Tische", [("ddTischePanel.Items", "ddTischePanel.Items", None)]),
]
out = []
for sid, t, ks in SCHRITTE:
    for key, prop, gegen in ks:
        c, p = prop.split(".", 1)
        kom = c == "App" and p == "Formulas"
        v0 = final[gegen] if gegen else ist[prop]
        out.append(dict(schritt=sid, titel=t, control=c, prop=p, neu=final[key], de=A.to_de(final[key], kom),
                        vorher_de=A.to_de(ist[prop], kom), gegen="Stufe 1 (L2)" if gegen else "Export 13.10.",
                        diff=diff(A.to_de(v0, kom), A.to_de(final[key], kom)), pfad=f.pfad(c) if c in f.typ else c))
json.dump(dict(app=out), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"Grundriss-Laden v1: {len(out)} Blöcke (6 Properties, App.Formulas zweistufig) in {len(SCHRITTE)} Schritten. Grundlage: Export 13.10. 09:59.",
     "Je Block: Anker genau 1x, Klammern, Rückübersetzung (App.Formulas mit Kommentaren), keine Kommentare in anderen Formeln,",
     "benannte Formeln eindeutig und je mit ';' (deutsch ';;') abgeschlossen, vorhandener Text unverändert, OnStart nur um die zwei Blöcke kürzer,",
     "varJetztTakt bleibt letzte Anweisung, Ladezeile unverändert, Positionen 1:1, keine Schreibzugriffe auf die Positionen, Felder vollständig,",
     "ein Record-Typ für varSelectedTisch/varDetailsTisch, Tische nur noch in TischeLokal + frische Gesperrt-Prüfung beim Speichern."] + notiz
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
