# Für andere buchen + weicher Hinweis (Tischbuchung Desktop, 26.10.2026)

Für Josias. Grundlage: **Export 25.10. 20:09** (`Tischbuchungsapp25.10.26_20261025200901.zip`). Erzeugt und maschinell geprüft mit `werkzeuge/fuer_andere.py` (0 Fehler, Mutationstest 8 von 8 erkannt). **Noch nicht unabhängig geprüft**. In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

**Voraussetzung:** Jeder Block ersetzt die **ganze** Property. Hast du nach dem 25.10. 20:09 an einer der 14 geänderten Properties etwas gespeichert, erst neu exportieren, ich erzeuge die Blöcke dann neu.

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
- **Umfang:** 14 bestehende Properties und 9 neue Steuerelemente, alle direkt im Screen oder im jeweiligen Container. Keine Auto-Layout-Container.
  - Neue Variablen tragen alle den Präfix `varFb…` (7 Stück).
  - Kein neuer Server-Filter: `GastName` wird nur lokal geprüft, deshalb keine neue Delegationswarnung.
- **Nicht angefasst:**
  - Ladezeile (17×), Tischpositionen, Grundriss-Layout.
  - Check-in, Stornieren, Mehrfach-Storno, Freigabe, App.OnStart.
  - Der nächtliche Lösch-Flow filtert nur nach `Endzeit` (laut Betriebshandbuch). Er ist nicht im Export.
- **Handy-App:** unverändert. Bekannte Folge, von dir akzeptiert: Gast-Buchungen blockieren dort den Buchenden zur selben Zeit.
- **Hinweistext:** Er nennt „Fragen: Axel Krägelius (PC-Admin) oder Norman Horn (Admin, NHN IT).“ Frage 5 ist offen. Ändern geht an einer Stelle: `lblFbHinweis.Text`.

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

**Was:** Ein Hinweis mit Vollbild-Hintergrund. Der Hintergrund fängt alle Klicks ab, solange der Hinweis offen ist. Daneben ist nichts bedienbar, also kann sich auch keine Variable ändern.
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
| `Width` | `440` |
| `Height` | `230` |
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
| `Height` | `130` |
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
| `Size` | `15` |
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
| `Size` | `15` |
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
@@ -44,3 +51,3 @@
     ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
-    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
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
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
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
@@ -44,3 +51,3 @@
     ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
-    RemoveIf(colNeuIch; !CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze);;
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
    ClearCollect(colNeuIch; Filter(Tischbuchungen; Person.Email = varNeuEmail && Startzeit < varNeuSpanEnde && Endzeit > varNeuSpanStart));;
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
2. Eigene andere Buchungen zur selben Zeit: Gast-Buchungen zählen nicht. Eine Gast-Buchung wird ohne diese Prüfung verlängert.
3. Statt „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ (Sperre) kommt der Hinweis mit „Trotzdem verlängern“.
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
@@ -18,3 +21,3 @@
     ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
-    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
@@ -26,4 +29,6 @@
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
-      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
+      Set(varFbQuelle; "verl");;
+      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
+      Set(varFbZeige; true);
       varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
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
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
      Set(varFbQuelle; "verl");;
      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
      Set(varFbZeige; true);
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
@@ -18,3 +21,3 @@
     ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
-    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
+    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
     If(
@@ -26,4 +29,6 @@
       Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
-      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch);
-      Notify("Du hast in dieser Zeit schon einen anderen Tisch gebucht."; NotificationType.Warning);
+      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
+      Set(varFbQuelle; "verltab");;
+      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
+      Set(varFbZeige; true);
       varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlKonflikt);
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
    ClearCollect(colVerlIch; Filter(Tischbuchungen; Person.Email = User().Email && Startzeit < varVerlEndeNeu && Endzeit > varVerlEndeAlt));;
    RemoveIf(colVerlIch; ID = varVerlBuchung.ID || !IsBlank(GastName) || !IsBlank(varVerlBuchung.GastName) || (!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze));;
    If(
      !varVerlBuchung.CheckedIn && varVerlBuchung.Startzeit <= varFreigabeGrenze && varVerlBuchung.Erstellt <= varFreigabeGrenze;
      Notify("Diese Buchung ist verfallen, weil nicht rechtzeitig eingecheckt wurde. Bitte neu buchen."; NotificationType.Warning);
      varVerlEndeNeu <= varVerlBuchung.Startzeit;
      Notify("Die Buchung wäre danach leer. Bitte weniger verkürzen."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && varVerlEndeNeu > varVerlTagesende;
      Notify("Eine Buchung kann nicht nach 22:00 Uhr enden."; NotificationType.Warning);
      varAusgewaehltePlusDauer > 0 && !IsEmpty(colVerlIch) && !varFbBestaetigt;
      Set(varFbQuelle; "verltab");;
      Set(varFbText; "Du hast in dieser Zeit schon einen anderen Tisch gebucht. Trotzdem verlängern?");;
      Set(varFbZeige; true);
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
- Im Popup wird `lblPerson` nur bei Gast-Buchungen breiter (bis vor das Bild) und zweizeilig. Die Zeitzeile `lblZeit2` rückt dann 12 nach unten, sonst würde die zweite Zeile sie berühren.
- Im Tab-Verwalten-Dialog wird der Titel nur bei Gast-Buchungen breiter.

**Rückfall:** alle Properties aus Anhang A.

#### `lblPerson.Width`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (im Export nicht gesetzt, Standardwert)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 150; Image7.X - Self.X - 6)
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
+If(IsBlank(varSelectedBuchung.GastName); 100; 112)
```

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 100; 112)
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
+  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & "  ·  für " & ThisItem.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(ThisItem.GastName);
  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
  Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & "  ·  für " & ThisItem.GastName
)
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
+  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & "  ·  für " & ThisItem.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(ThisItem.GastName);
  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm");
  Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm") & "  ·  für " & ThisItem.GastName
)
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
+  "Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value & "  ·  für " & varSelectedBuchungTab.GastName
+)
```

Vollständiger Block:

```
If(
  IsBlank(varSelectedBuchungTab.GastName);
  "Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value;
  "Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value & "  ·  für " & varSelectedBuchungTab.GastName
)
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
| ☐ | 9 | Panel: Serie „Für mich“ über dieselbe Woche 09:00–10:00 auf anderem Tisch | Hinweis „An x von y Terminen …“; Abbrechen → nichts; Trotzdem → alle Termine gebucht |
| ☐ | 10 | Tab „Buchungen“ → UG Desk 1 (morgen 14–15) verwalten → +2 Std (überschneidet eigene Desk 2 16–17) → Speichern | Hinweis „Trotzdem verlängern“; Abbrechen → unverändert; Trotzdem → 14–17 |
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
| U2 | `GastName` kommt in den Sammlungen `colNeuIch`/`colVerlIch` an (Studio lädt nur benutzte Spalten) | Test 7 und 11. Wenn nicht, erscheint der Hinweis bei Gast-Überschneidung unnötig, gebucht werden kann trotzdem. Kein falscher Datensatz |
| U3 | Der klassische Umschalter zeigt „Für mich“/„Für andere“ neben dem Schalter in Breite 165 | Sichtprüfung. Sonst `Width` auf 180 |
| U4 | Panel bei Fensterhöhe unter etwa 720: „Speichern“ kann unten abgeschnitten sein | Fenster verkleinern |
| U5 | Rolle von Axel Krägelius und Norman Horn im Hinweistext (Frage 5 offen) | Text in `lblFbHinweis.Text` anpassen |

## 6. Unabhängige Prüfung
Läuft noch.

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

**`lblRaumZeit.Text`**

```
Text(ThisItem.Startzeit; "dd.mm.yyyy") & "  " & Text(ThisItem.Startzeit; "hh:mm") & " – " & Text(ThisItem.Endzeit; "hh:mm")
```

**`lblZeit3.Text`**

```
If(IsBlank(varSelectedBuchung); ""; Text(varSelectedBuchung.Startzeit; "hh:mm") & " – " & Text(varSelectedBuchung.Endzeit; "hh:mm"))
```

**`lblTitel3_1.Text`**

```
"Verwalten: Tisch " & varSelectedBuchungTab.Tisch.Value
```

**`lblTitel3_1.Width`**

```
400
```

## Anhang B: Maschinelle Prüfung

```
Für andere buchen: 129 Properties (14 bestehende geändert, 115 an 9 neuen Steuerelementen). Grundlage: Export 25.10. 20:09.
Geänderte bestehende Properties: btnHitArea.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnSpeichernTischePanel.Y, btnTischHinzufügen.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect, lblPerson.Text, lblRaumZeit.Text, lblTitel3_1.Text, lblTitel3_1.Width, lblZeit2.Y, lblZeit3.Text, lblZeitHeute.Text
neue Variablen: varFbBestaetigt, varFbFuerAndere, varFbGast, varFbQuelle, varFbText, varFbTrotzdem, varFbZeige
Textbreite Schalter: „Für andere“ ca. 73 von 105
Textbreite Schalter: „Für mich“ ca. 58 von 105
Textbreite btnFbTrotzdem: „Trotzdem verlängern“ ca. 160 von 178
Textbreite btnFbAbbrechen: „Abbrechen“ ca. 76 von 178
Textbreite lblPerson: „gebucht von Josias Semeraf“ ca. 189 von 215
Textbreite lblZeit3: „für Max Mustermann“ ca. 131 von 140
Textbreite lblZeitHeute: „08:00 – 12:00  ·  für Max Mustermann“ ca. 242 von 285
Panel: Zeile „Für andere“ Y 531–571, Speichern Y 591–631, Panelhöhe bei 768 = 678
Dialog: Schalter X 270–435, Y 122–162, Namensfeld Y 186–226; frei zwischen Image2 (bis 245) und Eingaben (ab 448); Wochentage erst ab Y 290
Prüfung: 0 Fehler
```

Mutationstest: 8 von 8 absichtlich eingebauten Fehlern erkannt (GastName nicht gespeichert, Altbestand verändert, Panel liest Dialog-Schalter, Verlängern ohne Bestätigung, unbekannter Knopf im Select, Variable ohne Präfix, Trotzdem blendet selbst aus, Altbestand-Breite fehlt).
