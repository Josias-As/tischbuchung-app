# Weitere Fehler, Umbaupläne und Stil-Audit (Paket L)
**08.10.2026, nachts · Basis: veröffentlichter Export vom 07.10. · Paket L: 82 Properties, maschinell erzeugt und geprüft (`werkzeuge/paket_l.py`), ändert keine Property, die Paket K v2 ändert · Reihenfolge: erst Paket K v2, dann L · unabhängig geprüft, Befunde eingearbeitet**

Kennzeichnung: **belegt** (Export), **geschlussfolgert**, **UNSICHER**, **Einschätzung**.

## 0. Kurzfassung
- **Unabhängig geprüft** (`pruefung_paket_l.md`): Das Ergebnis waren 2 Fehler, 4 Risiken und 23 Hinweise. Eingearbeitet sind: Tab-Kontrast (L4), Titelbreite (L9: `lblTitel3` ohne Präfix), Outlook-Plan P5 neu, P3 mit Listen-Aktualisierung, P1-Datumsbedingung, P9 „nur eigene Elemente“, UTC-Hinweis bei P2 und die Zahlen im Stil-Audit. Danach wurde alles neu erzeugt und maschinell geprüft. **L10–L13 (25 Properties: Auswahl, Hover, Dialoghintergründe, Zurücksetzen) und die P1-Formeln kamen nach der Prüfung dazu. Sie sind maschinell geprüft, die zweite unabhängige Prüfung steht in `pruefung_paket_l_2.md`.**
- **Elf neue Befunde** (F-L1 bis F-L11), die Paket K v2 nicht abdeckt. Sieben davon behebt Paket L direkt, vier brauchen einen Umbau (P1, P3). **F-L11 (Datum bleibt stehen → Buchung am falschen Tag) wurde erst bei der Selbstprüfung gefunden und ist neben F-L1 der wichtigste.** Der wichtigste: Die Startliste bietet **22:00** an. Wählt man das, ist die Endliste leer, und die Buchung wird mit Ende **00:00 desselben Tages** gespeichert, also mit Ende vor Beginn (L1).
- **Die Oberfläche wirkt aus zwei Apps zusammengesetzt** (belegt). Der Buchungsdialog aus dem Grundriss nutzt das graublaue Standarddesign von Power Apps, das Tische-Panel das Markenblau `#171496`. „Speichern“ ist einmal grün, sonst blau. „Stornieren“ sieht aus wie „Speichern“. Bei sieben Knöpfen verschwindet beim Drücken die Schrift. Man sieht nicht, welcher Tab aktiv ist. Deutsch und Englisch sind gemischt.
- **Paket L** behebt das mit 82 kleinen Properties: nur Farben, Hover/Auswahl, Texte, Sortierung, eine Liste. Kein Schreibvorgang wird geändert. Risiko: niedrig.
- **Zehn größere Umbaupläne** (Abschnitt 3) sind durchdacht, aber nicht als Formel ausgearbeitet, weil sie neue Steuerelemente, Spalten oder Flows brauchen oder deine Entscheidung. Der wichtigste: **Im Grundriss kann man einen Tisch, der zu irgendeiner Zeit des Tages belegt ist, nicht für die freien Stunden buchen.**

## 1. Neue Fehler (nicht in Paket K v2)
| # | Fehler | Beleg | Folge | Lösung |
|---|---|---|---|---|
| F-L1 | Startliste endet bei **22:00**, die Endliste beginnt bei Start + 30 Min und endet 22:00 → Endliste leer → `Time(Value(""); …)` = 00:00 | `ddStart.Items`, `ddStartTischePanel.Items`: `Sequence(… + 1)`; `ddEnde.Items`: `Sequence(RoundDown((22*60 − start)/30))` | **Buchung 22:00–00:00 (Ende vor Beginn)** im veröffentlichten Stand (geschlussfolgert, nicht gemessen). Mit Paket K v2 kommt die Meldung „Ende muss nach Beginn liegen“. Fällt die leere Endliste allerdings auf ihren Standardwert „22:30“ zurück (UNSICHER), nähme K v2 sogar 22:00–22:30 an. Ab 21:31 ist 22:00 heute die **einzige** Startzeit | **L1** |
| F-L2 | Dashboard-Liste „My personal desk“ ist **nicht nach Uhrzeit sortiert** (Reihenfolge = ID = Buchungszeitpunkt) | `galTischbuchungenHeute.Items` ohne Sortierung | Wer erst nachmittags und dann vormittags bucht, sieht 14:00 vor 08:00 | **L2** (der Check-in-Dialog rechnet seine Position über dieselbe Reihenfolge und wird mit angepasst) |
| F-L3 | Gedrückter Knopf: **Schrift unsichtbar** (schwarz auf schwarz, grün auf grün) | `PressedColor = Self.Fill` bzw. `Color.Black` bei `PressedFill` gleicher Farbe: `btnSpeichern`, `btnAbbrechen`, `btnSchließen2/3/4/4_1`, `btnSchließenKlein` | Bei jedem Klick flackert der Knopf leer. Wirkt kaputt | **L3** |
| F-L4 | **Kein aktiver Tab erkennbar**: „Dashboard“ und „Buchungen“ haben immer dieselbe Farbe | `btnTabDashboard.Fill` = `btnTabBuchungen.Fill` = `#171496`, fest | Nutzer wissen nicht, wo sie sind | **L4** |
| F-L5 | **Profilfarbe zufällig bei jedem Start** | `App.OnStart`: `Set(varProfilFarbe; Switch(RandBetween(1; 8); …))` | Das eigene Initialen-Symbol wechselt jedes Mal die Farbe. Wirkt wie ein Fehler | **L5** (über `Circle2.Fill`, damit `App.OnStart` nicht mit Paket K kollidiert. `varProfilFarbe` wird danach nicht mehr gelesen und kann bei L4-Aufräumen weg) |
| F-L6 | Details-Popup zeigt immer **„Besetzt“ in Rot**, auch wenn nicht eingecheckt (Kachel ist dann orange) | `lblStatus.Text = "Besetzt"`, `Color = #EB3951` | Widerspricht der Kachelfarbe | **L6** |
| F-L7 | **App über Mitternacht offen**: `varAnsichtsDatum` bleibt auf gestern | wird nur in `App.OnStart` und `dpAnsichtsDatum.OnChange` gesetzt (belegt) | Wer die App morgens im alten Browser-Tab weiter benutzt, sieht gestern. Paket K verhindert immerhin Buchungen in der Vergangenheit | Plan P3 |
| F-L8 | **Grundriss: freie Restzeit eines belegten Tisches nicht buchbar** | `btnHitArea.OnSelect`: Ist irgendeine Buchung „relevant“, öffnet sich nur das Details-Popup. Heute: aktive Buchung oder Beginn in 30 Min. Anderer Tag: **irgendeine** Buchung an dem Tag | Tisch 08:00–10:00 gebucht → für 13:00–17:00 muss man ins Panel. Wer das nicht weiß, hält den Tisch für den ganzen Tag belegt | Plan P1 |
| F-L11 | **Eingaben bleiben vom letzten Öffnen stehen**: Datum, Start, Ende und Wiederholen-bis im Buchungsdialog (und Zeiten im Panel) werden beim Öffnen nicht zurückgesetzt | `Reset` gibt es im Export nur für Panel-Listen und -Schalter. `dpDatum`, `dpWiederholenBis(_1)` werden nirgends zurückgesetzt; `ddStart`/`ddEnde` nur bei Datumswechsel (belegt). `DefaultDate = varAnsichtsDatum` greift nur, wenn sich `varAnsichtsDatum` ändert (geschlussfolgert, Standardverhalten klassischer Steuerelemente) | **Stille Buchung am falschen Tag**: Wer im Dialog „morgen“ wählt, abbricht und eine andere Kachel anklickt, sieht wieder „morgen“, obwohl der Grundriss heute zeigt. Mit Paket K v2 kommt bei alten Uhrzeiten von heute die Meldung „Vergangenheit“, was ohne L13 verwirrt | **L13** (bei Paket K v2 Pflicht) |
| F-L10 | **Keine automatische Aktualisierung** (kein Timer in der App) | Steuerelement-Typen im Export: kein Timer (belegt) | Grundriss und Listen veralten, solange die App offen ist | Plan P3 |
| F-L9 | Heute ist eine Kachel **grün**, obwohl der Tisch ab 14:00 belegt ist. Der Buchungsdialog zeigt keine Belegung an | Kachelformel prüft nur „jetzt bis +30 Min“ (belegt) | Nutzer wählt 09:00–17:00 und bekommt „Tisch belegt“ ohne Hinweis, wann frei | Plan P1 |

## 2. Paket L (Formeln, nach Paket K v2 einfügen)
Ablauf wie bei Paket K: ganze Property ersetzen, App-Prüfung, kurzer Test. Alle Schritte sind unabhängig voneinander. **Rückfall:** Original aus Anhang. Die Texte (L9) sind Vorschläge. Wenn du andere Wörter willst, ändere nur den Text in Anführungszeichen.

### L1 Letzte Startzeit 21:30 statt 22:00

**`ddStart.Items`** (Ort: `Screen1 > conBuchungDialog > ddStart`) ersetzen durch:

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatum.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(Max(0; RoundDown((minutenEnde - minutenStart) / 30; 0)); 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStartTischePanel.Items`** (Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel`) ersetzen durch:

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatumTischePanel.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(Max(0; RoundDown((minutenEnde - minutenStart) / 30; 0)); 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**Test:** Panel und Buchungsdialog, Datum heute nach 21:30 → keine Startzeit wählbar. Datum morgen → letzte Startzeit 21:30, Ende 22:00 wählbar.

### L2 Eigene Buchungen des Tages nach Startzeit

**`galTischbuchungenHeute.Items`** (Ort: `Screen1 > conDashboard > galTischbuchungenHeute`) ersetzen durch:

```
SortByColumns(
  Filter(
    Tischbuchungen;
    Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
  );
  "Startzeit";
  SortOrder.Ascending
)
```

**`conCheckinDialog.Y`** (Ort: `Screen1 > conCheckinDialog`) ersetzen durch:

```
With(
        { _idx: CountRows(Filter(galTischbuchungenHeute.AllItems; Startzeit < varSelectedBuchung.Startzeit || (Startzeit = varSelectedBuchung.Startzeit && ID < varSelectedBuchung.ID))) + 1 };
            conDashboard.Y + galTischbuchungenHeute.Y + (_idx - galTischbuchungenHeute.VisibleIndex) * galTischbuchungenHeute.TemplateHeight + (galTischbuchungenHeute.TemplateHeight - Self.Height) / 2
            )
```

**Test:** Heute zwei Buchungen in umgekehrter Reihenfolge anlegen (erst 14:00, dann 08:00) → Dashboard zeigt 08:00 oben. „Einchecken“ bei der unteren → Dialog erscheint auf Höhe der richtigen Zeile.

### L3 Schrift beim Drücken weiß (vorher schwarz auf schwarz)

**`btnAbbrechen.PressedColor`** (Ort: `Screen1 > conBuchungDialog > btnAbbrechen`) ersetzen durch:

```
Color.White
```

**`btnAbbrechen.PressedFill`** (Ort: `Screen1 > conBuchungDialog > btnAbbrechen`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen2.PressedColor`** (Ort: `Screen1 > conCheckinDialog > btnSchließen2`) ersetzen durch:

```
Color.White
```

**`btnSchließen2.PressedFill`** (Ort: `Screen1 > conCheckinDialog > btnSchließen2`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen3.PressedColor`** (Ort: `Screen1 > conDetailsPopup > btnSchließen3`) ersetzen durch:

```
Color.White
```

**`btnSchließen3.PressedFill`** (Ort: `Screen1 > conDetailsPopup > btnSchließen3`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen4.PressedColor`** (Ort: `Screen1 > conVerwaltenDialog > btnSchließen4`) ersetzen durch:

```
Color.White
```

**`btnSchließen4.PressedFill`** (Ort: `Screen1 > conVerwaltenDialog > btnSchließen4`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSchließen4_1.PressedColor`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnSchließen4_1`) ersetzen durch:

```
Color.White
```

**`btnSchließen4_1.PressedFill`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnSchließen4_1`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSchließenKlein.PressedColor`** (Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnSchließenKlein`) ersetzen durch:

```
Color.White
```

**`btnSchließenKlein.PressedFill`** (Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnSchließenKlein`) ersetzen durch:

```
ColorFade(Color.Black; 30%)
```

**`btnSpeichern.PressedColor`** (Ort: `Screen1 > conBuchungDialog > btnSpeichern`) ersetzen durch:

```
Color.White
```

**Test:** Jeden dieser Knöpfe gedrückt halten: Schrift bleibt lesbar.

### L4 Aktiver Tab dunkel, inaktiver hell

**`btnTabDashboard.Fill`** (Ort: `Screen1 > conHeader > btnTabDashboard`) ersetzen durch:

```
If(varAktiverTab = "dashboard"; ColorValue("#171496"); ColorFade(ColorValue("#171496"); 35%))
```

**`btnTabBuchungen.Fill`** (Ort: `Screen1 > conHeader > btnTabBuchungen`) ersetzen durch:

```
If(varAktiverTab = "buchungen"; ColorValue("#171496"); ColorFade(ColorValue("#171496"); 35%))
```

**Test:** Tab wechseln: Der aktive Tab ist dunkelblau, der andere heller, aber gut lesbar. Die Aufhellung ist nach der Prüfung von 55 % auf 35 % gesenkt, damit die weiße Schrift auf dem inaktiven Tab genug Kontrast hat (etwa 5:1 statt 2,8:1).

### L5 Gleiche Farbe bei jedem Start (aus der Länge der E-Mail-Adresse)

**`Circle2.Fill`** (Ort: `Screen1 > conHeader > Circle2`) ersetzen durch:

```
Switch(
  Mod(Len(User().Email); 8) + 1;
  1; ColorValue("#8CAFF4");
  2; ColorValue("#82C7B3");
  3; ColorValue("#EFA897");
  4; ColorValue("#B59EDC");
  5; ColorValue("#82CCC5");
  6; ColorValue("#F5C295");
  7; ColorValue("#A1AADB");
  ColorValue("#A1B1BA")
)
```

**Test:** App zweimal starten: Profilkreis hat dieselbe Farbe.

### L6 Status statt immer „Besetzt“

**`lblStatus.Text`** (Ort: `Screen1 > conDetailsPopup > lblStatus`) ersetzen durch:

```
If(varSelectedBuchung.CheckedIn; "Eingecheckt"; "Gebucht")
```

**`lblStatus.Color`** (Ort: `Screen1 > conDetailsPopup > lblStatus`) ersetzen durch:

```
If(varSelectedBuchung.CheckedIn; ColorValue("#EB3951"); ColorValue("#FFA500"))
```

**Test:** Grundriss → belegte Kachel (orange) → Popup „Gebucht“ orange. Eingecheckte Kachel (rot) → „Eingecheckt“ rot.

### L7 Wochentag-Schalter grün wie im Panel

**`tglTagMo.TrueFill`** (Ort: `Screen1 > conBuchungDialog > tglTagMo`) ersetzen durch:

```
ColorValue("#00A96B")
```

**`tglTagDi.TrueFill`** (Ort: `Screen1 > conBuchungDialog > tglTagDi`) ersetzen durch:

```
ColorValue("#00A96B")
```

**`tglTagMi.TrueFill`** (Ort: `Screen1 > conBuchungDialog > tglTagMi`) ersetzen durch:

```
ColorValue("#00A96B")
```

**`tglTagDo.TrueFill`** (Ort: `Screen1 > conBuchungDialog > tglTagDo`) ersetzen durch:

```
ColorValue("#00A96B")
```

**`tglTagFr.TrueFill`** (Ort: `Screen1 > conBuchungDialog > tglTagFr`) ersetzen durch:

```
ColorValue("#00A96B")
```

**`dpDatum.IconBackground`** (Ort: `Screen1 > conBuchungDialog > dpDatum`) ersetzen durch:

```
ColorValue("#171496")
```

**`dpWiederholenBis.IconBackground`** (Ort: `Screen1 > conBuchungDialog > dpWiederholenBis`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddStart.ChevronBackground`** (Ort: `Screen1 > conBuchungDialog > ddStart`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddStart.HoverFill`** (Ort: `Screen1 > conBuchungDialog > ddStart`) ersetzen durch:

```
ColorFade(Self.Fill; -20%)
```

**`ddEnde.ChevronBackground`** (Ort: `Screen1 > conBuchungDialog > ddEnde`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddEnde.HoverFill`** (Ort: `Screen1 > conBuchungDialog > ddEnde`) ersetzen durch:

```
ColorFade(Self.Fill; -20%)
```

**`btnSpeichern.Fill`** (Ort: `Screen1 > conBuchungDialog > btnSpeichern`) ersetzen durch:

```
ColorValue("#171496")
```

**`btnSpeichern.PressedFill`** (Ort: `Screen1 > conBuchungDialog > btnSpeichern`) ersetzen durch:

```
ColorFade(Self.Fill; -20%)
```

**`tglAuswahlModus.TrueFill`** (Ort: `Screen1 > conBuchungen > tglAuswahlModus`) ersetzen durch:

```
ColorValue("#171496")
```

**Test:** Grundriss → freie Kachel → Buchungsdialog sieht aus wie das Tische-Panel (blaue Pfeile und Kalender, grüne Wochentage, blauer Speichern-Knopf).

### L8 Stornieren rot statt blau wie Speichern

**`btnStornieren.Fill`** (Ort: `Screen1 > conVerwaltenDialog > btnStornieren`) ersetzen durch:

```
ColorValue("#EB3951")
```

**`btnStornieren_1.Fill`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1`) ersetzen durch:

```
ColorValue("#EB3951")
```

**`btnStornierenKlein.Fill`** (Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein`) ersetzen durch:

```
ColorValue("#EB3951")
```

**Test:** Verwalten-Dialoge: Stornieren ist rot, Speichern/Verlängern blau.

### L9 Text vereinheitlicht

**`lblMyPersonalDesk.Text`** (Ort: `Screen1 > conDashboard > lblMyPersonalDesk`) ersetzen durch:

```
"Meine Tischbuchungen"
```

**`btnTischHinzufügen.Text`** (Ort: `Screen1 > conDashboard > btnTischHinzufügen`) ersetzen durch:

```
"Tisch buchen"
```

**`lblTischeBuchenPanel.Text`** (Ort: `Screen1 > conTischBuchungenPanel > lblTischeBuchenPanel`) ersetzen durch:

```
"Tisch buchen"
```

**`btnPlus1Std.Text`** (Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std`) ersetzen durch:

```
"+1 Std"
```

**`btnPlus2Std.Text`** (Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std`) ersetzen durch:

```
"+2 Std"
```

**`btnPlus3Std.Text`** (Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std`) ersetzen durch:

```
"+3 Std"
```

**`btnPlus1Std_1.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1`) ersetzen durch:

```
"+1 Std"
```

**`btnPlus2Std_1.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1`) ersetzen durch:

```
"+2 Std"
```

**`btnPlus3Std_1.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1`) ersetzen durch:

```
"+3 Std"
```

**`btnMinus1Std.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std`) ersetzen durch:

```
"−1 Std"
```

**`btnMinus2Std.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std`) ersetzen durch:

```
"−2 Std"
```

**`btnMinus3std.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std`) ersetzen durch:

```
"−3 Std"
```

**`lblTischLeer.Text`** (Ort: `Screen1 > conDashboard > lblTischLeer`) ersetzen durch:

```
"Keine Buchungen"
```

**`lblTischLeer_1.Text`** (Ort: `Screen1 > conBuchungen > lblTischLeer_1`) ersetzen durch:

```
"Keine Buchungen"
```

**`lblTitel3.Text`** (Ort: `Screen1 > conVerwaltenDialog > lblTitel3`) ersetzen durch:

```
If(IsBlank(varSelectedBuchung); ""; varSelectedBuchung.Tisch.Value)
```

**`lblTitel3_1.Text`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > lblTitel3_1`) ersetzen durch:

```
"Verwalten: " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel2.Text`** (Ort: `Screen1 > conDetailsPopup > lblTitel2`) ersetzen durch:

```
varSelectedBuchung.Tisch.Value
```

**`lblTischHeute.Text`** (Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblTischHeute`) ersetzen durch:

```
ThisItem.Tisch.Value
```

**Test:** Texte durchsehen. Breite der Plus-/Minus-Knöpfe prüfen: „+1 Std“ ist ein Zeichen länger als „+1Std“ (UNSICHER, ob es abgeschnitten wird; falls ja, `Size` um 1 verkleinern).

### L10 Auswahlbalken im Buchungen-Tab blau wie im Dashboard

**`Rectangle3_2.Fill`** (Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > Rectangle3_2`) ersetzen durch:

```
ColorValue("#171496")
```

**`Rectangle5.Fill`** (Ort: `Screen1 > conBuchungDialog > Rectangle5`) ersetzen durch:

```
ColorValue("#171496")
```

**`Rectangle6.Fill`** (Ort: `Screen1 > conBuchungDialog > Rectangle6`) ersetzen durch:

```
ColorValue("#171496")
```

**`Rectangle6_1.Fill`** (Ort: `Screen1 > conCheckinDialog > Rectangle6_1`) ersetzen durch:

```
ColorValue("#171496")
```

**`Rectangle6_2.Fill`** (Ort: `Screen1 > conDetailsPopup > Rectangle6_2`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddStockwerk.SelectionFill`** (Ort: `Screen1 > conGrundriss > ddStockwerk`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddTischePanel.SelectionFill`** (Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddStartTischePanel.SelectionFill`** (Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddEndTischePanel.SelectionFill`** (Ort: `Screen1 > conTischBuchungenPanel > ddEndTischePanel`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddStart.SelectionFill`** (Ort: `Screen1 > conBuchungDialog > ddStart`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddEnde.SelectionFill`** (Ort: `Screen1 > conBuchungDialog > ddEnde`) ersetzen durch:

```
ColorValue("#171496")
```

**`ddTischePanel.ChevronHoverBackground`** (Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`) ersetzen durch:

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddStartTischePanel.ChevronHoverBackground`** (Ort: `Screen1 > conTischBuchungenPanel > ddStartTischePanel`) ersetzen durch:

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddEndTischePanel.ChevronHoverBackground`** (Ort: `Screen1 > conTischBuchungenPanel > ddEndTischePanel`) ersetzen durch:

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddStart.ChevronHoverBackground`** (Ort: `Screen1 > conBuchungDialog > ddStart`) ersetzen durch:

```
ColorFade(Self.ChevronBackground; -20%)
```

**`ddEnde.ChevronHoverBackground`** (Ort: `Screen1 > conBuchungDialog > ddEnde`) ersetzen durch:

```
ColorFade(Self.ChevronBackground; -20%)
```

**Test:** Buchungen-Tab: Eine Zeile anklicken, der Auswahlbalken ist blau wie im Dashboard. Buchungsdialog, Check-in-Dialog und Details-Popup haben einen blauen Akzentbalken. Eine Auswahlliste öffnen: Die markierte Zeile ist blau. Über den Pfeil fahren: Er wird dunkler blau, nicht graublau.

### L11 Einheitliche Hover-Abdunklung für Klickflächen

**`btnHitArea.HoverFill`** (Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea`) ersetzen durch:

```
RGBA(0; 0; 0; 0,1)
```

**`btnEincheckenHeute.HoverFill`** (Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute`) ersetzen durch:

```
RGBA(0; 0; 0; 0,1)
```

**`btnVerwalten.HoverFill`** (Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten`) ersetzen durch:

```
RGBA(0; 0; 0; 0,1)
```

**`btnVerwalten_2.HoverFill`** (Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2`) ersetzen durch:

```
RGBA(0; 0; 0; 0,1)
```

**`btnHitArea_1.HoverFill`** (Ort: `Screen1 > conHeader > btnHitArea_1`) ersetzen durch:

```
RGBA(0; 0; 0; 0,1)
```

**Test:** Mit der Maus über Grundriss-Kachel, Einchecken-Fläche, Verwalten-Pfeil (Dashboard und Tab) und Logo fahren: Alle dunkeln gleich leicht ab.

### L12 Dialog weiß wie alle anderen Dialoge

**`conVerwaltenDialog_1.Fill`** (Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1`) ersetzen durch:

```
Color.White
```

**`conVerwaltenKlein.Fill`** (Ort: `Screen1 > conBuchungen > conVerwaltenKlein`) ersetzen durch:

```
Color.White
```

**Test:** Buchungen-Tab → Verwalten: Der Dialog ist weiß wie der Verwalten-Dialog im Dashboard. Der kleine Mehrfach-Dialog ebenso.

### L13 Buchungsdialog öffnet immer mit dem Grundriss-Datum und frischen Zeiten

**`btnHitArea.OnSelect`** (Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea`) ersetzen durch:

```
With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today();
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
      )
  };
  If(
    IsBlank(relevanteBuchung);
      Set(varSelectedTisch; ThisItem);;
      Reset(dpDatum);;
      Reset(ddStart);;
      Reset(ddEnde);;
      Reset(dpWiederholenBis);;
      Set(varZeigeDialog; true);;
      Set(varZeigeDetails; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false);;
      Set(varWiederholen; false);;
      Set(varWiederholenModus; "Wochentage");;
      Set(varTagMo; false);;
      Set(varTagDi; false);;
      Set(varTagMi; false);;
      Set(varTagDo; false);;
      Set(varTagFr; false);;
      Set(varTagSa; false);;
      Set(varTagSo; false);
      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; relevanteBuchung);;
      Set(varZeigeDetails; true);;
      Set(varZeigeDialog; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false)
  )
)
```

**`btnTischHinzufügen.OnSelect`** (Ort: `Screen1 > conDashboard > btnTischHinzufügen`) ersetzen durch:

```
Set(varZeigeTischBuchungForm; true);;
Reset(dpDatumTischePanel);;
Reset(ddTischePanel);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Reset(tglTagMo_1);;
Reset(tglTagDi_1);;
Reset(tglTagMi_1);;
Reset(tglTagDo_1);;
Reset(tglTagFr_1);;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

**Test:** (1) Grundriss → freie Kachel → im Dialog Datum auf morgen und 14:00 stellen → Abbrechen. Andere freie Kachel → Dialog zeigt wieder das Grundriss-Datum und die nächste halbe Stunde. (2) Panel öffnen, 09:00–10:00 wählen, mit „<“ schließen, wieder öffnen → Zeiten stehen auf dem Standard. (3) Wiederholen-bis auf in 10 Tagen stellen, abbrechen, neu öffnen → Bis-Datum zurückgesetzt.

## 3. Umbaupläne für größere Punkte (durchdacht, nicht als Formel)
Jeder Plan: Problem → Lösung → was du anlegen musst → Risiko → Aufwand (Einschätzung).

**P1 Grundriss: freie Zeiten belegter Tische buchen (F-L8, F-L9)**
- *Lösung:* Ins Details-Popup kommt ein Knopf **„Andere Zeit buchen“**. Er setzt `varSelectedTisch` auf den Tisch und öffnet den normalen Buchungsdialog (`varZeigeDialog`). Im Buchungsdialog steht eine Zeile **„Heute belegt: 08:00–10:00, 14:00–17:00“** aus `colGrundriss` (keine neue Abfrage). Die Zeile gilt nur, solange das Dialog-Datum dem Grundriss-Datum entspricht; bei einem anderen Datum blendet sie sich aus (`Visible: dpDatum.SelectedDate = varAnsichtsDatum`). Die Speichern-Prüfung aus Paket K v2 bleibt die letzte Instanz.
- *Anlegen:* einen Knopf `btnAndereZeit` im `conDetailsPopup` und ein Label `lblBelegtHeute` im `conBuchungDialog`.
- *Risiko:* niedrig. *Aufwand:* ~1 Std. Die Steuerelemente legst du an (Knopf im Popup, Label im Dialog unter dem Tischnamen).
- *Formeln (aus dem Export erzeugt, Klammern und Rückübersetzung geprüft; die beiden Steuerelemente sind neu):*
  - `btnAndereZeit.Text`: `"Andere Zeit buchen"`
  - `btnAndereZeit.OnSelect` (übernimmt den „frei“-Zweig aus `btnHitArea.OnSelect` in der Fassung nach L13, nur mit `varDetailsTisch` statt `ThisItem`; beide sind Datensätze aus `Tische`, also kein Typkonflikt):
```
Set(varSelectedTisch; varDetailsTisch);;
Reset(dpDatum);;
Reset(ddStart);;
Reset(ddEnde);;
Reset(dpWiederholenBis);;
Set(varZeigeDialog; true);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false)
```
  - `lblBelegtHeute.Text`:
```
With(
  { belegt: SortByColumns(Filter(colGrundriss; TischName = varSelectedTisch.Titel && Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)); "Startzeit"; SortOrder.Ascending) };
  If(IsEmpty(belegt); "An diesem Tag noch frei."; "Belegt: " & Concat(belegt; Text(Startzeit; "hh:mm") & "–" & Text(Endzeit; "hh:mm"); ", "))
)
```
  - `lblBelegtHeute.Visible`: `varZeigeDialog && dpDatum.SelectedDate = varAnsichtsDatum`
  - *Test:* Tisch heute 08:00–10:00 belegen. Grundriss-Kachel → Popup → „Andere Zeit buchen“ → Dialog zeigt „Belegt: 08:00–10:00“. 13:00–17:00 buchen → „Gebucht: …“. Datum im Dialog ändern → die Zeile verschwindet.


**P2 Check-in mit Folge oder ohne Check-in (größter fachlicher Punkt)**
- *Problem:* Einchecken bewirkt nichts. GoBright gibt nicht eingecheckte Tische frei.
- *Entscheidung nötig:* (a) **Automatische Freigabe:** Ein Power-Automate-Flow alle 15 Minuten löscht oder kürzt Buchungen von heute, die 30 Minuten nach Beginn nicht eingecheckt sind (Spalte intern `Checkedin`!). Dazu eine Mail an den Nutzer. Der Standard-Konnektor reicht (geschlussfolgert). **Achtung:** Der Flow sieht Datum/Uhrzeit in **UTC**. Vergleiche mit `utcNow()`, nicht mit Ortszeit. (b) **Check-in abschaffen** und die Knöpfe ausblenden: ehrlicher als eine Funktion ohne Wirkung.
- *Risiko (a):* Leute verlieren ihren Tisch, wenn sie den Check-in vergessen. Das braucht Kommunikation und wahrscheinlich die Zustimmung des Betriebsrats.
- *Aufwand:* (a) ~½ Tag, (b) 10 Min.

**P3 Automatisch aktualisieren und Tageswechsel (F-L7, F-L10)**
- *Problem (belegt):* Die App hat **keinen Timer**. Der Grundriss lädt nur bei einer Aktion neu, und `Now()` in den Kachelformeln wird nur dann neu berechnet. Bleibt die App offen, bleibt eine Kachel orange, obwohl die Buchung längst vorbei ist, und fremde neue Buchungen erscheinen nicht. Über Mitternacht bleibt `varAnsichtsDatum` auf gestern. GoBright aktualisiert live.
- *Lösung:* Josias fügt einen **Timer** `tmrAktualisieren` ein (irgendwo auf `Screen1`, `Visible = false`) mit `Duration = 300000` (5 Min), `Repeat = true`, `AutoStart = true` und `OnTimerEnd`:
```
If(
  !varIsLoading;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; neu)))
)
```
  **Ergänzung nach Prüfung:** Damit auch die Listen im Dashboard und im Tab aktuell werden (sie lesen direkt aus SharePoint), als erste Anweisung im inneren Teil zusätzlich `Refresh(Tischbuchungen);;` einfügen. Das kostet pro Nutzer etwa 25 Abfragen alle 5 Minuten. Das ist vertretbar, aber spürbar mehr. Ohne diese Zeile wird nur der Grundriss aktuell.
  Das ist die L2-Ladezeile, nur ohne Warnmeldung (alle 5 Minuten eine gelbe Meldung bei kurzem Netzausfall wäre lästig), plus der Tageswechsel. Kosten: **eine** delegierte Abfrage pro Nutzer alle 5 Minuten, bei 30 Nutzern 6 Abfragen pro Minute, weit unter dem Limit (geschlussfolgert).
- *Nebenwirkung:* Wer bewusst einen **vergangenen** Tag ansieht, wird nach spätestens 5 Minuten auf heute zurückgesetzt (selten, akzeptabel).
- *Aufwand:* 10 Min. *Risiko:* niedrig. (Formel aus dem Export erzeugt, Klammern und Rückübersetzung geprüft. Der Timer-Name ist neu.)

**P4 Tisch sperren (Admin)**
- *Lösung:* In der Liste `Tische` eine Ja/Nein-Spalte **„Gesperrt“** anlegen. `Gallery1` zeigt gesperrte Tische grau und ohne Klick. Panel-Liste (C1) und Speichern filtern sie heraus. Gesperrt wird direkt in der SharePoint-Liste, nur Admins haben dort Schreibrechte auf `Tische`.
- *Aufwand:* ~1 Std.
- *Hinweis:* Das ist auch die saubere Lösung für den Big Table („gesperrt für Einzelbuchung“) statt der Namensprüfung.

**P5 Buchung im Outlook-Kalender** (nach Prüfung überarbeitet)
- *Problem mit der ersten Fassung (Prüfbefund):* Der SharePoint-Trigger „Element gelöscht“ liefert keine Spaltenwerte. `SerienID` gilt für eine ganze Serie, nicht für einen Termin. Außerdem würde der Aufräum-Flow sonst Kalendereinträge vergangener Buchungen mitlöschen.
- *Lösung:* Ein Flow „Wenn Element erstellt“ schickt mit dem Office-365-Outlook-Konnektor (Standard) eine **Einladung** aus einem Funktionspostfach an die Person (kein Schreibrecht auf fremde Kalender nötig). Die Ereignis-ID kommt in eine neue Spalte **`KalenderID`** der Buchung. Beim Stornieren ruft die App einen zweiten Flow mit dem Trigger „Power Apps (V2)“ auf und übergibt die `KalenderID`. Der Flow sagt die Einladung ab. Der Aufräum-Flow fasst Kalender **nicht** an.
- *Risiko:* mittel. Funktionspostfach und Besitzer der Flows mit Michael klären.
- *Aufwand:* 1–2 Tage.

**P6 Bestätigung vor dem Stornieren (Handy V8)**
- *Lösung:* Ein Container `conStornoFrage` mit „Wirklich stornieren?“, „Ja“ und „Nein“. Die drei Storno-Knöpfe setzen nur `varZeigeStornoFrage`, und „Ja“ führt die Storno-Formel aus Paket K v2 aus (mit einer Variablen, die sagt, welcher Dialog gefragt hat).
- *Aufwand:* 1 Std.

**P7 Grundriss-Koordinaten aus der Liste statt fest im Code**
- *Problem:* 34 Positionen stehen in `App.OnStart` (`colTischPositionen`, `…UG`). Die Spalten `X`/`Y` in `Tische` sind leer bzw. ungenutzt (belegt).
- *Lösung:* Positionen und Ausrichtung in die Liste übertragen und `Gallery1` direkt daraus lesen. Ein neuer Tisch braucht dann keinen Code mehr.
- *Risiko:* mittel, weil die Positionen von dir final bestätigt sind und nicht verrutschen dürfen. Deshalb nur mit einem Vorher/Nachher-Screenshot je Stockwerk.
- *Aufwand:* ½ Tag. **Nach** dem Go-Live.

**P8 Betrieb: Umgebung, Lösung, Vertretung**
- *Lösung:* Michael fragen nach (1) einer eigenen Umgebung (z. B. „Tischbuchung Prod“) und einer Lösung (Solution), damit die App nicht in „Personal Productivity“ an deinem Konto hängt, (2) einem **Mitbesitzer** der App und der Listen und (3) einer Test-Kopie der Listen.
- Zusätzlich die zwei Klone „App“ und „App – Kopie“ löschen oder eindeutig umbenennen.
- *Aufwand:* je nach IT 1–3 Tage, **wichtigster Punkt für die Zeit nach dir**.

**P9 Berechtigungen der Liste**
- *Lösung:* Prüfen, wer auf `Tischbuchungen` Schreibrechte hat. Für Power Apps sind „Bearbeiten“-Rechte nötig. Strenger geht es nur mit Flows unter einem Dienstkonto (Premium für den HTTP-Trigger aus der App? UNSICHER) oder Dataverse (Premium).
- *Einfachste Verschärfung (ohne Premium, Prüfbefund):* In den Listeneinstellungen → Erweiterte Einstellungen → **Elementbasierte Berechtigungen: „Bearbeiten: nur eigene Elemente“**. Die App bearbeitet ohnehin nur eigene Buchungen. Dann kann niemand fremde Buchungen ändern oder löschen, auch nicht am Browser vorbei. Achtung: „eigene“ heißt **„Erstellt von“**, nicht die Spalte `Person`. Das passt, weil die App unter dem Konto des Nutzers schreibt. Vorher testen, dass der Aufräum-Flow (läuft mit Besitzerrechten) weiter löscht. Ein Flow mit dem Trigger „Power Apps (V2)“ ist laut Prüfung kein Premium (geschlussfolgert).
- *Empfehlung:* Für den Start akzeptieren, aber **bewusst entscheiden und dokumentieren**. Versionsverlauf der Liste einschalten, damit Manipulationen nachvollziehbar sind.

**P10 Barrierefreiheit**
- *Problem:* 64 der 134 Einträge der App-Prüfung (belegt): 37 fehlende Beschriftungen (`AccessibleLabel`), 19 fehlende Tab-Reihenfolge, 7 unsichtbare Fokusrahmen, 1 Bildschirmname.
- *Lösung:* `AccessibleLabel` für alle Knöpfe ohne Text (Kachel-Klickfläche, Verwalten-Pfeile, Aktualisieren-Symbole) setzen und `TabIndex` vergeben.
- *Aufwand:* 1–2 Std., maschinell erzeugbar. **Nach** dem Go-Live, es sei denn, ihr habt Mitarbeitende mit Screenreader.

## 4. Stil-Audit: Was nicht einheitlich wirkt (belegt am Export)
**Farben im Einsatz** (Anzahl Vorkommen):

| Farbe | Wo | Bedeutung heute | Bewertung |
|---|---|---|---|
| `#171496` Markenblau (18×) | Tabs, Panel, Verwalten-Knöpfe | Hauptaktion | gut, aber nicht überall |
| `RGBA(100,118,132)` Graublau (36×) | Buchungsdialog (Pfeile, Kalender, Schalter), alle Auswahl-Markierungen in Listen, Auswahlmodus | **Power-Apps-Standarddesign**, übrig geblieben | **uneinheitlich**: zwei „Hauptfarben“ |
| `RGBA(32,54,71)` Dunkelblau-Grau (132×) | Texte, Rahmen | Schrift | ok |
| `#00A96B`/`#00a96b` Grün (44×) | frei, Erfolg, ausgewählte Dauer, Speichern im Dialog, Schalter im Panel, eingecheckt im Dashboard | **fünf Bedeutungen** | überladen |
| `#4DC398` helles Grün (1×) | Kreis einer freien Kachel | frei | ok |
| `#EB3951` Rot (38×) | belegt/eingecheckt im Grundriss, gesperrte Dauer-Knöpfe, „Besetzt“, Auschecken | „nicht möglich“ und „eingecheckt“ zugleich | widersprüchlich (BD-14) |
| `#FFA500` Orange (10×) | gebucht, nicht eingecheckt | | ok |
| Grautöne: `#F7F7F7`, `#F0F0F0`, `#D0D0D0`, `RGBA(241…)`, `RGBA(234…)`, `RGBA(233…)`, `RGBA(220…)`, `RGBA(205…)`, `RGBA(166…)`, `RGBA(120…)` | Hintergründe, Trennlinien, „Tisch Buchen“-Knopf | | **zehn Grautöne**, drei würden reichen |

**Knöpfe** (44):
- **Hauptaktion:** Blau mit Hover −20 % (9×; `btnAbbrechenTischePanel` „<“ ist ebenfalls blau, nicht schwarz). Im Buchungsdialog aber grün (`btnSpeichern`), im Raum-Panel mit graublauem Hover (toter Code).
- **Schließen/Abbrechen:** schwarz mit Hover **heller** (+30 %), während blaue Knöpfe beim Hover **dunkler** werden. Vier Beschriftungen: „Schließen“, „Abbrechen“, „x“, „<“.
- **Gedrückt:** drei verschiedene Muster. Blau wird invertiert (weißer Grund, blaue Schrift). Schwarz und grün werden unlesbar (F-L3). Ohne Angabe gilt der Standard. → L3 vereinheitlicht die kaputten.
- **Gesperrt:** rot verblasst 70 % (11×) bzw. 85 % (4×, nur toter Raumcode). Sonst grau (Standard).
- **Schriftgrößen:** Standard bei 38 Knöpfen, dazu 10, 11, 14, 25. „Tisch Buchen“ ist mit 11 kleiner als alles andere.
- **Stornieren** sieht aus wie Speichern (blau). Im Tab-Dialog stehen beide nebeneinander → Fehlklick-Gefahr. → L8 (rot).
- **Dauer-Knöpfe:** „+1Std“, „-2std“, „5 Std“ → L9.

**Eingabefelder:**
- Auswahllisten im Panel: blauer Pfeil, Hover −20 %. Im Buchungsdialog: graublauer Pfeil, Hover hellgrau. Stockwerk: kein Rahmen, eigener Hover. → L7 gleicht den Dialog an.
- Kalender: Panel blau, Dialog graublau, Dashboard ohne Symbol. → L7.
- Wochentag-Schalter: Panel grün, Dialog graublau → L7.

**Texte und Titel** (L9 deckt die meisten ab):
- Englisch: „My personal desk“, „My meetings“ (ausgeblendet), „Dashboard“ (kann bleiben, ist gängig).
- Titel in vier Formen: „Check-in: X“, „Tisch: X“, „Tisch X“, „Verwalten: Tisch X“, plus „Tisch “ vor einem Namen, der schon „OG Desk 5“ heißt („Tisch OG Desk 5“).
- Leere Listen: „---“ und „-Keine Einträge-“.
- „Tisch Buchen“ und „Raum Buchen“ mit großem B.
- Adresse „Matthäus-Merian-Strasse“ (ss) steht dreimal hart im Code.

**Vollständige Prüfung aller Zustände (Hover, Gedrückt, Auswahl, Gesperrt) über alle Steuerelement-Typen** (Tabelle im Anhang B, maschinell aus dem Export):

| Bereich | Befund (belegt) | Paket L |
|---|---|---|
| Auswahllisten: Pfeil-Hover | `ChevronHoverBackground` ist bei **allen 7** sichtbaren Listen graublau, auch wo der Pfeil blau ist. Beim Hover springt ein blauer Pfeil auf Graublau | L10 |
| Auswahllisten: markierte Zeile | `SelectionFill` ist bei allen 8 graublau | L10 (6 Listen, Raumcode ausgenommen) |
| Auswahllisten: Hover | Panel `ColorFade(Self.Fill; −20 %)`, Dialog hellgrau `RGBA(205,209,213)`, Stockwerk blau 8 % | durch L7 (Dialog wie Panel) teilweise |
| Listen-Auswahlbalken | Dashboard blau `#171496`, Buchungen-Tab graublau | L10 |
| Akzentbalken in Dialogen | `Rectangle5`, `Rectangle6`, `Rectangle6_1`, `Rectangle6_2` graublau | L10 |
| Unsichtbare Klickflächen (Kachel, Einchecken, Verwalten, Logo) | **fünf** verschiedene Hover-Stärken: 4 %, 8 %, 15 %, 20 %, 20 % | L11 (einheitlich 10 %) |
| Dialog-Hintergründe | Popups weiß, aber Tab-Verwalten und Mehrfach-Dialog grau `RGBA(234,234,236)` | L12 |
| Knöpfe gedrückt | siehe oben, 7 unlesbar | L3 |
| Knöpfe Hover | dunkel → heller (+30 %), blau → dunkler (−20 %), Dauer-Knöpfe −15 % | **nicht** in L. Gewollt kann „dunkle Knöpfe werden heller“ sein, es wirkt aber uneinheitlich. Vorschlag für später: überall `ColorFade(Self.Fill; −15 %)`, schwarze Knöpfe durch Dunkelgrau ersetzen |
| Gesperrte Knöpfe | Dauer-Knöpfe rot verblasst (`DisabledFill`), Speichern/Stornieren grau (Standard). Nach Paket K sind gesperrte Speichern-Knöpfe grau | bewusst so: rot = „geht nicht wegen Belegung“, grau = „gerade nicht bedienbar“ |
| Schalter (Toggle) | `TrueFill` 6× graublau, 5× grün, `FalseFill` überall Standard | L7 (Wochentage grün, Auswahlmodus blau) |
| Kontrollkästchen | alle 4 gleich (belegt) | ok |
| Kalender | Symbolhintergrund blau, graublau, transparent, hellgrau (Raum) | L7 |
| Symbole (Aktualisieren) | dunkel, ohne eigene Hover-Farbe | ok, siehe „Drei Stellen zum Aktualisieren“ |
| Schriftfarben | vier Dunkeltöne: `RGBA(32,54,71)` (Standard, 132×), `RGBA(50,49,48)` (4×), Schwarz, Grau `RGBA(120,120,120)` | später mit der Farbtabelle |
| Bilder | Bearbeiten-Symbol in beiden Listen mit Hover, Tisch-Symbole ohne (richtig, sie sind nicht klickbar) | ok |
| **Logo als Knopf** | Das **Technoform-Logo** in der Kopfzeile (`Image6`) ist der Aktualisieren-Knopf (belegt). Das errät niemand | Vorschlag: eigenes Aktualisieren-Symbol in die Kopfzeile, das Logo nur als Logo |
| Kalender-Trick im Dashboard | `dpAnsichtsDatum` hat transparenten Text und Rahmen und liegt über „Heute“/Datum (gewollt) | ok, aber ohne `AccessibleLabel` für Screenreader unsichtbar (P10) |

**Sonstiges:**
- **Drei Stellen zum Aktualisieren** (Symbol im Dashboard, Symbol im Buchungen-Tab, Symbol in der Kopfzeile mit eigener Klickfläche `btnHitArea_1`), alle mit derselben Formel (belegt). Eine in der Kopfzeile reicht. Mit dem Timer aus P3 braucht man sie fast nie.
- Die **Handy-App** nutzt schon das Markenblau `RGBA(23, 20, 150)` = `#171496` (belegt). L7 zieht die Desktop-App in dieselbe Richtung, damit beide Apps gleich aussehen.

**Bewusst nicht in Paket L (deine Entscheidung):**
- Farbe für **eingecheckt** (BD-14).
- Grautöne zusammenfassen: viele Properties, nur Optik, später in einem Zug.
- Schriftgrößen-Raster.
- Eine **Farbtabelle in `App.Formulas`** (`FarbeHaupt = ColorValue("#171496");` usw.), auf die alle Properties verweisen. Das ist der saubere Weg, aber er berührt über 200 Properties. Lohnt sich erst, wenn die App länger lebt.

## 5. Weitere Verbesserungsvorschläge (Einschätzung, nach Nutzen sortiert)
1. **Kurzanleitung** (1 Seite) und ein Teams-Kanal für Rückmeldungen zum Go-Live: größter Nutzen pro Minute.
2. **P2 entscheiden** (Check-in mit Folge oder weg).
3. **P1** (Restzeit im Grundriss buchen): vermeidet die häufigste Verwirrung nach der Tischliste.
4. **„Heute“-Knopf** neben dem Datum im Dashboard (zurück zum heutigen Tag mit einem Klick).
5. **„Wer sitzt wo“ ohne Namen** als Option, falls der Datenschutz Namen ablehnt: nur Farbe, keine Initialen, kein Name im Popup.
6. **Serie direkt im Buchungs-Tab sichtbar machen:** Termine mit derselben `SerienID` zusammen anzeigen und gemeinsam stornieren. Das geht erst, wenn Paket K die `SerienID` schreibt.
7. **Kennzahlen für die Geschäftsleitung** (Auslastung pro Woche) über einen Flow, der jede Nacht vor dem Löschen zählt. Der Aufräum-Flow löscht heute alles nach 7 Tagen, damit ist **jede Auswertung unmöglich**. Wenn Auslastung je gefragt ist: vorher zählen oder archivieren.
8. **Fehlermeldungen protokollieren:** `Trace()` an den `IfError`-Stellen, damit du im Livemonitor oder in App Insights siehst, was bei Nutzern schiefgeht, statt auf Screenshots zu warten.
9. **Raumcode löschen** (L4, BD-22): 21 Steuerelemente, 36 Abfragen beim Start und Verwechslungsgefahr beim Lesen.
10. **Handy-App** vor oder mit dem Go-Live teilen (sie ist im Test sauberer als die Desktop-App).

## Anhang: Originale (Rückfall)

**`ddStart.Items`**

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatum.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30; 0) + 1; 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`ddStartTischePanel.Items`**

```
With(
  { minutenJetzt: Hour(Now())*60 + Minute(Now()) };
  With(
    {
      minutenStart:
        If(
          dpDatumTischePanel.SelectedDate = Today();
          30 * RoundUp(minutenJetzt / 30; 0);
          8 * 60
        );
      minutenEnde: 22 * 60
    };
    ForAll(
      Sequence(RoundDown((minutenEnde - minutenStart) / 30; 0) + 1; 0);
      With(
        { m: minutenStart + Value * 30 };
        { Value: Text(Time(RoundDown(m / 60; 0); Mod(m; 60); 0); "hh:mm") }
      )
    )
  )
)
```

**`galTischbuchungenHeute.Items`**

```
Filter(
  Tischbuchungen;
  Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
)
```

**`conCheckinDialog.Y`**

```
With(
        { _idx: CountRows(Filter(galTischbuchungenHeute.AllItems; ID < varSelectedBuchung.ID)) + 1 };
            conDashboard.Y + galTischbuchungenHeute.Y + (_idx - galTischbuchungenHeute.VisibleIndex) * galTischbuchungenHeute.TemplateHeight + (galTischbuchungenHeute.TemplateHeight - Self.Height) / 2
            )
```

**`btnAbbrechen.PressedColor`**

```
Self.Fill
```

**`btnAbbrechen.PressedFill`**

```
Color.Black
```

**`btnSchließen2.PressedColor`**

```
Self.Fill
```

**`btnSchließen2.PressedFill`**

```
Color.Black
```

**`btnSchließen3.PressedColor`**

```
Self.Fill
```

**`btnSchließen3.PressedFill`**

```
Color.Black
```

**`btnSchließen4.PressedColor`**

```
Color.Black
```

**`btnSchließen4.PressedFill`**

```
Color.Black
```

**`btnSchließen4_1.PressedColor`**

```
Color.Black
```

**`btnSchließen4_1.PressedFill`**

```
Color.Black
```

**`btnSchließenKlein.PressedColor`**

```
Color.Black
```

**`btnSchließenKlein.PressedFill`**

```
Color.Black
```

**`btnSpeichern.PressedColor`**

```
Self.Fill
```

**`btnTabDashboard.Fill`**

```
ColorValue("#171496")
```

**`btnTabBuchungen.Fill`**

```
ColorValue("#171496")
```

**`Circle2.Fill`**

```
varProfilFarbe
```

**`lblStatus.Text`**

```
"Besetzt"
```

**`lblStatus.Color`**

```
ColorValue("#EB3951")
```

**`tglTagMo.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`tglTagDi.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`tglTagMi.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`tglTagDo.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`tglTagFr.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`dpDatum.IconBackground`**

```
RGBA(100; 118; 132; 1)
```

**`dpWiederholenBis.IconBackground`**

```
RGBA(100; 118; 132; 1)
```

**`ddStart.ChevronBackground`**

```
RGBA(100; 118; 132; 1)
```

**`ddStart.HoverFill`**

```
RGBA(205; 209; 213; 1)
```

**`ddEnde.ChevronBackground`**

```
RGBA(100; 118; 132; 1)
```

**`ddEnde.HoverFill`**

```
RGBA(205; 209; 213; 1)
```

**`btnSpeichern.Fill`**

```
ColorValue("#00A96B")
```

**`btnSpeichern.PressedFill`**

```
ColorValue("#00a96b")
```

**`tglAuswahlModus.TrueFill`**

```
RGBA(100; 118; 132; 1)
```

**`btnStornieren.Fill`**

```
ColorValue("#171496")
```

**`btnStornieren_1.Fill`**

```
ColorValue("#171496")
```

**`btnStornierenKlein.Fill`**

```
ColorValue("#171496")
```

**`lblMyPersonalDesk.Text`**

```
"My personal desk"
```

**`btnTischHinzufügen.Text`**

```
"Tisch Buchen"
```

**`lblTischeBuchenPanel.Text`**

```
"Tisch Buchen"
```

**`btnPlus1Std.Text`**

```
"+1Std"
```

**`btnPlus2Std.Text`**

```
"+2Std"
```

**`btnPlus3Std.Text`**

```
"+3Std"
```

**`btnPlus1Std_1.Text`**

```
"+1Std"
```

**`btnPlus2Std_1.Text`**

```
"+2Std"
```

**`btnPlus3Std_1.Text`**

```
"+3Std"
```

**`btnMinus1Std.Text`**

```
"-1Std"
```

**`btnMinus2Std.Text`**

```
"-2std"
```

**`btnMinus3std.Text`**

```
"-3Std"
```

**`lblTischLeer.Text`**

```
"---"
```

**`lblTischLeer_1.Text`**

```
"-Keine Einträge-"
```

**`lblTitel3.Text`**

```
If(IsBlank(varSelectedBuchung); ""; "Tisch " & varSelectedBuchung.Tisch.Value)
```

**`lblTitel3_1.Text`**

```
"Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel2.Text`**

```
"Tisch: " & varSelectedBuchung.Tisch.Value
```

**`lblTischHeute.Text`**

```
"Tisch " & ThisItem.Tisch.Value
```

**`Rectangle3_2.Fill`**

```
RGBA(100; 118; 132; 1)
```

**`Rectangle5.Fill`**

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6.Fill`**

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6_1.Fill`**

```
RGBA(100; 118; 132; 1)
```

**`Rectangle6_2.Fill`**

```
RGBA(100; 118; 132; 1)
```

**`ddStockwerk.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddTischePanel.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddStartTischePanel.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddEndTischePanel.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddStart.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddEnde.SelectionFill`**

```
RGBA(100; 118; 132; 1)
```

**`ddTischePanel.ChevronHoverBackground`**

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddStartTischePanel.ChevronHoverBackground`**

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddEndTischePanel.ChevronHoverBackground`**

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddStart.ChevronHoverBackground`**

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`ddEnde.ChevronHoverBackground`**

```
ColorFade(RGBA(100; 118; 132; 1); -20%)
```

**`btnHitArea.HoverFill`**

```
RGBA(0; 0; 0; 0,15)
```

**`btnEincheckenHeute.HoverFill`**

```
RGBA(0; 0; 0; 0,04)
```

**`btnVerwalten.HoverFill`**

```
RGBA(0; 0; 0; 0,2)
```

**`btnVerwalten_2.HoverFill`**

```
RGBA(0; 0; 0; 0,2)
```

**`btnHitArea_1.HoverFill`**

```
RGBA(0; 0; 0; 0,08)
```

**`conVerwaltenDialog_1.Fill`**

```
RGBA(234; 234; 236; 1)
```

**`conVerwaltenKlein.Fill`**

```
RGBA(234; 234; 236; 1)
```

**`btnHitArea.OnSelect`**

```
With(
  {
    relevanteBuchung:
      If(
        varAnsichtsDatum = Today();
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
        LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
      )
  };
  If(
    IsBlank(relevanteBuchung);
      Set(varSelectedTisch; ThisItem);;
      Set(varZeigeDialog; true);;
      Set(varZeigeDetails; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false);;
      Set(varWiederholen; false);;
      Set(varWiederholenModus; "Wochentage");;
      Set(varTagMo; false);;
      Set(varTagDi; false);;
      Set(varTagMi; false);;
      Set(varTagDo; false);;
      Set(varTagFr; false);;
      Set(varTagSa; false);;
      Set(varTagSo; false);
      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; relevanteBuchung);;
      Set(varZeigeDetails; true);;
      Set(varZeigeDialog; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false)
  )
)
```

**`btnTischHinzufügen.OnSelect`**

```
Set(varZeigeTischBuchungForm; true);;
Reset(dpDatumTischePanel);;
Reset(ddTischePanel);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Reset(tglTagMo_1);;
Reset(tglTagDi_1);;
Reset(tglTagMi_1);;
Reset(tglTagDo_1);;
Reset(tglTagFr_1);;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "")
```

## Anhang B: Zustände aller bedienbaren Steuerelemente (Export 07.10., vor Paket K/L)

`·` = Standardwert. Erzeugt aus dem Export, nicht von Hand.

| Steuerelement | Typ | Ort | Fill | HoverFill | PressedFill | Color | HoverColor | PressedColor | DisabledFill | SelectionFill | ChevronBackground | ChevronHoverBackground | TrueFill | IconBackground | BorderColor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `btnHitArea` | Button | Gallery1 | `Color.Transparent` | `RGBA(0; 0; 0; 0,15)` | `ColorFade(Rectangle1.Fill; -30%)` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `ddStockwerk` | DropDown | conGrundriss | `RGBA(0; 0; 0; 0)` | `RGBA(23; 20; 150; 0,08)` | `RGBA(32; 54; 71; 1)` | `Color.Black` | `Color.Black` | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `RGBA(0; 0; 0; 0)` | `RGBA(0; 0; 0; 0)` | · | · | `RGBA(0; 0; 0; 0)` |
| `Image1_1` | Image | galTischbuchungenHeute | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `Image3` | Image | galTischbuchungenHeute | · | `ColorFade(Self.Fill; -20%)` | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnEincheckenHeute` | Button | galTischbuchungenHeute | `Color.Transparent` | `RGBA(0; 0; 0; 0,04)` | `RGBA(0; 0; 0; 0,1)` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnVerwalten` | Button | galTischbuchungenHeute | `Color.Transparent` | `RGBA(0; 0; 0; 0,2)` | `ColorFade(Self.Fill; -20%)` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `Image1_2` | Image | galRaumbuchungenHeute | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `Image3_1` | Image | galRaumbuchungenHeute | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnInfoRaum` | Button | galRaumbuchungenHeute | `Color.Transparent` | `RGBA(0; 0; 0; 0,04)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnVerwalten_1` | Button | galRaumbuchungenHeute | `Color.Transparent` | `RGBA(0; 0; 0; 0,2)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnRaumHinzufügen` | Button | conDashboard | `ColorValue("#D0D0D0")` | `RGBA(0; 0; 0; 0,2)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnTischHinzufügen` | Button | conDashboard | `ColorValue("#D0D0D0")` | `RGBA(0; 0; 0; 0,2)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `dpAnsichtsDatum` | DatePicker | conDashboard | `Color.Transparent` | · | · | `Color.Transparent` | · | · | · | · | · | · | · | `Color.Transparent` | `Color.Transparent` |
| `Icon1_1` | Icon | conDashboard | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `ddTischePanel` | DropDown | conTischBuchungenPanel | · | `ColorFade(Self.Fill; -20%)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `ColorValue("#171496")` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `ddStartTischePanel` | DropDown | conTischBuchungenPanel | · | `ColorFade(Self.Fill; -20%)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `ColorValue("#171496")` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `dpDatumTischePanel` | DatePicker | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | · | `ColorValue("#171496")` | `RGBA(32; 54; 71; 1)` |
| `ddEndTischePanel` | DropDown | conTischBuchungenPanel | · | `ColorFade(Self.Fill; -20%)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `ColorValue("#171496")` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `btnSpeichernTischePanel` | Button | conTischBuchungenPanel | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnAbbrechenTischePanel` | Button | conTischBuchungenPanel | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `tglTagMo_1` | Toggle | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | `ColorValue("#00a96b")` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagDi_1` | Toggle | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | `ColorValue("#00a96b")` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagMi_1` | Toggle | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | `ColorValue("#00a96b")` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagDo_1` | Toggle | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | `ColorValue("#00a96b")` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagFr_1` | Toggle | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | `ColorValue("#00a96b")` | · | `RGBA(32; 54; 71; 1)` |
| `chkWiederholenPanel` | CheckBox | conTischBuchungenPanel | · | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `dpWiederholenBis_1` | DatePicker | conTischBuchungenPanel | · | · | · | · | · | · | · | · | · | · | · | `ColorValue("#171496")` | `RGBA(32; 54; 71; 1)` |
| `btn5Std` | Button | conTischBuchungenPanel | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btn9Std` | Button | conTischBuchungenPanel | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `dpDatumRaum` | DatePicker | conRaumBuchungenPanel | `RGBA(241; 241; 241; 1)` | · | · | · | · | · | · | · | · | · | · | `RGBA(220; 220; 220; 1)` | `RGBA(32; 54; 71; 1)` |
| `ddDauerRaumPanel` | DropDown | conRaumBuchungenPanel | `RGBA(241; 241; 241; 1)` | `RGBA(205; 209; 213; 1)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `RGBA(100; 118; 132; 1)` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `ddBeginnRaumPanel` | DropDown | conRaumBuchungenPanel | `RGBA(241; 241; 241; 1)` | `RGBA(205; 209; 213; 1)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `RGBA(100; 118; 132; 1)` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `btnAbbrechenRaumPanel` | Button | conRaumBuchungenPanel | `RGBA(241; 241; 241; 1)` | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `Image1` | Image | galRäume | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `NextArrow1` | Icon | galRäume | · | · | · | `RGBA(166; 166; 166; 1)` | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnSlot1` | Button | galRäume | (Formel) | (Formel) | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 85%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSlot2` | Button | galRäume | (Formel) | (Formel) | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 85%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSlot3` | Button | galRäume | (Formel) | (Formel) | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 85%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSlot4` | Button | galRäume | (Formel) | (Formel) | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 85%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSpeichernRaumPanel` | Button | conRaumBestätigen | `ColorValue("#171496")` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `Button7` | Button | conRaumBestätigen | `Color.Black` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `ddStart` | DropDown | conBuchungDialog | · | `RGBA(205; 209; 213; 1)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `RGBA(100; 118; 132; 1)` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `ddEnde` | DropDown | conBuchungDialog | · | `RGBA(205; 209; 213; 1)` | `RGBA(32; 54; 71; 1)` | · | · | `RGBA(255; 255; 255; 1)` | · | `RGBA(100; 118; 132; 1)` | `RGBA(100; 118; 132; 1)` | `ColorFade(RGBA(100; 118; 132; 1); -20%)` | · | · | `RGBA(32; 54; 71; 1)` |
| `btnSpeichern` | Button | conBuchungDialog | `ColorValue("#00A96B")` | `ColorFade(Self.Fill; -20%)` | `ColorValue("#00a96b")` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnAbbrechen` | Button | conBuchungDialog | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `dpDatum` | DatePicker | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | `RGBA(32; 54; 71; 1)` |
| `chkWiederholen` | CheckBox | conBuchungDialog | · | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `tglTagMo` | Toggle | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagDi` | Toggle | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagMi` | Toggle | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagDo` | Toggle | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `tglTagFr` | Toggle | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `dpWiederholenBis` | DatePicker | conBuchungDialog | · | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | `RGBA(32; 54; 71; 1)` |
| `btnEinchecken` | Button | conCheckinDialog | (Formel) | `ColorFade(Self.Fill; -30%)` | `Self.Color` | `Color.White` | `RGBA(255; 255; 255; 1)` | (Formel) | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSchließen2` | Button | conCheckinDialog | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSchließen3` | Button | conDetailsPopup | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnStornieren` | Button | conVerwaltenDialog | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnVerlängern` | Button | conVerwaltenDialog | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSchließen4` | Button | conVerwaltenDialog | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Color.Black` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus1Std` | Button | conVerwaltenDialog | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus2Std` | Button | conVerwaltenDialog | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus3Std` | Button | conVerwaltenDialog | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `Image1_3` | Image | galAlleTischbuchungen | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `Image3_2` | Image | galAlleTischbuchungen | · | `ColorFade(Self.Fill; -20%)` | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnVerwalten_2` | Button | galAlleTischbuchungen | `Color.Transparent` | `RGBA(0; 0; 0; 0,2)` | `ColorFade(Self.Fill; -20%)` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `chkAuswahl` | CheckBox | galAlleTischbuchungen | · | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnStornieren_1` | Button | conVerwaltenDialog_1 | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnVerlängern_1` | Button | conVerwaltenDialog_1 | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSchließen4_1` | Button | conVerwaltenDialog_1 | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Color.Black` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus1Std_1` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus2Std_1` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnPlus3Std_1` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnMinus1Std` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnMinus2Std` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnMinus3std` | Button | conVerwaltenDialog_1 | (Formel) | `ColorFade(Self.Fill; -15%)` | `Self.Color` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | `ColorFade(ColorValue("#EB3951"); 70%)` | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnStornierenKlein` | Button | conVerwaltenKlein | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnSchließenKlein` | Button | conVerwaltenKlein | `Color.Black` | `ColorFade(Self.Fill; 30%)` | `Color.Black` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Color.Black` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `tglAuswahlModus` | Toggle | conBuchungen | · | · | · | · | · | · | · | · | · | · | `RGBA(100; 118; 132; 1)` | · | `RGBA(32; 54; 71; 1)` |
| `chkAlleAuswählen` | CheckBox | conBuchungen | · | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `Icon1` | Icon | conBuchungen | · | · | · | `RGBA(32; 54; 71; 1)` | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `Image6` | Image | conHeader | · | · | · | · | · | · | · | · | · | · | · | · | `RGBA(32; 54; 71; 1)` |
| `btnTabDashboard` | Button | conHeader | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnTabBuchungen` | Button | conHeader | `ColorValue("#171496")` | `ColorFade(Self.Fill; -20%)` | `` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |
| `btnHitArea_1` | Button | conHeader | `Color.Transparent` | `RGBA(0; 0; 0; 0,08)` | `ColorFade(Image6.Fill; -30%)` | `RGBA(255; 255; 255; 1)` | `RGBA(255; 255; 255; 1)` | `Self.Fill` | · | · | · | · | · | · | `ColorFade(Self.Fill; -15%)` |