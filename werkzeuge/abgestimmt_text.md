@@ P0.kopf
# P0 Design-Korrektur (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (Einsetzplan: `EINSETZPLAN.md` im selben Ordner). Grundlage: **Export 10.11. 08:13** („echt“, zeichengleich mit 25.10.). Erzeugt und geprüft mit `werkzeuge/design_korrektur.py` (0 Fehler) und `werkzeuge/abstimmung.py`. Nicht unabhängig geprüft. In Studio nichts getestet. Kennzeichnung: **belegt**, **gerechnet**, **UNSICHER**.

@@ P0.kurzfassung
## Kurzfassung
- **7 Properties, kein neues Steuerelement, keine Formel mit Daten.** Unabhängig von allen anderen Paketen, jederzeit einfügbar.
- **D1 `btnHeuteDatum`, gedrückt:** Die Schrift war beim Drücken Blau mit 16 % Deckkraft auf blauem Grund, also unsichtbar (belegt). Neu: Weiß, wie bei allen Hauptknöpfen der App.
- **D2 „Tisch Buchen“ (`btnTischHinzufügen`):** weiße Schrift auf Hellgrau `#D0D0D0`, Kontrast 1,5 : 1 (gerechnet). Neu im Stil des Hauptknopfs `btnSpeichern`: Markenblau `#171496`, Größe 15, Breite 160, Hover und Gedrückt wie dort. Kontrast 13,3 : 1. Der Text braucht etwa 158 px (geschätzt je Zeichenart).
- Keine andere Formel liest die Breite des Knopfs (maschinell geprüft). Die Position bleibt.

@@ P0.P0
Jeder Wert ist aus `btnSpeichern` übernommen (Fill, HoverFill, PressedFill, PressedColor, Size). Nur die Breite ist gerechnet.

**Test:** Dashboard ansehen: „Tisch Buchen“ ist blau mit weißer Schrift und nicht abgeschnitten. Darüberfahren wird dunkler, beim Drücken bleibt die Schrift lesbar. Datum auf morgen stellen, „Heute“ gedrückt halten: Schrift lesbar.

@@ P0.rueckfall
## Rückfall
Alle 7 Properties aus Anhang A. Sie hängen nicht voneinander ab, jede kann einzeln zurück.

@@ P1.kopf
# P1 Für andere buchen + weicher Hinweis, Fassung 2 (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`). Grundlage: **Export 10.11. 08:13** („echt“, zeichengleich mit 25.10.). Erzeugt und geprüft mit `werkzeuge/fuer_andere_v2.py` (0 Fehler) und `werkzeuge/abstimmung.py` (alle Pakete zusammen, 0 Fehler). Ersetzt Fassung 1 (`arbeit/2026-10-26_FuerAndere/`, bleibt erhalten). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

**Prüfstatus:** Die Logik (Speichern, Verlängern, Hinweis, Anzeige) ist dieselbe wie in Fassung 1, die **unabhängig geprüft** wurde (12 Befunde, B1–B5 behoben, Abschnitt 6). **Neu in Fassung 2 und nur maschinell geprüft:** Stil der neuen Steuerelemente aus der App, Titelzeile im Hinweis, Hinweis 580 breit, Kartenposition bei Gästen.

@@ P1.kurzfassung
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

@@ P1.ablauf
## 1. Einfügen (Reihenfolge)
1. **Kopie testen**, Sicherung `.msapp` vom Original. Reihenfolge der Pakete: `EINSETZPLAN.md`.
2. **S1 Spalte anlegen:** In der Liste `Tischbuchungen` neue Spalte **`GastName`**, Typ **Eine Textzeile**, nicht erforderlich. Dann in Studio: Daten → `Tischbuchungen` → … → **Aktualisieren** (nicht neu verbinden).
3. **S2–S4 Steuerelemente anlegen** (Tabelle unten), **exakt** so benennen und alle Properties setzen. Bei klassischen Steuerelementen stehen die Werte rechts unter „Erweitert“.
4. **S5–S8 Formeln ersetzen**, jeweils die **ganze** Property.
5. Nach jedem Schritt die App-Prüfung ansehen. Rote Fehler zwischen S2 und S5 sind normal, solange Steuerelemente fehlen, die eine Formel nennt. Nach S8 darf keiner mehr da sein.

**Neue Steuerelemente:**

| Name | Typ | liegt in | Schritt |
|---|---|---|---|
NEUE_TABELLE

**Ebenen (wichtig):**
- `btnFbHintergrund` und `conFbHinweis` liegen direkt in `Screen1` über allen Dialogen.
- Nach dem Anlegen `btnFbHintergrund` markieren → **Ganz nach vorne bringen**. Danach `conFbHinweis` → **Ganz nach vorne bringen**. Danach **`conLadeOverlay` → Ganz nach vorne bringen**, damit die Ladeanzeige weiter alles überdeckt.
- Strukturansicht danach von oben: `conLadeOverlay`, `conFbHinweis`, `btnFbHintergrund`, … Alle anderen bleiben, wo sie sind.
- In Studio verdecken die neuen Flächen nichts, weil `varFbZeige` leer ist. Zum Ansehen kurz `Visible` auf `true` setzen und danach die Formel aus dem Block zurück einsetzen.

@@ P1.S2
**Was:** Ein Hinweis (580 × 280, mittig) mit Titel und Vollbild-Hintergrund. Der Hintergrund fängt alle Klicks ab, solange der Hinweis offen ist. Daneben ist nichts bedienbar, also kann sich auch keine Variable ändern.
- **„Abbrechen“** schließt den Hinweis, nichts wird gespeichert. Dialog oder Panel bleibt offen.
- **„Trotzdem buchen“ / „Trotzdem verlängern“** führt den Knopf, der gefragt hat, noch einmal aus, diesmal mit Bestätigung (`varFbTrotzdem`). Die Speicherlogik steht nur einmal da.
- Der Knopf blendet den Hinweis nicht selbst aus. Das macht der Speichern- bzw. Verlängern-Knopf als erste Anweisung. So trifft ein Doppelklick nie den Dialog darunter, und während des Speicherns deckt die Ladeanzeige alles ab.
- Textbreiten und Höhen sind je Zeichenart geschätzt und an den gelieferten Werten geprüft (Anhang B).

**Rückfall:** `btnFbHintergrund` und `conFbHinweis` (samt Inhalt) löschen. Vorher S5 und S6 zurücknehmen, weil sie den Hinweis öffnen.

@@ P1.S3
**Was:** Im Buchungsdialog (aus dem Grundriss), in der mittleren Spalte unter dem Tischnamen: Umschalter `tglFuerAndere` (X 270, Y 128) und darunter das Namensfeld `txtGastName` (Y 186).
- Der Platz ist frei: Bild bis X 245, Eingaben ab X 448, Wochentage erst ab Y 290 (belegt, Export).
- Das Namensfeld erscheint nur bei „Für andere“.

**Rückfall:** beide löschen (erst S5 und S7 zurücknehmen).

@@ P1.S4
**Was:** Im Panel „Tisch buchen“ eine Zeile unter den Wochentagen: Umschalter `tglFuerAnderePanel` links, Namensfeld `txtGastNamePanel` rechts daneben (gleiche Zeile, Höhe 40). **`btnSpeichernTischePanel` rückt um eine Zeile nach unten:** bisher `tglTagFr_1.Y + tglTagFr_1.Height + 20`, neu 60 tiefer. Die Formel rechnet weiter von den Wochentagen aus, nicht mit festen Zahlen.

**Rückfall:** `btnSpeichernTischePanel.Y` aus Anhang A, beide Steuerelemente löschen.

@@ P1.S5
**Was, in beiden Speichern-Knöpfen gleich** (maschinell verglichen):
1. Als Erstes wird eine Bestätigung aus dem Hinweis verbraucht (`varFbBestaetigt`), `varFbTrotzdem` zurückgesetzt und der Hinweis ausgeblendet. Umschalter und Name werden gelesen.
2. „Für andere“ ohne Namen → Meldung, nichts gespeichert.
3. Eigene Buchungen zur selben Zeit (`colNeuIch`): Gast-Buchungen und verfallene zählen nicht. Bei einer Buchung **für** andere wird nicht geprüft. Der Server-Filter bleibt gleich, die Gast-Buchungen fallen lokal per `RemoveIf` heraus. `colNeuIch` wird mit genannten Spalten geladen (`ForAll(… As B; {ID; Startzeit; Endzeit; CheckedIn; Erstellt; GastName})`), damit `GastName` und `Erstellt` sicher ankommen.
4. **Statt Sperre:** Überschneidet ein Termin eine eigene Buchung, öffnet sich der Hinweis, und **nichts** wird gespeichert. Mit „Trotzdem buchen“ werden alle freien Termine gespeichert. Termine, an denen der Tisch selbst belegt ist, bleiben wie heute ausgeschlossen.
5. Der Sammel-Patch schreibt `GastName` mit. Bei eigenen Buchungen bleibt die Spalte leer.
6. Die Erfolgsmeldung nennt den Gast: „Gebucht: UG Desk 5 für Max Muster, …“.
7. Sperre, `IfError`, Nachlese, Ladezeile und Meldungen sind sonst unverändert (maschinell geprüft).

**Rückfall:** beide Properties aus Anhang A.

@@ P1.S6
**Was, in beiden Verlängern-Knöpfen gleich:**
1. Die Bestätigung wird am Anfang verbraucht.
2. Eigene andere Buchungen zur selben Zeit: Gast-Buchungen zählen nicht. Eine Gast-Buchung wird ohne diese Prüfung verlängert. `colVerlIch` wird wie oben mit genannten Spalten geladen.
3. Statt der Sperre „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ kommt der Hinweis mit „Trotzdem verlängern“. Er kommt erst **nach** der Prüfung „Tisch inzwischen belegt“, damit niemand etwas bestätigt, das danach doch scheitert.
4. Ist der Hinweis offen, bleibt die gewählte Dauer stehen. Sonst wäre der Knopf beim „Trotzdem“ gesperrt (Befund B1).
- Verkürzen, 22:00, „Tisch inzwischen belegt“ und verfallene Buchung bleiben wie heute.

**Rückfall:** beide Properties aus Anhang A.

@@ P1.S7
**Was:** Beim Öffnen des Buchungsdialogs (Kachel) und des Panels („Tisch Buchen“) werden Umschalter und Name zurückgesetzt, eine liegen gebliebene Bestätigung wird gelöscht.
- Heute sind das die einzigen beiden Öffner (belegt). Der dritte Öffner aus P3 („Neu buchen“) übernimmt dieselben Rücksetzungen (maschinell geprüft in `abstimmung.py`).

**Rückfall:** beide Properties aus Anhang A.

@@ P1.S8
**Was:** Gastname in der Anzeige. Jede Formel hat die Form `If(IsBlank(….GastName); <alte Formel>; <neu>)`. Altbestand sieht exakt aus wie heute.
Was sich nur bei Gast-Buchungen ändert:
- **Popup:** `lblPerson` ist breiter (bis vor das Bild), Größe 11, Höhe 46, zweizeilig. Die Zeitzeile `lblZeit2` rückt nach unten (Y 118).
- **Dashboard-Karte und Tab „Buchungen“:** Die Zeitzeile bekommt eine zweite Zeile „für Name“ und wird doppelt so hoch. Auf der Karte rückt der Tischname dafür von Y 27 auf 21, damit unten 8 Rand bleiben (gerechnet: Unterkante 85 von 86).
- **Verwalten (Dashboard):** Zeit plus zweite Zeile „für Name“ in Größe 10, breiter bis vor „+1Std“.
- **Verwalten (Tab):** Titel „Tisch X · für Name“ in Größe 15 statt „Verwalten: Tisch X“ in 18, breiter.
- **Lange Namen** ab etwa 15 Zeichen können im Popup und im Verwalten (Dashboard) abgeschnitten sein. Die Liste zeigt sie ganz.

**Rückfall:** alle Properties aus Anhang A. Die 6 bisher nicht gesetzten auf den Standardwert beim Block.

@@ P1.tests
## 3. Tests
Der Testbogen für alle Pakete zusammen steht im **`EINSETZPLAN.md`, Teil B** (Für andere, Hinweis, Anzeige, alles für **morgen**) und Teil A (Verlängern-Hinweis auf der Zeitachse). Er ersetzt den Testbogen der Fassung 1.

@@ P1.rueckfall
## 4. Rückfall gesamt
- **Einzelschritte:** siehe jeweiligen Schritt, Originale in Anhang A. Reihenfolge rückwärts: S8 → S7 → S6 → S5 → S4 → S3 → S2.
- **Ist P3 schon eingefügt:** erst P3 zurücknehmen (es baut auf `btnHitArea.OnSelect` aus S7 auf).
- **Alles:** frühere Version wiederherstellen (make.powerapps.com → App → Details → Versionen) oder die Sicherung `.msapp`.
- **Die Spalte `GastName` kann bleiben.** Alte Formeln lesen sie nicht (geschlussfolgert).

@@ P1.unsicher
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

@@ P1.pruefung
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

@@ P3.kopf
# P3 Nachtrag 6, Fassung 2: Verfallene Buchung – kein Check-in-Dialog, dafür „Neu buchen“ (10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`). Grundlage: **Export 10.11. 08:13 + P2 (Nachtrag 5) + P1 (Für andere buchen v2)**. `btnHitArea.OnSelect` rechnet gegen den Stand nach P1, alles andere gegen den Export. Erzeugt und geprüft mit `werkzeuge/nachtrag6_v2.py` (0 Fehler) und `werkzeuge/abstimmung.py`. Ersetzt Fassung 1 (`arbeit/2026-10-12_Nachtrag6/`, bleibt erhalten). **Nicht unabhängig geprüft** (Josias’ Entscheidung, 12.10.). In Studio nichts getestet.

@@ P3.kurzfassung
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

@@ P3.R1
**Regel:** gesperrt, wenn `Endzeit` erreicht ist **oder** die Buchung verfallen ist (nicht eingecheckt, Beginn und Buchungszeitpunkt älter als 30 Min). Zeichengleich mit `lblStatusHeute` nach S3b, rechnet mit dem 15-s-Takt.

**Test:** Einsetzplan Teil A, Test 8.

@@ P3.R2
**Neu anlegen, Name exakt so:**
1. In der Strukturansicht `galTischbuchungenHeute` markieren.
2. Das Stift-Symbol oben links in der **ersten Karte** anklicken (Vorlage gewählt).
3. Einfügen → Schaltfläche (klassisch) → umbenennen in **`btnNeuBuchenHeute`**.
4. Prüfen: `btnNeuBuchenHeute` liegt **in** `galTischbuchungenHeute` und in der Strukturansicht **über** `btnEincheckenHeute` (Neu anordnen → Ganz nach vorne).

**Ablauf beim Tippen:** Tisch frisch prüfen (gibt es ihn noch, ist er gesperrt). Dann Buchungsdialog mit genau den Rücksetzungen der Kachel, Datum heute, Beginn ab der nächsten halben Stunde, Ende = altes Ende. Beginn und Ende kannst du im Dialog ändern.

`lblStatusHeute.Visible` = `!btnNeuBuchenHeute.Visible`. Wo der Knopf steht, ist „Verfallen“ weg. Ist keine Restzeit mehr übrig, steht wieder „Verfallen“.

**Test:** Einsetzplan Teil A, Tests 7 und 9.

@@ P3.R3
`btnHitArea.OnSelect` bekommt nur eine Zeile: `Set(varEndeOverride; "")` vor `Reset(ddEnde)`. Sonst nichts (maschinell geprüft).

**Test:** Einsetzplan Teil A, Test 10.

@@ P3.unsicher
## UNSICHER
| Nr | Was | Test |
|---|---|---|
| R-U1 | `Set(varSelectedTisch; varNeuBuchenTisch)`: Datensatz aus `LookUp(Tische; …)`, die Kachel liefert einen aus `Gallery1` (`Filter(Tische; …)`). Gleiche Quelle, also gleicher Typ (geschlussfolgert). **Mit P4 ändert sich die Quelle der Galerie, deshalb ändert P4 auch diese Zeile (L5)** | App-Prüfung: kein Typfehler an `varSelectedTisch` |
| R-U2 | Liegt das alte Ende nicht im Halbstundenraster (nur bei Buchungen, die direkt in der Liste angelegt wurden), passt die Vorgabe nicht zur Ende-Liste | Ende im Dialog prüfen. `btnSpeichern` prüft „Ende nach Beginn“ |
| R-U3 | Knopf Größe 12 in Höhe 32: „Neu buchen“ ca. 90 px Text (geschätzt je Zeichenart, Semibold) plus Rand in Breite 120 | Sichtprüfung |

@@ P3.rueckfall
## Rückfall
- `btnNeuBuchenHeute` löschen, `lblStatusHeute.Visible` auf `true`.
- `btnEincheckenHeute.DisplayMode`, `.DisabledFill`, `.DisabledBorderColor` und `btnHitArea.OnSelect` aus Anhang A. Ohne den Knopf darf R3 bleiben.
- **Ist P4 schon eingefügt:** L5 ist dann mit dem Knopf weg, sonst nichts zu tun.

@@ P4.kopf
# P4 Grundriss-Laden, Fassung 2 (Tischbuchung Desktop, 10.11.2026)

Für Josias. Teil der **abgestimmten Pakete** (`EINSETZPLAN.md`), **als letztes** einzufügen, in einer ruhigen Stunde. Grundlage: **Export 10.11. 08:13 + P0–P3**. K1–L4 sind **unverändert** aus Fassung 1 (13.10.), ihre Vorher-Fassungen passen auf den Export 10.11. genau (maschinell geprüft). Neu ist **L5**. Erzeugt und geprüft mit `werkzeuge/grundriss_laden.py` und `werkzeuge/abstimmung.py` (0 Fehler). **Nicht unabhängig geprüft** (Josias’ Entscheidung, 13.10.). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

@@ P4.kurzfassung
## Kurzfassung
- **Was es bringt:** Keine Kacheln mehr kurz oben links bei 0/0 beim Start (Stufe 1: L1 + L2). Wechsel OG↔UG sofort, weil alle Tische einmal gelesen und dann lokal gefiltert werden (Stufe 2: L3, dazu L4 als Kann). K1 macht die gewählte Zeile im Geschoss-Menü lesbar.
- **Neu in Fassung 2, L5 (Befund der Abstimmung):** Nach L3 liefert die Grundriss-Galerie Datensätze aus `TischeLokal` (`{ID; Titel; Geschoss; Gesperrt}`). „Neu buchen“ aus P3 füllte `varSelectedTisch` aber mit einem vollen Datensatz aus `Tische`. **Zwei Datensatz-Typen in einer Variable** (Regel aus dem Projekt, belegt durch frühere Fehler). L5 ändert in `btnNeuBuchenHeute.OnSelect` ein Wort: `LookUp(TischeLokal; …)` statt `LookUp(Tische; …)`. Damit liest „Neu buchen“ auch keine Liste mehr.
- **Gesperrt:** Mit L5 kennt „Neu buchen“ die Sperre wie die Kachel ab App-Start. Buchen geht trotzdem nicht, weil `btnSpeichern` frisch am Server prüft (belegt).
- **Umfang:** 6 Properties (`App.Formulas` zweimal: Stufe 1, dann Endfassung) + L5 = 7 Blöcke. Kein neues Steuerelement, keine neue Variable, kein Schreibzugriff.
- **Reihenfolge:** K1 jederzeit. L1 → L2 direkt hintereinander. Dann L3, L4. **L5 direkt nach L3** (vorher passt der Typ noch, nachher nicht mehr). Fehlt P3, entfällt L5.

@@ P4.einfuegen
## 2. Einfügen
1. **Sicherung:** Datei → Speichern unter → Diesen Computer (`.msapp`). Bildschirmfotos für Test 5 machen, **bevor** etwas geändert wird (Test 0).
2. Reihenfolge: **K1** · **L1 → L2** direkt hintereinander, dann Tests 1–3 · **L3** (erst `App.Formulas`, dann `Gallery1.Items`) · **sofort L5** · dann Tests 4–8 und L5-Test · **L4** (Kann), dann Test 9.
3. Nach jedem Schritt die App-Prüfung ansehen: keine roten Fehler. Ausnahme: zwischen L1 und L2 kurz Fehler an `Rectangle1`/`conDetailsPopup` (siehe L1).
4. `App.Formulas` liegt in Studio bei **App** → Property-Liste oben links → `Formulas`. Den ganzen Inhalt markieren (Strg+A) und ersetzen.
5. Erst nach Test 10 veröffentlichen.

@@ P4.L5
**Was:** In `btnNeuBuchenHeute.OnSelect` wird nur `Tische` durch `TischeLokal` ersetzt. Sonst nichts (maschinell geprüft).
- Danach füllen alle Setzer von `varSelectedTisch` denselben Typ: `ThisItem` der Galerie (`TischeLokal`), `varNeuBuchenTisch` (`TischeLokal`) oder `Blank()` (maschinell geprüft). Gelesen werden nur `ID`, `Titel`, `Geschoss`, `Gesperrt`, die `TischeLokal` alle hat.

**Test (L5):** App-Prüfung ohne Fehler an `varSelectedTisch`/`btnNeuBuchenHeute`. Dann Einsetzplan Teil A Test 9 wiederholen (mit Testknopf): „Neu buchen“ öffnet den Dialog mit dem richtigen Tisch und Geschoss (wie beim Antippen der Kachel), Speichern bucht.

**Rückfall:** Anhang A (`LookUp(Tische; …)`). Nur zusammen mit Stufe 2 zurücknehmen, sonst entsteht der Typ-Konflikt umgekehrt.

@@ P4.unsicher_neu
| U8 | L5: `LookUp` auf eine benannte Formel mit `ForAll` im OnSelect einer Galerie-Karte (geschlussfolgert: geht wie auf jede Tabelle) | L5-Test |

@@ E.kopf
# EINSETZPLAN: abgestimmte Pakete (Tischbuchung Desktop, 10.11.2026)

Für Josias. Grundlage: **Export 10.11. 08:13** („echt“, App „Tischbuchung“, Desktop, zeichengleich mit 25.10.). Alle Pakete sind **der Reihe nach** auf diesen Export gelegt und zusammen geprüft (`werkzeuge/abstimmung.py`, 0 Fehler, Mutationstest MUTZAHL). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

@@ E.kurzfassung
## Kurzfassung
- **Fünf Pakete, eine Reihenfolge, keine Überschneidung ohne Abstimmung:**

| Paket | Inhalt | Properties | neue Steuerelemente | Dokument | geprüft |
|---|---|---|---|---|---|
PAKET_TABELLE

- **Jeder Block passt genau auf den Stand davor** (maschinell: das „Vorher“ jedes Blocks ist zeichengleich mit dem Stand nach den vorigen Paketen). Zusammen ZAHL_PROPS verschiedene Properties und 11 neue Steuerelemente.
- **Nur drei Properties ändern zwei Pakete,** jeweils aufeinander aufgebaut: `btnHitArea.OnSelect` (P1 → P3), `btnNeuBuchenHeute.OnSelect` (P3 → P4 L5), `App.Formulas` (P4 Stufe 1 → Endfassung).
- **Was die Abstimmung gefunden und behoben hat:**
  1. **P3 ↔ P4, Typ-Konflikt (neu, L5):** Nach Grundriss-Laden L3 liefert die Galerie `TischeLokal`-Datensätze, „Neu buchen“ füllte dieselbe Variable mit `Tische`-Datensätzen. P4 enthält jetzt L5 (ein Wort).
  2. **P1 ↔ P3:** Nachtrag 6 ist auf „Für andere buchen“ aufgebaut. Beide Öffner des Buchungsdialogs setzen Gast-Schalter, Namen und „Trotzdem“ zurück (maschinell geprüft).
  3. **Testbogen:** Der Testbogen aus Nachtrag 5 passte nicht mehr. Test 4 erwartete „erst ab 30 Minuten“, du hast am 25.10. das Check-in-Fenster auf **60 Minuten** gestellt. Test 13 erwartete die harte Sperre „zwei Tische“, mit P1 kommt der Hinweis. Test 8 tippte eine verfallene Karte an, mit P3 ist sie gesperrt. **Ersetzt durch den gemeinsamen Testbogen unten.**
- **Was der Endstand erfüllt (maschinell, über alle Pakete):** Klammern und Rückübersetzung in allen geänderten Properties. Jede gelesene Variable wird irgendwo gesetzt. Alle genannten Steuerelemente gibt es. Alle 8 Schreibstellen haben Zweifach-Sperre und Ladezeile, die Ladezeile steht 18× in einer Fassung. `GastName` steckt in jeder Füllung von `colNeuIch`/`colVerlIch`. Jede gewählte Buchung kommt aus `Tischbuchungen`. Freigabe-Grenze überall 30 Min.
- **Zwei Sitzungen:**
  1. **Sitzung 1 (P0, P2, P1, P3):** Spalte `GastName` anlegen, einfügen, Teil 0, A und B testen, veröffentlichen. Etwa 2–3 Std einfügen, 1,5 Std testen.
  2. **Sitzung 2 (P4) in einer ruhigen Stunde,** frühestens am nächsten Tag: Grundriss-Laden einfügen, Teil C testen, veröffentlichen.
- **Offen bei dir (blockiert nichts):** Kontaktzeile im Hinweis, Check-in-Frage beim Start und Erinnerung noch bei 30 Min (Abschnitt 5), Handy-App nicht angepasst.

@@ E.reihenfolge
## 1. Reihenfolge und Voraussetzungen
| Schritt | Was | Warum an dieser Stelle |
|---|---|---|
| 0 | **Sicherung** `.msapp` (Datei → Speichern unter → Dieser Computer). Am besten alles zuerst in deiner Kopie | Rückfall |
| 1 | **Neuer Export, falls du seit dem 10.11. 08:13 etwas gespeichert hast.** Dann erzeuge ich die Blöcke neu (Minuten). Sonst würde ein Block deine Änderung überschreiben | „ganze Property“ |
| 2 | **P0** Design (7) | unabhängig |
| 3 | **P2** Nachtrag 5 (21) | unabhängig von P1. Muss vor P3 rein (N4 bringt die Statusregel, an der P3 hängt) |
| 4 | **Spalte `GastName`** in `Tischbuchungen` (Eine Textzeile, nicht erforderlich), in Studio Daten → `Tischbuchungen` → Aktualisieren | P1 schreibt und liest sie |
| 5 | **P1** Für andere buchen v2 (179, 10 neue Steuerelemente) | vor P3 |
| 6 | **P3** Nachtrag 6 v2 (32, 1 neues Steuerelement) | braucht P1 und P2 |
| 7 | App-Prüfung ohne rote Fehler, **Testbogen Teil 0, A, B**, veröffentlichen, **Export an mich** (Abgleich gegen den Soll-Stand) | |
| 8 | **P4** Grundriss-Laden v2 (7) in Sitzung 2, dann **Teil C**, veröffentlichen, Export an mich | braucht P3 (wegen L5) |

- P1 und P2 berühren keine gemeinsame Property. Ihre Reihenfolge ist egal (maschinell geprüft), die Tabelle nimmt P2 zuerst, weil es kleiner ist.
- Jedes Dokument hat die Diffs gegen den Stand **direkt davor** und die Originale (Rückfall) im Anhang A.
- **Nachtrag 5 bleibt das Dokument vom 08.10.** Seine Blöcke sind unverändert gültig (Vorher zeichengleich mit dem Export 10.11.). **Nur dessen Abschnitt 3 (Testbogen) gilt nicht mehr**, dafür Teil A unten.
- Rote Fehler mitten in einem Paket sind normal, solange Steuerelemente fehlen, die eine Formel nennt. Am Ende jedes Pakets keine mehr.

@@ E.tests
## 3. Gemeinsamer Testbogen
Ersetzt: Nachtrag 5 Abschnitt 3, Für andere buchen Fassung 1 Abschnitt 3, die Einzeltests in Nachtrag 6. Jeder Test ist gegen die heutigen Regeln geprüft: **Einchecken ab 60 Min vor Beginn** (dein Stand 25.10.), Freigabe 30 Min nach Beginn **und** Buchungszeitpunkt, Startliste ab der nächsten halben Stunde, nie über 22:00, **weicher Hinweis** statt Sperre bei eigener Überschneidung.

### Teil 0: Sichtprüfung (nach dem Einfügen, 5 Min)
| ✓ | Nr | Test | Erwartung |
|---|---|---|---|
| ☐ | 0.1 | App-Prüfung | keine roten Fehler |
| ☐ | 0.2 | **Altbestand:** eine bestehende Buchung im Popup, auf der Dashboard-Karte, im Tab und in beiden Verwalten-Dialogen. Foto vorher (vor P1), Foto nachher | genau gleich |
| ☐ | 0.3 | Dashboard: „Tisch Buchen“ (P0) | blau, weiße Schrift, nicht abgeschnitten, beim Drücken lesbar |
| ☐ | 0.4 | Datum auf morgen, „Heute“ gedrückt halten (P0) | Schrift lesbar. Loslassen → heute |
| ☐ | 0.5 | Buchungsdialog öffnen (Kachel) und Panel („Tisch Buchen“) | Schalter „Für mich“, kein Namensfeld. Panel: Speichern unter der neuen Zeile, nicht abgeschnitten |

### Teil A: Zeitachse heute (etwa 1,5 Std)
**Vorbereitung**
- **N** = jetzt, **T** = nächste halbe Stunde. **Vor 16:00 beginnen** (sonst geht „5 Std“ über 22:00).
- Du brauchst einen Kollegen **K** (oder ein zweites Konto) und vier Tische **X, Y, Z, W** im selben Geschoss.
- Testknopf `btnTestFreigabe` **außerhalb** von `conGrundriss`, `OnSelect`: `Set(varFreigabeMinuten; 1)`. **`App.OnStart` nicht ändern.** „Verfallen“ heißt im Testmodus: Beginn **und** Buchungszeitpunkt mehr als 1 Min her.
- Bei jedem Schreiben kommt die Erfolgsmeldung, nie „nicht angekommen“. Check-in-Fragen, die zwischendurch kommen, mit „Schließen“ wegklicken, außer der Test verlangt etwas anderes.

| ✓ | Zeit | Test | Erwartung |
|---|---|---|---|
| ☐ | N | 1 **OnStart ausführen**, Vorschau | keine Fehler, die Grundriss-Sperre blitzt nicht auf |
| ☐ | N | 2 Testknopf tippen. **K** bucht **X von T bis T + 3 Std** und checkt nicht ein. Du buchst (Grundriss, „Für mich“) **S = W von T bis T + 60** und **E = Z von T + 60 bis T + 90** | „Gebucht …“, beide ohne Aktualisieren in der Dashboard-Liste. Kein Hinweis (keine Überschneidung) |
| ☐ | N | 3 **Erinnerung:** auf dem Dashboard bleiben, kein Dialog offen | Check-in-Frage zu **S** nach höchstens 15 s (N6). Schließen, **nicht** einchecken. Sie kommt frühestens nach 5 Min wieder |
| ☐ | N | 4 Karte **E** antippen → Einchecken (E beginnt bei T + 60, also mehr als 60 Min nach jetzt) | „Einchecken ist erst ab 60 Minuten vor Beginn möglich.“ |
| ☐ | N | 5 **Grundriss-Sperre:** 2:15 Min warten, Kachel und Stockwerk tippen, dann „Grundriss aktualisieren“ | Fläche und Knopf erscheinen, darunter passiert nichts, danach ist die Fläche weg |
| ☐ | ab T | 6 Karte **E** → Einchecken | „Eingecheckt.“ (E beginnt in 60 Min) |
| ☐ | ab T + 1 | 7 **Status ohne Tippen:** Dashboard ansehen | Bei **S** steht nach höchstens 15 s **„Neu buchen“** (blau) statt „Verfallen“ (P3 R2, Restzeit bis T + 60) |
| ☐ | ab T + 1 | 8 Karte **S** daneben (nicht den Knopf) antippen | **nichts passiert**, die Karte ist nicht grau (P3 R1). Karte **E** öffnet weiter den Dialog |
| ☐ | ab T + 1 | 9 **„Neu buchen“** bei S → Dialog: Tisch W, heute, Beginn T + 30, Ende T + 60, Schalter „Für mich“. Speichern. Doppelklick auf Speichern | „Gebucht …“ **ohne Hinweis** (die eigene verfallene S zählt nicht), nur **eine** neue Buchung **S2 = W T + 30 bis T + 60**. Die alte S zeigt weiter „Neu buchen“ (nichts wird gelöscht) |
| ☐ | ab T + 1 | 10 Dialog im Grundriss über eine freie Kachel öffnen | Ende = Beginn + 30 Min, nicht das Ende aus Test 9 (P3 R3). Schalter „Für mich“. Schließen |
| ☐ | ab T + 1 | 11 Aktualisieren. Kachel **X** | **grün**, Klick → Buchungsdialog. Schließen |
| ☐ | ab T + 1 | 12 Panel „Tisch Buchen“: heute, Beginn wie vorgeschlagen (T + 30), Tisch X wählen, **nicht speichern** | X steht in der Liste, „5 Std“ **hellgrün** und bedienbar (F5 über N4). Panel schließen |
| ☐ | ab T + 1 | 13 Grundriss → X → **T + 90 bis T + 120** buchen | „Gebucht …“ ohne Hinweis (E endet bei T + 90), ohne Aktualisieren in der Liste |
| ☐ | ab T + 1 | 14 Buchung X verlängern (+1 Std) | verlängert bis T + 180, weil die Buchung von K verfallen ist |
| ☐ | ab T + 1 | 15 **Y von T + 180 bis T + 210** buchen. Dann X noch einmal +1 Std | **Hinweis** „Zur selben Zeit schon gebucht“, Knopf „Trotzdem verlängern“. **Abbrechen** → X bleibt bis T + 180, die Dauer +1 Std bleibt gewählt. Noch einmal Speichern → Hinweis → **Trotzdem verlängern** → X bis T + 240 |
| ☐ | ab T + 61 | 16 **Auschecken E:** Karte E → „Auschecken“ → „Wirklich auschecken?“ → nach 1 s tippen. Vorher einmal doppelklicken | Der Doppelklick checkt nicht aus. Danach Ende = jetzt |
| ☐ | nach 16 | 17 **Stornieren (N1–N3):** Dashboard **Y**: erst doppelklicken, dann „Ja, stornieren“. Tab **X**: „Stornieren“, Tab wechseln, zurück, X öffnen → wieder „Stornieren“, dann bestätigen. **Mehrfach:** zwei Buchungen für morgen anlegen, im Tab beide anhaken → „Ja, 2 stornieren“, dabei einmal die Auswahl ändern | erst die Frage, dann „storniert“. Doppelklick löscht nicht. Nach Tab-Wechsel oder geänderter Auswahl fragt die App neu. S, S2 und E sind schon beendet und stehen nicht mehr in den Listen |
| ☐ | | 18 **Testknopf löschen. Dann OnStart ausführen** (oder Vorschau schließen und neu öffnen). Bis dahin bleibt `varFreigabeMinuten` = 1. Keine Test-Steuerelemente in der Strukturansicht. K storniert seine Buchung | |
| ☐ | hh:20 | 19 **Spätbuchung mit echten 30 Minuten (Muss, aus Nachtrag 5).** Nach Test 18. K bucht **am Handy** um hh:20 einen Tisch ab **hh:00** (die Handy-Startliste beginnt bei der laufenden halben Stunde) und checkt nicht ein, Dauer mindestens bis hh+1:00. **Kontrolle:** du buchst um hh:20 am PC einen anderen Tisch ab hh:30, nicht einchecken. Um hh:35 und hh:55 Grundriss aktualisieren | Kontrolle um hh:35 orange (sonst läuft noch der Testmodus → Test 18). **K** um hh:35 **belegt** (verfällt erst 30 Min nach dem Buchungszeitpunkt, hh:50), um hh:55 frei. **Ist K schon um hh:35 frei**, kommt `Erstellt` leer an → **nicht veröffentlichen**, an mich melden. Danach beide stornieren |

### Teil B: Für andere buchen (alles für morgen, ohne Zeitdruck, etwa 30 Min)
Alle Testbuchungen für **morgen**, damit keine Vergangenheits- oder Check-in-Regel stört. Am Ende alle stornieren. Tische frei wählen, aber getrennt halten.

| ✓ | Nr | Schritt | Erwartung |
|---|---|---|---|
| ☐ | B1 | Grundriss: UG Desk 1, morgen 14:00–15:00, „Für mich“ | gebucht, kein Hinweis |
| ☐ | B2 | UG Desk 2, morgen 16:00–17:00, „Für mich“ | gebucht, kein Hinweis |
| ☐ | B3 | UG Desk 3, morgen 14:00–15:00, „Für mich“ | **Hinweis** „Zur selben Zeit schon gebucht“ mit Abbrechen / Trotzdem buchen. **Abbrechen** → nichts gebucht (Tab prüfen), Dialog bleibt offen |
| ☐ | B4 | Dasselbe noch einmal → **Trotzdem buchen**, dabei doppelklicken | einmal gebucht, Erfolgsmeldung |
| ☐ | B5 | UG Desk 4, morgen 14:00–15:00, „Für andere“, Name leer → Speichern | Meldung „Bitte den Namen …“, nichts gebucht |
| ☐ | B6 | Wie B5 mit Name „Maximilian Mustermann“ | gebucht **ohne Hinweis**, Meldung „… für Maximilian Mustermann …“. Popup der Kachel (Datum morgen): Name, darunter „gebucht von <dir>“. Tab und Verwalten: „für Maximilian Mustermann“, Text nicht über anderen Elementen |
| ☐ | B7 | UG Desk 5, morgen 18:00–19:00 „Für andere“ (Name „Gast 2“), dann UG Desk 6, morgen 18:00–19:00 „Für mich“ | beide ohne Hinweis (Gast-Buchung zählt nicht) |
| ☐ | B8 | Panel: eigene Buchung **nächsten Montag** 09:00–10:00 anlegen. Dann Serie „Für andere“ (Name „Serie Gast“) Mo–Fr nächste Woche 09:00–10:00 auf anderem Tisch | Serie ohne Hinweis, alle 5 Termine mit Gastname |
| ☐ | B9 | Panel: Serie „Für mich“ über dieselbe Woche 09:00–10:00 auf drittem Tisch | Hinweis „An 1 von 5 Terminen …“. Abbrechen → nichts. Trotzdem → alle 5 gebucht |
| ☐ | B10 | Tab „Buchungen“ → UG Desk 1 (morgen 14–15) verwalten → +2 Std (überschneidet Desk 2 16–17) → Speichern | Hinweis „Trotzdem verlängern“. Abbrechen → unverändert, +2 Std bleibt gewählt. Speichern → Trotzdem → 14–17 |
| ☐ | B11 | Tab → Gast-Buchung UG Desk 5 (18–19) +1 Std, obwohl Desk 6 (18–19) dir gehört | verlängert, kein Hinweis |
| ☐ | B12 | Gast-Buchung stornieren (Verwalten → Stornieren → Ja, stornieren), eine weitere über Mehrfachauswahl | geht wie bei eigenen |
| ☐ | B13 | Buchungsdialog und Panel nach B6 neu öffnen | „Für mich“, Name leer |
| ☐ | B14 | **Gast heute einchecken:** eine Gast-Buchung für heute ab der nächsten halben Stunde anlegen, Karte antippen → Einchecken (geht ab 60 Min vor Beginn) | Check-in geht durch dich. Die Karte zeigt „für Name“ unter der Zeit |
| ☐ | B15 | Aufräumen: alle Testbuchungen stornieren | Liste leer |

### Teil C: nach P4 Grundriss-Laden (Sitzung 2)
Den Testbogen aus P4 Abschnitt 4 (Tests 0–11, Test 0 = Fotos **vor** dem Einfügen) und den L5-Test. Dazu einmal Teil A Tests 7 und 9 mit Testknopf (Neu buchen nach L5) und am Ende Testknopf löschen, OnStart ausführen.

@@ E.rueckfall
## 4. Rückfall
- **Ein Paket:** rückwärts in der Reihenfolge P4 → P3 → P1 → P2 → P0. Jedes Dokument hat die Originale im Anhang A, also den Stand direkt vor dem Paket.
- **P1 zurück:** vorher P3 zurück (P3 baut auf `btnHitArea.OnSelect` aus P1 auf). **P3 zurück:** vorher P4 L5 zurück oder P4 ganz.
- **Alles:** make.powerapps.com → App → Details → **Versionen** → Version vor dem Einfügen → Wiederherstellen. Oder die `.msapp`-Sicherung.
- Die Spalte `GastName` kann in jedem Fall bleiben.

@@ E.offen
## 5. Offene Punkte (blockieren nichts)
| Nr | Was | Vorschlag |
|---|---|---|
| O1 | **Check-in-Fenster:** Einchecken geht seit 25.10. ab 60 Min vor Beginn (`btnEinchecken`, Kachel). Die automatische Frage beim Start (`App.OnStart`, `colCheckinFrage`) und die Erinnerung im Timer kommen weiter erst ab **30 Min** (belegt) | So lassen: die Erinnerung soll kurz vorher kommen, nicht eine Stunde vorher. Willst du 60: 3 Zahlen, ich erzeuge die Blöcke |
| O2 | Kontaktzeile im Hinweis (Axel Krägelius / Norman Horn) | Text in `lblFbHinweis.Text` |
| O3 | **Handy-App** kennt `GastName` nicht: Gast-Buchungen blockieren dort den Buchenden zur selben Zeit, und dort gibt es keinen „Trotzdem“-Hinweis | von dir akzeptiert, Handy-Folge später |
| O4 | Check-in-Dialog zeigt den Gastnamen nicht (B9 aus der Prüfung) | kein Muss |
| O5 | Unabhängige Prüfung: P1 Logik ja (Fassung 1), P1 Stil, P3, P4, P0 und die Abstimmung nur maschinell | auf Wunsch eine Prüfung des Endstands |
| O6 | Stil-Audit D4 (Dropdown-Auswahlbalken graublau, 31 Stellen) | nicht Teil dieser Pakete |

@@ E.maschinell
## 6. Maschinelle Prüfung
`werkzeuge/abstimmung.py` legt P0 → P1 → P2 → P3 → P4 der Reihe nach auf den Export und prüft jedes Vorher und den Endstand. `werkzeuge/abstimmung_mutation.py` baut absichtlich Fehler ein: MUTLISTE.
