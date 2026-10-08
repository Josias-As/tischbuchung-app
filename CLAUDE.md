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
- `werkzeuge/gesamtplan.py` + `doc_gesamtplan.py`: Gesamtplan aus Export + K v2 + L + Interview-Entscheidungen (prüft: jede Property genau einmal, Schreibstellen mit Sperre/Ladezeile, Variablen, neue Steuerelemente).
- `werkzeuge/paket_f.py` + `doc_paket_f.py` + `paket_f_text.md`: Paket F auf den Endfassungen des Gesamtplans (liest `gesamtplan_bloecke.json`). Prüft zusätzlich jede einzelne Abfrage auf `Tischbuchungen` (Freigabe-Regel oder begründete Ausnahme). Mutationstest bestanden (6/6).
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

## 5a. Entscheidungen von Josias (Interview 08.10., `arbeit/2026-10-08_Interview/ANTWORTEN.md`)
- **Harter Umstieg am 14.10.**, der GoBright-Vertrag endet. Es gibt keinen Parallelbetrieb.
- Automatische Freigabe nicht eingecheckter Buchungen nach **30 Min**. ~~nur löschen, Flow unter Josias’ Konto~~ → **geändert 08.10.: kein Flow, Freigabe in der App, nichts löschen (Paket F).** Josias: „kein Fan von der Freigabe mit Flow, erscheint unsicher“.
- Regeln E1–E7: Claude entscheidet → Vorschläge aus K v2. Frühester Start **06:00**, Ende 22:00, Serien Mo–Fr.
- Namen bleiben sichtbar. Raumcode bleibt (nicht löschen). Liste: nur eigene Elemente bearbeiten.
- Josias darf Spalten und Steuerelemente anlegen. Nur Josias sperrt Tische. Big Table bleibt für alle über den Grundriss buchbar.
- Test mit 3–5 Kollegen möglich. Nach Paket K kommen ein Export und ein Trace. Vertretung: Michael/IT. Arbeitsweise: alles nach Wichtigkeit, möglichst vor dem Go-Live, nicht sparen.
- Tisch-Anzeigen (GoBright-Hardware über ein Gateway) fallen mit dem Vertragsende weg. Modell unbekannt, eine Anbindung ist zu recherchieren.

## 6. Stand der Arbeit
- **Erledigt (Josias, veröffentlicht):** L2 Grundriss-Performance (Serie 11 Termine ~4,7 s statt ~101 s, gemessen), Sammel-Patch in `btnSpeichern`, Mehrfach-Stornieren neu.
- **Paket K v2 (07.10., dieses Repo), nicht eingefügt:** `arbeit/2026-10-07_PaketK_v2/UEBERGABE_PaketK_v2.md`, 22 Schritte und 55 Properties, unabhängig geprüft (Befunde eingearbeitet). Ersetzt v1. Inhalt: Zweifach-Sperre an allen 8 Schreibstellen. Verwalten-Dialoge mit einmal berechneter Grenze (B0 an der Wurzel, 24 Abfrage-Properties weg). Verlängern/Stornieren/Einchecken frisch + `IfError` + Nachlese. Beide Speichern-Knöpfe gleich (Sammel-Patch, `SerienID`, Nachlese, Person-Prüfung, Vergangenheit, eine Meldung). Tischauswahl nur freie Tische. Kleinigkeiten BD-10/12/25/26. Entscheidungen E1–E7 mit Vorschlag nach den Handy-Regeln.
- **v1 (Claude Code, 07.10.) hatte einen echten Fehler:** Die K5-Sperre nur per `DisplayMode` hält nicht (siehe 4).
- **Kritische Analyse (08.10.):** `arbeit/2026-10-08_Kritische_Analyse/ANALYSE_Stand_App.md`. Urteil: veröffentlichter Stand nicht go-live-fähig, mit Paket K v2 als Pilot realistisch. Größte Risiken: Betrieb (eine Person, keine Test-Umgebung), Mitbestimmung/Datenschutz (Namen sichtbar), fehlende Funktionen gegenüber GoBright (automatische Freigabe, Outlook, Räume, Auswertung).
- **Paket L (08.10.), nicht eingefügt, unabhängig geprüft (Befunde eingearbeitet):** `arbeit/2026-10-08_Kritische_Analyse/FEHLER_UMBAUPLAN_STIL_PaketL.md`, 82 Properties (L10–L13 in zweiter Prüfung, siehe `pruefung_paket_l_2.md`), nach Paket K v2 einzufügen (keine Überschneidung, maschinell geprüft). Behebt: Startzeit 22:00 erzeugt Buchung mit Ende 00:00 (F-L1), Datum/Zeit im Buchungsdialog bleiben vom letzten Öffnen stehen → Buchung am falschen Tag (F-L11, L13), Dashboard-Liste unsortiert, unlesbare gedrückte Knöpfe, aktiver Tab unsichtbar, zufällige Profilfarbe, „Besetzt“ immer rot. Dazu Farben, Bedienelemente und Texte vereinheitlicht. Enthält Umbaupläne P1–P10 und ein Stil-Audit.

- **Selbstprüfung (08.10.):** `arbeit/2026-10-08_Kritische_Analyse/SELBSTPRUEFUNG.md`. K v2 + L = 137 Properties. **Muss vor Go-Live: 43** (K: 0, A1–A10, B1, B2, C2, D3; L: L1, L13), Soll 51, nach Go-Live 43. L12 zurückgezogen.

- **GESAMTPLAN (08.10.) = maßgeblich zum Einfügen:** `arbeit/2026-10-08_Gesamtplan/GESAMTPLAN.md`. Er ersetzt das Einfügen von K v2 und L einzeln: 26 App-Schritte, 253 Properties, jede genau einmal in ihrer Endfassung, 7 neue Steuerelemente (`conStornoFrage`, `lblStornoFrage`, `btnStornoJa`, `btnStornoNein`, `tmrAktualisieren`, `btnAndereZeit`, `lblBelegtHeute`). Dazu Phase 0 (Sicherung, Bestandsdaten, Spalte `Tische.Gesperrt`, Mail an Michael), Flow „Freigabe ohne Check-in“, Rechte, Handy-App 06:00 (2 Properties), Kollegentest, Go-Live-Checkliste, Rückfall, GoBright-Anzeigen. Erzeugt mit `werkzeuge/gesamtplan.py` + `doc_gesamtplan.py` + `gesamtplan_text.md`. Dazu gehören `START_PROMPT_fuer_Chat.md`, `BETRIEBSHANDBUCH_Michael.md` und `KURZANLEITUNG_und_GoLive_Mail.md`. **Interview-Ergänzungen (06:00, Gesperrt, Storno-Bestätigung, Timer, Andere Zeit, Raumcode ruhig, Barrierefreiheit, Handy) sind nur maschinell geprüft, nicht unabhängig.**

- **Feedback einer unabhängigen Durchsicht (08.10.)** zum Gesamtplan: alle 4 Punkte stimmten (Storno löscht evtl. fremde Buchung, Flow löscht spät Gebuchte/Ausgecheckte, Handy-App ohne B1–B11, Umfang). Josias: Größe egal, solange es fertigen Code gibt; Handy-App macht ein anderer Chat. `arbeit/2026-10-08_Gesamtplan/NACHTRAG_1_an_Chat_Feedback.md`.
- **Paket F (08.10.), nicht eingefügt:** `arbeit/2026-10-08_PaketF/UEBERGABE_PaketF.md`, nach dem vollständigen Gesamtplan einzufügen, ersetzt G-F. 8 Schritte, 44 Properties, 1 neues Steuerelement (`btnStornoHintergrund`). Regel: verfallen = `!CheckedIn && Startzeit <= varFreigabeGrenze && Erstellt <= varFreigabeGrenze` (Grenze = jetzt − `Coalesce(varFreigabeMinuten; 30)`), verfallene zählen überall als frei, nichts wird gelöscht. Server filtert nur Zeit/Tisch/Person, Ja/Nein und `Erstellt` lokal (ClearCollect + RemoveIf bzw. ForAll mit `Aktiv`). Ladezeile an 14 Stellen um `Erstellt` erweitert, Schema von `colGrundriss` per `DropColumns` gleich. Einchecken bis Frist, Auschecken = Ende jetzt, Check-in-Frage beim Start und im Timer, Verlängern prüft „zwei Tische“. Storno-Fix (`varStornoID`, Eigentümer mit `Lower()`, Vollbild-Hintergrund). Unabhängig geprüft, 13 Befunde eingearbeitet (`pruefung_paket_f.md`). Dazu `AUFTRAG_Handy_Freigabe.md` (für den Handy-Chat), `KURZANLEITUNG_und_GoLive_Mail_v2.md`, `BETRIEBSHANDBUCH_Michael_v2.md`, `NACHTRAG_2_an_Chat_PaketF.md`.

- **Nachtrag 3 (08.10.):** `arbeit/2026-10-08_Nachtrag3/NACHTRAG_3_Speichern_ohne_Refresh.md` (`werkzeuge/nachtrag3.py`). Das „erste Refresh“ in G6/F4 steht nicht vor dem Sammel-Patch, sondern im Zweig „nichts gebucht“. Entfernt, spart dort 2–7 Abfragen, bei erfolgreicher Buchung keine Änderung, Nachlese unberührt. Blöcke für G6 und F4. **Beim nächsten Neuerzeugen von Paket F (neue Fassung) gleich mit einbauen**, sonst bringt F4 das Refresh zurück. Idee (ungetestet): Nachlese über `SerienID = varSerienID` formen, dann wäre auch das Refresh vor der Nachlese verzichtbar.

- **Nachtrag 4 (08.10.), ersetzt Nachtrag 3:** `arbeit/2026-10-08_Nachtrag4/NACHTRAG_4_Nachlese_ohne_Refresh.md` (`werkzeuge/nachtrag4.py`). Speichern ganz ohne `Refresh(Tischbuchungen)`: Die Nachlese ist pro Klick eindeutig (`varNeuNachVon` = Beginn − Sekunden seit Mitternacht − 1), also kein Zwischenspeicher. Zählung über `SerienID` und Konflikt über Überlappung unverändert. Belege: Handy TB-1 (Liste zeigt die Buchung ohne Refresh, Nachlese anders geformt, gemessen), L2 eindeutige URL. Spart je Buchung 2 (Dialog) bis 7 (Panel) Abfragen. Test 2 (Liste ohne Aktualisieren) entscheidet. Rückfall Nachtrag 3. **Beim nächsten Neuerzeugen von Paket F gleich einbauen.**

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
- `Now()`/`Today()` in Datenformeln (Items/Default) werden nicht von selbst neu berechnet: Zeitpunkt beim Öffnen in eine Variable setzen (`varDialogJetzt`, `varPanelJetzt`) und damit rechnen (zweite Prüfung, 08.10.).
- Zustand von Eingaben beim erneuten Öffnen eines Dialogs nicht geprüft (F-L11: `DefaultDate` greift nur bei Änderung, ohne `Reset` bleibt die alte Eingabe stehen).
- Eine Messung aus der Schwester-App (Handy E-07) nicht übertragen. Erkenntnisse der Handy-App immer gegen die PC-App prüfen.
- Eine neue Sicherheitsabfrage (Storno-Rückfrage) ohne Hintergrund gebaut: Bei offener Frage blieb die App klickbar und eine globale Variable konnte sich ändern. Dialoge, die eine Aktion bestätigen, halten ihr Ziel in einer eigenen Variable fest und sperren den Rest.
- Einen Flow-Filter nicht gegen alle Wege durchgespielt, auf denen Daten entstehen (spät gebucht, ausgecheckt). Regeln gegen jeden Schreibweg prüfen.
- Tests geschrieben, die in der App so nicht ausführbar sind (Startliste rundet auf, `Erstellt` einer SharePoint-Testzeile ist „jetzt“). Jeden Test gegen die Eingabemöglichkeiten der App prüfen.
- Rechte „nur eigene Elemente“: zählt der **Ersteller**. Wer für andere anlegt, nimmt ihnen Einchecken, Stornieren und Verlängern.
