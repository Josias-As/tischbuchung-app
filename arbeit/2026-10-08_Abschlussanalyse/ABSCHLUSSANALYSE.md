# Abschlussanalyse beider Apps (08.10.2026, Exporte 14:25/14:26)

Grundlage:
- Export „PCAppfertig“ (Desktop, 08.10. 14:26) und Export „App8.10.fertig“ (Handy, 08.10. 14:25), abgelegt in `quellen/2026-10-08_Fertig/`.
- Abgleich Property für Property gegen den gemeldeten Stand.
- Zwei unabhängige Tiefenprüfungen: `pruefbericht_desktop.md`, `pruefbericht_handy.md`.
- Monitor-Messungen vom 07.10. und App-Prüfung (`AppCheckerResult.sarif`) aus beiden Exporten.

Kennzeichnung: **belegt**, **gemessen**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung: Sind wir fertig?
**Im Code fast, im Betrieb noch nicht.**
- In keiner App gibt es einen kritischen Fehler im Code (beide Prüfungen).
- Alle Schreibstellen haben die Zweifach-Sperre, lesen frisch und prüfen nach. Es gibt keine Testreste. Die Freigabe-Regel ist in beiden Apps gleich (30 Min).
- **Als Pilot sind beide go-live-fähig.** Vorher fehlen noch:
  1. **Desktop-Nachtrag 5 einfügen.** Der Export zeigt: S3b, `btn5Std.Fill` (F5) und ein G25-Teil fehlen, obwohl sie als eingefügt gemeldet waren (**belegt**). Dazu kommen die Storno-Bestätigung (Auftrag 2a) und zwei Funde der Prüfung (N6, N7).
  2. **Handy H8 einfügen.** Ohne H8 erkennt die Handy-App keinen Tageswechsel, wenn sie über Nacht offen bleibt. Dann gilt „Heute“ noch für gestern, und „Morgen“ bucht für heute (**belegt** aus den Formeln, mittel).
  3. **Tische umbenennen, nur mit Grundriss-Positionen.** Die Desktop-App ordnet jede Kachel über den **Tischnamen** einer festen Position zu (`colTischPositionen`/`colTischPositionenUG` in `App.OnStart`, **belegt**). Nach „neuer Tisch, ab Desk 13 alles um 1 verschoben“ stehen die Kacheln am falschen Platz, und der neue Tisch steht oben links. **Josias muss sagen, welches Geschoss es betrifft und wo der neue Tisch steht.** Dann erzeuge ich `App.OnStart` neu.
  4. **Zwei Tests, die nur echte Zeit klären** (Testbogen Nachtrag 5, Punkte 14 und 15):
     - Spätbuchung mit echten 30 Minuten: Kommt `Erstellt` in den Desktop-Sammlungen an?
     - Rückmeldungen: Erfolgsmeldungen statt „nicht angekommen“.
  5. **Betrieb:**
     - Lese-Recht auf beiden Listen bleibt „alle Elemente“.
     - Vertretung für Michael ab 12.10.
     - Gerätetest Handy.
     - Check-in-Pflicht ganz oben in die Mail.

## 1. Was die Änderungen gebracht haben

### Desktop (Export 07.10. → 08.10.)
| | Vorher (07.10.) | Jetzt (08.10.) | Beleg |
|---|---|---|---|
| Abfragen beim Start | 50, davon 36 auf `Raumbuchungen` | etwa 12–15. Mit Nachtrag 5 (N4, N5, N7) etwa 5 weniger, kein Raumcode mehr | gemessen bzw. geschlussfolgert |
| Delegationswarnungen | 56 | 10, alle im stillgelegten Raumcode | App-Prüfung |
| App-Prüfung gesamt | 134 Hinweise | 92 Hinweise, keine Fehler | App-Prüfung |
| Doppelklick | `DisplayMode` allein, hielt nicht | Zweifach-Sperre an allen 8 Schreibstellen | belegt |
| Stornieren | konnte eine fremde Buchung löschen | frisch, nur eigene, Nachlese. Mit N1/N2 auch mit Bestätigung | belegt |
| Freigabe nicht eingecheckter Buchungen | gab es nicht | in der App, nach 30 Min, nichts wird gelöscht | belegt |
| Grundriss veraltet | konnte beliebig alt sein | sperrt sich nach 2 Min bis zum Aktualisieren | belegt |
| Abfragen ohne Tippen | Timer gab es nicht. Mit F8 wären es 3 je 5 Min gewesen | 0, außer der gedrosselten Check-in-Erinnerung | belegt |
| Buchen | 2–7 Abfragen mehr (Refresh) | ohne Refresh (Nachtrag 4) | gemessen (Handy), belegt |

**Verschlechterungen:**
- Die Dashboard-Listen aktualisieren sich nicht mehr von selbst. Das hat Josias akzeptiert.
- Beim Verwalten werden mehr Abfragen fällig (frisch lesen, Nachlese), je Aktion 6–8. Das ist der Preis für die Sicherheit, die Dauer ist nicht gemessen.
- Das Panel macht je Eingabe etwa 5 Abfragen (geschlussfolgert). Das war vorher ähnlich.

### Handy (07.10. → 08.10. 14:25)
**Besser:**
- Alle Prüfbefunde aus `fix_pruefung.js`.
- Freigabe-Regel, Gesperrt und Einchecken bis zur Frist (H1–H7).
- Zeitumstellung in Buchen, Verlängern, Beenden und Einchecken.
- ID aus dem Patch.
- Der kritische Weg ist geschlossen: Einchecken auf eine verfallene, neu vergebene Buchung geht nicht mehr.

**Etwas mehr Abfragen:** je 1 beim Buchen und Einchecken, 1–2 beim Aktualisieren. Das ist der Preis für die eindeutige Nachprüfung, gemessen wird beim Gerätetest.

## 2. Alle Befunde und was damit passiert
| Nr | App | Schwere | Was | Maßnahme |
|---|---|---|---|---|
| A1 | PC | mittel | S3b fehlt: „Verfallen“ erst nach dem nächsten Laden (belegt) | Nachtrag 5 **N4** |
| A2 | PC | niedrig | `btn5Std.Fill` alt: Der Knopf sieht belegt aus, ist aber bedienbar (belegt) | **N4** |
| A3 | PC | niedrig | Raumcode: noch 4 Abfragen beim Start (gemessen 07.10.) | **N4**, **N5** |
| A4 | PC | mittel | Check-in-Erinnerung sucht über den Anzeigenamen (UNSICHER, ob er abweicht) | **N6** |
| A5 | PC | mittel | Tab-Liste fragt beim Start und nach jeder Aktion ab, auch unsichtbar. Beendete Buchungen bleiben stehen | **N7** |
| A6 | PC | Auftrag | Stornieren ohne Rückfrage | **N1–N3** |
| A7 | PC | mittel, UNSICHER | `Erstellt` in den Desktop-Sammlungen nicht nachgewiesen. Fehlt es, verfallen spät gebuchte Tische zu früh (Doppelvergabe möglich) | **Test 14** (Muss). Die Handy-App hat dasselbe Muster belegt (K1) |
| A8 | PC | hoch, wenn es eintritt | Grundriss-Positionen hängen am Tischnamen | **Muss**, Angaben von Josias nötig (siehe Kurzfassung 3) |
| A9 | Handy | mittel | Kein Tageswechsel bei offener App | **H8** |
| A10 | beide | mittel | Lese-Recht „nur eigene“ macht alle Tische frei. Betroffen sind Handy `ddTisch`, `btnBuchen`, `btnVerl1/2`, `btnEincheckenH` und PC 25 Properties, darunter alle Ladestellen (belegt). Josias' Besitzerkonto sieht den Fehler nicht | Betriebshandbuch v4: **Lesen immer alle** |
| A11 | beide | niedrig | Unterschiede: Einchecken „Älterer gewinnt“ nur am Handy. Leeres `Erstellt` nur am Handy abgesichert | nach Go-Live gleichziehen. Auswirkung nur bei Uhrabweichung an der Frist bzw. wenn A7 fehlschlägt |
| A12 | PC | niedrig | Zeitumstellung: Buchungen für Sonntag, 25.10. landen 1 Std zu früh (`T.Value + varNeuStartZeit`) | betrifft nur diesen Sonntag. Hinweis im Betriebshandbuch, nach Go-Live beheben |
| A13 | Handy | niedrig | `usenonblockingonstartrule` ist **an** (belegt), der Handy-Chat schreibt „aus“ | keine falsche Buchung (Prüfung), nur die Notiz korrigieren |
| A14 | Handy | niedrig | Big Table über `Gesperrt` steuern wäre falsch: Am PC wäre er dann auch im Grundriss gesperrt (G0.3) | beim Namen bleiben |
| A15 | beide | mittel | Tischname als Schlüssel der Kollisionsprüfung. Bei Umbenennung im Betrieb oder zwei gleichen Titeln: Doppelbuchung | vor dem Go-Live umbenennen, „Eindeutige Werte erzwingen“ für `Titel` |
| A16 | Liste | später | keine Indizes, ab 5.000 Zeilen scheitern Abfragen | jetzt beim Leeren Indizes auf `Startzeit`, `Endzeit`, `Tisch`, `Person` |
| A17 | PC | niedrig | Ein entsperrter Tisch bleibt in offenen Sitzungen gesperrt (`Tische` wird nicht neu geladen) | Betriebshandbuch: App neu laden |
| A18 | PC | niedrig | Aktualisieren-Symbole ohne Sperre (nur per Tastatur auslösbar), Refresh nach Patch doppelt, Check-in-Dialog nicht modal, vergangene Buchungen verwaltbar, 11 ungenutzte Variablen, Texte „---“ | nach Go-Live |
| A19 | Handy | niedrig | `lblTischH.Width` überlappt den Status um 58 px. App-Beschreibung „Testphase“ | Handy-Chat: `Parent.Width - 360`, Beschreibung ändern |
| A20 | Handy | niedrig, UNSICHER | `ddDatum.Items` über die Zeitumstellung: Erscheint der 25.10. doppelt? | 1-Min-Test (Handy-Bericht H-9) |
| A21 | PC | niedrig | Timer1 heißt nicht `tmrAktualisieren`, `icoAktualisierenGrundriss` zusätzlich | passt so (siehe 4) |

## 3. Muss vor dem 14.10. (Checkliste)
| ✓ | Was | Wer |
|---|---|---|
| ☐ | Desktop: Nachtrag 5 (N1–N7) einfügen, Testbogen Abschnitt 3 komplett, **Test 14 Spätbuchung** | Josias + Desktop-Chat |
| ☐ | Handy: H8 einfügen, testen (Gerät über Nacht offen lassen oder Uhrzeit-Test unten) | Handy-Chat |
| ☐ | Tische: Geschoss und Lage des neuen Tisches an Claude Code → neues `App.OnStart` mit Positionen. **Erst dann** in SharePoint umbenennen, von oben nach unten (Desk 17 → 18 zuerst), danach „Eindeutige Werte erzwingen“ | Josias |
| ☐ | Bestehende Buchungen löschen, danach Indizes anlegen (Listeneinstellungen → Indizierte Spalten) | Josias |
| ☐ | Rechte: Lesen auf `Tischbuchungen` und `Tische` = alle Elemente. Mit einem **normalen** Kollegen-Konto prüfen, ob fremde Buchungen im Grundriss erscheinen | Josias, Michael |
| ☐ | Gerätetest Handy mit einem Kollegen, Gegenprobe am PC (gleicher Tisch, gleiche Zeit) | Josias |
| ☐ | Sicherung `.msapp` beider Apps, App-Prüfung, veröffentlichen, Handy-Beschreibung ändern | Josias |
| ☐ | Vertretung ab 12.10. eintragen (Betriebshandbuch v4) | Josias |
| ☐ | Go-Live-Mail (v4) mit der Check-in-Pflicht ganz oben. **Erste Woche** (Vorschlag, Josias entscheidet): Viele kennen die Pflicht noch nicht, also werden viele Buchungen verfallen. Bei Bedarf `varFreigabeMinuten` in **beiden** Apps gleich hochsetzen (z. B. 60) und nach einer Woche zurück | Josias |

## 4. Antworten an den Desktop-Chat
- **(1) 17. Ladestelle:** `icoAktualisierenGrundriss.OnSelect` ist **zeichengleich** mit `Icon1_1.OnSelect` in der S2-Fassung, mit Stempel (**belegt**). **Behalten**, nichts zu tun. Es liegt unter der Sperrfläche (Ebene 7 unter 8). Gesperrt aktualisiert also nur der große Knopf, entsperrt geht beides. Optional: `AccessibleLabel` = `"Grundriss aktualisieren"`.
- **(2a)** Nachtrag 5 N1–N3. Einzel-Storno ebenfalls mit Bestätigung, Begründung in der Kurzfassung dort. Diff gegen den **Export**, der der S2-Stand ist.
- **(2b)** Der Testbogen steht in Nachtrag 5, Abschnitt 3, mit `Timer1` statt F8. Neu sind Test 14 (Spätbuchung, Muss) und Test 15.
- **(2c)** Sicherung, App-Prüfung und Veröffentlichen sind Testbogen Punkt 16.
- **(2d)** `KURZANLEITUNG_und_GoLive_Mail_v4.md` und `BETRIEBSHANDBUCH_Michael_v4.md` im Ordner `arbeit/2026-10-08_Nachtrag5/`. Enthalten: Satz „spätestens beim nächsten Bedienen“, Listen ohne automatisches Aktualisieren, Stornieren mit Bestätigung, Rechte nach Josias' Entscheidung, Lesezugriff nie einschränken.
- **(2e) Grundriss-Sperre am Handy: nein, bewusst nur Desktop.** Die Handy-App hat keinen Grundriss. Sie zeigt freie Tische in `ddTisch`, und `btnBuchen` prüft vor und nach dem Schreiben frisch. Ein veralteter Stand kann dort nicht zu einer falschen Buchung führen, nur zu einer Ablehnungsmeldung.
- **Achtung, Abweichungen im Export:** S3b, F5 an `btn5Std.Fill` und G25 an `recBuchungDanach1.Visible` fehlen trotz „passt“. Bitte nach dem Einfügen von N4 einmal neu exportieren, dann prüfe ich erneut maschinell.

## 5. Antworten an den Handy-Chat
- **H8 Tageswechsel (neu, bitte einfügen):** 4 Properties in `handy_h8_bloecke.json`.
  - `App.OnStart` (deine zusammengeführte Fassung mit Profilfarbe + `Set(varHeute; Today())`).
  - `tmrJetzt.OnTimerEnd` (bei neuem Tag `varHeute`, `Reset(ddDatum)`, `varNeuLaden + 1`).
  - `ddDatum.Items` und `lblHeuteTitel.Text` (`Coalesce(varHeute; Today())`).
  - Test: in Studio einen Testknopf mit `Set(varHeute; DateAdd(Today(); -1; TimeUnit.Days))` tippen. Nach höchstens 1 Minute (`tmrJetzt` ohne `Duration` = Standard 60 s, geschlussfolgert) zeigen Titel und Datumsliste wieder heute, und die Listen laden neu. Testknopf löschen.
- **Lese-Recht:** festgehalten (Betriebshandbuch v4). Bestätigt und erweitert: Am Handy sind `ddTisch`, `btnBuchen`, `btnVerl1/2` und `btnEincheckenH` betroffen. `galHeute` ist **nicht** betroffen, es filtert auf die eigene Person.
- **Freigabe-Regel abgeglichen:** gleich in beiden Apps. 30 Min, Beginn und Erstellt, 06:00 und 22:00, Vergangenheit, zwei Tische, Gesperrt, Einchecken bis zur Frist (belegt).
  - Unterschiede: „Älterer gewinnt“ und leeres `Erstellt` sind nur am Handy abgesichert. Die Desktop-App zieht nach dem Go-Live nach. Dafür gibt es keine neuen Handy-Blöcke.
  - Die Startliste beginnt am Handy bei der laufenden halben Stunde, am PC bei der nächsten. Der Big Table ist am Handy nie buchbar. Beides ist gewollt.
- **Big Table:** beim Namen lassen, **nicht** über `Gesperrt` steuern. Sonst wäre er auch am PC im Grundriss gesperrt, und laut Josias bleibt er dort buchbar.
- **Aufräum-Flow:** Laut Doku löscht er nur Zeilen, deren Ende mehr als 7 Tage zurückliegt. Das ist für beide Apps unkritisch.
- **B1–B11:** Alles, was dazu im Repo dokumentiert ist, ist in deiner App enthalten. Einzige Quelle ist `fix_pruefung.js`: B1/B4, B5/B8, B10 und die vier Verlängern-Teile. Achtung: Die Nummern „B5/B6/B7“ in Umbauplan v2, Zeile 3, meinen etwas anderes (ID aus Patch, Zeitumstellung). Auch das ist erledigt.
- **„Nicht blockierender OnStart“ ist im Export an** (`usenonblockingonstartrule: true`, belegt). Die Prüfung findet dadurch keine falsche Buchung, bitte nur die Notiz korrigieren.
- **Kleinigkeiten:**
  - `lblTischH.Width` = `Parent.Width - 360` (überlappt sonst den Status um 58 px).
  - App-Beschreibung „Testphase …“ vor dem Teilen ändern.
  - Tische vor dem Go-Live umbenennen (siehe Muss-Liste, auch der PC braucht neue Positionen).

## 6. Bewusst offen, nach dem Go-Live
- PC: „Älterer gewinnt“ beim Einchecken, leeres `Erstellt` nie verfallen, Zeitumstellung in G6/F4.
- PC: Refresh nach Patch entfernen, Panel-Abfragen senken, Aktualisieren-Symbole mit Sperre.
- Check-in-Dialog modal, vergangene Buchungen nicht verwaltbar, ungenutzte Variablen, Barrierefreiheit (G26).
- Handy: Abfragen nur im sichtbaren Tab (vom Handy-Chat bewusst verworfen). `galHeute` aus `galMeine` ableiten.
