# Nachtrag 2 zum Gesamtplan (08.10.): Paket F ist fertig

> An den Chat, der Josias durch den Gesamtplan führt. Im Vault neben `GESAMTPLAN.md` und Nachtrag 1 ablegen. Gilt ab sofort.

## Kurzfassung
- **Paket F** (`UEBERGABE_PaketF.md`) ersetzt Schritt **G-F (Flow)**. Es enthält:
  - **Freigabe in der App:** Nicht eingecheckte Buchungen verfallen nach 30 Min. Nichts wird gelöscht, es gibt keinen Flow.
  - **Storno-Fix:** richtige Buchung, nur eigene, Hintergrund sperrt.
  - **Check-in-Frage** beim Öffnen und alle 5 Minuten.
  - **Auschecken** beendet die Buchung.
  - **Verlängern** prüft „zwei Tische zur selben Zeit“.
- Umfang: 8 Schritte (F1–F8), 44 Properties, 1 neues Steuerelement (`btnStornoHintergrund`). Maschinell geprüft (0 Fehler) und unabhängig geprüft (kein kritischer Befund, alle Befunde eingearbeitet).

## Reihenfolge
1. Gesamtplan wie bisher: Phase 0, Phasen 1–7, **G-F weglassen**, Phase 8 (Handy) weglassen.
2. **Paket F, Schritte F1 → F8**, genau wie im Dokument. Wichtig:
   - Nach F1 in Studio **OnStart ausführen**.
   - In F2 `conStornoFrage` **„Ganz nach vorne bringen“**.
   - Für die Tests den **Testknopf** aus dem Testbogen verwenden (nicht `App.OnStart` ändern) und **vor dem Veröffentlichen löschen**.
3. Testbogen Paket F abarbeiten, dann **veröffentlichen**.
4. Statt der alten Texte gelten `KURZANLEITUNG_und_GoLive_Mail_v2.md` und `BETRIEBSHANDBUCH_Michael_v2.md`.
5. `AUFTRAG_Handy_Freigabe.md` an den **Handy-Chat** weitergeben. Die Handy-App erst teilen, wenn die Regel dort auch gilt.

## Für den Testbogen des Gesamtplans
- G5 (Einchecken) wird durch F7 ersetzt: Einchecken nur noch bis 30 Min nach Beginn. Den alten G5-Test „bis zum Ende“ nicht mehr erwarten.
- Go-Live-Checkliste ergänzen:
  - In `App.OnStart` steht `Set(varFreigabeMinuten; 30)`.
  - Kein Testknopf mehr in der App.
  - `conStornoFrage` liegt ganz oben.
