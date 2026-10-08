# Nachtrag 1 zum Gesamtplan (08.10.): Feedback und Änderungen

> An den Chat, der Josias durch den Gesamtplan führt. Bitte vollständig lesen, im Vault neben `GESAMTPLAN.md` ablegen und ab sofort beachten. Bei Widerspruch gilt dieser Nachtrag vor `GESAMTPLAN.md`.

## Kurzfassung
- Eine unabhängige Durchsicht hat vier Probleme gefunden. Claude Code hat alle vier gegen Plan und Exporte nachgeprüft: **alle stimmen**.
- **Schritt G-F (Flow „Freigabe ohne Check-in“) entfällt.** Josias will keine Freigabe per Flow. Claude Code baut die Freigabe gerade **in der App** neu (Paket F, kommt als eigenes Dokument). Den Flow **nicht** anlegen.
- **G4 (Stornieren) hat einen Fehler**, der eine fremde Buchung löschen kann. G4 darf eingefügt werden, aber die App **nicht veröffentlichen**, bevor der Storno-Fix aus Paket F drin ist.
- **G5 (Einchecken)** ändert sich mit Paket F noch einmal. Einfügen ist in Ordnung, Paket F ersetzt die Property später vollständig.
- Die **Handy-App** repariert ein anderer Chat. Phase 8 hier nicht ausführen.
- Phase 0 und alle übrigen Schritte laufen weiter wie geplant.

## Die vier Befunde und was daraus folgt

### 1. Stornieren kann eine fremde Buchung löschen (G4)
- Die Frage „Diese Buchung wirklich stornieren?“ ist nur ein kleines Kästchen. Der Rest der App bleibt klickbar.
- Klickt man bei offener Frage auf eine Grundriss-Kachel, setzt `btnHitArea` die Variable `varSelectedBuchung` auf die Buchung dieser Kachel, eventuell die eines Kollegen.
- „Ja, stornieren“ liest die ID erst beim Klick und löscht dann **diese** Buchung. Solange die Rechte „nur eigene Elemente“ (G-R) nicht gesetzt sind, klappt das.
- **Fix (kommt in Paket F):** ID beim Öffnen der Frage festhalten. Vor dem Löschen prüfen, dass die Buchung der angemeldeten Person gehört. Ein Hintergrund über den ganzen Bildschirm sperrt alle anderen Klicks.
- **Bis dahin:** G4 einfügen ist in Ordnung, testen nur mit eigenen Testbuchungen. **Nicht veröffentlichen.**

### 2. Der Freigabe-Flow löscht ungewollt (G-F)
- **Spät gebucht:** Eine Buchung darf ab der laufenden halben Stunde beginnen. Wer um 09:29 für 09:00 bucht, wäre beim nächsten Lauf gelöscht worden.
- **Auschecken:** Danach steht `Checkedin` wieder auf 0, und der Flow hätte die Buchung gelöscht.
- **Folge:** Der Flow fällt ganz weg. Die Freigabe kommt in die App (Paket F). **G-F überspringen.**
- Passt die Kurzanleitung oder Go-Live-Mail zur Freigabe nicht mehr, liefert Paket F den neuen Text.

### 3. Handy-App mit bekannten Fehlern
- Die Prüfbefunde B1–B11 vom 07.10. sind nicht in der veröffentlichten Handy-App (Export geprüft: kein `tmrJetzt`, „Jetzt beenden“ ohne Korrektur).
- **Folge:** Die Handy-App macht ein anderer Chat. **Phase 8 hier überspringen.** Die Handy-App erst teilen, wenn der andere Chat fertig ist und die Freigabe-Regel aus Paket F auch dort gilt.

### 4. Umfang
- Josias hat entschieden: Die Größe ist kein Problem, solange es für alles fertigen Code gibt. **Es bleibt beim ganzen Plan.**
- Die Ergänzungen aus dem Interview (G4-Dialog, G8, G14, G25, G26) sind nur maschinell geprüft. Darauf beim Testen besonders achten und jeden Test aus dem Plan wirklich ausführen.

## Kleinigkeiten (bitte beim jeweiligen Schritt beachten)
- **Go-Live-Mail:** nicht „ab 14.10. neu buchen“, sondern „**ab sofort** in der App Tische für den 14.10. und später buchen“. Das verteilt die Buchungen auf mehrere Tage.
- **Notbuchungen durch Michael:** Mit „nur eigene Elemente“ (G-R) zählt in SharePoint der **Ersteller**, nicht die Spalte `Person`. Legt Michael eine Buchung für jemanden an, kann diese Person sie in der App weder stornieren noch verlängern. Das macht dann Michael. Gehört ins Betriebshandbuch.
- **Teams-Chat „Tischbuchung – Hilfe“:** Den richtet der Plan nicht ein. Entweder Josias legt ihn in Phase 0 an, oder in Kurzanleitung und Mail steht stattdessen „Mail an Josias“.

## Reihenfolge ab jetzt
1. Phase 0 wie geplant.
2. Phase 1: G1–G7 einfügen und testen. G4 nur mit eigenen Testbuchungen. **Danach nicht veröffentlichen.**
3. Phase 2: G-F **überspringen**. G8 und G-R wie geplant.
4. Phasen 3–7 wie geplant.
5. Phase 8 (Handy) **überspringen**.
6. Sobald Paket F da ist: Paket F einfügen (Storno-Fix und Freigabe in der App), testen, **dann** veröffentlichen.
