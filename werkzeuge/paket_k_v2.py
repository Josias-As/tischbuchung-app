# Erzeugt Paket K v2 aus dem veröffentlichten Export vom 07.10.2026 und prüft jeden Block.
# Aufruf: python3 -I werkzeuge/paket_k_v2.py
# Ergebnis: arbeit/2026-10-07_PaketK_v2/bloecke.json (+ Prüfprotokoll auf stdout)
# Formeln werden hier in englischer Schreibweise geschrieben und mit to_de() übersetzt.
import difflib, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

a = A.lade_desktop()
ZIEL = os.path.join(A.REPO, "arbeit/2026-10-07_PaketK_v2")
os.makedirs(ZIEL, exist_ok=True)


def orig(c, p):
    return a.get(c, p)


# Die L2-Ladezeile genau so, wie sie im Export steht (aus btnEinchecken, letzte Anweisung).
LADE = orig("btnEinchecken", "OnSelect").split(";\n")[-1].strip()
assert LADE.startswith("With({neu: ForAll(Filter(Tischbuchungen,") and LADE.endswith("ClearCollect(colGrundriss, neu)))")
for c, p in [("App", "OnStart"), ("btnSpeichern", "OnSelect"), ("btnSpeichernTischePanel", "OnSelect"),
             ("btnVerlängern", "OnSelect"), ("btnVerlängern_1", "OnSelect"), ("btnStornieren", "OnSelect"),
             ("btnStornieren_1", "OnSelect"), ("btnStornierenKlein", "OnSelect"), ("Icon1", "OnSelect"),
             ("Icon1_1", "OnSelect"), ("Image6", "OnSelect"), ("btnHitArea_1", "OnSelect"),
             ("dpAnsichtsDatum", "OnChange"), ("ddStockwerk", "OnChange")]:
    assert orig(c, p).count(LADE) == 1, (c, p)

SPERRE_ENDE = "Set(varSperreBis, DateAdd(Now(), 2, TimeUnit.Seconds));\n  Set(varIsLoading, false)"


def einruecken(text, n):
    pad = " " * n
    return "\n".join(pad + z if z.strip() else z for z in text.split("\n"))


def aufraeumblock(c):
    """Anweisungen nach der Ladezeile bis vor Set(varIsLoading, false) – wörtlich aus dem Export."""
    f = orig(c, "OnSelect")
    rest = f.split(LADE + ";\n", 1)[1]
    assert rest.rstrip().endswith("Set(varIsLoading, false)"), c
    rest = rest.rstrip()[: -len("Set(varIsLoading, false)")].rstrip()
    assert rest.endswith(";"), c
    return rest[:-1]


# ---------------------------------------------------------------------------------------------
# Bausteine
# ---------------------------------------------------------------------------------------------
def tagesende(rec):
    return (f"DateAdd({rec}.Startzeit, 22 * 60 - (Hour({rec}.Startzeit) * 60 + Minute({rec}.Startzeit)), "
            f"TimeUnit.Minutes)")


def verwalten_oeffnen(rec_var, grenze_var):
    """Beim Öffnen eines Verwalten-Dialogs: späteste mögliche Endzeit EINMAL berechnen
    (nächste Buchung am selben Tisch nach meinem Ende, sonst 22:00 des Buchungstags)."""
    return f"""Set({rec_var}, ThisItem);
Set(varVerlTisch, ThisItem.Tisch.Value);
Set(varVerlEndeAlt, ThisItem.Endzeit);
Set(varVerlTagesende, {tagesende('ThisItem')});
Set(varVerlNaechste, First(Sort(Filter(Tischbuchungen, Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende), Startzeit, SortOrder.Ascending)));
Set({grenze_var}, If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende, varVerlTagesende, varVerlNaechste.Startzeit));
Set(varAusgewaehltePlusDauer, Blank())"""


def plus_displaymode(rec, grenze, minuten):
    return (f"If(IsBlank({rec}.ID) || DateAdd({rec}.Endzeit, {minuten}, TimeUnit.Minutes) > {grenze}, "
            f"DisplayMode.Disabled, DisplayMode.Edit)")


def plus_fill(rec, grenze, minuten):
    return f"""If(
  varAusgewaehltePlusDauer = {minuten},
  ColorValue("#00A96B"),
  If(
    IsBlank({rec}.ID) || DateAdd({rec}.Endzeit, {minuten}, TimeUnit.Minutes) > {grenze},
    ColorFade(ColorValue("#EB3951"), 70%),
    ColorFade(ColorValue("#00A96B"), 70%)
  )
)"""


def minus_displaymode(rec, minuten):
    return (f"If(IsBlank({rec}.ID) || DateAdd({rec}.Endzeit, -{minuten}, TimeUnit.Minutes) <= {rec}.Startzeit, "
            f"DisplayMode.Disabled, DisplayMode.Edit)")


def minus_fill(rec, minuten):
    return f"""If(
  varAusgewaehltePlusDauer = -{minuten},
  ColorValue("#00A96B"),
  If(
    IsBlank({rec}.ID) || DateAdd({rec}.Endzeit, -{minuten}, TimeUnit.Minutes) <= {rec}.Startzeit,
    ColorFade(ColorValue("#EB3951"), 70%),
    ColorFade(ColorValue("#00A96B"), 70%)
  )
)"""


def verlaengern(rec_var, zeige_var, grenze_var):
    return f"""If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),
  Set(varIsLoading, true);
  Set(varVerlBuchung, LookUp(Tischbuchungen, ID = {rec_var}.ID));
  If(
    IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0,
    Notify("Bitte eine Dauer auswählen.", NotificationType.Warning),
    IsBlank(varVerlBuchung.ID),
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning);
    Set({zeige_var}, false),
    Set(varVerlTisch, varVerlBuchung.Tisch.Value);
    Set(varVerlEndeAlt, varVerlBuchung.Endzeit);
    Set(varVerlEndeNeu, DateAdd(varVerlBuchung.Endzeit, varAusgewaehltePlusDauer, TimeUnit.Minutes));
    Set(varVerlTagesende, {tagesende('varVerlBuchung')});
    If(
      varVerlEndeNeu <= varVerlBuchung.Startzeit,
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen.", NotificationType.Warning),
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende,
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden.", NotificationType.Warning),
      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen, Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID),
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen.", NotificationType.Warning);
      Set({grenze_var}, varVerlEndeAlt),
      IfError(
        Patch(Tischbuchungen, varVerlBuchung, {{Endzeit: varVerlEndeNeu}}),
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
        Set({rec_var}, LookUp(Tischbuchungen, ID = varVerlBuchung.ID));
        If(
          {rec_var}.Endzeit = varVerlEndeNeu,
          Notify("Buchung geändert, neues Ende " & Text(varVerlEndeNeu, "hh:mm") & " Uhr.", NotificationType.Success);
          Set({zeige_var}, false),
          Notify("Die Änderung ist nicht angekommen. Bitte die Buchung in der Liste prüfen.", NotificationType.Warning)
        )
      )
    )
  );
  Refresh(Tischbuchungen);
  {LADE};
  Set(varAusgewaehltePlusDauer, Blank());
  {SPERRE_ENDE}
)"""


def stornieren(rec_var, zeige_var):
    return f"""If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),
  Set(varIsLoading, true);
  Set(varStornoBuchung, LookUp(Tischbuchungen, ID = {rec_var}.ID));
  If(
    IsBlank(varStornoBuchung.ID),
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert.", NotificationType.Warning);
    Set({zeige_var}, false),
    IfError(
      Remove(Tischbuchungen, varStornoBuchung),
      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
      If(
        IsBlank(LookUp(Tischbuchungen, ID = varStornoBuchung.ID).ID),
        Notify("Buchung storniert.", NotificationType.Success);
        Set({zeige_var}, false),
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen.", NotificationType.Warning)
      )
    )
  );
  Refresh(Tischbuchungen);
  {LADE};
  {SPERRE_ENDE}
)"""


EINCHECKEN = f"""If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),
  Set(varIsLoading, true);
  Set(varCheckinBuchung, LookUp(Tischbuchungen, ID = varSelectedBuchung.ID));
  If(
    IsBlank(varCheckinBuchung.ID),
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren.", NotificationType.Warning);
    Set(varZeigeCheckin, false),
    !varCheckinBuchung.CheckedIn && (Now() < DateAdd(varCheckinBuchung.Startzeit, -30, TimeUnit.Minutes) || Now() > varCheckinBuchung.Endzeit),
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn und nur bis zum Ende möglich.", NotificationType.Warning),
    IfError(
      Patch(Tischbuchungen, varCheckinBuchung, {{CheckedIn: !varCheckinBuchung.CheckedIn}}),
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen.", NotificationType.Error),
      Set(varSelectedBuchung, LookUp(Tischbuchungen, ID = varCheckinBuchung.ID));
      If(
        varSelectedBuchung.CheckedIn <> varCheckinBuchung.CheckedIn,
        Notify(If(varSelectedBuchung.CheckedIn, "Eingecheckt.", "Ausgecheckt."), NotificationType.Success);
        Set(varZeigeCheckin, false),
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren.", NotificationType.Warning)
      )
    )
  );
  {LADE};
  {SPERRE_ENDE}
)"""


def zeit_aus(dd):
    return f"Time(Value(Left({dd}.Selected.Value, 2)), Value(Mid({dd}.Selected.Value, 4, 2)), 0)"


WOCHENTAG = ("Switch(Weekday(D.Value, StartOfWeek.Monday), 1, varTagMo, 2, varTagDi, 3, varTagMi, "
             "4, varTagDo, 5, varTagFr, 6, varTagSa, 7, varTagSo)")


def speichern(tisch_titel, tisch_id, dp, dd_start, dd_ende, dp_bis, aufraeumen):
    """Gemeinsamer Speicherablauf für den Buchungsdialog und das Tische-Panel (Sammel-Patch, SerienID, Nachlese)."""
    return f"""If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),
  Set(varIsLoading, true);
  Set(varNeuTischTitel, {tisch_titel});
  Set(varNeuTischID, {tisch_id});
  Set(varNeuEmail, User().Email);
  Set(varNeuDatum, {dp}.SelectedDate);
  Set(varNeuStartZeit, {zeit_aus(dd_start)});
  Set(varNeuEndeZeit, {zeit_aus(dd_ende)});
  Set(varNeuBisRoh, If(varWiederholen, {dp_bis}.SelectedDate, varNeuDatum));
  Set(varNeuBis, If(varNeuBisRoh > varNeuDatum + 14, varNeuDatum + 14, varNeuBisRoh));
  Set(varNeuJetzt, DateAdd(Today(), 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30, 0), TimeUnit.Minutes));
  ClearCollect(
    colNeuTermine,
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum, 0, DateDiff(varNeuDatum, varNeuBis, TimeUnit.Days) + 1), 0), DateAdd(varNeuDatum, Value, TimeUnit.Days)) As D,
        !varWiederholen || {WOCHENTAG}
      ) As T,
      {{Start: T.Value + varNeuStartZeit, Ende: T.Value + varNeuEndeZeit}}
    )
  );
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID),
    Notify("Bitte einen Tisch auswählen.", NotificationType.Warning),
    varNeuEndeZeit <= varNeuStartZeit,
    Notify("Das Ende muss nach dem Beginn liegen.", NotificationType.Warning),
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo,
    Notify("Bitte mindestens einen Wochentag auswählen.", NotificationType.Warning),
    varWiederholen && varNeuBisRoh < varNeuDatum,
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen.", NotificationType.Warning),
    IsEmpty(colNeuTermine),
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen.", NotificationType.Warning),
    First(colNeuTermine).Start < varNeuJetzt,
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen.", NotificationType.Warning),
    Set(varNeuSpanStart, First(colNeuTermine).Start);
    Set(varNeuSpanEnde, Last(colNeuTermine).Ende);
    Set(varNeuGesamt, CountRows(colNeuTermine));
    ClearCollect(colNeuBelegt, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));
    ClearCollect(colNeuIch, Filter(Tischbuchungen, Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));
    ClearCollect(
      colNeuErgebnis,
      ForAll(
        colNeuTermine As T,
        {{
          Start: T.Start,
          Ende: T.Ende,
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt, Startzeit < T.Ende && Endzeit > T.Start).ID),
            "tisch",
            !IsBlank(LookUp(colNeuIch, Startzeit < T.Ende && Endzeit > T.Start).ID),
            "ich",
            "frei"
          )
        }}
      )
    );
    Set(varNeuTischBelegt, CountRows(Filter(colNeuErgebnis, Grund = "tisch")));
    Set(varNeuIchBelegt, CountRows(Filter(colNeuErgebnis, Grund = "ich")));
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt,
      Notify(
        If(
          varNeuGesamt = 1,
          If(varNeuTischBelegt = 1, "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen.", "Du hast in dieser Zeit schon einen Tisch gebucht."),
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        ),
        NotificationType.Warning
      );
      Refresh(Tischbuchungen),
      Set(varSerienID, Text(GUID()));
      IfError(
        Patch(
          Tischbuchungen,
          ForAll(Filter(colNeuErgebnis, Grund = "frei"), Defaults(Tischbuchungen)),
          ForAll(
            Filter(colNeuErgebnis, Grund = "frei") As F,
            {{
              Tisch: {{Id: varNeuTischID, Value: varNeuTischTitel}},
              Startzeit: F.Start,
              Endzeit: F.Ende,
              Person: {{
                Claims: "i:0#.f|membership|" & Lower(User().Email),
                Department: "",
                DisplayName: User().FullName,
                Email: User().Email,
                JobTitle: "",
                Picture: ""
              }},
              SerienID: varSerienID
            }}
          )
        ),
        Set(varNeuFehler, true),
        Set(varNeuFehler, false)
      );
      Refresh(Tischbuchungen);
      ClearCollect(colNeuNachlese, Filter(Tischbuchungen, Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));
      Set(varNeuAnzahl, CountRows(Filter(colNeuNachlese, SerienID = varSerienID)));
      Set(varNeuKonflikt, CountRows(Filter(colNeuNachlese As N, N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M, M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));
      If(
        varNeuAnzahl = 0,
        Notify(If(varNeuFehler, "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen.", "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."), NotificationType.Error),
        varNeuKonflikt > 0,
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren.", NotificationType.Error),
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis,
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1, Text(varNeuSpanStart, "dd.mm."), varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart, "dd.mm.")) & ", " & Text(varNeuSpanStart, "hh:mm") & " bis " & Text(varNeuSpanEnde, "hh:mm") & " Uhr.", NotificationType.Success),
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0, " " & varNeuTischBelegt & "× war der Tisch schon belegt.", "") &
          If(varNeuIchBelegt > 0, " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch.", "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl, " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden.", "") &
          If(varNeuBisRoh > varNeuBis, " Die Wiederholung wurde auf 2 Wochen begrenzt.", ""),
          NotificationType.Warning
        )
      );
      If(
        varNeuAnzahl > 0,
{einruecken(aufraeumen, 8)}
      )
    );
    {LADE}
  );
  {SPERRE_ENDE}
)"""


def panel_knopf_zeiten(stunden):
    return f"""With(
  {{ minutenStart: If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60) }},
  With(
    {{
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60, 0), Mod(minutenStart, 60), 0),
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60, 0), Mod(minutenStart, 60), 0), {stunden}, TimeUnit.Hours),
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22, 0, 0)
    }},
    __KERN__
  )
)"""


def panel_knopf_displaymode(stunden):
    kern = """If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde,
      DisplayMode.Disabled,
      If(
        IsBlank(ddTischePanel.Selected.Titel),
        DisplayMode.Edit,
        If(
          IsBlank(LookUp(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate, If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60) + __STD__ * 60, TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate, If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60), TimeUnit.Minutes)).ID),
          DisplayMode.Edit,
          DisplayMode.Disabled
        )
      )
    )"""
    return panel_knopf_zeiten(stunden).replace("__KERN__", kern).replace("__STD__", str(stunden))


def panel_knopf_fill(stunden):
    kern = f"""If(
      varAusgewaehltePanelDauer = {stunden},
      ColorValue("#00A96B"),
      If(
        endeZeit > tagesEnde,
        ColorFade(ColorValue("#EB3951"), 70%),
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel),
          ColorFade(ColorValue("#00A96B"), 70%),
          If(
            IsBlank(LookUp(Tischbuchungen, Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate, If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60) + __STD__ * 60, TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate, If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60), TimeUnit.Minutes)).ID),
            ColorFade(ColorValue("#00A96B"), 70%),
            ColorFade(ColorValue("#EB3951"), 70%)
          )
        )
      )
    )"""
    return panel_knopf_zeiten(stunden).replace("__KERN__", kern).replace("__STD__", str(stunden))


def panel_knopf_onselect(c):
    """Original, nur der Startpunkt: heute = nächste halbe Stunde (wie bisher), anderer Tag = 08:00 (wie ddStartTischePanel.Items)."""
    f = orig(c, "OnSelect")
    alt = "{ minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0) }"
    neu = "{ minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(), 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30, 0), 8 * 60) }"
    assert f.count(alt) == 1, c
    return f.replace(alt, neu)


PANEL_ITEMS = """With(
  {
    datum: dpDatumTischePanel.SelectedDate,
    startZeit: Time(Value(Left(ddStartTischePanel.Selected.Value, 2)), Value(Mid(ddStartTischePanel.Selected.Value, 4, 2)), 0),
    endeZeit: Time(Value(Left(ddEndTischePanel.Selected.Value, 2)), Value(Mid(ddEndTischePanel.Selected.Value, 4, 2)), 0),
    bisRoh: If(varWiederholen, dpWiederholenBis_1.SelectedDate, dpDatumTischePanel.SelectedDate)
  },
  With(
    { bis: If(bisRoh > datum + 14, datum + 14, bisRoh) },
    With(
      {
        termine: ForAll(
          Filter(
            ForAll(Sequence(If(bis < datum, 0, DateDiff(datum, bis, TimeUnit.Days) + 1), 0), DateAdd(datum, Value, TimeUnit.Days)) As D,
            !varWiederholen || __WOCHENTAG__
          ) As T,
          {Start: T.Value + startZeit, Ende: T.Value + endeZeit}
        )
      },
      With(
        {
          belegtListe: If(
            varZeigeTischBuchungForm,
            ForAll(
              Filter(
                Tischbuchungen,
                Startzeit < DateAdd(dpDatumTischePanel.SelectedDate, If(varWiederholen && dpWiederholenBis_1.SelectedDate > dpDatumTischePanel.SelectedDate, Min(DateDiff(dpDatumTischePanel.SelectedDate, dpWiederholenBis_1.SelectedDate, TimeUnit.Days), 14), 0) + 1, TimeUnit.Days) && Endzeit > dpDatumTischePanel.SelectedDate
              ),
              {TischName: Tisch.Value, Beginn: Startzeit, Schluss: Endzeit}
            ),
            FirstN(Table({TischName: "", Beginn: Now(), Schluss: Now()}), 0)
          )
        },
        SortByColumns(
          Filter(
            ForAll(
              Tische As Ti,
              With(
                { n: CountRows(Filter(termine As Z, !IsBlank(LookUp(belegtListe, TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) },
                {
                  Titel: Ti.Titel,
                  ID: Ti.ID,
                  Belegt: n,
                  Etage: If(Ti.Geschoss.Value = varAusgewaehltesStockwerk, 0, 1),
                  Schluessel: Ti.Geschoss.Value & Left(Ti.Titel, Len(Ti.Titel) - Len(Last(Split(Ti.Titel, " ")).Value)) & Text(IfError(Value(Last(Split(Ti.Titel, " ")).Value), 0), "000"),
                  Anzeige: Ti.Titel & If(n = 0, "", "  (an " & n & " von " & CountRows(termine) & " Tagen belegt)")
                }
              )
            ),
            !("big table" in Lower(Titel)) && (Belegt = 0 || Belegt < CountRows(termine))
          ),
          "Belegt", SortOrder.Ascending,
          "Etage", SortOrder.Ascending,
          "Schluessel", SortOrder.Ascending
        )
      )
    )
  )
)""".replace("__WOCHENTAG__", WOCHENTAG)


def aktualisieren(c):
    f = orig(c, "OnSelect")
    alt_lade = LADE
    neu_lade = LADE.replace(
        'Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen.", NotificationType.Warning), ClearCollect(colGrundriss, neu)))',
        'Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen.", NotificationType.Warning), ClearCollect(colGrundriss, neu); Notify("Aktualisiert.", NotificationType.Success)))')
    assert neu_lade != alt_lade
    ende = ';\nSet(varIsLoading, false);\nNotify("Aktualisiert.", NotificationType.Success)'
    assert f.endswith(ende), c
    g = f[: -len(ende)] + ";\nSet(varIsLoading, false)"
    assert g.count(alt_lade) == 1
    return g.replace(alt_lade, neu_lade)


def mit_sperre(c):
    """Bestehenden Handler (beginnt mit Set(varIsLoading, true), endet mit Set(varIsLoading, false)) in die Zweifach-Sperre einpacken."""
    f = orig(c, "OnSelect")
    assert f.startswith("Set(varIsLoading, true);") and f.rstrip().endswith("Set(varIsLoading, false)"), c
    innen = f.rstrip()[: -len("Set(varIsLoading, false)")] + "Set(varSperreBis, DateAdd(Now(), 2, TimeUnit.Seconds));\nSet(varIsLoading, false)"
    return "If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),\n" + einruecken(innen, 2) + "\n)"


def onstart():
    f = orig("App", "OnStart")
    return "Set(varSperreBis, Now());\nSet(varVerlGrenze, Now());\nSet(varVerlGrenzeTab, Now());\n" + f


def btn_tisch_hinzufuegen():
    f = orig("btnTischHinzufügen", "OnSelect")
    anker = "Set(varZeigeTischBuchungForm, true);\n"
    assert f.startswith(anker)
    return f.replace(anker, anker + "Reset(dpDatumTischePanel);\nReset(ddTischePanel);\n", 1)


def verwalten_tab():
    f = orig("btnVerwalten_2", "OnSelect")
    alt = "  Set(varSelectedBuchungTab, ThisItem);\n"
    assert f.count(alt) == 1
    return f.replace(alt, einruecken(verwalten_oeffnen("varSelectedBuchungTab", "varVerlGrenzeTab"), 2) + ";\n")


def verwalten_dash():
    f = orig("btnVerwalten", "OnSelect")
    alt = "Set(varSelectedBuchung, ThisItem);\n"
    ende = ";\nSet(varAusgewaehltePlusDauer, Blank())"
    assert f.startswith(alt) and f.endswith(ende)
    g = f[: -len(ende)]
    return g.replace(alt, verwalten_oeffnen("varSelectedBuchung", "varVerlGrenze") + ";\n", 1)


# ---------------------------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------------------------
S = []


def schritt(nr, teil, c, p, neu, titel, art="ersetzen"):
    S.append(dict(nr=nr, teil=teil, control=c, prop=p, neu=neu, titel=titel, art=art))


schritt("0", "0", "App", "OnStart", onstart(), "Neue Variablen anlegen (Sperre, Verlängern-Grenzen)")

# Teil A: Verwalten-Dialoge
schritt("A1", "A", "btnVerwalten", "OnSelect", verwalten_dash(), "Dashboard-Verwalten öffnen: Grenze einmal berechnen")
schritt("A2", "A", "btnVerwalten_2", "OnSelect", verwalten_tab(), "Buchungen-Tab-Verwalten öffnen: Grenze einmal berechnen, Dauer leeren")
nr = 3
for i, m in [(1, 60), (2, 120), (3, 180)]:
    schritt(f"A{nr}", "A", f"btnPlus{i}Std", "DisplayMode", plus_displaymode("varSelectedBuchung", "varVerlGrenze", m), f"+{i} Std (Dashboard) ohne Abfrage")
    schritt(f"A{nr}", "A", f"btnPlus{i}Std", "Fill", plus_fill("varSelectedBuchung", "varVerlGrenze", m), f"+{i} Std (Dashboard) ohne Abfrage")
nr += 1
for i, m in [(1, 60), (2, 120), (3, 180)]:
    schritt(f"A{nr}", "A", f"btnPlus{i}Std_1", "DisplayMode", plus_displaymode("varSelectedBuchungTab", "varVerlGrenzeTab", m), f"+{i} Std (Tab) richtige Buchung, ohne Abfrage")
    schritt(f"A{nr}", "A", f"btnPlus{i}Std_1", "Fill", plus_fill("varSelectedBuchungTab", "varVerlGrenzeTab", m), f"+{i} Std (Tab) richtige Buchung, ohne Abfrage")
nr += 1
for name, m in [("btnMinus1Std", 60), ("btnMinus2Std", 120), ("btnMinus3std", 180)]:
    schritt(f"A{nr}", "A", name, "DisplayMode", minus_displaymode("varSelectedBuchungTab", m), f"−{m // 60} Std (Tab) richtige Buchung, ohne Abfrage")
    schritt(f"A{nr}", "A", name, "Fill", minus_fill("varSelectedBuchungTab", m), f"−{m // 60} Std (Tab) richtige Buchung, ohne Abfrage")
schritt("A6", "A", "btnVerlängern", "OnSelect", verlaengern("varSelectedBuchung", "varZeigeVerwalten", "varVerlGrenze"), "Verlängern (Dashboard) prüft am Server, meldet ehrlich")
schritt("A6", "A", "btnVerlängern", "DisplayMode", "If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0, DisplayMode.Disabled, DisplayMode.Edit)", "Verlängern (Dashboard) erst mit Dauer bedienbar", "neu")
schritt("A7", "A", "btnVerlängern_1", "OnSelect", verlaengern("varSelectedBuchungTab", "varZeigeVerwaltenTab", "varVerlGrenzeTab"), "Verlängern/Verkürzen (Tab) prüft am Server, meldet ehrlich")
schritt("A7", "A", "btnVerlängern_1", "DisplayMode", "If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0, DisplayMode.Disabled, DisplayMode.Edit)", "Speichern (Tab) erst mit Dauer bedienbar", "neu")
schritt("A8", "A", "btnStornieren", "OnSelect", stornieren("varSelectedBuchung", "varZeigeVerwalten"), "Stornieren (Dashboard) auf frischem Datensatz, Nachlese")
schritt("A8", "A", "btnStornieren", "DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "Stornieren (Dashboard) während Laden gesperrt", "neu")
schritt("A9", "A", "btnStornieren_1", "OnSelect", stornieren("varSelectedBuchungTab", "varZeigeVerwaltenTab"), "Stornieren (Tab) auf frischem Datensatz, Nachlese")
schritt("A9", "A", "btnStornieren_1", "DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "Stornieren (Tab) während Laden gesperrt", "neu")
schritt("A10", "A", "btnEinchecken", "OnSelect", EINCHECKEN, "Einchecken: frischer Datensatz, Zeitfenster, Nachlese")
schritt("A10", "A", "btnEinchecken", "DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "Einchecken während Laden gesperrt", "neu")

# Teil B: Neue Buchung speichern
schritt("B1", "B", "btnSpeichern", "OnSelect",
        speichern("varSelectedTisch.Titel", "varSelectedTisch.ID", "dpDatum", "ddStart", "ddEnde", "dpWiederholenBis", aufraeumblock("btnSpeichern")),
        "Buchungsdialog: Sammel-Patch mit SerienID, Prüfungen, Nachlese, eine Meldung")
schritt("B1", "B", "btnSpeichern", "DisplayMode", "If(varIsLoading, DisplayMode.Disabled, DisplayMode.Edit)", "Speichern (Dialog) während Laden gesperrt", "neu")
schritt("B2", "B", "btnSpeichernTischePanel", "OnSelect",
        speichern("ddTischePanel.Selected.Titel", "ddTischePanel.Selected.ID", "dpDatumTischePanel", "ddStartTischePanel", "ddEndTischePanel", "dpWiederholenBis_1", aufraeumblock("btnSpeichernTischePanel")),
        "Tische-Panel: gleicher Ablauf wie B1 (Sammel-Patch statt Schleife)")
schritt("B2", "B", "btnSpeichernTischePanel", "DisplayMode", "If(varIsLoading || IsBlank(ddTischePanel.Selected.Titel), DisplayMode.Disabled, DisplayMode.Edit)", "Speichern (Panel) erst mit Tisch bedienbar", "neu")

# Teil C: Tischauswahl im Panel
schritt("C1", "C", "ddTischePanel", "Items", PANEL_ITEMS, "Nur freie Tische, sortiert, ohne Big Table")
schritt("C1", "C", "ddTischePanel", "Items.Value", "Anzeige", "Anzeige mit Hinweis bei Serien")
schritt("C1", "C", "ddTischePanel", "AllowEmptySelection", "true", "Leere Auswahl erlaubt", "neu")
schritt("C1", "C", "ddTischePanel", "Default", "Blank()", "Kein Tisch vorausgewählt", "neu")
schritt("C2", "C", "btnTischHinzufügen", "OnSelect", btn_tisch_hinzufuegen(), "Panel öffnen: Datum und Tisch zurücksetzen")
schritt("C3", "C", "btn5Std", "DisplayMode", panel_knopf_displaymode(5), "5 Std: anderer Tag ab 08:00, ohne Tisch bedienbar, Abfrage nur bei offenem Panel")
schritt("C3", "C", "btn5Std", "Fill", panel_knopf_fill(5), "5 Std: Farbe passend")
schritt("C3", "C", "btn5Std", "OnSelect", panel_knopf_onselect("btn5Std"), "5 Std: anderer Tag ab 08:00")
schritt("C4", "C", "btn9Std", "DisplayMode", panel_knopf_displaymode(9), "9 Std: wie 5 Std")
schritt("C4", "C", "btn9Std", "Fill", panel_knopf_fill(9), "9 Std: wie 5 Std")
schritt("C4", "C", "btn9Std", "OnSelect", panel_knopf_onselect("btn9Std"), "9 Std: anderer Tag ab 08:00")
l14 = orig("Label14", "Text")
assert l14.count("dpDatum.SelectedDate") == 1
schritt("C5", "C", "Label14", "Text", l14.replace("dpDatum.SelectedDate", "dpDatumTischePanel.SelectedDate"), "Hinweistext liest das Panel-Datum (BD-26)")
l14c = orig("Label14", "Color")
assert l14c.count("dpDatum.SelectedDate") == 1
schritt("C5", "C", "Label14", "Color", l14c.replace("dpDatum.SelectedDate", "dpDatumTischePanel.SelectedDate"), "Hinweisfarbe liest das Panel-Datum (BD-26)")

# Teil D: Kleinigkeiten
oss = orig("ddStockwerk", "OnSelect")
assert oss.count("Set(varAusgewaehltePlusDauer, 0)") == 1
schritt("D1", "D", "ddStockwerk", "OnSelect", oss.replace("Set(varAusgewaehltePlusDauer, 0)", "Set(varAusgewaehltePlusDauer, Blank())"), "Dauer leeren statt 0 (BD-12)")
for i, c in enumerate(["Icon1", "Icon1_1", "Image6", "btnHitArea_1"]):
    schritt("D2", "D", c, "OnSelect", aktualisieren(c), "„Aktualisiert.“ nur bei Erfolg (BD-10)")
schritt("D3", "D", "btnStornierenKlein", "OnSelect", mit_sperre("btnStornierenKlein"), "Mehrfach-Stornieren mit Zweifach-Sperre")
ab = orig("btnAbbrechenTischePanel", "OnSelect")
assert ab.count("Set(varZeigeTischBuchungForm, false);\n") == 2
schritt("D4", "D", "btnAbbrechenTischePanel", "OnSelect", ab.replace("Set(varZeigeTischBuchungForm, false);\n", "", 1), "Doppelte Zeile weg (BD-25)")

# ---------------------------------------------------------------------------------------------
# Prüfungen
# ---------------------------------------------------------------------------------------------
NEUE_VARS = {"varSperreBis", "varVerlGrenze", "varVerlGrenzeTab", "varVerlTisch", "varVerlEndeAlt", "varVerlTagesende",
             "varVerlNaechste", "varVerlBuchung", "varVerlEndeNeu", "varStornoBuchung", "varCheckinBuchung",
             "varNeuTischTitel", "varNeuTischID", "varNeuEmail", "varNeuDatum", "varNeuStartZeit", "varNeuEndeZeit",
             "varNeuBisRoh", "varNeuBis", "varNeuJetzt", "varNeuSpanStart", "varNeuSpanEnde", "varNeuGesamt",
             "varNeuTischBelegt", "varNeuIchBelegt", "varSerienID", "varNeuFehler", "varNeuAnzahl", "varNeuKonflikt",
             "colNeuTermine", "colNeuBelegt", "colNeuIch", "colNeuErgebnis", "colNeuNachlese"}
alt_text = "\n".join(a.props.values())
ALTE_VARS = set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", alt_text))
assert not (NEUE_VARS & ALTE_VARS), NEUE_VARS & ALTE_VARS
STEUER = set(a.typ)
PRAEFIX = r"(?:btn|dd|dp|gal|con|lbl|chk|tgl|Label|Icon|Image|img|Rectangle|Circle|Gallery)"

fehler = []
protokoll = []
benutzt = set()
for s in S:
    key = f"{s['control']}.{s['prop']}"
    neu = s["neu"]
    pr = []
    if s["control"] not in STEUER:
        fehler.append(f"{key}: Steuerelement fehlt im Export")
    if s["art"] == "ersetzen":
        if key not in a.props:
            fehler.append(f"{key}: Property fehlt im Export (art=ersetzen)")
    else:
        if key in a.props:
            fehler.append(f"{key}: Property existiert schon (art=neu)")
    if not A.klammern_ok(neu):
        fehler.append(f"{key}: Klammern")
    if "//" in A.ausserhalb_strings(neu):
        fehler.append(f"{key}: Kommentar")
    de = A.to_de(neu)
    if A.from_de(de) != neu:
        fehler.append(f"{key}: Rückübersetzung weicht ab")
    if not A.klammern_ok(de):
        fehler.append(f"{key}: Klammern (de)")
    ohne = A.ausserhalb_strings(neu)
    for v in set(re.findall(r"\b((?:var|col)[A-ZÄÖÜa-zäöü0-9_]+)\b", ohne)):
        benutzt.add(v)
        if v not in ALTE_VARS and v not in NEUE_VARS:
            fehler.append(f"{key}: unbekannte Variable {v}")
    for n in set(re.findall(r"\b(" + PRAEFIX + r"[A-ZÄÖÜa-zäöü0-9_]*)\.", ohne)):
        if n not in STEUER:
            fehler.append(f"{key}: unbekanntes Steuerelement {n}")
    for n in set(re.findall(r"\b(Reset)\((\w+)\)", ohne)):
        if n[1] not in STEUER:
            fehler.append(f"{key}: Reset auf unbekanntes Steuerelement {n[1]}")
    if s["prop"] == "OnSelect" and ("Patch(Tischbuchungen" in ohne or "Remove(Tischbuchungen" in ohne) and LADE not in neu:
        fehler.append(f"{key}: Schreibstelle ohne L2-Ladezeile")
    if s["prop"] == "OnSelect" and ("Patch(" in ohne or "Remove(" in ohne):
        if not neu.startswith("If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),"):
            fehler.append(f"{key}: Schreibstelle ohne Zweifach-Sperre")
        if neu.count("Set(varIsLoading, false)") != 1 or not neu.rstrip().endswith("Set(varIsLoading, false)\n)"):
            fehler.append(f"{key}: varIsLoading wird nicht genau einmal am Ende zurückgesetzt")
    s["de"] = de
    s["orig"] = a.props.get(key)
    s["orig_de"] = A.to_de(s["orig"]) if s["orig"] is not None else None
    if s["orig_de"] is not None:
        s["diff"] = "\n".join(difflib.unified_diff(s["orig_de"].split("\n"), de.split("\n"), lineterm="", n=2))
    else:
        s["diff"] = ""
    s["pfad"] = a.pfad(s["control"])

# Jede neue Variable muss irgendwo gesetzt werden.
for v in NEUE_VARS:
    gesetzt = any(re.search(r"(Set|ClearCollect)\(\s*" + v + r"\b", s["neu"]) for s in S)
    if not gesetzt:
        fehler.append(f"{v}: wird nirgends gesetzt")

# Kein Steuerelement/Property doppelt.
keys = [f"{s['control']}.{s['prop']}" for s in S]
for k in set(keys):
    if keys.count(k) > 1:
        fehler.append(f"{k}: doppelt im Paket")

# Wer liest varSelectedBuchung bzw. die Tab-Variable nach dem Paket? (B0 muss weg sein)
stand = dict(a.props)
for s in S:
    stand[f"{s['control']}.{s['prop']}"] = s["neu"]
for k, v in stand.items():
    if a.pfad(k.split(".")[0]).find("conVerwaltenDialog_1") >= 0 and re.search(r"\bvarSelectedBuchung\b", v):
        fehler.append(f"{k}: Tab-Dialog liest noch varSelectedBuchung (B0)")
# Dauer-Knöpfe fragen keine Daten mehr ab.
for k, v in stand.items():
    c = k.split(".")[0]
    if re.match(r"btn(Plus|Minus)\d", c) and "Tischbuchungen" in v:
        fehler.append(f"{k}: fragt noch Tischbuchungen ab")

# Nach dem Paket: jede Schreibstelle auf Tischbuchungen hat Zweifach-Sperre und Ladezeile.
schreib = sorted(k for k, v in stand.items() if re.search(r"(Patch|Remove)\(\s*Tischbuchungen", A.ausserhalb_strings(v)))
for k in schreib:
    v = stand[k]
    if not v.startswith("If(\n  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis),"):
        fehler.append(f"{k}: Schreibstelle nach dem Paket ohne Zweifach-Sperre")
    if LADE not in v:
        fehler.append(f"{k}: Schreibstelle nach dem Paket ohne L2-Ladezeile")

# Delegation: In Server-Prädikaten auf Tischbuchungen keine With-Werte (Handy-App, APP_WISSEN: Warnung gemessen).
def praedikate(f):
    ohne_s = A.ausserhalb_strings(f)
    for m in re.finditer(r"\b(Filter|LookUp)\(\s*Tischbuchungen\s*,", ohne_s):
        i, tiefe = m.end(), 1
        while tiefe:
            tiefe += {"(": 1, ")": -1}.get(ohne_s[i], 0)
            i += 1
        yield ohne_s[m.end(): i - 1]
ERLAUBT_KLEIN = {"true", "false"}
anzahl_praed = 0
for s in S:
    for pr in praedikate(s["neu"]):
        anzahl_praed += 1
        for w in re.findall(r"(?<![.\w])([a-zäöü][A-Za-zÄÖÜäöü0-9_]*)\b(?!\s*\()", pr):
            if w not in ERLAUBT_KLEIN and not w.startswith(("var", "col", "dd", "dp", "btn")):
                fehler.append(f"{s['control']}.{s['prop']}: With-Wert '{w}' im Server-Prädikat")

json.dump(S, open(os.path.join(ZIEL, "bloecke.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
zeilen = [f"Erzeugt von werkzeuge/paket_k_v2.py aus dem Export vom 07.10.2026 (veröffentlicht, enthält L2).",
          f"{len(S)} Properties in {len(set(s['nr'] for s in S))} Schritten, {len(NEUE_VARS)} neue Variablen/Collections (vorher in der App unbenutzt: geprüft).",
          "Je Property geprüft: Steuerelement im Export, Property vorhanden (ersetzen) bzw. noch nicht vorhanden (neu),",
          "Klammern (englisch und deutsch), keine Kommentare, deutsch -> englisch ergibt wieder exakt die Vorlage,",
          "alle var/col-Namen bekannt, alle Steuerelement-Namen im Export, Reset nur auf vorhandene Steuerelemente.", ""]
for s in S:
    plus = sum(1 for z in s["diff"].split("\n") if z.startswith("+") and not z.startswith("+++"))
    minus = sum(1 for z in s["diff"].split("\n") if z.startswith("-") and not z.startswith("---"))
    zeilen.append(f"OK  {s['nr']:<4} {s['control'] + '.' + s['prop']:<36} {s['art']:<9} {len(s['de'].splitlines()):>4} Zeilen  +{plus}/-{minus}")
zeilen += ["", "Gesamtprüfungen auf dem Stand NACH dem Paket:",
           f"OK  Schreibstellen auf Tischbuchungen ({len(schreib)}): alle mit Zweifach-Sperre und L2-Ladezeile: " + ", ".join(schreib),
           "OK  Kein Steuerelement im Tab-Dialog (conVerwaltenDialog_1) liest noch varSelectedBuchung (Befund B0 geschlossen)",
           "OK  Kein Plus-/Minus-Knopf fragt noch Tischbuchungen ab (vorher 24 Properties mit eigener Abfrage)",
           f"OK  {anzahl_praed} Server-Prädikate auf Tischbuchungen im Paket: keines nutzt With-Werte (nur Spalten, globale Variablen, Steuerelemente)",
           "OK  Jede neue Variable wird mindestens einmal gesetzt; keine Property doppelt im Paket"]
if fehler:
    zeilen = ["FEHLER:"] + ["  " + f for f in fehler]
open(os.path.join(ZIEL, "pruefung.txt"), "w", encoding="utf-8").write("\n".join(zeilen) + "\n")
print("\n".join(zeilen))
if fehler:
    sys.exit(1)
