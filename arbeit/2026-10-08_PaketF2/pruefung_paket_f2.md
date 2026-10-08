# Prüfung Paket F, Fassung 2 (08.10.2026)

## Maschinell (`werkzeuge/paket_f2.py`)
Ergebnis: 0 Fehler (siehe `pruefung.txt`). Geprüft auf dem Endstand im Studio (angenommener Ist-Stand + F2):
- Keine Verweise auf G4-, G8- oder G14-Teile.
- Alte Ladezeile an 0 Stellen.
- Jedes Patch/Remove steht hinter der Zweifach-Sperre.
- Storno: Eigentümerprüfung vor dem Remove.
- Auschecken: Frage-Zweig schreibt nicht und sperrt 1 s. Das Rücksetzen steht hinter der Sperre. Der Statusabgleich kommt vor dem Patch.
- Jede der 42 Abfragen auf `Tischbuchungen` ist einzeln eingeordnet.
- Notfassung (Anhang D) frei von der Freigabe, ohne F1 lauffähig.

## Unabhängig (Prüf-Agent, 08.10.)
Der Prüfer hat den Ist- und Endstand selbst nachgebaut. Diffs, Ausgangsstand und Verweise stimmen.

| Nr | Schwere | Befund | Erledigt |
|---|---|---|---|
| 1 | hoch | Doppelklick auf „Auschecken“ bestätigt sofort. Rücksetzen vor der Sperre verliert die Frage | Frage-Zweig setzt `varSperreBis` +1 s. `Set(varAuscheckFrageID; 0)` steht jetzt hinter der Sperre. Neue Prüfung im Generator |
| 2 | hoch | Veralteter Anzeigestatus (Galerie) beendet die Buchung ohne Rückfrage oder checkt nach der Frage ein | Abgleich `Coalesce(frisch.CheckedIn) <> Coalesce(Anzeige.CheckedIn)` → Anzeige aktualisieren, Meldung, nichts schreiben. Neue Prüfung |
| 3 | hoch | Notweg „F1 + F2 zuerst“ nicht unabhängig (F1 gehört zur Freigabe, F2 liest `varFreigabeMinuten`) | Kurzfassung korrigiert: F1–F8 gehören zusammen. **Anhang D:** Storno-Notfassung ohne Freigabe, maschinell geprüft |
| 4 | mittel | Rechte: Bearbeiten enthält „Listen verwalten“ (Einstellungen änderbar), `Tische.Gesperrt` änderbar | Frage 5 und Betriebshandbuch v3: Vererbung unterbrechen, Mitwirken auf `Tischbuchungen`, Lesen auf `Tische`, Test ergänzt |
| 5 | niedrig | Abfragetabelle teils falsch (Storno Dashboard/Tab, Einchecken, F4 gegen Studio) | korrigiert |
| 6 | niedrig | Nachlese per `LookUp` gleich der Frischlesung | als U10 aufgenommen (G3 nutzt dasselbe Muster) |
| 7 | niedrig | Rückfall nur in umgekehrter Reihenfolge | Rückfall-Abschnitt ergänzt |
| 8 | niedrig | „spätestens 5 Min“ zu stark | „meist innerhalb von 5 Minuten“ |
| 9 | niedrig | Vorab-Test 2 bei 0 Zeilen irreführend | Hinweis „mindestens 1 Zeile, sonst -14“ |
| 10 | niedrig | Prüfdatei fehlte; Kurzanleitung „Dashboard → Auschecken“ ungenau; Storno ohne Bestätigung weicht von Handy-Regel V8 ab; Timer-Ladung kann eine gleichzeitige überschreiben; Frage auch kurz vor Ende | Datei angelegt; Text korrigiert; Storno ohne Bestätigung ist **Josias’ Entscheidung** (ein „zweites Tippen“ wie beim Auschecken ginge ohne neues Steuerelement, auf Wunsch); Timer als U11 (harmlos); Frage kurz vor Ende bleibt (harmlos) |

Danach erneut maschinell geprüft: 0 Fehler.
