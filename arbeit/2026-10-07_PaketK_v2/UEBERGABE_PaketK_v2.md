# ÜBERGABE Tischbuchung: Paket K v2 (Korrektheit, Verlängern, Speichern, Tischauswahl)
**v2 · 07.10.2026 · Basis: veröffentlichter Export „Tischbuchung App 07.10.2026 verbesserung analyse“ (enthält L2) · alle 54 Properties maschinell aus diesem Export erzeugt und geprüft (`werkzeuge/paket_k_v2.py`, Anhang 2) · ersetzt `UEBERGABE_PaketK_v1.md` · noch nichts davon eingefügt**

Kennzeichnung: **belegt** = im Export/Dokument nachgesehen · **gemessen** = Livemonitor oder Test · **geschlussfolgert** = abgeleitet, nicht getestet · **UNSICHER** = offen, mit Prüftest (Abschnitt UNSICHER).

## 0. Kurzfassung
- **v1 hatte einen echten Fehler.** Die Doppelklick-Sperre nur über `DisplayMode` hält nicht. Die Handy-App hat das am 06.10. gemessen: Ein Doppeltipp auf „+1 Std“ hat zweimal verlängert (belegt, `ENTSCHEIDUNGEN.md` E-07). v2 nutzt deshalb an allen 8 Schreibstellen die dort erprobte Zweifach-Sperre `If(!varIsLoading && Now() >= varSperreBis; …)`.
- **Eine Regel für beide Apps.** v2 übernimmt die Regeln, die du für die Handy-App schon bestätigt hast: nie über 22:00, kein Buchen in der Vergangenheit, keine zwei Tische zur selben Zeit, Einchecken ab 30 Minuten vor Beginn. Außerdem dasselbe Schreibmuster: frisch lesen, prüfen, `IfError`, nachlesen, ehrlich melden. Die Formeln sind dort schon in Betrieb (belegt).
- **Verwalten-Dialoge neu gedacht (Teil A).** Beim Öffnen wird **einmal** berechnet, bis wann die Buchung verlängert werden kann. Die 24 Plus-/Minus-Properties fragen danach **keine Daten mehr ab** (vorher je eine eigene Abfrage, auch bei geschlossenem Dialog, gemessen ~50 Abfragen pro Schreibvorgang). Befund B0 ist damit an der Wurzel weg: Der Tab liest seine eigene Buchung (statt der Ein-Zeilen-Lösung K1).
- **Speichern (Teil B):** Beide Speichern-Knöpfe laufen gleich, beide mit Sammel-Patch. Neu dabei: Kollisionsprüfung mit Zeitfenster, Prüfung „du hast schon einen Tisch“, **`SerienID` wird geschrieben und nachgelesen** (ehrliche Anzahl statt lokaler Zählung), Erkennung gleichzeitiger Buchungen, **eine** Meldung mit allem. Bei einem Fehler bleiben die Eingaben stehen.
- **Tischauswahl (Teil C):** Das Panel zeigt nur noch freie Tische, sortiert, ohne Big Table, das aktuelle Stockwerk zuerst. Bei Serien steht dabei, an wie vielen Tagen ein Tisch belegt ist. Beim Öffnen ist kein Tisch vorausgewählt. „5 Std“/„9 Std“ starten an anderen Tagen um 08:00.
- **Aufwand:** 22 Schritte, 54 Properties, jeder Schritt einzeln testbar. Die Teile A bis D sind voneinander unabhängig; nur Schritt 0 muss zuerst kommen.
- **Was nur du entscheiden kannst:** sieben Punkte in Abschnitt 2. Überall steht ein Vorschlag (meist die Regel der Handy-App). Wenn du nichts sagst, gilt der Vorschlag.

## 1. Übersicht

| Schritt | Steuerelement.Property | Was | Behebt |
|---|---|---|---|
| 0 | `App.OnStart` | Neue Variablen anlegen (Sperre, Verlängern-Grenzen) | Voraussetzung für Sperre und Grenzen |
| A1 | `btnVerwalten.OnSelect` | Dashboard-Verwalten öffnen: Grenze einmal berechnen | L3 (keine Abfragen im versteckten Dialog), 22:00 im Knopf sichtbar |
| A2 | `btnVerwalten_2.OnSelect` | Buchungen-Tab-Verwalten öffnen: Grenze einmal berechnen, Dauer leeren | B0 (BD-02) an der Wurzel, alte Dauer blieb vorausgewählt |
| A3 | `btnPlus1Std.DisplayMode`, `btnPlus1Std.Fill`, `btnPlus2Std.DisplayMode`, `btnPlus2Std.Fill`, `btnPlus3Std.DisplayMode`, `btnPlus3Std.Fill` | +1 Std (Dashboard) ohne Abfrage | ~6 Abfragen je Welle weniger, 22:00 grau |
| A4 | `btnPlus1Std_1.DisplayMode`, `btnPlus1Std_1.Fill`, `btnPlus2Std_1.DisplayMode`, `btnPlus2Std_1.Fill`, `btnPlus3Std_1.DisplayMode`, `btnPlus3Std_1.Fill` | +1 Std (Tab) richtige Buchung, ohne Abfrage | B0, ~6 Abfragen weniger |
| A5 | `btnMinus1Std.DisplayMode`, `btnMinus1Std.Fill`, `btnMinus2Std.DisplayMode`, `btnMinus2Std.Fill`, `btnMinus3std.DisplayMode`, `btnMinus3std.Fill` | −1 Std (Tab) richtige Buchung, ohne Abfrage | B0, ~6 Abfragen weniger |
| A6 | `btnVerlängern.OnSelect`, `btnVerlängern.DisplayMode` | Verlängern (Dashboard) prüft am Server, meldet ehrlich | BD-03, BD-04, BD-12, BD-16, BD-09 |
| A7 | `btnVerlängern_1.OnSelect`, `btnVerlängern_1.DisplayMode` | Verlängern/Verkürzen (Tab) prüft am Server, meldet ehrlich | BD-03, BD-04, BD-12, BD-16, BD-09 |
| A8 | `btnStornieren.OnSelect`, `btnStornieren.DisplayMode` | Stornieren (Dashboard) auf frischem Datensatz, Nachlese | BD-05 „Item Not Found“ |
| A9 | `btnStornieren_1.OnSelect`, `btnStornieren_1.DisplayMode` | Stornieren (Tab) auf frischem Datensatz, Nachlese | BD-05 im Tab |
| A10 | `btnEinchecken.OnSelect`, `btnEinchecken.DisplayMode` | Einchecken: frischer Datensatz, Zeitfenster, Nachlese | BD-15, Doppeltipp, Fehler wurde verschluckt |
| B1 | `btnSpeichern.OnSelect`, `btnSpeichern.DisplayMode` | Buchungsdialog: Sammel-Patch mit SerienID, Prüfungen, Nachlese, eine Meldung | BD-01, BD-04, BD-06, BD-07, BD-08, BD-09, BD-11, BD-19, B3, E-4 |
| B2 | `btnSpeichernTischePanel.OnSelect`, `btnSpeichernTischePanel.DisplayMode` | Tische-Panel: gleicher Ablauf wie B1 (Sammel-Patch statt Schleife) | wie B1, dazu Schleife → Sammel-Patch |
| C1 | `ddTischePanel.Items`, `ddTischePanel.Items.Value`, `ddTischePanel.AllowEmptySelection`, `ddTischePanel.Default` | Nur freie Tische, sortiert, ohne Big Table | E-1 nur freie Tische, Frage 21 |
| C2 | `btnTischHinzufügen.OnSelect` | Panel öffnen: Datum und Tisch zurücksetzen | Frage 21 (alte Auswahl) |
| C3 | `btn5Std.DisplayMode`, `btn5Std.Fill`, `btn5Std.OnSelect` | 5 Std: anderer Tag ab 08:00, ohne Tisch bedienbar, Abfrage nur bei offenem Panel | Frage 20, BD-27, Abfragen bei geschlossenem Panel |
| C4 | `btn9Std.DisplayMode`, `btn9Std.Fill`, `btn9Std.OnSelect` | 9 Std: wie 5 Std | wie C3 |
| C5 | `Label14.Text` | Hinweistext liest das Panel-Datum (BD-26) | BD-26 |
| D1 | `ddStockwerk.OnSelect` | Dauer leeren statt 0 (BD-12) | BD-12 |
| D2 | `Icon1.OnSelect`, `Icon1_1.OnSelect`, `Image6.OnSelect`, `btnHitArea_1.OnSelect` | „Aktualisiert.“ nur bei Erfolg (BD-10) | BD-10 (U7) |
| D3 | `btnStornierenKlein.OnSelect` | Mehrfach-Stornieren mit Zweifach-Sperre | Doppeltipp bei Mehrfach-Stornieren |
| D4 | `btnAbbrechenTischePanel.OnSelect` | Doppelte Zeile weg (BD-25) | BD-25 |

## 2. Entscheidungen (Vorschlag, du bestätigst oder widersprichst)
| # | Frage | Vorschlag in v2 | Warum | Falls du es anders willst |
|---|---|---|---|---|
| E1 | 22:00 beim Verlängern | **ablehnen**, Plus-Knopf wird grau, wenn er über 22:00 führen würde | Handy-App V5 „nie über 22:00“ (bestätigt), Panel endet schon um 22:00 (belegt) | In A1/A2 `22 * 60` durch `24 * 60` ersetzen und die 22:00-Prüfung in A6/A7 entfernen: Bescheid geben, ich erzeuge es neu |
| E2 | Zwei Tische zur selben Zeit für dieselbe Person (BD-06, Frage 5) | **verhindern** | Handy-App V6 „nein, wird verhindert“ | Prüfung `colNeuIch` in B1/B2 entfernen (eine Zeile, ich erzeuge es neu) |
| E3 | Einchecken-Zeitfenster (BD-15, Frage 8) | **ab 30 Min vor Beginn bis Ende**, Auschecken jederzeit | Handy-App V2. Am PC bleibt Auschecken möglich (der Knopf heißt heute schon so), die Handy-App kennt es nicht (V3) | Arm `!varCheckinBuchung.CheckedIn && (…)` in A10 entfernen |
| E4 | Buchen in der Vergangenheit (BD-19, Frage 7) | **sperren** (vor der laufenden halben Stunde) | Handy-App E-06/A15 | Arm `First(colNeuTermine).Start < varNeuJetzt` entfernen |
| E5 | Big Table in der Panel-Liste | **nicht in der Liste**, über den Grundriss weiter buchbar | Wunsch E-1 und Handy-App V7. Der Grundriss bleibt unverändert, damit nichts wegfällt | Filter `!("big table" in …)` in C1 entfernen |
| E6 | „5 Std“/„9 Std“ an einem anderen Tag | **ab 08:00** (wie die Startliste) | Heute: ab der aktuellen Uhrzeit, an einem anderen Tag sinnlos. Um 07:00 morgens wird der Start „07:00“ gesetzt, den die Liste nicht enthält (Frage 20) | in C3/C4 `8 * 60` anders wählen |
| E7 | Mehrfachauswahl und Serienbuchung | **beide drinlassen** | Mehrfach-Stornieren gemessen 33 Buchungen ~9 s ohne Fehler. Serie gemessen ~4,7 s. v2 sichert beide zusätzlich ab (D3, B1/B2) | `tglAuswahlModus.Visible = false` blendet die Mehrfachauswahl aus |

**K4.2 bleibt verworfen** (geprüft, Begründung aus v1 stimmt): Wer „Wiederholen“ anhakt und das Bis-Datum nicht anfasst, bekäme mit K4.2 still nur eine Buchung. v2 ergänzt eine fehlende Meldung: Liegt das Bis-Datum **vor** dem Startdatum, kommt jetzt „Das Wiederholen-bis-Datum liegt vor dem Buchungsdatum“. Vorher konnte `Sequence` mit negativer Anzahl zu einem Fehler führen (geschlussfolgert).

## 3. Ablauf je Schritt (wie bei L2)
1. Vorher: **`.msapp` exportieren** (Datei → Speichern unter → Diesen Computer) und prüfen, dass seit dem Export vom 07.10. in Studio nichts geändert wurde. Wenn doch: neuen Export geben, dann erzeuge ich alles neu (`python3 -I werkzeuge/paket_k_v2.py`). Das Skript bricht ab, wenn ein Anker nicht mehr genau passt.
2. Steuerelement in der Strukturansicht wählen (der Ort steht bei jedem Block) → Property im Formelfeld → **ganze Property ersetzen** → Enter.
3. App-Prüfung (Baseline vor Paket: 134 Einträge, keine Formelfehler). Neue **Formelfehler** = sofort melden, nicht weitermachen. Neue Delegierungswarnungen sind nur bei C1 erwartet (UNSICHER U-V3).
4. Kurz testen (Test unter jedem Schritt), im Testbogen abhaken.
5. **Reihenfolge:** Schritt 0 zuerst (sonst sind die Knöpfe 2 Sekunden lang nach dem App-Start gesperrt, U-V1). Danach A, B, C, D in beliebiger Reihenfolge. Innerhalb eines Schritts alle Properties einfügen, bevor du testest.
6. **Besonderheit `Items.Value` (C1):** Das ist kein Formelfeld. Rechts im Eigenschaftenbereich „Wert“ auf **Anzeige** stellen, nachdem `Items` ersetzt ist.

## Teil 0: Vorbereitung (zuerst)

Legt drei Variablen mit Startwert an. `varSperreBis` muss einen Zeitwert haben, bevor der erste Knopf ihn vergleicht. Die Zeilen stehen **vor** der L2-Ladezeile, die Ladezeile bleibt die letzte Anweisung.

### 0 `App.OnStart`

Ort: `App`

Änderung an `App.OnStart` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -101,3 +101,6 @@
 Set(varIsLoading; false);;
 Set(varSpinnerWinkel; 0);;
+Set(varSperreBis; Now());;
+Set(varVerlGrenze; Now());;
+Set(varVerlGrenzeTab; Now());;
 With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**Einfügen: ganze Property `App.OnStart` ersetzen durch**

```
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
Set(varSperreBis; Now());;
Set(varVerlGrenze; Now());;
Set(varVerlGrenzeTab; Now());;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

**Test:** App-Prüfung ohne neue Fehler. Vorschau starten: Grundriss lädt wie bisher.

## Teil A: Verwalten-Dialoge (Verlängern, Stornieren, Einchecken)

**Was sich ändert (belegt am Export):** Heute rechnet jeder Plus-/Minus-Knopf seine Farbe und Bedienbarkeit mit einer eigenen Abfrage `LookUp(Tischbuchungen; ID = varSelectedBuchung.ID)` plus einer Kollisionsabfrage. Das sind 24 Properties, und sie laufen auch bei geschlossenem Dialog. Im Tab lesen sie die falsche Variable (B0). **Neu:** Beim Klick auf „Verwalten“ wird einmal die **Grenze** berechnet. Das ist der Beginn der nächsten Buchung am selben Tisch nach meinem Ende, höchstens 22:00 am Buchungstag. Das ist eine einzige delegierbare Abfrage (`First(Sort(Filter(…)))`). Die Knöpfe vergleichen dann nur noch Zahlen. Das bewertet dasselbe wie heute: Ein Plus-Knopf ist gesperrt genau dann, wenn eine Buchung mit `Startzeit < neues Ende` und `Endzeit > altes Ende` existiert (geschlussfolgert, gleichwertig umgeformt). Dazu kommt die 22:00-Grenze.

**Richtig benannt:** Der Dialog `conVerwaltenDialog` wird **vom Dashboard** geöffnet (`galTischbuchungenHeute > btnVerwalten`), nicht vom Grundriss. Eine Kachel im Grundriss öffnet das Details-Popup (`btnHitArea` → `varZeigeDetails`), belegt. v1 nannte ihn „Grundriss-Dialog“, deshalb war der B3-Test dort nicht ausführbar.

**Weil sich die Daten ändern können, während der Dialog offen ist,** prüft der Speichern-Knopf (A6/A7) **beim Klick** noch einmal frisch am Server. Wie in der Handy-App stehen die Werte dabei in globalen Variablen, weil die Handy-App nur so delegierbare Filter bekam (belegt, E-06 Punkt 2).

### A1 `btnVerwalten.OnSelect`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnVerwalten`

`btnVerwalten.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnVerwalten.OnSelect` ersetzen durch**

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

**Test:** Dashboard → bei einer heutigen Buchung „Verwalten“: +1/+2/+3 Std sind grün, wenn dahinter frei ist. Ist ein Knopf grau, dann reicht er in eine Folgebuchung oder über 22:00. Monitor (optional): beim Öffnen genau 1 Abfrage auf `Tischbuchungen`.

### A2 `btnVerwalten_2.OnSelect`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > btnVerwalten_2`

Änderung an `btnVerwalten_2.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -4,4 +4,10 @@
   Set(varZeigeVerwaltenKlein; true);
   Set(varSelectedBuchungTab; ThisItem);;
+  Set(varVerlTisch; ThisItem.Tisch.Value);;
+  Set(varVerlEndeAlt; ThisItem.Endzeit);;
+  Set(varVerlTagesende; DateAdd(ThisItem.Startzeit; 22 * 60 - (Hour(ThisItem.Startzeit) * 60 + Minute(ThisItem.Startzeit)); TimeUnit.Minutes));;
+  Set(varVerlNaechste; First(Sort(Filter(Tischbuchungen; Tisch.Value = varVerlTisch && Endzeit > varVerlEndeAlt && Startzeit < varVerlTagesende); Startzeit; SortOrder.Ascending)));;
+  Set(varVerlGrenzeTab; If(IsBlank(varVerlNaechste.ID) || varVerlNaechste.Startzeit > varVerlTagesende; varVerlTagesende; varVerlNaechste.Startzeit));;
+  Set(varAusgewaehltePlusDauer; Blank());;
   Set(varZeigeVerwaltenTab; true);;
   Set(varZeigeCheckin; false);;
```

**Einfügen: ganze Property `btnVerwalten_2.OnSelect` ersetzen durch**

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

**Test:** Tab „Buchungen“ → Buchung A verwalten, +3 wählen, schließen. Buchung B verwalten: **keine** Dauer ist vorausgewählt (vorher blieb +3 stehen). Auswahlmodus an: Klick öffnet wie bisher den kleinen Dialog.

### A3 `btnPlus1Std.DisplayMode`, `btnPlus1Std.Fill`, `btnPlus2Std.DisplayMode`, `btnPlus2Std.Fill`, `btnPlus3Std.DisplayMode`, `btnPlus3Std.Fill`

Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std`

`btnPlus1Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus1Std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conVerwaltenDialog > btnPlus1Std`

`btnPlus1Std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus1Std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std`

`btnPlus2Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus2Std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conVerwaltenDialog > btnPlus2Std`

`btnPlus2Std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus2Std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std`

`btnPlus3Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus3Std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenze; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conVerwaltenDialog > btnPlus3Std`

`btnPlus3Std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus3Std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchung.ID) || DateAdd(varSelectedBuchung.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenze;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**Test:** wie A1. Zusätzlich eine Buchung, die um 20:30 endet: +1 grün, +2 grau (würde 22:30).

### A4 `btnPlus1Std_1.DisplayMode`, `btnPlus1Std_1.Fill`, `btnPlus2Std_1.DisplayMode`, `btnPlus2Std_1.Fill`, `btnPlus3Std_1.DisplayMode`, `btnPlus3Std_1.Fill`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1`

`btnPlus1Std_1.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus1Std_1.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus1Std_1`

`btnPlus1Std_1.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus1Std_1.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 60; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1`

`btnPlus2Std_1.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus2Std_1.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus2Std_1`

`btnPlus2Std_1.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus2Std_1.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 120; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1`

`btnPlus3Std_1.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus3Std_1.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenzeTab; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnPlus3Std_1`

`btnPlus3Std_1.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnPlus3Std_1.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = 180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; 180; TimeUnit.Minutes) > varVerlGrenzeTab;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**Test (B0):** Im Dashboard Buchung A verwalten, schließen. Im Tab Buchung B verwalten, wobei hinter B direkt jemand gebucht hat: +1 ist **grau**. Vorher richtete sich die Farbe nach A.

### A5 `btnMinus1Std.DisplayMode`, `btnMinus1Std.Fill`, `btnMinus2Std.DisplayMode`, `btnMinus2Std.Fill`, `btnMinus3std.DisplayMode`, `btnMinus3std.Fill`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std`

`btnMinus1Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus1Std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -60; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus1Std`

`btnMinus1Std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus1Std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = -60;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -60; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std`

`btnMinus2Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus2Std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -120; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus2Std`

`btnMinus2Std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus2Std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = -120;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -120; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std`

`btnMinus3std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus3std.DisplayMode` ersetzen durch**

```
If(IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -180; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit; DisplayMode.Disabled; DisplayMode.Edit)
```

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnMinus3std`

`btnMinus3std.Fill` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnMinus3std.Fill` ersetzen durch**

```
If(
  varAusgewaehltePlusDauer = -180;
  ColorValue("#00A96B");
  If(
    IsBlank(varSelectedBuchungTab.ID) || DateAdd(varSelectedBuchungTab.Endzeit; -180; TimeUnit.Minutes) <= varSelectedBuchungTab.Startzeit;
    ColorFade(ColorValue("#EB3951"); 70%);
    ColorFade(ColorValue("#00A96B"); 70%)
  )
)
```

**Test:** Buchung 2 Std lang: −1 grün, −2 und −3 grau.

### A6 `btnVerlängern.OnSelect`, `btnVerlängern.DisplayMode`

Ablauf, gleich wie in der Handy-App (`btnVerl1`): Sperre → Buchung frisch laden → keine Dauer (auch `0`, BD-12)? → gelöscht? → würde leer? → über 22:00? → Tisch inzwischen belegt? → speichern in `IfError` → **nachlesen**, ob das neue Ende angekommen ist → Meldung → immer: `Refresh`, Grundriss neu laden, Dauer leeren, Sperre 2 s, Ladeanzeige aus. Der Knopf ist erst bedienbar, wenn eine Dauer gewählt ist.

Ort: `Screen1 > conVerwaltenDialog > btnVerlängern`

`btnVerlängern.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnVerlängern.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
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
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);
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

Ort: `Screen1 > conVerwaltenDialog > btnVerlängern`

**`btnVerlängern.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** (1) +1 Std → „Buchung geändert, neues Ende hh:mm Uhr.“, Dialog zu, Dashboard-Karte und Kachel stimmen. (2) **Doppelklick** auf Verlängern → genau +1 Std. (3) Zwei Browser-Tabs: In Tab 2 direkt hinter die Buchung buchen, in Tab 1 (Dialog war schon offen, +1 grün) verlängern → „Der Tisch ist in dieser Zeit inzwischen belegt…“. (4) In Tab 2 die Buchung stornieren, in Tab 1 verlängern → „Diese Buchung gibt es nicht mehr…“, Dialog zu.

### A7 `btnVerlängern_1.OnSelect`, `btnVerlängern_1.DisplayMode`

Wie A6, für den Tab (`varSelectedBuchungTab`, `varZeigeVerwaltenTab`). Verkürzen läuft über dieselbe Formel (negative Dauer). Weggefallen sind `Clear(colAusgewaehlteBuchungen)` und `Set(varMehrfachAuswahlModus; false)`: Der Tab-Dialog öffnet sich nur außerhalb des Auswahlmodus, dann ist die Auswahl leer. `varMehrfachAuswahlModus` liest niemand (BD-21, belegt).

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1`

`btnVerlängern_1.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnVerlängern_1.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
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
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);
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

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1`

**`btnVerlängern_1.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading || IsBlank(varAusgewaehltePlusDauer) || varAusgewaehltePlusDauer = 0; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** wie A6 im Tab, dazu −1 Std → „neues Ende …“. Ein Doppelklick auf Speichern verkürzt nur einmal.

### A8 `btnStornieren.OnSelect`, `btnStornieren.DisplayMode`

Behebt den gemeldeten Fehler „Item Not Found“ (BD-05, geschlussfolgert): Heute löscht der Knopf `Remove(Tischbuchungen; varSelectedBuchung)`, also den Stand vom Öffnen des Dialogs, ohne `IfError`. Neu: frisch laden, löschen in `IfError`, nachlesen.

Ort: `Screen1 > conVerwaltenDialog > btnStornieren`

`btnStornieren.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnStornieren.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwalten; false);
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

Ort: `Screen1 > conVerwaltenDialog > btnStornieren`

**`btnStornieren.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** Dashboard → Verwalten → Stornieren → „Buchung storniert.“, Karte weg, Kachel grün. Zwei-Tab-Test: In Tab 2 stornieren, in Tab 1 noch einmal stornieren → „Diese Buchung gibt es nicht mehr…“ (kein roher Fehler).

### A9 `btnStornieren_1.OnSelect`, `btnStornieren_1.DisplayMode`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1`

`btnStornieren_1.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnStornieren_1.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varStornoBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchungTab.ID));;
  If(
    IsBlank(varStornoBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Die Liste wurde aktualisiert."; NotificationType.Warning);;
    Set(varZeigeVerwaltenTab; false);
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

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnStornieren_1`

**`btnStornieren_1.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** wie A8 im Tab.

### A10 `btnEinchecken.OnSelect`, `btnEinchecken.DisplayMode`

Einchecken liest frisch, prüft das Fenster (E3), schreibt in `IfError` und liest nach. Die Grundriss-Ladezeile bleibt. Auschecken bleibt jederzeit möglich.

Ort: `Screen1 > conCheckinDialog > btnEinchecken`

`btnEinchecken.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnEinchecken.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
  Set(varIsLoading; true);;
  Set(varCheckinBuchung; LookUp(Tischbuchungen; ID = varSelectedBuchung.ID));;
  If(
    IsBlank(varCheckinBuchung.ID);
    Notify("Diese Buchung gibt es nicht mehr. Bitte aktualisieren."; NotificationType.Warning);;
    Set(varZeigeCheckin; false);
    !varCheckinBuchung.CheckedIn && (Now() < DateAdd(varCheckinBuchung.Startzeit; -30; TimeUnit.Minutes) || Now() > varCheckinBuchung.Endzeit);
    Notify("Einchecken ist erst ab 30 Minuten vor Beginn und nur bis zum Ende möglich."; NotificationType.Warning);
    IfError(
      Patch(Tischbuchungen; varCheckinBuchung; {CheckedIn: !varCheckinBuchung.CheckedIn});
      Notify("Speichern fehlgeschlagen. Bitte erneut versuchen."; NotificationType.Error);
      Set(varSelectedBuchung; LookUp(Tischbuchungen; ID = varCheckinBuchung.ID));;
      If(
        varSelectedBuchung.CheckedIn <> varCheckinBuchung.CheckedIn;
        Notify(If(varSelectedBuchung.CheckedIn; "Eingecheckt."; "Ausgecheckt."); NotificationType.Success);;
        Set(varZeigeCheckin; false);
        Notify("Die Änderung ist nicht angekommen. Bitte aktualisieren."; NotificationType.Warning)
      )
    )
  );;
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

Ort: `Screen1 > conCheckinDialog > btnEinchecken`

**`btnEinchecken.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** Heutige Buchung, die in mehr als 30 Minuten beginnt → „Einchecken ist erst ab 30 Minuten vor Beginn…“. Laufende Buchung → „Eingecheckt.“, Kachel rot. Noch einmal → „Ausgecheckt.“.

## Teil B: Neue Buchung speichern

**Ein Ablauf für beide Knöpfe** (der Buchungsdialog aus dem Grundriss und das Tische-Panel): Sperre → Werte zum Klickzeitpunkt in Variablen → Termine berechnen (wie bisher: Kappung auf Start + 14 Tage, Wochentage). Der unerreichbare Zweig „Taeglich“ entfällt (BD-24, `varWiederholenModus` wird nur auf „Wochentage“ gesetzt, belegt) → Plausibilität mit je eigener Meldung → **eine** Abfrage „Tisch belegt?“ und **eine** „ich schon gebucht?“, beide nur im Zeitraum der Serie (K4.1, delegierbar) → je Termin frei / Tisch belegt / ich belegt → **Sammel-Patch** der freien Termine mit gemeinsamer `SerienID` → **Nachlese** (dieselbe Zeitraum-Abfrage): Wie viele meiner Zeilen sind wirklich angekommen? Hat jemand mit kleinerer ID gleichzeitig denselben Tisch gebucht (Regel der Handy-App, nimmt nichts automatisch zurück)? → eine Meldung → nur wenn etwas gebucht wurde: Dialog schließen und Eingaben leeren (BD-11).

**Warum `SerienID` jetzt geschrieben wird:** Die Spalte gibt es schon (Text, filterbar, belegt in `DataSources.json`), sie war nur nie befüllt. So lässt sich nach dem Sammel-Patch exakt zählen, was angekommen ist (Frage 14), und eine Serie später gemeinsam finden (E-4). Der Aufräum-Flow wird nicht berührt (geschlussfolgert, er löscht nach Datum).

### B1 `btnSpeichern.OnSelect`, `btnSpeichern.DisplayMode`

Ort: `Screen1 > conBuchungDialog > btnSpeichern`

`btnSpeichern.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnSpeichern.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
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
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr."; NotificationType.Success);
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
    Refresh(Tischbuchungen);;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

Ort: `Screen1 > conBuchungDialog > btnSpeichern`

**`btnSpeichern.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** (1) Grundriss → freie Kachel → Buchen ohne Wiederholen → „Gebucht: OG Desk 5, 08.10., 09:00 bis 10:00 Uhr.“. In SharePoint (Listenansicht „Tischbuchungen“) hat die neue Zeile eine `SerienID`. (2) Serie Mo–Fr, 2 Wochen → „Gebucht: …, 10 Termine ab …“ oder, wenn Tage belegt sind, „8 von 10 Terminen gebucht (…). 2× war der Tisch schon belegt.“. (3) Bis-Datum 4 Wochen → Meldung endet mit „Die Wiederholung wurde auf 2 Wochen begrenzt.“. (4) Zur selben Zeit schon einen anderen Tisch gebucht → „Du hast in dieser Zeit schon einen Tisch gebucht.“, Dialog bleibt offen. (5) Datum gestern → „Diese Zeit liegt in der Vergangenheit…“. (6) **Doppelklick** auf Speichern → nur eine Buchung.

### B2 `btnSpeichernTischePanel.OnSelect`, `btnSpeichernTischePanel.DisplayMode`

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel`

`btnSpeichernTischePanel.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnSpeichernTischePanel.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
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
      ClearCollect(colNeuNachlese; Filter(Tischbuchungen; Tisch.Value = varNeuTischTitel && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
      Set(varNeuAnzahl; CountRows(Filter(colNeuNachlese; SerienID = varSerienID)));;
      Set(varNeuKonflikt; CountRows(Filter(colNeuNachlese As N; N.SerienID = varSerienID && !IsBlank(LookUp(colNeuNachlese As M; M.ID < N.ID && M.Startzeit < N.Endzeit && M.Endzeit > N.Startzeit).ID))));;
      If(
        varNeuAnzahl = 0;
        Notify(If(varNeuFehler; "Speichern fehlgeschlagen. Es wurde nichts gebucht. Bitte erneut versuchen."; "Die Buchung ist nicht angekommen. Bitte unter Buchungen prüfen."); NotificationType.Error);
        varNeuKonflikt > 0;
        Notify("Achtung: Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht (" & varNeuKonflikt & " Termin(e)). Bitte unter Buchungen prüfen und die doppelten stornieren."; NotificationType.Error);
        varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr."; NotificationType.Success);
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
    Refresh(Tischbuchungen);;
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel`

**`btnSpeichernTischePanel.DisplayMode` gibt es heute nicht (Standard). Neu setzen auf:**

```
If(varIsLoading || IsBlank(ddTischePanel.Selected.Titel); DisplayMode.Disabled; DisplayMode.Edit)
```

**Test:** wie B1 über „Tisch Buchen“ im Dashboard. Zusätzlich: Ohne gewählten Tisch ist Speichern grau. Nach dem Speichern springt die Ansicht wie bisher auf das Dashboard.

## Teil C: Tischauswahl im Tische-Panel

**Ablauf im Panel neu: erst Datum und Zeit, dann Tisch.** Die Tischliste rechnet mit denselben Terminen wie der Speichern-Knopf und holt dafür **eine** Abfrage „alle Buchungen im Zeitraum“ (delegierbar), dann wird lokal gerechnet. Die Liste zeigt nur Tische, die an **mindestens einem** Termin frei sind. Bei Serien steht dahinter z. B. „(an 2 von 10 Tagen belegt)“. Sortierung: ganz freie zuerst, dann das gerade gewählte Stockwerk, dann nach Nummer (Muster aus der Handy-App, `Desk 2` vor `Desk 10`). Bei geschlossenem Panel fragt die Liste nichts ab.

**Sicherheitsnetz (wichtig):** Ändert sich die Zeit, nachdem ein Tisch gewählt wurde, berechnet sich die Liste neu. Ob die klassische Auswahlliste den gewählten Tisch dann behält oder leert, ist UNSICHER (U-C1). Deshalb ist kein Tisch vorausgewählt (`Default` leer, `AllowEmptySelection` an), Speichern ist ohne Tisch grau, die Erfolgsmeldung nennt den Tisch, und Speichern prüft am Server noch einmal. Ein stiller Wechsel auf einen anderen Tisch ist so ausgeschlossen (geschlussfolgert).

**Optional, nicht nötig:** Die Tischauswahl im Panel nach unten unter die Zeit ziehen (nur Y-Position), damit die Reihenfolge auf dem Bildschirm der Logik folgt.

### C1 `ddTischePanel.Items`, `ddTischePanel.Items.Value`, `ddTischePanel.AllowEmptySelection`, `ddTischePanel.Default`

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`

`ddTischePanel.Items` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `ddTischePanel.Items` ersetzen durch**

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
          spanStart: If(IsEmpty(termine); datum + startZeit; First(termine).Start);
          spanEnde: If(IsEmpty(termine); datum + endeZeit; Last(termine).Ende)
        };
        With(
          { belegt: If(varZeigeTischBuchungForm; ForAll(Filter(Tischbuchungen; Startzeit < spanEnde && Endzeit > spanStart); {TischName: Tisch.Value; Beginn: Startzeit; Schluss: Endzeit})) };
          SortByColumns(
            Filter(
              ForAll(
                Tische As X;
                With(
                  { n: CountRows(Filter(termine As Z; !IsBlank(LookUp(belegt; TischName = X.Titel && Beginn < Z.Ende && Schluss > Z.Start).TischName))) };
                  {
                    Titel: X.Titel;
                    ID: X.ID;
                    Belegt: n;
                    Etage: If(X.Geschoss.Value = varAusgewaehltesStockwerk; 0; 1);
                    Schluessel: X.Geschoss.Value & Left(X.Titel; Len(X.Titel) - Len(Last(Split(X.Titel; " ")).Value)) & Text(IfError(Value(Last(Split(X.Titel; " ")).Value); 0); "000");
                    Anzeige: X.Titel & If(n = 0; ""; "  (an " & n & " von " & CountRows(termine) & " Tagen belegt)")
                  }
                )
              );
              !("big table" in Lower(Titel)) && (Belegt = 0 || Belegt < CountRows(termine))
            );
            "Belegt"; SortOrder.Ascending;
            "Etage"; SortOrder.Ascending;
            "Schluessel"; SortOrder.Ascending
          )
        )
      )
    )
  )
)
```

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`

`ddTischePanel.Items.Value` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `ddTischePanel.Items.Value` ersetzen durch**

```
Anzeige
```

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`

**`ddTischePanel.AllowEmptySelection` gibt es heute nicht (Standard). Neu setzen auf:**

```
true
```

Ort: `Screen1 > conTischBuchungenPanel > ddTischePanel`

**`ddTischePanel.Default` gibt es heute nicht (Standard). Neu setzen auf:**

```
Blank()
```

**Test:** (1) Panel öffnen: kein Tisch gewählt, Speichern grau. (2) Heute 09:00–10:00: belegte Tische fehlen, Big Table fehlt, Stockwerk des Grundrisses zuerst, `OG Desk 2` vor `OG Desk 10`. (3) Wiederholen Mo–Fr: Tische mit Hinweis „(an x von y Tagen belegt)“ stehen hinten. (4) Zeit ändern, nachdem ein Tisch gewählt war: Wird die Auswahl geleert oder bleibt sie? → im Testbogen notieren (U-C1). (5) App-Prüfung: Delegierungswarnung bei `ddTischePanel.Items` → notieren (U-V3).

### C2 `btnTischHinzufügen.OnSelect`

Ort: `Screen1 > conDashboard > btnTischHinzufügen`

Änderung an `btnTischHinzufügen.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -1,3 +1,5 @@
 Set(varZeigeTischBuchungForm; true);;
+Reset(dpDatumTischePanel);;
+Reset(ddTischePanel);;
 Set(varWiederholen; false);;
 Reset(chkWiederholenPanel);;
```

**Einfügen: ganze Property `btnTischHinzufügen.OnSelect` ersetzen durch**

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

**Test:** Tisch wählen, Panel schließen (Pfeil „<“), wieder öffnen → kein Tisch gewählt, Datum = Ansichtsdatum.

### C3 `btn5Std.DisplayMode`, `btn5Std.Fill`, `btn5Std.OnSelect`

Ort: `Screen1 > conTischBuchungenPanel > btn5Std`

`btn5Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btn5Std.DisplayMode` ersetzen durch**

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
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
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

Ort: `Screen1 > conTischBuchungenPanel > btn5Std`

Änderung an `btn5Std.Fill` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -1,8 +1,8 @@
 With(
-  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
+  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
   With(
     {
-      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
-      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
+      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
+      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 5; TimeUnit.Hours);
       tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
     };
@@ -14,8 +14,8 @@
         ColorFade(ColorValue("#EB3951"); 70%);
         If(
-          IsBlank(ddTischePanel.Selected);
+          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
           ColorFade(ColorValue("#00A96B"); 70%);
           If(
-            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
+            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
             ColorFade(ColorValue("#00A96B"); 70%);
             ColorFade(ColorValue("#EB3951"); 70%)
```

**Einfügen: ganze Property `btn5Std.Fill` ersetzen durch**

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
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
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

Ort: `Screen1 > conTischBuchungenPanel > btn5Std`

Änderung an `btn5Std.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -2,5 +2,5 @@
   { warAusgewaehlt: varAusgewaehltePanelDauer = 5 };
   With(
-    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
+    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
     With(
       {
```

**Einfügen: ganze Property `btn5Std.OnSelect` ersetzen durch**

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 };
  With(
    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 5));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

**Test:** Panel, Datum morgen → „5 Std“ grün; klicken → Start 08:00, Ende 13:00. Heute nach 17:00 → „5 Std“ grau. Mit gewähltem, ab jetzt belegtem Tisch → grau.

### C4 `btn9Std.DisplayMode`, `btn9Std.Fill`, `btn9Std.OnSelect`

Ort: `Screen1 > conTischBuchungenPanel > btn9Std`

`btn9Std.DisplayMode` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btn9Std.DisplayMode` ersetzen durch**

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
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
          IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
          DisplayMode.Edit;
          DisplayMode.Disabled
        )
      )
    )
  )
)
```

Ort: `Screen1 > conTischBuchungenPanel > btn9Std`

Änderung an `btn9Std.Fill` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -1,8 +1,8 @@
 With(
-  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
+  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
   With(
     {
-      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
-      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
+      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0);
+      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenStart/60; 0); Mod(minutenStart; 60); 0); 9; TimeUnit.Hours);
       tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
     };
@@ -14,8 +14,8 @@
         ColorFade(ColorValue("#EB3951"); 70%);
         If(
-          IsBlank(ddTischePanel.Selected);
+          !varZeigeTischBuchungForm || IsBlank(ddTischePanel.Selected.Titel);
           ColorFade(ColorValue("#00A96B"); 70%);
           If(
-            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
+            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
             ColorFade(ColorValue("#00A96B"); 70%);
             ColorFade(ColorValue("#EB3951"); 70%)
```

**Einfügen: ganze Property `btn9Std.Fill` ersetzen durch**

```
With(
  { minutenStart: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
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
            IsBlank(LookUp(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit).ID);
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

Ort: `Screen1 > conTischBuchungenPanel > btn9Std`

Änderung an `btn9Std.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -2,5 +2,5 @@
   { warAusgewaehlt: varAusgewaehltePanelDauer = 9 };
   With(
-    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
+    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
     With(
       {
```

**Einfügen: ganze Property `btn9Std.OnSelect` ersetzen durch**

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 };
  With(
    { minutenJetzt: If(dpDatumTischePanel.SelectedDate = Today(); 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0); 8 * 60) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 9));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

**Test:** wie C3 mit 9 Std (morgen 08:00–17:00).

### C5 `Label14.Text`

Ort: `Screen1 > conTischBuchungenPanel > Label14`

Änderung an `Label14.Text` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -1,4 +1,4 @@
 If(
-  DateDiff(dpDatum.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
+  DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
   "*Zu weit gewählt —      es werden 2 Wochen gespeichert";
   "*Wiederholung nur für max. 2 Wochen möglich"
```

**Einfügen: ganze Property `Label14.Text` ersetzen durch**

```
If(
  DateDiff(dpDatumTischePanel.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  "*Zu weit gewählt —      es werden 2 Wochen gespeichert";
  "*Wiederholung nur für max. 2 Wochen möglich"
)
```

**Test:** Panel → Wiederholen an → Bis-Datum 3 Wochen nach dem Panel-Datum → Text „*Zu weit gewählt …“. Vorher las der Text das Datum aus dem Buchungsdialog.

## Teil D: Kleinigkeiten

### D1 `ddStockwerk.OnSelect`

Ort: `Screen1 > conGrundriss > ddStockwerk`

Änderung an `ddStockwerk.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -7,4 +7,4 @@
 Set(varSelectedTisch; Blank());;
 Set(varSelectedBuchung; Blank());;
-Set(varAusgewaehltePlusDauer; 0)
+Set(varAusgewaehltePlusDauer; Blank())
 
```

**Einfügen: ganze Property `ddStockwerk.OnSelect` ersetzen durch**

```
Set(varStockwerkDropdownOffen; true);;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedTisch; Blank());;
Set(varSelectedBuchung; Blank());;
Set(varAusgewaehltePlusDauer; Blank())

```

**Test:** Stockwerk wechseln, danach eine Buchung verwalten → keine Dauer vorausgewählt, Verlängern grau.

### D2 `Icon1.OnSelect`, `Icon1_1.OnSelect`, `Image6.OnSelect`, `btnHitArea_1.OnSelect`

Ort: `Screen1 > conBuchungen > Icon1`

`Icon1.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `Icon1.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

Ort: `Screen1 > conDashboard > Icon1_1`

`Icon1_1.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `Icon1_1.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

Ort: `Screen1 > conHeader > Image6`

`Image6.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `Image6.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

Ort: `Screen1 > conHeader > btnHitArea_1`

`btnHitArea_1.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnHitArea_1.OnSelect` ersetzen durch**

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte erneut auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu);; Notify("Aktualisiert."; NotificationType.Success)));;
Set(varIsLoading; false)
```

**Test:** Aktualisieren (Dashboard, Buchungen, Kopfzeile, Profil) → „Aktualisiert.“. WLAN aus → nur die gelbe Grundriss-Warnung, nicht zusätzlich „Aktualisiert.“.

### D3 `btnStornierenKlein.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenKlein > btnStornierenKlein`

`btnStornierenKlein.OnSelect` wird komplett neu geschrieben (Original in Anhang 1).

**Einfügen: ganze Property `btnStornierenKlein.OnSelect` ersetzen durch**

```
If(
  !varIsLoading && Now() >= varSperreBis;
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

**Test:** Mehrfachauswahl, 2 Buchungen, Doppelklick auf Stornieren → „2 Buchungen storniert.“, keine zweite Meldung „gibt es nicht mehr“.

### D4 `btnAbbrechenTischePanel.OnSelect`

Ort: `Screen1 > conTischBuchungenPanel > btnAbbrechenTischePanel`

Änderung an `btnAbbrechenTischePanel.OnSelect` (rot = weg, grün = neu, Rest unverändert):
```diff
--- 
+++ 
@@ -1,3 +1,2 @@
-Set(varZeigeTischBuchungForm; false);;
 Set(varZeigeTischBuchungForm; false);;
 Set(varWiederholen; false);;
```

**Einfügen: ganze Property `btnAbbrechenTischePanel.OnSelect` ersetzen durch**

```
Set(varZeigeTischBuchungForm; false);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel)
```

**Test:** Panel öffnen und mit „<“ schließen wie bisher.

## Rückfall
- **Ein Schritt:** Original aus Anhang 1 einfügen. Für Properties, die es vorher nicht gab: `DisplayMode` → `DisplayMode.Edit`, `AllowEmptySelection` → `false`, `Default` (ddTischePanel) → Formel leeren, `Items.Value` → wieder `Titel` wählen.
- **Teil A zurück:** A3 bis A5 brauchen die Grenze aus A1/A2. Deshalb Teil A **ganz** zurücknehmen oder ganz behalten. B, C, D sind davon unabhängig.
- **Teil B zurück:** B1/B2 einzeln möglich. Bereits geschriebene `SerienID`-Werte stören nicht.
- **Teil C zurück:** C1 (vier Properties) zusammen zurücknehmen, sonst passt `Items.Value` nicht zu `Items`.
- **Schritt 0** zuletzt zurücknehmen: Ohne ihn sind alle Knöpfe mit Sperre ab App-Start 2 s gesperrt, danach normal (U-V1).
- **Komplett:** `.msapp`-Export oder Versionsverlauf.

## UNSICHER (mit Prüftest)
| # | Unsicherheit | Folge, falls falsch | Test |
|---|---|---|---|
| U-V1 | `Now() >= varSperreBis` mit leerem `varSperreBis`, falls Schritt 0 fehlt oder `OnStart` später fertig wird (nicht blockierendes OnStart) | Knopf reagiert in den ersten Sekunden nicht | Schritt 0 zuerst; direkt nach dem Start buchen |
| U-V2 | Die 2-Sekunden-Sperre fängt den eingereihten Zweitklick auch in der **PC**-App (in der Handy-App gemessen, gleiche App-Einstellungen, belegt `Properties.json`) | Doppelte Buchung/Verlängerung bei Doppelklick | Doppelklick-Tests A6, A7, B1 (6), D3 |
| U-V3 | `ddTischePanel.Items`: `ForAll(Tische …)` ist nicht delegierbar (Tische hat 34 Zeilen, belegt), deshalb vermutlich eine neue Delegierungswarnung. Die Abfrage auf `Tischbuchungen` ist delegierbar (nur `<`/`>` auf DateTime) | nur Warnung, kein Fehler, solange Tische < Datenzeilenlimit | App-Prüfung nach C1 |
| U-V4 | Datenzeilenlimit: Die Panel-Liste holt bei einer 2-Wochen-Serie **alle** Buchungen aller Tische im Zeitraum. Bei voller Auslastung über 500 Zeilen möglich (34 Tische × 15 Tage) | Liste zeigt einen Tisch als frei, der belegt ist. **Speichern prüft trotzdem richtig** (eigene, engere Abfrage) | App-Einstellungen → „Datenzeilenlimit“ ansehen und melden (Standard 500, max. 2000) |
| U-C1 | Behält die klassische Auswahlliste den gewählten Tisch, wenn sich `Items` neu berechnet? | Nutzer muss den Tisch nach einer Zeitänderung neu wählen (lästig, nicht gefährlich, siehe Sicherheitsnetz in Teil C) | C1-Test (4) |
| U-B1 | `SerienID` wird beim Sammel-Patch mitgeschrieben (Spalte vorhanden, read-write, belegt). Wenn nicht: Nachlese zählt 0 → Meldung „nicht angekommen“, obwohl gebucht ist | falsche rote Meldung. Ein erneuter Klick bucht **nicht** doppelt (Prüfung findet die eigene Buchung) | B1-Test (1): `SerienID` in der Liste gefüllt? |
| U-B2 | `Text(GUID())` liefert Text (App-Einstellung `useguiddatatypes` an, belegt) | rote Formel | App-Prüfung nach B1 |
| U-A1 | Gleichheit `Endzeit = varVerlEndeNeu` in der Nachlese (Muster aus der Handy-App) | falsche Meldung „nicht angekommen“ trotz Erfolg | A6-Test (1) |
| U-A2 | `First(Sort(Filter(…); Startzeit; SortOrder.Ascending))` ist delegierbar (Sort auf DateTime bei SharePoint) | Delegierungswarnung bei A1/A2 | App-Prüfung nach A1 |
| U-A3 | Mehrarmiges `If` mit Anweisungsketten in den Zweigen bei `powerfxv1 = false`. In der Handy-App mit denselben Einstellungen in Betrieb (belegt) | rote Formel | App-Prüfung nach A6 |

## Testbogen (abhaken, Ergebnis kurz melden)
| | Schritt | Ergebnis | Notiz |
|---|---|---|---|
| ☐ | 0 OnStart | | |
| ☐ | A1–A5 Dauer-Knöpfe Dashboard/Tab (inkl. B0-Test A4) | | |
| ☐ | A6/A7 Verlängern (inkl. Doppelklick, Zwei-Tab) | | |
| ☐ | A8/A9 Stornieren (inkl. Zwei-Tab) | | |
| ☐ | A10 Einchecken (Fenster, Ein/Aus) | | |
| ☐ | B1 Buchungsdialog (Einzel, Serie, Kappung, Person, Vergangenheit, Doppelklick, SerienID) | | |
| ☐ | B2 Panel speichern | | |
| ☐ | C1 Tischliste (frei, sortiert, Big Table, Serienhinweis; U-C1 notieren) | | |
| ☐ | C2–C5 Panel öffnen, 5/9 Std, Hinweistext | | |
| ☐ | D1–D4 Kleinigkeiten | | |
| ☐ | App-Prüfung: Anzahl Einträge vorher 134, nachher ___, neue Formelfehler ___ | | |
| ☐ | Monitor (optional): Serie 11 Termine über das Panel, nur diese Aktion | | erwartet deutlich unter 96 `getRows` (keine Abfragen der Dauer-Knöpfe mehr) |

## Unabhängige Prüfung
### a) Prüfung von Paket K v1 (Auftrag aus `01_PROMPT_fuer_den_Chat.md`, gegen den Export vom 07.10.)
| # | Frage | Ergebnis | Kennz. |
|---|---|---|---|
| 1 | Passen die Blöcke auf den veröffentlichten Stand? | Ja. Der Python-Leser liest alle 1.994 Properties genauso wie `props_de.json`. Die zehn Abweichungen sind nur Anführungszeichen-Reste des PowerShell-Lesers. L2-Ladezeile in B1, B3, C1, C2 vorhanden, Klammern ok. | belegt |
| 2a | B1/B3 Kollisionsprüfung gleichwertig zu den Plus-Knöpfen? | Ja, wortgleich. | belegt |
| 2b | `varIsLoading` auf jedem Pfad zurück? | Ja, die Zeilen stehen nach dem äußeren `With`. | belegt |
| 2c | Ungenannte Verhaltensänderung / Fehler | **(1)** Mit `varAusgewaehltePlusDauer = 0` (nach Stockwerkwechsel, BD-12) schreibt v1 dasselbe Ende und meldet „Buchung geändert“. **(2)** Im Tab bleibt die zuletzt gewählte Dauer stehen (`btnVerwalten_2` leert sie nicht, das Dashboard schon), v1 behebt das nicht. **(3)** B3-Test „über den Grundriss“ ist nicht ausführbar, der Dialog hängt am Dashboard. | belegt |
| 2d | `Date(…) + Time(22; 0; 0)` (U-K1) | Plausibel, aber unnötig: Die Handy-App rechnet `DateAdd(Startzeit; 22*60 − Minuten des Starts; Minutes)` und ist damit in Betrieb. v2 übernimmt das. | geschlussfolgert |
| 3 | Nebenwirkungen von A1 (K1) | Kein Typkonflikt: Alle Quellen von `varSelectedBuchung` sind Datensätze aus `Tischbuchungen` (Galerien, `LookUp`, `Patch`). Check-in, Details und `conCheckinDialog.Y` bleiben unberührt, weil A1 deren Sichtbarkeit auf falsch setzt. **Lücke:** Bleibt der Tab-Dialog offen, und man verwaltet inzwischen im Dashboard eine andere Buchung, zeigen die Tab-Knöpfe wieder die falsche Buchung. v2 löst B0 deshalb an der Wurzel (Tab liest `varSelectedBuchungTab`). | belegt / geschlussfolgert |
| 4 | K5: hält die DisplayMode-Sperre? | **Nein.** In der Handy-App am 06.10. gemessen: Doppeltipp verlängert zweimal trotz `DisplayMode`. U-K3 aus v1 war berechtigt, und der B2-Test hätte versagt. v2: Zweifach-Sperre wie in der Handy-App (E-07). | belegt (gemessen in der Handy-App) |
| 5 | K4.2 verwerfen? Test-Reihenfolge? | Begründung stimmt. Reihenfolge A vor B ok, nur der B3-Test war falsch (siehe 2c). | belegt |
| 6 | E1/E2/E3 mit den Messdaten | E1 ablehnen: passt (Handy V5). E2 drinlassen: passt (Trace 5 fehlerfrei; v2 sichert den Mehrfach-Knopf zusätzlich gegen Doppelklick ab). E3 drinlassen: passt (Trace 4, ~4,7 s). | gemessen / belegt |
| 7 | Fehlt etwas Wichtiges? | **Ja:** BD-05 („Item Not Found“), BD-06 (zwei Tische zur selben Zeit; die Handy-App verhindert es, die PC-App nicht), BD-19 (Vergangenheit), BD-15 (Check-in-Fenster), unterschiedliche Regeln PC/Handy, Tischauswahl (E-1, Frage 21). v2 baut alles davon ein. | belegt |

**Weitere Funde beim Lesen des ganzen Exports (v2 behebt sie):** `ddStockwerk.OnSelect` setzt die Dauer auf `0` (BD-12). Die vier Aktualisieren-Knöpfe überdecken die Grundriss-Warnung (BD-10). Das Panel liest im Hinweistext das falsche Datum (BD-26). Die Panel-Knöpfe 5/9 Std fragen auch bei geschlossenem Panel ab. `chkAuswahl.X` liest schon `btnVerwalten_2` (**BD-18 ist bereits erledigt**, belegt).

### b) Prüfung von v2
Noch ausstehend.

## Bewusst nicht in diesem Paket
| Vorhaben | Warum nicht jetzt |
|---|---|
| L4 Raumcode stilllegen (BD-22, −36 Abfragen beim Start), tote Variablen (BD-21) | Du musst bestätigen, dass Raumbuchung nicht gebraucht wird (Frage 11) |
| Bestätigung vor dem Stornieren (Handy V8) | braucht ein neues Steuerelement (Dialog), eigenes kleines Paket |
| Vorprüfung mit Alternativtischen für Serien (E-2) | mit C1 ist der größte Teil erreicht: Die Liste zeigt je Tisch, an wie vielen Tagen er belegt ist. Ersatztische je Konflikttag sind ein eigenes Konzept |
| Mehrfach-Verlängern (E-3) | acht Entwürfe verworfen, eigenes Konzept |
| Listen-Galerien (`galTischbuchungenHeute`, `galAlleTischbuchungen`) | fragen bei jedem `Refresh` neu ab (~24 Abfragen je Schreibvorgang). Das ist gewollt, sie zeigen die eigenen Buchungen |
| Buchungen-Tab „manchmal leer“ (D3 in der Gesamtliste, Frage 15) | Ursache nicht aus dem Code ableitbar, braucht einen Trace im Moment des Fehlers |
| Statusfarbe eingecheckt (BD-14) | Grundriss rot = „besetzt“ aus Sicht anderer, Dashboard grün = „du bist eingecheckt“. Beides ist begründbar, kein Fehler |
| `dpWiederholenBis_1.OnChange` ohne Wirkung (BD-23) | harmlos, beim Aufräumen mit L4 |

## Regeln
Deutsche Schreibweise (`;` trennt, `;;` verkettet), keine Kommentare, immer die **ganze** Property ersetzen, ein Studio-Fenster, nach jedem Schritt App-Prüfung. Die zwei Speichern-, Verlängern- und Stornieren-Knöpfe sind **nicht** wortgleich: jeden einzeln einfügen. Neu erzeugen nach einem neuen Export: `python3 -I werkzeuge/paket_k_v2.py && python3 -I werkzeuge/doc_paket_k_v2.py`.

## Anhang 1: Originale (Rückfall, aus dem Export vom 07.10.)

### `App.OnStart`

```
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

### `btnVerwalten.OnSelect`

```
Set(varSelectedBuchung; ThisItem);;
Set(varZeigeVerwalten; true);;
Set(varZeigeCheckin; false);;
Set(varZeigeDetails; false);;
Set(varZeigeDialog; false);;
Set(varAusgewaehltePlusDauer; Blank())
```

### `btnVerwalten_2.OnSelect`

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

### `btnPlus1Std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus1Std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 60;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnPlus2Std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus2Std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 120;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnPlus3Std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus3Std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes);
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 180;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnPlus1Std_1.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus1Std_1.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 60; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 60;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnPlus2Std_1.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus2Std_1.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit; 120; TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit)) > 0
    };
    If(
      varAusgewaehltePlusDauer = 120;
      ColorValue("#00A96B");
      If(
        direktBesetzt;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnPlus3Std_1.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes); tischWert: aktuelleBuchung.Tisch.Value; endeAlt: aktuelleBuchung.Endzeit };
    If(
      CountRows(Filter(Tischbuchungen; Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnPlus3Std_1.Fill`

```
With({ aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) }; With({ tischWert: aktuelleBuchung.Tisch.Value; endeAlt: aktuelleBuchung.Endzeit; neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; 180; TimeUnit.Minutes) }; With({ direktBesetzt: CountRows(Filter(Tischbuchungen; Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt)) > 0 }; If(varAusgewaehltePlusDauer = 180; ColorValue("#00A96B"); If(direktBesetzt; ColorFade(ColorValue("#EB3951"); 70%); ColorFade(ColorValue("#00A96B"); 70%))))))
```

### `btnMinus1Std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnMinus1Std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -60; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -60;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnMinus2Std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnMinus2Std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -120; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -120;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnMinus3std.DisplayMode`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    { neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes) };
    If(
      neueEndzeit <= aktuelleBuchung.Startzeit;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btnMinus3std.Fill`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  With(
    {
      neueEndzeit: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes);
      zuKurz: DateAdd(aktuelleBuchung.Endzeit; -180; TimeUnit.Minutes) <= aktuelleBuchung.Startzeit
    };
    If(
      varAusgewaehltePlusDauer = -180;
      ColorValue("#00A96B");
      If(
        zuKurz;
        ColorFade(ColorValue("#EB3951"); 70%);
        ColorFade(ColorValue("#00A96B"); 70%)
      )
    )
  )
)
```

### `btnVerlängern.OnSelect`

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

### `btnVerlängern.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnVerlängern_1.OnSelect`

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

### `btnVerlängern_1.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnStornieren.OnSelect`

```
Remove(Tischbuchungen; varSelectedBuchung);; Set(varZeigeVerwalten; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

### `btnStornieren.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnStornieren_1.OnSelect`

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

### `btnStornieren_1.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnEinchecken.OnSelect`

```
With(
  { aktuelleBuchung: LookUp(Tischbuchungen; ID = varSelectedBuchung.ID) };
  Set(varSelectedBuchung; Patch(Tischbuchungen; aktuelleBuchung; {CheckedIn: !aktuelleBuchung.CheckedIn}))
);;
Set(varZeigeCheckin; false);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)))
```

### `btnEinchecken.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnSpeichern.OnSelect`

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

### `btnSpeichern.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnSpeichernTischePanel.OnSelect`

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

### `btnSpeichernTischePanel.DisplayMode`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `ddTischePanel.Items`

```
Tische
```

### `ddTischePanel.Items.Value`

```
Title
```

### `ddTischePanel.AllowEmptySelection`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `ddTischePanel.Default`

Gibt es im Export nicht. Rückfall: Property leeren bzw. auf den Standard setzen (siehe Abschnitt Rückfall).

### `btnTischHinzufügen.OnSelect`

```
Set(varZeigeTischBuchungForm; true);;
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

### `btn5Std.DisplayMode`

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btn5Std.Fill`

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 5;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          IsBlank(ddTischePanel.Selected);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

### `btn5Std.OnSelect`

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 5 };
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 5; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 5 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 5));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

### `btn9Std.DisplayMode`

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      endeZeit > tagesEnde || IsBlank(ddTischePanel.Selected) || CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) > 0;
      DisplayMode.Disabled;
      DisplayMode.Edit
    )
  )
)
```

### `btn9Std.Fill`

```
With(
  { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
  With(
    {
      startZeit: dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
      endeZeit: DateAdd(dpDatumTischePanel.SelectedDate + Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
      tagesEnde: dpDatumTischePanel.SelectedDate + Time(22; 0; 0)
    };
    If(
      varAusgewaehltePanelDauer = 9;
      ColorValue("#00A96B");
      If(
        endeZeit > tagesEnde;
        ColorFade(ColorValue("#EB3951"); 70%);
        If(
          IsBlank(ddTischePanel.Selected);
          ColorFade(ColorValue("#00A96B"); 70%);
          If(
            CountRows(Filter(Tischbuchungen; Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit)) = 0;
            ColorFade(ColorValue("#00A96B"); 70%);
            ColorFade(ColorValue("#EB3951"); 70%)
          )
        )
      )
    )
  )
)
```

### `btn9Std.OnSelect`

```
With(
  { warAusgewaehlt: varAusgewaehltePanelDauer = 9 };
  With(
    { minutenJetzt: 30 * RoundUp((Hour(Now())*60 + Minute(Now())) / 30; 0) };
    With(
      {
        startZeit: Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0);
        endeZeit: DateAdd(Time(RoundDown(minutenJetzt/60; 0); Mod(minutenJetzt; 60); 0); 9; TimeUnit.Hours);
        tagesEnde: Time(22; 0; 0)
      };
      If(
        !warAusgewaehlt && endeZeit > tagesEnde;
        Notify("Für 9 Std. ab jetzt reicht der Tag nicht mehr aus."; NotificationType.Warning);
        Set(varAusgewaehltePanelDauer; If(warAusgewaehlt; Blank(); 9));;
        Set(varStartOverridePanel; If(warAusgewaehlt; ""; Text(startZeit; "hh:mm")));;
        Set(varEndeOverridePanel; If(warAusgewaehlt; ""; Text(endeZeit; "hh:mm")))
      )
    )
  )
);;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel)
```

### `Label14.Text`

```
If(
  DateDiff(dpDatum.SelectedDate; dpWiederholenBis_1.SelectedDate; TimeUnit.Days) > 14;
  "*Zu weit gewählt —      es werden 2 Wochen gespeichert";
  "*Wiederholung nur für max. 2 Wochen möglich"
)
```

### `ddStockwerk.OnSelect`

```
Set(varStockwerkDropdownOffen; true);;
Set(varZeigeDialog; false);;
Set(varZeigeDetails; false);;
Set(varZeigeCheckin; false);;
Set(varZeigeVerwalten; false);;
Set(varZeigeVerlaengern; false);;
Set(varSelectedTisch; Blank());;
Set(varSelectedBuchung; Blank());;
Set(varAusgewaehltePlusDauer; 0)

```

### `Icon1.OnSelect`

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

### `Icon1_1.OnSelect`

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

### `Image6.OnSelect`

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

### `btnHitArea_1.OnSelect`

```
Set(varIsLoading; true);;
Refresh(Tischbuchungen);;
With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; neu)));;
Set(varIsLoading; false);;
Notify("Aktualisiert."; NotificationType.Success)
```

### `btnStornierenKlein.OnSelect`

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

### `btnAbbrechenTischePanel.OnSelect`

```
Set(varZeigeTischBuchungForm; false);;
Set(varZeigeTischBuchungForm; false);;
Set(varWiederholen; false);;
Reset(chkWiederholenPanel)
```

## Anhang 2: Maschinelle Prüfung

```
Erzeugt von werkzeuge/paket_k_v2.py aus dem Export vom 07.10.2026 (veröffentlicht, enthält L2).
54 Properties in 22 Schritten, 34 neue Variablen/Collections (vorher in der App unbenutzt: geprüft).
Je Property geprüft: Steuerelement im Export, Property vorhanden (ersetzen) bzw. noch nicht vorhanden (neu),
Klammern (englisch und deutsch), keine Kommentare, deutsch -> englisch ergibt wieder exakt die Vorlage,
alle var/col-Namen bekannt, alle Steuerelement-Namen im Export, Reset nur auf vorhandene Steuerelemente.

OK  0    App.OnStart                          ersetzen   106 Zeilen  +3/-0
OK  A1   btnVerwalten.OnSelect                ersetzen    11 Zeilen  +7/-2
OK  A2   btnVerwalten_2.OnSelect              ersetzen    16 Zeilen  +6/-0
OK  A3   btnPlus1Std.DisplayMode              ersetzen     1 Zeilen  +1/-11
OK  A3   btnPlus1Std.Fill                     ersetzen     9 Zeilen  +7/-15
OK  A3   btnPlus2Std.DisplayMode              ersetzen     1 Zeilen  +1/-11
OK  A3   btnPlus2Std.Fill                     ersetzen     9 Zeilen  +7/-15
OK  A3   btnPlus3Std.DisplayMode              ersetzen     1 Zeilen  +1/-11
OK  A3   btnPlus3Std.Fill                     ersetzen     9 Zeilen  +7/-16
OK  A4   btnPlus1Std_1.DisplayMode            ersetzen     1 Zeilen  +1/-11
OK  A4   btnPlus1Std_1.Fill                   ersetzen     9 Zeilen  +7/-15
OK  A4   btnPlus2Std_1.DisplayMode            ersetzen     1 Zeilen  +1/-11
OK  A4   btnPlus2Std_1.Fill                   ersetzen     9 Zeilen  +7/-15
OK  A4   btnPlus3Std_1.DisplayMode            ersetzen     1 Zeilen  +1/-11
OK  A4   btnPlus3Std_1.Fill                   ersetzen     9 Zeilen  +9/-1
OK  A5   btnMinus1Std.DisplayMode             ersetzen     1 Zeilen  +1/-11
OK  A5   btnMinus1Std.Fill                    ersetzen     9 Zeilen  +7/-16
OK  A5   btnMinus2Std.DisplayMode             ersetzen     1 Zeilen  +1/-11
OK  A5   btnMinus2Std.Fill                    ersetzen     9 Zeilen  +7/-16
OK  A5   btnMinus3std.DisplayMode             ersetzen     1 Zeilen  +1/-11
OK  A5   btnMinus3std.Fill                    ersetzen     9 Zeilen  +7/-16
OK  A6   btnVerlängern.OnSelect               ersetzen    40 Zeilen  +38/-11
OK  A6   btnVerlängern.DisplayMode            neu          1 Zeilen  +0/-0
OK  A7   btnVerlängern_1.OnSelect             ersetzen    40 Zeilen  +37/-13
OK  A7   btnVerlängern_1.DisplayMode          neu          1 Zeilen  +0/-0
OK  A8   btnStornieren.OnSelect               ersetzen    24 Zeilen  +24/-2
OK  A8   btnStornieren.DisplayMode            neu          1 Zeilen  +0/-0
OK  A9   btnStornieren_1.OnSelect             ersetzen    24 Zeilen  +22/-9
OK  A9   btnStornieren_1.DisplayMode          neu          1 Zeilen  +0/-0
OK  A10  btnEinchecken.OnSelect               ersetzen    26 Zeilen  +26/-6
OK  A10  btnEinchecken.DisplayMode            neu          1 Zeilen  +0/-0
OK  B1   btnSpeichern.OnSelect                ersetzen   134 Zeilen  +130/-109
OK  B1   btnSpeichern.DisplayMode             neu          1 Zeilen  +0/-0
OK  B2   btnSpeichernTischePanel.OnSelect     ersetzen   142 Zeilen  +138/-105
OK  B2   btnSpeichernTischePanel.DisplayMode  neu          1 Zeilen  +0/-0
OK  C1   ddTischePanel.Items                  ersetzen    53 Zeilen  +53/-1
OK  C1   ddTischePanel.Items.Value            ersetzen     1 Zeilen  +1/-1
OK  C1   ddTischePanel.AllowEmptySelection    neu          1 Zeilen  +0/-0
OK  C1   ddTischePanel.Default                neu          1 Zeilen  +0/-0
OK  C2   btnTischHinzufügen.OnSelect          ersetzen    21 Zeilen  +2/-0
OK  C3   btn5Std.DisplayMode                  ersetzen    23 Zeilen  +13/-5
OK  C3   btn5Std.Fill                         ersetzen    27 Zeilen  +5/-5
OK  C3   btn5Std.OnSelect                     ersetzen    22 Zeilen  +1/-1
OK  C4   btn9Std.DisplayMode                  ersetzen    23 Zeilen  +13/-5
OK  C4   btn9Std.Fill                         ersetzen    27 Zeilen  +5/-5
OK  C4   btn9Std.OnSelect                     ersetzen    22 Zeilen  +1/-1
OK  C5   Label14.Text                         ersetzen     5 Zeilen  +1/-1
OK  D1   ddStockwerk.OnSelect                 ersetzen     9 Zeilen  +1/-1
OK  D2   Icon1.OnSelect                       ersetzen     4 Zeilen  +2/-3
OK  D2   Icon1_1.OnSelect                     ersetzen     4 Zeilen  +2/-3
OK  D2   Image6.OnSelect                      ersetzen     4 Zeilen  +2/-3
OK  D2   btnHitArea_1.OnSelect                ersetzen     4 Zeilen  +2/-3
OK  D3   btnStornierenKlein.OnSelect          ersetzen    40 Zeilen  +39/-35
OK  D4   btnAbbrechenTischePanel.OnSelect     ersetzen     3 Zeilen  +0/-1

Gesamtprüfungen auf dem Stand NACH dem Paket:
OK  Schreibstellen auf Tischbuchungen (8): alle mit Zweifach-Sperre und L2-Ladezeile: btnEinchecken.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnStornieren.OnSelect, btnStornierenKlein.OnSelect, btnStornieren_1.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect
OK  Kein Steuerelement im Tab-Dialog (conVerwaltenDialog_1) liest noch varSelectedBuchung (Befund B0 geschlossen)
OK  Kein Plus-/Minus-Knopf fragt noch Tischbuchungen ab (vorher 24 Properties mit eigener Abfrage)
OK  Jede neue Variable wird mindestens einmal gesetzt; keine Property doppelt im Paket
```
