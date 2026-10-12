@@ kopf
# Nachtrag 6: Verfallene Buchung – kein Check-in-Dialog, dafür „Neu buchen“ (12.10.2026)

Für den Desktop-Chat. Grundlage: **Export 08.10. 14:26** + **Nachtrag 5**. Nachtrag 5 ändert keine der Properties hier, deshalb rechnet jeder Diff gegen den Export. Erzeugt und geprüft mit `werkzeuge/nachtrag6.py`. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

@@ kurzfassung
## Kurzfassung
- **Fehler (belegt, von Josias gemeldet):** Die ganze Karte in der Dashboard-Liste ist ein unsichtbarer Knopf (`btnEincheckenHeute`, `DisplayMode.Edit` fest). Er öffnet immer den Check-in-Dialog, auch bei „Verfallen“. Erst dort kommt „Zu spät“.
  - Die Handy-App sperrt ihren Einchecken-Knopf bei „Verfallen“ schon (`btnEincheckenH.DisplayMode`, belegt).
- **R1:** Die Karte ist gesperrt, wenn die Buchung verfallen oder schon zu Ende ist. Eine laufende eingecheckte Buchung öffnet weiter den Dialog (Auschecken).
  - Wichtig, **belegt**: `DisabledFill` steht beim Knopf auf dem Standard-Hellgrau `RGBA(244, 244, 244, 1)` und `DisabledBorderColor` auf Grau. Ohne R1 vollständig würde eine gesperrte Karte grau überdeckt. Deshalb werden beide transparent gesetzt.
- **R2 „Neu buchen“:** Bei einer verfallenen Buchung von heute steht statt „Verfallen“ ein blauer Knopf **„Neu buchen“**. Er erscheint nur, wenn bis zum alten Ende noch mindestens eine halbe Stunde frei ist.
  - Er öffnet **den vorhandenen Buchungsdialog** für diesen Tisch, Beginn ab der nächsten halben Stunde, Ende = altes Ende.
  - Gespeichert wird mit `btnSpeichern`, also mit allen Prüfungen: frei, zwei Tische, Gesperrt, Vergangenheit, 22:00, Nachlese. Es gibt keinen neuen Schreibweg.
  - Die eigene verfallene Buchung blockiert nicht, weil die Freigabe-Regel in `btnSpeichern` sie als frei zählt (F4, belegt).
  - Ist der Tisch inzwischen an jemand anderen vergeben, meldet `btnSpeichern` das wie sonst auch.
- **R3:** Der Kachel-Dialog setzt die neue Ende-Vorgabe zurück, sonst stünde dort das Ende aus „Neu buchen“.
- **Umfang:** 25 Properties, 1 neues Steuerelement (`btnNeuBuchenHeute`). Maschinell 0 Fehler. In Studio ist nichts getestet.
- **Abfragen:** Die Karte rechnet nur mit Variablen und dem Takt (`varJetztTakt`, alle 15 s). „Neu buchen“ liest beim Tippen einmal `Tische` (Gesperrt). Keine Abfrage ohne Tippen.
- **Voraussetzung:** Nachtrag 5 N4 (S3b) ist eingefügt. Sonst zeigt die Statusanzeige „Verfallen“ später als Karte und Knopf.

@@ R1
**Regel:** gesperrt, wenn `Endzeit` erreicht ist **oder** die Buchung verfallen ist (nicht eingecheckt, Beginn und Buchungszeitpunkt älter als 30 Min).
- Es ist dieselbe Verfallsregel wie in `lblStatusHeute` nach S3b, zeichengleich (maschinell geprüft).
- Sie rechnet mit dem 15-s-Takt. Die Karte sperrt also spätestens 15 s nach Fristablauf, ohne Tippen.

**Test:**
1. Testknopf `Set(varFreigabeMinuten; 1)`.
2. Eigene Buchung zur nächsten halben Stunde, nicht einchecken.
3. Ab 1 Min nach Beginn ist die Karte nicht mehr anklickbar und nicht grau.
4. Eine eingecheckte, laufende Buchung öffnet weiter den Dialog.

@@ R2
**Neu anlegen, Name exakt so:**
1. In der Strukturansicht `galTischbuchungenHeute` markieren.
2. Das Stift-Symbol oben links in der **ersten Karte** anklicken. Damit ist die Vorlage gewählt.
3. Einfügen → Schaltfläche (klassisch) → umbenennen in **`btnNeuBuchenHeute`**.
4. Prüfen: `btnNeuBuchenHeute` liegt **in** `galTischbuchungenHeute` und in der Strukturansicht **über** `btnEincheckenHeute` (Neu anordnen → Ganz nach vorne).

**Ablauf:**
1. „Neu buchen“ prüft den Tisch frisch (gibt es ihn noch, ist er gesperrt).
2. Danach öffnet es den Buchungsdialog. Dabei werden genau die Werte zurückgesetzt, die auch die Kachel im Grundriss zurücksetzt (maschinell geprüft).
3. Datum heute, Beginn ab der nächsten halben Stunde, Ende = altes Ende.
4. Josias kann Beginn und Ende im Dialog noch ändern.

`lblStatusHeute.Visible` = `!btnNeuBuchenHeute.Visible`. Wo der Knopf steht, ist das Wort „Verfallen“ weg. Ist keine Restzeit mehr übrig, steht wieder „Verfallen“.

**Test:**
1. Testknopf `Set(varFreigabeMinuten; 1)`.
2. Eigene Buchung Tisch X von T bis T + 60 (T = nächste halbe Stunde), nicht einchecken.
3. Ab T + 1 Min: In der Karte steht nach höchstens 15 s **„Neu buchen“** statt „Verfallen“.
4. Tippen → Buchungsdialog für X, Beginn T + 30, Ende T + 60 → Speichern → „Gebucht …“, die neue Buchung steht in der Liste.
5. Die alte Buchung zeigt weiter „Neu buchen“, weil sie in der Liste bleibt (nichts wird gelöscht). Wer sie nicht mehr sehen will, storniert sie über den Stift.
6. Gegenprobe:
   - Kollege bucht X von T + 30 bis T + 60 vor dir → „Neu buchen“ → Speichern → Meldung „belegt“.
   - Tisch in SharePoint sperren → „Neu buchen“ → „Dieser Tisch ist zurzeit gesperrt.“
7. Danach `Set(varFreigabeMinuten; 30)` über OnStart wiederherstellen, Testknopf löschen.

@@ R3
`btnHitArea.OnSelect` bekommt nur eine Zeile vor `Reset(ddEnde)`: `Set(varEndeOverride; "")`. Sonst nichts (maschinell geprüft).
- Belegt: `ddEnde.Default` liest `varEndeOverride`.
- Belegt: Bisher setzte nur `App.OnStart` diese Variable, deshalb fiel das nie auf.

**Test:** Nach „Neu buchen“ (Dialog abbrechen) im Grundriss eine freie Kachel antippen → Ende = Beginn + 30 Min, nicht das alte Ende.

@@ unsicher
## UNSICHER
| Nr | Was | Test |
|---|---|---|
| R-U1 | `Set(varSelectedTisch; varNeuBuchenTisch)`: Datensatz aus `LookUp(Tische; …)`, bisher aus `Gallery1` (`Filter(Tische; …)`). Gleicher Datentyp (geschlussfolgert, gleiche Datenquelle) | App-Prüfung: kein Typfehler an `varSelectedTisch` |
| R-U2 | Liegt das alte Ende nicht im Halbstundenraster (nur bei Buchungen, die direkt in der Liste angelegt wurden), passt die Vorgabe nicht zur Ende-Liste (geschlussfolgert) | Ende im Dialog prüfen. `btnSpeichern` prüft „Ende nach Beginn“ |
| R-U3 | Ändert man im Dialog das Datum, setzt `dpDatum.OnChange` die Ende-Liste zurück und nimmt wieder das alte Ende (belegt: `Reset(ddEnde)` dort). Das ist gewollt, der Hinweis dient nur der Vollständigkeit | — |

@@ rueckfall
## Rückfall
- `btnNeuBuchenHeute` löschen.
- `lblStatusHeute.Visible` auf `true` setzen.
- `btnEincheckenHeute.DisplayMode`, `.DisabledFill`, `.DisabledBorderColor` und `btnHitArea.OnSelect` auf die Fassungen in Anhang A zurücksetzen. Ohne den Knopf darf R3 bleiben.
