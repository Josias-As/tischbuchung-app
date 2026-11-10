# EINSETZPLAN: abgestimmte Pakete (Tischbuchung Desktop, 10.11.2026)

Für Josias. Grundlage: **Export 10.11. 08:13** („echt“, App „Tischbuchung“, Desktop, zeichengleich mit 25.10.). Alle Pakete sind **der Reihe nach** auf diesen Export gelegt und zusammen geprüft (`werkzeuge/abstimmung.py`, 0 Fehler, Mutationstest 11 von 11 erkannt). In Studio nichts getestet. Kennzeichnung: **belegt**, **geschlussfolgert**, **UNSICHER**.

## Kurzfassung
- **Fünf Pakete, eine Reihenfolge, keine Überschneidung ohne Abstimmung:**

| Paket | Inhalt | Properties | neue Steuerelemente | Dokument | geprüft |
|---|---|---|---|---|---|
| **P0** Design-Korrektur | „Tisch Buchen“ blau, „Heute“ gedrückt lesbar | 7 | 0 | [`UEBERGABE_P0_Design.md`](P0_Design/UEBERGABE_P0_Design.md) | maschinell |
| **P1** Für andere buchen v2 | Für andere buchen, weicher Hinweis „Trotzdem“, Gastname in der Anzeige | 179 | 10 | [`UEBERGABE_FuerAndere_v2.md`](P1_FuerAndere_v2/UEBERGABE_FuerAndere_v2.md) | Logik unabhängig (Fassung 1), Stil maschinell |
| **P2** Nachtrag 5 | Stornieren mit Bestätigung, Nachholen S3b/F5/G25, Raumcode-Abfragen weg, Erinnerung per E-Mail, Tab lädt nur offen | 21 | 0 | [`NACHTRAG_5.md`](../2026-10-08_Nachtrag5/NACHTRAG_5.md) | unabhängig (08.10.) |
| **P3** Nachtrag 6 v2 | Verfallene Karte gesperrt, Knopf „Neu buchen“ | 32 | 1 | [`UEBERGABE_Nachtrag6_v2.md`](P3_Nachtrag6_v2/UEBERGABE_Nachtrag6_v2.md) | maschinell |
| **P4** Grundriss-Laden v2 | Positionen als benannte Formeln, Tische einmal laden, L5 Typ-Abgleich | 7 | 0 | [`UEBERGABE_GrundrissLaden_v2.md`](P4_GrundrissLaden_v2/UEBERGABE_GrundrissLaden_v2.md) | maschinell |

- **Jeder Block passt genau auf den Stand davor** (maschinell: das „Vorher“ jedes Blocks ist zeichengleich mit dem Stand nach den vorigen Paketen). Zusammen 243 verschiedene Properties und 11 neue Steuerelemente.
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

## 2. Dokumente zum Einfügen

| Paket | Dokument | Ordner |
|---|---|---|
| P0 Design-Korrektur | [`UEBERGABE_P0_Design.md`](P0_Design/UEBERGABE_P0_Design.md) | `P0_Design` |
| P1 Für andere buchen v2 | [`UEBERGABE_FuerAndere_v2.md`](P1_FuerAndere_v2/UEBERGABE_FuerAndere_v2.md) | `P1_FuerAndere_v2` |
| P2 Nachtrag 5 | [`NACHTRAG_5.md`](../2026-10-08_Nachtrag5/NACHTRAG_5.md) | `../2026-10-08_Nachtrag5` |
| P3 Nachtrag 6 v2 | [`UEBERGABE_Nachtrag6_v2.md`](P3_Nachtrag6_v2/UEBERGABE_Nachtrag6_v2.md) | `P3_Nachtrag6_v2` |
| P4 Grundriss-Laden v2 | [`UEBERGABE_GrundrissLaden_v2.md`](P4_GrundrissLaden_v2/UEBERGABE_GrundrissLaden_v2.md) | `P4_GrundrissLaden_v2` |

- **P2 Nachtrag 5:** Dokument vom 08.10. unverändert. Nur sein Abschnitt 3 (Testbogen) ist ersetzt durch Abschnitt 3 hier.
- **Ältere Fassungen** (Für andere buchen v1, Nachtrag 6 v1, Grundriss-Laden v1) **nicht mehr einfügen.** Sie bleiben zum Nachlesen erhalten.
- Design-Prüfung und Skizzen: [`DESIGN_PRUEFUNG.md`](DESIGN_PRUEFUNG.md), Ordner `design/`.

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

## 4. Rückfall
- **Ein Paket:** rückwärts in der Reihenfolge P4 → P3 → P1 → P2 → P0. Jedes Dokument hat die Originale im Anhang A, also den Stand direkt vor dem Paket.
- **P1 zurück:** vorher P3 zurück (P3 baut auf `btnHitArea.OnSelect` aus P1 auf). **P3 zurück:** vorher P4 L5 zurück oder P4 ganz.
- **Alles:** make.powerapps.com → App → Details → **Versionen** → Version vor dem Einfügen → Wiederherstellen. Oder die `.msapp`-Sicherung.
- Die Spalte `GastName` kann in jedem Fall bleiben.

## 5. Offene Punkte (blockieren nichts)
| Nr | Was | Vorschlag |
|---|---|---|
| O1 | **Check-in-Fenster:** Einchecken geht seit 25.10. ab 60 Min vor Beginn (`btnEinchecken`, Kachel). Die automatische Frage beim Start (`App.OnStart`, `colCheckinFrage`) und die Erinnerung im Timer kommen weiter erst ab **30 Min** (belegt) | So lassen: die Erinnerung soll kurz vorher kommen, nicht eine Stunde vorher. Willst du 60: 3 Zahlen, ich erzeuge die Blöcke |
| O2 | Kontaktzeile im Hinweis (Axel Krägelius / Norman Horn) | Text in `lblFbHinweis.Text` |
| O3 | **Handy-App** kennt `GastName` nicht: Gast-Buchungen blockieren dort den Buchenden zur selben Zeit, und dort gibt es keinen „Trotzdem“-Hinweis | von dir akzeptiert, Handy-Folge später |
| O4 | Check-in-Dialog zeigt den Gastnamen nicht (B9 aus der Prüfung) | kein Muss |
| O5 | Unabhängige Prüfung: P1 Logik ja (Fassung 1), P1 Stil, P3, P4, P0 und die Abstimmung nur maschinell | auf Wunsch eine Prüfung des Endstands |
| O6 | Stil-Audit D4 (Dropdown-Auswahlbalken graublau, 31 Stellen) | nicht Teil dieser Pakete |

## 6. Maschinelle Prüfung
`werkzeuge/abstimmung.py` legt P0 → P1 → P2 → P3 → P4 der Reihe nach auf den Export und prüft jedes Vorher und den Endstand. `werkzeuge/abstimmung_mutation.py` baut absichtlich Fehler ein: L5 fehlt, „Neu buchen“ ohne Gast-Rücksetzung, Vorher eines N5-Blocks passt nicht, Speichern ohne Sperre, `colNeuIch` ohne GastName, Ladezeile an einer Stelle anders, Panel liest ein Feld, das die Liste nicht hat, doppelter Steuerelement-Name, Positionen noch als Sammlung in OnStart, Freigabe-Grenze 60 statt 30, gewählte Buchung aus einer Sammlung ohne GastName. Ergebnis: 11 von 11 erkannt.

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
