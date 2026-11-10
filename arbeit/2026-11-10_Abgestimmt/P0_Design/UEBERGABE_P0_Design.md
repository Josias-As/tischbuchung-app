# P0 Design-Korrektur (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (Einsetzplan: `EINSETZPLAN.md` im selben Ordner). Grundlage: **Export 10.11. 08:13** („echt“, zeichengleich mit 25.10.). Erzeugt und geprüft mit `werkzeuge/design_korrektur.py` (0 Fehler) und `werkzeuge/abstimmung.py`. Nicht unabhängig geprüft. In Studio nichts getestet. Kennzeichnung: **belegt**, **gerechnet**, **UNSICHER**.

## Kurzfassung
- **7 Properties, kein neues Steuerelement, keine Formel mit Daten.** Unabhängig von allen anderen Paketen, jederzeit einfügbar.
- **D1 `btnHeuteDatum`, gedrückt:** Die Schrift war beim Drücken Blau mit 16 % Deckkraft auf blauem Grund, also unsichtbar (belegt). Neu: Weiß, wie bei allen Hauptknöpfen der App.
- **D2 „Tisch Buchen“ (`btnTischHinzufügen`):** weiße Schrift auf Hellgrau `#D0D0D0`, Kontrast 1,5 : 1 (gerechnet). Neu im Stil des Hauptknopfs `btnSpeichern`: Markenblau `#171496`, Größe 15, Breite 160, Hover und Gedrückt wie dort. Kontrast 13,3 : 1. Der Text braucht etwa 158 px (geschätzt je Zeichenart).
- Keine andere Formel liest die Breite des Knopfs (maschinell geprüft). Die Position bleibt.

## 1. Schritt

### P0 Design-Korrektur

Jeder Wert ist aus `btnSpeichern` übernommen (Fill, HoverFill, PressedFill, PressedColor, Size). Nur die Breite ist gerechnet.

**Test:** Dashboard ansehen: „Tisch Buchen“ ist blau mit weißer Schrift und nicht abgeschnitten. Darüberfahren wird dunkler, beim Drücken bleibt die Schrift lesbar. Datum auf morgen stellen, „Heute“ gedrückt halten: Schrift lesbar.

#### `btnHeuteDatum.PressedColor`

Ort: `Screen1 > conDashboard > btnHeuteDatum` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-RGBA(23; 20; 150; 0,16)
+RGBA(255; 255; 255; 1)
```

Vollständiger Block:

```
RGBA(255; 255; 255; 1)
```

#### `btnTischHinzufügen.Fill`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-ColorValue("#D0D0D0")
+ColorValue("#171496")
```

Vollständiger Block:

```
ColorValue("#171496")
```

#### `btnTischHinzufügen.HoverFill`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-RGBA(0; 0; 0; 0,2)
+ColorFade(Self.Fill; -20%)
```

Vollständiger Block:

```
ColorFade(Self.Fill; -20%)
```

#### `btnTischHinzufügen.PressedFill`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-
+ColorFade(Self.Fill; -20%)
```

Vollständiger Block:

```
ColorFade(Self.Fill; -20%)
```

#### `btnTischHinzufügen.PressedColor`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-Self.Fill
+Color.White
```

Vollständiger Block:

```
Color.White
```

#### `btnTischHinzufügen.Size`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-11
+15
```

Vollständiger Block:

```
15
```

#### `btnTischHinzufügen.Width`

Ort: `Screen1 > conDashboard > btnTischHinzufügen` · **ganze Property ersetzen**

Änderung gegenüber Export 10.11. 08:13 (`-` alt, `+` neu):

```diff
@@ -1 +1 @@
-80
+160
```

Vollständiger Block:

```
160
```

## Rückfall
Alle 7 Properties aus Anhang A. Sie hängen nicht voneinander ab, jede kann einzeln zurück.

## Anhang A: Originale aus dem Export 10.11. 08:13 (Rückfall)

**`btnHeuteDatum.PressedColor`**

```
RGBA(23; 20; 150; 0,16)
```

**`btnTischHinzufügen.Fill`**

```
ColorValue("#D0D0D0")
```

**`btnTischHinzufügen.HoverFill`**

```
RGBA(0; 0; 0; 0,2)
```

**`btnTischHinzufügen.PressedFill`**

```

```

**`btnTischHinzufügen.PressedColor`**

```
Self.Fill
```

**`btnTischHinzufügen.Size`**

```
11
```

**`btnTischHinzufügen.Width`**

```
80
```

## Anhang B: Maschinelle Prüfung

Paket allein:

```
P0 Design-Korrektur: 7 Properties, kein neues Steuerelement. Grundlage: Export 10.11. 08:13 (echt).
„Tisch Buchen“: Text ca. 158 px in Breite 160; Kontrast weiße Schrift alt 1.5:1, neu 13.3:1.
Breite von btnTischHinzufügen liest keine andere Formel (nur Y/Height, unverändert).
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
