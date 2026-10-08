# CLAUDE.md – Tischbuchungs-App (Power Apps Canvas, SharePoint)

Stand: 07.10.2026 (Sitzung Claude Code im Cloud-Repo `tischbuchung-app`). Löst die `CLAUDE.md` aus `quellen/2026-10-07_ClaudeCode_Paket/` ab (bleibt als alte Fassung erhalten). Kennzeichnung: **belegt** (Export/Dokument), **gemessen** (Monitor/Test), **geschlussfolgert**, **UNSICHER**.

## 1. Rahmen
- **Josias** (Werkstudent Digitalisierung, Technoform) ist der einzige Entwickler. Er fügt **jede Formel selbst** in Power Apps Studio ein. Claude liest nur Exporte und bearbeitet nie die App, die SharePoint-Listen oder Flows.
- Josias gibt alle Freiheiten unter zwei Bedingungen: **dokumentieren** und **nichts kaputt machen**. Handeln statt fragen, begründete Annahmen kennzeichnen. Fragen nur, wenn es fachlich bei Josias liegt.
- Prüfkette: eigene Prüfung → unabhängiger Prüf-Agent → App-Prüfung in Studio → Josias’ Tests.
- Stil der Übergaben (von Josias ausdrücklich gelobt): Kurzfassung zuerst. Je Schritt `Steuerelement.Property`, vollständiger Block, Test, Rückfall. Originale im Anhang. Alles maschinell aus dem Export erzeugt und geprüft. Deutsch mit Umlauten, kurz.
- Desktop-App „Tischbuchung“ (1366 × 768), Go-Live 14.10.2026. Handy-App „Tischbuchung Handy“ ist ein eigenes Vorhaben (gleiche Listen).
- Berechtigungs- und Tenant-Themen gehen an **Michael** (IT-Admin).

## 2. Ordner in diesem Repo
| Ordner | Inhalt | Regel |
|---|---|---|
| `quellen/2026-10-07_Wissenspaket/` | Josias’ Wissenspaket vom 07.10.: Übergaben, Gesamtaufgaben, Export-ZIPs (Desktop + Handy), Handy-Doku, Hintergrund | **nur lesen**, nie ändern |
| `quellen/2026-10-07_ClaudeCode_Paket/` | ältere Claude-Code-Übergabe (06.10., vor L2): alte CLAUDE.md, `tools/build.py`, `monitor.py` | nur lesen |
| `werkzeuge/` | eigene Python-Werkzeuge (siehe 3) | |
| `arbeit/<datum>_<thema>/` | Ergebnisse, datiert. **Alte Fassungen nie überschreiben**, neue Version = neue Datei/neuer Ordner | |
| `arbeit/_entpackt/` | entpackte Exporte (aus den ZIPs erzeugt, nicht eingecheckt) | |

Monitor-Dateien (`PowerAppsTraceEvents_*.json`, 23 MB) sind nicht im Repo, nur bei Josias und im Upload. Ihre Auswertung steht in `quellen/…/01_AKTUELL/00_UEBERGABE_an_Chat_PaketK_2026-10-07.md` Abschnitt 4.

## 3. Werkzeuge (immer `python3 -I`)
- `werkzeuge/app.py`: Export-ZIP → `.msapp` → `arbeit/_entpackt/…`. `App`-Klasse mit allen Properties (`"Steuerelement.Property"` → Formel englisch), Eltern, Typ und Pfad. Dazu `to_de()`/`from_de()`, `klammern_ok()`. Geprüft: liest dieselben 1.994 Properties wie Claude Codes `props_de.json` (die einzigen Abweichungen sind Anführungszeichen-Reste des PowerShell-Lesers).
- `werkzeuge/paket_k_v2.py`: erzeugt Paket K v2 aus dem Export. Bricht ab, wenn ein Anker nicht genau passt. Prüft Klammern, Rückübersetzung, Namen, Variablen, Sperre und Ladezeile an allen Schreibstellen → `arbeit/2026-10-07_PaketK_v2/bloecke.json`, `pruefung.txt`.
- `werkzeuge/doc_paket_k_v2.py` + `werkzeuge/paket_k_v2_text.md`: erzeugen `UEBERGABE_PaketK_v2.md`.
- **Nach einem neuen Export:** ZIP nach `quellen/<datum>…/` legen, Pfad in `app.py` anpassen, beide Skripte neu laufen lassen.

## 4. Formelregeln (alle schon einmal verletzt oder gemessen)
- Deutsch: `;` trennt, `;;` verkettet, `,` Dezimal. **Immer die ganze Property.** Keine Kommentare in Verhaltensformeln (in `App.Formulas` erlaubt).
- `With()`-Felder werden gleichzeitig ausgewertet. Abhängiges verschachteln.
- Lookup schreiben `{Id: …; Value: …}`, Person mit vollem Satz (Claims, Department, DisplayName, Email, JobTitle, Picture), ohne `'@odata.type'` (belegt 06.10.).
- Patch/Remove nur auf einen **frisch** gelesenen Datensatz (`LookUp` direkt davor). Eine Variable nie mit zwei Record-Typen füllen.
- **Doppelklick:** `DisplayMode`-Sperre allein reicht **nicht** (gemessen 06.10. in der Handy-App, E-07). Jede Schreibstelle braucht `If(!varIsLoading && (IsBlank(varSperreBis) || Now() >= varSperreBis); …; Set(varSperreBis; DateAdd(Now(); 2; TimeUnit.Seconds));; Set(varIsLoading; false))`.
- Werte in Filter-Prädikaten von Verhaltensformeln über **globale Variablen** übergeben (Handy-App E-06: so delegierbar).
- Delegation SharePoint: `=` auf Text/Lookup/Person.Email/DateTime ja, `<`/`>` auf DateTime ja, auf ID nur `=`. `in`, `IsBlank`, `Not` im Filter nicht. Statt `CountRows(Filter(…)) > 0` besser `!IsBlank(LookUp(…).ID)` (BD-27).
- Unsichtbar ≠ nicht berechnet: Versteckte Steuerelemente fragen trotzdem ab (gemessen). Abfragen hinter `If(<Dialog offen>; …)` stellen oder ganz vermeiden.
- `Set(var; false)` setzt keine Checkbox zurück → `Reset(control)`. `Fill` wird bei `DisplayMode.Disabled` nicht angezeigt (DisabledFill).
- Die L2-Ladezeile (`colGrundriss`) gehört an **jede** Schreibstelle und ans **Ende** von `App.OnStart`.
- Mehrarmiges `If` mit Anweisungsketten funktioniert bei `powerfxv1 = false` (in der Handy-App in Betrieb, belegt).

## 5. Fakten aus dem Export (07.10.2026, veröffentlicht, enthält L2)
- Eine Screen `Screen1`, 189 Steuerelemente, 1.994 Properties. Beide Apps haben dieselben App-Einstellungen (`Properties.json`, belegt).
- Listen: `Tischbuchungen` (`Tisch` Lookup, `Person`, `Startzeit`, `Endzeit`, `CheckedIn` (intern `Checkedin`), `SerienID` Text read-write filterbar eq, `Titel`), `Tische` (`Titel`, `Geschoss` Auswahl, 34 Zeilen: OG 16, UG 18 inkl. „Big Table“), toter Raumcode auf `Räume`/`Raumbuchungen`.
- **Dialoge richtig zugeordnet:** `conVerwaltenDialog` (`varSelectedBuchung`, `varZeigeVerwalten`) wird vom **Dashboard** geöffnet (`galTischbuchungenHeute > btnVerwalten`). Eine Grundriss-Kachel öffnet nur das Details-Popup (`btnHitArea` → `varZeigeDetails`). Tab-Dialog: `conBuchungen > conVerwaltenDialog_1` (`varSelectedBuchungTab`, `varZeigeVerwaltenTab`). Buchungsdialog aus dem Grundriss: `conBuchungDialog > btnSpeichern` (`varSelectedTisch`). Panel: `conTischBuchungenPanel` (`ddTischePanel`, `dpDatumTischePanel`, `ddStartTischePanel`, `ddEndTischePanel`, `dpWiederholenBis_1`, `btn5Std`, `btn9Std`).
- `varWiederholenModus` wird nur auf „Wochentage“ gesetzt, der Zweig „Taeglich“ ist tot (BD-24, belegt). `varTagSa`/`varTagSo` haben keine Schalter.
- `chkAuswahl.X` liest schon `btnVerwalten_2` → BD-18 ist erledigt (belegt).
- Zwei Designs in einer App: Buchungsdialog (Grundriss) im Power-Apps-Standard-Graublau `RGBA(100,118,132)`, Panel/Tabs im Markenblau `#171496`. Grün `#00A96B` hat fünf Bedeutungen. Zehn Grautöne. Paket L vereinheitlicht den Buchungsdialog.
- Werkzeuge für Paket L: `werkzeuge/paket_l.py`, `doc_paket_l.py`, `paket_l_text.md`.
- Handy-App-Regeln (von Josias bestätigt, `05_HANDY_APP/FRAGEN_AN_JOSIAS.md` V1–V9): nie über 22:00, Einchecken ab 30 Min vor Beginn bis Ende, keine zwei Tische zur selben Zeit, Big Table nicht buchbar, Stornieren mit Bestätigung, keine Buchung in der Vergangenheit.

## 6. Stand der Arbeit
- **Erledigt (Josias, veröffentlicht):** L2 Grundriss-Performance (Serie 11 Termine ~4,7 s statt ~101 s, gemessen), Sammel-Patch in `btnSpeichern`, Mehrfach-Stornieren neu.
- **Paket K v2 (07.10., dieses Repo), nicht eingefügt:** `arbeit/2026-10-07_PaketK_v2/UEBERGABE_PaketK_v2.md`, 22 Schritte und 55 Properties, unabhängig geprüft (Befunde eingearbeitet). Ersetzt v1. Inhalt: Zweifach-Sperre an allen 8 Schreibstellen. Verwalten-Dialoge mit einmal berechneter Grenze (B0 an der Wurzel, 24 Abfrage-Properties weg). Verlängern/Stornieren/Einchecken frisch + `IfError` + Nachlese. Beide Speichern-Knöpfe gleich (Sammel-Patch, `SerienID`, Nachlese, Person-Prüfung, Vergangenheit, eine Meldung). Tischauswahl nur freie Tische. Kleinigkeiten BD-10/12/25/26. Entscheidungen E1–E7 mit Vorschlag nach den Handy-Regeln.
- **v1 (Claude Code, 07.10.) hatte einen echten Fehler:** Die K5-Sperre nur per `DisplayMode` hält nicht (siehe 4).
- **Kritische Analyse (08.10.):** `arbeit/2026-10-08_Kritische_Analyse/ANALYSE_Stand_App.md`. Urteil: veröffentlichter Stand nicht go-live-fähig, mit Paket K v2 als Pilot realistisch. Größte Risiken: Betrieb (eine Person, keine Test-Umgebung), Mitbestimmung/Datenschutz (Namen sichtbar), fehlende Funktionen gegenüber GoBright (automatische Freigabe, Outlook, Räume, Auswertung).
- **Paket L (08.10.), nicht eingefügt, unabhängig geprüft (Befunde eingearbeitet):** `arbeit/2026-10-08_Kritische_Analyse/FEHLER_UMBAUPLAN_STIL_PaketL.md`, 57 Properties, nach Paket K v2 einzufügen (keine Überschneidung, maschinell geprüft). Behebt: Startzeit 22:00 erzeugt Buchung mit Ende 00:00 (F-L1), Dashboard-Liste unsortiert, unlesbare gedrückte Knöpfe, aktiver Tab unsichtbar, zufällige Profilfarbe, „Besetzt“ immer rot. Dazu Farben, Bedienelemente und Texte vereinheitlicht. Enthält Umbaupläne P1–P10 und ein Stil-Audit.

## 7. Backlog (nach Paket K v2)
1. Josias: Paket K v2 einfügen und testen (Testbogen im Dokument). Entscheidungen E1–E7 bestätigen.
2. Paket L einfügen (nach K v2). Entscheidung P2: Check-in mit automatischer Freigabe oder abschaffen.
3. P1 Grundriss: freie Restzeit belegter Tische buchbar machen (braucht `btnAndereZeit`, `lblBelegtHeute`). P3 Mitternachts-Timer. P4 Spalte „Gesperrt“ in `Tische`.
4. P8 Betrieb: eigene Umgebung/Lösung, Mitbesitzer, Test-Listen (mit Michael).
5. L4 Raumcode stilllegen + `App.OnStart`/tote Variablen aufräumen (erst nach Josias’ Bestätigung, Frage 11).
6. Bestätigungsdialog vor dem Stornieren (Handy V8), braucht ein neues Steuerelement.
7. Vorprüfung mit Alternativtischen (E-2). C1 zeigt schon „an x von y Tagen belegt“.
8. Mehrfach-Verlängern (E-3), eigenes Konzept.
9. Buchungen-Tab „manchmal leer“ (Frage 15): Trace im Moment des Fehlers nötig.
10. Rechercheauftrag App Store / Zusammenarbeit PC–Handy (`06_RECHERCHE/`), nicht ausgeführt.

## 8. Fehler, die passiert sind (nicht wiederholen)
- Namen aus Briefings übernommen statt im Export geprüft (`ddEndeTischePanel`, `T.Aktiv`/`T.Standort` in `AUFGABE_UMBAU.md`).
- Teilersatz statt ganzer Property. Reihenfolge, die einen falschen Zwischenzustand erzeugt.
- Monitor-Dauern doppelt gezählt (`getRows` + `showGetRowsCount` paarweise; `time` = Ende der Antwort).
- Behauptungen als Fakt verkauft, die nur geschlussfolgert waren.
- Dialog falsch zugeordnet („Grundriss-Dialog“ ist der Dashboard-Dialog), dadurch ein nicht ausführbarer Test (v1 B3).
- Eine Messung aus der Schwester-App (Handy E-07) nicht übertragen. Erkenntnisse der Handy-App immer gegen die PC-App prüfen.
