@@ kopf
# Für andere buchen + weicher Hinweis (Tischbuchung Desktop, 26.10.2026)

Für Josias. Grundlage: **Export 25.10. 20:09** (`Tischbuchungsapp25.10.26_20261025200901.zip`). Erzeugt und maschinell geprüft mit `werkzeuge/fuer_andere.py` (0 Fehler, Mutationstest 8 von 8 erkannt). PRUEFSTATUS. In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

**Voraussetzung:** Jeder Block ersetzt die **ganze** Property. Hast du nach dem 25.10. 20:09 an einer der 14 geänderten Properties etwas gespeichert, erst neu exportieren, ich erzeuge die Blöcke dann neu.

@@ kurzfassung
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

@@ ablauf
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
NEUE_TABELLE

**Ebenen (wichtig):**
- `btnFbHintergrund` und `conFbHinweis` liegen in `Screen1` über allen Dialogen.
- Nach dem Anlegen `btnFbHintergrund` markieren → **Ganz nach vorne bringen**. Danach `conFbHinweis` → **Ganz nach vorne bringen**. Danach **`conLadeOverlay` → Ganz nach vorne bringen**, damit die Ladeanzeige weiter alles überdeckt.
- In der Strukturansicht steht dann von oben nach unten: `conLadeOverlay`, `conFbHinweis`, `btnFbHintergrund`, … Alle anderen bleiben, wo sie sind.
- **In Studio** verdecken die neuen Flächen den Bildschirm nicht, weil `varFbZeige` leer ist. Zum Gestalten kurz `Visible` auf `true` setzen und danach die Formel aus dem Block zurück einsetzen.

@@ S2
**Was:** Ein Hinweis mit Vollbild-Hintergrund. Der Hintergrund fängt alle Klicks ab, solange der Hinweis offen ist. Daneben ist nichts bedienbar, also kann sich auch keine Variable ändern.
- **„Abbrechen“** schließt den Hinweis, nichts wird gespeichert. Der Buchungsdialog oder das Panel bleibt offen.
- **„Trotzdem buchen“ / „Trotzdem verlängern“** führt den Knopf, der gefragt hat, noch einmal aus, diesmal mit Bestätigung (`varFbTrotzdem`). Die Speicherlogik steht also nur einmal da.
- Der Knopf blendet den Hinweis nicht selbst aus. Das macht der Speichern- bzw. Verlängern-Knopf als erste Anweisung. So trifft ein Doppelklick nie den Dialog darunter, und während des Speicherns deckt die Ladeanzeige alles ab.

**Rückfall:** `btnFbHintergrund` und `conFbHinweis` (samt Inhalt) löschen. Vorher S5 und S6 zurücknehmen, weil sie den Hinweis öffnen.

@@ S3
**Was:** Im Buchungsdialog (aus dem Grundriss), in der mittleren Spalte unter dem Tischnamen: Umschalter `tglFuerAndere` und darunter das Namensfeld `txtGastName`.
- Der Platz ist frei: Bild bis X 245, Eingaben ab X 448, Wochentage erst ab Y 290 (belegt, Export).
- Das Namensfeld erscheint nur, wenn der Umschalter auf „Für andere“ steht.

**Rückfall:** beide löschen (erst S5/S7 zurücknehmen).

@@ S4
**Was:** Im Panel „Tisch buchen“ eine Zeile mit Umschalter `tglFuerAnderePanel` und Namensfeld `txtGastNamePanel`. Sie steht unter den Wochentagen. **`btnSpeichernTischePanel` rückt 60 nach unten** (Y 531 → 591, Unterkante 631 von 678 bei 768 Höhe, gerechnet).

**Rückfall:** `btnSpeichernTischePanel.Y` aus Anhang A, beide Steuerelemente löschen.

@@ S5
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

@@ S6
**Was, in beiden Verlängern-Knöpfen gleich:**
1. Die Bestätigung wird am Anfang verbraucht.
2. Eigene andere Buchungen zur selben Zeit: Gast-Buchungen zählen nicht. Eine Gast-Buchung wird ohne diese Prüfung verlängert.
3. Statt „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“ (Sperre) kommt der Hinweis mit „Trotzdem verlängern“.
- Verkürzen, 22:00, „Tisch inzwischen belegt“ und verfallene Buchung bleiben wie heute.

**Rückfall:** beide Properties aus Anhang A.

@@ S7
**Was:** Beim Öffnen des Buchungsdialogs (Kachel) und des Panels („Tisch Buchen“) werden Umschalter und Name zurückgesetzt. Eine liegen gebliebene Bestätigung wird gelöscht.
- Das sind die beiden einzigen Stellen, die Dialog bzw. Panel öffnen (belegt).
- Etage, Datum, Tab und Mehrfachauswahl schließen den Dialog wie bisher. Beim nächsten Öffnen ist alles zurückgesetzt.

**Rückfall:** beide Properties aus Anhang A.

@@ S8
**Was:** Gastname in der Anzeige. Jede Formel hat die Form `If(IsBlank(….GastName); <alte Formel>; <neu>)`. Altbestand sieht also exakt aus wie heute.
- Im Popup wird `lblPerson` nur bei Gast-Buchungen breiter (bis vor das Bild) und zweizeilig. Die Zeitzeile `lblZeit2` rückt dann 12 nach unten, sonst würde die zweite Zeile sie berühren.
- Im Tab-Verwalten-Dialog wird der Titel nur bei Gast-Buchungen breiter.

**Rückfall:** alle Properties aus Anhang A.

@@ tests
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

@@ rueckfall
## 4. Rückfall gesamt
- **Einzelschritte:** siehe jeweiligen Schritt, Originale in Anhang A. Reihenfolge rückwärts: S8 → S7 → S6 → S5 → S4 → S3 → S2.
- **Alles:** frühere Version wiederherstellen (make.powerapps.com → App → Details → Versionen) oder die Sicherung `.msapp`.
- **Die Spalte `GastName` kann bleiben.** Alte Formeln lesen sie nicht, und der Flow reagiert nicht auf sie (geschlussfolgert). Löschen ist nicht nötig.

@@ unsicher
## 5. UNSICHER
| Nr | Was | Prüfen |
|---|---|---|
| U1 | `Select(btnSpeichern)` usw. aus dem Hinweis führt den Knopf im Container aus | Test 4, 9, 10. Passiert bei „Trotzdem“ nichts: mir melden. Notweg: Hinweis per „Abbrechen“ schließen geht immer |
| U2 | `GastName` kommt in den Sammlungen `colNeuIch`/`colVerlIch` an (Studio lädt nur benutzte Spalten) | Test 7 und 11. Wenn nicht, erscheint der Hinweis bei Gast-Überschneidung unnötig, gebucht werden kann trotzdem. Kein falscher Datensatz |
| U3 | Der klassische Umschalter zeigt „Für mich“/„Für andere“ neben dem Schalter in Breite 165 | Sichtprüfung. Sonst `Width` auf 180 |
| U4 | Panel bei Fensterhöhe unter etwa 720: „Speichern“ kann unten abgeschnitten sein | Fenster verkleinern |
| U5 | Rolle von Axel Krägelius und Norman Horn im Hinweistext (Frage 5 offen) | Text in `lblFbHinweis.Text` anpassen |

@@ pruefung_unabh
## 6. Unabhängige Prüfung
PRUEFUNG_PLATZHALTER
