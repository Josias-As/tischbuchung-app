# P3 Nachtrag 6, Fassung 2: Verfallene Buchung – kein Check-in-Dialog, dafür „Neu buchen“ (10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`). Grundlage: **Export 10.11. 08:13 + P2 (Nachtrag 5) + P1 (Für andere buchen v2)**. `btnHitArea.OnSelect` rechnet gegen den Stand nach P1, alles andere gegen den Export. Erzeugt und geprüft mit `werkzeuge/nachtrag6_v2.py` (0 Fehler) und `werkzeuge/abstimmung.py`. Ersetzt Fassung 1 (`arbeit/2026-10-12_Nachtrag6/`, bleibt erhalten). **Nicht unabhängig geprüft** (Josias’ Entscheidung, 12.10.). In Studio nichts getestet.

## Kurzfassung
- **Fehler (belegt, von dir gemeldet):** Die ganze Karte in der Dashboard-Liste ist ein unsichtbarer Knopf (`btnEincheckenHeute`). Er öffnete auch bei „Verfallen“ den Check-in-Dialog.
- **R1:** Die Karte ist gesperrt, wenn die Buchung verfallen oder schon zu Ende ist. Eine laufende eingecheckte Buchung öffnet weiter den Dialog (Auschecken). `DisabledFill`/`DisabledBorderColor` werden transparent, sonst läge Hellgrau über der Karte (belegt: Standard).
- **R2 „Neu buchen“:** Bei einer verfallenen Buchung von heute steht statt „Verfallen“ ein blauer Knopf **„Neu buchen“**, wenn bis zum alten Ende noch mindestens eine halbe Stunde frei ist. Er öffnet den **vorhandenen** Buchungsdialog: Tisch wie vorher, Beginn ab der nächsten halben Stunde, Ende = altes Ende. Gespeichert wird mit `btnSpeichern`, also mit allen Prüfungen. Die eigene verfallene Buchung blockiert nicht (Freigabe-Regel in `btnSpeichern`, belegt).
- **R3:** Der Kachel-Dialog setzt die Ende-Vorgabe zurück, sonst stünde dort das Ende aus „Neu buchen“.
- **Neu in Fassung 2:**
  - Baut auf P1 auf: `btnHitArea.OnSelect` enthält die Rücksetzungen von „Für andere“. „Neu buchen“ setzt genau dieselben zurück (Umschalter „Für mich“, Name leer), maschinell gegen die Kachel geprüft.
  - Knopfstil 1:1 vom Hauptknopf `btnSpeichern` (Markenblau, Semibold, Radius 10). Größe 12 und Höhe 32, damit er in die Karte passt.
- **Umfang:** 32 Properties, 1 neues Steuerelement (`btnNeuBuchenHeute`). Keine neue Abfrage ohne Tippen. „Neu buchen“ liest beim Tippen einmal `Tische` (ab P4: `TischeLokal`, keine Abfrage).
- **Voraussetzung:** P2 (Nachtrag 5, wegen N4/S3b: gleiche Verfallsregel wie die Statusanzeige) und P1.
- **Gast-Buchung verfallen:** „Neu buchen“ bucht zunächst **für dich**. Für den Gast im Dialog „Für andere“ einschalten und den Namen eintragen (geschlussfolgert, so gewollt: der Dialog startet immer zurückgesetzt).

## Schritte (Reihenfolge R1 → R2 → R3)

### R1 Karte öffnet bei verfallener oder beendeter Buchung keinen Check-in-Dialog

**Regel:** gesperrt, wenn `Endzeit` erreicht ist **oder** die Buchung verfallen ist (nicht eingecheckt, Beginn und Buchungszeitpunkt älter als 30 Min). Zeichengleich mit `lblStatusHeute` nach S3b, rechnet mit dem 15-s-Takt.

**Test:** Einsetzplan Teil A, Test 8.

#### `btnEincheckenHeute.DisplayMode`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **neu setzen** (bisher nicht gesetzt, Standard `Standard`, Rückfall: `Standard`)

Vollständiger Block:

```
If(
  ThisItem.Endzeit <= Coalesce(varJetztTakt; Now()) || (!ThisItem.CheckedIn && ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));
  DisplayMode.Disabled;
  DisplayMode.Edit
)
```

#### `btnEincheckenHeute.DisabledFill`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **neu setzen** (bisher nicht gesetzt, Standard `Standard`, Rückfall: `Standard`)

Vollständiger Block:

```
Color.Transparent
```

#### `btnEincheckenHeute.DisabledBorderColor`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > btnEincheckenHeute` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-RGBA(166; 166; 166; 1)
+Color.Transparent
```

Vollständiger Block:

```
Color.Transparent
```

### R2 Knopf „Neu buchen“ (neu)

**Neu anlegen, Name exakt so:**
1. In der Strukturansicht `galTischbuchungenHeute` markieren.
2. Das Stift-Symbol oben links in der **ersten Karte** anklicken (Vorlage gewählt).
3. Einfügen → Schaltfläche (klassisch) → umbenennen in **`btnNeuBuchenHeute`**.
4. Prüfen: `btnNeuBuchenHeute` liegt **in** `galTischbuchungenHeute` und in der Strukturansicht **über** `btnEincheckenHeute` (Neu anordnen → Ganz nach vorne).

**Ablauf beim Tippen:** Tisch frisch prüfen (gibt es ihn noch, ist er gesperrt). Dann Buchungsdialog mit genau den Rücksetzungen der Kachel, Datum heute, Beginn ab der nächsten halben Stunde, Ende = altes Ende. Beginn und Ende kannst du im Dialog ändern.

`lblStatusHeute.Visible` = `!btnNeuBuchenHeute.Visible`. Wo der Knopf steht, ist „Verfallen“ weg. Ist keine Restzeit mehr übrig, steht wieder „Verfallen“.

**Test:** Einsetzplan Teil A, Tests 7 und 9.

#### `btnNeuBuchenHeute` (neu, Button (Einfügen → Schaltfläche, klassisch), in `galTischbuchungenHeute`)

Anlegen: in die **erste Zeile** von `galTischbuchungenHeute` einfügen (Galerie markieren, Stift-Symbol der Vorlage, dann Einfügen).

| Property | Wert |
|---|---|
| `Text` | `"Neu buchen"` |
| `X` | `lblStatusHeute.X` |
| `Y` | `lblStatusHeute.Y + 5` |
| `Width` | `120` |
| `Height` | `32` |
| `Size` | `12` |
| `DisplayMode` | `If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)` |
| `AccessibleLabel` | `"Tisch " & ThisItem.Tisch.Value & " neu buchen"` |
| `Fill` | `ColorValue("#171496")` |
| `Color` | `RGBA(255; 255; 255; 1)` |
| `BorderColor` | `ColorFade(Self.Fill; -15%)` |
| `BorderThickness` | `2` |
| `DisabledBorderColor` | `RGBA(166; 166; 166; 1)` |
| `Font` | `Font.'Open Sans'` |
| `FontWeight` | `FontWeight.Semibold` |
| `HoverBorderColor` | `ColorFade(Self.BorderColor; 20%)` |
| `HoverColor` | `RGBA(255; 255; 255; 1)` |
| `HoverFill` | `ColorFade(Self.Fill; -20%)` |
| `PressedBorderColor` | `Self.Fill` |
| `PressedColor` | `Color.White` |
| `PressedFill` | `ColorFade(Self.Fill; -20%)` |
| `RadiusTopLeft` | `10` |
| `RadiusTopRight` | `10` |
| `RadiusBottomLeft` | `10` |
| `RadiusBottomRight` | `10` |

`btnNeuBuchenHeute.Visible`:

```
varAnsichtsDatum = Today() && !ThisItem.CheckedIn && ThisItem.Startzeit <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) && ThisItem.Erstellt <= DateAdd(Coalesce(varJetztTakt; Now()); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes) &&
Hour(ThisItem.Endzeit) * 60 + Minute(ThisItem.Endzeit) > 30 * RoundUp((Hour(Coalesce(varJetztTakt; Now())) * 60 + Minute(Coalesce(varJetztTakt; Now()))) / 30; 0)
```

`btnNeuBuchenHeute.OnSelect`:

```
If(
  !varIsLoading;
  Set(varNeuBuchenTisch; LookUp(Tische; Titel = ThisItem.Tisch.Value));;
  If(
    IsBlank(varNeuBuchenTisch.ID);
    Notify("Diesen Tisch gibt es nicht mehr."; NotificationType.Warning);
    varNeuBuchenTisch.Gesperrt;
    Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
    Set(varSelectedTisch; varNeuBuchenTisch);;
    Set(varDialogJetzt; Now());;
    Reset(tglFuerAndere);;
    Reset(txtGastName);;
    Set(varFbTrotzdem; false);;
    Set(varEndeOverride; Text(ThisItem.Endzeit; "hh:mm"));;
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
  )
)
```

#### `lblStatusHeute.Visible`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblStatusHeute` · **neu setzen** (bisher nicht gesetzt, Standard `Standard`, Rückfall: `Standard`)

Vollständiger Block:

```
!btnNeuBuchenHeute.Visible
```

### R3 Kachel-Dialog: Ende-Vorgabe zurücksetzen

`btnHitArea.OnSelect` bekommt nur eine Zeile: `Set(varEndeOverride; "")` vor `Reset(ddEnde)`. Sonst nichts (maschinell geprüft).

**Test:** Einsetzplan Teil A, Test 10.

#### `btnHitArea.OnSelect`

Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen**

Änderung gegenüber P1 (Für andere buchen v2) (`-` alt, `+` neu):

```diff
@@ -14,2 +14,3 @@
       Set(varSelectedTisch; ThisItem);;
+      Set(varEndeOverride; "");;
       Set(varDialogJetzt; Now());;
```

Vollständiger Block:

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  If(
    varAnsichtsDatum = Today();
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes)));
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)))
  );;
  RemoveIf(colKachel; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varKachelID; First(SortByColumns(colKachel; "Startzeit"; SortOrder.Ascending)).ID);;
  If(
    IsBlank(varKachelID);
      Set(varSelectedTisch; ThisItem);;
      Set(varEndeOverride; "");;
      Set(varDialogJetzt; Now());;
      Reset(tglFuerAndere);;
      Reset(txtGastName);;
      Set(varFbTrotzdem; false);;
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

## UNSICHER
| Nr | Was | Test |
|---|---|---|
| R-U1 | `Set(varSelectedTisch; varNeuBuchenTisch)`: Datensatz aus `LookUp(Tische; …)`, die Kachel liefert einen aus `Gallery1` (`Filter(Tische; …)`). Gleiche Quelle, also gleicher Typ (geschlussfolgert). **Mit P4 ändert sich die Quelle der Galerie, deshalb ändert P4 auch diese Zeile (L5)** | App-Prüfung: kein Typfehler an `varSelectedTisch` |
| R-U2 | Liegt das alte Ende nicht im Halbstundenraster (nur bei Buchungen, die direkt in der Liste angelegt wurden), passt die Vorgabe nicht zur Ende-Liste | Ende im Dialog prüfen. `btnSpeichern` prüft „Ende nach Beginn“ |
| R-U3 | Knopf Größe 12 in Höhe 32: „Neu buchen“ ca. 90 px Text (geschätzt je Zeichenart, Semibold) plus Rand in Breite 120 | Sichtprüfung |

## Rückfall
- `btnNeuBuchenHeute` löschen, `lblStatusHeute.Visible` auf `true`.
- `btnEincheckenHeute.DisplayMode`, `.DisabledFill`, `.DisabledBorderColor` und `btnHitArea.OnSelect` aus Anhang A. Ohne den Knopf darf R3 bleiben.
- **Ist P4 schon eingefügt:** L5 ist dann mit dem Knopf weg, sonst nichts zu tun.

## Anhang A: Stand vor P3 (Export 10.11. 08:13, `btnHitArea.OnSelect` nach P1) – Rückfall

**`btnEincheckenHeute.DisabledBorderColor`**

```
RGBA(166; 166; 166; 1)
```

**`btnHitArea.OnSelect`**

```
If(
  ThisItem.Gesperrt;
  Notify("Dieser Tisch ist zurzeit gesperrt."; NotificationType.Warning);
  Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
  If(
    varAnsichtsDatum = Today();
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes)));
    ClearCollect(colKachel; Filter(Tischbuchungen; Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)))
  );;
  RemoveIf(colKachel; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
  Set(varKachelID; First(SortByColumns(colKachel; "Startzeit"; SortOrder.Ascending)).ID);;
  If(
    IsBlank(varKachelID);
      Set(varSelectedTisch; ThisItem);;
      Set(varDialogJetzt; Now());;
      Reset(tglFuerAndere);;
      Reset(txtGastName);;
      Set(varFbTrotzdem; false);;
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

## Anhang B: Maschinelle Prüfung

Paket allein:

```
32 Properties in 3 Schritten, 1 neues Steuerelement (btnNeuBuchenHeute). Grundlage: Export 10.11. 08:13 + Nachtrag 5 + Für andere buchen v2.
Je Property: Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden, keine neue Abfrage und kein Schreiben auf Tischbuchungen (nur „Neu buchen“ liest einmal Tische).
„Neu buchen“ öffnet den Buchungsdialog mit denselben Rücksetzungen wie die Kachel (btnHitArea), nur Tisch und Ende-Vorgabe anders.
Öffner des Buchungsdialogs: btnHitArea.OnSelect, btnNeuBuchenHeute.OnSelect; jeder setzt die Ende-Vorgabe vor Reset(ddEnde).
Verfallsregel in Karte und Knopf zeichengleich mit lblStatusHeute (S3b über Nachtrag 5 N4).
Prüfung: 0 Fehler
```

Alle Pakete zusammen (`werkzeuge/abstimmung.py`):

```
Abstimmung der Pakete, Grundlage Export 10.11. 08:13 („echt“, App „Tischbuchung“, Desktop).
Reihenfolge: P0 Design → P1 Für andere buchen v2 → P2 Nachtrag 5 → P3 Nachtrag 6 v2 → P4 Grundriss-Laden v2 (= v1 + L5).

P0: 7 Properties, davon 7 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente
P1: 179 Properties, davon 19 mit Vorher (alle passen genau), 160 neu/bisher Standard, 10 neue Steuerelemente
P2: 21 Properties, davon 21 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente
P3: 32 Properties, davon 2 mit Vorher (alle passen genau), 30 neu/bisher Standard, 1 neue Steuerelemente
P4: 7 Properties, davon 7 mit Vorher (alle passen genau), 0 neu/bisher Standard, 0 neue Steuerelemente

Zusammen: 243 verschiedene Properties, 246 Blöcke, 11 neue Steuerelemente: tglFuerAndere (P1), txtGastName (P1), tglFuerAnderePanel (P1), txtGastNamePanel (P1), btnFbHintergrund (P1), conFbHinweis (P1), lblFbTitel (P1), lblFbHinweis (P1), btnFbAbbrechen (P1), btnFbTrotzdem (P1), btnNeuBuchenHeute (P3)
Properties, die mehr als ein Paket ändert (jeweils auf dem Stand des vorigen aufgebaut, Vorher geprüft):
  btnHitArea.OnSelect: P1 → P3
  btnNeuBuchenHeute.OnSelect: P3 → P4
  App.Formulas: P4 → P4

Endzustand:
  Klammern, Rückübersetzung, Variablen gesetzt, Steuerelemente vorhanden: alle 243 geänderten Properties.
  Öffner Buchungsdialog (btnHitArea.OnSelect, btnNeuBuchenHeute.OnSelect): setzen Gast-Schalter, Gastname, „Trotzdem“, Ende-Vorgabe, Datum und Ende zurück.
  Öffner Panel (btnTischHinzufügen.OnSelect): setzen Gast-Schalter, Gastname und „Trotzdem“ zurück.
  Schreibstellen (8): alle mit Zweifach-Sperre und Ladezeile. Ladezeile 18× in einer Fassung (Aktualisieren-Knöpfe zusätzlich mit Erfolgsmeldung).
  varSelectedTisch: Setzer ['Blank()', 'ThisItem', 'varNeuBuchenTisch']; Gallery1 und „Neu buchen“ lesen beide aus TischeLokal.
  GastName in jeder Füllung von colNeuIch, colVerlIch (dort mit GastName gelesen).
  Gewählte Buchung (varSelectedBuchung, …Tab, varCheckinBuchung): jeder Setzer liefert einen Datensatz aus Tischbuchungen (mit GastName).
  Positionen: benannte Formeln, keine Sammlung mehr. Freigabe-Grenze überall 30 Min (Coalesce).

Check-in-Fenster (Bestand, nicht geändert):
  App.OnStart: 30, 60 Min
  Timer1.OnTimerEnd: 30 Min
  btnEinchecken.OnSelect: 60 Min

Prüfung: 0 Fehler
```
