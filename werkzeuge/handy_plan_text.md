@@ kopf
# Umbauplan Handy-App „Tischbuchung Handy“ (08.10.2026)

Für den Chat, der die Handy-App weiterbaut. Erzeugt von Claude Code (Desktop-Repo `tischbuchung-app`) mit `werkzeuge/handy_plan.py` aus dem **Handy-Export vom 08.10., 11:51** und maschinell geprüft. Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**. Ersetzt `AUFTRAG_Handy_Freigabe.md` (jetzt mit fertigen Formeln).

@@ start
## 0. Startprompt für den Handy-Chat (so übergeben)
> Du baust mit Josias die Handy-App „Tischbuchung Handy“ (App-ID `e218702e-…`) weiter. Sie nutzt dieselben SharePoint-Listen wie die Desktop-App „Tischbuchung“. Die Desktop-App bekommt gerade dieselben Regeln (Paket F Fassung 2). Damit beide Apps zusammenpassen, setze bitte diesen Umbauplan **Schritt für Schritt** um (H0 → H7). Pro Schritt: ganze Property ersetzen (Block unverändert, deutsche Schreibweise), App-Prüfung, Test, Strg+S. Arbeitest du lieber mit YAML, stehen die englischen Formeln in `handy_bloecke.json` (Feld `yaml`). **Formeln nicht umschreiben.** Passt ein Block nicht zum Stand im Studio (der Diff zeigt, was vorher dort stehen muss), stoppen und Claude Code einen neuen Export geben. Die Handy-App wird erst geteilt, wenn H1–H6 drin und getestet sind. Lege diesen Plan und `handy_bloecke.json` im Vault unter `Tischbuchung/2026-10-08_Handy` ab.

@@ kurzfassung
## 1. Kurzfassung
- **Warum jetzt:** Die Desktop-App gibt ab Paket F nicht eingecheckte Buchungen **in der App** frei. Es gibt keinen Flow, und nichts wird gelöscht. Eine Buchung **verfällt**, wenn sie nicht eingecheckt ist und Beginn **und** Buchungszeitpunkt (`Erstellt`) mehr als 30 Minuten zurückliegen. Verfallene Buchungen zählen überall als frei.
- **Ohne denselben Umbau in der Handy-App** passiert Folgendes (geschlussfolgert aus den Formeln):
  1. Die Handy-App zeigt freigegebene Tische weiter als belegt. Das ist harmlos.
  2. Sie lässt **Einchecken auf eine verfallene Buchung** zu, auch wenn der Tisch inzwischen neu vergeben ist. Dann sind zwei Personen am selben Tisch eingecheckt.
  3. **Fehlalarm beim Buchen:** Die Nachprüfung nach dem Patch meldet „Jemand hat diesen Tisch fast gleichzeitig vor dir gebucht“, sobald auf dem Tisch eine verfallene Buchung liegt. Der Grund: Sie zählt jede ältere Zeile mit.
  4. **Falsche Rücknahme beim Verlängern:** Die Nachprüfung nimmt die Verlängerung zurück, sobald irgendeine andere Zeile im Zeitraum liegt, auch eine verfallene.
- **Umfang:** 7 Schritte, **17 Properties**, **kein neues Steuerelement**. Dazu ein Vorab-Test (H0).
- **Enthalten:**
  - Freigabe-Regel.
  - Gesperrte Tische (`Tische.Gesperrt`) ausblenden.
  - Einchecken bis zur Frist, mit dem noch offenen **B5/B8** (eigene Variable `varCheckinID`, Knopfanzeige mit `varJetzt`).
  - Nachprüfungen ohne Fehlalarm und pro Klick eindeutig (kein Zwischenspeicher).
  - Stornieren und Jetzt beenden nur für eigene Buchungen.
  - Startzeiten ab 06:00.
- **Geprüft:** maschinell 0 Fehler (Anhang B) und unabhängig (`pruefung_handy.md`). In Studio nichts getestet.

@@ stand
## 2. Stand der Handy-App (Export 08.10., belegt)
- 69 Steuerelemente, 793 Properties. Gegenüber dem 07.10. sind 18 Properties geändert und 7 neu.
- **Neu: `tmrJetzt`** (setzt `varJetzt` jede Minute) und **`App.OnError`**.
- **Schon drin aus der Prüfung B1–B11** (`05_HANDY_APP/skripte/fix_pruefung.js`):
  - Verlängern +1/+2: 22:00 per `DateTime`, „bereits beendet“, „zwei Tische“, Nachprüfung mit Rücknahme.
  - Jetzt beenden (B1/B4): nicht vor Beginn, nicht nach Ende, Ende auf die halbe Stunde.
  - Stornieren-Knopf mit Sperre (B10).
  - `tmrJetzt`.
- **Noch nicht drin: B5/B8 (Einchecken).** Die Galerie setzt weiter `varBuchungID`, das auch der Verwalten-Dialog nutzt, und die Knopfanzeige rechnet mit `Now()` statt `varJetzt`. **Kommt mit H6.**
- **Was fehlt (für die gemeinsamen Regeln):** Freigabe-Regel, gesperrte Tische, Startzeit 06:00. `colTische` wird nur beim Start geladen: Ein Tisch, den Josias sperrt, erscheint erst nach Neustart als gesperrt. Das behebt H3 beim Aktualisieren.

@@ regeln
## 3. Gemeinsame Regeln Desktop + Handy (Stand 08.10.)
| Regel | Desktop | Handy nach diesem Plan |
|---|---|---|
| Buchbar | 06:00–22:00, nicht in der Vergangenheit | gleich (H7, vorhanden) |
| Einchecken | ab 30 Min vor Beginn bis zur Frist (Beginn bzw. Buchungszeitpunkt + 30 Min) | gleich (H6) |
| Verfallen | nicht eingecheckt, Beginn **und** Erstellt > 30 Min her; zählt als frei, nichts gelöscht | gleich (H3–H6) |
| Gesperrte Tische | nicht buchbar | gleich (H3, H4) |
| Keine zwei Tische zur selben Zeit | beim Buchen und Verlängern | vorhanden, jetzt ohne verfallene (H4, H5) |
| Stornieren / Beenden | nur eigene, Desktop ohne Rückfrage (Josias), Auschecken mit zweitem Tippen | nur eigene (H2), Handy behält seine Rückfrage beim Stornieren |
| Auschecken / Jetzt beenden | Desktop: Ende = nächste Minute | Handy: Ende = laufende halbe Stunde (vorhanden, bleibt) |
| Big Table | Desktop: für alle über den Grundriss buchbar | Handy: nicht buchbar (V-Regel, bleibt) |
| Die 30 Minuten | `varFreigabeMinuten` in `App.OnStart` | gleich (H1); beide Apps **gleich halten** |

@@ nutzung
## 4. So arbeitest du
1. **H0 zuerst** (Vorab-Test), dann H1 → H7. H1 legt `varFreigabeMinuten` und `varFreigabeGrenze` an, alle anderen lesen sie.
2. Je Property: Steuerelement suchen (Ort steht dabei), **ganze Property ersetzen**. Der Diff zeigt, was sich gegenüber dem Export vom 08.10. ändert (`-` alt, `+` neu). **Steht im Studio etwas anderes als die `-`-Zeilen:** stoppen, neuen Export an Claude Code.
3. Nach jedem Schritt App-Prüfung (keine neuen roten Fehler), Test, Strg+S. Nach H1 in Studio **OnStart ausführen**.
4. **Daten aktualisieren:** Vor H3 in Studio Daten → `Tische` → **Aktualisieren**, damit die Spalte `Gesperrt` bekannt ist (gibt es seit Phase 0).
5. **Rückfall:** Anhang A enthält die Fassung vor dem Umbau (Export 08.10.). Ganz zurück nur in umgekehrter Reihenfolge (H7 → H1).
6. **YAML:** Arbeitest du mit YAML (`… → Ansichtscode`), nimm die englischen Formeln aus `handy_bloecke.json` (Feld `yaml`, mit `=` davor).

@@ H0
**Vorab-Test, 2 Minuten:** wie in der Desktop-App (Paket F2, Abschnitt 3), diesmal **in der Handy-App**, weil die Datenquelle dort eine eigene Verbindung ist.
1. Textbeschriftung `lblTestErstellt`, `Text`:
```
"Erstellt: " & Text(First(Tischbuchungen).Erstellt; "dd.mm.yyyy hh:mm")
```
2. Schaltfläche `btnTestErstellt`, `OnSelect`:
```
ClearCollect(colTestErstellt; Filter(Tischbuchungen; Endzeit > DateAdd(Now(); -14; TimeUnit.Days)));; Notify(CountRows(colTestErstellt) & " Zeilen, Erstellt der ersten: " & Text(First(colTestErstellt).Erstellt; "dd.mm.yyyy hh:mm"); NotificationType.Information)
```
- Erwartung: Datum in beiden, mindestens 1 Zeile. Danach **beide löschen**.
- Rot bei `Erstellt` → mit `Created` probieren und an Claude Code melden. Der Plan wird dann neu erzeugt. Nicht selbst ersetzen.

@@ H1
**Was neu ist:** `Set(varFreigabeMinuten; 30)` und `Set(varFreigabeGrenze; …)` vor dem Laden von `colTische`.
**Danach:** OnStart ausführen.
**Test:** App-Prüfung ohne rote Fehler.

@@ H2
**Was neu ist:**
- Stornieren („Ja, stornieren“) und „Jetzt beenden“ prüfen vor dem Schreiben, ob die Buchung der angemeldeten Person gehört (`Lower(E-Mail)`).
- Meldung beim Beenden: „Andere können den Tisch wieder buchen“ statt „wieder frei“. Andere Apps sehen es erst beim nächsten Laden.
- **Warum:** `varBuchung` kommt heute nur aus den eigenen Listen. Die Prüfung schützt, falls das später anders wird, und entspricht der Desktop-App.

**Test:** eigene Buchung stornieren → „Buchung storniert.“. Laufende eigene Buchung „Jetzt beenden“ → „Buchung beendet …“.

@@ H3
**Was neu ist:**
- `ddTisch.Items` zählt nur **aktive** Buchungen als belegt. Gesperrte Tische fehlen.
- Die Grenze wird beim Öffnen des Buchen-Tabs (Tab-Knopf, „Zum Buchen“) und beim Aktualisieren gesetzt.
- Aktualisieren lädt `colTische` neu (gesperrte Tische ohne Neustart).
- **Absichtlich nicht im Minutentakt:** Die Grenze ändert sich nur bei diesen Klicks. Sonst würde die Tischliste jede Minute neu abfragen, auch unsichtbar (gemessen: versteckte Steuerelemente fragen trotzdem ab). Eine alte Grenze ist vorsichtig: Es werden höchstens zu wenige Tische als frei gezeigt.

**Test:**
- In SharePoint eine Testzeile anlegen (Tisch X, Beginn vor 1 Std, CheckedIn = Nein). `Erstellt` ist dann „jetzt“: 30 Min warten oder `varFreigabeMinuten` per Testknopf auf 1 setzen (Testknopf danach löschen).
- Tab „Buchen“ öffnen, heute, die Zeit der Testzeile → Tisch X steht in der Liste.
- Tisch Y in `Tische` auf Gesperrt = Ja → Aktualisieren → Tisch Y fehlt.

@@ H4
**Was neu ist:**
- **Vorprüfungen** als Collections, verfallene Buchungen entfernt (`colBuchBelegt`, `colBuchIch`).
- **Neu: gesperrter Tisch** → Meldung (falls jemand vor dem Aktualisieren bucht).
- **Nachprüfung pro Klick eindeutig:** untere Grenze um die Sekunden seit Mitternacht verschoben, wie in Desktop-Nachtrag 4. Sonst ist sie wortgleich zur Vorprüfung und könnte aus dem Zwischenspeicher kommen.
- Die Nachprüfung entfernt verfallene Buchungen und die zusätzlich geholten, früher endenden Zeilen. Danach entspricht sie genau der alten. **Kein Fehlalarm mehr bei verfallenen Buchungen.**
- Die Erfolgsmeldung erinnert ans Einchecken.

**Test:** Auf den Tisch der verfallenen Testzeile buchen → „Gebucht: … Bitte bis 30 Minuten nach Beginn einchecken.“, **keine** „Achtung“-Meldung. Gesperrten Tisch (Studio-Vorschau ohne Aktualisieren) → Meldung.

@@ H5
**Was neu ist:**
- Vorprüfungen ohne verfallene Buchungen.
- Eigene verfallene Buchung → „verfallen“, kein Verlängern.
- **Nachprüfung eindeutig und ohne verfallene oder früher endende Zeilen.** Die vorhandene Rücknahme greift damit nur noch bei echten gleichzeitigen Buchungen.

**Test:** Eigene laufende Buchung, die eine verfallene fremde Buchung desselben Tisches überlappt (Testzeile) → +1 Std → „Buchung verlängert.“, **keine** Rücknahme.

@@ H6
**Was neu ist:**
- **B5:** eigene Variable `varCheckinID`, nicht mehr `varBuchungID` (die der Verwalten-Dialog nutzt).
- Frisch lesen. Fenster ab 30 Min vor Beginn bis zur **Frist**.
- Vor dem Check-in prüfen, ob der Tisch schon an jemand anderen vergeben ist.
- Nachprüfung (eindeutig): angekommen? Gleichzeitig neu vergeben?
- **B8:** Die Knopfanzeige rechnet mit `varJetzt` (`tmrJetzt`, jede Minute). Der Knopf wird also zur richtigen Zeit aktiv und nach der Frist grau.
- Status „Verfallen“ (grau) in Karte und Knopf.

**Test:** Buchung in 1 Std → Knopf grau. Ab 30 Min vor Beginn aktiv → „Eingecheckt.“. Verfallene Testzeile (eigene) → Status „Verfallen“, Knopf grau. Doppeltipp → eine Meldung.

@@ H7
**Was neu ist:** Startliste ab 06:00 (heute ab der laufenden halben Stunde, nicht vor 06:00). Neu ist eine **Vorgabe**: heute die erste mögliche Zeit, an anderen Tagen 08:00. Bisher nahm die Liste den ersten Eintrag, das wäre 06:00.
**Test:** Morgen → 08:00 vorgeschlagen, Liste ab 06:00.

@@ offen
## 6. Offen, später, Hinweise
- **`App.OnError` (neu im Export):** Die Formel zeigt bei **jedem** nicht abgefangenen Fehler „Die Verbindung zu SharePoint hat nicht geklappt …“, auch bei Formelfehlern. Die Fehlersuche wird dadurch schwer. Vorschlag (optional): `Notify("Fehler: " & FirstError.Message; NotificationType.Error)`. **UNSICHER**, ob die englischen Meldungen für Kollegen verständlich sind. Entscheidung bei Josias.
- **Startlisten mit `Now()`** (`ddDatum`, `ddStart`): Sie veralten, wenn die App stundenlang offen bleibt. Speichern prüft aber „Vergangenheit“ frisch. `varJetzt` dort einzusetzen würde die Listen jede Minute neu bauen und kann die Auswahl zurücksetzen. Deshalb bewusst nicht.
- **QR-Check-in am Tisch** (`Param("tisch")`) wäre der nächste sinnvolle Schritt gegen Einchecken von zu Hause. Eigenes Konzept nach dem Go-Live.
- **Rechte „nur eigene Elemente“:** Die Handy-App schreibt als angemeldete Person. Das passt.

@@ testbogen
## 7. Testbogen
| ✓ | Test | Ergebnis |
|---|---|---|
| ☐ | H0 Vorab-Test, Test-Steuerelemente gelöscht | |
| ☐ | H1 App-Prüfung, OnStart ausgeführt | |
| ☐ | H2 eigene Buchung stornieren / beenden | |
| ☐ | H3 Liste zeigt Tisch mit verfallener Buchung, gesperrter Tisch fehlt | |
| ☐ | H4 Buchen über verfallene Buchung ohne „Achtung“, gesperrt → Meldung | |
| ☐ | H5 Verlängern über verfallene Buchung ohne Rücknahme | |
| ☐ | H6 Knopf aktiv/grau nach Zeit, Einchecken, „Verfallen“, Doppeltipp | |
| ☐ | H7 Startzeiten 06:00, Vorgabe 08:00 | |
| ☐ | Gegenprobe Desktop: dieselbe Testzeile zeigt dort dasselbe (grün, buchbar) | |
| ☐ | Testknopf gelöscht, `Set(varFreigabeMinuten; 30)` in `App.OnStart`; veröffentlichen, erst dann teilen | |
