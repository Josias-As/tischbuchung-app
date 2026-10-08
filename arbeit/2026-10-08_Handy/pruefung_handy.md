# Prüfung Umbauplan Handy-App (08.10.2026)

## Maschinell (`werkzeuge/handy_plan.py`)
Ergebnis: 0 Fehler (`pruefung.txt`). Geprüft wird:
- Klammern, Rückübersetzung, Steuerelemente und Variablen.
- Jedes Patch/Remove hinter der Sperre.
- Eigentümerprüfung vor Remove/Patch.
- Nachprüfungen eindeutig und ohne verfallene Buchungen.
- Jede der 14 Abfragen auf `Tischbuchungen` eingeordnet.

## Unabhängig (Prüf-Agent, 08.10.)
Der Prüfer hat die Ausgangslage Zeichen für Zeichen gegen den Export vom 08.10. geprüft (alle 17 „vorher“ gleich). Er hat bestätigt, dass die neuen Nachprüfungen exakt gleichwertig zu den alten sind (ohne verfallene Zeilen). **Kein kritischer oder hoher Befund.**

| Nr | Schwere | Befund | Erledigt |
|---|---|---|---|
| M1 | mittel | Begründung „Fehlalarm beim Buchen / falsche Rücknahme beim Verlängern“ stimmt für die heutige App nicht: Die Vorprüfung blockt vorher. Diese Fehler entstünden erst bei halbem Umbau | Kurzfassung korrigiert: echter Grund ist das Einchecken auf verfallene, neu vergebene Buchungen. Das andere ist als „Falle beim Umbau“ beschrieben |
| M2 | mittel, UNSICHER | Leeres `Erstellt` (Spalte nicht geladen) würde als „lange her“ gelten → zu frühe Freigabe | `!IsBlank(Erstellt)` in der Regel bzw. `IsBlank(X.Erstellt)` als aktiv. Leer zählt nie als verfallen. Test mit echten 30 Minuten im Testbogen |
| N1 | niedrig | Tests H3/H5 so nicht ausführbar | H3: Testzeile mit Ende in der Zukunft. H5: zuerst einchecken |
| N2 | niedrig | Prüfdatei fehlte | diese Datei |
| N3 | niedrig | Startprompt H1–H6 statt H1–H7 | korrigiert |
| N4 | niedrig | H7 = Phase 8 des Gesamtplans | Hinweis „nicht doppelt einfügen“ |
| N5 | niedrig | „Buchbar: gleich“ stimmt nicht (Handy rundet ab, Desktop auf) | Tabelle präzisiert |
| N6 | niedrig | Rückfall H1 allein → rote Fehler | Hinweis ergänzt |
| N7 | niedrig | Einchecken bei gleichzeitiger Doppelbuchung sperrt auch den Älteren | ID-Regel: Ältere Buchung gewinnt (`ID >= varCheckinID` entfernt) |
| N8 | niedrig | Grenze in Buchen/Verlängern/Einchecken löst eine Abfrage der unsichtbaren Liste aus | eigene `varListeGrenze` nur für die Liste |
| N9 | niedrig | „Meine“ zeigt „Verfallen“ nicht | als „später“ notiert |
| N10 | niedrig | `Gesperrt` im Export noch nicht im Schema | H0 prüft `Gesperrt` nach dem Aktualisieren |

**Hinweis für die Desktop-App (Paket F2), vom Prüfer außerhalb des Auftrags:**
- Die Nachprüfung beim Einchecken (`colCheckinAndere` nach dem Patch) ist dort wortgleich zur Vorprüfung, also anfällig für den Zwischenspeicher.
- M2 (leeres `Erstellt`) und N7 (Älterer gewinnt) gelten dort genauso.
- **Vorgemerkt für die nächste F2-Fassung.** Beide Apps sollen gleich bleiben.

Danach erneut maschinell geprüft: 0 Fehler.
