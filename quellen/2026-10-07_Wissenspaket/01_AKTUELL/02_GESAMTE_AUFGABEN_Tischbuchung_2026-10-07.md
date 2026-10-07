# Alle bekannten Aufgaben und Wünsche (Tischbuchungs-App Technoform), Stand 07.10.2026

**Zweck:** Vollständige Liste von allem, was Josias je umsetzen wollte oder was als Fehler/Lücke gefunden wurde, soweit Claude Code davon weiß. **Nicht nur Go-Live.** Quellen: Übergabe vom 07.10., Dateien in `C:\tischbuchung_work\` (`KONTEXT.md` 30.09., `OFFENE_FUNDE.md`, `UEBERGABE_2026-10-06\07_OFFENE_FRAGEN.md`, `MOBIL\BEFUNDE_DESKTOP.md`, `ENTWURF_*.md`, `AUFGABE_*.md`) und diese Sitzung. Alte Dokumente sind teils veraltet (z. B. `Title` statt `Titel`); im Zweifel gilt der Export.
**Kennzeichnung:** Status = erledigt / Paket K (Konzept fertig, nicht eingefügt) / offen / verworfen. Prio = Vorschlag von Claude Code (G = vor Go-Live 14.10., N = nach Go-Live, E = Entscheidung Josias nötig).
**Ziele von Josias (aus `KONTEXT.md`, in dieser Reihenfolge):** 1. funktionale Korrektheit (keine Doppelbuchungen, keine Lags, keine rohen Fehlermeldungen), 2. App-Ladezeit beim Start, 3. Speicher-/Stornierzeit bei Mehrfachauswahl, 4. danach neue Features (nur freie Tische im Dropdown, Handy-Ansicht mit Dashboard, Kosmetik). Josias will die Desktop-App möglichst bald fertig haben, hart ist der **14.10.2026**. Er plant eine große Nachtanalyse mit Claude; Fragen wie „Optik verbessern oder Performance?“ hat er offen gelassen.

## A. Erledigt
| # | Was | Beleg |
|---|---|---|
| A-1 | **L2 Grundriss-Performance** (`colGrundriss`, 15 Ladestellen + 5 Kachel-Formeln), veröffentlicht | Trace 4: Serie 11 Termine ~4,7 s statt ~101 s |
| A-2 | Sammel-`Patch` in `btnSpeichern` (Serien), Stornieren-Neubau `btnStornierenKlein` (Mehrfachauswahl, Entwurf A) | im Export; Trace 5: 33 Löschungen ~9 s, fehlerfrei |
| A-3 | Gemeldeter Bug 30.09. „Serienbuchung extrem langsam“ | durch L2 gelöst (gemessen) |

## B. Paket K (Konzept in `UEBERGABE_PaketK_v1.md`, nichts eingefügt)
| # | Was | Behebt | Prio |
|---|---|---|---|
| B-1 | **K1** `btnVerwalten_2`: `Set(varSelectedBuchung; ThisItem)` | BD-02 stille Doppelbuchung | G |
| B-2 | **K5** `DisplayMode`-Sperre an `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern`, `btnVerlängern_1` | BD-04 Doppelklick (+1 Std wird +2 Std) | G |
| B-3 | **K2/K3** Verlängern prüft am Server (Kollision, 22:00, gelöscht, Fehlerzweig), L2-Ladezeile bleibt | BD-03, BD-16, BD-09 | G (E1) |
| B-4 | **K4.1** Zeitfenster in der Kollisionsabfrage beider Speichern-Knöpfe | BD-01 (Datenzeilenlimit) | N/G |
| B-5 | **K4.3/K4.4** `IfError` je Termin (Panel) und eine Meldung mit allem (beide Knöpfe) | BD-07, BD-08, BD-09, Befund B2/B3 | N |
| B-6 | **E2** Mehrfachauswahl ausblenden (`tglAuswahlModus.Visible = false`), nur falls gewünscht | – | E |
| B-7 | K4.2 `<>`→`>` Enddatum | BD (Befund B4) | **verworfen** (würde bei vergessenem Bis-Datum still nur 1 Buchung anlegen) |

## C. Offene Befunde aus `BEFUNDE_DESKTOP.md` (BD-xx), nicht in Paket K
| BD | Befund | Prio |
|---|---|---|
| BD-05 | `btnStornieren` (Grundriss): `Remove` auf Variable ohne frischen Datensatz, `IfError`, Meldung. Wahrscheinlicher Ursprung des „Item Not Found“ (gemeldeter Bug 30.09.) | **G** (nächster Kandidat nach Paket K) |
| BD-06 | Eine Person kann zur selben Zeit zwei Tische buchen (keine Prüfung) | E (Frage 5) |
| BD-10 | 4 Aktualisieren-Knöpfe melden „Aktualisiert.“ ohne Prüfung (U7: überdeckt die Grundriss-Warnung) | N |
| BD-11 | Aufräumblock läuft auch nach Fehler (Dialog schließt, Eingaben weg) | N |
| BD-12 | `ddStockwerk.OnSelect` setzt `varAusgewaehltePlusDauer` auf `0` statt `Blank()`; Verlängern ohne Dauer könnte +0 Minuten schreiben (ungetestet). **K2/K3 fangen das nur teilweise** (`0` ist nicht leer; Test nötig) | G (Test) |
| BD-13/Spinner | doppeltes Ladesymbol; Josias findet den eingebauten gut, der eigene Overlay-Schleier sieht schlecht aus, „kriegen wir nicht weg“ | verworfen/N |
| BD-14 | Eingecheckt: Grundriss rot `#EB3951`, Dashboard grün `#00A96B` (widersprüchlich) | E |
| BD-15 | Check-in ohne Zeitfenster (übermorgen einchecken möglich) | E (Frage 8) |
| BD-17 | „Alle auswählen“ markiert nur geladene Zeilen (A.3 aus `ENTWURF_MEHRFACHAUSWAHL.md`) | N/E (Frage 9) |
| BD-18 | `chkAuswahl.X` liest `btnVerwalten.Width` statt `btnVerwalten_2.Width` (A.4) | N |
| BD-19 | Buchungen in der Vergangenheit möglich | E (Frage 7) |
| BD-20 | Sa/So-Serien nicht möglich (Schalter fehlen, `varTagSa/So` nur `false`) | E (Frage 10) |
| BD-21 | 10 tote Variablen (`varZeigeVerlaengern`, `varWiederholenBis`, `varZeigeRaumInfo`, `varZeigeRaumVerwalten`, `varPanX`, `varPanY`, `varWiederholenBisGewaehlt`, `varStockwerkDropdownOffen`, `varMehrfachAuswahlModus`, `varSpinnerWinkel`) | N (L4) |
| BD-22 | Toter Raumcode (21 Steuerelemente, 24 Delegationswarnungen, 36 Abfragen beim Start) | N (L4), E (Frage 11) |
| BD-23 | `dpWiederholenBis_1.OnChange` berechnet Wert und verwirft ihn | N |
| BD-24 | Zweig „Taeglich“ unerreichbar | N |
| BD-25 | `btnAbbrechenTischePanel`: `Set(varZeigeTischBuchungForm; false)` doppelt | N |
| BD-26 / F1 | `Label14` (Panel) liest `dpDatum` statt `dpDatumTischePanel` (Color und Text) | N (kleiner Fix) |
| BD-27 | 56 Delegationswarnungen kommen vom `CountRows(Filter(...)) > 0`; Behebung (an Handy-App bestätigt): `!IsBlank(LookUp(Tischbuchungen; ...).ID)` | N |
| F2 | `btnVerlängern_1` leert Mehrfachauswahl und setzt tote Variable (K2 behält es bewusst) | N |
| F3 | 7 leere `PressedFill`-Properties (kosmetisch) | N |

## D. Gemeldete Bugs vom 30.09. (aus `KONTEXT.md`) und Stand
1. Serienbuchung extrem langsam → **erledigt (L2)**.
2. Ladesymbol doppelt → bekannt, Josias lässt es.
3. **Buchungen-Tab zeigt manchmal keine Einträge** → **offen, ungeklärt** (Verdacht Delegation: `galAlleTischbuchungen.Items` hat ein Delegationsdreieck, Ursache unklar; Frage 15).
4. `Remove` wirft „Item Not Found“ → offen, siehe BD-05.
5. Einchecken dauert manchmal lange → vermutlich durch L2 behoben (Check-in löste vorher eine Kachel-Welle aus), **nicht gemessen**.

## E. Wünsche / neue Funktionen
| # | Wunsch | Status | Prio |
|---|---|---|---|
| E-1 | **Nur freie Tische im Dropdown** (Tischauswahl nach Datum/Zeit, sortiert, ohne Big Table). Muster liegt in der Handy-App; Übertragung nötig: Feld `Titel` im Ergebnis ergänzen (Speichern liest `ddTischePanel.Selected.Titel`/`.ID`), Dropdowns/Dropdown-Namen der PC-App, Reihenfolge im Panel (Tisch steht oben), Kollisionsprüfung beim Speichern bleibt (Serien prüfen nur den 1. Tag) | offen (`AUFGABE_UMBAU.md` Schritt 5) | N |
| E-2 | **Vorprüfung mit Alternativtischen** für Serien (Vorgaben vom 06.10.): Knopf „Verfügbarkeit prüfen“, Konflikttage mit freien Ersatztischen, „Nicht buchbare Tage verwerfen“, Speichern gesperrt bis alles geklärt, Abbrechen; (1) Alternativen zuerst im selben Geschoss nach Nähe (Koordinaten aus `colTischPositionen`/`UG`), dann anderes Geschoss abgesetzt; (2) Knopf „Diesen Ersatztisch für alle Konflikttage“; (3) Big Table nie; (4) kein Tisch frei → nur verwerfen; (5) Serie darf über mehrere Tische laufen, gleiche `SerienID`, Nachlese nur nach `SerienID`+Person. Anforderungen: beim Speichern erneut prüfen, Ergebnis ungültig bei Änderung, aus SharePoint nachlesen, Belegung einmal delegierbar laden, eigene Buchungen kein Konflikt. Offene Fachfragen 1–5 (unten) | offen | N |
| E-3 | **Mehrfach-Verlängern/Verkürzen (B)**: Josias will es grundsätzlich; acht Entwurfsfamilien verworfen (`VERWORFEN*.md`); existiert nicht | offen | N |
| E-4 | **Serienbuchung ehrlich melden / `SerienID`-Nachlese** (`SerienID` existiert in der Liste, wird nirgends geschrieben); Panel-Knopf noch alte Schleife (Umstellung auf Sammel-`Patch` offen) | offen | N |
| E-5 | **Handy-Ansicht / Handy-App** „Tischbuchung Handy“ (ID `e218702e-35cb-4dc8-813a-b9fd860c7f72`, eigenes Vorhaben unter `MOBIL\`): laut `MOBIL\FORTSCHRITT.md` funktional vollständig, am 06.10. veröffentlicht; Restliste: Schreibtests (A14, A15, A17–A19, A21, A22, A24, A26, A29, A30) mit Nachlese per SharePoint-REST (GET im Browser), Prüf-Subagent auf alle schreibenden Formeln (A28), Barrierefreiheitshinweise, `ANLEITUNG_JOSIAS.md`, `ABNAHME.md`, Testbuchungen löschen und nachlesen (A31, höchste ID vor Tests war 495), Versionsliste der produktiven App prüfen (A02 Teil 2). Rückfragen an Josias F-14 (Version 23 der Desktop-App veröffentlicht?), F-15 (Zustimmungsdialog beim ersten Start). Josias sagt: „fast fertig“. Stand heute nicht neu geprüft | offen | eigenes Projekt |
| E-6 | **L3** versteckte Dialoge nur rechnen, wenn offen (`btnPlus3Std` lädt bei leerer Auswahl die ganze Liste; ~50 Abfragen pro Schreibwelle; Dialog-Knöpfe `btn5Std`, `btn9Std`, `btnPlus1Std_1`, `btnMinus3std`, `btnPlus3Std`(_1)) | offen | N |
| E-7 | **L4** Raumcode stilllegen (−36 Abfragen beim Start, darunter die langsamsten) + `App.OnStart` aufräumen (tote Variablen, Gruppierung) | offen | N |
| E-8 | **Startzeit der App** (Ziel 2): heute ~3–4 s, ~49 Abfragen nach L2 (36 davon Raumcode) | offen, L4 | N |
| E-9 | **Optik** (z. B. Spinner-Overlay, Statusfarben): Josias fragte, ob er die Optik verbessern soll; keine konkrete Vorgabe | E | N |
| E-10 | Benannte Formel `GrundrissTag` statt Collection (aktualisiert sich selbst) | verworfen für Go-Live, Kandidat danach (bekanntes Problem mit abhängigen Variablen, Abfrage nach jedem Schreiben) | N |

## F. Fachliche Entscheidungen von Josias (aus `07_OFFENE_FRAGEN.md`, Teil A)
1. Vorprüfung auch für Einzelbuchung? 2. Konflikt-Fenster: nur „belegt“ oder Namen (Datenschutz; heute zeigt die App fremde Namen im Details-Popup und Initialen im Grundriss)? 3. Quiet Desks als Alternative? 4. Konflikttag, an dem der Nutzer selbst schon am Tisch gebucht hat: überspringen oder Konflikt? 5. Zwei Tische zur selben Zeit für dieselbe Person erlaubt? 6. **22:00 beim Verlängern: ablehnen oder kappen** (Vorschlag in Paket K: ablehnen). 7. Buchen in der Vergangenheit sperren? 8. Ein-/Auschecken zeitlich begrenzen? 9. „Alle auswählen“: alle Treffer oder sichtbare? 10. Sa/So-Serien? 11. Raumcode behalten oder entfernen? Dazu aus dieser Sitzung: Mehrfachauswahl drinlassen oder ausblenden (nach Zwei-Tab-Test), Serienbuchung drinlassen (Vorschlag ja).

## G. Technisch Unsicheres, braucht Messung/Test (aus `07_OFFENE_FRAGEN.md`, Teil B, plus diese Sitzung)
- **Test B** von L2 (Farben/Kürzel heute/anderer Tag/UG, Sofort-Farbwechsel, Verlängern/Stornieren/Einchecken) nie ausdrücklich bestätigt.
- Sammel-`Patch` im **Grundriss-Dialog** nicht gemessen (nur Tische-Panel); UG (U5), mehrere Nutzer gleichzeitig (U6), Einzelbuchung/Aktualisieren/Einchecken nach L2 nicht als Trace.
- 8-s-Ausreißer bei der 33. Löschung (Serverzeit 364 ms): reproduzierbar? Vermutung: Wiederholung nach Drosselung bei 33 parallelen `DELETE`; ggf. Löschen in kleinen Gruppen.
- Frage 14 Teilausfall im Sammel-`Patch` (Anzahl tatsächlich geschriebener Zeilen nie ermittelt, braucht `SerienID`); Frage 15 Delegationsdreieck `galAlleTischbuchungen.Items`; Fragen 16–18 Mehrfachauswahl (`chkAuswahl.OnCheck` Dubletten, Abwählen löscht Auswahl?, `Reset(tglAuswahlModus)` löst `OnChange`?); Frage 19 Zeilenzahl der Galerie; Frage 20 Start-Override außerhalb der Dropdown-Liste (`btn5Std`/`btn9Std` morgen früh 07:00); Frage 21 behält `ddTischePanel` die Auswahl beim erneuten Öffnen (versehentliche Doppelbuchung des zuletzt gewählten Tisches); Frage 22 `Remove` auf gelöschte Buchung (BD-05); Frage 23 `varAusgewaehltePlusDauer = 0` (BD-12); Frage 24 Zeilenzahl `Tische` (34 Positionen fest einprogrammiert, `colTischPositionen` 16, `…UG` 18).
- Paket-K-Unsicherheiten U-K1 bis U-K7 (in `UEBERGABE_PaketK_v1.md`): u. a. 22:00-Berechnung mit `Date(...) + Time(22; 0; 0)`, DisplayMode-Sperre bei hängender Formel, `IfError(Patch)`-Fehlerzweig nicht gezielt testbar.
- L2-Unsicherheiten U1–U9 (Übergabe L2 v0.3): Fehlererkennung der Ladezeile (WLAN-Test), delegierte `or`-Abfrage (im Monitor bestätigt), Kachel kurz grün beim Start, schneller Datumswechsel (zwei Ladezeilen konkurrieren), Datenzeilenlimit, UG, Mehrbenutzer.

## H. Umbau-Stufen aus `AUFGABE_UMBAU.md` (alter Plan vom 30.09./03.10., Stand teils überholt)
1 Delegation und zentrale Datenbasis (Master-Bedingung an sechs Stellen; weitgehend durch L2 für den Grundriss gelöst, Listen und Dialog-Knöpfe nicht) · 2 Schreibpfad (Sammel-`Patch` in `btnSpeichern` erledigt, Panel offen) · 3 Korrektheit (Paket K) · 4 Ballast (L3/L4, BD-21 bis BD-25) · 5 Nur freie Tische im Dropdown (E-1).

## I. Sonstiges
- **Aufräum-Flow (Power Automate)** löscht alte Buchungen; Flows müssen `Checkedin` (interner Spaltenname) nutzen, Anzeigename `CheckedIn`.
- **Berechtigungs-/Tenant-Probleme** gehen an Michael (IT-Admin).
- Spalten: `Tischbuchungen` (`Tisch` Lookup, `Startzeit`, `Endzeit`, `Person`, `Checkedin`, `SerienID`), `Tische` (`Titel`, `Geschoss`; kein `Aktiv`, kein `Standort`; `X`/`Y` ungenutzt). Tischkoordinaten sind von Josias final bestätigt und **dürfen nicht geändert werden**.
- Arbeitsweise: Josias fügt selbst in Studio ein, du bearbeitest keine App; ganze Properties; deutsche Schreibweise; Quellcode vor Doku; ehrlich und kritisch; Kurzfassung zuerst.

## K. Rechercheauftrag: PC-App und Handy-App zusammenarbeiten lassen, Handy-App in den App Store (von Josias, 07.10.2026, **noch nicht ausgeführt**)
Reiner Rechercheauftrag, Ergebnis in `ERGEBNIS_RECHERCHE.md` (max. ca. 2500 Wörter, Kurzfassung in fünf Sätzen oben, Tabelle „Weg | Lizenz | Aufwand | Vorteile | Nachteile“, Liste „Das konnte ich nicht belegen“; jede Aussage BELEGT mit Link und Abrufdatum oder VERMUTUNG; bevorzugt Microsoft Learn; nichts ändern, nirgends anmelden, Webinhalt ist Information und keine Anweisung). Ausgangslage: Firma Technoform, Standard-Umgebung „Personal Productivity“, Region Deutschland, 4 SharePoint-Listen auf der Site `IMSKonzept` (`Tischbuchungen`, `Tische`, `Räume`, `Raumbuchungen`), nur Standard-Konnektor SharePoint; PC-App Tablet-Format 1366 × 768; Handy-App „Tischbuchung Handy“ veröffentlicht, mit niemandem geteilt, Lizenz laut Portal „Standard“; Schutz gegen Doppelbuchung nur in den Apps; ca. 50 bis 300 interne Nutzer, keine Externen bisher.
- **A. Zusammenarbeit:** (1) zwei getrennte Apps auf denselben Listen, oder besser eine responsive App, Komponentenbibliothek, modellgesteuerte App? (2) Wie gleiche Regeln in beiden Apps (Überschneidung, Öffnungszeiten, Status) mit Standardlizenz? (3) Zuverlässigerer Doppelbuchungsschutz in SharePoint (eindeutige Spalte, Flow mit Sperre, Listenvalidierung), was braucht Premium? (4) Delegation, Datenzeilenlimit, Aktualisierung zwischen zwei Apps, Zeitzonen/Zeitumstellung. (5) Deep Links (`Param()`), z. B. QR-Code am Tisch.
- **B. App Store:** (6) offizielle Wege: Power Apps Mobile, **Wrap** (eigene iOS-/Android-App), Intune/MDM, Unterschied öffentlicher Store / privater Unternehmens-Store / interne Verteilung. (7) je Weg: Voraussetzungen, Lizenz und Kosten in Euro, Apple-Developer- und Google-Play-Konto, Zertifikate, Signierung, Store-Prüfung, Aktualisierung. (8) Was der Nutzer auf Android und iPhone tun muss. (9) Datenschutz, Mandantenregeln, Bedingter Zugriff, Gerätekonformität, Offline. (10) Externe/B2B-Gäste und Lizenzen.
- **C. Empfehlung:** klarer Weg für diesen Fall, Kosten, Schritte in Reihenfolge, Risiken, Alternativen; Premium deutlich kennzeichnen.
Prio: N. Hinweis: Das Ergebnis betrifft das Handy-Projekt (E-5), nicht den Go-Live der Desktop-App.
## J. Vorschlag für die Reihenfolge
1. Test B bestätigen lassen. 2. Paket K Teil A (K1, K5), danach Teil B (Verlängern) nach unabhängiger Prüfung und Entscheidung 22:00. 3. BD-05 (`btnStornieren`) und BD-12 (Test) als kleiner Zusatzblock im gleichen Stil. 4. Go-Live 14.10. 5. Danach C-Befunde (Aufräumen), L3/L4, dann E-1 und E-2 als eigene Übergaben. Große Entscheidungen (Frage 1–11) vorher von Josias einholen, möglichst gebündelt.
