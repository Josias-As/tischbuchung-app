# RETRO Analyse-Chat Tischbuchung (07.–13.10.2026)

Selbstprüfung der Claude-Code-Cloud-Sitzung `fafe6d49…` (Branch `claude/ziel-problematiken-verstehen-vspfp6`). Alle Zeiten in **UTC** (Transkript/Git). Ortszeit CEST = UTC + 2.
Kennzeichnung: **belegt** (Datei/Export, Pfad + Zeile/Zitat) · **gemessen** (Zahl aus Monitor/Test) · **berichtet** (jemand hat es gesagt, nicht geprüft) · **geschlussfolgert** · **UNSICHER**. Kosten in Klassen K1–K5, immer **geschätzt**.
Abkürzungen der Quellen: `T#n` = Zeile n im Transkript `~/.claude/projects/-home-user-tischbuchung-app/fafe6d49-1ca2-5d29-8a0f-ef9d848e481e.jsonl` (gezählt als JSONL-Zeile). Pfade relativ zum Repo.

## 0. Steckbrief
| Punkt | Inhalt | Kennz. / Quelle |
|---|---|---|
| Thema | Analyse, Umbaupläne und maschinell erzeugte Formelpakete für die Desktop-App „Tischbuchung“ und Pläne für die Handy-App „Tischbuchung Handy“. Ersatz für GoBright, Go-Live 14.10.2026 (harter Umstieg) | belegt, `CLAUDE.md` §1, §5a |
| Zeitraum | 07.10. 10:16 bis 13.10. 08:41 UTC, Retro 13.10. ab 17:01. 48 Commits, 3 Kontext-Zusammenfassungen (08.10. 07:49, 08.10. 13:21, 13.10. 08:21) | belegt, `git log`, T#1347, T#2791, T#4366 |
| Apps | Desktop „Tischbuchung“, App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. Handy „Tischbuchung Handy“, App-ID `e218702e-35cb-4dc8-813a-b9fd860c7f72` | belegt, `BETRIEBSHANDBUCH_Michael_v4.md` Z. 10; T#2616 |
| Exporte (Desktop) | 07.10. 09:14, 08.10. 14:26, 12.10. 07:26 (= 08.10. zeichengleich), 12.10. 11:52, 13.10. 09:59 (letzter Stand) | belegt, `quellen/…`, `werkzeuge/app.py` |
| Exporte (Handy) | 07.10., 08.10. 11:51, 08.10. 14:25, 12.10. 12:05 („handy echt“) | belegt, `werkzeuge/app.py` |
| Gelesen | Gesamtes Transkript (81 Nutzer-Nachrichten, 169 Antworttexte maschinell extrahiert, 3 Zusammenfassungen vollständig), `CLAUDE.md`, `git log`, alle Prüfberichte in `arbeit/**/pruefung*.md`, Abschlussanalyse, Exporte über `werkzeuge/app.py` | belegt |
| Nicht gelesen | Monitor-Traces (nicht im Repo, nur die Auswertung in den Übergaben), Josias’ Obsidian-Vault (aus der Cloud nicht erreichbar), Studio-Stand zwischen den Exporten, SharePoint-Listen und Rechte, Handy-Studio-Stand nach 12.10. 12:05. Rohberichte der Prüf-Agenten im Scratchpad früherer Kontexte (`analyse_desktop/BERICHT.md` u. a.) habe ich nicht erneut geöffnet, nur ihre Zusammenfassungen in `arbeit/2026-10-08_Abschlussanalyse/` und T#3279, T#3319, T#3448 | belegt (fehlt) |

## 1. Was diese Sitzung gemacht hat
**Bekommen (Eingänge):**
| Zeit (UTC) | Eingang | Quelle |
|---|---|---|
| 07.10. 10:16 | Paket-K-Übergabe, Claude-Code-Paket (06.10.), Export 07.10. 09:14. Auftrag: Paket K v1 kritisch prüfen, v2 im Stil L2 v0.3 | T#3, T#63 |
| 07.10. 10:40 / 10:48 | Wissenspaket „Alle Aufgaben“, Freiheiten-Notiz („handle statt fragen“, „nichts kaputt machen“) | T#111, T#157 |
| 08.10. 02:42 | Kritische Analyse „knallhart“, Go-Live-Realismus, GoBright-Vergleich | T#618 |
| 08.10. 02:52 | /goal: weitere Fehler, Umbaupläne, Farb-/Hover-Audit bis 06:00 | T#672 |
| 08.10. 07:04 | Interview (6 Runden) | T#1087, `arbeit/2026-10-08_Interview/ANTWORTEN.md` |
| 08.10. 07:34 | /goal: Copy-and-paste-Gesamtplan für einen zweiten Chat | T#1187 |
| 08.10. 08:01 | Externe Durchsicht des Gesamtplans (4 Punkte) | T#1443 |
| 08.10. 08:08–08:13 | Josias: Freigabe ohne Flow, in der App; Storno fixen | T#1516, T#1529 |
| 08.10. 08:58 / 09:07 | Desktop-Chat: Refresh vor Sammel-Patch / Nachlese über SerienID | T#1971, T#2073 |
| 08.10. 09:14 | Fotos GoBright-Geräte, Michael ab 12.10. im Urlaub | T#2134 |
| 08.10. 11:30 | Externer Prüfer: Studio-Stand „passt“, Storno ohne Dialog, Einfügeliste mit Diffs | T#2165 |
| 08.10. 11:52 | Handy-Export 11:51, Umbauplan für den Handy-Chat | T#2389 |
| 08.10. 12:12 | Studio-Fehler `DropColumns` (F1) | T#2560 |
| 08.10. 12:54 | Handy-Chat: Zeitumstellung, `varNeuID` | T#2616 |
| 08.10. 13:07 | Desktop-Chat: Grundriss-Sperre nach 2 Min | T#2689 |
| 08.10. 14:36 | Exporte „fertig“ (Desktop 14:26, Handy 14:25), Auftrag Abschlussanalyse | T#2956 |
| 12.10. 07:18 | Josias: verfallene Buchung öffnet Check-in-Dialog | T#3555 |
| 12.10. 07:27 | Export 12.10. 07:26 | T#3691 |
| 12.10. 08:14–10:37 | Verteilung Handy/Home-Bildschirm, Kurzanleitung | T#3729–T#3863 |
| 12.10. 11:34–12:06 | Handy-Chat „Tisch zeigen“: Konzept, Paket, Exporte (einer verwechselt) | T#3910, T#4036, T#4124 |
| 13.10. 08:12–08:20 | Analyse-Auftrag Claude Code (Grundriss-Laden, Stand-Abgleich), Export 13.10. 09:59 | T#4253, T#4305, T#4342 |

**Geliefert (alle unter `arbeit/`, belegt per Git):**
| Datum | Lieferung | Umfang | Status laut letztem Export |
|---|---|---|---|
| 07.10. | `2026-10-07_PaketK_v2/UEBERGABE_PaketK_v2.md` | 55 Properties | nie einzeln eingefügt, im Gesamtplan aufgegangen |
| 08.10. | Kritische Analyse, Paket L (82 P.), Selbstprüfung, Interview | | L nur über Gesamtplan teilweise |
| 08.10. | `2026-10-08_Gesamtplan/GESAMTPLAN.md` | 253 Properties, 7 neue Steuerelemente | teilweise eingefügt (berichtet T#2165) |
| 08.10. | Paket F (44 P.) → F2 (37 P.) → F2.1 | | F1–F7 eingefügt (berichtet T#2689), belegt im Export 08.10. bis auf S3b/F5/G25 |
| 08.10. | Nachtrag 1–4 | | N4 (Nachlese) in G6 eingefügt (berichtet T#2165) |
| 08.10. | Handy-Umbauplan v1 → v2 | 17 P. | v2 im Handy-Export 14:25 (belegt T#3279) |
| 08.10. | Grundriss-Sperre | 53 P., 2 Steuerelemente | eingefügt (belegt, Export 13.10.: `btnGrundrissSperre`, `Timer1`) |
| 08.10. | Abschlussanalyse, Nachtrag 5 (21 P.), H8 (4 P.), Texte v4 | | N5 **nicht** eingefügt (belegt, Export 13.10.), H8 zu 3/4 (belegt, Handy 12.10.) |
| 12.10. | Nachtrag 6 (25 P., 1 Steuerelement) | | nicht eingefügt (belegt, Export 13.10.) |
| 12.10. | Verteilung + Kurzanleitung v5 | | unbekannt |
| 12.10. | Tisch zeigen v1 (Bilder/Tabelle), v2 Handy-Properties (123 P., 8 Steuerelemente) | | unbekannt (kein Handy-Export danach) |
| 13.10. | Grundriss-Laden v1 (6 Blöcke) + Antwort an Josias | | nach Go-Live geplant |

## 2. Zeitstrahl (Wendepunkte)
| Zeit (UTC) | Wendepunkt | Kennz. / Quelle |
|---|---|---|
| 07.10. 10:17 | Ziel verstanden, Paket K v1 als Grundlage. Tischauswahl-Problem selbst nicht erkannt, erst auf Nachfrage im Export gefunden (`ddTischePanel.Items: =Tische`) | belegt T#63, T#87 |
| 07.10. 11:22 | Unabhängige Prüfung K v2: 1 Fehler (Label14.Color), 3 Risiken (With-Locals im Filter, Alias `X` = Spalte `X`, Test Schritt 0) | belegt `2026-10-07_PaketK_v2/pruefung_v2_roh.md` Z. 13–16 |
| 08.10. 02:43 | Kritische Analyse: veröffentlichter Stand nicht go-live-fähig, 65–75 % Chance mit K | belegt T#665 |
| 08.10. 03:03 | Prüfung Paket L: 2 Fehler (Tab-Kontrast 2,8:1, P5 Outlook nicht umsetzbar) | belegt `pruefung_paket_l.md` Z. 23, 36 |
| 08.10. 03:05 | Stop-Hook lehnt „fertig“ ab: Hover-Audit unvollständig | belegt T#845 |
| 08.10. 06:52 | Zweite Prüfung: L13 bringt veraltete Startzeit zurück (`Now()` in Items) | belegt `pruefung_paket_l_2.md` Z. 19 |
| 08.10. 06:54 | Selbstkorrektur: 65–75 % war Bauchgefühl, „Doppelklick bucht doppelt“ am PC nur geschlussfolgert | belegt T#1073 |
| 08.10. 07:34–07:45 | Gesamtplan 253 Properties | belegt `GESAMTPLAN.md`, Commit 8c2812a |
| 08.10. 08:01 | Externe Durchsicht: Storno-Rückfrage kann fremde Buchung löschen, Flow löscht falsch, Handy, Umfang | belegt T#1443, T#1501 |
| 08.10. 08:08 | **Kurswechsel:** Freigabe in der App, kein Flow | belegt T#1516 |
| 08.10. 08:30–08:48 | Paket F, Prüfung 13 Befunde (3 mittel) | belegt `2026-10-08_PaketF/pruefung_paket_f.md` Z. 28–40 |
| 08.10. 09:00–09:10 | Nachtrag 3, nach 10 Min durch Nachtrag 4 ersetzt | belegt Commits d5abd2f, d6c7237 |
| 08.10. 11:30 | **Kurswechsel:** Storno ohne Dialog, Basis = gemeldeter Studio-Stand → Paket F2 | belegt T#2165 |
| 08.10. 11:47 | Prüfung F2: 3 hohe Befunde (Doppelklick Auschecken, veralteter Status, Notweg) | belegt `pruefung_paket_f2.md` Z. 18–20 |
| 08.10. 12:12 | Studio-Fehler `DropColumns` mit Text → F2.1 | belegt T#2560, Commit 639060d |
| 08.10. 12:54 | Handy-Chat: YAML-Stand weiter als Export → Handy v2 | belegt T#2616, Commit 31be213 |
| 08.10. 13:18 | Prüfung Grundriss-Sperre: Aufblitzen beim Start (`usenonblockingonstartrule`) | belegt `pruefung_grundriss_sperre.md` Z. 9 |
| 08.10. 14:45 | **Export ≠ gemeldeter Stand:** S3b, F5, G25 fehlen trotz „passt“ | belegt `ABSCHLUSSANALYSE.md` Z. 16, 103 |
| 08.10. 15:12 | Prüfung Nachtrag 5: Formeln ok, Testbogen 1 hoch + 3 mittel | belegt `pruefung_nachtrag5.md` Z. 7–10 |
| 12.10. 07:18 | Josias findet Fehler, den keine Prüfung fand (Check-in-Karte bei „Verfallen“) | belegt T#3555, T#3687 |
| 12.10. 07:28 | Export 12.10. = 08.10. zeichengleich, keiner der Nachträge drin | belegt T#3723 |
| 12.10. 12:04 | Handy-Chat: meine Positionstabelle OG 6–13 falsch (Reihenfolge angenommen) | belegt T#4036 Abschnitt 2 |
| 12.10. 12:10 | Verwechselter Export erkannt (Handy-ZIP = Desktop-App), H8 nur 3/4 | belegt T#4192 |
| 12.10. 12:17 | Selbstprüfung: Knopfbreite, Titelgröße, zirkuläre Prüfung | belegt T#4247 |
| 13.10. 08:21–08:41 | Analyse-Paket, Grundriss-Laden v1 (`TischeLokal` statt `colTische`), Antwort zum Stand, Prüfung auf Wunsch abgebrochen | belegt Commits 47ee987–6ed8b3a, T#4746 |

## 3. Fehlerliste
Format: ID · Titel · Symptom · technische Ursache · tiefere Ursache · Lösung/Status · Kosten · Regel · Kennz. · Quelle.

| ID | Titel | Symptom | technische Ursache | tiefere Ursache | Status | Kosten | Regel | Kennz. | Quelle |
|---|---|---|---|---|---|---|---|---|---|
| LOG-ana-01 | Storno-Rückfrage löscht evtl. fremde Buchung | Bei offener Frage Klick auf eine Kachel → „Ja“ löscht deren Buchung | `conStornoFrage` 420×150 ohne Vollbild-Hintergrund. `btnStornoJa` liest `varSelectedBuchung` erst beim Klick | G5 – Dialog als Sicherung gebaut, ohne den Rest zu sperren und ohne Ziel festzuhalten | gelöst in Paket F (`varStornoID`, Eigentümer `Lower()`, Hintergrund), dann Dialog verworfen | K2 | Bestätigungsdialoge: Ziel beim Öffnen in eigene Variable, Vollbild-Sperre, vor dem Schreiben gegen frischen Stand prüfen | belegt | T#1443 Punkt 1; T#1501 („Den Fehler habe ich mit der Rückfrage selbst eingebaut“) |
| LOG-ana-02 | Freigabe-Flow löscht Spätbucher und Ausgecheckte | Buchung 09:29 für 09:00 wird gelöscht. Nach Auschecken wird gelöscht | Filter nur `Checkedin eq 0 and Startzeit le jetzt−30` | G4/G8 – Regel nicht gegen alle Schreibwege durchgespielt | umgangen: Flow verworfen, Regel mit `Erstellt` in der App (Paket F) | K2 | Jede Regel gegen jeden Schreibweg (buchen spät, auschecken, verlängern, Flow) als Tabelle prüfen | belegt | T#1443 Punkt 2; summary1 („Flow filter used …“) |
| DAT-ana-03 | `DropColumns(…; "Erstellt")` mit Text | Studio: „Erwarteter Name des Bezeichners“, F1 zurückgenommen | App-Einstellung `supportcolumnnamesasidentifiers: true` | G1/G6 – Schreibweise als „gilt bei powerfxv1=false“ angenommen, Einstellung nicht geprüft | gelöst F2.1, Generator prüft Text-Spaltennamen | K2 | Bei Funktionen mit Spaltennamen `Properties.json` prüfen oder Vorab-Test (1 Property) vor dem Paket | berichtet (Studio-Meldung über Desktop-Chat), belegt (Einstellung) | T#2560; `CLAUDE.md` §8 letzte Zeile |
| VAR-ana-04 | Leeres `varFreigabeMinuten` → alles verfallen | In Studio vor OnStart verfällt jede begonnene Buchung sofort | Grenze `DateAdd(Now(); -varFreigabeMinuten…)` mit Blank = 0 | G5 – kein Standardwert | gelöst: überall `Coalesce(…; 30)` | K1 | Jede Konfig-Variable in Formeln mit `Coalesce(Default)` lesen | belegt | `PaketF/pruefung_paket_f.md` Z. 29 |
| UI-ana-05 | „Nach vorne bringen“ statt „Ganz nach vorne“ | „Ja“ hätte den Hintergrund getroffen | Studio hebt nur eine Ebene | G6 | gelöst im Text | K1 | Z-Order immer als „Ganz nach vorne“ + Prüfung in der Strukturansicht formulieren | belegt | `pruefung_paket_f.md` Z. 28 |
| LOG-ana-06 | Doppelklick bestätigt Auschecken sofort | 2. Event eines Doppelklicks geht in den Bestätigungszweig | Frage-Zweig vor der Sperre, Sperre frei | G5 | gelöst: 1-s-Sperre im Frage-Zweig | K1 | Zwei-Tipp-Bestätigung: erster Tipp setzt `varSperreBis` +1 s | belegt | `pruefung_paket_f2.md` Z. 18 |
| LOG-ana-07 | Veralteter Galeriestatus entscheidet beim Auschecken | Buchung wird ohne Rückfrage beendet oder eingecheckt | Zweig prüft Anzeige-Datensatz statt frisch gelesenen | G2 (Anzeige statt Server als Wahrheit) | gelöst: Abgleich frisch ↔ Anzeige | K1 | Frage-Zweige vor dem Schreiben gegen frisch gelesenen Stand abgleichen | belegt | `pruefung_paket_f2.md` Z. 19 |
| MET-ana-08 | Notweg „F1 + F2 zuerst“ nicht unabhängig | Notfassung hätte Variablen aus F1 gebraucht | gemeinsame Variable `varFreigabeMinuten` | G4 | gelöst: Anhang D Notfassung | K1 | Teilpakete/Notwege maschinell auf Abhängigkeiten prüfen (Variablen gesetzt/gelesen) | belegt | `pruefung_paket_f2.md` Z. 20 |
| LOG-ana-09 | L13 holt veraltete Startzeit zurück | Nach `Reset` alte Uhrzeit, wenn Datum gleich | `ddStart.Items` mit `Now()` rechnet nicht neu | G6 | gelöst: `varDialogJetzt`/`varPanelJetzt` | K1 | `Now()` in Datenformeln nie direkt, Zeitpunkt beim Öffnen in Variable | belegt | `pruefung_paket_l_2.md` Z. 19; T#1073 |
| LOG-ana-10 | F-L11 im ersten Paket L übersehen | Dialog zeigt Datum/Zeit vom letzten Öffnen → Buchung am falschen Tag | `DefaultDate` greift ohne `Reset` nicht | G8 – Zustand beim zweiten Öffnen nicht geprüft | gelöst L13 | K1 | Jeder Dialog: Test „öffnen, ändern, abbrechen, anderen Tisch öffnen“ | belegt | T#1073; `CLAUDE.md` §8 |
| UI-ana-11 | Kontrast und Breiten nicht geprüft (L4, L9) | Inaktiver Tab 2,8:1, `lblTitel3` zu schmal | keine Kontrast-/Textbreitenprüfung im Generator | G8 | gelöst; Textbreitenprüfung erst am 12.10. eingebaut | K1 | Generator rechnet Kontrast (≥ 4,5:1) und Textbreite für jede neue Farbe/jeden neuen Text | belegt | `pruefung_paket_l.md` Z. 23, 28 |
| DAT-ana-12 | K v2: With-Locals im Server-Filter, Alias `X`, fehlende Property | Delegation unsicher, Alias kollidiert mit Spalte `X`, `Label14.Color` vergessen | Muster aus der Handy-App nicht übertragen; Spalten von `Tische` nicht geprüft | G6/G2 | gelöst vor Einfügen | K1 | Alias-Namen gegen Spaltennamen der Liste prüfen; Befundtext („Color und Text“) in Checkliste je Property | belegt | `pruefung_v2_roh.md` Z. 13–15 |
| LOG-ana-13 | Grundriss-Sperre blitzt beim Start auf | Sperre bei jedem Start sichtbar, Knopf bedienbar | `usenonblockingonstartrule: true`, `varGrundrissStand` leer | G6 | gelöst: `varJetztTakt` zuletzt in OnStart | K1 | Anzeigen, die auf OnStart-Variablen reagieren, an die zuletzt gesetzte Variable koppeln | belegt | `pruefung_grundriss_sperre.md` Z. 9 |
| LOG-ana-14 | Status „Verfallen“ veraltet ohne Timer-Laden | `lblStatusHeute` hing an `varFreigabeGrenze` | Grenze nur beim Laden gesetzt | G3 (Regel an mehreren Stellen) | gelöst S3b (Takt) | K1 | Zeitabhängige Anzeigen rechnen mit dem Takt, nicht mit einer Lade-Variable | belegt | `pruefung_grundriss_sperre.md` Z. 10 |
| MET-ana-15 | Rückfall nicht ausführbar | Verweis auf falschen Anhang, Originale fehlten | Dokument ohne Anhang A erzeugt | G8 | gelöst (Anhang aus `vorher_de`) | K1 | Jedes Dokument mit Anhang „Originale“ aus dem Generator, nie per Verweis | belegt | `pruefung_grundriss_sperre.md` Z. 11 |
| HAN-ana-16 | Falsche Begründung im Handy-Plan v1 | „Fehlalarm/falsche Rücknahme“ gab es heute nicht | Begründung aus Zielzustand abgeleitet | G1 | gelöst | K1 | Gründe für einen Umbau am heutigen Export belegen | belegt | `2026-10-08_Handy/pruefung_handy.md` Z. 16 |
| HAN-ana-17 | Handy-Plan hätte Stand des Handy-Chats überschrieben | Zeitumstellung (25.10.) und `varBuchungID` | Handy-Chat arbeitet mit YAML-Quellen, die weiter sind als der Export | G7 | gelöst Handy v2 | K1 | Vor jedem Paket den Ziel-Chat nach nicht exportierten Ständen fragen; Basis im Dokument nennen | berichtet (Handy-Chat) | T#2616; Commit 31be213 |
| MET-ana-18 | Testbögen nicht ausführbar | Testmodus lief nach Test 12 weiter → Test 14 falsch; Tests kollidieren mit „zwei Tische“; „Erstellt“ einer Testzeile = jetzt | Tests ohne Zeitachse und ohne Eingabemöglichkeiten der App | G8 | gelöst (Zeitachse) | K2 | Testbogen als Zeitachse, getrennte Buchungen, Testmodus-Ende ausdrücklich, jeder Test gegen die Eingabeliste der App | belegt | `pruefung_nachtrag5.md` Z. 7–9; `pruefung_paket_f.md` Z. 30–31 |
| LOG-ana-19 | Check-in-Karte öffnet Dialog bei verfallener Buchung | Josias kann bei „Verfallen“ in den Check-in-Dialog | `btnEincheckenHeute.DisplayMode` fest `Edit` (Karte = unsichtbarer Knopf) | G8 – Prüfungen deckten Schreibstellen ab, nicht Einstiegsflächen | Nachtrag 6 gebaut, **nicht eingefügt** (Export 13.10.) | K2 | Für jede neue Regel alle Einstiegsflächen (Knöpfe, Karten, Kacheln) mit `DisplayMode` auflisten | berichtet (Symptom, Josias), belegt (Ursache im Export) | T#3555, T#3687; `CLAUDE.md` §6 Nachtrag 6 |
| ORG-ana-20 | Gemeldeter Stand „passt“ ≠ Export | S3b, F5 (`btn5Std.Fill`), G25 fehlen | Teil-Einfügen ohne Abgleich | G2/G7 | erkannt; N4 holt nach, Stand 13.10. **noch offen** | K2 | Nach jedem Einfügeblock: speichern, exportieren, maschinell gegen Soll | belegt | `ABSCHLUSSANALYSE.md` Z. 16; Abgleich 13.10. (`VORHER` für alle 21 N5-Properties) |
| ORG-ana-21 | Export 12.10. 07:26 = Export 08.10. | Dateiname „Einchecken“, aber nichts Neues drin | vermutlich veröffentlichte Fassung exportiert | G7 | erkannt, Josias gebeten neu zu exportieren | K1 | Export-Datum + gewünschten Inhalt vor dem Abgleich bestätigen lassen | belegt (gleich), geschlussfolgert (Grund) | T#3723 |
| WZ-ana-22 | Verwechselter Export | „handy…grundrisseinbauen“ enthält die Desktop-App | falsche Datei hochgeladen | G7 | erkannt über App-ID, „handy echt“ nachgeliefert | K1 | Jeder Export: App-ID und Name prüfen, bevor gerechnet wird | belegt | T#4192 |
| DAT-ana-23 | Positionstabelle mit falscher Reihenfolge | OG Desk 6–13 im Handy-Plan falsch | Galerie-Versatz hängt an SharePoint-ID-Reihenfolge, ich nahm Tabellenreihenfolge an | G1 | gelöst (REST-Reihenfolge, `tisch_zeigen_v2.py` 0 Abweichungen) | K2 | Reihenfolge von SharePoint-Zeilen nie aus App-Tabellen ableiten, per REST belegen | belegt | T#4036 Abschnitt 2; `2026-10-12_TischZeigen2/pruefung_tabelle.txt` |
| MET-ana-24 | Zirkuläre Sichtprüfung | Probe „OG Desk 7“ bestätigte die falsche Tabelle | Rechteck auf ein Bild gelegt, das aus denselben Daten gezeichnet war | G8 | gelöst (unabhängige Quelle) | K1 | Sichtprüfung nur gegen unabhängige Quelle (fremdes Bild, REST) | belegt | T#4027 („Probe mit OG Desk 7“), T#4247 Punkt 3 |
| UI-ana-25 | Text passt nicht in Knopf / Titel | „Tisch zeigen“ braucht ~184 bei 170; Titel Größe 26 zu breit | keine Textbreitenprüfung | G8 | gelöst (200, 22), Generator schätzt Breiten | K1 | Neue Texte: Breite je Zeichenart schätzen, Mindestbreite 640 prüfen | belegt | T#4247 Punkte 1–2 |
| HAN-ana-26 | H8 nur zu 3/4 eingefügt | Datumsauswahl springt ~60 s nach Start auf „Heute“ | `varHeute` nicht in OnStart, `tmrJetzt` (Standard 60 s) vergleicht mit Blank | G2/G7 | T0 geliefert, Stand **offen** | K5 (Buchung am falschen Tag im Betrieb möglich) | wie ORG-ana-20, auch für Handy | belegt (Formeln), geschlussfolgert (Wirkung) | `app.lade_handy_1210_echt()` `tmrJetzt.OnTimerEnd`; T#4192 |
| MET-ana-27 | Dokumente beschreiben nicht eingefügte Funktionen | Kurzanleitung/Handbuch v4: Storno mit Bestätigung, Tab „Buchungen“ lädt neu, 34 Tische | Texte im selben Zug wie Nachtrag 5 geschrieben, nicht an den Einfügestand gebunden | G2/G4 | Korrekturtabelle 13.10., Dateien **offen** | K2 | Nutzertexte erst nach Export-Abgleich freigeben; jede Aussage im Text mit Property verknüpfen | belegt | `KURZANLEITUNG_und_GoLive_Mail_v4.md` Z. 17, 26–27; `BETRIEBSHANDBUCH_Michael_v4.md` Z. 13, 24 |
| ORG-ana-28 | GoBright-Import nie geklärt | Mail: „nicht übernommen“; Claude Code plant ~237 per Flow | Annahme in der Mail seit 08.10., nur als „Hinweis für Josias“ markiert | G12/G4 | **offen** (Antwort 13.10. mit I1–I9) | K5 (Doppelbuchungen am Go-Live möglich) | Betriebsfragen (Datenübernahme, Vertretung, Rechte) als Muss-Entscheidung mit Frist ganz oben führen | belegt | `KURZANLEITUNG…v4.md` Z. 38, 51; `00_UEBERGABE_an_Analyse-Chat_2026-10-13.md` §4 |
| MET-ana-29 | Gesamtplan zu groß | 253 Properties, Pflicht 138 statt 43 (eigene Selbstprüfung) | Interview-Wünsche alle in einen Plan | G4 | Josias fügte Teilmenge ein; Paket F v1 baute auf dem vollen Plan → F2 neu | K3 | Vor einem Gesamtplan: Muss-Liste und Einfrierpunkt mit Josias festlegen, Pakete auf die Muss-Liste beschränken | belegt | T#1443 Punkt 4; T#2165 („Bewusst nicht eingefügt … Aufgeschoben“) |
| KI-ana-30 | Zu sichere Aussagen in der kritischen Analyse | „Doppelklick bucht doppelt“ als belegt für den PC, 65–75 % | Messung aus Handy-App übertragen, Prozente ohne Grundlage | G1 | selbst korrigiert 06:54 | K1 | Prozent-Schätzungen nur mit Herleitung oder gar nicht; Messung immer mit App nennen | belegt | T#665, T#1073 |
| KI-ana-31 | Falsche Aussage über `/goal` | „`/goal` ist kein eigener Befehl“ | /goal setzt einen Stop-Hook (T#674) | G6 (Werkzeugwissen geraten) | nicht korrigiert in der Sitzung | K1 | Aussagen über das eigene Werkzeug nur nach Prüfung (Doku, Systemhinweis) | belegt | T#630, T#674 |
| KI-ana-32 | Abschlussanalyse zu streng/zu stark | „go-live-fähig nach Nachtrag 5“ | N5 ist nicht für richtige Buchungen nötig | G1 | korrigiert 13.10. | K1 | „Muss vor Go-Live“ nur, wenn ohne die Änderung ein falscher Datensatz entsteht | belegt | `ABSCHLUSSANALYSE.md` Z. 15–16; `2026-10-13_GrundrissLaden/ANTWORT_an_Josias_Stand_13.10.md` Kurzfassung |
| KI-ana-33 | Kopfzeile „unabhängig geprüft“ vor der Prüfung | Dokument gepusht mit „unabhängig geprüft (Abschnitt 7)“, Abschnitt 7 „Noch nicht durchgeführt“ | Kopf vorab geschrieben | G5 | gelöst 7 Min später (6ed8b3a) | K1 | Prüfstatus im Kopf nur aus Datei erzeugen (Bericht vorhanden → „geprüft“) | belegt | `git show 47ee987:…UEBERGABE_Grundriss_Laden_v1.md` Z. 2 und 622–623 |
| KI-ana-34 | Handy-Regel auf Desktop übertragen | Erster Entwurf I4: „nicht Big Table“ beim Import | Regel V3 (Handy) statt Entscheidung 5a (PC: Big Table für alle) | G2 | vor Commit korrigiert | K1 | Vor jeder Regelaussage `CLAUDE.md` §5a gegenlesen | belegt | Transkript 13.10. (Edit vor `git add`, Commit 47ee987) |
| WZ-ana-35 | Prüfung im Generator nicht an die Formel gebunden | `FELDER` war eine Konstante; Mutation „Gesperrt fehlt“ wäre durchgerutscht | Prüfung prüfte gegen Liste statt gegen erzeugten Text | G5 | gelöst vor Commit (aus `LOKAL` abgeleitet), Mutation 6/6 | K1 | Jede Generator-Prüfung per Mutationstest bestätigen | belegt | `werkzeuge/grundriss_laden.py` Z. 206 (`FELDER = set(re.findall(…, LOKAL))`) |
| WZ-ana-36 | Dateien für Josias und andere Chats nicht erreichbar | SendUserFile-Karten nicht herunterladbar; Artifact-URL für andere Chats nicht lesbar; ZIP über Artifact nicht möglich | Werkzeuggrenzen | G6 | umgangen: GitHub-Links + ZIP im Repo | K1 | Lieferungen immer als GitHub-Link + Datei, Artifact nur für Ansicht | belegt | T#1332, T#2073; summary2 Abschnitt 4 |
| MET-ana-37 | Farb-/Hover-Audit unvollständig als fertig gemeldet | Stop-Hook lehnt ab | nur Knöpfe geprüft | G8 | gelöst (alle Steuerelementtypen, L10–L12) | K1 | „Alle“ im Auftrag maschinell über alle Steuerelementtypen abdecken, Zählung im Bericht | belegt | T#845, T#900 |
| ORG-ana-38 | Pakete ohne unabhängige Prüfung | Nachtrag 6, Tisch zeigen, Grundriss-Laden v1 nur maschinell | Josias’ Entscheidung (Zeit/Guthaben) | G5/G9 | **offen** | K2–K5 (unbekannt) | siehe Regel R8 | belegt | T#3666, T#4746; jede **geprüfte** Lieferung hatte ≥ 1 mittleren/hohen Befund (Zeilen in Abschnitt 4, Nr. 3) |
| DAT-ana-39 | Rechte „nur eigene Elemente“ ungenau | Bearbeiten enthält „Listen verwalten“, `Tische.Gesperrt` änderbar | Rechtemodell SharePoint nicht vollständig | G6 | gelöst Betriebshandbuch v3 | K1 | Rechteempfehlung je Liste mit Rolle (Mitwirken/Lesen) und Test | belegt | `pruefung_paket_f2.md` Z. 21 |
| LOG-ana-40 | Verlängern prüfte „zwei Tische“ nicht | eigene Überlappung beim Verlängern möglich | Regel nur beim Buchen | G3 | gelöst Paket F (`colVerlIch`) | K1 | Jede Geschäftsregel als Tabelle × Schreibweg | belegt | `pruefung_paket_f.md` Z. 38 |
| LOG-ana-41 | Zeitumstellung 25.10. am Desktop ungeprüft | `T.Value + varNeuStartZeit` (Datum + Zeit) in G6/F4 | in Handy v2 behoben, Desktop nur vorgemerkt | G3/G10 | **offen** | K5 möglich (Buchungen am 25./26.10.) | Erkenntnis aus einer App sofort als Prüfauftrag für die andere anlegen | belegt (vorgemerkt), UNSICHER (Wirkung) | `CLAUDE.md` §6 Handy-Plan Fassung 2 |
| LOG-ana-42 | Desktop: leeres `Erstellt`, „Älterer gewinnt“ nicht nachgezogen | Handy-Regeln strenger als Desktop | nur vorgemerkt | G3 | **offen** | K2 | wie LOG-ana-41 | belegt | `CLAUDE.md` §6 Handy-Export 08.10. („Vorgemerkt …“) |

## 4. Lösungen und Zeitsparer
| Nr | Was | Mechanismus | Ersparnis (geschätzt) | wiederverwendbar bei | Quelle |
|---|---|---|---|---|---|
| 1 | Generator aus dem Export (Anker genau 1×, ganze Property, `to_de`/`from_de`, Diff, Anhang) | Kein Abtippen. Jeder Block ist Export + gezielte Ersetzung, die Rückübersetzung muss identisch sein. Alle Prüfer bestätigten „vorher zeichengleich“ | K4 (sonst Kopier- und Locale-Fehler je Paket) | jede Power-Apps-Änderung, auch Lieferantenreklas | `werkzeuge/*.py`; z. B. `pruefung_nachtrag5.md` „18 Blöcke … zeichengleich“ |
| 2 | Mutationstests der Generator-Prüfungen | Absichtlich eingebaute Fehler müssen erkannt werden, sonst ist die Prüfung blind | K2 | jeder Generator | Paket F (6/6), Tisch zeigen (3/3), Grundriss-Laden (6/6) |
| 3 | Unabhängiger Prüf-Agent mit frischem Kontext | Eigene Skripte, eigener Nachbau des Endstands. Fand in **jedem** geprüften Paket mittlere oder hohe Befunde: K v2 (1 Fehler), L (2), L zweite Runde (1), F (3 mittel), F2 (3 hoch), Handy v1 (2 mittel), Grundriss-Sperre (3 mittel), N5 (1 hoch + 3 mittel) | K4 (Fehler vor dem Einfügen statt im Betrieb) | jedes Paket > 10 Properties | Prüfberichte in `arbeit/**/pruefung*.md` |
| 4 | Export nach dem Einfügen maschinell gegen Soll | Deckte S3b/F5/G25 auf und zeigte am 12./13.10., dass N5/N6 nicht drin sind, dass alle Vorher-Fassungen aber noch passen → keine Neuerzeugung nötig | K2 | jedes Projekt mit Hand-Einfügen | `ABSCHLUSSANALYSE.md` Z. 103; T#3723 |
| 5 | Freigabe in der App statt Flow, nichts löschen | Regel `!CheckedIn && Startzeit <= G && Erstellt <= G` lokal, Server filtert nur delegierbar. Kein Datenverlust, kein Flow-Konto | K3 (Flow-Fehlerfälle, Betrieb) | Fristen/Verfall in SharePoint-Apps | `CLAUDE.md` §6 Paket F |
| 6 | Zweifach-Sperre aus der Handy-Messung | `!varIsLoading && Now() >= varSperreBis` an allen 8 Schreibstellen | K3 (Doppelbuchungen) | jede Schreibstelle in Canvas-Apps | `CLAUDE.md` §4; Prüfbericht Desktop T#3319 |
| 7 | Grundriss-Sperre statt Timer-Laden | Takt-Timer vergleicht nur Variablen; nach 2 Min Sperre bis Tippen. 0 Abfragen ohne Tippen | K2 (Leistung/Abfragen) | Anzeigen mit Live-Daten ohne Push | `pruefung_grundriss_sperre.md`; Abschlussanalyse Tabelle |
| 8 | Nachlese ohne `Refresh` über eindeutige Abfrage | untere Grenze je Klick anders → kein Zwischenspeicher | 2–7 Abfragen je Buchung (geschlussfolgert) | Nachprüfen nach Patch | `CLAUDE.md` §6 Nachtrag 4 |
| 9 | REST-Reihenfolge als unabhängige Quelle | Bricht die zirkuläre Prüfung | K2 | Positionen/Reihenfolgen aus SharePoint | `tisch_zeigen_v2.py`, `pruefung_tabelle.txt` („0 Abweichungen“) |
| 10 | App-Prüfung (SARIF) als Beleg | `CollectingReadOnlyTable` ×2 begründete benannte Formeln mit Microsoft-Text | K1 | Leistungsfragen in Canvas-Apps | `arbeit/_entpackt/desktop_2026-10-13/AppCheckerResult.sarif` |
| 11 | Storno-Bestätigung per zweitem Tippen ohne neues Steuerelement | 2 Properties je Knopf statt ~60 Properties Dialog | K2 Handarbeit für Josias | Bestätigungen in Canvas-Apps | `NACHTRAG_5.md` Kurzfassung; T#2165 Punkt A |
| 12 | `CLAUDE.md` mit Fehlerliste §8 | Regeln überleben 3 Kontext-Zusammenfassungen | K3 (Wiederholungsfehler) | jede lange Sitzung | `CLAUDE.md` §8 |

## 5. Sackgassen
| Was | Warum gescheitert | Stattdessen | Quelle |
|---|---|---|---|
| Freigabe-Flow (G-F) | löscht Spätbucher/Ausgecheckte; Josias: „erscheint unsicher“ | Freigabe in der App (Paket F) | T#1443, T#1516 |
| Storno-Rückfrage als Dialog (5 Steuerelemente) | Sicherheitslücke (LOG-ana-01), ~60 Properties Handarbeit | erst direkt (F2), dann zweites Tippen (N1–N3) | T#2165 A, `NACHTRAG_5.md` |
| Timer F8 lädt alle 5 Min | Abfragen ohne Tippen, Konflikt mit Sperre nach 2 Min | Grundriss-Sperre mit Takt | `CLAUDE.md` §6 Grundriss-Sperre |
| Paket K v2 einzeln einfügen | durch Gesamtplan ersetzt, dann „überholt“ | Gesamtplan → F2.1 → Nachträge | `00_UEBERGABE_an_Analyse-Chat_2026-10-13.md` §5/7 |
| Paket F v1 auf vollem Gesamtplan | Josias fügte G4/G5/G8 nicht ein | F2 auf gemeldetem Studio-Stand | T#2165 |
| Nachtrag 3 | nach 10 Min durch Nachtrag 4 ersetzt (Nachlese ohne Refresh) | Nachtrag 4 | Commits d5abd2f → d6c7237 |
| P5 Outlook-Plan | Lösch-Trigger liefert keine Spaltenwerte | neu entworfen | `pruefung_paket_l.md` Z. 36 |
| L12 „alle Dialoge weiß“ | Weiß auf `#f7f7f7` = 1,07:1 | zurückgezogen | `pruefung_paket_l_2.md` Z. 28 |
| GoBright-Tischanzeigen anbinden | Cloud-gebunden, keine lokale Schnittstelle | abschalten | `CLAUDE.md` §5a |
| Artifact-Downloadseite | ZIP nicht lieferbar, für Chats nicht lesbar | GitHub-Links | summary2 Abschnitt 4 |
| `colTische` (Plan Claude Code 13.10.) | neue OnStart-Abhängigkeit, Prüfhinweis | benannte Formel `TischeLokal` | `UEBERGABE_Grundriss_Laden_v1.md` Kurzfassung |

## 6. Meine eigenen Fehler als Claude
| Moment (UTC) | Fehler | Folge | ID |
|---|---|---|---|
| 07.10. 10:20 | Tischauswahl-Problem nicht selbst erkannt, nur K angesehen | Nachfrage von Josias nötig | – (T#87) |
| 08.10. 02:43 | `/goal` als „kein eigener Befehl“ bezeichnet | falsche Auskunft über Werkzeug | KI-ana-31 |
| 08.10. 02:45 | 65–75 % und „Doppelklick belegt“ ohne Grundlage | korrigiert nach 4 h | KI-ana-30 |
| 08.10. 03:05 | Hover-Audit als fertig gemeldet | Stop-Hook lehnte ab | MET-ana-37 |
| 08.10. ~03:00 | F-L11 übersehen, L13 mit veraltetem `Now()` | 2 Prüfrunden | LOG-ana-09/10 |
| 08.10. 07:34 | Storno-Rückfrage ohne Sperre, Flow-Filter ohne Schreibwege, Plan zu groß | externe Durchsicht nötig, Kurswechsel | LOG-ana-01/02, MET-ana-29 |
| 08.10. 07:34 | Mail-Annahme „GoBright nicht übernommen“ ohne Frage | Widerspruch am 13.10. | ORG-ana-28 |
| 08.10. ~08:30 | `DropColumns` mit Text trotz bekannter Einstellung | Josias fügte F1 ein und nahm es zurück | DAT-ana-03 |
| 08.10. ~11:37 | Auschecken-Bestätigung ohne Sperre | 3 hohe Befunde | LOG-ana-06/07 |
| 08.10. ~11:57 | Handy-Begründung aus Zielzustand, Basis ohne YAML-Stand | Handy v2 | HAN-ana-16/17 |
| 08.10. ~13:13 | `usenonblockingonstartrule` übersehen | Aufblitzen (vor Einfügen behoben) | LOG-ana-13 |
| 08.10. ~14:45 | Testbogen ohne Zeitachse | 1 hoher Befund | MET-ana-18 |
| 08.10. ~14:45 | Texte v4 beschreiben Funktionen vor dem Einfügen | Dokument-Widerspruch | MET-ana-27 |
| 08.10. ~15:00 | Check-in-Karte nicht betrachtet (F7/Abschlussanalyse) | Josias fand den Fehler | LOG-ana-19 |
| 12.10. 11:38 | Reihenfolge angenommen, zirkulär geprüft | Handy-Chat fand OG 6–13 falsch | DAT-ana-23, MET-ana-24 |
| 12.10. 12:10 | Textbreiten nicht geprüft | Selbstprüfung fand es | UI-ana-25 |
| 12.10. ~11:52 | Betriebshandbuch nicht auf 35 Tische aktualisiert, obwohl Export 11:52 UG Desk 14 zeigte | veraltete Zahl | MET-ana-27 |
| 13.10. 08:34 | „unabhängig geprüft“ im Kopf vor der Prüfung gepusht | 7 Min falscher Status | KI-ana-33 |
| 13.10. ~08:30 | Big-Table-Regel vom Handy übernommen; Feldprüfung als Konstante | vor Commit behoben | KI-ana-34, WZ-ana-35 |

## 7. Offene Punkte und Risiken (Stand 13.10. 08:41)
| Nr | Punkt | Risiko | Kennz. / Quelle |
|---|---|---|---|
| O1 | Handy T0 (`varHeute` in OnStart) | Buchung am falschen Tag | belegt (Export 12.10.), Stand danach unbekannt |
| O2 | GoBright-Import entscheiden (I1–I9: Namen 14–17→15–18, Zeitzone 25.10., Kollisionen, Markierung) | Doppelbuchungen | belegt `ANTWORT_an_Josias_Stand_13.10.md` §3 |
| O3 | Dokumente v4/v5 korrigieren (Storno, Tab, 35 Tische) | falsche Erwartung der Nutzer | belegt ebd. §2 |
| O4 | N4 + R1 + K1 (+ N1–N3) einfügen, danach Export-Abgleich | „Verfallen“ verspätet, Check-in-Dialog bei verfallen | belegt (Export 13.10.) |
| O5 | Test 17 (Spätbuchung, echte 30 Min), Rechte „Lesen = alle“, Gerätetest Handy, Sicherung | Doppelbuchung / Zugriff | belegt `ABSCHLUSSANALYSE.md` Z. 15–30 |
| O6 | Vertretung für Michael (Urlaub ab 12.10.) | kein Admin am Go-Live | belegt `CLAUDE.md` §5a |
| O7 | Zeitumstellung 25.10. am Desktop (G6/F4) | Uhrzeit um 1 h verschoben | UNSICHER, LOG-ana-41 |
| O8 | Nachtrag 6, Tisch zeigen, Grundriss-Laden v1 ohne unabhängige Prüfung | unbekannte Fehler | belegt |
| O9 | Grundriss-Laden v1 nach Go-Live; Backlog Galerie-Versatz | Kacheln verrutschen bei neuen Tischen | belegt `CLAUDE.md` §6 Backlog |

## 8. Regeln und Vorschläge für CLAUDE.md (prüfbar)
| Nr | Vorgeschlagene Zeile |
|---|---|
| R1 | Nach jedem Einfügeblock: Josias speichert in Studio und exportiert den **Studio-Stand**; Claude prüft maschinell jede Property gegen den Soll-Stand und meldet „eingefügt / fehlt / abweichend“, bevor Nutzertexte freigegeben werden. |
| R2 | Jeder Export wird vor dem Rechnen auf App-ID, App-Name und Unterschied zum letzten Export geprüft (0 Unterschiede → nachfragen). |
| R3 | Jede Geschäftsregel steht als Tabelle „Regel × Schreibweg × Einstiegsfläche“ (Buchen Dialog/Panel, Verlängern, Stornieren, Einchecken, Auschecken, Flow/Import, Karten/Kacheln mit `DisplayMode`) im Dokument; der Generator prüft, dass jede Zelle belegt ist. |
| R4 | Erkenntnisse aus einer App werden am selben Tag als Prüfauftrag für die andere App in `CLAUDE.md` §7 eingetragen, mit Frist. Offene „vorgemerkt“-Punkte werden in jeder Lieferung unter „Offen“ wiederholt. |
| R5 | Konfigurations-Variablen werden in Formeln nur mit `Coalesce(var; Standard)` gelesen. |
| R6 | Jede Zwei-Tipp-Bestätigung setzt im Frage-Zweig `varSperreBis` +1 s und prüft vor dem Schreiben gegen den frisch gelesenen Datensatz. |
| R7 | Der Kopf eines Dokuments (Prüfstatus) wird aus Dateien erzeugt: „unabhängig geprüft“ nur, wenn `pruefung_*.md` existiert. |
| R8 | Pakete ab 10 Properties oder mit neuen Steuerelementen: unabhängige Prüfung ist Standard. Lässt Josias sie weg, steht im Kopf „nicht unabhängig geprüft“ und in „Offen“ ein Prüftermin nach dem Go-Live. |
| R9 | Jede Generator-Prüfung wird per Mutationstest bestätigt (mindestens 1 Mutation je Prüfung, Ergebnis im Anhang). Prüfungen leiten Soll-Werte aus dem erzeugten Text ab, nicht aus Konstanten. |
| R10 | Neue Texte/Farben: Generator schätzt Textbreite und rechnet Kontrast (≥ 4,5 : 1) und meldet Abweichungen. |
| R11 | Nutzertexte (Kurzanleitung, Mail, Handbuch) beschreiben nur Funktionen, die im letzten Export belegt sind; geplante Funktionen in einem getrennten Abschnitt „kommt mit Nachtrag X“. |
| R12 | Betriebsentscheidungen (Datenübernahme, Rechte, Vertretung, Einfrierpunkt) stehen als Muss-Entscheidung mit Datum ganz oben in jeder Lieferung, bis Josias sie beantwortet hat; Annahmen dazu werden nicht in Nutzertexte geschrieben. |
| R13 | Reihenfolgen von SharePoint-Zeilen nur per REST oder Export der Liste belegen; Sichtprüfungen nur gegen eine unabhängige Quelle. |
| R14 | Aussagen über das eigene Werkzeug (Befehle, Limits) nur nach Prüfung (Systemhinweis/Doku), sonst „UNSICHER“. |

## 9. Gegenprüfung
**Gestrichen oder abgeschwächt:**
- Behauptung „Josias hat F1–F7 eingefügt und getestet“ als **berichtet** markiert (nur Aussage des Desktop-Chats T#2689), belegt ist nur der Export 08.10. 14:26.
- „Nachlese spart 2–7 Abfragen“ als geschlussfolgert, nicht gemessen.
- Kosten durchgehend als geschätzte Klassen, keine Stunden.
- Den Punkt „Rechte ‚Listen verwalten‘ war mein Fehler“ habe ich nicht als eigenen Fehler geführt: Die falsche Annahme stand in der Frage des externen Prüfers (T#2165 Frage 5). Ob meine früheren Texte sie enthielten, habe ich nicht belegt → nur als DAT-ana-39 mit Quelle Prüfbericht.

**Widersprüche zu anderen Quellen:**
- Claude Code (13.10.): „L2-Ladezeile steht 11× zeichengleich“. Prüfbericht Desktop: „Alle 17 Ladestellen wortgleich“. **Aufgelöst, belegt:** Export 13.10. hat 17 Ladestellen; 11 sind zeichengleich, die übrigen unterscheiden sich nur im `Notify`-Text (maschinell: nach Ersetzen des Meldetexts 1 Variante, 17×).
- Claude Code (13.10.): „`btn5Std.Fill` in neuerer Fassung, ob F5 unklar“. **Belegt:** Die Fassung ist die Vorher-Fassung von N4, F5 fehlt.
- Meine Abschlussanalyse (08.10.) „vorher Nachtrag 5 einfügen“ ↔ meine Antwort (13.10.) „nichts aus N5 zwingend“: Widerspruch durch mich selbst, am 13.10. ausdrücklich korrigiert.

**Was mir fehlt:**
- Keine Monitor-Messung nach den Umbauten. Alle Leistungsaussagen nach dem 07.10. sind geschlussfolgert.
- Der Studio-Stand nach 13.10. 09:59 und der Handy-Stand nach 12.10. 12:05 sind unbekannt.
- Ob Josias Pakete getestet hat (außer „passt“-Meldungen) ist nicht belegt.
- Rohberichte der Prüf-Agenten aus früheren Kontexten nur über Zusammenfassungen gelesen.

**Was gut lief und in der Fehlersuche untergeht:** Abschnitt 4. Insbesondere fanden die Prüf-Agenten in 8 von 8 geprüften Paketen echte Befunde, bevor etwas eingefügt wurde, und kein Paket musste wegen eines Kopier- oder Locale-Fehlers zurückgenommen werden außer F1 (`DropColumns`, Einstellungsfrage, nicht Kopierfehler).

## 10. Die 3 größten Zeitkiller und Zeitsparer
**Zeitkiller:**
1. **Kurswechsel nach großen Plänen (Gesamtplan → Paket F → F2 → F2.1):** Ein 253-Property-Plan wurde gebaut, bevor Muss-Liste, Freigabe-Weg und Storno-Variante mit Josias geklärt waren (MET-ana-29, LOG-ana-01/02).
2. **Gemeldeter ≠ tatsächlicher Stand (Desktop und Handy):** Teil-Einfügungen ohne Export-Abgleich erzeugten Nachholpakete und Dokument-Widersprüche (ORG-ana-20, HAN-ana-26, MET-ana-27).
3. **Annahmen statt Belege bei Daten und Einstellungen:** Reihenfolge der Tische, `DropColumns`-Schreibweise, Wirkung von `Now()` kosteten je eine Korrekturrunde (DAT-ana-23, DAT-ana-03, LOG-ana-09).

**Zeitsparer:**
1. **Generator aus dem Export mit Anker- und Rückübersetzungsprüfung:** Kein Kopierfehler erreichte Studio, und alte Blöcke blieben gültig, weil Vorher-Fassungen maschinell bestätigt werden konnten.
2. **Unabhängige Prüf-Agenten:** Sie fanden die hohen Befunde (Auschecken, Storno, Testbogen) vor dem Einfügen.
3. **Export-Abgleich nach dem Einfügen:** Er machte sichtbar, was wirklich drin ist, und sparte Neuerzeugungen (12.10., 13.10.: alle Vorher-Fassungen passen).
