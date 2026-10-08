# Paket F, Fassung 2.1: Freigabe in der App, Stornieren direkt, Timer

> **Fassung 2.1 (08.10.):** einzige Änderung gegenüber Fassung 2 ist `DropColumns(…; Erstellt)` statt `DropColumns(…; "Erstellt")` in der Ladezeile (16 Properties). Studio hat bei F1 gemeldet: „Die Funktion ‚DropColumns‘ weist ungültige Argumente auf. Erwarteter Name des Bezeichners“ (**belegt**, U2 war damit falsch). Andere Funktionen mit Spaltennamen als Text gibt es im Paket nicht; `SortByColumns(…; "Startzeit")` läuft schon im veröffentlichten Export (**belegt**). Fassung 2 nicht mehr verwenden.

Stand 08.10.2026 · erzeugt mit `werkzeuge/paket_f2.py` und `doc_paket_f2.py` · **ersetzt Paket F (Fassung 1), Nachtrag 3 und 4 sowie G4, G5 und G8** · Ausgangslage ist der **tatsächliche Stand im Studio** (siehe 1) · Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**

## 0. Kurzfassung (wo A bis E stehen)
- **A Stornieren ohne Rückfrage-Dialog (Schritt F2):**
  - Die drei Stornieren-Knöpfe stornieren direkt, ohne neues Steuerelement.
  - Jeder Knopf hat: Sperre, frische Daten, **nur eigene** Buchungen, `IfError`, ehrliche Meldung, Ladezeile.
  - Dashboard und Tab lesen zusätzlich nach (Vergleich `Lower(E-Mail)`).
  - Mehrfach-Stornieren: gleich viele Abfragen wie heute (1 Abfrage, 1 Sammel-Remove, Refresh, Ladezeile), also **nicht langsamer** als die gemessenen 9 s für 33 Buchungen.
  - G4 entfällt ganz.
- **B Timer (Schritt F8):** Legt `tmrAktualisieren` an und **ersetzt G8**, ohne `varZeigeStornoFrage`. Mit Check-in-Erinnerung, die nur dann eine Abfrage macht, wenn du laut Grundriss gerade eine nicht eingecheckte Buchung hast. Eine reine G8-Fassung ohne Paket F steht in Anhang C.
- **C Paket F angepasst:** F1 bis F8 in der richtigen Einfügereihenfolge.
  - F4 enthält Nachtrag 4.
  - F7 enthält G5 (`btnEinchecken.DisplayMode`) und neu das **Auschecken mit zweitem Tippen**.
- **D Einfügeliste ohne Doppelarbeit (Abschnitt 2):** Jede Property kommt **genau einmal** vor. Zu jeder steht, was neu ist, und bei jedem Block ein **Diff gegen den Stand im Studio**.
- **E Vorab-Test „Erstellt“ (Abschnitt 3):** zwei Minuten, **vor** F1.
- **Umfang:** 8 Schritte, 37 Properties, 1 neues Steuerelement (`tmrAktualisieren`, das schon aus G8 vorgesehen war).
- **Geprüft:** maschinell 0 Fehler. Unabhängig geprüft: 3 hohe Befunde (Auschecken per Doppelklick, Auschecken nach veraltetem Status, Notweg) und 7 kleinere, **alle eingearbeitet** (`pruefung_paket_f2.md`). In Studio nichts getestet.
- **Wenn die Zeit knapp wird:** F1 bis F8 gehören **zusammen** (F1 legt `varFreigabeMinuten` an, alle anderen lesen sie). Entweder alle vor dem Go-Live oder keiner. **Notweg für sicheres Stornieren ohne Freigabe:** die drei Blöcke aus **Anhang D** (ohne F1, ohne Freigabe). Später ersetzt F2 sie.

## 1. Ausgangslage (nach Josias’ Angaben, nicht im Export prüfbar)
- **Eingefügt:** G1, G2, G3, G6 (Fassung Nachtrag 4), G7, G9, G10, G11, G12, G13, G15, G16, G17, G18, G19, G20, G25. G22 teilweise.
- **Nicht eingefügt:** G4, G5, G8, G14, G21, G23, G24, G26.
- **Phase 0:** erledigt bis auf die Mail an Michael.
- Die Diffs und Anhang A rechnen mit genau diesem Stand: Gesamtplan-Endfassung, wo eingefügt, sonst Export 07.10. **Keine Property dieses Pakets liegt in G22** (maschinell geprüft). Der unklare Stand dort spielt also keine Rolle.
- **Sieht ein Diff anders aus als das, was im Studio steht:** stoppen und melden. Dann stimmt die Ausgangslage nicht, z. B. wenn ein Schritt doch (nicht) eingefügt wurde.

## 2. Einfügeliste (D): jede Property genau einmal

Reihenfolge: **Vorab-Test (Abschnitt 3) → F1 → F2 → … → F8**. „Im Studio jetzt“ ist die Fassung, gegen die der Diff rechnet.

| Schritt | Property | im Studio jetzt | was neu ist |
|---|---|---|---|
| F1 | `App.OnStart` | Gesamtplan G1 | 3 Variablen vorbelegt (`varFreigabeMinuten`, `varCheckinGefragtID`, `varAuscheckFrageID`), Check-in-Frage vor der Ladezeile, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F2 | `btnStornieren.OnSelect` | Export 07.10. | direkt und sicher: Sperre, frisch lesen, nur eigene, IfError, Nachlese, Meldung, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F2 | `btnStornieren.DisplayMode` | – (neu) | neu: grau während des Speicherns |
| F2 | `btnStornieren_1.OnSelect` | Export 07.10. | wie `btnStornieren`, für den Tab |
| F2 | `btnStornieren_1.DisplayMode` | – (neu) | neu: grau während des Speicherns |
| F2 | `btnStornierenKlein.OnSelect` | Export 07.10. | Sperre dazu, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss`. Ablauf und Abfragen wie heute |
| F2 | `btnStornierenKlein.DisplayMode` | – (neu) | neu: grau während des Speicherns |
| F3 | `btnHitArea.OnSelect` | Gesamtplan G7 | Buchungen des Tisches holen, verfallene entfernen, dann Dialog oder Popup |
| F3 | `ddStockwerk.OnChange` | Export 07.10. | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F3 | `dpAnsichtsDatum.OnChange` | Export 07.10. | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F3 | `Icon1_1.OnSelect` | Gesamtplan G12 | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F3 | `Icon1.OnSelect` | Gesamtplan G12 | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F3 | `Image6.OnSelect` | Gesamtplan G12 | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F3 | `btnHitArea_1.OnSelect` | Gesamtplan G12 | Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F4 | `btnSpeichern.OnSelect` | Gesamtplan G6 (Fassung Nachtrag 4) | Grenze, verfallene aus Vorprüfung und Nachlese entfernen, Minuten in der Meldung, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss`. Nachtrag 4 bleibt |
| F4 | `btnSpeichernTischePanel.OnSelect` | Gesamtplan G6 (Fassung Nachtrag 4) | wie `btnSpeichern` |
| F5 | `btnTischHinzufügen.OnSelect` | Gesamtplan G7 | eine Zeile: Grenze beim Öffnen setzen |
| F5 | `ddTischePanel.Items` | Gesamtplan G9 | Feld `Aktiv`, nur aktive Buchungen zählen |
| F5 | `btn5Std.DisplayMode` | Gesamtplan G10 | Kollisionsprüfung nur mit aktiven Buchungen |
| F5 | `btn5Std.Fill` | Gesamtplan G10 | Kollisionsprüfung nur mit aktiven Buchungen |
| F5 | `btn9Std.DisplayMode` | Gesamtplan G10 | Kollisionsprüfung nur mit aktiven Buchungen |
| F5 | `btn9Std.Fill` | Gesamtplan G10 | Kollisionsprüfung nur mit aktiven Buchungen |
| F6 | `btnVerwalten.OnSelect` | Gesamtplan G2 | nächste Buchung am Tisch ohne verfallene (Collection statt direkter Abfrage) |
| F6 | `btnVerwalten_2.OnSelect` | Gesamtplan G2 | wie `btnVerwalten`, für den Tab |
| F6 | `btnVerlängern.OnSelect` | Gesamtplan G3 | Grenze, Kollision ohne verfallene, neu „zwei Tische“, eigene verfallene → Meldung, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F6 | `btnVerlängern_1.OnSelect` | Gesamtplan G3 | wie `btnVerlängern`, für den Tab |
| F7 | `btnEinchecken.OnSelect` | Export 07.10. | ersetzt G5: Fenster bis Frist, Prüfung „schon vergeben“ vor und nach dem Check-in, Auschecken = Ende jetzt mit zweitem Tippen, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss` |
| F7 | `btnEinchecken.DisplayMode` | – (neu) | aus G5: grau während des Speicherns |
| F7 | `btnEinchecken.Text` | Export 07.10. | „Wirklich auschecken?“ nach dem ersten Tippen |
| F7 | `btnEincheckenHeute.OnSelect` | Export 07.10. | setzt die Auscheck-Frage beim Öffnen zurück |
| F7 | `lblStatusHeute.Text` | Export 07.10. | neu „Verfallen“ |
| F7 | `lblStatusHeute.Color` | Export 07.10. | grau bei „Verfallen“ |
| F8 | `tmrAktualisieren.Duration` | – (neu) | neu (wie G8) |
| F8 | `tmrAktualisieren.Repeat` | – (neu) | neu (wie G8) |
| F8 | `tmrAktualisieren.AutoStart` | – (neu) | neu (wie G8) |
| F8 | `tmrAktualisieren.Visible` | – (neu) | neu (wie G8) |
| F8 | `tmrAktualisieren.OnTimerEnd` | – (neu) | neu: G8 ohne `varZeigeStornoFrage`, Ladezeile: Grenze setzen, `Erstellt` mitladen, verfallene nicht in `colGrundriss`, Check-in-Erinnerung mit lokaler Vorprüfung |

**Nicht mehr einfügen:** G4 (ganz), G5 (steckt in F7), G8 (steckt in F8), Paket F Fassung 1, Nachtrag 3 und 4 (stecken in F4).

## 3. Vorab-Test „Erstellt“ (E), vor F1, etwa 2 Minuten
**Warum:** Paket F liest die SharePoint-Spalte „Erstellt“ (intern `Created`).
- Im Export steht sie mit dem Anzeigenamen „Erstellt“, lesbar und filterbar (**belegt**).
- Ob Studio den Namen `Erstellt` annimmt, ist **UNSICHER** (U1).
- Ob die Spalte in Collections mitkommt, ist ebenfalls **UNSICHER** (U7, explizite Spaltenauswahl).

**Test 1 (Name):**
1. Auf `Screen1` vorübergehend eine Textbeschriftung `lblTestErstellt` einfügen.
2. `Text`:
```
"Erstellt: " & Text(First(Tischbuchungen).Erstellt; "dd.mm.yyyy hh:mm")
```
- Erwartung: ein Datum, kein roter Fehler. Ein gelbes Delegations-Dreieck ist hier egal.

**Test 2 (Spalte in einer Collection):**
1. Vorübergehend eine Schaltfläche `btnTestErstellt` einfügen.
2. `OnSelect`:
```
ClearCollect(colTestErstellt; Filter(Tischbuchungen; Endzeit > DateAdd(Now(); -1; TimeUnit.Days)));; Notify(CountRows(colTestErstellt) & " Zeilen, Erstellt der ersten: " & Text(First(colTestErstellt).Erstellt; "dd.mm.yyyy hh:mm"); NotificationType.Information)
```
3. In der Vorschau klicken. Erwartung: „… Zeilen, Erstellt der ersten: 07.10.2026 …“ mit Datum.

**Nur aussagekräftig, wenn mindestens 1 Zeile** geladen wird. Bei 0 Zeilen fehlt das Datum immer: dann `-1` durch `-14` ersetzen. Das Datum „07.10.“ ist nur ein Beispiel.

**Danach beide Steuerelemente löschen.**

**Wenn Test 1 rot ist:**
1. Im Test `Erstellt` durch `Created` ersetzen.
2. Geht es dann, an Claude Code melden „Spalte heißt Created“. Paket F wird mit `Created` neu erzeugt (etwa 15 Minuten).
3. **Nicht** selbst in den Blöcken ersetzen: Ein Teil der Namen ist ein eigener Feldname und muss bleiben.

**Wenn Test 2 kein Datum zeigt** (leer): melden. Dann verliert nur „spät gebucht“ die Schonfrist (U7). Paket F kann trotzdem eingefügt werden.

## 4. Schritte

### F1 App-Start: Einstellung, Check-in-Frage beim Öffnen

**Was neu ist:**
- `Set(varFreigabeMinuten; 30)` (die eine Zahl zum Ändern), `varCheckinGefragtID` und `varAuscheckFrageID` vorbelegt.
- Vor der Ladezeile: Check-in-Frage beim Öffnen.
- Die Ladezeile lädt `Erstellt` mit und lässt verfallene Buchungen weg.

**Danach:** in der Strukturansicht `App` → … → **OnStart ausführen**.
**Test:** App-Prüfung ohne rote Fehler. Eigene Buchung „jetzt bis +1 Std“ (vorher angelegt, nicht eingecheckt) → OnStart ausführen → Check-in-Dialog erscheint.

#### `App.OnStart`

Ort: `App` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G1

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,2 +1,5 @@
+Set(varFreigabeMinuten; 30);;
+Set(varCheckinGefragtID; 0);;
+Set(varAuscheckFrageID; 0);;
 Set(varSperreBis; Now());;
 Set(varVerlGrenze; Now());;
@@ -104,3 +107,13 @@
 Set(varIsLoading; false);;
 Set(varSpinnerWinkel; 0);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+ClearCollect(colCheckinFrage; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes) && Endzeit > Now()));;
+RemoveIf(colCheckinFrage; CheckedIn || (Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+If(
+  !IsEmpty(colCheckinFrage);
+  Set(varCheckinGefragtID; First(SortByColumns(colCheckinFrage; "Startzeit"; SortOrder.Ascending)).ID);;
+  Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinGefragtID));;
+  Set(varZeigeCheckin; true)
+);;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block zum Einfügen:

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

**Rückfall F1:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F2 Stornieren direkt und sicher (ohne Rückfrage-Dialog)

**Was neu ist (A):**
- Alle drei Knöpfe stornieren **direkt**, wie heute, aber sicher:
  - Zweifach-Sperre gegen Doppelklick.
  - Buchung frisch per `LookUp` lesen.
  - **Nur eigene** (`Lower(varStornoBuchung.Person.Email) <> Lower(User().Email)` → „Nur eigene Buchungen können storniert werden.“).
  - `Remove` in `IfError`, danach nachlesen, ob die Zeile weg ist, und eine ehrliche Meldung.
  - Ladezeile mit Freigabe-Regel.
- `DisplayMode`: grau, solange gespeichert wird.
- **Warum es ohne Rückfrage sicher ist:** Der Fehler aus G4 entstand, weil **zwischen** Frage und „Ja“ eine Variable wechseln konnte. Ohne Rückfrage gibt es dieses Zeitfenster nicht. Die Buchung wird beim Klick gelesen.
- **Mehrfach-Stornieren:** gleicher Ablauf wie heute (eine Abfrage der eigenen Buchungen, **ein** `Remove` mit allen Zielen, `Refresh`, Ladezeile). Neu sind nur Sperre und Freigabe-Ladezeile. Gleiche Zahl an Abfragen (**geschlussfolgert** aus den Formeln, gemessen sind 33 in ca. 9 s mit dem heutigen Ablauf).

**Test:**
- Dashboard → Verwalten → Stornieren → „Buchung storniert.“, Zeile in SharePoint weg.
- Doppelklick → eine Meldung.
- Tab „Buchungen“ → Verwalten → Stornieren → ebenso.
- Mehrfachauswahl mit 5 Buchungen → „5 Buchungen storniert.“ (Zeit grob vergleichen).

#### `btnStornieren.OnSelect`

Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,2 +1,27 @@
-Remove(Tischbuchungen; varSelectedBuchung);; Set(varZeigeVerwalten; false);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+If(
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
+  If(
+    IsBlank(varStornoBuchung.ID);
+    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+    Set(varZeigeVerwalten; false);
+    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+    IfError(
+      Remove(Tischbuchungen; varStornoBuchung);
+      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+      If(
+        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+        Notify("Buchung storniert."; NotificationType.Success);;
+        Set(varZeigeVerwalten; false);
+        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+      )
+    )
+  );;
+  Refresh(Tischbuchungen);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block zum Einfügen:

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

#### `btnStornieren.DisplayMode`

Ort: `Screen1 > conVerwaltenDialog > btnStornieren` · **neu setzen**

Vollständiger Block zum Einfügen:

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

#### `btnStornieren_1.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,11 +1,27 @@
-Set(varIsLoading; true);;
 If(
-  IsBlank(varSelectedBuchungTab);
-  Notify("Keine Buchung ausgewählt."; NotificationType.Warning);
-  Remove(Tischbuchungen; varSelectedBuchungTab);;
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
+  If(
+    IsBlank(varStornoBuchung.ID);
+    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+    Set(varZeigeVerwaltenTab; false);
+    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+    IfError(
+      Remove(Tischbuchungen; varStornoBuchung);
+      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+      If(
+        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+        Notify("Buchung storniert."; NotificationType.Success);;
+        Set(varZeigeVerwaltenTab; false);
+        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+      )
+    )
+  );;
   Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
-  Notify("Buchung storniert."; NotificationType.Success)
-);;
-Set(varZeigeVerwaltenTab; false);;
-Set(varIsLoading; false)
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block zum Einfügen:

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

#### `btnStornieren_1.DisplayMode`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1` · **neu setzen**

Vollständiger Block zum Einfügen:

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

#### `btnStornierenKlein.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,36 +1,41 @@
-Set(varIsLoading; true);;
-ClearCollect(
-    colStornoFrisch;
-    Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
-);;
-ClearCollect(
-    colStornoZiele;
-    Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
-);;
 If(
-    CountRows(colAusgewaehlteBuchungen) = 0;
-    Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
-    If(
-        CountRows(colStornoZiele) = 0;
-        Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
-        IfError(
-            Remove(Tischbuchungen; colStornoZiele);
-            Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
-            If(
-                CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
-                Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
-                Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
-            )
-        )
-    )
-);;
-Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
-Clear(colStornoFrisch);;
-Clear(colStornoZiele);;
-Clear(colAusgewaehlteBuchungen);;
-Set(varGeklickteBuchungKlein; Blank());;
-Set(varZeigeVerwaltenKlein; false);;
-Set(varAuswahlModusAktiv; false);;
-Reset(tglAuswahlModus);;
-Set(varIsLoading; false)
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  ClearCollect(
+      colStornoFrisch;
+      Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
+  );;
+  ClearCollect(
+      colStornoZiele;
+      Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
+  );;
+  If(
+      CountRows(colAusgewaehlteBuchungen) = 0;
+      Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
+      If(
+          CountRows(colStornoZiele) = 0;
+          Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
+          IfError(
+              Remove(Tischbuchungen; colStornoZiele);
+              Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
+              If(
+                  CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
+                  Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
+                  Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
+              )
+          )
+      )
+  );;
+  Refresh(Tischbuchungen);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
+  Clear(colStornoFrisch);;
+  Clear(colStornoZiele);;
+  Clear(colAusgewaehlteBuchungen);;
+  Set(varGeklickteBuchungKlein; Blank());;
+  Set(varZeigeVerwaltenKlein; false);;
+  Set(varAuswahlModusAktiv; false);;
+  Reset(tglAuswahlModus);;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block zum Einfügen:

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

#### `btnStornierenKlein.DisplayMode`

Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein` · **neu setzen**

Vollständiger Block zum Einfügen:

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Rückfall F2:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F3 Grundriss: verfallene Buchungen als frei

**Was neu ist:**
- **Kachel-Klick:** holt die Buchungen des Tisches, entfernt verfallene, öffnet den Buchungsdialog, wenn nichts übrig ist.
- **Sechs reine Ladestellen** (Stockwerk, Datum, vier Aktualisieren-Symbole): `Set(varFreigabeGrenze; …)` davor, `Erstellt` mitladen, verfallene nicht in `colGrundriss`. Die Spalten von `colGrundriss` bleiben gleich (`DropColumns`).

**Test:** Testzeile in SharePoint anlegen (Beginn vor 1 Std, CheckedIn = Nein). Nach `varFreigabeMinuten` (Testmodus siehe Testbogen) → Aktualisieren → Kachel grün, Klick öffnet den Buchungsdialog.

#### `btnHitArea.OnSelect`

Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G7

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -2,40 +2,38 @@
   ThisItem.Gesperrt;
   Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
-  With(
-    {
-      relevanteBuchung:
-        If(
-          varAnsichtsDatum = Today();
-          LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes));
-          LookUp(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
-        )
-    };
-    If(
-      IsBlank(relevanteBuchung);
-        Set(varSelectedTisch; ThisItem);;
-        Set(varDialogJetzt; Now());;
-        Reset(dpDatum);;
-        Reset(ddStart);;
-        Reset(ddEnde);;
-        Reset(dpWiederholenBis);;
-        Set(varZeigeDialog; true);;
-        Set(varZeigeDetails; false);;
-        Set(varZeigeCheckin; false);;
-        Set(varZeigeVerwalten; false);;
-        Set(varWiederholen; false);;
-        Set(varWiederholenModus; "Wochentage");;
-        Set(varTagMo; false);;
-        Set(varTagDi; false);;
-        Set(varTagMi; false);;
-        Set(varTagDo; false);;
-        Set(varTagFr; false);;
-        Set(varTagSa; false);;
-        Set(varTagSo; false);
-        Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; relevanteBuchung);;
-        Set(varZeigeDetails; true);;
-        Set(varZeigeDialog; false);;
-        Set(varZeigeCheckin; false);;
-        Set(varZeigeVerwalten; false)
-    )
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  If(
+    varAnsichtsDatum = Today();
+    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes)));
+    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)))
+  );;
+  RemoveIf(colKachel; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+  Set(varKachelID; First(SortByColumns(colKachel; "Startzeit"; SortOrder.Ascending)).ID);;
+  If(
+    IsBlank(varKachelID);
+      Set(varSelectedTisch; ThisItem);;
+      Set(varDialogJetzt; Now());;
+      Reset(dpDatum);;
+      Reset(ddStart);;
+      Reset(ddEnde);;
+      Reset(dpWiederholenBis);;
+      Set(varZeigeDialog; true);;
+      Set(varZeigeDetails; false);;
+      Set(varZeigeCheckin; false);;
+      Set(varZeigeVerwalten; false);;
+      Set(varWiederholen; false);;
+      Set(varWiederholenModus; "Wochentage");;
+      Set(varTagMo; false);;
+      Set(varTagDi; false);;
+      Set(varTagMi; false);;
+      Set(varTagDo; false);;
+      Set(varTagFr; false);;
+      Set(varTagSa; false);;
+      Set(varTagSo; false);
+      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varKachelID));;
+      Set(varZeigeDetails; true);;
+      Set(varZeigeDialog; false);;
+      Set(varZeigeCheckin; false);;
+      Set(varZeigeVerwalten; false)
   )
 )
```

Vollständiger Block zum Einfügen:

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  If(
    varAnsichtsDatum = Today();
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes)));
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)))
  );;
  RemoveIf(colKachel; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varKachelID; First(SortByColumns(colKachel; "Startzeit"; SortOrder.Ascending)).ID);;
  If(
    IsBlank(varKachelID);
      Set(varSelectedTisch; ThisItem);;
      Set(varDialogJetzt; Now());;
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
      Set(varDetailsTisch; ThisItem);; Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varKachelID));;
      Set(varZeigeDetails; true);;
      Set(varZeigeDialog; false);;
      Set(varZeigeCheckin; false);;
      Set(varZeigeVerwalten; false)
  )
)
```

#### `ddStockwerk.OnChange`

Ort: `Screen1 > conGrundriss > ddStockwerk` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,3 +1,4 @@
 Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
 Set(varStockwerkDropdownOffen; false);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block zum Einfügen:

```
Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
Set(varStockwerkDropdownOffen; false);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

#### `dpAnsichtsDatum.OnChange`

Ort: `Screen1 > conDashboard > dpAnsichtsDatum` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,2 +1,3 @@
 Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

Vollständiger Block zum Einfügen:

```
Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
```

#### `Icon1_1.OnSelect`

Ort: `Screen1 > conDashboard > Icon1_1` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G12

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,4 +1,5 @@
 Set(varIsLoading; true);;
 Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
 Set(varIsLoading; false)
```

Vollständiger Block zum Einfügen:

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

#### `Icon1.OnSelect`

Ort: `Screen1 > conBuchungen > Icon1` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G12

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,4 +1,5 @@
 Set(varIsLoading; true);;
 Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
 Set(varIsLoading; false)
```

Vollständiger Block zum Einfügen:

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

#### `Image6.OnSelect`

Ort: `Screen1 > conHeader > Image6` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G12

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,4 +1,5 @@
 Set(varIsLoading; true);;
 Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
 Set(varIsLoading; false)
```

Vollständiger Block zum Einfügen:

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

#### `btnHitArea_1.OnSelect`

Ort: `Screen1 > conHeader > btnHitArea_1` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G12

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,4 +1,5 @@
 Set(varIsLoading; true);;
 Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
 Set(varIsLoading; false)
```

Vollständiger Block zum Einfügen:

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**Rückfall F3:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F4 Buchen: verfallene Buchungen blockieren nicht (mit Nachtrag 4)

**Was neu ist (gegenüber G6 aus Nachtrag 4):**
- `Set(varFreigabeGrenze; …)`.
- Nach den Vorprüfungen `RemoveIf(…verfallen…)`.
- In der Nachlese werden verfallene **fremde** Buchungen ignoriert.
- Die Erfolgsmeldung nennt die Minuten.
- Ladezeile mit Freigabe-Regel.
- **Nachtrag 4 bleibt** (kein Refresh).

**Test:** Auf einen Tisch mit verfallener Buchung buchen → „Gebucht …“, keine Warnung. Nachtrag-4-Test 2: die neue Buchung erscheint ohne Aktualisieren in der Liste.

#### `btnSpeichern.OnSelect`

Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G6 (Fassung Nachtrag 4)

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -11,4 +11,5 @@
   Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
   Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   ClearCollect(
     colNeuTermine;
@@ -40,5 +41,7 @@
     Set(varNeuGesamt; CountRows(colNeuTermine));;
     ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
+    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
     ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
+    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
     ClearCollect(
       colNeuErgebnis;
@@ -98,4 +101,5 @@
       Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
       ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
+      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
       Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
       Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
@@ -106,5 +110,5 @@
         Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
         varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
-        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
+        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
         Notify(
           varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
@@ -130,5 +134,6 @@
       )
     );;
-    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
   );;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block zum Einfügen:

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

#### `btnSpeichernTischePanel.OnSelect`

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G6 (Fassung Nachtrag 4)

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -11,4 +11,5 @@
   Set(varNeuBis; If(varNeuBisRoh > varNeuDatum + 14; varNeuDatum + 14; varNeuBisRoh));;
   Set(varNeuJetzt; DateAdd(Today(); 30 * RoundDown((Hour(Now()) * 60 + Minute(Now())) / 30; 0); TimeUnit.Minutes));;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   ClearCollect(
     colNeuTermine;
@@ -40,5 +41,7 @@
     Set(varNeuGesamt; CountRows(colNeuTermine));;
     ClearCollect(colNeuBelegt; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
+    RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
     ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
+    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
     ClearCollect(
       colNeuErgebnis;
@@ -98,4 +101,5 @@
       Set(varNeuNachVon; DateAdd(varNeuSpanStart; -(Hour(Now()) * 3600 + Minute(Now()) * 60 + Second(Now()) + 1); TimeUnit.Seconds));;
       ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuNachVon));;
+      RemoveIf(colNeuNachlese; SerienID <> varSerienID && !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
       Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
       Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
@@ -106,5 +110,5 @@
         Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
         varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
-        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis 30 Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
+        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
         Notify(
           varNeuAnzahl & " von " & varNeuGesamt & " Terminen gebucht (" & varNeuTischTitel & ")." &
@@ -138,5 +142,6 @@
       )
     );;
-    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))))
   );;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block zum Einfügen:

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

**Rückfall F4:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F5 Panel „Tisch buchen“: Liste und 5/9-Std.-Knöpfe

**Was neu ist:**
- `btnTischHinzufügen`: setzt `varFreigabeGrenze` beim Öffnen.
- `ddTischePanel.Items`: jede Buchung bekommt `Aktiv`, gezählt werden nur aktive.
- 5/9-Std.-Knöpfe: gleiche Prüfung, nur aktive Buchungen.

**Test:** Panel, heute, Zeit der verfallenen Testbuchung → Tisch ohne „(an … belegt)“, 5 Std wählbar.

#### `btnTischHinzufügen.OnSelect`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G7

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -21,4 +21,5 @@
 Set(varEndeOverridePanel; "");;
 Set(varPanelJetzt; Now());;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
 Reset(ddStartTischePanel);;
 Reset(ddEndTischePanel);;
```

Vollständiger Block zum Einfügen:

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
Set(varPanelJetzt; Now());;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

#### `ddTischePanel.Items`

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G9

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -27,7 +27,7 @@
                 Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(varWiederholen && dpWiederholenBis_1.SelectedDate > dpDatumTischePanel.SelectedDate; Min(DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days); 14); 0) + 1; TimeUnit.Days) && Endzeit > dpDatumTischePanel.SelectedDate
               );
-              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit}
+              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit; Aktiv: CheckedIn || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze}
             );
-            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now()}); 0)
+            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now(); Aktiv: true}); 0)
           )
         };
@@ -37,5 +37,5 @@
               Tische As Ti;
               With(
-                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
+                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; Aktiv && TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
                 {
                   Titel: Ti.Titel;
```

Vollständiger Block zum Einfügen:

```
With(
  {
    datum: dpDatumTischePanel.SelectedDate;
    startZeit: Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    endeZeit: Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    bisRoh: If(varWiederholen; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate)
  };
  With(
    { bis: If(bisRoh > datum + 14; datum + 14; bisRoh) };
    With(
      {
        termine: ForAll(
          Filter(
            ForAll(Sequence(If(bis < datum; 0; DateDiff(datum; bis; TimeUnit.Days) + 1); 0); DateAdd(datum; Value; TimeUnit.Days)) As D;
            !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
          ) As T;
          {Start: T.Value + startZeit; Ende: T.Value + endeZeit}
        )
      };
      With(
        {
          belegtListe: If(
            varZeigeTischBuchungForm;
            ForAll(
              Filter(
                Tischbuchungen;
                Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(varWiederholen && dpWiederholenBis_1.SelectedDate > dpDatumTischePanel.SelectedDate; Min(DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days); 14); 0) + 1; TimeUnit.Days) && Endzeit > dpDatumTischePanel.SelectedDate
              );
              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit; Aktiv: CheckedIn || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze}
            );
            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now(); Aktiv: true}); 0)
          )
        };
        SortByColumns(
          Filter(
            ForAll(
              Tische As Ti;
              With(
                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; Aktiv && TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
                {
                  Titel: Ti.Titel;
                  Gesperrt: Ti.Gesperrt;
                  ID: Ti.ID;
                  Belegt: n;
                  Etage: If(Ti.Geschoss.Value = varAusgewaehltesStockwerk; 0; 1);
                  Schluessel: Ti.Geschoss.Value & Left(Ti.Titel; Len(Ti.Titel) - Len(Last(Split(Ti.Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Ti.Titel; " ")).Value); 0); "000");
                  Anzeige: Ti.Titel & If(n = 0; ""; "  (an " & n & " von " & CountRows(termine) & " Tagen belegt)")
                }
              )
            );
            !Gesperrt && !("big table" in Lower(Titel)) && (Belegt = 0 || Belegt < CountRows(termine))
          );
          "Belegt"; SortOrder.Ascending;
          "Etage"; SortOrder.Ascending;
          "Schluessel"; SortOrder.Ascending
        )
      )
    )
  )
)
```

#### `btn5Std.DisplayMode`

Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G10

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -14,5 +14,5 @@
         DisplayMode.Edit;
         If(
-          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
+          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
           DisplayMode.Edit;
           DisplayMode.Disabled
```

Vollständiger Block zum Einfügen:

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

#### `btn5Std.Fill`

Ort: `Screen1 > conTischBuchungenPanel > btn5Std` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G10

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -17,5 +17,5 @@
           ColorFade(ColorValue("#00A96B"); 70%);
           If(
-            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
+            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
             ColorFade(ColorValue("#00A96B"); 70%);
             ColorFade(ColorValue("#EB3951"); 70%)
```

Vollständiger Block zum Einfügen:

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

#### `btn9Std.DisplayMode`

Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G10

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -14,5 +14,5 @@
         DisplayMode.Edit;
         If(
-          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
+          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
           DisplayMode.Edit;
           DisplayMode.Disabled
```

Vollständiger Block zum Einfügen:

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

#### `btn9Std.Fill`

Ort: `Screen1 > conTischBuchungenPanel > btn9Std` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G10

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -17,5 +17,5 @@
           ColorFade(ColorValue("#00A96B"); 70%);
           If(
-            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
+            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
             ColorFade(ColorValue("#00A96B"); 70%);
             ColorFade(ColorValue("#EB3951"); 70%)
```

Vollständiger Block zum Einfügen:

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 9;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsEmpty(Filter(ForAll(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)) As X; {Aktiv: X.CheckedIn || X.Startzeit > varFreigabeGrenze || X.Erstellt > varFreigabeGrenze}); Aktiv));
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**Rückfall F5:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F6 Verlängern: verfallene blockieren nicht, keine zwei Tische

**Was neu ist:**
- Verwalten-Dialoge: die Grenze für die Dauer-Knöpfe ohne verfallene Buchungen. `varVerlNaechste` kommt jetzt aus einer Collection: Ein roter Zwischenfehler nach `btnVerwalten` verschwindet nach `btnVerwalten_2`.
- Verlängern: Kollision ohne verfallene. **Neu:** „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“
- Eigene verfallene Buchung: „Diese Buchung ist verfallen …“.

**Test:** +1 Std über eine verfallene fremde Buchung geht. Eigene Buchung in eine zweite eigene hinein verlängern → Meldung.

#### `btnVerwalten.OnSelect`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G2

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -3,5 +3,8 @@
 Set(varVerlEndeAlt; ThisItem.Endzeit);;
 Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
-Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
+Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
+RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
 Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
 Set(varAusgewaehltePlusDauer; Blank());;
```

Vollständiger Block zum Einfügen:

```
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

#### `btnVerwalten_2.OnSelect`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G2

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -7,5 +7,8 @@
   Set(varVerlEndeAlt; ThisItem.Endzeit);;
   Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
-  Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
+  RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+  Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
   Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
   Set(varAusgewaehltePlusDauer; Blank());;
```

Vollständiger Block zum Einfügen:

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  ClearCollect(colVerlNaechste; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende));;
  RemoveIf(colVerlNaechste; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varVerlNaechste; First(Sort(colVerlNaechste; Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

#### `btnVerlängern.OnSelect`

Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G3

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -2,4 +2,5 @@
   !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
   Set(varIsLoading; true);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
   If(
@@ -13,10 +14,18 @@
     Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
     Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
+    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
+    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
+      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
+      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
       varVerlEndeNeu <= varVerlBuchung.Startzeit;
       Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
       varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
+      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
       Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
       Set(varVerlGrenze; varVerlEndeAlt);
@@ -35,5 +44,6 @@
   );;
   Refresh(Tischbuchungen);;
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
   Set(varAusgewaehltePlusDauer; Blank());;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block zum Einfügen:

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

#### `btnVerlängern_1.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1` · **ganze Property ersetzen** · im Studio jetzt: Gesamtplan G3

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -2,4 +2,5 @@
   !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
   Set(varIsLoading; true);;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
   Set(varVerlBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
   If(
@@ -13,10 +14,18 @@
     Set(varVerlEndeNeu; DateAdd(varVerlBuchung.Endzeit; varAusgewaehltePlusDauer; TimeUnit.Minutes));;
     Set(varVerlTagesende; DateAdd(varVerlBuchung.Startzeit; 22 * 60 - (Hour(varVerlBuchung.Startzeit) * 60 + Minute(varVerlBuchung.Startzeit)); TimeUnit.Minutes));;
+    ClearCollect(colVerlKonflikt; Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
+    RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
+      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
+      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
       varVerlEndeNeu <= varVerlBuchung.Startzeit;
       Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
       varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
+      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
       Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
       Set(varVerlGrenzeTab; varVerlEndeAlt);
@@ -35,5 +44,6 @@
   );;
   Refresh(Tischbuchungen);;
-  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
   Set(varAusgewaehltePlusDauer; Blank());;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block zum Einfügen:

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

**Rückfall F6:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F7 Einchecken bis Frist, Auschecken mit zweitem Tippen

**Was neu ist (ersetzt G5):**
- Einchecken nur von 30 Min vor Beginn bis zur Frist. Davor und danach wird frisch geprüft, ob der Tisch schon an jemand anderen vergeben ist.
- **Auschecken nach Beginn mit zweitem Tippen (Frage 1):**
  - Erstes Tippen: Meldung „Zum Auschecken bitte noch einmal tippen …“, und der Knopf heißt „Wirklich auschecken?“.
  - Zweites Tippen (nach mindestens 1 Sekunde): Ende = jetzt (nächste Minute).
  - Der erste Tipp schreibt nichts und sperrt für 1 Sekunde. Ein **Doppelklick** bestätigt also nicht.
  - Die Frage wird erst **hinter** der Sperre zurückgesetzt, ein geschlucktes Tippen verliert sie nicht.
  - **Abgleich mit dem frischen Stand:** Wurde die Buchung inzwischen anderswo ein- oder ausgecheckt (z. B. Handy), passiert nichts. Es kommt nur die Meldung „Der Status hat sich inzwischen geändert …“, und die Anzeige wird aktualisiert.
  - Beim Öffnen des Dialogs wird die Frage zurückgesetzt (`btnEincheckenHeute`).
  - Vor dem Beginn nimmt Auschecken wie bisher nur den Check-in zurück.
- `btnEinchecken.DisplayMode` aus G5.
- Dashboard-Status „Verfallen“ (grau).
- Meldungen versprechen nicht mehr „frei“, sondern „andere können den Tisch wieder buchen“ (Frage 2).

**Test:**
- Buchung in 1 Std → „erst ab 30 Minuten vor Beginn“.
- Laufende Buchung → „Eingecheckt.“.
- Auschecken → erstes Tippen: Meldung, Knopftext ändert sich. **Doppelklick** → nur die Meldung, nicht ausgecheckt. Zweites Tippen nach 1–2 s → „Ausgecheckt. Deine Buchung endet um …“.
- Statusabgleich: Buchung im PC-Dashboard offen lassen, in SharePoint `CheckedIn` umstellen, dann tippen → „Der Status hat sich inzwischen geändert …“, nichts geschrieben.
- Dialog schließen und wieder öffnen → Knopf heißt wieder „Auschecken“.
- Verfallene Buchung → „Zu spät …“, Status grau.

#### `btnEinchecken.OnSelect`

Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1,6 +1,87 @@
-With(
-  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
-  Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {CheckedIn: !aktuelleBuchung.CheckedIn}))
-);;
-Set(varZeigeCheckin; false);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+If(
+  varSelectedBuchung.CheckedIn && Now() >= varSelectedBuchung.Startzeit && varAuscheckFrageID <> varSelectedBuchung.ID;
+  Set(varAuscheckFrageID; varSelectedBuchung.ID);;
+  Set(varSperreBis; DateAdd(Now(); 1; TimeUnit.Seconds));;
+  Notify("Zum Auschecken bitte noch einmal tippen. Deine Buchung endet dann jetzt."; NotificationType.Information);
+  If(
+    !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+    Set(varIsLoading; true);;
+    Set(varAuscheckFrageID; 0);;
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
+    Set(varCheckinTisch; varCheckinBuchung.Tisch.Value);;
+    Set(varCheckinStart; varCheckinBuchung.Startzeit);;
+    Set(varCheckinEnde; varCheckinBuchung.Endzeit);;
+    If(
+      IsBlank(varCheckinBuchung.ID);
+      Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);;
+      Set(varZeigeCheckin; false);
+      Coalesce(varCheckinBuchung.CheckedIn; false) <> Coalesce(varSelectedBuchung.CheckedIn; false);
+      Set(varSelectedBuchung; varCheckinBuchung);;
+      Notify("Der Status hat sich inzwischen geändert. Bitte noch einmal prüfen und tippen."; NotificationType.Information);
+      varCheckinBuchung.CheckedIn && Now() < varCheckinStart;
+      IfError(
+        Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: false});
+        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
+        If(
+          !varSelectedBuchung.CheckedIn;
+          Notify("Ausgecheckt. Die Buchung bleibt bestehen, bitte zum Beginn wieder einchecken."; NotificationType.Success);;
+          Set(varZeigeCheckin; false);
+          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
+        )
+      );
+      varCheckinBuchung.CheckedIn && DateAdd(Now(); 1; TimeUnit.Minutes) >= varCheckinEnde;
+      Notify("Die Buchung endet ohnehin jetzt."; NotificationType.Information);;
+      Set(varZeigeCheckin; false);
+      varCheckinBuchung.CheckedIn;
+      Set(varCheckinNeuesEnde; DateAdd(Today(); Hour(Now()) * 60 + Minute(Now()) + 1; TimeUnit.Minutes));;
+      IfError(
+        Patch(Tischbuchungen; varCheckinBuchung; {Endzeit: varCheckinNeuesEnde});
+        Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+        Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
+        If(
+          varSelectedBuchung.Endzeit < varCheckinEnde;
+          Notify("Ausgecheckt. Deine Buchung endet um " & Text(varSelectedBuchung.Endzeit; "hh:mm") & " Uhr. Andere können den Tisch wieder buchen."; NotificationType.Success);;
+          Set(varZeigeCheckin; false);
+          Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
+        )
+      );
+      Now() < DateAdd(varCheckinStart; -30; TimeUnit.Minutes);
+      Notify("Einchecken ist erst ab 30 Minuten vor Beginn möglich."; NotificationType.Warning);
+      Now() >= varCheckinEnde;
+      Notify("Diese Buchung ist schon zu Ende."; NotificationType.Warning);;
+      Set(varZeigeCheckin; false);
+      varCheckinStart <= varFreigabeGrenze && varCheckinBuchung.Erstellt <= varFreigabeGrenze;
+      Notify("Zu spät: Ohne Check-in bis " & Coalesce(varFreigabeMinuten; 30) & " Minuten nach Beginn verfällt die Buchung. Bitte neu buchen."; NotificationType.Warning);;
+      Set(varZeigeCheckin; false);
+      ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
+      RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+      If(
+        !IsEmpty(colCheckinAndere);
+        Notify("Der Tisch ist in dieser Zeit schon an jemand anderen vergeben. Bitte neu buchen."; NotificationType.Error);;
+        Set(varZeigeCheckin; false);
+        IfError(
+          Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: true});
+          Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+          Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
+          ClearCollect(colCheckinAndere; Filter(Tischbuchungen; Tisch.Value = varCheckinTisch && Startzeit < varCheckinEnde && Endzeit > varCheckinStart));;
+          RemoveIf(colCheckinAndere; ID = varCheckinBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+          If(
+            varSelectedBuchung.CheckedIn && !IsEmpty(colCheckinAndere);
+            Notify("Eingecheckt, aber der Tisch wurde gleichzeitig an jemand anderen vergeben. Bitte unter Buchungen prüfen und klären."; NotificationType.Error);;
+            Set(varZeigeCheckin; false);
+            varSelectedBuchung.CheckedIn;
+            Notify("Eingecheckt."; NotificationType.Success);;
+            Set(varZeigeCheckin; false);
+            Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
+          )
+        )
+      )
+    );;
+    Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
+    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt))));;
+    Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+    Set(varIsLoading; false)
+  )
+)
```

Vollständiger Block zum Einfügen:

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

#### `btnEinchecken.DisplayMode`

Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **neu setzen**

Vollständiger Block zum Einfügen:

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

#### `btnEinchecken.Text`

Ort: `Screen1 > conCheckinDialog > btnEinchecken` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(varSelectedBuchung.CheckedIn; "Auschecken"; "Einchecken")
+If(varSelectedBuchung.CheckedIn; If(varAuscheckFrageID = varSelectedBuchung.ID; "Wirklich auschecken?"; "Auschecken"); "Einchecken")
```

Vollständiger Block zum Einfügen:

```
If(varSelectedBuchung.CheckedIn; If(varAuscheckFrageID = varSelectedBuchung.ID; "Wirklich auschecken?"; "Auschecken"); "Einchecken")
```

#### `btnEincheckenHeute.OnSelect`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Set(varSelectedBuchung; ThisItem);; Set(varZeigeCheckin; true);; Set(varZeigeDetails; false);; Set(varZeigeDialog; false);; Set(varZeigeVerwalten; false)
+Set(varAuscheckFrageID; 0);; Set(varSelectedBuchung; ThisItem);; Set(varZeigeCheckin; true);; Set(varZeigeDetails; false);; Set(varZeigeDialog; false);; Set(varZeigeVerwalten; false)
```

Vollständiger Block zum Einfügen:

```
Set(varAuscheckFrageID; 0);; Set(varSelectedBuchung; ThisItem);; Set(varZeigeCheckin; true);; Set(varZeigeDetails; false);; Set(varZeigeDialog; false);; Set(varZeigeVerwalten; false)
```

#### `lblStatusHeute.Text`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; "Eingecheckt"; "Einchecken")
+If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; "Verfallen"; "Einchecken")
```

Vollständiger Block zum Einfügen:

```
If(ThisItem.CheckedIn; "Eingecheckt"; ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; "Verfallen"; "Einchecken")
```

#### `lblStatusHeute.Color`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **ganze Property ersetzen** · im Studio jetzt: Export 07.10.

Änderungen gegenüber dem Studio (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-If(ThisItem.CheckedIn; ColorValue("#00A96B"); ColorValue("#FFA500"))
+If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

Vollständiger Block zum Einfügen:

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ThisItem.Startzeit <= varFreigabeGrenze && ThisItem.Erstellt <= varFreigabeGrenze; ColorValue("#A6A6A6"); ColorValue("#FFA500"))
```

**Rückfall F7:** die Fassungen aus Anhang A wieder einsetzen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

### F8 Timer anlegen: automatisch aktualisieren und an Check-in erinnern (ersetzt G8)

**Was neu ist (ersetzt G8, B):**
- `tmrAktualisieren` neu anlegen (5 Properties).
- `OnTimerEnd`: alle 5 Min aktualisieren, wenn kein Dialog offen ist. Wie G8, aber **ohne** `varZeigeStornoFrage`.
- Ladezeile mit Freigabe-Regel.
- **Check-in-Erinnerung:**
  - Nur wenn das Dashboard für heute offen ist **und** der Grundriss (`colGrundriss`, lokal, ohne Abfrage) eine nicht eingecheckte Buchung unter deinem Namen zeigt, die in 30 Min beginnt oder läuft.
  - Erst dann **eine** Abfrage der eigenen Buchungen. Gefragt wird einmal je Buchung.

**Anlegen:** `Screen1` markieren → Einfügen → Eingabe → Timer → umbenennen in `tmrAktualisieren`.
**Test:** App 5 Min offen lassen, in einem zweiten Fenster eine Buchung ändern → spätestens nach 5 Min sichtbar. Eigene Buchung mit Beginn in 20 Min → Check-in-Dialog nach höchstens 5 Min, nur einmal.

Neues Steuerelement (zuerst anlegen, Name exakt so): `tmrAktualisieren` (Timer (Einfügen → Eingabe → Timer), auf oberster Ebene einfügen (nicht in einen Container))

#### `tmrAktualisieren.Duration`

Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen**

Vollständiger Block zum Einfügen:

```
300000
```

#### `tmrAktualisieren.Repeat`

Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen**

Vollständiger Block zum Einfügen:

```
true
```

#### `tmrAktualisieren.AutoStart`

Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen**

Vollständiger Block zum Einfügen:

```
true
```

#### `tmrAktualisieren.Visible`

Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen**

Vollständiger Block zum Einfügen:

```
false
```

#### `tmrAktualisieren.OnTimerEnd`

Ort: `(neu) Screen1 > tmrAktualisieren` · **neu setzen**

Vollständiger Block zum Einfügen:

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

**Rückfall F8:** die Fassungen aus Anhang A wieder einsetzen, neues Steuerelement löschen. Neu gesetzte `DisplayMode` auf `DisplayMode.Edit` zurück.

**Rückfall des ganzen Pakets:** in **umgekehrter** Reihenfolge F8 → F1 (Anhang A). F1 zuletzt, weil alle anderen `varFreigabeMinuten` lesen. Wer nur F1 zurücknimmt, bekommt rote Fehler in F2–F8.

## 5. Antworten auf die Fragen
**1. Bestätigung beim Auschecken:** Ja, jetzt per **zweitem Tippen** auf denselben Knopf, ohne neues Steuerelement (F7). Begründung: Auschecken nach Beginn beendet die Buchung, und neu buchen geht erst ab der nächsten halben Stunde. Ein versehentlicher Klick kostet also den Tisch.

**2. „Sofort frei“:** Das ist korrigiert, in den App-Meldungen (F7) und in `KURZANLEITUNG_und_GoLive_Mail_v3.md` / `BETRIEBSHANDBUCH_Michael_v3.md`. Die Formulierung ist jetzt: „andere können den Tisch wieder buchen“. Der Grundriss zeigt das bei anderen nach dem nächsten Laden, **meist innerhalb von 5 Minuten**: Der Timer lädt nur, wenn bei ihnen kein Dialog offen ist. Buchbar ist der Tisch ab der nächsten halben Stunde.

**3. Zusätzliche Abfragen** (**geschlussfolgert** aus den Formeln, im Monitor prüfbar):

| Stelle | zusätzlich | Häufigkeit |
|---|---|---|
| F1 App-Start | +1 (eigene anstehende Buchungen), +1 nur wenn eine gefunden wird | 1× je App-Start |
| F8 Timer, Erinnerung | **0**, solange laut Grundriss keine eigene, nicht eingecheckte Buchung ansteht. Sonst +1 (+1 beim Fragen), höchstens bis zum Check-in oder Verfall, also etwa 12 Ticks | alle 5 Min je offener App |
| F8 Timer, Grundlast (wie G8) | `Refresh` (2 Galerien) + Ladezeile (1) = 3 | alle 5 Min je offener App, nur ohne offenen Dialog |
| F3 Kachel-Klick | +1 nur bei belegtem Tisch (Datensatz für das Popup per ID) | je Klick |
| F6 Verlängern | +1 („zwei Tische“) | je Verlängern |
| F7 Einchecken | +3 (Tisch schon vergeben? vorher und nachher, dazu die Nachlese) gegenüber dem Export | je Check-in |
| F4 Speichern | ±0 gegenüber dem Studio (Nachtrag 4 ist schon drin; gegenüber G6 ohne Nachtrag 4 waren es −2 bis −7) | je Buchung |
| F2 Stornieren Dashboard | etwa +4 gegenüber heute (frisch lesen, nachlesen, `Refresh` mit 2 Galerien) | je Storno |
| F2 Stornieren Tab | +2 (frisch lesen, nachlesen) | je Storno |
| F2 Mehrfach-Stornieren | ±0 | je Storno |

Bei 30 Nutzern und offener App sind das etwa 18 Abfragen pro Minute durch den Timer, fast alles Grundlast aus G8. Die Freigabe selbst kostet in der Anzeige **keine** Abfrage.

**4. Handy-App:** bestätigt. Die Handy-App wird erst geteilt, wenn die Regel aus `AUFTRAG_Handy_Freigabe.md` dort eingebaut und getestet ist. Sonst kann man in der Handy-App eine verfallene Buchung einchecken, deren Tisch schon neu vergeben ist.

**5. „Nur eigene Elemente“: zu korrigieren.**
- **Nicht** „Listen verwalten“ befreit von der Einstellung, sondern die Berechtigung **„Listenverhalten außer Kraft setzen“** (Override List Behaviors). Sie steckt standardmäßig in **Entwerfen** und **Vollzugriff**, **nicht** in **Bearbeiten**. „Bearbeiten“ enthält dagegen „Listen verwalten“ ([Microsoft Learn](https://learn.microsoft.com/en-nz/sharePoint/sites/user-permissions-and-permission-levels), **belegt**).
- **Folgen:**
  - Kollegen als **Mitglieder** (Bearbeiten) sind betroffen, so soll es sein.
  - Josias als **Besitzer** (Vollzugriff) ist nicht betroffen.
  - Michael ist nur dann nicht betroffen, wenn er **Websitebesitzer** (Vollzugriff) ist, „Mitbesitzer der App“ allein reicht dafür nicht.
  - Der **Aufräum-Flow** läuft mit der Verbindung dessen, der sie angelegt hat. Mit Josias’ Verbindung (Vollzugriff) ist er nicht betroffen.
- **Vorsicht** (**geschlussfolgert**, Community-Bericht [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/378127/sharepoint-list-permissions-read-only-for-all-item)): Bekommt jemand zusätzlich über eine andere Gruppe „Entwerfen“ oder „Vollzugriff“, sieht und ändert er wieder alles. Deshalb **nach dem Setzen mit einem Kollegen-Konto testen**: fremde Buchung in der Liste ändern geht nicht, eigene geht.
- **Zusätzlich zu klären (Michael/IT, Prüf-Agent, belegt):**
  - **Bearbeiten** enthält **„Listen verwalten“**. Mitglieder mit Bearbeiten können deshalb die Listeneinstellungen ändern, auch „nur eigene Elemente“ wieder abschalten, und Spalten oder ganze Listen löschen.
  - In der Liste `Tische` können sie direkt `Gesperrt` und `Titel` ändern. Das widerspricht „nur Josias sperrt Tische“.
  - **Empfehlung:** Auf `Tischbuchungen` die Vererbung unterbrechen und den Mitgliedern **Mitwirken** statt Bearbeiten geben. Auf `Tische` (und `Räume`/`Raumbuchungen`) nur **Lesen**. Die App braucht nicht mehr.
  - Test mit einem Kollegen-Konto: Ein Kollege ändert `Tische.Gesperrt` → nicht erlaubt.
- **Was ein künftiger Flow beachten muss:**
  1. Seine Verbindung braucht Vollzugriff oder Entwerfen, sonst kann er nur selbst angelegte Zeilen ändern oder löschen.
  2. **Zeilen, die ein Flow anlegt, gehören dem Konto der Verbindung.** Legt ein Flow Buchungen für andere an (z. B. aus Outlook), können diese Personen sie in der App **nicht einchecken, verlängern oder stornieren**. Ohne Check-in verfallen sie. Ein solcher Flow muss `CheckedIn` setzen oder die Buchung über die App der Person anlegen lassen.
  3. Die Verbindung nicht an ein persönliches Konto binden, das wegfallen kann (Vertretung).

## 6. Testbogen

| ✓ | Test | Ergebnis |
|---|---|---|
| ☐ | E Vorab-Test 1 (Name) und 2 (Collection), Test-Steuerelemente gelöscht | |
| ☐ | F1 App-Prüfung ohne rote Fehler, OnStart ausgeführt, Check-in-Frage beim Start | |
| ☐ | F2 Stornieren Dashboard, Tab, Mehrfach (5 Stück, Zeit), Doppelklick | |
| ☐ | Testmodus: Testknopf `btnTestFreigabe` mit `Set(varFreigabeMinuten; 1)`, in der Vorschau drücken. **`App.OnStart` nicht ändern** | |
| ☐ | F3 verfallene Testzeile → Kachel grün, Klick → Buchungsdialog | |
| ☐ | F4 über verfallene Buchung buchen, neue Buchung ohne Aktualisieren in der Liste | |
| ☐ | F5 Panel-Liste und 5 Std | |
| ☐ | F6 Verlängern über verfallene Buchung, „zwei Tische“ | |
| ☐ | F7 Einchecken (zu früh, laufend, zu spät), Auschecken mit zweitem Tippen | |
| ☐ | F8 Timer aktualisiert, Erinnerung einmal | |
| ☐ | **Testknopf gelöscht**, in `App.OnStart` steht `Set(varFreigabeMinuten; 30)` | |
| ☐ | Veröffentlichen | |

## 7. UNSICHER
| Nr | Was | Test / Abhilfe |
|---|---|---|
| U1 | Name `Erstellt` in Studio | Vorab-Test 1 |
| U7 | `Erstellt` in Collections (explizite Spaltenauswahl) | Vorab-Test 2 |
| U8 | Die Timer-Vorprüfung vergleicht `colGrundriss.Name` (Anzeigename aus SharePoint) mit `User().FullName`. Weichen beide ab (Schreibweise im Profil), fragt der Timer nie, nur der App-Start fragt | Test F8. Fragt der Timer nicht, melden |
| U9 | Ob die Galerien nach `Remove` ohne `Refresh` aktualisieren, ist in der Handy-App gemessen (T-23). Hier bleibt `Refresh` beim Stornieren trotzdem drin. Grund: Der Tab „Buchungen“ hat einen bekannten Neuaufbau-Trick (`varGalleryNeuAufbauen`, Frage 15) | kein Test nötig |
| U3 | Geräteuhr | wie Paket F |
| U10 | Die Nachlese beim Stornieren und Einchecken ist dieselbe Abfrage (`LookUp(…; ID = …)`) wie das frische Lesen davor. Käme sie aus einem Zwischenspeicher, wäre die Meldung „nicht angekommen“ falsch (Daten richtig). Dasselbe Muster läuft schon in G3 (Verlängern) | Hat G3 beim Test „Buchung geändert, neues Ende …“ gemeldet, ist das entkräftet. Sonst F2-Test beachten |
| U11 | Ein Timer-Ladevorgang, der während eines Speicherns läuft, kann `colGrundriss` mit einem älteren Stand überschreiben (bis zum nächsten Laden) | selten, harmlos, nächster Tick korrigiert |

## Anhang A: Fassungen im Studio vor diesem Paket (Rückfall)

**`App.OnStart`** (F1, Gesamtplan G1)

```
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
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnStornieren.OnSelect`** (F2, Export 07.10.)

```
Remove(Tischbuchungen; varSelectedBuchung);; Set(varZeigeVerwalten; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnStornieren_1.OnSelect`** (F2, Export 07.10.)

```
Set(varIsLoading; true);;
If(
  IsBlank(varSelectedBuchungTab);
  Notify("Keine Buchung ausgewählt."; NotificationType.Warning);
  Remove(Tischbuchungen; varSelectedBuchungTab);;
  Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Notify("Buchung storniert."; NotificationType.Success)
);;
Set(varZeigeVerwaltenTab; false);;
Set(varIsLoading; false)
```

**`btnStornierenKlein.OnSelect`** (F2, Export 07.10.)

```
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
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Clear(colStornoFrisch);;
Clear(colStornoZiele);;
Clear(colAusgewaehlteBuchungen);;
Set(varGeklickteBuchungKlein; Blank());;
Set(varZeigeVerwaltenKlein; false);;
Set(varAuswahlModusAktiv; false);;
Reset(tglAuswahlModus);;
Set(varIsLoading; false)
```

**`btnHitArea.OnSelect`** (F3, Gesamtplan G7)

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
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
        Set(varDialogJetzt; Now());;
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
)
```

**`ddStockwerk.OnChange`** (F3, Export 07.10.)

```
Set(varAusgewaehltesStockwerk; ddStockwerk.Selected.Kurz);;
Set(varStockwerkDropdownOffen; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`dpAnsichtsDatum.OnChange`** (F3, Export 07.10.)

```
Set(varAnsichtsDatum; dpAnsichtsDatum.SelectedDate);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`Icon1_1.OnSelect`** (F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Icon1.OnSelect`** (F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`Image6.OnSelect`** (F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnHitArea_1.OnSelect`** (F3, Gesamtplan G12)

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**`btnSpeichern.OnSelect`** (F4, Gesamtplan G6 (Fassung Nachtrag 4))

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

**`btnSpeichernTischePanel.OnSelect`** (F4, Gesamtplan G6 (Fassung Nachtrag 4))

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

**`btnTischHinzufügen.OnSelect`** (F5, Gesamtplan G7)

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
Set(varPanelJetzt; Now());;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

**`ddTischePanel.Items`** (F5, Gesamtplan G9)

```
With(
  {
    datum: dpDatumTischePanel.SelectedDate;
    startZeit: Time(Value(Left(ddStartTischePanel.Selected.Value; 2)); Value(Mid(ddStartTischePanel.Selected.Value; 4; 2)); 0);
    endeZeit: Time(Value(Left(ddEndTischePanel.Selected.Value; 2)); Value(Mid(ddEndTischePanel.Selected.Value; 4; 2)); 0);
    bisRoh: If(varWiederholen; dpWiederholenBis_1.SelectedDate; dpDatumTischePanel.SelectedDate)
  };
  With(
    { bis: If(bisRoh > datum + 14; datum + 14; bisRoh) };
    With(
      {
        termine: ForAll(
          Filter(
            ForAll(Sequence(If(bis < datum; 0; DateDiff(datum; bis; TimeUnit.Days) + 1); 0); DateAdd(datum; Value; TimeUnit.Days)) As D;
            !varWiederholen || Switch(Weekday(D.Value; StartOfWeek.Monday); 1; varTagMo; 2; varTagDi; 3; varTagMi; 4; varTagDo; 5; varTagFr; 6; varTagSa; 7; varTagSo)
          ) As T;
          {Start: T.Value + startZeit; Ende: T.Value + endeZeit}
        )
      };
      With(
        {
          belegtListe: If(
            varZeigeTischBuchungForm;
            ForAll(
              Filter(
                Tischbuchungen;
                Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(varWiederholen && dpWiederholenBis_1.SelectedDate > dpDatumTischePanel.SelectedDate; Min(DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days); 14); 0) + 1; TimeUnit.Days) && Endzeit > dpDatumTischePanel.SelectedDate
              );
              {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit}
            );
            FirstN(Table({TischName: ""; Beginn: Now(); Schluss: Now()}); 0)
          )
        };
        SortByColumns(
          Filter(
            ForAll(
              Tische As Ti;
              With(
                { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegtListe; TischName = Ti.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
                {
                  Titel: Ti.Titel;
                  Gesperrt: Ti.Gesperrt;
                  ID: Ti.ID;
                  Belegt: n;
                  Etage: If(Ti.Geschoss.Value = varAusgewaehltesStockwerk; 0; 1);
                  Schluessel: Ti.Geschoss.Value & Left(Ti.Titel; Len(Ti.Titel) - Len(Last(Split(Ti.Titel; " ")).Value)) & Text(IfError(Value(Last(Split(Ti.Titel; " ")).Value); 0); "000");
                  Anzeige: Ti.Titel & If(n = 0; ""; "  (an " & n & " von " & CountRows(termine) & " Tagen belegt)")
                }
              )
            );
            !Gesperrt && !("big table" in Lower(Titel)) && (Belegt = 0 || Belegt < CountRows(termine))
          );
          "Belegt"; SortOrder.Ascending;
          "Etage"; SortOrder.Ascending;
          "Schluessel"; SortOrder.Ascending
        )
      )
    )
  )
)
```

**`btn5Std.DisplayMode`** (F5, Gesamtplan G10)

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn5Std.Fill`** (F5, Gesamtplan G10)

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 5 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btn9Std.DisplayMode`** (F5, Gesamtplan G10)

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      !varZeigeTischBuchungForm || endeZeit > tagesEnde;
      DisplayMode.Disabled;
      If(
        IsBlank(ddTischePanel.Selected.Titel);
        DisplayMode.Edit;
        If(
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

**`btn9Std.Fill`** (F5, Gesamtplan G10)

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 9;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60) + 9 * 60; TimeUnit.Minutes) && Endzeit > DateAdd(dpDatumTischePanel.SelectedDate; If(dpDatumTischePanel.SelectedDate = Date(Year(varPanelJetzt); Month(varPanelJetzt); Day(varPanelJetzt)); Max(6 * 60; 30 * RoundUp((Hour(varPanelJetzt)*60 + Minute(varPanelJetzt)) / 30; 0)); 8 * 60); TimeUnit.Minutes)).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

**`btnVerwalten.OnSelect`** (F6, Gesamtplan G2)

```
Set(varSelectedBuchung; ThisItem);;
Set(varVerlTisch; ThisItem.Tisch.Value);;
Set(varVerlEndeAlt; ThisItem.Endzeit);;
Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
Set(varVerlGrenze; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
Set(varAusgewaehltePlusDauer; Blank());;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false)
```

**`btnVerwalten_2.OnSelect`** (F6, Gesamtplan G2)

```
If(
  varAuswahlModusAktiv;
  Set(varGeklickteBuchungKlein; ThisItem);;
  Set(varZeigeVerwaltenKlein; true);
  Set(varSelectedBuchungTab; ThisItem);;
  Set(varVerlTisch; ThisItem.Tisch.Value);;
  Set(varVerlEndeAlt; ThisItem.Endzeit);;
  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
  Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varZeigeVerwaltenTab; true);;
  Set(varZeigeCheckin; false);;
  Set(varZeigeDetails; false);;
  Set(varZeigeDialog; false)
)
```

**`btnVerlängern.OnSelect`** (F6, Gesamtplan G3)

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
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
    If(
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern_1.OnSelect`** (F6, Gesamtplan G3)

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
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
    If(
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsBlank(LookUp(Tischbuchungen; Tisch.Value = varVerlTisch && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt).ID);
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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnEinchecken.OnSelect`** (F7, Export 07.10.)

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {CheckedIn: !aktuelleBuchung.CheckedIn}))
);;
Set(varZeigeCheckin; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**`btnEinchecken.Text`** (F7, Export 07.10.)

```
If(varSelectedBuchung.CheckedIn; "Auschecken"; "Einchecken")
```

**`btnEincheckenHeute.OnSelect`** (F7, Export 07.10.)

```
Set(varSelectedBuchung; ThisItem);; Set(varZeigeCheckin; true);; Set(varZeigeDetails; false);; Set(varZeigeDialog; false);; Set(varZeigeVerwalten; false)
```

**`lblStatusHeute.Text`** (F7, Export 07.10.)

```
If(ThisItem.CheckedIn; "Eingecheckt"; "Einchecken")
```

**`lblStatusHeute.Color`** (F7, Export 07.10.)

```
If(ThisItem.CheckedIn; ColorValue("#00A96B"); ColorValue("#FFA500"))
```

## Anhang B: Prüfung

Maschinell (`werkzeuge/paket_f2.py`):

```
37 Properties in 8 Schritten, 1 neues Steuerelement (tmrAktualisieren, ersetzt G8).
Ausgangslage = Studio-Stand nach Josias' Angaben (Export + eingefügte Gesamtplan-Schritte, G6 in Fassung Nachtrag 4). Keine Property liegt in G22 (nur teilweise eingefügt).
Ladezeile neu an 16 Stellen, alte an 0. Keine Verweise auf den Rückfrage-Dialog (G4), auf G14-Steuerelemente oder varZeigeStornoFrage.
Schreibstellen: 8 (btnEinchecken.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnStornieren.OnSelect, btnStornierenKlein.OnSelect, btnStornieren_1.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect), jedes Patch/Remove hinter der Zweifach-Sperre, alle mit neuer Ladezeile.
Stornieren: frischer Datensatz, Eigentümerprüfung vor dem Remove (Dashboard, Tab), Mehrfach nur eigene. Speichern ohne Refresh (Nachtrag 4).
Abfragen auf Tischbuchungen (ohne reine ID-Abfragen): 42, jede einzeln: Freigabe-Regel lokal oder begründet ausgenommen (3).
Je Property: Klammern, Rückübersetzung, keine Kommentare, Steuerelement im Studio vorhanden, jede var/col wird gesetzt, varFreigabeGrenze vor Gebrauch gesetzt.
Prüfung: 0 Fehler
```

Unabhängige Prüfung: siehe `../2026-10-08_PaketF2/pruefung_paket_f2.md` (Fassung 2; Fassung 2.1 ändert nur die DropColumns-Schreibweise).

Bewusst ohne Freigabe-Regel:

- `galTischbuchungenHeute.Items`: eigene Buchungen im Dashboard; verfallene bleiben sichtbar (Status „Verfallen“)
- `galAlleTischbuchungen.Items`: eigene Buchungen im Tab; verfallene dürfen storniert werden
- `btnStornierenKlein.OnSelect`: Mehrfach-Stornieren eigener Buchungen; verfallene dürfen mit storniert werden

## Anhang C: G8 ohne Paket F (nur falls Paket F nicht eingefügt wird)
Wenn F3–F8 nicht vor dem Go-Live kommen, aber der Timer schon: `tmrAktualisieren` wie in F8 anlegen (`Duration`, `Repeat`, `AutoStart`, `Visible` wie dort) und `OnTimerEnd` so setzen. Das ist G8 ohne `varZeigeStornoFrage`. Später ersetzt F8 diese Property.

**`tmrAktualisieren.OnTimerEnd`** (nur ohne Paket F)

```
If(
  !varIsLoading && !varZeigeDialog && !varZeigeTischBuchungForm && !varZeigeVerwalten && !varZeigeVerwaltenTab && !varZeigeVerwaltenKlein && !varZeigeCheckin;
  If(
    varAnsichtsDatum < Today() && dpAnsichtsDatum.SelectedDate < Today();
    Set(varAnsichtsDatum; Today());;
    Reset(dpAnsichtsDatum)
  );;
  Refresh(Tischbuchungen);;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); false; ClearCollect(colGrundriss; neu)))
)
```

## Anhang D: Notweg „sicher stornieren ohne Freigabe“
Nur falls F1–F8 **nicht** vor dem Go-Live kommen. Die drei Blöcke stornieren direkt und sicher (Sperre, frisch, nur eigene, Nachlese, Meldung) mit der **bisherigen** Ladezeile, ohne `varFreigabe…`, ohne F1. Kommt Paket F später, ersetzt F2 sie. `DisplayMode` wie in F2 setzen.

#### `btnStornieren.OnSelect` (Notweg)

Änderungen gegenüber dem Studio:

```diff
@@ -1,2 +1,26 @@
-Remove(Tischbuchungen; varSelectedBuchung);; Set(varZeigeVerwalten; false);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
+If(
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
+  If(
+    IsBlank(varStornoBuchung.ID);
+    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+    Set(varZeigeVerwalten; false);
+    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+    IfError(
+      Remove(Tischbuchungen; varStornoBuchung);
+      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+      If(
+        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+        Notify("Buchung storniert."; NotificationType.Success);;
+        Set(varZeigeVerwalten; false);
+        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+      )
+    )
+  );;
+  Refresh(Tischbuchungen);;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block:

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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnStornieren_1.OnSelect` (Notweg)

Änderungen gegenüber dem Studio:

```diff
@@ -1,11 +1,26 @@
-Set(varIsLoading; true);;
 If(
-  IsBlank(varSelectedBuchungTab);
-  Notify("Keine Buchung ausgewählt."; NotificationType.Warning);
-  Remove(Tischbuchungen; varSelectedBuchungTab);;
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
+  If(
+    IsBlank(varStornoBuchung.ID);
+    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
+    Set(varZeigeVerwaltenTab; false);
+    Lower(varStornoBuchung.Person.Email) <> Lower(User().Email);
+    Notify("Nur eigene Buchungen können storniert werden."; NotificationType.Error);
+    IfError(
+      Remove(Tischbuchungen; varStornoBuchung);
+      Notify("Stornieren fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
+      If(
+        IsBlank(LookUp(Tischbuchungen; ID = varStornoBuchung.ID).ID);
+        Notify("Buchung storniert."; NotificationType.Success);;
+        Set(varZeigeVerwaltenTab; false);
+        Notify("Die Stornierung ist nicht angekommen. Bitte aktualisieren und prüfen."; NotificationType.Warning)
+      )
+    )
+  );;
   Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
-  Notify("Buchung storniert."; NotificationType.Success)
-);;
-Set(varZeigeVerwaltenTab; false);;
-Set(varIsLoading; false)
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block:

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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnStornierenKlein.OnSelect` (Notweg)

Änderungen gegenüber dem Studio:

```diff
@@ -1,36 +1,40 @@
-Set(varIsLoading; true);;
-ClearCollect(
-    colStornoFrisch;
-    Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
-);;
-ClearCollect(
-    colStornoZiele;
-    Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
-);;
 If(
-    CountRows(colAusgewaehlteBuchungen) = 0;
-    Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
-    If(
-        CountRows(colStornoZiele) = 0;
-        Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
-        IfError(
-            Remove(Tischbuchungen; colStornoZiele);
-            Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
-            If(
-                CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
-                Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
-                Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
-            )
-        )
-    )
-);;
-Refresh(Tischbuchungen);;
-With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
-Clear(colStornoFrisch);;
-Clear(colStornoZiele);;
-Clear(colAusgewaehlteBuchungen);;
-Set(varGeklickteBuchungKlein; Blank());;
-Set(varZeigeVerwaltenKlein; false);;
-Set(varAuswahlModusAktiv; false);;
-Reset(tglAuswahlModus);;
-Set(varIsLoading; false)
+  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
+  Set(varIsLoading; true);;
+  ClearCollect(
+      colStornoFrisch;
+      Filter(Tischbuchungen; Person.Email = User().Email && Endzeit >= Now())
+  );;
+  ClearCollect(
+      colStornoZiele;
+      Filter(colStornoFrisch As F; !IsBlank(LookUp(colAusgewaehlteBuchungen As A; A.ID = F.ID)))
+  );;
+  If(
+      CountRows(colAusgewaehlteBuchungen) = 0;
+      Notify("Keine Buchungen ausgewählt."; NotificationType.Warning);
+      If(
+          CountRows(colStornoZiele) = 0;
+          Notify("Die ausgewählten Buchungen gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);
+          IfError(
+              Remove(Tischbuchungen; colStornoZiele);
+              Notify("Stornieren fehlgeschlagen. Die Liste wurde aktualisiert, bitte erneut versuchen."; NotificationType.Error);
+              If(
+                  CountRows(colStornoZiele) < CountRows(colAusgewaehlteBuchungen);
+                  Notify(CountRows(colStornoZiele) & " von " & CountRows(colAusgewaehlteBuchungen) & " Buchungen storniert. Die übrigen waren bereits storniert."; NotificationType.Warning);
+                  Notify(CountRows(colStornoZiele) & " Buchungen storniert."; NotificationType.Success)
+              )
+          )
+      )
+  );;
+  Refresh(Tischbuchungen);;
+  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
+  Clear(colStornoFrisch);;
+  Clear(colStornoZiele);;
+  Clear(colAusgewaehlteBuchungen);;
+  Set(varGeklickteBuchungKlein; Blank());;
+  Set(varZeigeVerwaltenKlein; false);;
+  Set(varAuswahlModusAktiv; false);;
+  Reset(tglAuswahlModus);;
+  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
+  Set(varIsLoading; false)
+)
```

Vollständiger Block:

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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
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
