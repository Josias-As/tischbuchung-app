# Umbauplan Handy-App, Fassung 2 (08.10.2026; Fassung 1 bleibt in arbeit/2026-10-08_Handy). Neu: Zeitumstellung (DateTime statt DateAdd auf Minuten), ID aus Patch (varNeuID).
# Umbauplan Handy-App (08.10.2026): gleiche Regeln wie die Desktop-App (Paket F Fassung 2).
# Ausgangslage: Handy-Export vom 08.10. (quellen/2026-10-08_HandyExport). Freigabe-Regel, Gesperrt, 06:00,
# Einchecken bis Frist (+ B5/B8), Nachprüfungen ohne Fehlalarm, nur eigene Buchungen stornieren/beenden.
# Aufruf: python3 -I werkzeuge/handy_plan.py -> arbeit/2026-10-08_Handy/handy_bloecke.json + pruefung.txt
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

h = A.lade_handy_0810()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_Handy_v2")
os.makedirs(ZIEL, exist_ok=True)
final, herkunft = {}, {}


def akt(k):
    return final.get(k, h.props.get(k))


def aendere(k, alt, neu, tag, n=1):
    f = akt(k)
    assert f.count(alt) == n, (k, alt[:80], f.count(alt))
    final[k] = f.replace(alt, neu)
    herkunft.setdefault(k, []).append(tag)


def setze(k, v, tag):
    final[k] = v
    herkunft.setdefault(k, []).append(tag)


LOCK = "!varIsLoading && Now() >= varSperreBis"
GRENZE = "Set(varFreigabeGrenze, DateAdd(Now(), -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes))"
VERF = "!CheckedIn && Startzeit <= varFreigabeGrenze && !IsBlank(Erstellt) && Erstellt <= varFreigabeGrenze"
MIN = "Coalesce(varFreigabeMinuten, 30)"
VERF_ITEM = (f"!ThisItem.CheckedIn && DateAdd(ThisItem.Startzeit, {MIN}, TimeUnit.Minutes) <= varJetzt"
             f" && !IsBlank(ThisItem.Erstellt) && DateAdd(ThisItem.Erstellt, {MIN}, TimeUnit.Minutes) <= varJetzt")
GRENZE_LISTE = "Set(varListeGrenze, DateAdd(Now(), -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes))"
EINDEUTIG = "-(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1)"

# H1 App.OnStart: Einstellung und Grenze -------------------------------------------------------------------------------
aendere("App.OnStart", "Set(varJetzt, Now()); ClearCollect(colTische, Tische)",
        "Set(varJetzt, Now()); Set(varFreigabeMinuten, 30); " + GRENZE + "; " + GRENZE_LISTE + "; ClearCollect(colTische, Tische)", "H1")

# H2 Stornieren / Jetzt beenden: nur eigene ----------------------------------------------------------------------------
aendere("btnStornoJa.OnSelect",
        "    Set(varZeigeStorno, false);\n    Set(varZeigeVerwalten, false),\n    IfError(\n      Remove(",
        "    Set(varZeigeStorno, false);\n    Set(varZeigeVerwalten, false),\n    Lower(varBuchung.Person.Email) <> Lower(User().Email),\n"
        '    Notify("Nur eigene Buchungen können storniert werden.", NotificationType.Error);\n    Set(varZeigeStorno, false),\n    IfError(\n      Remove(', "H2")
aendere("btnJetztBeenden.OnSelect",
        "    If(\n      Now() <= varBuchung.Startzeit,",
        "    If(\n      Lower(varBuchung.Person.Email) <> Lower(User().Email),\n"
        '      Notify("Nur eigene Buchungen können beendet werden.", NotificationType.Error),\n      Now() <= varBuchung.Startzeit,', "H2")
aendere("btnJetztBeenden.OnSelect", '"Buchung beendet. Der Tisch ist wieder frei."', '"Buchung beendet. Andere können den Tisch wieder buchen."', "H2")

# H3 Tischauswahl: verfallene zählen nicht, gesperrte Tische fehlen; Grenze beim Öffnen setzen ------------------------
f = akt("ddTisch.Items")
m = re.search(r"\{ belegt: ForAll\(Filter\(Tischbuchungen, (.*?)\), Tisch\.Value\) \}", f)
assert m, "ddTisch belegt"
setze("ddTisch.Items", f[:m.start()] + "{ belegt: Filter(ForAll(Filter(Tischbuchungen, " + m.group(1) + ") As X, "
      "{ TischName: X.Tisch.Value, Aktiv: X.CheckedIn || X.Startzeit > varListeGrenze || IsBlank(X.Erstellt) || X.Erstellt > varListeGrenze }), Aktiv) }" + f[m.end():], "H3")
DT = lambda dd: f"DateTime(Year(ddDatum.Selected.Tag), Month(ddDatum.Selected.Tag), Day(ddDatum.Selected.Tag), RoundDown({dd}.Selected.Min / 60, 0), Mod({dd}.Selected.Min, 60), 0)"
for dd in ["ddStart", "ddEnde"]:
    aendere("ddTisch.Items", f"DateAdd(ddDatum.Selected.Tag, {dd}.Selected.Min, TimeUnit.Minutes)", DT(dd), "H3 Zeitumstellung")
aendere("ddTisch.Items", 'Filter(colTische, !("big table" in Lower(Titel)) && !(Titel in belegt))',
        'Filter(colTische, !Gesperrt && !("big table" in Lower(Titel)) && !(Titel in belegt.TischName))', "H3")
aendere("btnTabBuchen.OnSelect", 'Set(varTab, "buchen");\n', 'Set(varTab, "buchen");\n' + GRENZE_LISTE + ";\n", "H3")
aendere("btnZumBuchen.OnSelect", 'Set(varTab, "buchen")', 'Set(varTab, "buchen"); ' + GRENZE_LISTE, "H3")
aendere("icoAktualisieren_1.OnSelect", "Refresh(Tische);\n", "Refresh(Tische);\nClearCollect(colTische, Tische);\n" + GRENZE_LISTE + ";\n", "H3")

# H4 Buchen ------------------------------------------------------------------------------------------------------------
k = "btnBuchen.OnSelect"
aendere(k, "  Set(varBuchStart, DateAdd(ddDatum.Selected.Tag, ddStart.Selected.Min, TimeUnit.Minutes));\n", f"  Set(varBuchStart, {DT('ddStart')});\n", "H4 Zeitumstellung")
aendere(k, "  Set(varBuchEnde, DateAdd(ddDatum.Selected.Tag, ddEnde.Selected.Min, TimeUnit.Minutes));\n", f"  Set(varBuchEnde, {DT('ddEnde')});\n", "H4 Zeitumstellung")
aendere(k, "  Set(varTagesEnde, DateAdd(ddDatum.Selected.Tag, 22 * 60, TimeUnit.Minutes));\n",
        "  Set(varTagesEnde, DateTime(Year(ddDatum.Selected.Tag), Month(ddDatum.Selected.Tag), Day(ddDatum.Selected.Tag), 22, 0, 0));\n", "H4 Zeitumstellung")
aendere(k, "    varBuchStart < DateAdd(Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), TimeUnit.Minutes),\n",
        "    varBuchStart < DateTime(Year(Now()), Month(Now()), Day(Now()), Hour(Now()), If(Minute(Now()) >= 30, 30, 0), 0),\n", "H4 Zeitumstellung")
aendere(k, "  Set(varTischID, ddTisch.Selected.ID);\n",
        "  Set(varTischID, ddTisch.Selected.ID);\n  " + GRENZE + ";\n"
        "  ClearCollect(colBuchBelegt, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));\n"
        f"  RemoveIf(colBuchBelegt, {VERF});\n"
        "  ClearCollect(colBuchIch, Filter(Tischbuchungen, Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart));\n"
        f"  RemoveIf(colBuchIch, {VERF});\n", "H4")
aendere(k, "    !IsBlank(LookUp(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID),\n",
        "    !IsBlank(LookUp(Tische, ID = varTischID && Gesperrt = true).ID),\n"
        '    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen.", NotificationType.Warning),\n'
        "    !IsEmpty(colBuchBelegt),\n", "H4")
aendere(k, "    !IsBlank(LookUp(Tischbuchungen, Person.Email = User().Email && Startzeit < varBuchEnde && Endzeit > varBuchStart).ID),\n",
        "    !IsEmpty(colBuchIch),\n", "H4")
aendere(k, "      ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchStart));\n",
        f"      Set(varBuchNachVon, DateAdd(varBuchStart, {EINDEUTIG}, TimeUnit.Seconds));\n"
        "      ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varBuchEnde && Endzeit > varBuchNachVon));\n"
        f"      RemoveIf(colKollision, ({VERF}) || Endzeit <= varBuchStart);\n", "H4")
aendere(k, '" bis " & Text(varBuchEnde, "hh:mm") & " Uhr", NotificationType.Success);',
        '" bis " & Text(varBuchEnde, "hh:mm") & " Uhr. Bitte bis " & ' + MIN + ' & " Minuten nach Beginn einchecken.", NotificationType.Success);', "H4")

f = akt("btnBuchen.OnSelect")
i = f.index("    IfError(\n      Patch(\n        Tischbuchungen,\n        Defaults(Tischbuchungen),")
j = f.index("      Notify(\"Das Buchen ist fehlgeschlagen. Bitte erneut versuchen.\", NotificationType.Error),\n", i)
patch = f[i + len("    IfError(\n"):j].rstrip().rstrip(",")
assert patch.startswith("      Patch(") and patch.endswith(")")
rest_start = j + len("      Notify(\"Das Buchen ist fehlgeschlagen. Bitte erneut versuchen.\", NotificationType.Error),\n")
k_end = f.index("  );\n  Set(varNeuLaden, varNeuLaden + 1);")
alt_rest = f[rest_start:k_end]
nach = alt_rest[:alt_rest.index("      Set(varBuchung, LookUp(colKollision,")]
assert nach.startswith("      Set(varBuchNachVon,") and "RemoveIf(colKollision," in nach
erfolg = 'Notify("Gebucht: " & varTischName & ", " & Text(varBuchStart, "dd.mm.") & ", " & Text(varBuchStart, "hh:mm") & " bis " & Text(varBuchEnde, "hh:mm") & " Uhr. Bitte bis " & Coalesce(varFreigabeMinuten, 30) & " Minuten nach Beginn einchecken.", NotificationType.Success);'
assert erfolg in alt_rest
patch_ein = "\n".join(("  " + z[6:]) if z.startswith("      ") else z for z in patch.split("\n"))
neu_teil = ("    Set(varNeuID, IfError(\n" + "\n".join("  " + z for z in patch_ein.split("\n")) + ".ID,\n      -1\n    ));\n"
            "    If(\n      varNeuID = -1,\n      Notify(\"Das Buchen ist fehlgeschlagen. Bitte erneut versuchen.\", NotificationType.Error),\n"
            + nach
            + "      Set(varNeuBuchung, LookUp(colKollision, ID = varNeuID));\n"
            "      If(\n        IsBlank(varNeuBuchung.ID) || varNeuBuchung.Startzeit <> varBuchStart || varNeuBuchung.Endzeit <> varBuchEnde || Lower(varNeuBuchung.Person.Email) <> Lower(User().Email),\n"
            "        Notify(\"Die Buchung ist nicht vollständig angekommen. Bitte unter „Meine“ prüfen.\", NotificationType.Warning),\n"
            "        !IsBlank(LookUp(colKollision, ID < varNeuID).ID),\n"
            "        Notify(\"Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht. Bitte storniere deine Buchung unter „Meine“ und wähle einen anderen Tisch.\", NotificationType.Error),\n"
            "        " + erfolg + "\n"
            "        Set(varTab, If(varBuchStart < DateAdd(Today(), 1, TimeUnit.Days), \"heute\", \"meine\"))\n"
            "      )\n    )\n")
setze("btnBuchen.OnSelect", f[:i] + neu_teil + f[k_end:], "H4 ID aus Patch (B5/B6)")

# H5 Verlängern (+1 / +2) ------------------------------------------------------------------------------------------------
for c in ["btnVerl1", "btnVerl2"]:
    k = f"{c}.OnSelect"
    aendere(k, "  Set(varIsLoading, true);\n", "  Set(varIsLoading, true);\n  " + GRENZE + ";\n", "H5")
    f = akt(k)
    m = re.search(r"(?m)^([ \t]*)Set\(varTagesEnde, [^\n]*\n", f)
    e = m.group(1)
    setze(k, f[:m.end()]
          + f"{e}ClearCollect(colVerlBelegt, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));\n"
          + f"{e}RemoveIf(colVerlBelegt, {VERF});\n"
          + f"{e}ClearCollect(colVerlIch, Filter(Tischbuchungen, Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt));\n"
          + f"{e}RemoveIf(colVerlIch, ID = varBuchungID || ({VERF}));\n" + f[m.end():], "H5")
    aendere(k, "      varEndeAlt <= Now(),\n      Notify(\"Diese Buchung ist bereits beendet.\", NotificationType.Information); Set(varZeigeVerwalten, false),\n",
            "      varEndeAlt <= Now(),\n      Notify(\"Diese Buchung ist bereits beendet.\", NotificationType.Information); Set(varZeigeVerwalten, false),\n"
            "      !varBuchung.CheckedIn && varBuchung.Startzeit <= varFreigabeGrenze && !IsBlank(varBuchung.Erstellt) && varBuchung.Erstellt <= varFreigabeGrenze,\n"
            "      Notify(\"Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen.\", NotificationType.Warning),\n", "H5")
    aendere(k, "      !IsBlank(LookUp(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID),\n",
            "      !IsEmpty(colVerlBelegt),\n", "H5")
    aendere(k, "      !IsBlank(LookUp(Tischbuchungen, Person.Email = User().Email && Startzeit < varNeuEnde && Endzeit > varEndeAlt).ID),\n",
            "      !IsEmpty(colVerlIch),\n", "H5")
    aendere(k, "        ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varEndeAlt));\n",
            f"        Set(varVerlNachVon, DateAdd(varEndeAlt, {EINDEUTIG}, TimeUnit.Seconds));\n"
            "        ClearCollect(colKollision, Filter(Tischbuchungen, Tisch.Value = varTischName && Startzeit < varNeuEnde && Endzeit > varVerlNachVon));\n"
            f"        RemoveIf(colKollision, ID <> varBuchungID && (({VERF}) || Endzeit <= varEndeAlt));\n", "H5")

# H6 Einchecken: eigene Variable (B5), Fenster bis Frist, schon vergeben?, Anzeige mit varJetzt (B8) ------------------
setze("btnEincheckenH.OnSelect", f"""If(
  {LOCK},
  Set(varIsLoading, true);
  {GRENZE};
  Set(varCheckinID, ThisItem.ID);
  Set(varCheckinBuchung, LookUp(Tischbuchungen, ID = varCheckinID));
  Set(varCheckinTisch, varCheckinBuchung.Tisch.Value);
  Set(varCheckinStart, varCheckinBuchung.Startzeit);
  Set(varCheckinEnde, varCheckinBuchung.Endzeit);
  If(
    IsBlank(varCheckinBuchung.ID),
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren.", NotificationType.Warning),
    varCheckinBuchung.CheckedIn,
    Notify("Du bist bereits eingecheckt.", NotificationType.Information),
    Now() < DateAdd(varCheckinStart, -30, TimeUnit.Minutes),
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich.", NotificationType.Warning),
    Now() >= varCheckinEnde,
    Notify("Diese Buchung ist schon zu Ende.", NotificationType.Warning),
    varCheckinStart <= varFreigabeGrenze && !IsBlank(varCheckinBuchung.Erstellt) && varCheckinBuchung.Erstellt <= varFreigabeGrenze,
    Notify("Zu spät: Ohne Check-in bis " & {MIN} & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen.", NotificationType.Warning),
    ClearCollect(colCheckinAndere, Filter(Tischbuchungen, Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));
    RemoveIf(colCheckinAndere, ID >= varCheckinID || ({VERF}));
    If(
      !IsEmpty(colCheckinAndere),
      Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen.", NotificationType.Error),
      IfError(
        Patch(Tischbuchungen, varCheckinBuchung, {{ CheckedIn: true }}),
        Notify("Einchecken fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
        Set(varCheckinNachVon, DateAdd(varCheckinStart, {EINDEUTIG}, TimeUnit.Seconds));
        ClearCollect(colCheckinAndere, Filter(Tischbuchungen, Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinNachVon));
        If(
          !LookUp(colCheckinAndere, ID = varCheckinID).CheckedIn,
          Notify("Der Check-in ist nicht angekommen. Bitte aktualisieren und erneut versuchen.", NotificationType.Warning),
          !IsBlank(LookUp(colCheckinAndere, ID < varCheckinID && Endzeit > varCheckinStart && !({VERF})).ID),
          Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter „Meine“ prüfen und klären.", NotificationType.Error),
          Notify("Eingecheckt.", NotificationType.Success)
        )
      )
    )
  );
  Set(varNeuLaden, varNeuLaden + 1);
  Set(varSperreBis, DateAdd(Now(), 2, TimeUnit.Seconds));
  Set(varIsLoading, false)
)""", "H6 (B5)")
setze("btnEincheckenH.DisplayMode", f"""If(
  ThisItem.CheckedIn || varIsLoading,
  DisplayMode.Disabled,
  varJetzt >= DateAdd(ThisItem.Startzeit, -30, TimeUnit.Minutes) && varJetzt < ThisItem.Endzeit && !({VERF_ITEM}),
  DisplayMode.Edit,
  DisplayMode.Disabled
)""", "H6 (B8)")
setze("btnEincheckenH.Text", f'If(ThisItem.CheckedIn, "Eingecheckt", {VERF_ITEM}, "Verfallen", "Einchecken")', "H6")
setze("lblStatusH.Text", f'If(ThisItem.CheckedIn, "Eingecheckt", {VERF_ITEM}, "Verfallen", "Nicht eingecheckt")', "H6")
setze("lblStatusH.Color", f"If(ThisItem.CheckedIn, RGBA(0, 169, 107, 1), {VERF_ITEM}, RGBA(166, 166, 166, 1), RGBA(255, 165, 0, 1))", "H6")

# H7 06:00 (wie Gesamtplan Phase 8) -----------------------------------------------------------------------------------
alt = "If(ddDatum.Selected.Tag = Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), 8 * 60)"
aendere("ddStart.Items", alt, "If(ddDatum.Selected.Tag = Today(), Max(6 * 60, 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0)), 6 * 60)", "H7")
setze("ddStart.Default", "If(\n  ddDatum.Selected.Tag = Today(),\n  With(\n    { ab: Max(6 * 60, 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0)) },\n"
      '    Text(Time(RoundDown(ab / 60, 0), Mod(ab, 60), 0), "hh:mm")\n  ),\n  "08:00"\n)', "H7")

SCHRITTE = [
    ("H1", "App-Start: Einstellung 30 Minuten", ["App.OnStart"]),
    ("H2", "Stornieren und Jetzt beenden: nur eigene Buchungen", ["btnStornoJa.OnSelect", "btnJetztBeenden.OnSelect"]),
    ("H3", "Tischauswahl: verfallene Buchungen frei, gesperrte Tische weg", ["ddTisch.Items", "btnTabBuchen.OnSelect", "btnZumBuchen.OnSelect", "icoAktualisieren_1.OnSelect"]),
    ("H4", "Buchen: Regel, gesperrt, Nachprüfung ohne Fehlalarm", ["btnBuchen.OnSelect"]),
    ("H5", "Verlängern: Regel, keine falsche Rücknahme", ["btnVerl1.OnSelect", "btnVerl2.OnSelect"]),
    ("H6", "Einchecken bis zur Frist, Status „Verfallen“ (mit B5/B8)", ["btnEincheckenH.OnSelect", "btnEincheckenH.DisplayMode", "btnEincheckenH.Text", "lblStatusH.Text", "lblStatusH.Color"]),
    ("H7", "Startzeiten ab 06:00", ["ddStart.Items", "ddStart.Default"]),
]
fehler = []
zug = {}
for sid, t, ks in SCHRITTE:
    for k in ks:
        if k in zug or k not in final:
            fehler.append(f"{k}: doppelt oder ohne Formel")
        zug[k] = sid
for k in final:
    if k not in zug:
        fehler.append(f"{k}: keinem Schritt zugeteilt")

stand = dict(h.props)
stand.update(final)
gesetzt = set()
for v in stand.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
STEUER = set(h.typ)
for k, f in final.items():
    o = A.ausserhalb_strings(f)
    if not A.klammern_ok(f):
        fehler.append(f"{k}: Klammern")
    if A.from_de(A.to_de(f)) != f:
        fehler.append(f"{k}: Rückübersetzung")
    if "//" in o:
        fehler.append(f"{k}: Kommentar")
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", o)):
        if v not in gesetzt:
            fehler.append(f"{k}: Variable {v} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr|ico)[A-ZÄÖÜa-zäöü0-9_]*)\.", o)):
        if n not in STEUER:
            fehler.append(f"{k}: Steuerelement {n} unbekannt")
    if "varFreigabeGrenze" in o and k.endswith("OnSelect") and GRENZE not in f:
        fehler.append(f"{k}: liest varFreigabeGrenze, ohne sie zu setzen")
# Schreibstellen
for k, v in stand.items():
    o = A.ausserhalb_strings(v)
    for m in re.finditer(r"(Patch|Remove)\(\s*Tischbuchungen", o):
        if LOCK not in v or m.start() < o.index(A.ausserhalb_strings(LOCK)):
            fehler.append(f"{k}: Schreibvorgang ohne Sperre")
for k in ["btnStornoJa.OnSelect", "btnJetztBeenden.OnSelect"]:
    v = stand[k]
    if "Lower(varBuchung.Person.Email) <> Lower(User().Email)" not in v or v.index("Lower(varBuchung.Person.Email)") > v.index("Remove(" if "Remove(" in v else "Patch("):
        fehler.append(f"{k}: Eigentümerprüfung fehlt oder kommt zu spät")
for k, v in stand.items():
    if k in final and "DateAdd(ddDatum.Selected.Tag" in v:
        fehler.append(f"{k}: Datum + Minuten per DateAdd (Zeitumstellung)")
vb = stand["btnBuchen.OnSelect"]
if "Set(varBuchungID" in vb or "Set(varNeuID, IfError(" not in vb or "LookUp(colKollision, ID < varNeuID)" not in vb:
    fehler.append("btnBuchen: ID nicht aus Patch oder varBuchungID überschrieben")
if vb.index("Set(varNeuID, IfError(") < vb.index(LOCK):
    fehler.append("btnBuchen: Patch vor der Sperre")
# Nachprüfungen eindeutig und ohne verfallene (sonst Fehlalarm bzw. falsche Rücknahme)
for k, var in [("btnBuchen.OnSelect", "varBuchNachVon"), ("btnVerl1.OnSelect", "varVerlNachVon"), ("btnVerl2.OnSelect", "varVerlNachVon"), ("btnEincheckenH.OnSelect", "varCheckinNachVon")]:
    v = stand[k]
    if f"Endzeit > {var}" not in v:
        fehler.append(f"{k}: Nachprüfung nicht eindeutig (Zwischenspeicher)")
for k in ["btnBuchen.OnSelect", "btnVerl1.OnSelect", "btnVerl2.OnSelect"]:
    if "RemoveIf(colKollision, " not in stand[k]:
        fehler.append(f"{k}: Nachprüfung ohne Freigabe-Regel")
if "!(Titel in belegt.TischName)" not in stand["ddTisch.Items"] or "!Gesperrt" not in stand["ddTisch.Items"]:
    fehler.append("ddTisch.Items: Regel oder Gesperrt fehlt")
# jede Abfrage auf Tischbuchungen eingeordnet


def klammer_ende(f, start):
    t, i, s = 0, start, False
    while i < len(f):
        ch = f[i]
        if ch == '"':
            s = not s
        elif not s:
            if ch == "(":
                t += 1
            elif ch == ")":
                t -= 1
                if t == 0:
                    return i
        i += 1
    raise ValueError


AUSGENOMMEN = {"galHeute.Items": "eigene Buchungen heute; verfallene bleiben sichtbar (Status „Verfallen“)",
               "galMeine.Items": "eigene Buchungen; verfallene dürfen storniert werden"}
abfragen, offen = [], []
for k, v in stand.items():
    for m in re.finditer(r"(LookUp|Filter)\(\s*Tischbuchungen,\s*", v):
        zu = klammer_ende(v, m.start() + len(m.group(1)))
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
            if cc.group(1) == "colCheckinAndere" and "varCheckinNachVon" in pred and "!(!CheckedIn" in v:
                continue
        if davor.endswith("ForAll(") and "Erstellt" in v[zu:zu + 250]:
            continue
        if k in AUSGENOMMEN:
            continue
        offen.append(f"{k}: {pred[:80]}")
fehler += ["Abfrage ohne Freigabe-Regel: " + x for x in offen]


def diff(a, b):
    return "\n".join(list(difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=2))[2:])


out = []
for sid, t, ks in SCHRITTE:
    for k in ks:
        c, p = k.split(".", 1)
        vorher = h.props.get(k)
        out.append(dict(schritt=sid, titel=t, control=c, prop=p, neu=final[k], de=A.to_de(final[k]),
                        yaml="=" + final[k], vorher=vorher, vorher_de=A.to_de(vorher) if vorher is not None else None,
                        diff=diff(A.to_de(vorher), A.to_de(final[k])) if vorher is not None else None,
                        art="neu" if vorher is None else "ersetzen", herkunft=herkunft.get(k, []), pfad=h.pfad(c)))
json.dump(dict(app=out, ausgenommen=AUSGENOMMEN), open(os.path.join(ZIEL, "handy_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
z = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, kein neues Steuerelement. Ausgangslage: Handy-Export 08.10. (11:51).",
     "Je Property: Klammern, Rückübersetzung, keine Kommentare, Steuerelemente vorhanden, jede var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt.",
     "Jedes Patch/Remove hinter der Sperre. Stornieren/Beenden mit Eigentümerprüfung davor. Nachprüfungen (Buchen, Verlängern, Einchecken) pro Klick eindeutig und ohne verfallene Buchungen.",
     f"Abfragen auf Tischbuchungen (ohne reine ID-Abfragen): {len(abfragen)}, jede eingeordnet (Freigabe-Regel lokal oder begründet ausgenommen: {', '.join(AUSGENOMMEN)})."]
z += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(z) + "\n")
print("\n".join(z))
sys.exit(1 if fehler else 0)
