# Paket F (08.10.2026): Freigabe nicht eingecheckter Buchungen IN DER APP (ersetzt den Flow G-F) + Storno-Fix.
# Grundlage: Export 07.10. + Endfassungen aus dem Gesamtplan (gesamtplan_bloecke.json). Jede Property genau einmal.
# Regel: Eine Buchung ist "verfallen", wenn sie nicht eingecheckt ist und Beginn UND Buchungszeitpunkt (Erstellt)
# mehr als varFreigabeMinuten zurückliegen. Verfallene Buchungen zählen überall als frei. Es wird nichts gelöscht.
# Server filtert nur nach Zeit/Tisch/Person (belegt delegierbar), CheckedIn/Erstellt werden lokal geprüft.
# Aufruf: python3 -I werkzeuge/paket_f.py -> arbeit/2026-10-08_PaketF/paket_f_bloecke.json + pruefung.txt
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_PaketF")
os.makedirs(ZIEL, exist_ok=True)
G = json.load(open(os.path.join(A.REPO, "arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json"), encoding="utf-8"))

gplan = {f"{s['control']}.{s['prop']}": s for s in G["app"]}
basis = dict(a.props)
basis.update({k: s["neu"] for k, s in gplan.items()})
final, herkunft = {}, {}
NEUE_STEUER = {}


def aktuell(k):
    return final[k] if k in final else basis[k]


def aendere(k, alt, neu, tag, n=1):
    f = aktuell(k)
    assert f.count(alt) == n, (k, alt[:70], f.count(alt))
    final[k] = f.replace(alt, neu)
    herkunft.setdefault(k, []).append(tag)


def setze(k, wert, tag):
    final[k] = wert
    herkunft.setdefault(k, []).append(tag)


GRENZE = "Set(varFreigabeGrenze, DateAdd(Now(), -varFreigabeMinuten, TimeUnit.Minutes))"
VERF = "!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze"


def verf(p):
    return f"!{p}CheckedIn && {p}Startzeit <= varFreigabeGrenze && {p}Erstellt <= varFreigabeGrenze"


# --- Ladezeile L2 -> L2F: lädt Erstellt mit, nimmt verfallene Buchungen nicht in colGrundriss auf -----------------
# Das Schema von colGrundriss bleibt gleich (DropColumns), damit jede Ladestelle einzeln umgestellt werden kann.
L_ALT_KOPF = "With({neu: ForAll(Filter(Tischbuchungen, (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes))) As B, {TischName: B.Tisch.Value, Startzeit: B.Startzeit, Endzeit: B.Endzeit, Eingecheckt: B.CheckedIn, Name: B.Person.DisplayName})}"
L_NEU_KOPF = L_ALT_KOPF.replace("Name: B.Person.DisplayName})}", "Name: B.Person.DisplayName, Erstellt: B.Erstellt})}")
L_ALT_CC = "ClearCollect(colGrundriss, neu)"
L_NEU_CC = 'ClearCollect(colGrundriss, DropColumns(Filter(neu, Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze), "Erstellt"))'


def lade_f(k):
    f = aktuell(k)
    n = f.count(L_ALT_KOPF)
    assert n >= 1 and f.count(L_ALT_CC) == n, (k, n, f.count(L_ALT_CC))
    f = re.sub(r"(?m)^([ \t]*)" + re.escape(L_ALT_KOPF), lambda m: m.group(1) + GRENZE + ";\n" + m.group(1) + L_NEU_KOPF, f)
    assert f.count(L_NEU_KOPF) == n, k
    f = f.replace(L_ALT_CC, L_NEU_CC)
    final[k] = f
    herkunft.setdefault(k, []).append("F Ladezeile")


LADE_STELLEN = [k for k, v in basis.items() if L_ALT_KOPF in v]
assert len(LADE_STELLEN) == 14, LADE_STELLEN
for k in LADE_STELLEN:
    lade_f(k)

# --- F1 App-Start: Einstellung, Grenze, Check-in-Frage ------------------------------------------------------------
FRAGE = ("ClearCollect(colCheckinFrage, Filter(Tischbuchungen, Person.Email = User().Email && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes) && Endzeit > Now()));\n"
         "RemoveIf(colCheckinFrage, CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));\n")
ERSTE = 'First(SortByColumns(colCheckinFrage, "Startzeit", SortOrder.Ascending)).ID'
aendere("App.OnStart", "Set(varSperreBis, Now());\n",
        "Set(varFreigabeMinuten, 30);\nSet(varCheckinGefragtID, 0);\nSet(varSperreBis, Now());\n", "F1 Einstellung")
f = aktuell("App.OnStart")
i = f.rindex(GRENZE + ";\n" + L_NEU_KOPF)
setze("App.OnStart", f[:i] + GRENZE + ";\n" + FRAGE
      + f"If(\n  !IsEmpty(colCheckinFrage),\n  Set(varCheckinGefragtID, {ERSTE});\n"
        "  Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinGefragtID));\n  Set(varZeigeCheckin, true)\n);\n" + f[i:], "F1 Check-in-Frage")

# --- F2 Storno-Fix -------------------------------------------------------------------------------------------------
setze("btnStornieren.OnSelect", 'Set(varStornoID, varSelectedBuchung.ID);\nSet(varStornoQuelle, "dash");\nSet(varZeigeStornoFrage, true)', "F2 Storno")
setze("btnStornieren_1.OnSelect", 'Set(varStornoID, varSelectedBuchungTab.ID);\nSet(varStornoQuelle, "tab");\nSet(varZeigeStornoFrage, true)', "F2 Storno")
aendere("btnStornoJa.OnSelect", "LookUp(Tischbuchungen, ID = varSelectedBuchung.ID)", "LookUp(Tischbuchungen, ID = varStornoID)", "F2 Storno")
aendere("btnStornoJa.OnSelect", "LookUp(Tischbuchungen, ID = varSelectedBuchungTab.ID)", "LookUp(Tischbuchungen, ID = varStornoID)", "F2 Storno")
for v in ["varZeigeVerwalten", "varZeigeVerwaltenTab"]:
    alt = (f'      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning);\n'
           f"      Set({v}, false);\n      IfError(")
    neu = (f'      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning);\n'
           f"      Set({v}, false),\n      Lower(varStornoBuchung.Person.Email) <> Lower(User().Email),\n"
           f'      Notify("Nur eigene Buchungen können storniert werden.", NotificationType.Error),\n      IfError(')
    aendere("btnStornoJa.OnSelect", alt.replace(";\n      IfError(", ",\n      IfError("), neu, "F2 Storno")
NEUE_STEUER["btnStornoHintergrund"] = ("Button (Einfügen → Schaltfläche, klassisch)", "Screen1",
                                       "auf oberster Ebene einfügen, danach `conStornoFrage` markieren → **Nach vorne bringen**")
for k, v in {
    "btnStornoHintergrund.Text": '""', "btnStornoHintergrund.X": "0", "btnStornoHintergrund.Y": "0",
    "btnStornoHintergrund.Width": "Parent.Width", "btnStornoHintergrund.Height": "Parent.Height",
    "btnStornoHintergrund.Visible": "varZeigeStornoFrage",
    "btnStornoHintergrund.Fill": "RGBA(0, 0, 0, 0.35)", "btnStornoHintergrund.HoverFill": "RGBA(0, 0, 0, 0.35)",
    "btnStornoHintergrund.PressedFill": "RGBA(0, 0, 0, 0.35)", "btnStornoHintergrund.BorderThickness": "0",
    "btnStornoHintergrund.FocusedBorderThickness": "0",
    "btnStornoHintergrund.RadiusTopLeft": "0", "btnStornoHintergrund.RadiusTopRight": "0",
    "btnStornoHintergrund.RadiusBottomLeft": "0", "btnStornoHintergrund.RadiusBottomRight": "0",
    "btnStornoHintergrund.OnSelect": "Set(varZeigeStornoFrage, false)",
    "btnStornoHintergrund.AccessibleLabel": '"Abfrage schließen"',
}.items():
    setze(k, v, "F2 Storno neu")

# --- F3 Grundriss-Kachel: verfallene Buchung zählt als frei --------------------------------------------------------
hit = aktuell("btnHitArea.OnSelect")
kopf = 'If(\n  ThisItem.Gesperrt,\n  Notify("Dieser Tisch ist zurzeit gesperrt.", NotificationType.Warning),\n'
assert hit.startswith(kopf)
j = hit.index("    If(\n      IsBlank(relevanteBuchung),")
schluss = "\n  )\n)"
assert hit.endswith(schluss)
inner = hit[j:len(hit) - len(schluss)]
assert inner.count("relevanteBuchung") == 2
inner = inner.replace("IsBlank(relevanteBuchung)", "IsBlank(varKachelID)").replace(
    "Set(varSelectedBuchung, relevanteBuchung)", "Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varKachelID))")
inner = "\n".join(z[2:] if z.startswith("  ") else z for z in inner.split("\n"))
setze("btnHitArea.OnSelect", kopf + "  " + GRENZE + ";\n"
      "  If(\n    varAnsichtsDatum = Today(),\n"
      "    ClearCollect(colKachel, Filter(Tischbuchungen, Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes))),\n"
      "    ClearCollect(colKachel, Filter(Tischbuchungen, Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)))\n"
      "  );\n"
      f"  RemoveIf(colKachel, {VERF});\n"
      "  Set(varKachelID, First(colKachel).ID);\n" + inner + "\n)", "F3 Kachel")

# --- F4 Buchen: verfallene Buchungen blockieren nicht ---------------------------------------------------------------
for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
    k = f"{c}.OnSelect"
    aendere(k, "  Set(varNeuJetzt, DateAdd(Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), TimeUnit.Minutes));\n",
            "  Set(varNeuJetzt, DateAdd(Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), TimeUnit.Minutes));\n  " + GRENZE + ";\n", "F4 Buchen")
    aendere(k, "    ClearCollect(colNeuBelegt, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n",
            "    ClearCollect(colNeuBelegt, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n"
            f"    RemoveIf(colNeuBelegt, {VERF});\n", "F4 Buchen")
    aendere(k, "    ClearCollect(colNeuIch, Filter(Tischbuchungen, Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n",
            "    ClearCollect(colNeuIch, Filter(Tischbuchungen, Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n"
            f"    RemoveIf(colNeuIch, {VERF});\n", "F4 Buchen")
    aendere(k, "      ClearCollect(colNeuNachlese, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n",
            "      ClearCollect(colNeuNachlese, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));\n"
            f"      RemoveIf(colNeuNachlese, SerienID <> varSerienID && {VERF});\n", "F4 Buchen")
    aendere(k, '" Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."',
            '" Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."', "F4 Buchen")

# --- F5 Tisch-buchen-Panel: Liste und 5/9-Std.-Knöpfe ---------------------------------------------------------------
aendere("btnTischHinzufügen.OnSelect", "Set(varPanelJetzt, Now());\n", "Set(varPanelJetzt, Now());\n" + GRENZE + ";\n", "F5 Panel")
aendere("ddTischePanel.Items", "{TischName: Tisch.Value, Beginn: Startzeit, Schluss: Endzeit}",
        "{TischName: Tisch.Value, Beginn: Startzeit, Schluss: Endzeit, Aktiv: CheckedIn || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze}", "F5 Panel")
aendere("ddTischePanel.Items", 'FirstN(Table({TischName: "", Beginn: Now(), Schluss: Now()}), 0)',
        'FirstN(Table({TischName: "", Beginn: Now(), Schluss: Now(), Aktiv: true}), 0)', "F5 Panel")
aendere("ddTischePanel.Items", "LookUp(belegtListe, TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start)",
        "LookUp(belegtListe, Aktiv && TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start)", "F5 Panel")


def klammer_ende(f, start):
    tiefe, i, im_str = 0, start, False
    while i < len(f):
        ch = f[i]
        if ch == '"':
            im_str = not im_str
        elif not im_str:
            if ch == "(":
                tiefe += 1
            elif ch == ")":
                tiefe -= 1
                if tiefe == 0:
                    return i
        i += 1
    raise ValueError("Klammer")


for c in ["btn5Std", "btn9Std"]:
    for p in ["DisplayMode", "Fill"]:
        k = f"{c}.{p}"
        f = aktuell(k)
        s = "IsBlank(LookUp(Tischbuchungen, "
        assert f.count(s) == 1, k
        i = f.index(s)
        lu = i + len("IsBlank(")
        e = klammer_ende(f, lu)
        pred = f[lu + len("LookUp(Tischbuchungen, "):e]
        assert f[e:e + 5] == ").ID)", k
        neu = (f"IsEmpty(Filter(ForAll(Filter(Tischbuchungen, {pred}) As X, "
               "{Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}), Aktiv))")
        setze(k, f[:i] + neu + f[e + 5:], "F5 Panel")

# --- F6 Verlängern: verfallene Buchungen blockieren nicht, eigene verfallene nicht verlängern -----------------------
for c in ["btnVerwalten", "btnVerwalten_2"]:
    k = f"{c}.OnSelect"
    f = aktuell(k)
    m = re.search(r"(?m)^([ \t]*)Set\(varVerlNaechste, First\(Sort\(Filter\(Tischbuchungen, (Tisch\.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende)\), Startzeit, SortOrder\.Ascending\)\)\);\n", f)
    assert m and len(re.findall("Set\\(varVerlNaechste", f)) == 1, k
    e = m.group(1)
    neu = (f"{e}{GRENZE};\n{e}ClearCollect(colVerlNaechste, Filter(Tischbuchungen, {m.group(2)}));\n"
           f"{e}RemoveIf(colVerlNaechste, {VERF});\n{e}Set(varVerlNaechste, First(Sort(colVerlNaechste, Startzeit, SortOrder.Ascending)));\n")
    setze(k, f[:m.start()] + neu + f[m.end():], "F6 Verlängern")
for c in ["btnVerlängern", "btnVerlängern_1"]:
    k = f"{c}.OnSelect"
    aendere(k, "  Set(varIsLoading, true);\n", "  Set(varIsLoading, true);\n  " + GRENZE + ";\n", "F6 Verlängern")
    f = aktuell(k)
    m = re.search(r"(?m)^([ \t]*)Set\(varVerlTagesende, [^\n]*\n", f)
    assert m, k
    e = m.group(1)
    setze(k, f[:m.end()] + f"{e}ClearCollect(colVerlKonflikt, Filter(Tischbuchungen, Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));\n"
          f"{e}RemoveIf(colVerlKonflikt, {VERF});\n" + f[m.end():], "F6 Verlängern")
    aendere(k, "!IsBlank(LookUp(Tischbuchungen, Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID)",
            "!IsEmpty(colVerlKonflikt)", "F6 Verlängern")
    f = aktuell(k)
    m = re.search(r"(?m)^([ \t]*)If\(\n([ \t]*)varVerlEndeNeu <= varVerlBuchung\.Startzeit,\n", f)
    assert m, k
    e2 = m.group(2)
    setze(k, f[:m.end() - len(f"{e2}varVerlEndeNeu <= varVerlBuchung.Startzeit,\n")]
          + f"{e2}{verf('varVerlBuchung.')},\n"
          + f'{e2}Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen.", NotificationType.Warning),\n'
          + f[m.end() - len(f"{e2}varVerlEndeNeu <= varVerlBuchung.Startzeit,\n"):], "F6 Verlängern")

# --- F7 Einchecken / Auschecken -------------------------------------------------------------------------------------
LADE_F = "  " + GRENZE + ";\n  " + L_NEU_KOPF + ', If(IsError(neu) || IsError(First(neu)), Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen.", NotificationType.Warning), ' + L_NEU_CC + "))"
assert LADE_F in aktuell("btnEinchecken.OnSelect")
setze("btnEinchecken.OnSelect", """If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),
  Set(varIsLoading, true);
  @GRENZE@;
  Set(varCheckinBuchung, LookUp(Tischbuchungen, ID = varSelectedBuchung.ID));
  Set(varCheckinTisch, varCheckinBuchung.Tisch.Value);
  Set(varCheckinStart, varCheckinBuchung.Startzeit);
  Set(varCheckinEnde, varCheckinBuchung.Endzeit);
  If(
    IsBlank(varCheckinBuchung.ID),
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren.", NotificationType.Warning);
    Set(varZeigeCheckin, false),
    varCheckinBuchung.CheckedIn && Now() < varCheckinStart,
    IfError(
      Patch(Tischbuchungen, varCheckinBuchung, {CheckedIn: false}),
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
      Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinBuchung.ID));
      If(
        !varSelectedBuchung.CheckedIn,
        Notify("Ausgecheckt. Die Buchung bleibt bestehen, bitte zum Beginn wieder einchecken.", NotificationType.Success);
        Set(varZeigeCheckin, false),
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning)
      )
    ),
    varCheckinBuchung.CheckedIn && DateAdd(Now(), 1, TimeUnit.Minutes) >= varCheckinEnde,
    Notify("Die Buchung endet ohnehin jetzt. Der Tisch ist gleich wieder frei.", NotificationType.Information);
    Set(varZeigeCheckin, false),
    varCheckinBuchung.CheckedIn,
    Set(varCheckinNeuesEnde, DateAdd(Today(), Hour(Now()) * 60 + Minute(Now()) + 1, TimeUnit.Minutes));
    IfError(
      Patch(Tischbuchungen, varCheckinBuchung, {Endzeit: varCheckinNeuesEnde}),
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
      Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinBuchung.ID));
      If(
        varSelectedBuchung.Endzeit < varCheckinEnde,
        Notify("Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit, "hh:mm") & " Uhr, der Tisch ist wieder frei.", NotificationType.Success);
        Set(varZeigeCheckin, false),
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning)
      )
    ),
    Now() < DateAdd(varCheckinStart, -30, TimeUnit.Minutes),
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich.", NotificationType.Warning),
    Now() >= varCheckinEnde,
    Notify("Diese Buchung ist schon zu Ende.", NotificationType.Warning);
    Set(varZeigeCheckin, false),
    varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze,
    Notify("Zu spät: Ohne Check-in bis " & varFreigabeMinuten & " Minuten nach Beginn verfällt die Buchung, der Tisch ist wieder frei. Bitte neu buchen.", NotificationType.Warning);
    Set(varZeigeCheckin, false),
    ClearCollect(colCheckinAndere, Filter(Tischbuchungen, Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));
    RemoveIf(colCheckinAndere, ID = varCheckinBuchung.ID || (@VERF@));
    If(
      !IsEmpty(colCheckinAndere),
      Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen.", NotificationType.Error);
      Set(varZeigeCheckin, false),
      IfError(
        Patch(Tischbuchungen, varCheckinBuchung, {CheckedIn: true}),
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
        Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinBuchung.ID));
        If(
          varSelectedBuchung.CheckedIn,
          Notify("Eingecheckt.", NotificationType.Success);
          Set(varZeigeCheckin, false),
          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning)
        )
      )
    )
  );
@LADE@;
  Set(varSperreBis, DateAdd(Now(), 2, TimeUnit.Seconds));
  Set(varIsLoading, false)
)""".replace("@GRENZE@", GRENZE).replace("@VERF@", VERF).replace("@LADE@", LADE_F), "F7 Einchecken")
setze("lblStatusHeute.Text", 'If(ThisItem.CheckedIn, "Eingecheckt", ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze, "Verfallen", "Einchecken")', "F7 Status")
setze("lblStatusHeute.Color", 'If(ThisItem.CheckedIn, ColorValue("#00A96B"), ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze, ColorValue("#A6A6A6"), ColorValue("#FFA500"))', "F7 Status")

# --- F8 Erinnerung im Timer -----------------------------------------------------------------------------------------
f = aktuell("tmrAktualisieren.OnTimerEnd")
assert f.endswith("ClearCollect(colGrundriss, " + L_NEU_CC[len("ClearCollect(colGrundriss, "):] + "))\n)") or f.endswith("))\n)"), f[-80:]
assert f.endswith("\n)")
ein = lambda t, n: "\n".join(" " * n + z if z.strip() else z for z in t.split("\n"))
setze("tmrAktualisieren.OnTimerEnd", f[:-2] + ";\n  If(\n    varAktiverTab = \"dashboard\" && varAnsichtsDatum = Today() && !varZeigeDetails && !varZeigeRaumBuchungForm,\n"
      + ein(FRAGE.rstrip("\n"), 4) + "\n"
      f"    If(\n      !IsEmpty(colCheckinFrage) && {ERSTE} <> varCheckinGefragtID,\n"
      f"      Set(varCheckinGefragtID, {ERSTE});\n"
      "      Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinGefragtID));\n      Set(varZeigeCheckin, true)\n    )\n  )\n)", "F8 Erinnerung")

# --- Schritte -------------------------------------------------------------------------------------------------------
P = lambda *ks: list(ks)
REIN_LADE = [k for k in LADE_STELLEN if herkunft[k] == ["F Ladezeile"]]
SCHRITTE = [
    ("F1", "App-Start: Einstellung 30 Minuten, Check-in-Frage beim Öffnen", P("App.OnStart")),
    ("F2", "Storno-Fix: richtige Buchung, nur eigene, Hintergrund sperrt", P(*[k for k in final if k.startswith("btnStornoHintergrund.")],
        "btnStornieren.OnSelect", "btnStornieren_1.OnSelect", "btnStornoJa.OnSelect")),
    ("F3", "Grundriss: verfallene Buchungen als frei anzeigen", P("btnHitArea.OnSelect", *REIN_LADE)),
    ("F4", "Buchen: verfallene Buchungen blockieren nicht", P("btnSpeichern.OnSelect", "btnSpeichernTischePanel.OnSelect")),
    ("F5", "Panel „Tisch buchen“: Liste und 5/9-Std.-Knöpfe", P("btnTischHinzufügen.OnSelect", "ddTischePanel.Items",
        "btn5Std.DisplayMode", "btn5Std.Fill", "btn9Std.DisplayMode", "btn9Std.Fill")),
    ("F6", "Verlängern: verfallene Buchungen blockieren nicht", P("btnVerwalten.OnSelect", "btnVerwalten_2.OnSelect", "btnVerlängern.OnSelect", "btnVerlängern_1.OnSelect")),
    ("F7", "Einchecken bis 30 Min nach Beginn, Auschecken beendet die Buchung", P("btnEinchecken.OnSelect", "lblStatusHeute.Text", "lblStatusHeute.Color")),
    ("F8", "Check-in-Erinnerung alle 5 Minuten", P("tmrAktualisieren.OnTimerEnd")),
]
fehler = []
zugeteilt = {}
for sid, titel, keys in SCHRITTE:
    for k in keys:
        if k in zugeteilt:
            fehler.append(f"{k}: doppelt in {zugeteilt[k]} und {sid}")
        zugeteilt[k] = sid
for k in final:
    if k not in zugeteilt:
        fehler.append(f"{k}: keinem Schritt zugeteilt")

# --- Prüfungen ------------------------------------------------------------------------------------------------------
STEUER = set(a.typ) | {k.split(".")[0] for k in basis} | set(NEUE_STEUER)
stand = dict(basis)
stand.update(final)
gesetzt = set()
for v in stand.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
for k, f in final.items():
    c = k.split(".")[0]
    if c not in STEUER:
        fehler.append(f"{k}: Steuerelement unbekannt")
    if not A.klammern_ok(f):
        fehler.append(f"{k}: Klammern")
    if A.from_de(A.to_de(f)) != f:
        fehler.append(f"{k}: Rückübersetzung")
    ohne = A.ausserhalb_strings(f)
    if "//" in ohne:
        fehler.append(f"{k}: Kommentar")
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", ohne)):
        if v not in gesetzt:
            fehler.append(f"{k}: Variable {v} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr)[A-ZÄÖÜa-zäöü0-9_]*)\.", ohne)):
        if n not in STEUER:
            fehler.append(f"{k}: unbekanntes Steuerelement {n}")
    if "varFreigabeGrenze" in ohne and k.endswith(("OnSelect", "OnStart", "OnTimerEnd", "OnChange")) and GRENZE not in f:
        fehler.append(f"{k}: liest varFreigabeGrenze, ohne sie vorher zu setzen")
# Alte Ladezeile darf nirgends mehr stehen, neue genau an den 14 Stellen
for k, v in stand.items():
    if L_ALT_KOPF in v or L_ALT_CC in v:
        fehler.append(f"{k}: alte Ladezeile übrig")
lade_neu = sorted(k for k, v in stand.items() if L_NEU_KOPF in v)
if len(lade_neu) != 14:
    fehler.append(f"Ladezeile neu an {len(lade_neu)} statt 14 Stellen")
# Schreibstellen: Sperre + neue Ladezeile
schreib = [k for k, v in stand.items() if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", A.ausserhalb_strings(v))]
for k in schreib:
    v = stand[k]
    if not (v.startswith("If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),") or k == "btnStornoJa.OnSelect"):
        fehler.append(f"{k}: Schreibstelle ohne Sperre")
    if v.count(L_NEU_KOPF) < (3 if k == "btnStornoJa.OnSelect" else 1):
        fehler.append(f"{k}: Schreibstelle ohne neue Ladezeile")
if stand["btnStornoJa.OnSelect"].count("If(\n    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),") != 3:
    fehler.append("btnStornoJa.OnSelect: nicht alle drei Arme gesperrt")
if "varSelectedBuchung" in stand["btnStornoJa.OnSelect"] or "varSelectedBuchungTab" in stand["btnStornoJa.OnSelect"]:
    fehler.append("btnStornoJa.OnSelect: liest noch die ausgewählte Buchung statt varStornoID")
# Jede Abfrage auf Tischbuchungen nach dem Paket (auch mehrzeilig), einzeln eingeordnet:
#  A) ClearCollect(colX, Filter(...)) und danach RemoveIf(colX, ...Freigabe-Regel...)
#  B) ForAll(Filter(...) ...) mit Erstellt im Datensatz (Ladezeile, Panel-Liste, 5/9-Std.-Knöpfe)
#  C) bewusst ohne Regel (eigene Listen), mit Grund
AUSGENOMMEN = {
    "galTischbuchungenHeute.Items": "eigene Buchungen im Dashboard; die verfallene Buchung bleibt sichtbar (Status „Verfallen“)",
    "galAlleTischbuchungen.Items": "eigene Buchungen im Tab; eine verfallene Buchung darf storniert werden",
    "btnStornoJa.OnSelect#Person.Email = User().Email && Endzeit >= Now()": "Mehrfach-Stornieren eigener Buchungen; verfallene dürfen mit storniert werden",
}
abfragen, ungeklaert = [], []
for k, v in stand.items():
    for m in re.finditer(r"(LookUp|Filter)\(\s*Tischbuchungen,\s*", v):
        auf = m.start() + len(m.group(1))
        zu = klammer_ende(v, auf)
        pred = " ".join(v[m.end():zu].split())
        if pred.startswith("ID = "):
            continue
        abfragen.append((k, pred))
        davor = v[:m.start()].rstrip()
        cc = re.search(r"ClearCollect\(\s*(col\w+),\s*$", davor)
        if cc:
            r = re.search(r"RemoveIf\(" + cc.group(1) + r", ([^\n]*)", v[zu:])
            if r and "Erstellt <= varFreigabeGrenze" in r.group(1):
                continue
        if davor.endswith("ForAll(") and "Erstellt" in v[zu:zu + 250]:
            continue
        if k in AUSGENOMMEN or f"{k}#{pred}" in AUSGENOMMEN:
            continue
        ungeklaert.append(f"{k}: {pred[:80]}")
for u in ungeklaert:
    fehler.append("Abfrage ohne Freigabe-Regel: " + u)

out = []
for sid, titel, keys in SCHRITTE:
    for k in keys:
        c, p = k.split(".", 1)
        vorher = basis.get(k)
        out.append(dict(schritt=sid, titel=titel, control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        vorher=vorher, vorher_de=A.to_de(vorher) if vorher is not None else None,
                        quelle_vorher=("Gesamtplan " + gplan[k]["schritt"]) if k in gplan else ("Export 07.10." if vorher is not None else None),
                        art="neu" if vorher is None else "ersetzen", herkunft=herkunft.get(k, []),
                        pfad=a.pfad(c) if c in a.typ else (gplan[k]["pfad"] if k in gplan else f"(neu) {NEUE_STEUER[c][1]} > {c}"),
                        neues_steuerelement=NEUE_STEUER.get(c)))
json.dump(dict(app=out, neue_steuerelemente=NEUE_STEUER, ausgenommen=AUSGENOMMEN), open(os.path.join(ZIEL, "paket_f_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
zeilen = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, {len(NEUE_STEUER)} neues Steuerelement.",
          f"Grundlage: Export 07.10. + Endfassungen Gesamtplan ({sum(1 for s in out if s['quelle_vorher'] and s['quelle_vorher'].startswith('Gesamtplan'))} Properties bauen auf dem Gesamtplan auf).",
          f"Ladezeile neu an {len(lade_neu)} Stellen, alte Ladezeile an 0 Stellen.",
          f"Schreibstellen: {len(schreib)} ({', '.join(sorted(schreib))}), alle mit Zweifach-Sperre und neuer Ladezeile.",
          f"Abfragen auf Tischbuchungen (ohne reine ID-Abfragen, auch mehrzeilige): {len(abfragen)}, jede einzeln geprüft: Freigabe-Regel lokal angewandt oder bewusst ausgenommen ({len(AUSGENOMMEN)}: eigene Listen und Mehrfach-Stornieren).",
          "Je Property geprüft: Klammern, Rückübersetzung deutsch->englisch, keine Kommentare, Steuerelemente bekannt/neu, jede gelesene var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt.",
          "Jede Property kommt genau einmal vor."]
zeilen += ["FEHLER: " + f for f in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))
sys.exit(1 if fehler else 0)
