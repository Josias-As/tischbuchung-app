# Für andere buchen + weicher Hinweis (Tischbuchung Desktop, 26.10.2026)

Für Josias. Grundlage: **Export 25.10. 20:09** (`Tischbuchungsapp25.10.26_20261025200901.zip`). Erzeugt und maschinell geprüft mit `werkzeuge/fuer_andere.py` (0 Fehler, Mutationstest 13 von 13 erkannt). Unabhängig geprüft, Befunde in Abschnitt 6. In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

**Voraussetzung:** Jeder Block ersetzt die **ganze** Property. Hast du nach dem 25.10. 20:09 an einer der 17 geänderten Properties etwas gespeichert, erst neu exportieren, ich erzeuge die Blöcke dann neu.

## Kurzfassung
- **Deine Entscheidungen:** 1 A, 2 a, 3 ja, 4 ja, 6 ok.
  - Die vorhandene Regel „kein zweiter Tisch zur selben Zeit“ sperrt nicht mehr. Stattdessen fragt ein Hinweis „Trotzdem buchen / Abbrechen“. Beim Verlängern genauso („Trotzdem verlängern“).
  - Gäste checkt der Buchende ein.
  - Der Gastname steht im Popup des Grundrisses. Die Kachel zeigt weiter die Kürzel des Buchenden.
  - Serien gelten für Gäste wie für dich, aber ohne Prüfung auf eigene Buchungen.
- **Für andere buchen:**
  - Im Buchungsdialog und im Panel gibt es den Umschalter **„Für mich / Für andere“**. Steht er auf „Für andere“, erscheint ein Namensfeld. Es ist Pflicht und nimmt höchstens 100 Zeichen.
  - Gespeichert wird in der neuen Spalte `GastName`. `Person` bleibt der Buchende, Stornieren und Einchecken laufen weiter über ihn.
- **Gast-Buchungen zählen nicht als eigene:** Sie lösen keinen Hinweis aus, und sie blockieren dich nicht. Das gilt beim Buchen und beim Verlängern.
- **Anzeige:**
  - Grundriss-Popup: Gastname, darunter „gebucht von <Buchender>“.
  - „My personal desk“, Tab „Buchungen“ und beide Verwalten-Dialoge: „für <Gast>“.
  - **Altbestand ohne Gastnamen sieht genau aus wie heute.** Jede geänderte Anzeige enthält die alte Formel zeichengleich im Zweig „GastName leer“ (maschinell geprüft).
- **Umfang:**
  - 17 bestehende Properties werden ersetzt. 6 bisher nicht gesetzte Maße an bestehenden Labels kommen dazu (Rückfall: Standardwert, steht beim Block).
  - 9 neue Steuerelemente, alle direkt im Screen oder im jeweiligen Container. Keine Auto-Layout-Container.
  - Neue Variablen tragen alle den Präfix `varFb…` (7 Stück).
  - Kein neuer Server-Filter: `GastName` wird nur lokal geprüft, deshalb keine neue Delegationswarnung.
- **Nicht angefasst:**
  - Ladezeile (17×), Tischpositionen, Grundriss-Layout.
  - Check-in, Stornieren, Mehrfach-Storno, Freigabe, App.OnStart.
  - Der nächtliche Lösch-Flow filtert nur nach `Endzeit` (laut Betriebshandbuch). Er ist nicht im Export.
- **Handy-App:** unverändert. Bekannte Folge, von dir akzeptiert: Gast-Buchungen blockieren dort den Buchenden zur selben Zeit.
- **Hinweistext:** Er nennt „Fragen: Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT).“ Frage 5 ist offen. Ändern geht an einer Stelle: `lblFbHinweis.Text`.
- **Unabhängig geprüft (Abschnitt 6):**
  - 3 Befunde sind behoben, die das Einfügen blockiert hätten:
    - „Trotzdem verlängern“ lief ins Leere.
    - Zweizeilige Texte wurden abgeschnitten.
    - Texte überlappten oder waren zu lang.
  - Dazu kleinere Punkte.
  - Für die Breiten rechnet der Generator jetzt je Zeichenart und mit Pixeln, nicht mehr mit einer Pauschale.
- **Nachtrag 6 (noch nicht eingefügt)** ändert ebenfalls `btnHitArea.OnSelect`. Fügst du ihn später ein, erzeuge ich ihn auf diesem Stand neu.

## 1. Einfügen (Reihenfolge)
1. **Kopie testen:** Alles zuerst in deiner Kopie der App. Sicherung `.msapp` vom Original.
2. **S1 Spalte anlegen:** In der Liste `Tischbuchungen` neue Spalte **`GastName`**, Typ **Eine Textzeile**, nicht erforderlich. Dann in Studio: Daten → `Tischbuchungen` → … → **Aktualisieren** (nicht neu verbinden).
3. **S2–S4 Steuerelemente anlegen** (Tabelle unten), **exakt** so benennen und die Properties setzen.
4. **S5–S8 Formeln ersetzen**, jeweils die **ganze** Property.
5. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler. Rote Fehler zwischen S2 und S5 sind normal, solange Steuerelemente noch fehlen, die eine Formel nennt.
6. Testbogen (Abschnitt 3) in der Kopie, dann ins Original übernehmen, speichern, **Export an mich** zum Abgleich, veröffentlichen.

**Neue Steuerelemente:**

| Name | Typ | liegt in | Schritt |
|---|---|---|---|
| `tglFuerAndere` | Umschalter (klassisch, „Umschalten“) | `conBuchungDialog` | S3 |
| `txtGastName` | Texteingabe (klassisch) | `conBuchungDialog` | S3 |
| `tglFuerAnderePanel` | Umschalter (klassisch, „Umschalten“) | `conTischBuchungenPanel` | S4 |
| `txtGastNamePanel` | Texteingabe (klassisch) | `conTischBuchungenPanel` | S4 |
| `btnFbHintergrund` | Schaltfläche (klassisch) | `Screen1` | S2 |
| `conFbHinweis` | Container (Layout → Container, nicht horizontal/vertikal) | `Screen1` | S2 |
| `lblFbHinweis` | Textbeschriftung | `conFbHinweis` | S2 |
| `btnFbAbbrechen` | Schaltfläche (klassisch) | `conFbHinweis` | S2 |
| `btnFbTrotzdem` | Schaltfläche (klassisch) | `conFbHinweis` | S2 |

**Ebenen (wichtig):**
- `btnFbHintergrund` und `conFbHinweis` liegen in `Screen1` über allen Dialogen.
- Nach dem Anlegen `btnFbHintergrund` markieren → **Ganz nach vorne bringen**. Danach `conFbHinweis` → **Ganz nach vorne bringen**. Danach **`conLadeOverlay` → Ganz nach vorne bringen**, damit die Ladeanzeige weiter alles überdeckt.
- In der Strukturansicht steht dann von oben nach unten: `conLadeOverlay`, `conFbHinweis`, `btnFbHintergrund`, … Alle anderen bleiben, wo sie sind.
- **In Studio** verdecken die neuen Flächen den Bildschirm nicht, weil `varFbZeige` leer ist. Zum Gestalten kurz `Visible` auf `true` setzen und danach die Formel aus dem Block zurück einsetzen.

## 2. Schritte

### S2 Hinweisdialog anlegen (direkt in Screen1)

**Was:** Ein Hinweis (500 × 280) mit Vollbild-Hintergrund. Der Hintergrund fängt alle Klicks ab, solange der Hinweis offen ist. Daneben ist nichts bedienbar, also kann sich auch keine Variable ändern.
- **„Abbrechen“** schließt den Hinweis, nichts wird gespeichert. Der Buchungsdialog oder das Panel bleibt offen.
- **„Trotzdem buchen“ / „Trotzdem verlängern“** führt den Knopf, der gefragt hat, noch einmal aus, diesmal mit Bestätigung (`varFbTrotzdem`). Die Speicherlogik steht also nur einmal da.
- Der Knopf blendet den Hinweis nicht selbst aus. Das macht der Speichern- bzw. Verlängern-Knopf als erste Anweisung. So trifft ein Doppelklick nie den Dialog darunter, und während des Speicherns deckt die Ladeanzeige alles ab.

**Rückfall:** `btnFbHintergrund` und `conFbHinweis` (samt Inhalt) löschen. Vorher S5 und S6 zurücknehmen, weil sie den Hinweis öffnen.

#### `btnFbHintergrund` (neu, Schaltfläche (klassisch), in `Screen1`)

| Property | Wert |
|---|---|
| `X` | `0` |
| `Y` | `0` |
| `Width` | `Parent.Width` |
| `Height` | `Parent.Height` |
| `Text` | `""` |
| `Fill` | `RGBA(0; 0; 0; 0,35)` |
| `HoverFill` | `RGBA(0; 0; 0; 0,35)` |
| `PressedFill` | `RGBA(0; 0; 0; 0,35)` |
| `BorderThickness` | `0` |
| `FocusedBorderThickness` | `0` |
| `RadiusTopLeft` | `0` |
| `RadiusTopRight` | `0` |
| `RadiusBottomLeft` | `0` |
| `RadiusBottomRight` | `0` |
| `TabIndex` | `-1` |
| `Visible` | `varFbZeige` |
| `OnSelect` | `false` |
| `AccessibleLabel` | `"Hinweis offen"` |

#### `conFbHinweis` (neu, Container (Layout → Container, nicht horizontal/vertikal), in `Screen1`)

| Property | Wert |
|---|---|
| `Width` | `500` |
| `Height` | `280` |
| `X` | `(Parent.Width - Self.Width) / 2` |
| `Y` | `(Parent.Height - Self.Height) / 2` |
| `Fill` | `Color.White` |
| `RadiusTopLeft` | `16` |
| `RadiusTopRight` | `16` |
| `RadiusBottomLeft` | `16` |
| `RadiusBottomRight` | `16` |
| `Visible` | `varFbZeige` |

#### `lblFbHinweis` (neu, Textbeschriftung, in `conFbHinweis`)

| Property | Wert |
|---|---|
| `X` | `20` |
| `Y` | `20` |
| `Width` | `Parent.Width - 40` |
| `Height` | `Parent.Height - 100` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Color` | `RGBA(50; 49; 48; 1)` |
| `VerticalAlign` | `VerticalAlign.Top` |

`lblFbHinweis.Text`:

```
varFbText & Char(10) & Char(10) & "Fragen: Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT)."
```

#### `btnFbAbbrechen` (neu, Schaltfläche (klassisch), in `conFbHinweis`)

| Property | Wert |
|---|---|
| `X` | `20` |
| `Y` | `Parent.Height - 60` |
| `Width` | `(Parent.Width - 60) / 2` |
| `Height` | `40` |
| `Text` | `"Abbrechen"` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Fill` | `Color.Black` |
| `Color` | `RGBA(255; 255; 255; 1)` |
| `HoverFill` | `ColorFade(Self.Fill; 30%)` |
| `PressedFill` | `ColorFade(Color.Black; 30%)` |
| `PressedColor` | `Color.White` |
| `AccessibleLabel` | `"Abbrechen, nichts buchen"` |

`btnFbAbbrechen.OnSelect`:

```
Set(varFbZeige; false);;
Set(varFbTrotzdem; false)
```

#### `btnFbTrotzdem` (neu, Schaltfläche (klassisch), in `conFbHinweis`)

| Property | Wert |
|---|---|
| `X` | `Parent.Width - Self.Width - 20` |
| `Y` | `btnFbAbbrechen.Y` |
| `Width` | `btnFbAbbrechen.Width` |
| `Height` | `40` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Fill` | `ColorValue("#171496")` |
| `Color` | `RGBA(255; 255; 255; 1)` |
| `HoverFill` | `ColorFade(Self.Fill; -20%)` |
| `PressedFill` | `ColorFade(Self.Fill; -20%)` |
| `PressedColor` | `Color.White` |
| `DisplayMode` | `If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)` |
| `AccessibleLabel` | `Self.Text` |

`btnFbTrotzdem.Text`:

```
If(varFbQuelle = "verl" || varFbQuelle = "verltab"; "Trotzdem verlängern"; "Trotzdem buchen")
```

`btnFbTrotzdem.OnSelect`:

```
If(
  !varIsLoading && varFbZeige;
  Set(varFbTrotzdem; true);;
  Set(varSperreBis; Blank());;
  Switch(
    varFbQuelle;
    "panel"; Select(btnSpeichernTischePanel);
    "verl"; Select(btnVerlängern);
    "verltab"; Select(btnVerlängern_1);
    Select(btnSpeichern)
  )
)
```

### S3 Buchungsdialog: Schalter und Namensfeld

**Was:** Im Buchungsdialog (aus dem Grundriss), in der mittleren Spalte unter dem Tischnamen: Umschalter `tglFuerAndere` und darunter das Namensfeld `txtGastName`.
- Der Platz ist frei: Bild bis X 245, Eingaben ab X 448, Wochentage erst ab Y 290 (belegt, Export).
- Das Namensfeld erscheint nur, wenn der Umschalter auf „Für andere“ steht.

**Rückfall:** beide löschen (erst S5/S7 zurücknehmen).

#### `tglFuerAndere` (neu, Umschalter (klassisch, „Umschalten“), in `conBuchungDialog`)

| Property | Wert |
|---|---|
| `X` | `270` |
| `Y` | `122` |
| `Width` | `165` |
| `Height` | `40` |
| `Default` | `false` |
| `FalseText` | `"Für mich"` |
| `TrueText` | `"Für andere"` |
| `TrueFill` | `ColorValue("#00A96B")` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `AccessibleLabel` | `"Für jemand anderen buchen"` |

#### `txtGastName` (neu, Texteingabe (klassisch), in `conBuchungDialog`)

| Property | Wert |
|---|---|
| `X` | `270` |
| `Y` | `186` |
| `Width` | `165` |
| `Height` | `40` |
| `Default` | `""` |
| `HintText` | `"Name (Pflicht)"` |
| `MaxLength` | `100` |
| `Visible` | `tglFuerAndere.Value` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `AccessibleLabel` | `"Name der Person, für die gebucht wird"` |

### S4 Panel: Schalter und Namensfeld, Speichern rückt nach unten

**Was:** Im Panel „Tisch buchen“ eine Zeile mit Umschalter `tglFuerAnderePanel` und Namensfeld `txtGastNamePanel`. Sie steht unter den Wochentagen. **`btnSpeichernTischePanel` rückt 60 nach unten** (Y 531 → 591, Unterkante 631 von 678 bei 768 Höhe, gerechnet).

**Rückfall:** `btnSpeichernTischePanel.Y` aus Anhang A, beide Steuerelemente löschen.

#### `tglFuerAnderePanel` (neu, Umschalter (klassisch, „Umschalten“), in `conTischBuchungenPanel`)

| Property | Wert |
|---|---|
| `X` | `ddTischePanel.X` |
| `Y` | `tglTagFr_1.Y + tglTagFr_1.Height + 20` |
| `Width` | `165` |
| `Height` | `40` |
| `Default` | `false` |
| `FalseText` | `"Für mich"` |
| `TrueText` | `"Für andere"` |
| `TrueFill` | `ColorValue("#00A96B")` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `AccessibleLabel` | `"Für jemand anderen buchen"` |

#### `txtGastNamePanel` (neu, Texteingabe (klassisch), in `conTischBuchungenPanel`)

| Property | Wert |
|---|---|
| `X` | `ddTischePanel.X + 175` |
| `Y` | `tglFuerAnderePanel.Y` |
| `Width` | `ddTischePanel.Width - 175` |
| `Height` | `40` |
| `Default` | `""` |
| `HintText` | `"Name (Pflicht)"` |
| `MaxLength` | `100` |
| `Visible` | `tglFuerAnderePanel.Value` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `AccessibleLabel` | `"Name der Person, für die gebucht wird"` |

#### `btnSpeichernTischePanel.Y`

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-tglTagFr_1.Y + tglTagFr_1.Height + 20
+tglFuerAnderePanel.Y + tglFuerAnderePanel.Height + 20
```

Vollständiger Block:

```
tglFuerAnderePanel.Y + tglFuerAnderePanel.Height + 20
```

### S5 Speichern: Gast, weicher Hinweis, GastName

**Was, in beiden Speichern-Knöpfen gleich** (maschinell verglichen):
1. Als Erstes wird eine Bestätigung aus dem Hinweis verbraucht (`varFbBestaetigt`), `varFbTrotzdem` zurückgesetzt und der Hinweis ausgeblendet. Umschalter und Name werden gelesen.
2. Neue Prüfung: „Für andere“ ohne Namen → Meldung, nichts gespeichert.
3. Eigene Buchungen, die zur selben Zeit liegen (`colNeuIch`): Gast-Buchungen (`GastName` nicht leer) zählen nicht. Bei einer Buchung **für** andere wird gar nicht geprüft.
   - Der Server-Filter bleibt gleich, die Gast-Buchungen fallen lokal per `RemoveIf` heraus. So entsteht keine neue Delegationswarnung.
   - `colNeuIch` wird jetzt mit genannten Spalten geladen (`ForAll(… As B; {ID; Startzeit; Endzeit; CheckedIn; Erstellt; GastName})`, wie in der Ladezeile). So kommen `GastName` und `Erstellt` sicher an.
4. **Statt Sperre:** Überschneidet mindestens ein Termin eine eigene Buchung, öffnet sich der Hinweis, und **nichts** wird gespeichert. Mit „Trotzdem buchen“ werden alle freien Termine gespeichert, auch die mit Überschneidung. Termine, an denen der Tisch selbst belegt ist, bleiben wie heute ausgeschlossen.
5. Der Sammel-Patch schreibt `GastName` mit. Bei eigenen Buchungen bleibt die Spalte leer.
6. Die Erfolgsmeldung nennt den Gast: „Gebucht: UG Desk 5 für Max Muster, …“.
7. Sperre, `IfError`, Nachlese, Ladezeile und Meldungen sind sonst unverändert (maschinell geprüft: keine andere Zeile weg).

**Rückfall:** beide Properties aus Anhang A.

#### `btnSpeichern.OnSelect`

Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -3,2 +3,7 @@
   Set(varIsLoading; true);;
+  Set(varFbBestaetigt; varFbTrotzdem);;
+  Set(varFbTrotzdem; false);;
+  Set(varFbZeige; false);;
+  Set(varFbFuerAndere; tglFuerAndere.Value);;
+  Set(varFbGast; If(tglFuerAndere.Value; Trim(txtGastName.Text); Blank()));;
   Set(varNeuTischTitel; varSelectedTisch.Titel);;
@@ -26,2 +31,4 @@
     Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
+    varFbFuerAndere && IsBlank(varFbGast);
+    Notify("Bitte den Namen der Person eingeben, für die du buchst."; NotificationType.Warning);
     varNeuEndeZeit <= varNeuStartZeit;
@@ -43,4 +50,4 @@
     RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
-    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
-    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colNeuIch; ForAll(Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
+    RemoveIf(colNeuIch; varFbFuerAndere || !IsBlank(GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     ClearCollect(
@@ -55,3 +62,3 @@
             "tisch";
-            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
+            !varFbBestaetigt && !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
             "ich";
@@ -65,2 +72,6 @@
     If(
+      varNeuIchBelegt > 0;
+      Set(varFbQuelle; "dialog");;
+      Set(varFbText; If(varNeuGesamt = 1; "Du hast zu dieser Zeit schon einen Tisch gebucht."; "An " & varNeuIchBelegt & " von " & varNeuGesamt & " Terminen hast du zu dieser Zeit schon einen Tisch gebucht.") & " Trotzdem einen weiteren Tisch buchen?");;
+      Set(varFbZeige; true);
       varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
@@ -93,3 +104,4 @@
               };
-              SerienID: varSerienID
+              SerienID: varSerienID;
+              GastName: varFbGast
             }
@@ -111,3 +123,3 @@
         varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
-        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
+        Notify("Gebucht: " & varNeuTischTitel & If(IsBlank(varFbGast); ""; " für " & varFbGast) & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
         Notify(
```

Vollständiger Block:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFbBestaetigt; varFbTrotzdem);;
  Set(varFbTrotzdem; false);;
  Set(varFbZeige; false);;
  Set(varFbFuerAndere; tglFuerAndere.Value);;
  Set(varFbGast; If(tglFuerAndere.Value; Trim(txtGastName.Text); Blank()));;
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
    varFbFuerAndere && IsBlank(varFbGast);
    Notify("Bitte den Namen der Person eingeben, für die du buchst."; NotificationType.Warning);
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
    ClearCollect(colNeuIch; ForAll(Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
    RemoveIf(colNeuIch; varFbFuerAndere || !IsBlank(GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
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
            !varFbBestaetigt && !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuIchBelegt > 0;
      Set(varFbQuelle; "dialog");;
      Set(varFbText; If(varNeuGesamt = 1; "Du hast zu dieser Zeit schon einen Tisch gebucht."; "An " & varNeuIchBelegt & " von " & varNeuGesamt & " Terminen hast du zu dieser Zeit schon einen Tisch gebucht.") & " Trotzdem einen weiteren Tisch buchen?");;
      Set(varFbZeige; true);
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
              SerienID: varSerienID;
              GastName: varFbGast
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
        Notify("Gebucht: " & varNeuTischTitel & If(IsBlank(varFbGast); ""; " für " & varFbGast) & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnSpeichernTischePanel.OnSelect`

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -3,2 +3,7 @@
   Set(varIsLoading; true);;
+  Set(varFbBestaetigt; varFbTrotzdem);;
+  Set(varFbTrotzdem; false);;
+  Set(varFbZeige; false);;
+  Set(varFbFuerAndere; tglFuerAnderePanel.Value);;
+  Set(varFbGast; If(tglFuerAnderePanel.Value; Trim(txtGastNamePanel.Text); Blank()));;
   Set(varNeuTischTitel; ddTischePanel.Selected.Titel);;
@@ -26,2 +31,4 @@
     Notify("Bitte einen Tisch auswählen."; NotificationType.Warning);
+    varFbFuerAndere && IsBlank(varFbGast);
+    Notify("Bitte den Namen der Person eingeben, für die du buchst."; NotificationType.Warning);
     varNeuEndeZeit <= varNeuStartZeit;
@@ -43,4 +50,4 @@
     RemoveIf(colNeuBelegt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
-    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
-    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
+    ClearCollect(colNeuIch; ForAll(Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
+    RemoveIf(colNeuIch; varFbFuerAndere || !IsBlank(GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     ClearCollect(
@@ -55,3 +62,3 @@
             "tisch";
-            !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
+            !varFbBestaetigt && !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
             "ich";
@@ -65,2 +72,6 @@
     If(
+      varNeuIchBelegt > 0;
+      Set(varFbQuelle; "panel");;
+      Set(varFbText; If(varNeuGesamt = 1; "Du hast zu dieser Zeit schon einen Tisch gebucht."; "An " & varNeuIchBelegt & " von " & varNeuGesamt & " Terminen hast du zu dieser Zeit schon einen Tisch gebucht.") & " Trotzdem einen weiteren Tisch buchen?");;
+      Set(varFbZeige; true);
       varNeuTischBelegt + varNeuIchBelegt = varNeuGesamt;
@@ -93,3 +104,4 @@
               };
-              SerienID: varSerienID
+              SerienID: varSerienID;
+              GastName: varFbGast
             }
@@ -111,3 +123,3 @@
         varNeuAnzahl = varNeuGesamt && varNeuBisRoh <= varNeuBis;
-        Notify("Gebucht: " & varNeuTischTitel & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
+        Notify("Gebucht: " & varNeuTischTitel & If(IsBlank(varFbGast); ""; " für " & varFbGast) & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
         Notify(
```

Vollständiger Block:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFbBestaetigt; varFbTrotzdem);;
  Set(varFbTrotzdem; false);;
  Set(varFbZeige; false);;
  Set(varFbFuerAndere; tglFuerAnderePanel.Value);;
  Set(varFbGast; If(tglFuerAnderePanel.Value; Trim(txtGastNamePanel.Text); Blank()));;
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
    varFbFuerAndere && IsBlank(varFbGast);
    Notify("Bitte den Namen der Person eingeben, für die du buchst."; NotificationType.Warning);
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
    ClearCollect(colNeuIch; ForAll(Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
    RemoveIf(colNeuIch; varFbFuerAndere || !IsBlank(GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
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
            !varFbBestaetigt && !IsBlank(LookUp(colNeuIch; Startzeit < T.Ende && Endzeit > T.Start).ID);
            "ich";
            "frei"
          )
        }
      )
    );;
    Set(varNeuTischBelegt; CountRows(Filter(colNeuErgebnis; Grund = "tisch")));;
    Set(varNeuIchBelegt; CountRows(Filter(colNeuErgebnis; Grund = "ich")));;
    If(
      varNeuIchBelegt > 0;
      Set(varFbQuelle; "panel");;
      Set(varFbText; If(varNeuGesamt = 1; "Du hast zu dieser Zeit schon einen Tisch gebucht."; "An " & varNeuIchBelegt & " von " & varNeuGesamt & " Terminen hast du zu dieser Zeit schon einen Tisch gebucht.") & " Trotzdem einen weiteren Tisch buchen?");;
      Set(varFbZeige; true);
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
              SerienID: varSerienID;
              GastName: varFbGast
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
        Notify("Gebucht: " & varNeuTischTitel & If(IsBlank(varFbGast); ""; " für " & varFbGast) & ", " & If(varNeuGesamt = 1; Text(varNeuSpanStart; "dd.mm."); varNeuAnzahl & " Termine ab " & Text(varNeuSpanStart; "dd.mm.")) & ", " & Text(varNeuSpanStart; "hh:mm") & " bis " & Text(varNeuSpanEnde; "hh:mm") & " Uhr. Bitte bis " & varFreigabeMinuten & " Minuten nach Beginn einchecken, sonst wird der Tisch freigegeben."; NotificationType.Success);
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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### S6 Verlängern: Gast-Buchungen zählen nicht, weicher Hinweis

**Was, in beiden Verlängern-Knöpfen gleich:**
1. Die Bestätigung wird am Anfang verbraucht.
2. Eigene andere Buchungen zur selben Zeit: Gast-Buchungen zählen nicht. Eine Gast-Buchung wird ohne diese Prüfung verlängert. `colVerlIch` wird wie oben mit genannten Spalten geladen.
3. Statt „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ (Sperre) kommt der Hinweis mit „Trotzdem verlängern“. Er kommt erst **nach** der Prüfung „Tisch inzwischen belegt“, damit niemand etwas bestätigt, das danach doch scheitert.
4. Ist der Hinweis offen, bleibt die gewählte Dauer stehen (`If(!varFbZeige; Set(varAusgewaehltePlusDauer; Blank()))`). Sonst wäre der Knopf beim „Trotzdem“ gesperrt und meldete „Bitte eine Dauer auswählen“ (Befund B1).
- Verkürzen, 22:00, „Tisch inzwischen belegt“ und verfallene Buchung bleiben wie heute.

**Rückfall:** beide Properties aus Anhang A.

#### `btnVerlängern.OnSelect`

Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -3,2 +3,5 @@
   Set(varIsLoading; true);;
+  Set(varFbBestaetigt; varFbTrotzdem);;
+  Set(varFbTrotzdem; false);;
+  Set(varFbZeige; false);;
   Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
@@ -17,4 +20,4 @@
     RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
-    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
-    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+    ClearCollect(colVerlIch; ForAll(Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
@@ -26,4 +29,2 @@
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
-      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
       varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
@@ -31,2 +32,6 @@
       Set(varVerlGrenze; varVerlEndeAlt);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
+      Set(varFbQuelle; "verl");;
+      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
+      Set(varFbZeige; true);
       IfError(
@@ -47,3 +52,3 @@
   With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
-  Set(varAusgewaehltePlusDauer; Blank());;
+  If(!varFbZeige; Set(varAusgewaehltePlusDauer; Blank()));;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFbBestaetigt; varFbTrotzdem);;
  Set(varFbTrotzdem; false);;
  Set(varFbZeige; false);;
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
    ClearCollect(colVerlIch; ForAll(Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenze; varVerlEndeAlt);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
      Set(varFbQuelle; "verl");;
      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
      Set(varFbZeige; true);
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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  If(!varFbZeige; Set(varAusgewaehltePlusDauer; Blank()));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

#### `btnVerlängern_1.OnSelect`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > btnVerlängern_1` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -3,2 +3,5 @@
   Set(varIsLoading; true);;
+  Set(varFbBestaetigt; varFbTrotzdem);;
+  Set(varFbTrotzdem; false);;
+  Set(varFbZeige; false);;
   Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
@@ -17,4 +20,4 @@
     RemoveIf(colVerlKonflikt; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
-    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
-    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+    ClearCollect(colVerlIch; ForAll(Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
@@ -26,4 +29,2 @@
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
-      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
       varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
@@ -31,2 +32,6 @@
       Set(varVerlGrenzeTab; varVerlEndeAlt);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
+      Set(varFbQuelle; "verltab");;
+      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
+      Set(varFbZeige; true);
       IfError(
@@ -47,3 +52,3 @@
   With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
-  Set(varAusgewaehltePlusDauer; Blank());;
+  If(!varFbZeige; Set(varAusgewaehltePlusDauer; Blank()));;
   Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
```

Vollständiger Block:

```
If(
  !varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis);
  Set(varIsLoading; true);;
  Set(varFbBestaetigt; varFbTrotzdem);;
  Set(varFbTrotzdem; false);;
  Set(varFbZeige; false);;
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
    ClearCollect(colVerlIch; ForAll(Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
      Notify("Der Tisch ist in dieser Zeit inzwischen belegt. Bitte eine kürzere Dauer wählen."; NotificationType.Warning);;
      Set(varVerlGrenzeTab; varVerlEndeAlt);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
      Set(varFbQuelle; "verltab");;
      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
      Set(varFbZeige; true);
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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  If(!varFbZeige; Set(varAusgewaehltePlusDauer; Blank()));;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

### S7 Öffner setzen Schalter und Name zurück

**Was:** Beim Öffnen des Buchungsdialogs (Kachel) und des Panels („Tisch Buchen“) werden Umschalter und Name zurückgesetzt. Eine liegen gebliebene Bestätigung wird gelöscht.
- Das sind die beiden einzigen Stellen, die Dialog bzw. Panel öffnen (belegt).
- Etage, Datum, Tab und Mehrfachauswahl schließen den Dialog wie bisher. Beim nächsten Öffnen ist alles zurückgesetzt.

**Rückfall:** beide Properties aus Anhang A.

#### `btnHitArea.OnSelect`

Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -15,2 +15,5 @@
       Set(varDialogJetzt; Now());;
+      Reset(tglFuerAndere);;
+      Reset(txtGastName);;
+      Set(varFbTrotzdem; false);;
       Reset(dpDatum);;
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

#### `btnTischHinzufügen.OnSelect`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -25,2 +25,5 @@
 Reset(ddEndTischePanel);;
-Reset(dpWiederholenBis_1)
+Reset(dpWiederholenBis_1);;
+Reset(tglFuerAnderePanel);;
+Reset(txtGastNamePanel);;
+Set(varFbTrotzdem; false)
```

Vollständiger Block:

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
Reset(dpWiederholenBis_1);;
Reset(tglFuerAnderePanel);;
Reset(txtGastNamePanel);;
Set(varFbTrotzdem; false)
```

### S8 Anzeige: Gastname und „gebucht von“

**Was:** Gastname in der Anzeige. Jede Formel hat die Form `If(IsBlank(….GastName); <alte Formel>; <neu>)`. Altbestand sieht also exakt aus wie heute.
Was sich nur bei Gast-Buchungen ändert:
- **Popup:** `lblPerson` ist breiter (bis vor das Bild), Größe 11, Höhe 46, zweizeilig. Die Zeitzeile `lblZeit2` rückt nach unten (Y 118).
- **„My personal desk“ und Tab „Buchungen“:** Die Zeitzeile bekommt eine zweite Zeile „für <Name>“, die Zeile wird doppelt so hoch. Der Name steht unter der Zeit, nicht daneben. Daneben läge sonst der Status bzw. das Auswahlkästchen.
- **Verwalten (Dashboard):** Zeit plus zweite Zeile „für <Name>“ in Größe 10, breiter bis vor „+1Std“.
- **Verwalten (Tab):** Titel „Tisch X · für <Name>“ in Größe 15 statt „Verwalten: Tisch X“ in 18, breiter.
- **Lange Namen** (ab etwa 15 Zeichen) können in Popup und Verwalten (Dashboard) abgeschnitten sein, die Liste zeigt sie ganz.

**Rückfall:** alle Properties aus Anhang A.

#### `lblPerson.Width`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (im Export nicht gesetzt, Standard `150`, Rückfall: `150`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 150; Image7.X - Self.X - 6)
```

#### `lblPerson.Size`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (im Export nicht gesetzt, Standard `13`, Rückfall: `13`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 13; 11)
```

#### `lblPerson.Height`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (im Export nicht gesetzt, Standard `40`, Rückfall: `40`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 40; 46)
```

#### `lblZeit3.Size`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (im Export nicht gesetzt, Standard `13`, Rückfall: `13`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 13; 10)
```

#### `lblZeit3.Width`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (im Export nicht gesetzt, Standard `150`, Rückfall: `150`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 150; btnPlus1Std.X - Self.X - 1)
```

#### `lblZeit3.Height`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (im Export nicht gesetzt, Standard `40`, Rückfall: `40`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 40; 50)
```

#### `lblPerson.Text`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1,5 @@
-varSelectedBuchung.Person.DisplayName
+If(
+  IsBlank(varSelectedBuchung.GastName);
+  varSelectedBuchung.Person.DisplayName;
+  varSelectedBuchung.GastName & Char(10) & "gebucht von " & varSelectedBuchung.Person.DisplayName
+)
```

Vollständiger Block:

```
If(
  IsBlank(varSelectedBuchung.GastName);
  varSelectedBuchung.Person.DisplayName;
  varSelectedBuchung.GastName & Char(10) & "gebucht von " & varSelectedBuchung.Person.DisplayName
)
```

#### `lblZeit2.Y`

Ort: `Screen1 > conDetailsPopup > lblZeit2` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-100
+If(IsBlank(varSelectedBuchung.GastName); 100; 118)
```

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 100; 118)
```

#### `lblZeitHeute.Text`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblZeitHeute` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1,5 @@
-Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm")
+If(
+  IsBlank(ThisItem.GastName);
+  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
+  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & Char(10) & "für " & ThisItem.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(ThisItem.GastName);
  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & Char(10) & "für " & ThisItem.GastName
)
```

#### `lblZeitHeute.Height`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblZeitHeute` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Self.Size * 1,8
+If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

Vollständiger Block:

```
If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

#### `lblRaumZeit.Text`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > lblRaumZeit` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1,5 @@
-Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm")
+If(
+  IsBlank(ThisItem.GastName);
+  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
+  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & Char(10) & "für " & ThisItem.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(ThisItem.GastName);
  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & Char(10) & "für " & ThisItem.GastName
)
```

#### `lblRaumZeit.Height`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > lblRaumZeit` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Self.Size * 1,8
+If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

Vollständiger Block:

```
If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

#### `lblZeit3.Text`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1,5 @@
-If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm"))
+If(
+  IsBlank(varSelectedBuchung.GastName);
+  If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm"));
+  If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm")) & Char(10) & "für " & varSelectedBuchung.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(varSelectedBuchung.GastName);
  If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm"));
  If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm")) & Char(10) & "für " & varSelectedBuchung.GastName
)
```

#### `lblTitel3_1.Text`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > lblTitel3_1` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1,5 @@
-"Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
+If(
+  IsBlank(varSelectedBuchungTab.GastName);
+  "Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value;
+  "Tisch " & varSelectedBuchungTab.Tisch.Value & "  ·  für " & varSelectedBuchungTab.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(varSelectedBuchungTab.GastName);
  "Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value;
  "Tisch " & varSelectedBuchungTab.Tisch.Value & "  ·  für " & varSelectedBuchungTab.GastName
)
```

#### `lblTitel3_1.Size`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > lblTitel3_1` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-18
+If(IsBlank(varSelectedBuchungTab.GastName); 18; 15)
```

Vollständiger Block:

```
If(IsBlank(varSelectedBuchungTab.GastName); 18; 15)
```

#### `lblTitel3_1.Width`

Ort: `Screen1 > conBuchungen > conVerwaltenDialog_1 > lblTitel3_1` · **ganze Property ersetzen**

Änderung gegenüber dem Export 25.10. 20:09 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-400
+If(IsBlank(varSelectedBuchungTab.GastName); 400; Parent.Width - 24)
```

Vollständiger Block:

```
If(IsBlank(varSelectedBuchungTab.GastName); 400; Parent.Width - 24)
```

## 3. Testbogen (Zeitachse, in der Kopie)
Alle Testbuchungen für **morgen**, damit keine Vergangenheits- oder Check-in-Regel stört. Tische frei wählen, aber getrennt halten. Am Ende alle Testbuchungen stornieren.

| ✓ | Nr | Schritt | Erwartung |
|---|---|---|---|
| ☐ | 0 | Altbestand ansehen: eine bestehende Buchung im Popup, in „My personal desk“, im Tab und im Verwalten-Dialog. Foto vorher, Foto nachher | genau gleich |
| ☐ | 1 | Grundriss: UG Desk 1, morgen 14:00–15:00, „Für mich“ | gebucht, kein Hinweis |
| ☐ | 2 | UG Desk 2, morgen 16:00–17:00, „Für mich“ (andere Zeit) | gebucht, kein Hinweis (eine eigene Buchung, keine Überschneidung) |
| ☐ | 3 | UG Desk 3, morgen 14:00–15:00, „Für mich“ | **Hinweis** „Du hast zu dieser Zeit schon einen Tisch gebucht. Trotzdem …“. **Abbrechen** → nichts gebucht (Tab „Buchungen“ prüfen), Dialog bleibt offen |
| ☐ | 4 | Dasselbe noch einmal → **Trotzdem buchen** | gebucht, Erfolgsmeldung. Doppelklick auf „Trotzdem“ bucht nur einmal |
| ☐ | 5 | UG Desk 4, morgen 14:00–15:00, „Für andere“, Name leer → Speichern | Meldung „Bitte den Namen …“, nichts gebucht |
| ☐ | 6 | Wie 5 mit Name „Test Gast“ | gebucht **ohne Hinweis**, Meldung „… für Test Gast …“. Popup der Kachel: „Test Gast“, darunter „gebucht von <dir>“. Liste/Tab/Verwalten: „für Test Gast“ |
| ☐ | 7 | UG Desk 5, morgen 18:00–19:00 „Für andere“ (Name „Gast 2“), dann UG Desk 6, morgen 18:00–19:00 „Für mich“ | beide ohne Hinweis (Gast-Buchung zählt nicht) |
| ☐ | 8 | Panel: Serie „Für andere“ (Name „Serie Gast“), Mo–Fr nächste Woche, 09:00–10:00; vorher eine eigene Buchung Mo 09:00–10:00 anlegen | Serie ohne Hinweis gebucht, alle Termine mit Gastname |
| ☐ | 9 | Panel: Serie „Für mich“ über dieselbe Woche 09:00–10:00 auf anderem Tisch | Hinweis „An 1 von 5 Terminen …“; Abbrechen → nichts; Trotzdem → alle 5 gebucht |
| ☐ | 9b | Gemischte Serie: vorher einen Termin der Woche 11:00–12:00 auf UG Desk 8 von **jemand anderem** buchen lassen (oder als Gast „Belegt Test“). Dann Serie „Für mich“ 11:00–12:00 auf UG Desk 8 Mo–Fr, mit einer eigenen Buchung Di 11:00–12:00 auf einem anderen Tisch | Hinweis (Di); Trotzdem → 4 von 5 gebucht, Meldung „1× war der Tisch schon belegt“ |
| ☐ | 10 | Tab „Buchungen“ → UG Desk 1 (morgen 14–15) verwalten → +2 Std (überschneidet eigene Desk 2 16–17) → Speichern | Hinweis „Trotzdem verlängern“; **Abbrechen** → unverändert, die Dauer +2 Std bleibt gewählt; Speichern → Hinweis → **Trotzdem verlängern** → 14–17 |
| ☐ | 11 | Tab „Buchungen“ → Gast-Buchung UG Desk 5 (18–19) +1 Std, obwohl Desk 6 (18–19) dir gehört | verlängert, kein Hinweis |
| ☐ | 12 | Gast-Buchung stornieren (Verwalten → Stornieren), eine weitere über Mehrfachauswahl im Tab | beides geht wie bei eigenen |
| ☐ | 13 | Einchecken: eine Gast-Buchung für **heute** in der nächsten halben Stunde anlegen, dann im Dashboard einchecken | Check-in geht durch dich (Gast hat kein Konto) |
| ☐ | 14 | Buchungsdialog und Panel nach Test 6 neu öffnen | Umschalter „Für mich“, Name leer |
| ☐ | 15 | Aufräumen: alle Testbuchungen stornieren | Liste leer |

## 4. Rückfall gesamt
- **Einzelschritte:** siehe jeweiligen Schritt, Originale in Anhang A. Reihenfolge rückwärts: S8 → S7 → S6 → S5 → S4 → S3 → S2.
- **Alles:** frühere Version wiederherstellen (make.powerapps.com → App → Details → Versionen) oder die Sicherung `.msapp`.
- **Die Spalte `GastName` kann bleiben.** Alte Formeln lesen sie nicht, und der Flow reagiert nicht auf sie (geschlussfolgert). Löschen ist nicht nötig.

## 5. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| U1 | `Select(btnSpeichern)` usw. aus dem Hinweis führt den Knopf im Container aus | Test 4, 9, 10. Passiert bei „Trotzdem“ nichts: mir melden. Notweg: Hinweis per „Abbrechen“ schließen geht immer |
| U2 | `GastName` in `varSelectedBuchung`/`varVerlBuchung` (aus `LookUp`): Studio lädt nur benutzte Spalten. In den Sammlungen ist es jetzt per `ForAll` abgesichert | Test 6 (Popup und Verwalten zeigen den Namen) und 11. Fehlt er, zeigen die Anzeigen den Buchenden wie bisher, bzw. der Hinweis erscheint unnötig. Kein falscher Datensatz |
| U3 | Der klassische Umschalter zeigt „Für mich“/„Für andere“ neben dem Schalter in Breite 165 | Sichtprüfung. Sonst `Width` auf 180 |
| U4 | Panel bei Fensterhöhe unter etwa 720: „Speichern“ kann unten abgeschnitten sein | Fenster verkleinern |
| U5 | Rolle von Axel Krägelius und Norman Horn im Hinweistext (Frage 5 offen; NHN ist laut Projektwissen der GoBright-Dienstleister) | Text in `lblFbHinweis.Text` anpassen |
| U6 | Textbreiten sind geschätzt (Open Sans je Zeichenart) | Test 6 mit einem langen Namen ansehen |

## 6. Unabhängige Prüfung
### Unabhängige Prüfung „Für andere buchen“ (26.10.2026)

Geprüft: `werkzeuge/fuer_andere.py`, `bloecke.json`, `pruefung.txt` (129 Properties). Quelle der Wahrheit: Export 25.10. 20:09 (`app.lade_desktop_2510()`) und die Rohdaten `arbeit/_entpackt/desktop_2026-10-25/Controls/*.json` mit Standardwerten. Eigene Skripte im Scratchpad (`python3 -I`).

#### Kurzurteil
- **Speichern (Dialog und Panel) ist richtig gebaut.** Gast-Pflichtname, Gast ohne „ich“-Prüfung, weicher Hinweis, Abbrechen ohne Schreiben, Serie, Sammel-Patch mit `GastName`: alles gegen den Export nachvollzogen.
- Sperre, `IfError`, Nachlese und Ladezeile sind unverändert. Das ist maschinell belegt: Rückübersetzung 0 Abweichungen, alle Vorher-Fassungen zeichengleich, die Diffs enthalten nur die Einfügungen.
- **Doppelklick auf „Trotzdem“ ist abgesichert.** `!varIsLoading && varFbZeige` gilt im Knopf, die 2-s-Sperre steht am Ende des Zielknopfs.
- **Ein hängendes `varFbTrotzdem` habe ich nicht gefunden.** Der Hinweis lässt sich nur über „Abbrechen“ oder über einen Lauf des Zielknopfs schließen, und beide setzen die Variable zurück.
- **„Trotzdem verlängern“ funktioniert nie (B1, hoch).** Vor dem Einfügen beheben.
- **Mehrere neue Texte werden abgeschnitten oder überlappen (B2, B3).** Die Breitenschätzung des Generators fällt hinter CLAUDE.md §8 zurück.
- **UNSICHER: Kommt `GastName` in den Sammlungen an (B4)?** Dafür braucht es einen Test.
- **Urteil:** Erst nach B1 bis B3 einfügen. Den Testbogen um B4 und B11 ergänzen.

#### Befunde

| Nr | Schwere | Ort | Befund | Beleg | Vorschlag |
|---|---|---|---|---|---|
| B1 | **hoch** | `btnVerlängern.OnSelect`, `btnVerlängern_1.OnSelect` (S6) | **„Trotzdem verlängern“ verlängert nie.** Im Lauf, der den Hinweis zeigt, laufen danach `Refresh`, die Ladezeile und `Set(varAusgewaehltePlusDauer, Blank())`. Beim Tippen auf „Trotzdem“ ist die Dauer also leer. Damit ist `btnVerlängern.DisplayMode` = Disabled (`IsBlank(varAusgewaehltePlusDauer)`). Zwei Fälle: Läuft `Select` trotzdem, endet der Lauf im ersten Zweig „Bitte eine Dauer auswählen.“. Läuft `Select` bei gesperrtem Knopf nicht (UNSICHER), passiert nichts, und der Hinweis bleibt offen, bis man „Abbrechen“ tippt. | Export: Ende von `btnVerlängern.OnSelect` mit `Set(varAusgewaehltePlusDauer, Blank())` nach dem äußeren `If`. Dazu `btnVerlängern.DisplayMode` und der erste Zweig `IsBlank(varAusgewaehltePlusDauer) \|\| … = 0` → Notify. `btnVerlängern_1` ist gleich gebaut. | Die Zeile ersetzen durch `If(!varFbZeige, Set(varAusgewaehltePlusDauer, Blank()))`. Dann bleibt die Dauer samt grüner Markierung für „Trotzdem“ erhalten, und `Abbrechen` muss sie nicht löschen. In den Generator eine Prüfung aufnehmen: Kein Zustand, den der Zielknopf liest (Dauer, `DisplayMode`-Bedingung), darf im Hinweis-Lauf geändert werden. Test „Trotzdem verlängern“ aufnehmen (siehe B11). |
| B2 | mittel | `lblPerson.Text`, `lblZeit3.Text`, `lblFbHinweis` (S8/S2) | **Mehrzeilige Texte stehen in Labels fester Höhe.** `lblPerson` ist 40 hoch (Y 71–111), bekommt aber Gastname + `Char(10)` + „gebucht von Josias Semeraf“. Die zweite Zeile ist ca. 237 px breit bei 225 verfügbar, das ergibt 3 Zeilen. Bei Size 13 braucht das ca. 57–80 px. `lblZeit3` (`conVerwaltenDialog`, 150 × 40, Y 50–90, darunter die Knöpfe ab Y 100) bekommt Zeit + `Char(10)` + „für Max Mustermann“ (ca. 171 px bei 140). Auch das sind 3 Zeilen in 40 px, abgeschnitten. Der Hinweistext einer Serie hat geschätzt 6 Zeilen ≈ 151 px in `lblFbHinweis.Height` 130, die Kontaktzeile fällt weg. Der Generator prüft nur Breiten und keine Höhen. | Rohdaten: `lblPerson` Height 40, `lblStatus` Y 45 + H 26, `lblZeit2` Y 100, `conDetailsPopup.Height` 154, `lblZeit3` Y 50 H 40, `btnSchließen4` Y 100. Schätzung mit `textbreite()` aus `handy_tisch_zeigen.py` (Zeichenart, pt→px 1,333). | Detail-Popup: Gastname allein in `lblPerson` (eine Zeile), „gebucht von …“ in die Zeile von `lblZeit2` oder in ein neues Label. Alternativ `conDetailsPopup.Height` bei Gast erhöhen. `lblZeit3`: Gast nicht anhängen, sondern `lblTitel3` („Tisch …“) oder ein eigenes Label nutzen. `lblFbHinweis.Height` auf 145 setzen (Knöpfe ab 170) oder die Kontaktzeile kürzen. Im Generator eine Höhenprüfung ergänzen (Zeilen × Size × 1,333 × 1,36 + 10). |
| B3 | mittel | `lblZeitHeute.Text` (My personal desk), dazu `lblRaumZeit.Text`, `lblTitel3_1`, `btnFbTrotzdem.Text` | **Überlappung und abgeschnittene Texte.** `lblZeitHeute` liegt bei X 100 (Breite 297, Y ≈ 52–74), `lblStatusHeute` bei X 270–420, Y 43–83 („Einchecken“/„Eingecheckt“/„Verfallen“, linksbündig). Schon „08:00 – 12:00  ·  für Max“ ist ca. 190 px breit und läuft damit in den Status hinein. `lblRaumZeit` überlappt im Auswahlmodus `chkAuswahl` (X 465). Bei 1366 überlappt es ab ca. 365 px Text, geschätzt 378 px. `lblTitel3_1` (Size 18, Höhe 40) bricht bei Namen ab etwa 10 Zeichen um, dann ist die zweite Zeile abgeschnitten. „Trotzdem verlängern“ (Size 15) braucht ca. 216 px in 190. Der Generator schätzt mit `len × Size × 0,56`, ohne pt→px. Genau dieser Fehler steht in CLAUDE.md §8 („Tisch zeigen“ passte nicht). | Rohdaten `galTischbuchungenHeute`: `lblTischHeute` X 100, W `TemplateWidth − 173`, `lblStatusHeute` X 270. `galAlleTischbuchungen`: `chkAuswahl.X` = `btnVerwalten_2.X − 60`. `conVerwaltenDialog_1` bei 1366 Breite 550. | Gastname in eine eigene, auf `lblStatusHeute.X − Self.X` begrenzte Zeile oder kürzen (`Left(…; 14) & "…"`). Knopftext „Trotzdem“ / „Abbrechen“ oder Size 13. Im Generator die Schätzfunktion je Zeichenart aus `handy_tisch_zeigen.py` übernehmen und gegen Nachbar-Steuerelemente prüfen, nicht nur gegen die eigene Breite. |
| B4 | mittel, UNSICHER | `RemoveIf(colNeuIch, … !IsBlank(GastName) …)`, `RemoveIf(colVerlIch, … !IsBlank(GastName) \|\| !IsBlank(varVerlBuchung.GastName) …)` | **`GastName` wird nur über Sammlungen und Variablen gelesen.** Bei `sharepointselectsenabled: true` lädt die App nur Spalten, die die Datenflussanalyse als genutzt erkennt. Für `Erstellt` in Sammlungen ist das bis heute nicht belegt (Abschlussanalyse A7, Test 17). Kommt `GastName` leer an, zählen eigene Gast-Buchungen wieder als „ich“. Folge: Ein falscher Hinweis beim Buchen und Verlängern, also weich, aber genau der Fall, den Josias ausschließen will. Josias' Testliste prüft nur die Gegenrichtung (Gast buchen, wenn eigene da sind). Die geht über `varFbFuerAndere` und hängt nicht an der Spalte. | `Properties.json`: `sharepointselectsenabled: true`. `ABSCHLUSSANALYSE.md` A7, `pruefbericht_desktop.md` Z. 52. | Test mit Zeitachse: (1) Für Gast 10–12 an Tisch A buchen, danach für mich 10–12 an Tisch B → **kein** Hinweis. (2) Eigene Buchung verlängern, die eine eigene Gast-Buchung überschneidet → kein Hinweis. (3) Gast-Buchung verlängern → kein Hinweis. Kommt der Hinweis doch, ist `GastName` in der Sammlung leer. Rückweg: Gast-Ausschluss direkt im Datensatz, z. B. `ClearCollect(colNeuIch; ForAll(Filter(…) As B; {ID: B.ID; Startzeit: B.Startzeit; Endzeit: B.Endzeit; CheckedIn: B.CheckedIn; Erstellt: B.Erstellt; GastName: B.GastName}))`, wie bei der Ladezeile, die mit `B.Erstellt` im `ForAll` sicher ist. |
| B5 | niedrig | `btnVerlängern(_1).OnSelect` | Der Hinweis „Trotzdem verlängern?“ steht vor der Prüfung `colVerlKonflikt`. Wer bestätigt, bekommt danach „Der Tisch ist in dieser Zeit inzwischen belegt“. Beim Speichern ist es richtig: „tisch“ geht vor „ich“. | Reihenfolge der Zweige im `If` (Hinweis, dann `!IsEmpty(colVerlKonflikt)`). | Den Hinweis-Zweig hinter den Konflikt-Zweig stellen. |
| B6 | niedrig | `bloecke.json`, `pruefung.txt` | `lblPerson.Width` ist eine bestehende Property (Standard **150** in `Controls/4.json`, fehlt nur im YAML), steht aber als `art: "neu"` ohne Vorher-Fassung. Damit fehlt der Rückfall. „115 an 9 neuen Steuerelementen“ stimmt nicht: Es sind 114 + 1 an einem bestehenden. | `bloecke.json` (einziger Eintrag „neu“ außerhalb von `neue`), Rohregel `lblPerson.Width = 150`. | Den Generator für bestehende Steuerelemente Standardwerte aus den Rohdaten lesen lassen. Dann gilt `art = ersetzen` und der Rückfall lautet `150`. |
| B7 | niedrig | Einfügeanleitung (S2), Ebenen | Die Ebenen sind nicht vorgegeben. Neue Steuerelemente landen in `Screen1` ganz oben, also auch über `conLadeOverlay` (heute die oberste Ebene, Export-Reihenfolge). `btnFbHintergrund` muss unter `conFbHinweis` liegen, beide über `conBuchungDialog`, `conTischBuchungenPanel`, `conVerwaltenDialog` und `conBuchungen`. Im Hinweis-Lauf laufen nach `Set(varFbZeige, true)` noch Ladezeile und `Refresh`. In dieser Zeit liegt der Hinweis über dem Ladebild und „Trotzdem“ ist 1–3 s grau. | Export: Kinder von `Screen1`, `conLadeOverlay` vorletzte Stelle. | In der Anleitung festlegen: zuerst `btnFbHintergrund`, dann `conFbHinweis` einfügen, danach `conLadeOverlay` → „Nach vorne bringen“. |
| B8 | niedrig | `btnHitArea.OnSelect` / Nachtrag 6 | Nachtrag 6 (nicht eingefügt) ersetzt dieselbe Property (R3). `btnNeuBuchenHeute` (R2) öffnet `conBuchungDialog`, ohne `tglFuerAndere`/`txtGastName` zurückzusetzen. Fügt Josias N6 später ein, überschreibt einer den anderen, oder der Schalter bleibt vom letzten Öffnen stehen. | Überschneidungsprüfung gegen `2026-10-12_Nachtrag6/bloecke.json`: nur `btnHitArea.OnSelect`. Andere offene Pakete: keine Überschneidung. | Im Dokument vermerken. Wer N6 später einfügt, erzeugt N6 neu und nimmt die Resets an beiden Öffnern mit. |
| B9 | niedrig | Check-in (`conCheckinDialog.lblTitel`, `Timer1.OnTimerEnd`, `App.OnStart`) | Gast-Buchungen erscheinen beim Buchenden als eigene Check-in-Frage („Check-in: Tisch X“), ohne Gastnamen. Mit „Trotzdem buchen“ und mit Gast-Buchungen kann der Buchende jetzt zwei Buchungen zur selben Zeit haben. Die Frage nimmt die früheste, und er sieht nicht, ob er für sich oder für den Gast eincheckt. Funktional ist 2a erfüllt. | `Timer1.OnTimerEnd`: `colCheckinFrage` nach `Person.Email`, `First(SortByColumns(…))`. | `lblTitel` in `conCheckinDialog` wie die anderen Anzeigen mit „für <Gast>“ ergänzen (ohne Abfrage, `varSelectedBuchung` ist ein ganzer Datensatz). |
| B10 | niedrig | Handy-App | Die Folge reicht über Josias' Antwort 6 hinaus. Nicht nur Gast-Buchungen, auch eigene Doppelbuchungen per „Trotzdem“ blockieren am Handy hart das Verlängern beider Buchungen. Das Handy zeigt Gast-Buchungen als eigene, ohne Namen. | Handy-Regel „keine zwei Tische“ (`btnVerl1/2`, Diagnose Abschnitt 1). | Für Josias als Hinweis aufnehmen. Kein Code. |
| B11 | niedrig | Testbogen (Auftrag Abschnitt 6) | Josias' Liste geht von „2 Buchungen“ aus. Mit Regel A gibt es schon bei **einer** überschneidenden eigenen Buchung einen Hinweis („0/1 eigene ohne Meldung“ stimmt nur ohne Überschneidung). Es fehlen: Trotzdem verlängern (hätte B1 gefunden), Abbrechen im Verlängern-Hinweis, Doppelklick auf „Trotzdem“, Serie mit gemischt „tisch“/„ich“, B4 (1)–(3). | Auftrag Abschnitt 6, Regel A aus der Diagnose. | Testbogen als Zeitachse mit Überschneidungen schreiben (CLAUDE.md §8). |
| B12 | Hinweis, UNSICHER | `lblFbHinweis.Text` | Die Kontaktzeile „Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT)“ ist unbestätigt (Frage 5 offen). Laut CLAUDE.md ist NHN der GoBright-Dienstleister, IT-Admin ist Michael. | CLAUDE.md §5a, Diagnose Frage 5. | Vor dem Einfügen von Josias bestätigen lassen, sonst die Zeile weglassen. |

#### Geprüft ohne Befund
- **Gast:** `varFbFuerAndere` leert `colNeuIch` ganz (keine „ich“-Prüfung). Die „tisch“-Prüfung bleibt. `Trim` + `IsBlank("")` erzwingen den Pflichtnamen. Der Name wird vor der Vergangenheits- und Tischprüfung geprüft, nach „Tisch wählen“.
- **Hinweis:** `varNeuIchBelegt > 0` steht vor „alles belegt“. Bei einem einzelnen Termin geht „tisch“ vor „ich“ (`If`-Reihenfolge in `Grund`), dann kommt kein Hinweis. Der Hinweis-Zweig schreibt nichts. „Abbrechen“ setzt nur `varFbZeige`/`varFbTrotzdem` zurück, Dialog und Eingaben bleiben stehen.
- **Trotzdem:** Das Ziel wird über `varFbQuelle` gewählt, und jede Quelle hat einen eigenen Zweig. Der Zielknopf verbraucht die Bestätigung als erste Anweisung nach `varIsLoading` und blendet den Hinweis aus. `Set(varSperreBis, Blank())` ist nötig, weil der Hinweis-Lauf die 2-s-Sperre gesetzt hat.
- **Doppelklick:** Klick 2 wird entweder vom Wächter im Knopf geblockt (`varIsLoading`/`varFbZeige`), oder der zweite eingereihte Lauf scheitert an der Sperre, die Lauf 1 am Ende setzt. In beiden Fällen bleibt `varFbTrotzdem` = false.
- **`btnSpeichern`/`btnSpeichernTischePanel`:** `DisplayMode` hängt nur an `varIsLoading` bzw. dem gewählten Tisch. Beides ändert der Hinweis-Lauf nicht. `Timer1` läuft bei offenem Dialog, Panel oder Verwalten nicht, kann den Hinweis also nicht stören.
- **Typen:** Alle Zuweisungen an `varSelectedBuchung`/`Tab` sind Datensätze aus `Tischbuchungen` (`ThisItem` aus ungeformten Galerien oder `LookUp`), `.GastName` passt also. `varFbGast` ist Text oder Blank, die `varFb…`-Schalter sind Boolean. Nicht vorbelegt heißt Blank, das verhält sich wie false.
- **Delegation:** Kein `GastName` im Server-Filter, die Server-Filter sind unverändert.
- **Altbestand:** Bei leerem `GastName` ist der Originaltext zeichengleich im ersten Zweig. Die Altwerte 150/100/400 stimmen mit den Rohdaten überein.
- **Properties:** Alle verwendeten Properties gibt es am jeweiligen Typ. Toggle: `TrueText`/`FalseText`/`TrueFill`/`Font`/`Size`, belegt an `tglTagFr_1`. Classic TextInput: `HintText`/`MaxLength`/`Default`; in der App gibt es noch keine Texteingabe, die Properties sind Standard. Container: `Radius*`. Keine Kommentare, ganze Properties, Namen aus dem Export, Präfix `varFb`, keine toten Variablen.
- **Lage:** Dialog-Schalter und Namensfeld (X 270–435, Y 122–226) überlappen nichts (Label2 bis Y 100, `Rectangle5` bei Y 278, Wochentage ab Y 290). Die Panel-Zeile Y 531–571 und Speichern 591–631 liegen innerhalb von 678.
- **Unverändert:** Storno, Mehrfach-Storno und Einchecken (über `Person`). Der Flow ist nicht im Export, und die Spalte ist optional.
- UNSICHER, durch B1 gegenstandslos: Ob `Select()` auf einen gesperrten Knopf feuert. In Studio prüfen: `btnVerlängern` gesperrt lassen, „Trotzdem“ tippen.

### Was aus den Befunden wurde
| Nr | Befund | Umsetzung |
|---|---|---|
| B1 | „Trotzdem verlängern“ fand die Dauer gelöscht | behoben: Dauer bleibt bei offenem Hinweis stehen, Prüfung im Generator |
| B2 | Mehrzeilige Texte in festen Höhen abgeschnitten | behoben: Größe und Höhe nur bei Gast angepasst, Höhen gerechnet, Hinweis 500 × 280 |
| B3 | Überlappungen, zu lange Texte, falsche Schätzung | behoben: Name in zweiter Zeile unter der Zeit, Tab-Titel kürzer, Knöpfe Größe 13. Schätzung je Zeichenart in Pixeln, Prüfungen an den gelieferten Werten (Mutation erkennt falsche Größe/Höhe) |
| B4 | `GastName` in Sammlungen evtl. nicht geladen | behoben für `colNeuIch`/`colVerlIch` (Projektion). Für Datensatz-Variablen bleibt U2 mit Test |
| B5 | Hinweis vor „Tisch belegt“ beim Verlängern | behoben: Reihenfolge getauscht, Prüfung im Generator |
| B6 | `lblPerson.Width` ist bestehend (Standard 150) | behoben: als „bisher Standard“ mit Rückfallwert ausgewiesen, Zählung korrigiert |
| B7 | Ebenen | steht in Abschnitt 1 (Einfügen, Ganz nach vorne, `conLadeOverlay` zuletzt) |
| B8 | Nachtrag 6 ändert auch `btnHitArea.OnSelect` | in der Kurzfassung: N6 wird danach neu erzeugt |
| B9 | Check-in-Dialog ohne Gastnamen | nach der Abnahme, kein Muss (der Buchende sieht Tisch und Zeit) |
| B10 | Handy: auch eigene Doppelbuchungen per „Trotzdem“ sperren dort das Verlängern | Josias zur Kenntnis, Handy-Anpassung nach der Abnahme |
| B11 | Testliste unvollständig | ergänzt: Abbrechen im Verlängern-Hinweis, gemischte Serie (9b), Anzeige des Namens (6) |
| B12 | Kontaktzeile unbestätigt | U5 |

## Anhang A: Originale aus dem Export 25.10. 20:09 (Rückfall)

**`btnSpeichernTischePanel.Y`**

```
tglTagFr_1.Y + tglTagFr_1.Height + 20
```

**`btnSpeichern.OnSelect`**

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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnSpeichernTischePanel.OnSelect`**

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
    With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())))
  );;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern.OnSelect`**

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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
```

**`btnVerlängern_1.OnSelect`**

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
  With({neu: ForAll(Filter(Tischbuchungen; (Endzeit > varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum; 1; TimeUnit.Days)) || (Endzeit >= Now() && Startzeit <= DateAdd(Now(); 60; TimeUnit.Minutes))) As B; {TischName: B.Tisch.Value; Startzeit: B.Startzeit; Endzeit: B.Endzeit; Eingecheckt: B.CheckedIn; Name: B.Person.DisplayName; Erstellt: B.Erstellt})}; If(IsError(neu) || IsError(First(neu)); Notify("Grundriss konnte nicht aktualisiert werden. Bitte auf Aktualisieren tippen."; NotificationType.Warning); ClearCollect(colGrundriss; DropColumns(Filter(neu; Eingecheckt || Startzeit > varFreigabeGrenze || Erstellt > varFreigabeGrenze); Erstellt));; Set(varGrundrissStand; Now())));;
  Set(varAusgewaehltePlusDauer; Blank());;
  Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));;
  Set(varIsLoading; false)
)
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
Set(varEndeOverridePanel; "");;
Set(varPanelJetzt; Now());;
Set(varFreigabeGrenze; DateAdd(Now(); -Coalesce(varFreigabeMinuten; 30); TimeUnit.Minutes));;
Reset(ddStartTischePanel);;
Reset(ddEndTischePanel);;
Reset(dpWiederholenBis_1)
```

**`lblPerson.Text`**

```
varSelectedBuchung.Person.DisplayName
```

**`lblZeit2.Y`**

```
100
```

**`lblZeitHeute.Text`**

```
Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm")
```

**`lblZeitHeute.Height`**

```
Self.Size * 1,8
```

**`lblRaumZeit.Text`**

```
Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm")
```

**`lblRaumZeit.Height`**

```
Self.Size * 1,8
```

**`lblZeit3.Text`**

```
If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm"))
```

**`lblTitel3_1.Text`**

```
"Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel3_1.Size`**

```
18
```

**`lblTitel3_1.Width`**

```
400
```

## Anhang B: Maschinelle Prüfung

```
Für andere buchen: 137 Properties: 17 bestehende ersetzt, 6 an bestehenden Steuerelementen neu gesetzt (bisher Standard), 114 an 9 neuen Steuerelementen. Grundlage: Export 25.10. 20:09.
Bisher Standard: lblPerson.Height (40), lblPerson.Size (13), lblPerson.Width (150), lblZeit3.Height (40), lblZeit3.Size (13), lblZeit3.Width (150)
Geänderte bestehende Properties: btnHitArea.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnSpeichernTischePanel.Y, btnTischHinzufügen.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect, lblPerson.Text, lblRaumZeit.Height, lblRaumZeit.Text, lblTitel3_1.Size, lblTitel3_1.Text, lblTitel3_1.Width, lblZeit2.Y, lblZeit3.Text, lblZeitHeute.Height, lblZeitHeute.Text
neue Variablen: varFbBestaetigt, varFbFuerAndere, varFbGast, varFbQuelle, varFbText, varFbTrotzdem, varFbZeige
Textbreite tglFuerAndere Text: „Für andere“ ca. 97 von 110
Textbreite btnFbTrotzdem: „Trotzdem verlängern“ ca. 187 von 200
Textbreite btnFbAbbrechen: „Abbrechen“ ca. 92 von 200
Textbreite lblPerson Zeile 2: „gebucht von Josias Semeraf“ ca. 211 von 215
Textbreite lblZeit3 Zeile 2 (bis btnPlus1Std X 175): „für Max Mustermann“ ca. 138 von 152
Textbreite lblZeitHeute Zeile 1 (bis lblStatusHeute X 270): „08:00 – 12:00“ ca. 101 von 158
Textbreite lblZeitHeute Zeile 2: „für Max Mustermann“ ca. 166 von 285
Textbreite lblRaumZeit Zeile 2 (bis chkAuswahl): „für Max Mustermann“ ca. 166 von 353
Textbreite lblTitel3_1 Gast: „Tisch UG Desk 14  ·  für Max Mustermann“ ca. 408 von 516
Höhe lblPerson (Gast): 2 Zeilen ca. 45 von 46
Höhe lblZeit3 (Gast): 2 Zeilen ca. 42 von 50
Höhe lblZeitHeute (Gast): 2 Zeilen ca. 38 von 43
Lage Popup lblPerson bis lblZeit2: 117 ≤ 118
Lage Popup lblZeit2 Textmitte: 148 ≤ 154
Lage Verwalten lblZeit3 bis Knöpfe: 100 ≤ 100
Lage Karte lblZeitHeute 2 Zeilen: 95 ≤ 104
Höhe lblFbHinweis: längster Text 6 Zeilen ca. 135 von 180
lblPerson.Width: Altbestand 150 (Standard, im Export nicht gesetzt)
lblPerson.Size: Altbestand 13 (Standard, im Export nicht gesetzt)
lblPerson.Height: Altbestand 40 (Standard, im Export nicht gesetzt)
lblZeit2.Y: Altbestand 100
lblZeit3.Size: Altbestand 13 (Standard, im Export nicht gesetzt)
lblZeit3.Width: Altbestand 150 (Standard, im Export nicht gesetzt)
lblZeit3.Height: Altbestand 40 (Standard, im Export nicht gesetzt)
lblTitel3_1.Size: Altbestand 18
lblTitel3_1.Width: Altbestand 400
lblZeitHeute.Height: Altbestand Self.Size * 1.8
lblRaumZeit.Height: Altbestand Self.Size * 1.8
Prüfung: 0 Fehler
```

Mutationstest: 13 von 13 absichtlich eingebauten Fehlern erkannt (GastName nicht gespeichert, Altbestand verändert, Panel liest Dialog-Schalter, Verlängern ohne Bestätigung, unbekannter Knopf im Select, Variable ohne Präfix, Trotzdem blendet selbst aus, Altbestand-Breite fehlt, Dauer gelöscht bei offenem Hinweis, Sammlung ohne GastName-Spalte, zu große Schrift, zu kleine Höhe, zu schmaler Hinweis).
