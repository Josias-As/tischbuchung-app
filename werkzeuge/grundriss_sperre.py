# Grundriss-Sperre (08.10.2026): Nach varGrundrissSperreSekunden (120) seit dem letzten Laden von colGrundriss
# wird conGrundriss verblasst und gesperrt, nur „Grundriss aktualisieren“ ist bedienbar.
# Ausgangslage: Paket F Fassung 2.1 (F1–F8) im Studio. Zeitstempel an JEDER Ladestelle, Timer nur noch lokal.
# Aufruf: python3 -I werkzeuge/grundriss_sperre.py -> arbeit/2026-10-08_GrundrissSperre/
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_GrundrissSperre")
os.makedirs(ZIEL, exist_ok=True)
F21 = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2_1/paket_f2_bloecke.json"), encoding="utf-8"))
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))
N4 = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Nachtrag4/nachtrag4_bloecke.json"), encoding="utf-8"))

# Studio-Stand = Ist (wie in paket_f2.py) + Paket F2.1
EINGEFUEGT = {"G1", "G2", "G3", "G6", "G7", "G9", "G10", "G11", "G12", "G13", "G15", "G16", "G17", "G18", "G19", "G20", "G25"}
stand = dict(a.props)
for s in G["app"]:
    if s["schritt"] in EINGEFUEGT:
        stand[f"{s['control']}.{s['prop']}"] = s["neu"]
for b in N4:
    if b["schritt"] == "G6":
        stand[f"{b['control']}.OnSelect"] = b["neu"]
for s in F21["app"]:
    stand[f"{s['control']}.{s['prop']}"] = s["neu"]
basis = dict(stand)

final, NEUE = {}, {}
CC = "ClearCollect(colGrundriss, DropColumns(Filter(neu, Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze), Erstellt))"
STEMPEL = "Set(varGrundrissStand, Now())"
LADESTELLEN = sorted(k for k, v in basis.items() if CC in v)
assert len(LADESTELLEN) == 16, LADESTELLEN

# 1) Zeitstempel an jeder Ladestelle (nur bei Erfolg, direkt hinter dem ClearCollect). Der Timer lädt künftig nicht mehr.
for k in LADESTELLEN:
    if k == "tmrAktualisieren.OnTimerEnd":
        continue
    v = basis[k]
    assert v.count(CC) == 1, k
    final[k] = v.replace(CC, CC + "; " + STEMPEL)

# 2) App.OnStart: Einstellung und Takt vorbelegen
k = "App.OnStart"
alt = "Set(varAuscheckFrageID, 0);\n"
assert final[k].count(alt) == 1
final[k] = final[k].replace(alt, alt + "Set(varGrundrissSperreSekunden, 120);\nSet(varJetztTakt, Now());\n")

# 3) Timer: nur noch lokal (kein Refresh, keine Ladezeile), Takt 15 s, Erinnerung höchstens alle 5 Min
t = basis["tmrAktualisieren.OnTimerEnd"]
erinnerung = t[t.index('  If(\n    varAktiverTab = "dashboard"'):t.rindex("\n)")]
assert erinnerung.count("ClearCollect(colCheckinFrage") == 1
erinnerung = erinnerung.replace(
    "    !IsBlank(LookUp(colGrundriss, Name = User().FullName && !Eingecheckt && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes) && Endzeit > Now()).TischName),\n",
    "    Now() >= Coalesce(varErinnerungAb, Now()) &&\n"
    "    !IsBlank(LookUp(colGrundriss, Name = User().FullName && !Eingecheckt && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes) && Endzeit > Now()).TischName),\n"
    "    Set(varErinnerungAb, DateAdd(Now(), 5, TimeUnit.Minutes));\n"
    "    Set(varFreigabeGrenze, DateAdd(Now(), -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes));\n")
assert "varErinnerungAb" in erinnerung
final["tmrAktualisieren.OnTimerEnd"] = (
    "Set(varJetztTakt, Now());\n"
    "If(\n  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab && !varZeigeVerwaltenKlein && !varZeigeCheckin,\n"
    "  If(\n    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today(),\n"
    "    Set(varAnsichtsDatum, Today());\n    Reset(dpAnsichtsDatum);\n    Set(varGrundrissStand, Blank())\n  );\n"
    + erinnerung + "\n)")
final["tmrAktualisieren.Duration"] = "15000"

# 4) Neue Steuerelemente in conGrundriss: Sperrfläche (verblasst, fängt Klicks) und Knopf
ALT_GR = "IsBlank(varGrundrissStand) || varJetztTakt >= DateAdd(varGrundrissStand, Coalesce(varGrundrissSperreSekunden, 120), TimeUnit.Seconds)"
NEUE["btnGrundrissSperre"] = ("Button (Einfügen → Schaltfläche, klassisch)", "conGrundriss",
                              "in `conGrundriss` einfügen (conGrundriss markieren, dann Einfügen)")
NEUE["btnGrundrissAktualisieren"] = ("Button (Einfügen → Schaltfläche, klassisch)", "conGrundriss",
                                     "danach ebenfalls in `conGrundriss` einfügen, er muss **über** `btnGrundrissSperre` liegen")
for k, v in {
    "btnGrundrissSperre.Text": '""', "btnGrundrissSperre.X": "0", "btnGrundrissSperre.Y": "0",
    "btnGrundrissSperre.Width": "Parent.Width", "btnGrundrissSperre.Height": "Parent.Height",
    "btnGrundrissSperre.Visible": ALT_GR,
    "btnGrundrissSperre.Fill": "RGBA(255, 255, 255, 0.65)", "btnGrundrissSperre.HoverFill": "RGBA(255, 255, 255, 0.65)",
    "btnGrundrissSperre.PressedFill": "RGBA(255, 255, 255, 0.65)", "btnGrundrissSperre.BorderThickness": "0",
    "btnGrundrissSperre.FocusedBorderThickness": "0", "btnGrundrissSperre.TabIndex": "-1",
    "btnGrundrissSperre.RadiusTopLeft": "0", "btnGrundrissSperre.RadiusTopRight": "0",
    "btnGrundrissSperre.RadiusBottomLeft": "0", "btnGrundrissSperre.RadiusBottomRight": "0",
    "btnGrundrissSperre.OnSelect": "false",
    "btnGrundrissAktualisieren.Text": '"Grundriss aktualisieren"',
    "btnGrundrissAktualisieren.Width": "280", "btnGrundrissAktualisieren.Height": "56",
    "btnGrundrissAktualisieren.X": "(Parent.Width - Self.Width) / 2", "btnGrundrissAktualisieren.Y": "(Parent.Height - Self.Height) / 2",
    "btnGrundrissAktualisieren.Visible": ALT_GR,
    "btnGrundrissAktualisieren.Fill": 'ColorValue("#171496")', "btnGrundrissAktualisieren.Color": "Color.White",
    "btnGrundrissAktualisieren.HoverFill": "ColorFade(Self.Fill, -20%)", "btnGrundrissAktualisieren.PressedFill": "ColorFade(Self.Fill, -30%)",
    "btnGrundrissAktualisieren.PressedColor": "Color.White", "btnGrundrissAktualisieren.Size": "14",
    "btnGrundrissAktualisieren.FontWeight": "FontWeight.Semibold",
    "btnGrundrissAktualisieren.DisplayMode": "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)",
    "btnGrundrissAktualisieren.AccessibleLabel": '"Grundriss aktualisieren"',
    "btnGrundrissAktualisieren.OnSelect": final["Icon1_1.OnSelect"],
}.items():
    final[k] = v

# --- Prüfungen ---------------------------------------------------------------------------------------------------
fehler = []
end = dict(basis); end.update(final)
for k, v in end.items():
    if CC in v and (CC + "; " + STEMPEL) not in v:
        fehler.append(f"{k}: lädt colGrundriss ohne Zeitstempel")
lade_nachher = sorted(k for k, v in end.items() if CC in v)
if "tmrAktualisieren.OnTimerEnd" in lade_nachher:
    fehler.append("Timer lädt noch")
tm = end["tmrAktualisieren.OnTimerEnd"]
if "Refresh(" in tm or "With({neu:" in tm:
    fehler.append("Timer fragt ab (Refresh/Ladezeile)")
abfr = re.findall(r"(Filter|LookUp)\(\s*Tischbuchungen", tm)
if len(abfr) != 2 or "Now() >= Coalesce(varErinnerungAb, Now())" not in tm:
    fehler.append("Timer: Abfragen nur in der gedrosselten Erinnerung erlaubt")
if not tm.startswith("Set(varJetztTakt, Now());"):
    fehler.append("Timer: Takt nicht unabhängig von offenen Dialogen")
gesetzt = set()
for v in end.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
STEUER = set(a.typ) | {k.split(".")[0] for k in end}
LOCK = "!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis)"
for k, f in final.items():
    o = A.ausserhalb_strings(f)
    if not A.klammern_ok(f) or A.from_de(A.to_de(f)) != f:
        fehler.append(f"{k}: Klammern/Rückübersetzung")
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if v not in gesetzt:
            fehler.append(f"{k}: Variable {v} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in STEUER:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")
    if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", o) and LOCK not in f:
        fehler.append(f"{k}: Schreibstelle ohne Sperre")
    if k in basis:
        rest = f.replace("; " + STEMPEL, "")
        if k not in ("App.OnStart", "tmrAktualisieren.OnTimerEnd", "tmrAktualisieren.Duration") and rest != basis[k]:
            fehler.append(f"{k}: mehr geändert als der Zeitstempel")


def diff(x, y):
    return "\n".join(list(difflib.unified_diff(x.split("\n"), y.split("\n"), lineterm="", n=1))[2:])


SCHRITTE = [
    ("S1", "App-Start: Einstellung 120 Sekunden und Takt", ["App.OnStart"]),
    ("S2", "Zeitstempel an allen übrigen Ladestellen", [k for k in LADESTELLEN if k not in ("App.OnStart", "tmrAktualisieren.OnTimerEnd")]),
    ("S3", "Timer nur noch lokal (ändert F8)", ["tmrAktualisieren.Duration", "tmrAktualisieren.OnTimerEnd"]),
    ("S4", "Sperrfläche und Knopf in conGrundriss (neu)", [k for k in final if k.startswith("btnGrundrissSperre.")] + [k for k in final if k.startswith("btnGrundrissAktualisieren.")]),
]
zug = [k for _, _, ks in SCHRITTE for k in ks]
if sorted(zug) != sorted(final) or len(zug) != len(set(zug)):
    fehler.append("Schritte decken nicht genau alle Properties ab")
out = []
for sid, t, ks in SCHRITTE:
    for k in ks:
        c, p = k.split(".", 1)
        v0 = basis.get(k)
        out.append(dict(schritt=sid, titel=t, control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        vorher_de=A.to_de(v0) if v0 is not None else None, diff=diff(A.to_de(v0), A.to_de(final[k])) if v0 is not None else None,
                        art="neu" if v0 is None else "ersetzen",
                        pfad=a.pfad(c) if c in a.typ else (f"(neu) Screen1 > conGrundriss > {c}" if c in NEUE else "Screen1 > " + c)))
json.dump(dict(app=out, neue=NEUE, ladestellen=LADESTELLEN), open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, 2 neue Steuerelemente (btnGrundrissSperre, btnGrundrissAktualisieren).",
     f"Ladestellen von colGrundriss im F2.1-Stand: {len(LADESTELLEN)} ({', '.join(LADESTELLEN)}).",
     f"Nachher: {len(lade_nachher)} Ladestellen (Timer lädt nicht mehr, neu: btnGrundrissAktualisieren), jede setzt varGrundrissStand bei Erfolg.",
     "Timer: kein Refresh, keine Ladezeile; Abfragen nur in der Check-in-Erinnerung, höchstens alle 5 Minuten und nur mit eigener anstehender Buchung im Grundriss.",
     "Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, Schreibstellen mit Sperre; an Ladestellen nur der Zeitstempel geändert."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
