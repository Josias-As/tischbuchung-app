# FORTSCHRITT: L2 Grundriss-Performance (Tischbuchung)

Quelle der Wahrheit: Export vom 06.10.2026 (`export_06.10\msapp_src\Src`, nur lesen). Formeln: `UEBERGABE_Grundriss_L2_v0.3.md`.

## 07.10.2026 Vorprüfung (Claude Code)
- ZIP und `.msapp` entpackt nach `C:\tischbuchung_work\export_06.10\` (nur gelesen, nichts gepackt). Zeilenzahlen wie in der Übergabe: App 139, Screen1 4.359.
- Python fehlt auf dem Rechner, deshalb `pruefe_formeln.ps1` (PowerShell-Port, gleiche Logik). Ergebnis: **15 Schritt-A-Formeln = Export + Ladezeile** (6 davon mit zusätzlichem `;;` vor der Ladezeile, gewollt), **5 Originale (Anhang 1) = Export exakt**. Abweichungen: 0. (gemessen am Export)
- Schritt 0 (Versionsverlauf: letzte Speicherung 06.10. 14:12 Berlin) steht aus.

## 07.10.2026 L2 abgeschlossen und veröffentlicht
- A1–A15, B1–B5 eingefügt, Test A ok (134 Einträge, keine Formelfehler, `colGrundriss` gefüllt). Veröffentlicht laut Josias; Export `export_07.10_veroeffentlicht` enthält L2.
- Gemessen (Trace 4): Serie 11 Termine ~4,7 s statt ~101 s, 96 statt 1.020 Abfragen, 0 Kachel-Abfragen. Mehrfachstornierung 33 Buchungen ~9 s fehlerfrei (Trace 5, 1 Ausreißer 8 s).

## 07.10.2026 Paket K (PAUSIERT auf Wunsch von Josias)
- Entwurf: `UEBERGABE_PaketK_v1.md`, erzeugt von `erzeuge_konzept.ps1` aus `export_07.10_veroeffentlicht\props_de.json` (vorher `exportiere_props.ps1`). Begleittext: `konzept_text.md`.
- Inhalt: A1 K1, A2/A3 DisplayMode Speichern; B1–B4 Verlängern neu + DisplayMode; C1/C2 K4.1 + Meldungen; E2 Mehrfachauswahl ausblenden (optional). K4.2 bewusst verworfen (Begründung im Dokument).
- Maschinelle Prüfung: keine Fehler (Anker je 1x, Klammern, Kommas, Namen, nur erlaubte Zeilen geändert).
- Eigene Durchsicht: A1, B1, C1, C2 gelesen und stimmig. B3 nicht einzeln gelesen (wortgleich zu B1 laut Generator, Namensprüfung ok).
- **Offen:** unabhängige Prüfung durch zweiten Agenten wurde gestartet und **abgebrochen** (kein Ergebnis). Vor dem Einfügen nachholen. Nichts aus Paket K ist eingefügt.

## Schritte
| Zeit | Steuerelement.Property | Ergebnis | Fehlertext |
|---|---|---|---|
| | Schritt 0: Versionsverlauf + .msapp-Export | offen | |
| | A1 App.OnStart | offen | |
| | A2 dpAnsichtsDatum.OnChange | offen | |
| | A3 ddStockwerk.OnChange | offen | |
| | A4 Icon1.OnSelect | offen | |
| | A5 Icon1_1.OnSelect | offen | |
| | A6 Image6.OnSelect | offen | |
| | A7 btnHitArea_1.OnSelect | offen | |
| | A8 btnSpeichern.OnSelect | offen | |
| | A9 btnSpeichernTischePanel.OnSelect | offen | |
| | A10 btnVerlängern_1.OnSelect | offen | |
| | A11 btnStornieren_1.OnSelect | offen | |
| | A12 btnStornierenKlein.OnSelect | offen | |
| | A13 btnVerlängern.OnSelect | offen | |
| | A14 btnStornieren.OnSelect | offen | |
| | A15 btnEinchecken.OnSelect | offen | |
| | Test A | offen | |
| | B: Rectangle1.Fill, Circle1.BorderColor, Circle1.BorderStyle, Circle1.Fill, Label1.Text | offen | |
| | Test B | offen | |
