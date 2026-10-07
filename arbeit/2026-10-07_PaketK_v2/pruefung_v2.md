Ein unabhängiger Prüf-Agent hat v2 geprüft: frischer Kontext, nur Dateien und Prüfauftrag, eigene Skripte. Der vollständige Bericht liegt in `arbeit/2026-10-07_PaketK_v2/pruefung_v2_roh.md`. **Urteil: einfügebereit nach Korrekturen.** Ohne Befund blieben:
- Alle Originale sind zeichengleich mit dem Export.
- Eine eigene Rückübersetzung deutsch → englisch ergibt für alle Blöcke genau die Vorlage.
- Keine Variable wird mit zwei Typen gesetzt.
- `varIsLoading` wird auf jedem Ast zurückgesetzt.
- Die Grenze-Logik (A1–A5) ist gleichwertig zur alten Kollisionsprüfung, plus 22:00.
- Kappung, Wochentage und Aufräumblöcke in B1/B2 entsprechen dem Original.
- Alle Namen existieren, die Zuordnung „Dashboard-Dialog“ stimmt.

| Nr | Befund | Schwere | Umgang in dieser Fassung |
|---|---|---|---|
| F1 | C5 korrigiert nur `Label14.Text`, `Label14.Color` liest weiter das falsche Datum | Fehler | **behoben:** `Label14.Color` ist in C5 aufgenommen |
| R1 | C1: With-Werte im Server-Filter. In der Handy-App gemessen: Das erzeugt eine Delegierungswarnung | Risiko | **behoben:** Die Grenzen stehen direkt als Steuerelement-Ausdrücke im Filter (ganze Tage). Gleich umgestellt: C3/C4 (5/9 Std). Neue automatische Prüfung: Kein Server-Prädikat im Paket nutzt With-Werte (Anhang 2). Rest-Unsicherheit U-V3 |
| R2 | C1: Alias `X` heißt wie die Spalte `X` der Liste `Tische`, und `belegt`/`Belegt` unterscheiden sich nur in der Schreibweise | Risiko | **behoben:** Alias `Ti`, Name `belegtListe` |
| R3 | Schritt 0: Studio führt OnStart nicht neu aus. Ob `Now() >= Blank()` wahr ist, ist unsicher; die Begründung „2 s gesperrt“ war falsch | Risiko | **behoben:** Die Sperre fängt `IsBlank(varSperreBis)` ab. Die Startwerte stehen am Anfang von OnStart. „OnStart ausführen“ steht im Ablauf und im Test. Der Rückfall-Text ist korrigiert |
| H1 | Das Lade-Overlay erscheint jetzt auch bei Verlängern, Stornieren und Einchecken; D2 ändert den Warntext | Hinweis | im Dokument ergänzt (Kurzfassung, Test D2) |
| H2 | Die 2-s-Sperre gilt für alle Schreibknöpfe, nicht nur gegen den Doppelklick | Hinweis | in der Kurzfassung ergänzt |
| H3 | Nach „inzwischen belegt“ bleiben die Plus-Knöpfe grün | Hinweis | **behoben:** Die Grenze wird auf das alte Ende gesetzt, die Plus-Knöpfe werden grau |
| H4 | Das Datenzeilenlimit ist 1.000, nicht 500 | Hinweis | U-V4 korrigiert |
| H5 | „Stiller Tischwechsel ausgeschlossen“ ist zu stark | Hinweis | umformuliert, U-C1 bleibt |
| H6 | Die Nachlese könnte aus dem Zwischenspeicher kommen | Hinweis | **behoben:** `Refresh` steht jetzt vor der Nachlese (statt danach, also keine zusätzliche Abfragewelle) |
| H7 | `If` ohne Else liefert eine Tabelle (C1) | Hinweis | **behoben:** Bei geschlossenem Panel kommt eine typgleiche leere Tabelle (`FirstN(Table(…); 0)`) |
| H8 | Die Liste kennt „ich habe schon einen Tisch“ nicht | Hinweis | im Dokument erwähnt, bleibt so (Speichern prüft es) |
| H9 | `Tische` wird auch bei geschlossenem Panel gelesen | Hinweis | Satz eingeschränkt |
| H10 | Tests D1, C1(2) und D2 nicht aussagekräftig bzw. nicht ausführbar | Hinweis | alle drei Tests umgeschrieben |
| H11 | 47 der 134 Prüf-Einträge liegen auf ersetzten Properties | Hinweis | Erwartungswert (etwa 87 plus wenige) im Ablauf und im Testbogen |
| H12 | Lesefehler gilt als „gibt es nicht mehr“ bzw. „alles frei“ | Hinweis | als U-B3 aufgenommen, bleibt wie in der Handy-App |

Nach den Korrekturen sind Generator und maschinelle Prüfung neu gelaufen: 0 Fehler (Anhang 2). Die Korrekturen selbst wurden **nicht** noch einmal unabhängig geprüft. Das ist die nächste Stufe der Prüfkette: App-Prüfung in Studio und Josias’ Tests.
