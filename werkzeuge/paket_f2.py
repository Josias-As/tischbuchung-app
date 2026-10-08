# Paket F, Fassung 2 (08.10.2026): Freigabe in der App + Storno direkt (ohne Rückfrage-Dialog) + Timer + Einfügeliste.
# Ausgangslage = tatsächlicher Studio-Stand nach Josias' Angaben ("Ist"): Export 07.10. + eingefügte Gesamtplan-Schritte
# (G1 G2 G3 G6[Nachtrag 4] G7 G9 G10 G11 G12 G13 G15 G16 G17 G18 G19 G20 G25, G22 teilweise). Nicht eingefügt: G4 G5 G8 G14 G21 G23 G24 G26.
# Zielformeln: Paket F (Fassung 1, paket_f_bloecke.json) + Nachtrag 4 (F4) + Änderungen dieser Fassung.
# Aufruf: python3 -I werkzeuge/paket_f2.py -> arbeit/2026-10-08_PaketF2/paket_f2_bloecke.json + pruefung.txt
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-08_PaketF2")
os.makedirs(ZIEL, exist_ok=True)
lade = lambda p: json.load(open(os.path.join(A.REPO, p), encoding="utf-8"))
G = lade("arbeit/2026-10-08_Gesamtplan/gesamtplan_bloecke.json")
F1 = lade("arbeit/2026-10-08_PaketF/paket_f_bloecke.json")
N4 = lade("arbeit/2026-10-08_Nachtrag4/nachtrag4_bloecke.json")
K = lade("arbeit/2026-10-07_PaketK_v2/bloecke.json")

EINGEFUEGT = {"G1", "G2", "G3", "G6", "G7", "G9", "G10", "G11", "G12", "G13", "G15", "G16", "G17", "G18", "G19", "G20", "G25"}
TEILWEISE = {"G22"}
gplan = {f"{s['control']}.{s['prop']}": s for s in G["app"]}

# --- Ist-Stand im Studio -----------------------------------------------------------------------------------------
ist = dict(a.props)
for k, s in gplan.items():
    if s["schritt"] in EINGEFUEGT:
        ist[k] = s["neu"]
for b in N4:
    if b["schritt"] == "G6":
        ist[f"{b['control']}.OnSelect"] = b["neu"]
ist_quelle = {}
for k in ist:
    if k in gplan and gplan[k]["schritt"] in EINGEFUEGT:
        ist_quelle[k] = "Gesamtplan " + gplan[k]["schritt"]
    else:
        ist_quelle[k] = "Export 07.10."
for c in ["btnSpeichern", "btnSpeichernTischePanel"]:
    ist_quelle[f"{c}.OnSelect"] = "Gesamtplan G6 (Fassung Nachtrag 4)"

# --- Ziel: Paket F Fassung 1 als Ausgangspunkt -----------------------------------------------------------------------
final, herkunft = {}, {}
for s in F1["app"]:
    k = f"{s['control']}.{s['prop']}"
    if s["control"] in ("btnStornoHintergrund",) or k == "btnStornoJa.OnSelect":
        continue
    final[k] = s["neu"]
    herkunft[k] = list(s["herkunft"])
for b in N4:
    if b["schritt"] == "F4":
        final[f"{b['control']}.OnSelect"] = b["neu"]
        herkunft[f"{b['control']}.OnSelect"] = ["F4 Buchen", "Nachtrag 4"]
NEUE_STEUER = {}


def setze(k, wert, tag):
    final[k] = wert
    herkunft.setdefault(k, []).append(tag)


def aendere(k, alt, neu, tag, n=1):
    f = final[k]
    assert f.count(alt) == n, (k, alt[:70], f.count(alt))
    final[k] = f.replace(alt, neu)
    herkunft.setdefault(k, []).append(tag)


GRENZE = "Set(varFreigabeGrenze, DateAdd(Now(), -Coalesce(varFreigabeMinuten, 30), TimeUnit.Minutes))"
VERF = "!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze"
L_ALT_KOPF = "With({neu: ForAll(Filter(Tischbuchungen, (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes))) As B, {TischName: B.Tisch.Value, Startzeit: B.Startzeit, Endzeit: B.Endzeit, Eingecheckt: B.CheckedIn, Name: B.Person.DisplayName})}"
L_NEU_KOPF = L_ALT_KOPF.replace("Name: B.Person.DisplayName})}", "Name: B.Person.DisplayName, Erstellt: B.Erstellt})}")
L_ALT_CC = "ClearCollect(colGrundriss, neu)"
L_NEU_CC = 'ClearCollect(colGrundriss, DropColumns(Filter(neu, Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze), "Erstellt"))'
LOCK = "!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis)"


def lade_f(f):
    n = f.count(L_ALT_KOPF)
    assert n >= 1 and f.count(L_ALT_CC) == n
    f = re.sub(r"(?m)^([ \t]*)" + re.escape(L_ALT_KOPF), lambda m: m.group(1) + GRENZE + ";\n" + m.group(1) + L_NEU_KOPF, f)
    return f.replace(L_ALT_CC, L_NEU_CC)


# --- A: Stornieren direkt, ohne Rückfrage-Dialog ---------------------------------------------------------------------
kv2 = {f"{s['control']}.{s['prop']}": s["neu"] for s in K}
for c, zeige in [("btnStornieren", "varZeigeVerwalten"), ("btnStornieren_1", "varZeigeVerwaltenTab")]:
    f = kv2[f"{c}.OnSelect"]
    assert f.startswith("If(\n  " + LOCK + ","), c
    m = re.search(r"(?m)^([ \t]*)Notify\(\"Diese Buchung gibt es nicht mehr\. Die Liste wurde aktualisiert\.\", NotificationType\.Warning\);\n\1Set\(" + zeige + r", false\),\n\1IfError\(", f)
    assert m, c
    e = m.group(1)
    f = f[:m.end() - len("IfError(")] + f"Lower(varStornoBuchung.Person.Email) <> Lower(User().Email),\n{e}" \
        + 'Notify("Nur eigene Buchungen können storniert werden.", NotificationType.Error),\n' + e + "IfError(" + f[m.end():]
    setze(f"{c}.OnSelect", lade_f(f), "A Storno direkt")
    setze(f"{c}.DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "A Storno direkt")
f = kv2["btnStornierenKlein.OnSelect"]
assert f.startswith("If(\n  " + LOCK + ",") and "Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now())" in f
setze("btnStornierenKlein.OnSelect", lade_f(f), "A Storno direkt")
setze("btnStornierenKlein.DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "A Storno direkt")

# --- B: Timer anlegen (G8 ohne varZeigeStornoFrage) + Erinnerung mit lokaler Vorprüfung (keine Abfrage ohne Anlass) --
NEUE_STEUER["tmrAktualisieren"] = ("Timer (Einfügen → Eingabe → Timer)", "Screen1", "auf oberster Ebene einfügen (nicht in einen Container)")
for p in ["Duration", "Repeat", "AutoStart", "Visible"]:
    setze(f"tmrAktualisieren.{p}", gplan[f"tmrAktualisieren.{p}"]["neu"], "B Timer (aus G8)")
aendere("tmrAktualisieren.OnTimerEnd", " && !varZeigeCheckin && !varZeigeStornoFrage,", " && !varZeigeCheckin,", "B ohne Storno-Dialog")
aendere("tmrAktualisieren.OnTimerEnd", '    varAktiverTab = "dashboard" && varAnsichtsDatum = Today() && !varZeigeDetails && !varZeigeRaumBuchungForm,\n',
        '    varAktiverTab = "dashboard" && varAnsichtsDatum = Today() && !varZeigeDetails && !varZeigeRaumBuchungForm &&\n'
        '    !IsBlank(LookUp(colGrundriss, Name = User().FullName && !Eingecheckt && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes) && Endzeit > Now()).TischName),\n',
        "B Vorprüfung lokal")

# --- F7: Auschecken mit zweitem Tippen, Texte ohne "sofort frei" ------------------------------------------------------
f = final["btnEinchecken.OnSelect"]
assert f.startswith("If(\n  " + LOCK + ",")
f = f.replace('"Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit, "hh:mm") & " Uhr, der Tisch ist wieder frei."',
              '"Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit, "hh:mm") & " Uhr. Andere können den Tisch wieder buchen."')
f = f.replace('Notify("Die Buchung endet ohnehin jetzt. Der Tisch ist gleich wieder frei.", NotificationType.Information);',
              'Notify("Die Buchung endet ohnehin jetzt.", NotificationType.Information);')
f = f.replace('"Zu spät: Ohne Check-in bis " & varFreigabeMinuten & " Minuten nach Beginn verfällt die Buchung, der Tisch ist wieder frei. Bitte neu buchen."',
              '"Zu spät: Ohne Check-in bis " & Coalesce(varFreigabeMinuten, 30) & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen."')
assert "wieder frei" not in f
assert f.count("Set(varZeigeCheckin, false),\n        Notify(\"Die Änderung ist nicht angekommen. Bitte aktualisieren.\", NotificationType.Warning)") >= 1
innen = "\n".join(("  " + z) if z.strip() else z for z in f.split("\n"))
setze("btnEinchecken.OnSelect",
      "If(\n  varSelectedBuchung.CheckedIn && Now() >= varSelectedBuchung.Startzeit && varAuscheckFrageID <> varSelectedBuchung.ID,\n"
      "  Set(varAuscheckFrageID, varSelectedBuchung.ID);\n"
      '  Notify("Zum Auschecken bitte noch einmal tippen. Deine Buchung endet dann jetzt.", NotificationType.Information),\n'
      "  Set(varAuscheckFrageID, 0);\n" + innen + "\n)", "F7 Auschecken bestätigen")
setze("btnEinchecken.Text", 'If(varSelectedBuchung.CheckedIn, If(varAuscheckFrageID = varSelectedBuchung.ID, "Wirklich auschecken?", "Auschecken"), "Einchecken")', "F7 Auschecken bestätigen")
setze("btnEinchecken.DisplayMode", gplan["btnEinchecken.DisplayMode"]["neu"], "F7 (aus G5)")
eh = a.props["btnEincheckenHeute.OnSelect"]
assert eh.startswith("Set(varSelectedBuchung, ThisItem);")
setze("btnEincheckenHeute.OnSelect", "Set(varAuscheckFrageID, 0); " + eh, "F7 Auschecken bestätigen")
aendere("App.OnStart", "Set(varCheckinGefragtID, 0);\n", "Set(varCheckinGefragtID, 0);\nSet(varAuscheckFrageID, 0);\n", "F7 Auschecken bestätigen")

# --- Schritte (Einfügereihenfolge) --------------------------------------------------------------------------------
REIN_LADE = ["ddStockwerk.OnChange", "dpAnsichtsDatum.OnChange", "Icon1_1.OnSelect", "Icon1.OnSelect", "Image6.OnSelect", "btnHitArea_1.OnSelect"]
SCHRITTE = [
    ("F1", "App-Start: Einstellung, Check-in-Frage beim Öffnen", ["App.OnStart"]),
    ("F2", "Stornieren direkt und sicher (ohne Rückfrage-Dialog)", ["btnStornieren.OnSelect", "btnStornieren.DisplayMode", "btnStornieren_1.OnSelect",
                                                                    "btnStornieren_1.DisplayMode", "btnStornierenKlein.OnSelect", "btnStornierenKlein.DisplayMode"]),
    ("F3", "Grundriss: verfallene Buchungen als frei", ["btnHitArea.OnSelect"] + REIN_LADE),
    ("F4", "Buchen: verfallene Buchungen blockieren nicht (mit Nachtrag 4)", ["btnSpeichern.OnSelect", "btnSpeichernTischePanel.OnSelect"]),
    ("F5", "Panel „Tisch buchen“: Liste und 5/9-Std.-Knöpfe", ["btnTischHinzufügen.OnSelect", "ddTischePanel.Items", "btn5Std.DisplayMode", "btn5Std.Fill", "btn9Std.DisplayMode", "btn9Std.Fill"]),
    ("F6", "Verlängern: verfallene blockieren nicht, keine zwei Tische", ["btnVerwalten.OnSelect", "btnVerwalten_2.OnSelect", "btnVerlängern.OnSelect", "btnVerlängern_1.OnSelect"]),
    ("F7", "Einchecken bis Frist, Auschecken mit zweitem Tippen", ["btnEinchecken.OnSelect", "btnEinchecken.DisplayMode", "btnEinchecken.Text", "btnEincheckenHeute.OnSelect", "lblStatusHeute.Text", "lblStatusHeute.Color"]),
    ("F8", "Timer anlegen: automatisch aktualisieren und an Check-in erinnern (ersetzt G8)", [f"tmrAktualisieren.{p}" for p in ["Duration", "Repeat", "AutoStart", "Visible", "OnTimerEnd"]]),
]
fehler = []
zugeteilt = {}
for sid, titel, keys in SCHRITTE:
    for k in keys:
        if k in zugeteilt:
            fehler.append(f"{k}: doppelt")
        zugeteilt[k] = sid
        if k not in final:
            fehler.append(f"{k}: ohne Formel")
for k in final:
    if k not in zugeteilt:
        fehler.append(f"{k}: keinem Schritt zugeteilt")
    if k in gplan and gplan[k]["schritt"] in TEILWEISE:
        fehler.append(f"{k}: liegt in einem nur teilweise eingefügten Schritt, Ist-Stand unbekannt")

# --- Prüfungen auf dem Endstand im Studio (Ist + Paket F2) ---------------------------------------------------------
stand = dict(ist)
stand.update(final)
STEUER = set(a.typ) | {k.split(".")[0] for k in stand}
gesetzt = set()
for v in stand.values():
    for m in re.finditer(r"(?:Set|ClearCollect|Collect)\(\s*((?:var|col)\w+)", v):
        gesetzt.add(m.group(1))
nicht_da = {"conStornoFrage", "lblStornoFrage", "btnStornoJa", "btnStornoNein", "btnStornoHintergrund", "btnAndereZeit", "lblBelegtHeute"}
for k, f in final.items():
    ohne = A.ausserhalb_strings(f)
    if not A.klammern_ok(f):
        fehler.append(f"{k}: Klammern")
    if A.from_de(A.to_de(f)) != f:
        fehler.append(f"{k}: Rückübersetzung")
    if "//" in ohne:
        fehler.append(f"{k}: Kommentar")
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", ohne)):
        if v not in gesetzt:
            fehler.append(f"{k}: Variable {v} wird nirgends gesetzt")
    for n in set(re.findall(r"\b((?:btn|dd|dp|gal|con|lbl|chk|tgl|tmr)[A-ZÄÖÜa-zäöü0-9_]*)\.", ohne)):
        if n not in STEUER or n in nicht_da:
            fehler.append(f"{k}: Steuerelement {n} gibt es im Studio nicht")
    if "varFreigabeGrenze" in ohne and k.endswith(("OnSelect", "OnStart", "OnTimerEnd", "OnChange")) and GRENZE not in f:
        fehler.append(f"{k}: liest varFreigabeGrenze, ohne sie vorher zu setzen")
for k, v in stand.items():
    o = A.ausserhalb_strings(v)
    if "varZeigeStornoFrage" in o or "varStornoQuelle" in o:
        fehler.append(f"{k}: hängt noch am Rückfrage-Dialog")
    if L_ALT_KOPF in v or L_ALT_CC in v:
        fehler.append(f"{k}: alte Ladezeile übrig")
    if re.search(r"\b(conStornoFrage|btnStornoJa|btnStornoHintergrund|lblBelegtHeute|btnAndereZeit)\b", o):
        fehler.append(f"{k}: verweist auf ein Steuerelement, das nicht eingefügt wird")
if "Refresh(Tischbuchungen)" in stand["btnSpeichern.OnSelect"] or "Refresh(Tischbuchungen)" in stand["btnSpeichernTischePanel.OnSelect"]:
    fehler.append("Speichern: Refresh übrig (Nachtrag 4 verloren)")
# Schreibstellen: jedes Patch/Remove hinter der Zweifach-Sperre, neue Ladezeile vorhanden
schreib = [k for k, v in stand.items() if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", A.ausserhalb_strings(v))]
for k in schreib:
    v = stand[k]
    if LOCK not in v:
        fehler.append(f"{k}: Schreibstelle ohne Sperre")
        continue
    lock_i = v.index(LOCK)
    for m in re.finditer(r"(Patch|Remove)\(\s*Tischbuchungen", v):
        if m.start() < lock_i:
            fehler.append(f"{k}: Schreibvorgang vor der Sperre")
    if L_NEU_KOPF not in v:
        fehler.append(f"{k}: Schreibstelle ohne neue Ladezeile")
for c in ["btnStornieren", "btnStornieren_1"]:
    v = stand[f"{c}.OnSelect"]
    if "Lower(varStornoBuchung.Person.Email) <> Lower(User().Email)" not in v or "Remove(Tischbuchungen, varStornoBuchung)" not in v:
        fehler.append(f"{c}: Eigentümerprüfung oder Remove auf frischem Datensatz fehlt")
    if v.index("Lower(varStornoBuchung.Person.Email)") > v.index("Remove(Tischbuchungen, varStornoBuchung)"):
        fehler.append(f"{c}: Eigentümerprüfung nach dem Remove")
if "Person.Email = User().Email" not in stand["btnStornierenKlein.OnSelect"]:
    fehler.append("btnStornierenKlein: nicht auf eigene Buchungen gefiltert")
v = stand["btnEinchecken.OnSelect"]
if v.index("Set(varAuscheckFrageID, varSelectedBuchung.ID)") > v.index(LOCK) or "Patch(" in v[:v.index(LOCK)]:
    fehler.append("btnEinchecken: Rückfrage-Zweig schreibt oder liegt hinter der Sperre")


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
    raise ValueError


AUSGENOMMEN = {
    "galTischbuchungenHeute.Items": "eigene Buchungen im Dashboard; verfallene bleiben sichtbar (Status „Verfallen“)",
    "galAlleTischbuchungen.Items": "eigene Buchungen im Tab; verfallene dürfen storniert werden",
    "btnStornierenKlein.OnSelect": "Mehrfach-Stornieren eigener Buchungen; verfallene dürfen mit storniert werden",
}
abfragen, ungeklaert = [], []
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
        if davor.endswith("ForAll(") and "Erstellt" in v[zu:zu + 250]:
            continue
        if k in AUSGENOMMEN:
            continue
        ungeklaert.append(f"{k}: {pred[:80]}")
fehler += ["Abfrage ohne Freigabe-Regel: " + u for u in ungeklaert]


# --- Ausgabe mit Diff gegen den Ist-Stand ----------------------------------------------------------------------------
def diff(alt, neu):
    zeilen = list(difflib.unified_diff(alt.split("\n"), neu.split("\n"), lineterm="", n=2))
    return "\n".join(z for z in zeilen[2:])


out = []
for sid, titel, keys in SCHRITTE:
    for k in keys:
        c, p = k.split(".", 1)
        vorher = ist.get(k)
        neu_de = A.to_de(final[k])
        out.append(dict(schritt=sid, titel=titel, control=c, prop=p, neu=final[k], de=neu_de,
                        vorher=vorher, vorher_de=A.to_de(vorher) if vorher is not None else None,
                        quelle_vorher=ist_quelle.get(k) if vorher is not None else None,
                        art="neu" if vorher is None else "ersetzen", herkunft=herkunft.get(k, []),
                        diff=diff(A.to_de(vorher), neu_de) if vorher is not None else None,
                        pfad=a.pfad(c) if c in a.typ else f"(neu) {NEUE_STEUER[c][1]} > {c}",
                        neues_steuerelement=NEUE_STEUER.get(c)))
json.dump(dict(app=out, neue_steuerelemente=NEUE_STEUER, ausgenommen=AUSGENOMMEN), open(os.path.join(ZIEL, "paket_f2_bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
lade_neu = sorted(k for k, v in stand.items() if L_NEU_KOPF in v)
zeilen = [f"{len(out)} Properties in {len(SCHRITTE)} Schritten, {len(NEUE_STEUER)} neues Steuerelement (tmrAktualisieren, ersetzt G8).",
          "Ausgangslage = Studio-Stand nach Josias' Angaben (Export + eingefügte Gesamtplan-Schritte, G6 in Fassung Nachtrag 4). Keine Property liegt in G22 (nur teilweise eingefügt).",
          f"Ladezeile neu an {len(lade_neu)} Stellen, alte an 0. Keine Verweise auf den Rückfrage-Dialog (G4), auf G14-Steuerelemente oder varZeigeStornoFrage.",
          f"Schreibstellen: {len(schreib)} ({', '.join(sorted(schreib))}), jedes Patch/Remove hinter der Zweifach-Sperre, alle mit neuer Ladezeile.",
          "Stornieren: frischer Datensatz, Eigentümerprüfung vor dem Remove (Dashboard, Tab), Mehrfach nur eigene. Speichern ohne Refresh (Nachtrag 4).",
          f"Abfragen auf Tischbuchungen (ohne reine ID-Abfragen): {len(abfragen)}, jede einzeln: Freigabe-Regel lokal oder begründet ausgenommen ({len(AUSGENOMMEN)}).",
          "Je Property: Klammern, Rückübersetzung, keine Kommentare, Steuerelement im Studio vorhanden, jede var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt."]
zeilen += ["FEHLER: " + x for x in fehler] if fehler else ["Prüfung: 0 Fehler"]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))
sys.exit(1 if fehler else 0)
