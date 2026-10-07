# ÜBERGABE Tischbuchung: Paket K (Korrekturen zum Go-Live)
**v1 · 07.10.2026 · Basis: veröffentlichter Export „Tischbuchung App 07.10.2026 verbesserung analyse“ (erstellt 2026-10-07T09:14:57.2164854Z, enthält L2) · alle Formeln maschinell aus diesem Export erzeugt und geprüft (Anhang 2) · noch nichts davon eingefügt**

## 0. Kurzfassung
- **Teil A (klein, empfohlen vor dem Go-Live):** K1 stille Doppelbuchung im Tab + Doppelklick-Sperre beim Speichern. 1 Formel ersetzen, 2 Properties setzen. Ca. 10 Minuten.
- **Teil B (empfohlen, wenn A ok):** Verlängern prüft vor dem Schreiben am Server (Kollision, 22:00, gelöschte Buchung), meldet ehrlich, Doppelklick-Sperre. 2 Formeln ersetzen, 2 Properties setzen.
- **Teil C (optional, auch nach dem Go-Live):** Speichern lädt weniger Daten, Serienmeldungen nennen alles in einer Meldung, Panel erkennt Schreibfehler. 2 Formeln ersetzen.
- **Teil E (nur bei Bedarf):** Mehrfachauswahl ausblenden.
- Alles, was nicht in A–C/E steht, ist bewusst **nach** dem Go-Live (Abschnitt 9).

Ablauf je Schritt wie bei L2: Steuerelement.Property öffnen → **ganze Property ersetzen** → App-Prüfung → kurzer Test → Ergebnis melden. Jeder Block ist vollständig, deutsche Schreibweise, ohne Kommentare.

**Voraussetzung:** Seit dem Export (07.10.) wurde in Studio nichts mehr gespeichert. Sonst neuen Export erstellen, entpacken und `exportiere_props.ps1` + `erzeuge_konzept.ps1` neu laufen lassen (die Skripte brechen ab, wenn ein Anker nicht mehr genau passt). Vorher `.msapp` exportieren.

## 1. Übersicht
| Schritt | Steuerelement.Property | Was | Behebt | Impact | Risiko |
|---|---|---|---|---|---|
| A1 | `btnVerwalten_2.OnSelect` | +1 Zeile `Set(varSelectedBuchung; ThisItem)` | B0 stille Doppelbuchung beim Verlängern im Tab | hoch | niedrig |
| A2, A3 | `btnSpeichern.DisplayMode`, `btnSpeichernTischePanel.DisplayMode` | neu: gesperrt während `varIsLoading` | Doppelklick = doppelte Buchung | mittel | niedrig |
| B1 | `btnVerlängern_1.OnSelect` | neu: prüft am Server, meldet ehrlich | Kollision zwischen Anzeige und Klick, über 22:00, gelöschte Buchung, „gespeichert“ trotz Fehler | mittel–hoch | mittel |
| B2 | `btnVerlängern_1.DisplayMode` | neu: Doppelklick-Sperre | „+1 Std“ wird zu „+2 Std“ | mittel | niedrig |
| B3 | `btnVerlängern.OnSelect` | wie B1 im Grundriss | wie B1 | mittel–hoch | mittel |
| B4 | `btnVerlängern.DisplayMode` | wie B2 im Grundriss | wie B2 | mittel | niedrig |
| C1 | `btnSpeichern.OnSelect` | Zeitfenster in Kollisionsabfrage (K4.1) + eine Meldung mit Anzahl, Kollision, Kappung | B3 Kappungsmeldung verdrängt Kollisionsmeldung; weniger Daten | niedrig–mittel | niedrig |
| C2 | `btnSpeichernTischePanel.OnSelect` | K4.1 + `IfError` je Termin + Meldung wie C1 | B2 Fehler wird als „gespeichert“ gezählt | niedrig–mittel | niedrig |
| E2 | `tglAuswahlModus.Visible` | `false` (nur falls gewünscht) | Mehrfachauswahl zum Go-Live aus | – | niedrig |

Herkunft: K1–K5 stammen aus `ENTWURF_SPEICHERN.md` (Claude Code, vor L2). Hier sind sie an den **heutigen** Stand angepasst: L2-Ladezeile bleibt überall erhalten, `btnSpeichern` hat inzwischen den Sammel-Patch (deshalb C1 neu geschrieben), die Verlängern-Prüfung ist delegierbar und wortgleich mit der der Plus-Knöpfe.

**Bewusst verworfen: K4.2 (`<>` → `>` beim Serien-Enddatum).** Geprüft am Export: Wer „Wiederholen“ anhakt und das Bis-Datum vergisst (Standard = heute), bekommt heute „… Bitte Enddatum anpassen“. Mit K4.2 bekäme er still nur **eine** Buchung, obwohl er eine Serie wollte. Das wäre schlechter. Der Test im alten Entwurf war nicht stimmig (ohne gewählten Wochentag kommt auch danach „Bitte mindestens einen Wochentag auswählen“).

## 2. Entscheidungen (Vorschlag, du bestätigst)
- **E1 22:00-Grenze beim Verlängern: ablehnen** (Meldung, nichts ändern). Begründung: Das Tische-Panel behandelt 22:00 schon als Tagesende (`btn5Std`, `btn9Std`), die Handy-App erlaubt Verlängern bis 22:00. Verkürzen ist immer erlaubt, auch bei alten Buchungen über 22:00. Wenn du **keine** Grenze willst: B1/B3 nicht einfügen und Bescheid geben, dann wird die Variante ohne Grenze erzeugt.
- **E2 Mehrfachauswahl: drinlassen** (Trace mit 33 Stornierungen fehlerfrei). Nur wenn dein Zwei-Tab-Test scheitert: Schritt E2.
- **E3 Serienbuchung: drinlassen** (gemessen ~5 s statt ~101 s).

## 3. Teil A: klein, vor dem Go-Live (empfohlen)
Reihenfolge einhalten. Nach jedem Schritt: App-Prüfung (Baseline 134 Einträge, keine Formelfehler), kurz testen, Ergebnis melden.

### A1 `btnVerwalten_2.OnSelect`
**K1: Dauer-Knöpfe im Buchungen-Tab bewerten die richtige Buchung**

Eine Zeile neu. Behebt Befund B0: Die 12 Plus-/Minus-Properties lesen `varSelectedBuchung`, der Tab-Dialog setzte bisher nur `varSelectedBuchungTab`. Danach ist der Plus-Knopf nur grün, wenn **diese** Buchung verlängert werden kann.

Änderung (rot = weg, grün = neu, `...` = unverändert):
```diff
  ...
    Set(varSelectedBuchungTab; ThisItem);;
+   Set(varSelectedBuchung; ThisItem);;
    Set(varZeigeVerwaltenTab; true);;
  ...
```
**Einfügen: ganze Property `btnVerwalten_2.OnSelect` ersetzen durch**

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varSelectedBuchung; ThisItem);;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```
**Test:** Im Grundriss eine Buchung A verwalten, Dialog schließen. Im Tab „Meine Buchungen“ eine andere Buchung B verwalten: Plus-/Minus-Knöpfe passen zu B (z. B. Plus grau, wenn hinter B direkt jemand gebucht hat). Danach umgekehrt (erst Tab, dann Grundriss).

### A2 `btnSpeichern.DisplayMode` und A3 `btnSpeichernTischePanel.DisplayMode`
**K5: Doppelklick-Riegel beim Speichern**

Die Property `DisplayMode` ist bei beiden Knöpfen heute nicht gesetzt (Standard = bedienbar). Neu wird der Knopf gesperrt, solange `varIsLoading` wahr ist. Beide Knöpfe setzen `varIsLoading` schon am Anfang auf wahr und am Ende auf falsch, auf jedem Weg.

**Einfügen: bei beiden Knöpfen die Property `DisplayMode` setzen auf**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```
**Test:** Buchen und dabei zweimal schnell auf Speichern klicken → nur eine Buchung, nur eine Meldung. Danach ist der Knopf wieder bedienbar.

## 4. Teil B: Verlängern sicher machen (vor dem Go-Live, wenn Teil A ok)
Ersetzt K2/K3 aus `ENTWURF_SPEICHERN.md` (dort fehlte die L2-Ladezeile, und die Prüfung mit `ID <>` ist nicht delegierbar). Die Kollisionsprüfung ist **wortgleich** mit der, die die Plus-Knöpfe heute schon benutzen (`Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit`, delegierbar, die eigene Buchung fällt automatisch raus). Nur zweiarmige `If`, das Speichermuster `IfError(Patch(...); "fehler"; "ok")` ist aus `btnSpeichern` übernommen und dort gemessen.

Was der neue Knopf tut, in dieser Reihenfolge: Ladeanzeige an → Buchung frisch vom Server → keine Dauer gewählt? / Buchung gelöscht? / Buchung würde leer? / über 22:00? / Tisch inzwischen belegt? → jeweils Meldung, nichts schreiben → sonst speichern, bei Fehler ehrliche Meldung, bei Erfolg Meldung mit neuem Ende und Dialog schließen → immer: Liste neu laden, Grundriss neu laden, Dauer-Auswahl leeren, Ladeanzeige aus.

### B1 `btnVerlängern_1.OnSelect`
**K2 neu: Verlängern/Verkürzen im Buchungen-Tab**

Ganze Property neu (Ablauf siehe oben). Bleibt gleich: frische Buchung per `LookUp`, `varSelectedBuchungTab` wird nach dem Speichern aktualisiert, `Refresh`, L2-Ladezeile, `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)` beim Erfolg. Neu: `varIsLoading`, die Prüfungen, Erfolgs-/Fehlermeldung. Die Dauer-Auswahl wird jetzt auch nach einer Warnung geleert (man wählt neu).

Änderung (rot = weg, grün = neu, `...` = unverändert):
```diff
+ Set(varIsLoading; true);;
  With(
  ...
      Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
-     Set(varSelectedBuchungTab; Patch(Tischbuchungen; aktuelleBuchung; {
-       Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
-     }));;
-     Refresh(Tischbuchungen);;
- With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
-     Set(varZeigeVerwaltenTab; false);;
-     Set(varAusgewaehltePlusDauer; Blank());;
-     Clear(colAusgewaehlteBuchungen);;
-     Set(varMehrfachAuswahlModus; false)
+     If(
+       IsBlank(aktuelleBuchung);
+       Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+       Set(varZeigeVerwaltenTab; false);
+       With(
+         {
+           neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
+           tagesEnde: Date(Year(aktuelleBuchung.Startzeit); Month(aktuelleBuchung.Startzeit); Day(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
+         };
+         If(
+           neueEndzeit <= aktuelleBuchung.Startzeit;
+           Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
+           If(
+             varAusgewaehltePlusDauer > 0 && neueEndzeit > tagesEnde;
+             Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
+             If(
+               varAusgewaehltePlusDauer > 0 && CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
+               Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
+               With(
+                 { speicherStatus: IfError(Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit }); "fehler"; "ok") };
+                 If(
+                   speicherStatus = "fehler";
+                   Notify("Speichern fehlgeschlagen. Bitte die Buchung in der Liste prüfen."; NotificationType.Error);
+                   Set(varSelectedBuchungTab; LookUp(Tischbuchungen; ID = aktuelleBuchung.ID));;
+                   Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
+                   Set(varZeigeVerwaltenTab; false);;
+                   Clear(colAusgewaehlteBuchungen);;
+                   Set(varMehrfachAuswahlModus; false)
+                 )
+               )
+             )
+           )
+         )
+       )
+     )
    )
- )
+ );;
+ Refresh(Tischbuchungen);;
+ With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+ Set(varAusgewaehltePlusDauer; Blank());;
+ Set(varIsLoading; false)
```
**Einfügen: ganze Property `btnVerlängern_1.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    If(
      IsBlank(aktuelleBuchung);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwaltenTab; false);
      With(
        {
          neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
          tagesEnde: Date(Year(aktuelleBuchung.Startzeit); Month(aktuelleBuchung.Startzeit); Day(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
        };
        If(
          neueEndzeit <= aktuelleBuchung.Startzeit;
          Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
          If(
            varAusgewaehltePlusDauer > 0 && neueEndzeit > tagesEnde;
            Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
            If(
              varAusgewaehltePlusDauer > 0 && CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
              Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
              With(
                { speicherStatus: IfError(Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit }); "fehler"; "ok") };
                If(
                  speicherStatus = "fehler";
                  Notify("Speichern fehlgeschlagen. Bitte die Buchung in der Liste prüfen."; NotificationType.Error);
                  Set(varSelectedBuchungTab; LookUp(Tischbuchungen; ID = aktuelleBuchung.ID));;
                  Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
                  Set(varZeigeVerwaltenTab; false);;
                  Clear(colAusgewaehlteBuchungen);;
                  Set(varMehrfachAuswahlModus; false)
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varIsLoading; false)
```
**Test:** (1) Buchung im Tab um +1 Std verlängern → Meldung „Buchung geändert, neues Ende …“, Liste und Grundriss stimmen. (2) Verkürzen −1 Std → ok. (3) Buchung 19:00–21:30, +1 Std → „Über 22:00 Uhr …“, nichts geändert. (4) Zwei-Tab-Test: in Tab 2 direkt hinter die Buchung buchen, in Tab 1 (Dialog war schon offen, Knopf noch grün) +1 Std → „Der Tisch ist … inzwischen belegt“. (5) In Tab 2 die Buchung stornieren, in Tab 1 verlängern → „Diese Buchung gibt es nicht mehr“, Dialog zu.

### B2 `btnVerlängern_1.DisplayMode`
**K5 für Verlängern im Tab** (erst nach B1, denn erst B1 setzt `varIsLoading`)

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```
**Test:** Zweimal schnell auf Verlängern (+1 Std) → genau +1 Std, eine Meldung.

### B3 `btnVerlängern.OnSelect`
**K3 neu: Verlängern im Grundriss-Dialog**

Dieselbe Formel wie B1, nur mit den Grundriss-Namen: `varSelectedBuchung` statt `varSelectedBuchungTab`, `varZeigeVerwalten` statt `varZeigeVerwaltenTab`, ohne die zwei Mehrfachauswahl-Zeilen (die hatte der Grundriss-Knopf auch heute nicht). Neu gegenüber heute zusätzlich `Refresh(Tischbuchungen)` (fehlte hier bisher). Die Namen sind maschinell geprüft: B3 enthält keine Tab-Variable, B1 keine Grundriss-Variable.

Änderung (rot = weg, grün = neu, `...` = unverändert):
```diff
+ Set(varIsLoading; true);;
  With(
  ...
      Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
-     Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {
-       Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
-     }));;
-     Set(varZeigeVerwalten; false);;
-     Set(varAusgewaehltePlusDauer; Blank())
+     If(
+       IsBlank(aktuelleBuchung);
+       Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+       Set(varZeigeVerwalten; false);
+       With(
+         {
+           neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
+           tagesEnde: Date(Year(aktuelleBuchung.Startzeit); Month(aktuelleBuchung.Startzeit); Day(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
+         };
+         If(
+           neueEndzeit <= aktuelleBuchung.Startzeit;
+           Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
+           If(
+             varAusgewaehltePlusDauer > 0 && neueEndzeit > tagesEnde;
+             Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
+             If(
+               varAusgewaehltePlusDauer > 0 && CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
+               Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
+               With(
+                 { speicherStatus: IfError(Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit }); "fehler"; "ok") };
+                 If(
+                   speicherStatus = "fehler";
+                   Notify("Speichern fehlgeschlagen. Bitte die Buchung in der Liste prüfen."; NotificationType.Error);
+                   Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = aktuelleBuchung.ID));;
+                   Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
+                   Set(varZeigeVerwalten; false)
+                 )
+               )
+             )
+           )
+         )
+       )
+     )
    )
  );;
- With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+ Refresh(Tischbuchungen);;
+ With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+ Set(varAusgewaehltePlusDauer; Blank());;
+ Set(varIsLoading; false)
```
**Einfügen: ganze Property `btnVerlängern.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    If(
      IsBlank(aktuelleBuchung);
      Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
      Set(varZeigeVerwalten; false);
      With(
        {
          neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes);
          tagesEnde: Date(Year(aktuelleBuchung.Startzeit); Month(aktuelleBuchung.Startzeit); Day(aktuelleBuchung.Startzeit)) + Time(22; 0; 0)
        };
        If(
          neueEndzeit <= aktuelleBuchung.Startzeit;
          Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
          If(
            varAusgewaehltePlusDauer > 0 && neueEndzeit > tagesEnde;
            Notify("Über 22:00 Uhr hinaus kann nicht verlängert werden."; NotificationType.Warning);
            If(
              varAusgewaehltePlusDauer > 0 && CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
              Notify("Der Tisch ist in diesem Zeitraum inzwischen belegt. Bitte eine andere Dauer wählen."; NotificationType.Warning);
              With(
                { speicherStatus: IfError(Patch(Tischbuchungen; aktuelleBuchung; { Endzeit: neueEndzeit }); "fehler"; "ok") };
                If(
                  speicherStatus = "fehler";
                  Notify("Speichern fehlgeschlagen. Bitte die Buchung in der Liste prüfen."; NotificationType.Error);
                  Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = aktuelleBuchung.ID));;
                  Notify("Buchung geändert, neues Ende " & Text(neueEndzeit; "hh:mm") & " Uhr."; NotificationType.Success);;
                  Set(varZeigeVerwalten; false)
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varIsLoading; false)
```
**Test:** Wie B1 Punkt (1), (3), (4), (5), aber über den Grundriss (Kachel anklicken → Verwalten). Verkürzen gibt es im Grundriss-Dialog nicht (nur Plus-Knöpfe), der Zweig ist harmlos. Zusätzlich: Nach dem Verlängern stimmen Kachelfarbe und, beim erneuten Öffnen, die angezeigte Endzeit (`lblZeit`).

### B4 `btnVerlängern.DisplayMode`
**K5 für Verlängern im Grundriss** (erst nach B3)

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```
**Test:** wie B2 im Grundriss.

## 5. Teil C: ehrliche Meldungen bei Serien (optional, auch nach dem Go-Live möglich)
**Jeder Speichern-Knopf wird hier nur einmal angefasst.** C1/C2 enthalten zusätzlich K4.1: Die Kollisionsabfrage holt nur noch die Buchungen dieses Tisches im Serienzeitraum (Startdatum bis +16 Tage) statt aller, die es je gab. Das spart Daten und schützt vor dem Datenzeilenlimit. Der Rest der Formel ist wortgleich mit heute (inkl. L2-Ladezeile).

### C1 `btnSpeichern.OnSelect`
**K4.1 + K4.4 (angepasst an den Sammel-Patch): weniger Daten, eine Meldung, die alles sagt**

Zwei Stellen: (1) Zeile `bestehendeBuchungenTisch` mit Zeitfenster. (2) Meldungsteil: Heute verdrängt „auf 2 Wochen begrenzt“ die Kollisionsmeldung (Befund B3). Neu: Normalfall unverändert „Buchung(en) erfolgreich gespeichert.“, sonst **eine** gelbe Meldung mit allem, z. B. „8 von 11 Terminen gespeichert. Wegen Kollision nicht gebucht: 3. Die Wiederholung wurde auf 2 Wochen begrenzt.“ Fehlerfall wie bisher.

Änderung (rot = weg, grün = neu, `...` = unverändert):
```diff
  ...
      effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate);
-     bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel)
+     bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Endzeit > dpDatum.SelectedDate && Startzeit < DateAdd(dpDatum.SelectedDate; 16; TimeUnit.Days))
    };
  ...
                  With(
-                   { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) };
+                   {
+                     anzahlGespeichert: If(speicherStatus = "ok"; CountRows(neueDatensaetze); 0);
+                     anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze)
+                   };
                    If(
  ...
                      If(
-                       effektivesBisRoh > effektivesBis;
-                       Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
-                       If(
-                         anzahlUebersprungen > 0;
-                         Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
-                         Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
+                       anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
+                       Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
+                       Notify(
+                         anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
+                         If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
+                         If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
+                         NotificationType.Warning
                        )
  ...
```
**Einfügen: ganze Property `btnSpeichern.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel && Endzeit > dpDatum.SelectedDate && Startzeit < DateAdd(dpDatum.SelectedDate; 16; TimeUnit.Days))
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatum.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatum.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatum.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                neueDatensaetze:
                  ForAll(
                    Filter(
                      datumsListe As Eintrag;
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0
                    ) As Frei;
                    {
                      Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
                      Startzeit: Frei.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                      Endzeit: Frei.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                      Person: {
                        Claims: "i:0#.f|membership|" & Lower(User().Email);
                        Department: "";
                        DisplayName: User().FullName;
                        Email: User().Email;
                        JobTitle: "";
                        Picture: ""
                      }
                    }
                  )
              };
              With(
                {
                  speicherStatus:
                    If(
                      CountRows(neueDatensaetze) = 0;
                      "keine";
                      IfError(
                        Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze);
                        "fehler";
                        "ok"
                      )
                    )
                };
                With(
                  {
                    anzahlGespeichert: If(speicherStatus = "ok"; CountRows(neueDatensaetze); 0);
                    anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze)
                  };
                  If(
                    speicherStatus = "fehler";
                    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen."; NotificationType.Error);
                    If(
                      anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
                      Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
                      Notify(
                        anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
                        If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
                        If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
                        NotificationType.Warning
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varZeigeDialog; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varIsLoading; false)
```
**Test:** Einzelbuchung → „Buchung(en) erfolgreich gespeichert.“ Serie mit Bis-Datum in 4 Wochen (wird gekappt) auf einen Tisch mit einer fremden Buchung im Zeitraum → eine Meldung nennt Anzahl, Kollision und Kappung; die fremde Buchung wurde nicht doppelt belegt.

### C2 `btnSpeichernTischePanel.OnSelect`
**K4.1 + K4.3 + K4.4: Panel mit weniger Daten, erkennt Schreibfehler, eine Meldung**

Drei Stellen: (1) `bestehendeBuchungenTisch` mit Zeitfenster wie C1. (2) Der einzelne `Patch` steht in `IfError`: Schlägt ein Termin fehl, zählt er als „fehler“ statt als „gespeichert“ (Befund B2). (3) Meldung wie C1, zusätzlich mit Fehleranzahl (dann rot). Aufräumteil unverändert.

Änderung (rot = weg, grün = neu, `...` = unverändert):
```diff
  ...
      effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate);
-     bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel)
+     bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Endzeit > dpDatumTischePanel.SelectedDate && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; 16; TimeUnit.Days))
    };
  ...
                        CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0;
-                       With(
-                         {
-                           neuerEintrag: Patch(Tischbuchungen; Defaults(Tischbuchungen); {
-                             Tisch: {Id: ddTischePanel.Selected.ID; Value: ddTischePanel.Selected.Titel};
-                             Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
-                             Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
-                             Person: {
-                               Claims: "i:0#.f|membership|" & Lower(User().Email);
-                               Department: "";
-                               DisplayName: User().FullName;
-                               Email: User().Email;
-                               JobTitle: "";
-                               Picture: ""
-                             }
-                           })
-                         };
+                       IfError(
+                         Patch(Tischbuchungen; Defaults(Tischbuchungen); {
+                           Tisch: {Id: ddTischePanel.Selected.ID; Value: ddTischePanel.Selected.Titel};
+                           Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
+                           Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
+                           Person: {
+                             Claims: "i:0#.f|membership|" & Lower(User().Email);
+                             Department: "";
+                             DisplayName: User().FullName;
+                             Email: User().Email;
+                             JobTitle: "";
+                             Picture: ""
+                           }
+                         });
+                         "fehler";
                          "gespeichert"
  ...
                With(
-                 { anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen")) };
+                 {
+                   anzahlGespeichert: CountRows(Filter(ergebnisse; Value = "gespeichert"));
+                   anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen"));
+                   anzahlFehler: CountRows(Filter(ergebnisse; Value = "fehler"))
+                 };
                  If(
-                   effektivesBisRoh > effektivesBis;
-                   Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
-                   If(
-                     anzahlUebersprungen > 0;
-                     Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
-                     Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
+                   anzahlFehler = 0 && anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
+                   Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
+                   Notify(
+                     anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
+                     If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
+                     If(anzahlFehler > 0; " Fehler beim Speichern: " & anzahlFehler & ", bitte unter Meine Buchungen prüfen."; "") &
+                     If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
+                     If(anzahlFehler > 0; NotificationType.Error; NotificationType.Warning)
                    )
  ...
```
**Einfügen: ganze Property `btnSpeichernTischePanel.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Endzeit > dpDatumTischePanel.SelectedDate && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; 16; TimeUnit.Days))
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatumTischePanel.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatumTischePanel.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatumTischePanel.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatumTischePanel.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag;
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0;
                      IfError(
                        Patch(Tischbuchungen; Defaults(Tischbuchungen); {
                          Tisch: {Id: ddTischePanel.Selected.ID; Value: ddTischePanel.Selected.Titel};
                          Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                          Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                          Person: {
                            Claims: "i:0#.f|membership|" & Lower(User().Email);
                            Department: "";
                            DisplayName: User().FullName;
                            Email: User().Email;
                            JobTitle: "";
                            Picture: ""
                          }
                        });
                        "fehler";
                        "gespeichert"
                      );
                      "übersprungen"
                    )
                  )
              };
              With(
                {
                  anzahlGespeichert: CountRows(Filter(ergebnisse; Value = "gespeichert"));
                  anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen"));
                  anzahlFehler: CountRows(Filter(ergebnisse; Value = "fehler"))
                };
                If(
                  anzahlFehler = 0 && anzahlUebersprungen = 0 && !(effektivesBisRoh > effektivesBis);
                  Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success);
                  Notify(
                    anzahlGespeichert & " von " & CountRows(datumsListe) & " Terminen gespeichert." &
                    If(anzahlUebersprungen > 0; " Wegen Kollision nicht gebucht: " & anzahlUebersprungen & "."; "") &
                    If(anzahlFehler > 0; " Fehler beim Speichern: " & anzahlFehler & ", bitte unter Meine Buchungen prüfen."; "") &
                    If(effektivesBisRoh > effektivesBis; " Die Wiederholung wurde auf 2 Wochen begrenzt."; "");
                    If(anzahlFehler > 0; NotificationType.Error; NotificationType.Warning)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
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
Set(varEndeOverridePanel; "");;
Set(varIsLoading; false)
```
**Test:** Wie C1 über das Tische-Panel. Den Fehlerfall kann man nicht gezielt auslösen (UNSICHER, siehe U-K6).

## 6. Teil E: Entscheidung Mehrfachauswahl (nur falls du sie zum Go-Live ausblenden willst)
### E2 `tglAuswahlModus.Visible`
Der Schalter hat heute keine `Visible`-Property (= sichtbar). Ausblenden genügt: Ohne Schalter bleibt `varAuswahlModusAktiv` falsch (`App.OnStart`), alle Einzel-Funktionen bleiben.

```
false
```
**Rückgängig:** `true`. **Test:** Tab „Meine Buchungen“: kein Auswahlschalter, Verwalten-Knopf öffnet den normalen Dialog.


## 7. Rückfall
- Einzelner Schritt: die Originalformel aus Anhang 1 einfügen (bei DisplayMode/Visible: `DisplayMode.Edit` bzw. `true`).
- Teil B zurück, Teil A behalten: geht, A und B sind unabhängig. B2/B4 vor B1/B3 zurücknehmen (sonst ist der Knopf nach einem Fehler gesperrt, siehe U-K2).
- Teil C zurück: Original aus Anhang 1 einfügen. A, B und C sind unabhängig voneinander (C ändert `OnSelect` der Speichern-Knöpfe, A nur deren `DisplayMode`).
- Komplett: `.msapp`-Export oder Versionsverlauf.

## 8. UNSICHER (mit Prüftest)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-K1 | `Date(Year(x); Month(x); Day(x)) + Time(22; 0; 0)` ergibt 22:00 Ortszeit am Buchungstag. Das Muster `Datum + Time(22; 0; 0)` nutzt die App schon (`btn5Std`), `Date(...)` aus einer Buchung noch nicht | 22:00-Grenze greift zu früh/spät | B1-Test (3): 19:00–21:30, +1 Std → abgelehnt; 19:00–20:30, +1 Std → erlaubt |
| U-K2 | DisplayMode-Sperre: Hängt eine Formel unerwartet ab, bleibt `varIsLoading` wahr und der Knopf gesperrt | Knopf bleibt grau bis zum Neustart | Bei jedem Test prüfen, ob Overlay und Knopf danach wieder frei sind. Alle Wege setzen `varIsLoading` am Ende auf falsch |
| U-K3 | Ob die DisplayMode-Sperre einen sehr schnellen Doppelklick wirklich abfängt (Power Apps garantiert kein Neuzeichnen zwischen zwei Anweisungen) | Ein zweiter Klick kommt selten doch durch | A2- und B2-Test mehrmals. Restrisiko bleibt; die Serverprüfung in B1/B3 fängt es nicht ab, weil die eigene Buchung nicht als Kollision zählt |
| U-K4 | `IfError(Patch(...); "fehler"; "ok")` in `With` erkennt einen fehlgeschlagenen Patch. Muster aus `btnSpeichern`, dort läuft es, ein echter Fehler wurde aber nie ausgelöst | Fehler wird als Erfolg gemeldet (wie heute) | WLAN kurz aus, verlängern → erwartet rote Meldung |
| U-K5 | Mehrere geschachtelte `If` mit `Notify` und `Set` in den Zweigen bei `powerfxv1 = false`. Die App mischt das schon (z. B. `btnStornierenKlein`, L2-Ladezeile) | rote Formel beim Einfügen | App-Prüfung nach B1 |
| U-K6 | C2-Fehlerzweig nicht gezielt testbar | Fehlermeldung unerprobt | hinnehmen, Normalfall testen |
| U-K7 | C1/C2: Zeitfenster 16 Tage muss größer als die Serien-Kappung (Start + 14 Tage) bleiben | Kollision am letzten Serientag übersehen | Falls die Kappung je geändert wird: Zahl 16 mitändern |

## 9. Nach dem Go-Live (bewusst nicht in diesem Paket)
| Vorhaben | Warum später |
|---|---|
| L3 versteckte Dialoge nur rechnen, wenn offen | nach L2 kaum spürbar (~50 Abfragen pro Schreibwelle, Speichern ~5 s) |
| L4 Raumcode stilllegen + `App.OnStart` aufräumen | Start ~3 s, stört nicht; größere Änderung |
| Plus-Knöpfe ab 22:00 grau | B1/B3 lehnen schon ab; Komfort |
| Nur freie Tische im Panel (Muster aus der Handy-App) | Umbau von Panel und Speichern |
| Vorprüfung mit Alternativtischen, `SerienID`-Nachlese | großes Konzept |
| Panel-Speichern auf Sammel-Patch | Panel misst ~5 s, kein Bedarf |
| Spinner-Optik | kosmetisch, verworfen |
| Fund am Rande: `dpWiederholenBis_1.OnChange` rechnet ein `If` ohne `Set` (wirkungslos, harmlos) | Aufräumen bei L4 |

## 10. Regeln
Deutsche Schreibweise (`;` trennt, `;;` verkettet), keine Kommentare, immer die **ganze** Property ersetzen, ein Studio-Fenster, Schritte einzeln, nach jedem Schritt App-Prüfung. Die zwei Speichern-Knöpfe und die zwei Verlängern-Knöpfe sind **nicht** wortgleich: jeden einzeln einfügen.

## Anhang 1: Originale (für den Rückfall, aus dem Export)
**`btnVerwalten_2.OnSelect`**

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```
**`btnSpeichern.OnSelect`**

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatum.SelectedDate + Time(Value(Left(ddStart.Selected.Value; 2)); Value(Mid(ddStart.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatum.SelectedDate + Time(Value(Left(ddEnde.Selected.Value; 2)); Value(Mid(ddEnde.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis.SelectedDate <> dpDatum.SelectedDate; dpWiederholenBis.SelectedDate; dpDatum.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = varSelectedTisch.Titel)
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatum.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatum.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatum.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatum.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                neueDatensaetze:
                  ForAll(
                    Filter(
                      datumsListe As Eintrag;
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0
                    ) As Frei;
                    {
                      Tisch: {Id: varSelectedTisch.ID; Value: varSelectedTisch.Titel};
                      Startzeit: Frei.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                      Endzeit: Frei.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                      Person: {
                        Claims: "i:0#.f|membership|" & Lower(User().Email);
                        Department: "";
                        DisplayName: User().FullName;
                        Email: User().Email;
                        JobTitle: "";
                        Picture: ""
                      }
                    }
                  )
              };
              With(
                {
                  speicherStatus:
                    If(
                      CountRows(neueDatensaetze) = 0;
                      "keine";
                      IfError(
                        Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze);
                        "fehler";
                        "ok"
                      )
                    )
                };
                With(
                  { anzahlUebersprungen: CountRows(datumsListe) - CountRows(neueDatensaetze) };
                  If(
                    speicherStatus = "fehler";
                    Notify("Speichern fehlgeschlagen. Möglicherweise wurden einzelne Termine gespeichert, bitte unter Meine Buchungen prüfen."; NotificationType.Error);
                    If(
                      effektivesBisRoh > effektivesBis;
                      Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
                      If(
                        anzahlUebersprungen > 0;
                        Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
                        Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varZeigeDialog; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varIsLoading; false)
```
**`btnSpeichernTischePanel.OnSelect`**

```
Set(varIsLoading; true);;
With(
  {
    neuStart: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    neuEnde: dpDatumTischePanel.SelectedDate + Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    effektivesBisRoh: If(varWiederholen && dpWiederholenBis_1.SelectedDate <> dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate);
    bestehendeBuchungenTisch: Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel)
  };
  With(
    { effektivesBis: Min(effektivesBisRoh; dpDatumTischePanel.SelectedDate + 14) };
    With(
      { anzahlTage: DateDiff(dpDatumTischePanel.SelectedDate; effektivesBis; TimeUnit.Days) + 1 };
      With(
        { alleDatumsWerte: ForAll(Sequence(anzahlTage; 0); DateAdd(dpDatumTischePanel.SelectedDate; Value; TimeUnit.Days)) };
        With(
          {
            datumsListe:
              If(
                !varWiederholen;
                [dpDatumTischePanel.SelectedDate];
                If(
                  varWiederholenModus = "Taeglich";
                  alleDatumsWerte;
                  Filter(
                    alleDatumsWerte;
                    Switch(
                      Weekday(Value; StartOfWeek.Monday);
                      1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo
                    )
                  )
                )
              )
          };
          If(
            varWiederholen && CountRows(datumsListe) = 0;
            If(
              !varTagMo && !varTagDi && !varTagMi && !varTagDo && !varTagFr && !varTagSa && !varTagSo;
              Notify("Bitte mindestens einen Wochentag auswählen."; NotificationType.Warning);
              Notify("Der gewählte Zeitraum enthält keinen der ausgewählten Wochentage. Bitte Enddatum anpassen."; NotificationType.Warning)
            );
            With(
              {
                ergebnisse:
                  ForAll(
                    datumsListe As Eintrag;
                    If(
                      CountRows(Filter(bestehendeBuchungenTisch; Startzeit < (Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0)) && Endzeit > (Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0)))) = 0;
                      With(
                        {
                          neuerEintrag: Patch(Tischbuchungen; Defaults(Tischbuchungen); {
                            Tisch: {Id: ddTischePanel.Selected.ID; Value: ddTischePanel.Selected.Titel};
                            Startzeit: Eintrag.Value + Time(Hour(neuStart); Minute(neuStart); 0);
                            Endzeit: Eintrag.Value + Time(Hour(neuEnde); Minute(neuEnde); 0);
                            Person: {
                              Claims: "i:0#.f|membership|" & Lower(User().Email);
                              Department: "";
                              DisplayName: User().FullName;
                              Email: User().Email;
                              JobTitle: "";
                              Picture: ""
                            }
                          })
                        };
                        "gespeichert"
                      );
                      "übersprungen"
                    )
                  )
              };
              With(
                { anzahlUebersprungen: CountRows(Filter(ergebnisse; Value = "übersprungen")) };
                If(
                  effektivesBisRoh > effektivesBis;
                  Notify("Wiederholung wurde auf 2 Wochen begrenzt."; NotificationType.Warning);
                  If(
                    anzahlUebersprungen > 0;
                    Notify(anzahlUebersprungen & " von " & CountRows(datumsListe) & " Terminen konnten wegen Kollision nicht gebucht werden."; NotificationType.Warning);
                    Notify("Buchung(en) erfolgreich gespeichert."; NotificationType.Success)
                  )
                )
              )
            )
          )
        )
      )
    )
  )
);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
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
Set(varEndeOverridePanel; "");;
Set(varIsLoading; false)
```
**`btnVerlängern_1.OnSelect`**

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    Set(varSelectedBuchungTab; Patch(Tischbuchungen; aktuelleBuchung; {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
    }));;
    Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
    Set(varZeigeVerwaltenTab; false);;
    Set(varAusgewaehltePlusDauer; Blank());;
    Clear(colAusgewaehlteBuchungen);;
    Set(varMehrfachAuswahlModus; false)
  )
)
```
**`btnVerlängern.OnSelect`**

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  If(
    IsBlank(varAusgewaehltePlusDauer);
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {
      Endzeit: DateAdd(aktuelleBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes)
    }));;
    Set(varZeigeVerwalten; false);;
    Set(varAusgewaehltePlusDauer; Blank())
  )
);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```
**`btnSpeichern.DisplayMode`, `btnSpeichernTischePanel.DisplayMode`, `btnVerlängern.DisplayMode`, `btnVerlängern_1.DisplayMode`**: im Export nicht gesetzt. Rückgängig: `DisplayMode.Edit`.

## Anhang 2: Maschinelle Prüfung (erzeugt von `erzeuge_konzept.ps1`)
```
OK  L2-Ladezeile in allen Verlaengern/Speichern-Knoepfen vorhanden (Export = L2-Stand)
OK  Die 4 Knoepfe haben noch kein DisplayMode, tglAuswahlModus kein Visible
OK  A1 K1 : Anker genau 1x gefunden
OK  C1 K4.1 : Anker genau 1x gefunden
OK  C2 K4.1 : Anker genau 1x gefunden
OK  B1 nutzt nur Tab-Variablen, B3 nur Grundriss-Variablen
OK  C1 Meldung Dialog : Block genau 1x gefunden
OK  C2 K4.3 : Patch-Block genau 1x gefunden und in IfError gesetzt
OK  C2 K4.4 Meldung Panel : Block genau 1x gefunden
OK  A1 : Klammern, Strings, Kommas, Namen geprueft
OK  B1 : Klammern, Strings, Kommas, Namen geprueft
OK  B3 : Klammern, Strings, Kommas, Namen geprueft
OK  C1 : Klammern, Strings, Kommas, Namen geprueft
OK  C2 : Klammern, Strings, Kommas, Namen geprueft
OK  K5 : Klammern, Strings, Kommas, Namen geprueft
OK  A1 : nur erlaubte Zeilen geaendert (1 Zeilen)
OK  K4.1 Dialog : nur erlaubte Zeilen geaendert (2 Zeilen)
OK  K4.1 Panel : nur erlaubte Zeilen geaendert (2 Zeilen)
Keine Fehler.
```
