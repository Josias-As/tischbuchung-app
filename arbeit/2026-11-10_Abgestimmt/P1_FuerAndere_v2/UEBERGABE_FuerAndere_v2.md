# P1 Für andere buchen + weicher Hinweis, Fassung 2 (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`). Grundlage: **Export 10.11. 08:13** („echt“, zeichengleich mit 25.10.). Erzeugt und geprüft mit `werkzeuge/fuer_andere_v2.py` (0 Fehler) und `werkzeuge/abstimmung.py` (alle Pakete zusammen, 0 Fehler). Ersetzt Fassung 1 (`arbeit/2026-10-26_FuerAndere/`, bleibt erhalten). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

**Prüfstatus:** Die Logik (Speichern, Verlängern, Hinweis, Anzeige) ist dieselbe wie in Fassung 1, die **unabhängig geprüft** wurde (12 Befunde, B1–B5 behoben, Abschnitt 6). **Neu in Fassung 2 und nur maschinell geprüft:** Stil der neuen Steuerelemente aus der App, Titelzeile im Hinweis, Hinweis 580 breit, Kartenposition bei Gästen.

## Kurzfassung
- **Deine Entscheidungen:** 1 A, 2 a, 3 ja, 4 ja, 6 ok.
  - Die vorhandene Regel „kein zweiter Tisch zur selben Zeit“ sperrt nicht mehr. Stattdessen fragt ein Hinweis „Zur selben Zeit schon gebucht“ mit **Abbrechen / Trotzdem buchen** (beim Verlängern „Trotzdem verlängern“).
  - Gäste checkt der Buchende ein. Der Gastname steht im Popup, die Kachel zeigt weiter die Kürzel des Buchenden. Serien gehen für Gäste wie für dich, ohne Prüfung auf eigene Buchungen.
- **Für andere buchen:** Im Buchungsdialog und im Panel gibt es den Umschalter **„Für mich / Für andere“**. Bei „Für andere“ erscheint ein Namensfeld (Pflicht, höchstens 100 Zeichen). Gespeichert wird in der neuen Spalte `GastName`. `Person` bleibt der Buchende.
- **Gast-Buchungen zählen nicht als eigene.** Sie lösen keinen Hinweis aus und blockieren dich nicht, beim Buchen und beim Verlängern.
- **Anzeige:** Popup „Name“ und darunter „gebucht von …“. Dashboard-Karte, Tab „Buchungen“ und beide Verwalten-Dialoge: „für Name“. **Altbestand ohne Gastnamen sieht genau aus wie heute** (alte Formel zeichengleich im Zweig „GastName leer“, maschinell geprüft).
- **Design (Fassung 2):** Alle neuen Steuerelemente übernehmen ihren Stil aus vorhandenen der App: Knöpfe wie `btnSpeichern`/`btnAbbrechen` (Größe 15, Radius 10, Höhe 40), Eingaben wie `ddStart` (Navy-Rand 2, Höhe 40), Schalter wie die Wochentage (grün, Höhe 28), Hinweis wie `conDetailsPopup` (Weiß, Radius 16, Schatten), Hintergrund wie die Ladeanzeige (Schwarz 40 %), Titel wie `lblTischeBuchenPanel` (17, fett). Gast-Zeile neutral wie die Zeit. Skizzen: `design/`.
- **Umfang:** 179 Properties: 19 bestehende ersetzt, 6 bisher nicht gesetzte Maße an bestehenden Labels (Rückfall: Standardwert, steht beim Block), 154 an **10 neuen Steuerelementen**. Neue Variablen alle mit Präfix `varFb…` (7). Kein neuer Server-Filter, keine neue Delegationswarnung.
- **Nicht angefasst:** Ladezeile (18×), Tischpositionen, Check-in, Stornieren, Freigabe, `App.OnStart`.
- **Handy-App:** unverändert. Bekannte Folge, von dir akzeptiert: Gast-Buchungen blockieren dort den Buchenden zur selben Zeit.
- **Offen:** die Kontaktzeile im Hinweis (Axel Krägelius / Norman Horn). Ändern an einer Stelle: `lblFbHinweis.Text`.
- **Danach:** P3 (Nachtrag 6 v2) baut auf `btnHitArea.OnSelect` aus diesem Paket auf.

## 1. Einfügen (Reihenfolge)
1. **Kopie testen**, Sicherung `.msapp` vom Original. Reihenfolge der Pakete: `EINSETZPLAN.md`.
2. **S1 Spalte anlegen:** In der Liste `Tischbuchungen` neue Spalte **`GastName`**, Typ **Eine Textzeile**, nicht erforderlich. Dann in Studio: Daten → `Tischbuchungen` → … → **Aktualisieren** (nicht neu verbinden).
3. **S2–S4 Steuerelemente anlegen** (Tabelle unten), **exakt** so benennen und alle Properties setzen. Bei klassischen Steuerelementen stehen die Werte rechts unter „Erweitert“.
4. **S5–S8 Formeln ersetzen**, jeweils die **ganze** Property.
5. Nach jedem Schritt die App-Prüfung ansehen. Rote Fehler zwischen S2 und S5 sind normal, solange Steuerelemente fehlen, die eine Formel nennt. Nach S8 darf keiner mehr da sein.

**Neue Steuerelemente:**

| Name | Typ | liegt in | Schritt |
|---|---|---|---|
| `tglFuerAndere` | Umschalter (klassisch, „Umschalten“) | `conBuchungDialog` | S3 |
| `txtGastName` | Texteingabe (klassisch) | `conBuchungDialog` | S3 |
| `tglFuerAnderePanel` | Umschalter (klassisch, „Umschalten“) | `conTischBuchungenPanel` | S4 |
| `txtGastNamePanel` | Texteingabe (klassisch) | `conTischBuchungenPanel` | S4 |
| `btnFbHintergrund` | Schaltfläche (klassisch) | `Screen1` | S2 |
| `conFbHinweis` | Container (Layout → Container, nicht horizontal/vertikal) | `Screen1` | S2 |
| `lblFbTitel` | Textbeschriftung | `conFbHinweis` | S2 |
| `lblFbHinweis` | Textbeschriftung | `conFbHinweis` | S2 |
| `btnFbAbbrechen` | Schaltfläche (klassisch) | `conFbHinweis` | S2 |
| `btnFbTrotzdem` | Schaltfläche (klassisch) | `conFbHinweis` | S2 |

**Ebenen (wichtig):**
- `btnFbHintergrund` und `conFbHinweis` liegen direkt in `Screen1` über allen Dialogen.
- Nach dem Anlegen `btnFbHintergrund` markieren → **Ganz nach vorne bringen**. Danach `conFbHinweis` → **Ganz nach vorne bringen**. Danach **`conLadeOverlay` → Ganz nach vorne bringen**, damit die Ladeanzeige weiter alles überdeckt.
- Strukturansicht danach von oben: `conLadeOverlay`, `conFbHinweis`, `btnFbHintergrund`, … Alle anderen bleiben, wo sie sind.
- In Studio verdecken die neuen Flächen nichts, weil `varFbZeige` leer ist. Zum Ansehen kurz `Visible` auf `true` setzen und danach die Formel aus dem Block zurück einsetzen.

## 2. Schritte

### S2 Hinweisdialog anlegen (direkt in Screen1)

**Was:** Ein Hinweis (580 × 280, mittig) mit Titel und Vollbild-Hintergrund. Der Hintergrund fängt alle Klicks ab, solange der Hinweis offen ist. Daneben ist nichts bedienbar, also kann sich auch keine Variable ändern.
- **„Abbrechen“** schließt den Hinweis, nichts wird gespeichert. Dialog oder Panel bleibt offen.
- **„Trotzdem buchen“ / „Trotzdem verlängern“** führt den Knopf, der gefragt hat, noch einmal aus, diesmal mit Bestätigung (`varFbTrotzdem`). Die Speicherlogik steht nur einmal da.
- Der Knopf blendet den Hinweis nicht selbst aus. Das macht der Speichern- bzw. Verlängern-Knopf als erste Anweisung. So trifft ein Doppelklick nie den Dialog darunter, und während des Speicherns deckt die Ladeanzeige alles ab.
- Textbreiten und Höhen sind je Zeichenart geschätzt und an den gelieferten Werten geprüft (Anhang B).

**Rückfall:** `btnFbHintergrund` und `conFbHinweis` (samt Inhalt) löschen. Vorher S5 und S6 zurücknehmen, weil sie den Hinweis öffnen.

#### `btnFbHintergrund` (neu, Schaltfläche (klassisch), in `Screen1`)

| Property | Wert |
|---|---|
| `X` | `0` |
| `Y` | `0` |
| `Width` | `Parent.Width` |
| `Height` | `Parent.Height` |
| `Text` | `""` |
| `Fill` | `RGBA(0; 0; 0; 0,4)` |
| `HoverFill` | `RGBA(0; 0; 0; 0,4)` |
| `PressedFill` | `RGBA(0; 0; 0; 0,4)` |
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
| `Width` | `580` |
| `Height` | `280` |
| `X` | `(Parent.Width - Self.Width) / 2` |
| `Y` | `(Parent.Height - Self.Height) / 2` |
| `Visible` | `varFbZeige` |
| `Fill` | `Color.White` |
| `RadiusTopLeft` | `16` |
| `RadiusTopRight` | `16` |
| `RadiusBottomLeft` | `16` |
| `RadiusBottomRight` | `16` |
| `DropShadow` | `DropShadow.Light` |

#### `lblFbTitel` (neu, Textbeschriftung, in `conFbHinweis`)

| Property | Wert |
|---|---|
| `X` | `20` |
| `Y` | `20` |
| `Width` | `Parent.Width - 40` |
| `Height` | `40` |
| `Text` | `"Zur selben Zeit schon gebucht"` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `17` |
| `FontWeight` | `FontWeight.Bold` |
| `Color` | `RGBA(0; 0; 0; 1)` |

#### `lblFbHinweis` (neu, Textbeschriftung, in `conFbHinweis`)

| Property | Wert |
|---|---|
| `X` | `20` |
| `Y` | `70` |
| `Width` | `Parent.Width - 40` |
| `Height` | `Parent.Height - 150` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Color` | `RGBA(0; 0; 0; 1)` |
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
| `Text` | `"Abbrechen"` |
| `AccessibleLabel` | `"Abbrechen, nichts buchen"` |
| `Fill` | `Color.Black` |
| `Color` | `RGBA(255; 255; 255; 1)` |
| `BorderColor` | `ColorFade(Self.Fill; -15%)` |
| `BorderThickness` | `2` |
| `DisabledBorderColor` | `RGBA(166; 166; 166; 1)` |
| `Font` | `Font.'Open Sans'` |
| `FontWeight` | `FontWeight.Semibold` |
| `HoverBorderColor` | `ColorFade(Self.BorderColor; 20%)` |
| `HoverColor` | `RGBA(255; 255; 255; 1)` |
| `HoverFill` | `ColorFade(Self.Fill; 30%)` |
| `PressedBorderColor` | `Self.Fill` |
| `PressedColor` | `Color.White` |
| `PressedFill` | `ColorFade(Color.Black; 30%)` |
| `RadiusTopLeft` | `10` |
| `RadiusTopRight` | `10` |
| `RadiusBottomLeft` | `10` |
| `RadiusBottomRight` | `10` |
| `Size` | `15` |
| `Height` | `40` |

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
| `DisplayMode` | `If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)` |
| `AccessibleLabel` | `Self.Text` |
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
| `Size` | `15` |
| `Height` | `40` |

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

**Was:** Im Buchungsdialog (aus dem Grundriss), in der mittleren Spalte unter dem Tischnamen: Umschalter `tglFuerAndere` (X 270, Y 128) und darunter das Namensfeld `txtGastName` (Y 186).
- Der Platz ist frei: Bild bis X 245, Eingaben ab X 448, Wochentage erst ab Y 290 (belegt, Export).
- Das Namensfeld erscheint nur bei „Für andere“.

**Rückfall:** beide löschen (erst S5 und S7 zurücknehmen).

#### `tglFuerAndere` (neu, Umschalter (klassisch, „Umschalten“), in `conBuchungDialog`)

| Property | Wert |
|---|---|
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `TrueFill` | `ColorValue("#00A96B")` |
| `Color` | `RGBA(0; 0; 0; 1)` |
| `X` | `270` |
| `Y` | `122 + 6` |
| `Width` | `165` |
| `Height` | `28` |
| `Default` | `false` |
| `FalseText` | `"Für mich"` |
| `TrueText` | `"Für andere"` |
| `AccessibleLabel` | `"Für jemand anderen buchen"` |

#### `txtGastName` (neu, Texteingabe (klassisch), in `conBuchungDialog`)

| Property | Wert |
|---|---|
| `Fill` | `RGBA(255; 255; 255; 1)` |
| `Color` | `RGBA(0; 0; 0; 1)` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `BorderThickness` | `2` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Height` | `40` |
| `X` | `270` |
| `Y` | `186` |
| `Width` | `165` |
| `Default` | `""` |
| `HintText` | `"Name (Pflicht)"` |
| `MaxLength` | `100` |
| `Visible` | `tglFuerAndere.Value` |
| `AccessibleLabel` | `"Name der Person, für die gebucht wird"` |

### S4 Panel: Schalter und Namensfeld, Speichern rückt nach unten

**Was:** Im Panel „Tisch buchen“ eine Zeile unter den Wochentagen: Umschalter `tglFuerAnderePanel` links, Namensfeld `txtGastNamePanel` rechts daneben (gleiche Zeile, Höhe 40). **`btnSpeichernTischePanel` rückt um eine Zeile nach unten:** bisher `tglTagFr_1.Y + tglTagFr_1.Height + 20`, neu 60 tiefer. Die Formel rechnet weiter von den Wochentagen aus, nicht mit festen Zahlen.

**Rückfall:** `btnSpeichernTischePanel.Y` aus Anhang A, beide Steuerelemente löschen.

#### `tglFuerAnderePanel` (neu, Umschalter (klassisch, „Umschalten“), in `conTischBuchungenPanel`)

| Property | Wert |
|---|---|
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `TrueFill` | `ColorValue("#00A96B")` |
| `Color` | `RGBA(0; 0; 0; 1)` |
| `X` | `ddTischePanel.X` |
| `Y` | `(tglTagFr_1.Y + tglTagFr_1.Height + 20) + 6` |
| `Width` | `165` |
| `Height` | `28` |
| `Default` | `false` |
| `FalseText` | `"Für mich"` |
| `TrueText` | `"Für andere"` |
| `AccessibleLabel` | `"Für jemand anderen buchen"` |

#### `txtGastNamePanel` (neu, Texteingabe (klassisch), in `conTischBuchungenPanel`)

| Property | Wert |
|---|---|
| `Fill` | `RGBA(255; 255; 255; 1)` |
| `Color` | `RGBA(0; 0; 0; 1)` |
| `BorderColor` | `RGBA(32; 54; 71; 1)` |
| `BorderThickness` | `2` |
| `Font` | `Font.'Open Sans'` |
| `Size` | `13` |
| `Height` | `40` |
| `X` | `ddTischePanel.X + 175` |
| `Y` | `tglTagFr_1.Y + tglTagFr_1.Height + 20` |
| `Width` | `ddTischePanel.Width - 175` |
| `Default` | `""` |
| `HintText` | `"Name (Pflicht)"` |
| `MaxLength` | `100` |
| `Visible` | `tglFuerAnderePanel.Value` |
| `AccessibleLabel` | `"Name der Person, für die gebucht wird"` |

#### `btnSpeichernTischePanel.Y`

Ort: `Screen1 > conTischBuchungenPanel > btnSpeichernTischePanel` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-tglTagFr_1.Y + tglTagFr_1.Height + 20
+(tglTagFr_1.Y + tglTagFr_1.Height + 20) + 40 + 20
```

Vollständiger Block:

```
(tglTagFr_1.Y + tglTagFr_1.Height + 20) + 40 + 20
```

### S5 Speichern: Gast, weicher Hinweis, GastName

**Was, in beiden Speichern-Knöpfen gleich** (maschinell verglichen):
1. Als Erstes wird eine Bestätigung aus dem Hinweis verbraucht (`varFbBestaetigt`), `varFbTrotzdem` zurückgesetzt und der Hinweis ausgeblendet. Umschalter und Name werden gelesen.
2. „Für andere“ ohne Namen → Meldung, nichts gespeichert.
3. Eigene Buchungen zur selben Zeit (`colNeuIch`): Gast-Buchungen und verfallene zählen nicht. Bei einer Buchung **für** andere wird nicht geprüft. Der Server-Filter bleibt gleich, die Gast-Buchungen fallen lokal per `RemoveIf` heraus. `colNeuIch` wird mit genannten Spalten geladen (`ForAll(… As B; {ID; Startzeit; Endzeit; CheckedIn; Erstellt; GastName})`), damit `GastName` und `Erstellt` sicher ankommen.
4. **Statt Sperre:** Überschneidet ein Termin eine eigene Buchung, öffnet sich der Hinweis, und **nichts** wird gespeichert. Mit „Trotzdem buchen“ werden alle freien Termine gespeichert. Termine, an denen der Tisch selbst belegt ist, bleiben wie heute ausgeschlossen.
5. Der Sammel-Patch schreibt `GastName` mit. Bei eigenen Buchungen bleibt die Spalte leer.
6. Die Erfolgsmeldung nennt den Gast: „Gebucht: UG Desk 5 für Max Muster, …“.
7. Sperre, `IfError`, Nachlese, Ladezeile und Meldungen sind sonst unverändert (maschinell geprüft).

**Rückfall:** beide Properties aus Anhang A.

#### `btnSpeichern.OnSelect`

Ort: `Screen1 > conBuchungDialog > btnSpeichern` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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
3. Statt der Sperre „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ kommt der Hinweis mit „Trotzdem verlängern“. Er kommt erst **nach** der Prüfung „Tisch inzwischen belegt“, damit niemand etwas bestätigt, das danach doch scheitert.
4. Ist der Hinweis offen, bleibt die gewählte Dauer stehen. Sonst wäre der Knopf beim „Trotzdem“ gesperrt (Befund B1).
- Verkürzen, 22:00, „Tisch inzwischen belegt“ und verfallene Buchung bleiben wie heute.

**Rückfall:** beide Properties aus Anhang A.

#### `btnVerlängern.OnSelect`

Ort: `Screen1 > conVerwaltenDialog > btnVerlängern` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

**Was:** Beim Öffnen des Buchungsdialogs (Kachel) und des Panels („Tisch Buchen“) werden Umschalter und Name zurückgesetzt, eine liegen gebliebene Bestätigung wird gelöscht.
- Heute sind das die einzigen beiden Öffner (belegt). Der dritte Öffner aus P3 („Neu buchen“) übernimmt dieselben Rücksetzungen (maschinell geprüft in `abstimmung.py`).

**Rückfall:** beide Properties aus Anhang A.

#### `btnHitArea.OnSelect`

Ort: `Screen1 > conGrundriss > Gallery1 > btnHitArea` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

**Was:** Gastname in der Anzeige. Jede Formel hat die Form `If(IsBlank(….GastName); <alte Formel>; <neu>)`. Altbestand sieht exakt aus wie heute.
Was sich nur bei Gast-Buchungen ändert:
- **Popup:** `lblPerson` ist breiter (bis vor das Bild), Größe 11, Höhe 46, zweizeilig. Die Zeitzeile `lblZeit2` rückt nach unten (Y 118).
- **Dashboard-Karte und Tab „Buchungen“:** Die Zeitzeile bekommt eine zweite Zeile „für Name“ und wird doppelt so hoch. Auf der Karte rückt der Tischname dafür von Y 27 auf 21, damit unten 8 Rand bleiben (gerechnet: Unterkante 85 von 86).
- **Verwalten (Dashboard):** Zeit plus zweite Zeile „für Name“ in Größe 10, breiter bis vor „+1Std“.
- **Verwalten (Tab):** Titel „Tisch X · für Name“ in Größe 15 statt „Verwalten: Tisch X“ in 18, breiter.
- **Lange Namen** ab etwa 15 Zeichen können im Popup und im Verwalten (Dashboard) abgeschnitten sein. Die Liste zeigt sie ganz.

**Rückfall:** alle Properties aus Anhang A. Die 6 bisher nicht gesetzten auf den Standardwert beim Block.

#### `lblPerson.Width`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (bisher nicht gesetzt, Standard `150`, Rückfall: `150`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 150; Image7.X - Self.X - 6)
```

#### `lblPerson.Size`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (bisher nicht gesetzt, Standard `13`, Rückfall: `13`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 13; 11)
```

#### `lblPerson.Height`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **neu setzen** (bisher nicht gesetzt, Standard `40`, Rückfall: `40`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 40; 46)
```

#### `lblZeit3.Size`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (bisher nicht gesetzt, Standard `13`, Rückfall: `13`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 13; 10)
```

#### `lblZeit3.Width`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (bisher nicht gesetzt, Standard `150`, Rückfall: `150`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 150; btnPlus1Std.X - Self.X - 1)
```

#### `lblZeit3.Height`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **neu setzen** (bisher nicht gesetzt, Standard `40`, Rückfall: `40`)

Vollständiger Block:

```
If(IsBlank(varSelectedBuchung.GastName); 40; 50)
```

#### `lblPerson.Text`

Ort: `Screen1 > conDetailsPopup > lblPerson` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Self.Size * 1,8
+If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

Vollständiger Block:

```
If(IsBlank(ThisItem.GastName); Self.Size * 1,8; Self.Size * 3,6)
```

#### `lblTischHeute.Y`

Ort: `Screen1 > conDashboard > galTischbuchungenHeute > lblTischHeute` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-27
+If(IsBlank(ThisItem.GastName); 27; 21)
```

Vollständiger Block:

```
If(IsBlank(ThisItem.GastName); 27; 21)
```

#### `lblTischName.Y`

Ort: `Screen1 > conBuchungen > galAlleTischbuchungen > lblTischName` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-27
+If(IsBlank(ThisItem.GastName); 27; 21)
```

Vollständiger Block:

```
If(IsBlank(ThisItem.GastName); 27; 21)
```

#### `lblZeit3.Text`

Ort: `Screen1 > conVerwaltenDialog > lblZeit3` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

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

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-400
+If(IsBlank(varSelectedBuchungTab.GastName); 400; Parent.Width - 24)
```

Vollständiger Block:

```
If(IsBlank(varSelectedBuchungTab.GastName); 400; Parent.Width - 24)
```

## 3. Tests
Der Testbogen für alle Pakete zusammen steht im **`EINSETZPLAN.md`, Teil B** (Für andere, Hinweis, Anzeige, alles für **morgen**) und Teil A (Verlängern-Hinweis auf der Zeitachse). Er ersetzt den Testbogen der Fassung 1.

## 4. Rückfall gesamt
- **Einzelschritte:** siehe jeweiligen Schritt, Originale in Anhang A. Reihenfolge rückwärts: S8 → S7 → S6 → S5 → S4 → S3 → S2.
- **Ist P3 schon eingefügt:** erst P3 zurücknehmen (es baut auf `btnHitArea.OnSelect` aus S7 auf).
- **Alles:** frühere Version wiederherstellen (make.powerapps.com → App → Details → Versionen) oder die Sicherung `.msapp`.
- **Die Spalte `GastName` kann bleiben.** Alte Formeln lesen sie nicht (geschlussfolgert).

## 5. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| U1 | `Select(btnSpeichern)` usw. aus dem Hinweis führt den Knopf im Container aus | Einsetzplan Teil B Test B4, B9, B10, Teil A Test 15. Passiert bei „Trotzdem“ nichts: mir melden. Notweg: „Abbrechen“ geht immer |
| U2 | `GastName` in `varSelectedBuchung`/`varVerlBuchung` (aus `LookUp`): Studio lädt nur benutzte Spalten. In den Sammlungen per `ForAll` abgesichert. Alle Setzer liefern Datensätze aus `Tischbuchungen` (maschinell geprüft) | Einsetzplan Teil B Test B6 und B11 |
| U3 | Der klassische Umschalter zeigt „Für mich“/„Für andere“ neben dem Schalter in Breite 165 (Text ca. 97 px geschätzt) | Sichtprüfung. Sonst `Width` auf 180 |
| U4 | Panel bei Fensterhöhe unter etwa 720: „Speichern“ kann unten abgeschnitten sein | Fenster verkleinern |
| U5 | Kontaktzeile im Hinweis (Axel Krägelius / Norman Horn) ist nicht bestätigt | `lblFbHinweis.Text` anpassen |
| U6 | Textbreiten sind geschätzt (Open Sans je Zeichenart) | Einsetzplan Teil B Test B6 (langer Name) |
| U7 | Stil aus der App übernommen, aber nur aus den Maßen skizziert (kein Studio-Bild) | Sichtprüfung gegen `design/*.png` |

## 6. Unabhängige Prüfung (Fassung 1, gilt für die Logik)
Fassung 1 wurde am 26.10. unabhängig geprüft (Bericht: `arbeit/2026-10-26_FuerAndere/pruefung_fuer_andere.md`). Was daraus wurde:

| Nr | Befund | Umsetzung |
|---|---|---|
| B1 | „Trotzdem verlängern“ fand die Dauer gelöscht | behoben, Prüfung im Generator |
| B2 | Mehrzeilige Texte in festen Höhen abgeschnitten | behoben: Größe und Höhe nur bei Gast angepasst, Höhen gerechnet |
| B3 | Überlappungen, zu lange Texte, falsche Schätzung | behoben: Name in zweiter Zeile, Schätzung je Zeichenart in Pixeln, Prüfungen an den gelieferten Werten |
| B4 | `GastName` in Sammlungen evtl. nicht geladen | behoben (Projektion), in der Abstimmung je Füllstelle geprüft |
| B5 | Hinweis vor „Tisch belegt“ beim Verlängern | behoben |
| B6 | `lblPerson.Width` ist bestehend (Standard 150) | als „bisher Standard“ mit Rückfallwert |
| B7 | Ebenen | Abschnitt 1 |
| B8 | Nachtrag 6 ändert auch `btnHitArea.OnSelect` | erledigt: P3 baut auf diesem Paket auf |
| B9 | Check-in-Dialog ohne Gastnamen | offen, kein Muss |
| B10 | Handy: „Trotzdem“-Doppelbuchungen sperren dort das Verlängern | Handy-Anpassung später |
| B11 | Testliste unvollständig | im gemeinsamen Testbogen ergänzt |
| B12 | Kontaktzeile unbestätigt | U5 |

**Fassung 2 ist nicht unabhängig geprüft.** Geändert sind nur Stil-Werte, die Titelzeile, die Hinweisbreite und die Kartenposition. Die Formeln in S5–S7 sind gegenüber Fassung 1 bis auf `btnTischHinzufügen.OnSelect` (gleiche Rücksetzungen) unverändert in der Logik.

## Anhang A: Originale aus dem Export 10.11. 08:13 (Rückfall)

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

**`lblTischHeute.Y`**

```
27
```

**`lblTischName.Y`**

```
27
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

Paket allein:

```
Für andere buchen: 179 Properties: 19 bestehende ersetzt, 6 an bestehenden Steuerelementen neu gesetzt (bisher Standard), 154 an 10 neuen Steuerelementen. Grundlage: Export 10.11. 08:13 (echt, zeichengleich mit 25.10.).
Bisher Standard: lblPerson.Height (40), lblPerson.Size (13), lblPerson.Width (150), lblZeit3.Height (40), lblZeit3.Size (13), lblZeit3.Width (150)
Geänderte bestehende Properties: btnHitArea.OnSelect, btnSpeichern.OnSelect, btnSpeichernTischePanel.OnSelect, btnSpeichernTischePanel.Y, btnTischHinzufügen.OnSelect, btnVerlängern.OnSelect, btnVerlängern_1.OnSelect, lblPerson.Text, lblRaumZeit.Height, lblRaumZeit.Text, lblTischHeute.Y, lblTischName.Y, lblTitel3_1.Size, lblTitel3_1.Text, lblTitel3_1.Width, lblZeit2.Y, lblZeit3.Text, lblZeitHeute.Height, lblZeitHeute.Text
neue Variablen: varFbBestaetigt, varFbFuerAndere, varFbGast, varFbQuelle, varFbText, varFbTrotzdem, varFbZeige
Textbreite tglFuerAndere Text: „Für andere“ ca. 97 von 110
Textbreite btnFbTrotzdem: „Trotzdem verlängern“ ca. 216 von 240
Textbreite btnFbAbbrechen: „Abbrechen“ ca. 107 von 240
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
Lage Karte lblZeitHeute 2 Zeilen (Gast, Titel bei Y 21, Kartenunterkante 94, 8 Rand): 85 ≤ 86
Höhe lblFbHinweis: längster Text 5 Zeilen ca. 114 von 180
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
