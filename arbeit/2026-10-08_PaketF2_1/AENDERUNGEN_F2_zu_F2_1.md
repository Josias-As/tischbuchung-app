# Paket F: Änderungen von Fassung 2 zu Fassung 2.1 (08.10.2026)

**Anlass (belegt):** App-Prüfung nach F1: „Die Funktion ‚DropColumns‘ weist ungültige Argumente auf. Erwarteter Name des Bezeichners“.

**Änderung:** In der Ladezeile `DropColumns(…; Erstellt)` statt `DropColumns(…; "Erstellt")`. Sonst ändert sich **nichts** (maschinell geprüft: alte und neue Fassung unterscheiden sich in jedem Block nur an dieser Stelle).

**Betroffen:** 16 von 37 Properties. Die übrigen 21 sind unverändert.

**Andere Stellen geprüft:** `AddColumns`, `RenameColumns` und `ShowColumns` kommen weder im Export noch im Gesamtplan, in Paket F2 oder im Handy-Plan vor.

`SortByColumns(…; "Startzeit")` mit Text steht schon im veröffentlichten Export (`galAlleTischbuchungen`, `Label4`/`Label5`, Handy `galMeine`/`galHeute`) und läuft dort (**belegt**). Deshalb bleibt es so.

Der Generator meldet ab jetzt jeden Spaltennamen als Text in `Add/Drop/Rename/ShowColumns` als Fehler. Gegenprobe gemacht: Die alte Schreibweise wird erkannt.

**So einfügen:**
- **F1 neu einfügen** mit dem Block unten. Danach OnStart ausführen und die App-Prüfung ansehen.
- Ist `Erstellt` **an anderer Stelle** rot (nicht in `DropColumns`), sofort melden. Das ist dann U1 (Spaltenname), siehe Vorab-Test.
- Für F2 bis F8 die Blöcke aus `UEBERGABE_PaketF2_1.md` nehmen oder die Blöcke hier. Sie sind identisch.

Die Diffs gegen den Stand im Studio stehen in `UEBERGABE_PaketF2_1.md`.

## Geänderte Blöcke

### F1 `App.OnStart`

Änderung gegenüber Fassung 2:

```diff
@@ -119 +119 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block (Fassung 2.1):

```
Set(varFreigabeMinuten; 30);;
Set(varCheckinGefragtID; 0);;
Set(varAuscheckFrageID; 0);;
Set(varSperreBis; Now());;
Set(varVerlGrenze; Now());;
Set(varVerlGrenzeTab; Now());;
Set(varSelectedTisch; Blank());;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedBuchung; Blank());;
Set(varAktiverTab; "dashboard");;
Set(varZeigeRaumBuchungForm; false);;
Set(varAusgewähltRaum; Blank());;
Set(varAusgewählteStartzeit; Blank());;
Set(varAusgewählteEndzeit; Blank());;
Set(varZeigeRaumBestätigung; false);;
Set(varWiederholen; false);;
Set(varWiederholenModus; "Wochentage");;
Set(varTagMo; false);;
Set(varTagDi; false);;
Set(varTagMi; false);;
Set(varTagDo; false);;
Set(varTagFr; false);;
Set(varTagSa; false);;
Set(varTagSo; false);;
Set(varWiederholenBis; Today() + 14);;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeRaumInfo; false);;
Set(varZeigeRaumVerwalten; false);;
Set(
  varProfilFarbe;
  Switch(
    RandBetween(1; 8);
    1; ColorValue("#8CAFF4");
    2; ColorValue("#82C7B3");
    3; ColorValue("#EFA897");
    4; ColorValue("#B59EDC");
    5; ColorValue("#82CCC5");
    6; ColorValue("#F5C295");
    7; ColorValue("#A1AADB");
    ColorValue("#A1B1BA")
  )
);;
Set(varZoom; 1);;
Set(varPanX; 0);;
Set(varPanY; 0);;
Set(varWiederholenBisGewaehlt; false);;
ClearCollect(
  colTischPositionen;
  {Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 2"; X: 1629; Y: 290; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 3"; X: 1732; Y: 288; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 4"; X: 1629; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 5"; X: 1732; Y: 346; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 6"; X: 1734; Y: 536; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 7"; X: 1734; Y: 596; Ausrichtung: "Horizontal"};
  {Tisch: "OG Desk 8"; X: 1500; Y: 484; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 9"; X: 1500; Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 10"; X: 1500; Y: 683; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 11"; X: 1560; Y: 468; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 12"; X: 1560; Y: 582; Ausrichtung: "Vertikal"};
  {Tisch: "OG Desk 13"; X: 1560; Y: 681; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 3"; X: 870; Y: 687; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 2"; X: 870; Y: 594; Ausrichtung: "Vertikal"};
  {Tisch: "Quiet Desk 1"; X: 870; Y: 501; Ausrichtung: "Vertikal"}
);;
Set(varSelectedBuchungTab; Blank());;
Set(varZeigeVerwaltenTab; false);;
Set(varStartOverridePanel; "");;
Set(varEndeOverridePanel; "");;
Set(varAusgewaehltePanelDauer; Blank());;
Set(varAnsichtsDatum; Today());;
Set(varAusgewaehltesStockwerk; "OG");;
Set(varStockwerkDropdownOffen; false);;
Set(varStartOverride; "");;
Set(varEndeOverride; "");;
Clear(colAusgewaehlteBuchungen);;
Set(varMehrfachAuswahlModus; false);;
Set(varAuswahlModusAktiv; false);;
Set(varZeigeVerwaltenKlein; false);;
Set(varGalleryNeuAufbauen; 0);;
Set(varGeklickteBuchungKlein; Blank());;
ClearCollect(
  colTischPositionenUG;
  {Tisch: "UG Desk 1";  X: 530;  Y: 592; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 2";  X: 530;  Y: 679; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 3";  X: 582;  Y: 588; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 4";  X: 582;  Y: 675; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 5";  X: 738;  Y: 584; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 6";  X: 738;  Y: 671; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 7";  X: 790;  Y: 579; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 8";  X: 790;  Y: 666; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 9";  X: 1011; Y: 575; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 10"; X: 1011; Y: 662; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 11"; X: 1063; Y: 571; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 12"; X: 1063; Y: 658; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 13"; X: 1202; Y: 260; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 14"; X: 1210; Y: 348; Ausrichtung: "Horizontal"};
  {Tisch: "UG Desk 15"; X: 1255; Y: 256; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 16"; X: 1360; Y: 254; Ausrichtung: "Vertikal"};
  {Tisch: "UG Desk 17"; X: 1410; Y: 252; Ausrichtung: "Vertikal"};
  {Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
);;
Set(varIsLoading; false);;
Set(varSpinnerWinkel; 0);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colCheckinFrage; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()));;
RemoveIf(colCheckinFrage; CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
If(
  !IsEmpty(colCheckinFrage);
  Set(varCheckinGefragtID; First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID);;
  Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinGefragtID));;
  Set(varZeigeCheckin; true)
);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

### F2 `btnStornieren.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -24 +24 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwalten; false);
    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
    IfError(
      Remove(Tischbuchungen; varStornoBuchung);
      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeVerwalten; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F2 `btnStornieren_1.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -24 +24 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwaltenTab; false);
    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
    IfError(
      Remove(Tischbuchungen; varStornoBuchung);
      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      If(
        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
        Notify("Buchung storniert."; NotificationType.Success);;
        Set(varZeigeVerwaltenTab; false);
        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F2 `btnStornierenKlein.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -31 +31 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  ClearCollect(
      colStornoFrisch;
      Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
  );;
  ClearCollect(
      colStornoZiele;
      Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
  );;
  If(
      CountRows(colAusgewaehlteBuchungen) = 0;
      Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
      If(
          CountRows(colStornoZiele) = 0;
          Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
          IfError(
              Remove(Tischbuchungen; colStornoZiele);
              Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
              If(
                  CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
                  Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
                  Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
              )
          )
      )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  Clear(colStornoFrisch);;
  Clear(colStornoZiele);;
  Clear(colAusgewaehlteBuchungen);;
  Set(varGeklickteBuchungKlein; Blank());;
  Set(varZeigeVerwaltenKlein; false);;
  Set(varAuswahlModusAktiv; false);;
  Reset(tglAuswahlModus);;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F3 `ddStockwerk.OnChange`

Änderung gegenüber Fassung 2:

```diff
@@ -4 +4 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block (Fassung 2.1):

```
Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
Set(varStockwerkDropdownOffen; false);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

### F3 `dpAnsichtsDatum.OnChange`

Änderung gegenüber Fassung 2:

```diff
@@ -3 +3 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block (Fassung 2.1):

```
Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

### F3 `Icon1_1.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -4 +4 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
```

Vollständiger Block (Fassung 2.1):

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

### F3 `Icon1.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -4 +4 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
```

Vollständiger Block (Fassung 2.1):

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

### F3 `Image6.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -4 +4 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
```

Vollständiger Block (Fassung 2.1):

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

### F3 `btnHitArea_1.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -4 +4 @@
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"));; Notify("Aktualisiert."; NotificationType.Success)));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
```

Vollständiger Block (Fassung 2.1):

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

### F4 `btnSpeichern.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -137 +137 @@
-    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block (Fassung 2.1):

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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F4 `btnSpeichernTischePanel.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -145 +145 @@
-    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))))
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block (Fassung 2.1):

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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F6 `btnVerlängern.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -47 +47 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0;
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    IsBlank(varVerlBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwalten; false);
    Set(varVerlTisch; varVerlBuchung.Tisch.Value);;
    Set(varVerlEndeAlt; varVerlBuchung.Endzeit);;
    Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
    Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenze; varVerlEndeAlt);
      IfError(
        Patch(Tischbuchungen; varVerlBuchung; {Endzeit: varVerlEndeNeu});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varVerlBuchung.ID));;
        If(
          varSelectedBuchung.Endzeit = varVerlEndeNeu;
          Notify("Buchung geändert, neues Ende " & Text(varVerlEndeNeu; "hh:mm") & " Uhr."; NotificationType.Success);;
          Set(varZeigeVerwalten; false);
          Notify("Die Änderung ist nicht angekommen. Bitte die Buchung in der Liste prüfen."; NotificationType.Warning)
        )
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F6 `btnVerlängern_1.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -47 +47 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
  If(
    IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0;
    Notify("Bitte eine Dauer auswählen."; NotificationType.Warning);
    IsBlank(varVerlBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwaltenTab; false);
    Set(varVerlTisch; varVerlBuchung.Tisch.Value);;
    Set(varVerlEndeAlt; varVerlBuchung.Endzeit);;
    Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
    Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenzeTab; varVerlEndeAlt);
      IfError(
        Patch(Tischbuchungen; varVerlBuchung; {Endzeit: varVerlEndeNeu});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchungTab; LookUp(Tischbuchungen; ID = varVerlBuchung.ID));;
        If(
          varSelectedBuchungTab.Endzeit = varVerlEndeNeu;
          Notify("Buchung geändert, neues Ende " & Text(varVerlEndeNeu; "hh:mm") & " Uhr."; NotificationType.Success);;
          Set(varZeigeVerwaltenTab; false);
          Notify("Die Änderung ist nicht angekommen. Bitte die Buchung in der Liste prüfen."; NotificationType.Warning)
        )
      )
    )
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### F7 `btnEinchecken.OnSelect`

Änderung gegenüber Fassung 2:

```diff
@@ -83 +83 @@
-    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  varSelectedBuchung.CheckedIn && Now() >= varSelectedBuchung.Startzeit && varAuscheckFrageID <> varSelectedBuchung.ID;
  Set(varAuscheckFrageID; varSelectedBuchung.ID);;
  Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
  Notify("Zum Auschecken bitte noch einmal tippen. Deine Buchung endet dann jetzt."; NotificationType.Information);
  If(
    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
    Set(varIsLoading; true);;
    Set(varAuscheckFrageID; 0);;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
    Set(varCheckinTisch; varCheckinBuchung.Tisch.Value);;
    Set(varCheckinStart; varCheckinBuchung.Startzeit);;
    Set(varCheckinEnde; varCheckinBuchung.Endzeit);;
    If(
      IsBlank(varCheckinBuchung.ID);
      Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);;
      Set(varZeigeCheckin; false);
      Coalesce(varCheckinBuchung.CheckedIn; false) <> Coalesce(varSelectedBuchung.CheckedIn; false);
      Set(varSelectedBuchung; varCheckinBuchung);;
      Notify("Der Status hat sich inzwischen geändert. Bitte noch einmal prüfen und tippen."; NotificationType.Information);
      varCheckinBuchung.CheckedIn && Now() < varCheckinStart;
      IfError(
        Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: false});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
        If(
          !varSelectedBuchung.CheckedIn;
          Notify("Ausgecheckt. Die Buchung bleibt bestehen, bitte zum Beginn wieder einchecken."; NotificationType.Success);;
          Set(varZeigeCheckin; false);
          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
        )
      );
      varCheckinBuchung.CheckedIn && DateAdd(Now(); 1; TimeUnit.Minutes) >= varCheckinEnde;
      Notify("Die Buchung endet ohnehin jetzt."; NotificationType.Information);;
      Set(varZeigeCheckin; false);
      varCheckinBuchung.CheckedIn;
      Set(varCheckinNeuesEnde; DateAdd(Today(); Hour(Now()) * 60 + Minute(Now()) + 1; TimeUnit.Minutes));;
      IfError(
        Patch(Tischbuchungen; varCheckinBuchung; {Endzeit: varCheckinNeuesEnde});
        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
        If(
          varSelectedBuchung.Endzeit < varCheckinEnde;
          Notify("Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit; "hh:mm") & " Uhr. Andere können den Tisch wieder buchen."; NotificationType.Success);;
          Set(varZeigeCheckin; false);
          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
        )
      );
      Now() < DateAdd(varCheckinStart; -30; TimeUnit.Minutes);
      Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich."; NotificationType.Warning);
      Now() >= varCheckinEnde;
      Notify("Diese Buchung ist schon zu Ende."; NotificationType.Warning);;
      Set(varZeigeCheckin; false);
      varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Zu spät: Ohne Check-in bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen."; NotificationType.Warning);;
      Set(varZeigeCheckin; false);
      ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
      RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
      If(
        !IsEmpty(colCheckinAndere);
        Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen."; NotificationType.Error);;
        Set(varZeigeCheckin; false);
        IfError(
          Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: true});
          Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
          Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
          ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
          RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
          If(
            varSelectedBuchung.CheckedIn && !IsEmpty(colCheckinAndere);
            Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter Buchungen prüfen und klären."; NotificationType.Error);;
            Set(varZeigeCheckin; false);
            varSelectedBuchung.CheckedIn;
            Notify("Eingecheckt."; NotificationType.Success);;
            Set(varZeigeCheckin; false);
            Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
          )
        )
      )
    );;
    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
    Set(varIsLoading; false)
  )
)
```

### F8 `tmrAktualisieren.OnTimerEnd`

Änderung gegenüber Fassung 2:

```diff
@@ -10 +10 @@
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); "Erstellt"))));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
```

Vollständiger Block (Fassung 2.1):

```
If(
  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab && !varZeigeVerwaltenKlein && !varZeigeCheckin;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  Refresh(Tischbuchungen);;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
  If(
    varAktiverTab = "dashboard" && varAnsichtsDatum = Today() && !varZeigeDetails && !varZeigeRaumBuchungForm &&
    !IsBlank(LookUp(colGrundriss; Name = User().FullName && !Eingecheckt && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()).TischName);
    ClearCollect(colCheckinFrage; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()));;
    RemoveIf(colCheckinFrage; CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !IsEmpty(colCheckinFrage) && First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID <> varCheckinGefragtID;
      Set(varCheckinGefragtID; First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID);;
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinGefragtID));;
      Set(varZeigeCheckin; true)
    )
  )
)
```
