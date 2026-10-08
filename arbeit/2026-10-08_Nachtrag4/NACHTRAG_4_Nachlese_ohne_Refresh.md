# Nachtrag 4 (08.10.): Nachlese ohne `Refresh`, bei jeder Buchung schneller

> Für den Chat, der Josias führt. Gilt für **G6** (Gesamtplan) und **F4** (Paket F). **Ersetzt Nachtrag 3** (enthält dessen Änderung schon). Im Vault ablegen.

## Kurzfassung
- **Was sich ändert:** Beide Speichern-Knöpfe kommen ganz **ohne** `Refresh(Tischbuchungen)` aus.
  - Nachtrag 3 hat das `Refresh` im Zweig „nichts gebucht“ entfernt.
  - Jetzt entfällt auch das `Refresh` vor der Nachlese. Das ist der Teil, der bei **jeder** Buchung läuft.
- **Warum es vorher nötig schien (H6):** Die Nachlese war **wortgleich** mit der Vorprüfung `colNeuBelegt`. Hätte Power Apps die gleiche Abfrage aus einem Zwischenspeicher beantwortet, hätte die Nachlese den Stand **vor** dem Patch gezeigt. Das `Refresh` sollte das verhindern.
- **Die Lösung:** Die Nachlese ist jetzt eine **eigene, bei jedem Klick eindeutige** Abfrage. Ihre untere Zeitgrenze `varNeuNachVon` liegt um die Sekunden seit Mitternacht (plus 1) vor dem Beginn. Damit ist die Abfrage-URL bei jedem Klick anders und kann nicht aus einem Zwischenspeicher kommen. Das ist dasselbe Prinzip wie die gemessene L2-Ladezeile, die dafür `Now()` nutzt.
- **Ausgewertet wird wie bisher:**
  - Eigene neue Zeilen werden über **`SerienID`** gezählt (`varNeuAnzahl`).
  - Gleichzeitige fremde Buchungen findet die **Überlappung** mit kleinerer ID (`varNeuKonflikt`).
  - Zusätzlich geholte Zeilen (Ende bis zu 24 Std. vor Beginn) überlappen nie mit den neuen Terminen und zählen daher nicht.
- **Warum nicht nur über `SerienID`?** Eine reine `SerienID`-Abfrage zählt die eigenen Zeilen, findet aber **keine** gleichzeitige fremde Buchung. Die Warnung „Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht“ wäre weg. Deshalb bleibt die Abfrage über Tisch und Zeit, nur eindeutig gemacht. Das sind 1 statt 2 Abfragen.

## Belege
| Was | Kennzeichnung | Quelle |
|---|---|---|
| Nach einem Patch zeigt die eigene Liste die neue Buchung **ohne** `Refresh` | **gemessen** in der Handy-App (gleiche App-Einstellungen, gleiche Liste) | `05_HANDY_APP/TESTPROTOKOLL.md`, Test TB-1: „Gebucht: UG Desk 17 … automatischer Wechsel zu „Meine“; dort am Ende „UG Desk 17 …““. `btnBuchen` hat kein `Refresh` |
| Nachlese mit einer **anders geformten** Abfrage als die Vorprüfung, ohne `Refresh` | **gemessen** in der Handy-App (TB-1 „Gebucht“, also Nachlese gefunden) | Handy `btnBuchen.OnSelect`: Vorprüfung `LookUp`, Nachlese `ClearCollect(colKollision; Filter(…))` |
| Eindeutige Abfrage-URL schließt den Zwischenspeicher aus | **belegt** als Prinzip in L2 (veröffentlicht, gemessen schnell) | `UEBERGABE_Grundriss_L2_v0.3_1.md`: „Durch `Now()` ist außerdem jede Abfrage-URL eindeutig …“ |
| Ob die Desktop-Galerien nach dem Sammel-Patch (Tabelle) genauso von selbst aktualisieren | **geschlussfolgert** aus der Handy-Messung (dort Einzel-Patch) | Test 2 unten |

## Wirkung auf die Abfragen (geschlussfolgert, im Monitor prüfbar)
Erfolgreiche Buchung, **vorher** (Gesamtplan bzw. Paket F):
1. Vorprüfung: 3 Abfragen (Tisch belegt, ich belegt, Tisch gesperrt).
2. Sammel-Patch.
3. `Refresh`: Neuabfrage aller an `Tischbuchungen` gebundenen Anzeigen, also 2 Galerien. Aus dem Panel bis zu **7**, weil das Panel zu diesem Zeitpunkt noch offen ist (Tischliste, Knöpfe 5/9 Std.).
4. Nachlese: 1.
5. Ladezeile: 1.

**Nachher:** Schritt 3 entfällt. **Ersparnis je Buchung: 2 Abfragen aus dem Grundriss-Dialog, bis zu 7 aus dem Panel.** Dazu kommt Nachtrag 3 (nur im Zweig „nichts gebucht“).
- Ob Power Apps nach dem Patch die beiden Galerien einmal selbst neu lädt, zeigt der Monitor. Laut Handy-Messung zeigen sie die neue Buchung. Das `Refresh` war dann eine **zweite** Welle.
- Die Nachlese holt bis zu einem Tag mehr Zeilen **eines** Tisches, also höchstens ein paar Zeilen mehr.

## So einfügen
- **G6** (noch nicht oder schon eingefügt, auch nach Nachtrag 3): die beiden G6-Blöcke unten, ganze Property ersetzen.
- **Paket F, Schritt F4:** die beiden F4-Blöcke unten statt der F4-Blöcke aus `UEBERGABE_PaketF.md` bzw. Nachtrag 3.

## Test
1. **Einzelbuchung** im Grundriss-Dialog → „Gebucht: …“. In SharePoint steht die Zeile.
2. **Liste ohne Aktualisieren:** Direkt danach steht die neue Buchung im Dashboard („My personal desk“, wenn heute) und im Tab „Buchungen“, **ohne** auf Aktualisieren zu tippen. Dasselbe aus dem Panel „Tisch buchen“.
3. **Serie** (Mo–Fr, 2 Wochen, ein Tag belegt) → „9 von 10 Terminen gebucht …“. Die Zählung kommt aus der Nachlese.
4. **Gleichzeitig:** zwei Browserfenster (zwei Konten oder Josias + Kollege), derselbe Tisch und dieselbe Zeit, möglichst gleichzeitig „Speichern“ → einer bekommt „Gebucht“, der andere „Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht …“.
5. **Zweimal hintereinander dieselbe Zeit:** buchen, stornieren, sofort dieselbe Zeit wieder buchen → „Gebucht“, **nicht** „nicht angekommen“. Das ist der Zwischenspeicher-Fall.
6. **Optional Monitor:** Speichern → nach dem Patch genau **eine** `getRows`-Anfrage der Nachlese mit `Endzeit gt …`. Diese Uhrzeit weicht von der Vorprüfung ab. Keine `Refresh`-Welle mehr.

**Wenn Test 2 scheitert** (neue Buchung erst nach Aktualisieren sichtbar): Das ist kein Datenfehler, nur die Anzeige. Rückfall auf Nachtrag 3 (Refresh vor der Nachlese) oder melden. Dann setzt Claude Code ein `Refresh` **nach** dem Schließen des Panels, also nur 2 statt 7 Abfragen.
**Wenn Test 1, 3 oder 5 „nicht angekommen“ zeigt, obwohl die Zeile in SharePoint steht:** sofort Rückfall auf Nachtrag 3 und melden.

## Rückfall
Die Blöcke aus **Nachtrag 3** (`arbeit/2026-10-08_Nachtrag3/NACHTRAG_3_Speichern_ohne_Refresh.md`) einsetzen: mit `Refresh` vor der Nachlese, ohne das im Zweig „nichts gebucht“. Ganz zurück: G6 aus `GESAMTPLAN.md` bzw. F4 aus `UEBERGABE_PaketF.md`.

## Blöcke für G6 (statt G6 in `GESAMTPLAN.md` bzw. Nachtrag 3)

**`btnSpeichern.OnSelect`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen**

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; varSelectedTisch.Titel);;
  Set(varNeuTischID; varSelectedTisch.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatum.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeDialog; false);;
        Set(varWiederholen; false);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Set(varTagSa; false);;
        Set(varTagSo; false)
      )
    );;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichernTischePanel.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen**

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; ddTischePanel.Selected.Titel);;
  Set(varNeuTischID; ddTischePanel.Selected.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatumTischePanel.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis_1.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeTischBuchungForm; false);;
        Set(varAktiverTab; "dashboard");;
        Set(varWiederholen; false);;
        Reset(chkWiederholenPanel);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Reset(tglTagMo_1);;
        Reset(tglTagDi_1);;
        Reset(tglTagMi_1);;
        Reset(tglTagDo_1);;
        Reset(tglTagFr_1);;
        Set(varAusgewaehltePanelDauer; Blank());;
        Set(varStartOverridePanel; "");;
        Set(varEndeOverridePanel; "")
      )
    );;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

## Blöcke für F4 (statt F4 in `UEBERGABE_PaketF.md` bzw. Nachtrag 3)

**`btnSpeichern.OnSelect`** · Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen**

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; varSelectedTisch.Titel);;
  Set(varNeuTischID; varSelectedTisch.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatum.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeDialog; false);;
        Set(varWiederholen; false);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Set(varTagSa; false);;
        Set(varTagSo; false)
      )
    );;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichernTischePanel.OnSelect`** · Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen**

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varNeuTischTitel; ddTischePanel.Selected.Titel);;
  Set(varNeuTischID; ddTischePanel.Selected.ID);;
  Set(varNeuEmail; User().Email);;
  Set(varNeuDatum; dpDatumTischePanel.SelectedDate);;
  Set(varNeuStartZeit; Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuEndeZeit; Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0));;
  Set(varNeuBisRoh; If(varWiederholen; dpWiederholenBis_1.SelectedDate; varNeuDatum));;
  Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
  Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(
    colNeuTermine;
    ForAll(
      Filter(
        ForAll(Sequence(If(varNeuBis < varNeuDatum; 0; DateDiff(varNeuDatum; varNeuBis; TimeUnit.Days) + 1); 0); DateAdd(varNeuDatum; Value; TimeUnit.Days)) As D;
        !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
      ) As T;
      {Start: T.Value + varNeuStartZeit; Ende: T.Value + varNeuEndeZeit}
    )
  );;
  If(
    IsBlank(varNeuTischTitel) || IsBlank(varNeuTischID);
    Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
    varNeuEndeZeit <= varNeuStartZeit;
    Notify("Das Ende muss nach dem Beginn liegen."; NotificationType.Warning);
    varWiederholen && !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
    Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
    varWiederholen && varNeuBisRoh < varNeuDatum;
    Notify("Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum. Bitte das Enddatum anpassen."; NotificationType.Warning);
    !IsBlank(LookUp(Tische; ID = varNeuTischID && Gesperrt = true).ID);
    Notify("Dieser Tisch ist zurzeit gesperrt. Bitte einen anderen Tisch wählen."; NotificationType.Warning);
    IsEmpty(colNeuTermine);
    Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning);
    First(colNeuTermine).Start < varNeuJetzt;
    Notify("Diese Zeit liegt in der Vergangenheit. Bitte eine spätere Zeit wählen."; NotificationType.Warning);
    Set(varNeuSpanStart; First(colNeuTermine).Start);;
    Set(varNeuSpanEnde; Last(colNeuTermine).Ende);;
    Set(varNeuGesamt; CountRows(colNeuTermine));;
    ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(
      colNeuErgebnis;
      ForAll(
        colNeuTermine As T;
        {
          Start: T.Start;
          Ende: T.Ende;
          Grund: If(
            !IsBlank(LookUp(colNeuBelegt; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "tisch";
            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
      Notify(
        If(
          varNeuGesamt = 1;
          If(varNeuTischBelegt = 1; "Der Tisch ist in dieser Zeit schon belegt. Bitte einen anderen Tisch oder eine andere Zeit wählen."; "Du hast in dieser Zeit schon einen Tisch gebucht.");
          "Nichts gebucht: An allen " & varNeuGesamt & " Terminen ist der Tisch belegt oder du hast schon einen Tisch."
        );
        NotificationType.Warning
      );
      Set(varSerienID; Text(GUID()));;
      IfError(
        Patch(
          Tischbuchungen;
          ForAll(Filter(colNeuErgebnis; Grund = "frei"); Defaults(Tischbuchungen));
          ForAll(
            Filter(colNeuErgebnis; Grund = "frei") As F;
            {
              Tisch: {Id: varNeuTischID; Value: varNeuTischTitel};
              Startzeit: F.Start;
              Endzeit: F.Ende;
              Person: {
                Claims: "i:0#.f|membership|" & Lower(User().Email);
                Department: "";
                DisplayName: User().FullName;
                Email: User().Email;
                JobTitle: "";
                Picture: ""
              };
              SerienID: varSerienID
            }
          )
        );
        Set(varNeuFehler; true);
        Set(varNeuFehler; false)
      );;
      Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
        Notify(
          varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
          If(varNeuTischBelegt > 0; " " & varNeuTischBelegt & "× war der Tisch schon belegt."; "") &
          If(varNeuIchBelegt > 0; " " & varNeuIchBelegt & "× hattest du zu der Zeit schon einen Tisch."; "") &
          If(varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt > varNeuAnzahl; " " & (varNeuGesamt - varNeuTischBelegt - varNeuIchBelegt - varNeuAnzahl) & " Termin(e) konnten nicht gespeichert werden."; "") &
          If(varNeuBisRoh > varNeuBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
          NotificationType.Warning
        )
      );;
      If(
        varNeuAnzahl > 0;
        Set(varZeigeTischBuchungForm; false);;
        Set(varAktiverTab; "dashboard");;
        Set(varWiederholen; false);;
        Reset(chkWiederholenPanel);;
        Set(varWiederholenModus; "Wochentage");;
        Set(varTagMo; false);;
        Set(varTagDi; false);;
        Set(varTagMi; false);;
        Set(varTagDo; false);;
        Set(varTagFr; false);;
        Reset(tglTagMo_1);;
        Reset(tglTagDi_1);;
        Reset(tglTagMi_1);;
        Reset(tglTagDo_1);;
        Reset(tglTagFr_1);;
        Set(varAusgewaehltePanelDauer; Blank());;
        Set(varStartOverridePanel; "");;
        Set(varEndeOverridePanel; "")
      )
    );;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

## Maschinelle Prüfung

```
4 Properties (G6 und F4, je btnSpeichern + btnSpeichernTischePanel), Grundlage: Gesamtplan bzw. Paket F + Nachtrag 3.
Je Block geprüft: genau zwei Stellen geändert (Nachtrag 3 + Nachlese), kein Refresh(Tischbuchungen) mehr, Nachlese anders geformt als die Vorprüfung, Reihenfolge Patch → varNeuNachVon → Nachlese, keine With-Lokale im Server-Prädikat, Auswertung (SerienID-Zählung, Überlappung) unverändert, Zweifach-Sperre und Ladezeile vorhanden, in F4 die Freigabe-Regel in der Nachlese, Klammern, Rückübersetzung.
Prüfung: 0 Fehler
```
