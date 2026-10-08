# Prüfung Paket F (08.10.2026)

## 1. Eigene Prüfung (Claude Code)
- **Maschinell** (`werkzeuge/paket_f.py`, Ergebnis `pruefung.txt`): 0 Fehler. Geprüft werden:
  - Klammern und Rückübersetzung deutsch → englisch, keine Kommentare.
  - Steuerelemente bekannt oder neu angelegt. Jede gelesene `var`/`col` wird irgendwo gesetzt.
  - `varFreigabeGrenze` wird in jeder Verhaltensformel vor dem Gebrauch gesetzt. Das Panel setzt die Grenze beim Öffnen.
  - Die alte Ladezeile steht an 0 Stellen, die neue an 14.
  - Alle 6 Schreibstellen haben die Zweifach-Sperre und die neue Ladezeile.
  - Storno: liest `varStornoID`, Eigentümerprüfung in beiden Armen, Mehrfach-Storno nur eigene.
  - **Jede einzelne Abfrage** auf `Tischbuchungen` (42, auch mehrzeilige) wendet die Freigabe-Regel lokal an oder ist mit Grund ausgenommen.
- **Mutationstest der Prüfung:** Sechs absichtliche Fehler wurden eingebaut, alle sechs hat die Prüfung erkannt:
  1. `RemoveIf` beim Verlängern fehlt.
  2. Eine Ladestelle vergessen.
  3. Storno liest wieder `varSelectedBuchung`.
  4. Grenze im Panel nicht gesetzt.
  5. `RemoveIf` in der Nachlese fehlt.
  6. Eigentümerprüfung fehlt.
- **Selbst gefunden:**
  - Bei einer Notbuchung durch Michael kann die Person **nicht einchecken** (fremdes Element). Das Betriebshandbuch v2 sagt deshalb: CheckedIn = Ja beim Anlegen.
  - Risiko „explizite Spaltenauswahl“: Wird `Erstellt` nicht geladen, verliert nur „spät gebucht“ die Schonfrist. Steht als U7 mit Test im Dokument.

## 2. Unabhängige Prüfung (Prüf-Agent, 08.10.)
Der Prüfer hat den Endstand selbst aufgebaut: Export + Gesamtplan + Paket F, 2.127 Properties. „Vorher“-Fassungen und Rückübersetzung sind identisch. **Kein kritischer Befund.** Alle 13 Befunde und was daraus wurde:

| Nr | Schwere | Befund | Erledigt |
|---|---|---|---|
| 1 | mittel | Z-Order: „Nach vorne bringen“ hebt nur eine Ebene, `tmrAktualisieren` liegt darüber. Dann trifft „Ja“ den Hintergrund | F2-Text: **Ganz nach vorne bringen**, Prüfung in der Strukturansicht |
| 2 | mittel | Leeres `varFreigabeMinuten` (Studio vor OnStart) macht jede begonnene Buchung sofort verfallen | Überall `Coalesce(varFreigabeMinuten; 30)`. F1: „OnStart ausführen“ |
| 3 | mittel | Test U7 „um hh:20 für hh:00 buchen“ geht in der Desktop-App nicht (Startliste rundet auf) | U7 neu: Monitor `$select` enthält `Created`. Praxistest über Handy-App oder vorher geöffneten Dialog. Kurzfassung/Regel präzisiert |
| 4 | niedrig–mittel | F3-Test behauptete, `Erstellt` sei bei SharePoint-Testzeilen „alt genug“ | korrigiert (Erstellt = jetzt, Testmodus) |
| 5 | niedrig–mittel | Testmodus durch Ändern von `App.OnStart` ist gefährlich, falls so veröffentlicht | Testknopf `btnTestFreigabe`, OnStart unverändert, Löschen im Testbogen |
| 6 | niedrig | Nach dem Check-in fehlte die Nachlese bei gleichzeitiger Neuvergabe | Nachlese + Fehlermeldung in F7 eingebaut |
| 7 | niedrig | „Schützt bei falsch gehender Uhr“ war zu stark formuliert | U3 und F7 ehrlich: verhindert Doppelbelegung, nicht zu frühen Verlust |
| 8 | niedrig | `First(colKachel)` unsortiert → Popup zeigt evtl. die spätere Buchung | nach `Startzeit` sortiert |
| 9 | niedrig | „Auschecken → sofort frei“ stimmt für andere nicht ganz (nächste halbe Stunde, Anzeige bis 5 Min) | Texte angepasst (Dokument, Kurzanleitung, Mail) |
| 10 | niedrig | Erinnerung nur einmal und nur im Dashboard | Texte eingeschränkt. Zweite Erinnerung bewusst nicht gebaut (kein Nerven) |
| 11 | niedrig | Handbuch: Überlappungsregel ungenau, Auschecken vor Beginn. Verlängern prüfte „zwei Tische zur selben Zeit“ nicht (vorbestehend aus G3) | Handbuch korrigiert. **Verlängern prüft jetzt auch die eigenen Buchungen** (`colVerlIch`, Meldung „Du hast in dieser Zeit schon einen anderen Tisch gebucht.“) |
| 12 | niedrig | „Vergessener Gesamtplan-Schritt wird mit erledigt“ führt in die Irre | Satz ersetzt: Paket F setzt den vollständigen Gesamtplan voraus |
| 13 | niedrig | `varVerlNaechste` wechselt den Typ → Zwischenfehler zwischen den zwei Properties möglich | Hinweis in F6 |

Danach erneut maschinell geprüft: 0 Fehler. Alle 6 Mutationen werden weiter erkannt.
