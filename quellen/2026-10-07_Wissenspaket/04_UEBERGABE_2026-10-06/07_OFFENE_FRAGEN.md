# 07 — Offene Fragen

**Kurzfassung:** Zwei Sorten von Fragen. **A: fachliche Entscheidungen**, die Josias treffen muss, bevor der nächste Claude baut — das sind die Nummern 1 bis 11. **B: technisch Unsicheres**, das sich am Quellcode nicht klären lässt und eine Messung oder einen Test braucht — Nummern 12 bis 24. Jede Frage nennt, warum sie offen ist und wo sie im Code hängt.

---

## A — Fachliche Entscheidungen von Josias

### 1. Gilt die Vorprüfung auch für die Einzelbuchung?
Das Konzept beschreibt die Vorprüfung für Serien. Bei einer Einzelbuchung kostet sie einen zusätzlichen Klick („Verfügbarkeit prüfen", dann „Speichern"). Alternative: Bei genau einem Termin direkt speichern, wie heute. Dann gäbe es zwei Pfade mit unterschiedlichem Verhalten.

### 2. Was zeigt das Konflikt-Fenster über fremde Buchungen?
Nur „belegt", oder auch wer gebucht hat? Heute zeigt die App bereits fremde Namen: `conDetailsPopup.lblPerson` zeigt `varSelectedBuchung.Person.DisplayName` in voller Länge, und `Gallery1.Label1` zeigt die Initialen jeder fremden Buchung im Grundriss. Eine Datenschutzentscheidung, die zu dem passen sollte, was die App schon preisgibt.

### 3. Dürfen die drei „Quiet Desk"-Tische als Alternative angeboten werden?
Sie werden im Grundriss schmaler gezeichnet (`Gallery1.Rectangle1.Width`: `- If(StartsWith(ThisItem.Titel, "Quiet Desk"), 10, 0)`), sind aber normal buchbar. „Big Table" ist bereits ausgeschlossen (Vorgabe 3). Für Quiet Desks gibt es keine Vorgabe.

### 4. Was passiert, wenn der Nutzer an einem Konflikttag selbst schon am gewünschten Tisch gebucht hat?
Das ist kein fremder Konflikt. Soll der Tag als „schon gebucht" übersprungen und am Ende gemeldet werden, oder als Konflikt mit Alternative behandelt?

### 5. Darf ein Nutzer am selben Tag zur selben Zeit zwei Tische haben?
Die App prüft das heute nirgends. Wenn eine Serie auf einen Ersatztisch ausweicht, kann genau das entstehen (eigene Buchung an Tisch A, Ersatz an Tisch B zur selben Zeit). Soll die Alternativensuche eigene Buchungen zur selben Zeit ausschließen?

### 6. Die 22:00-Regel: ablehnen oder kappen?
Offene Frage 4 des Briefings, unverändert offen. Heute: Die Dropdowns enden bei 22:00 (`ddStart.Items`, `ddEnde.Items`: `minutenEnde: 22 * 60`), die Verlängern-Knöpfe im Verwalten-Dialog kennen aber **keine** 22:00-Grenze (`btnPlus1Std` bis `btnPlus3Std` prüfen nur Kollision). Eine Buchung kann also über 22:00 hinaus verlängert werden und sogar in den Folgetag reichen.

### 7. Darf in die Vergangenheit gebucht werden?
`dpAnsichtsDatum` hat kein Mindestdatum. `dpDatum` und `dpDatumTischePanel` übernehmen `varAnsichtsDatum` als `DefaultDate`. Für vergangene Tage beginnen die Zeit-Dropdowns bei 08:00. Keine Formel prüft `Startzeit >= Now()`. Soll das gesperrt werden?

### 8. Soll Ein- und Auschecken zeitlich begrenzt werden?
`btnEincheckenHeute` und `btnEinchecken` prüfen keine Uhrzeit. Man kann eine Buchung für übermorgen heute einchecken. Die Kachelfarbe im Grundriss zeigt „rot = eingecheckt", was dann irreführend ist.

### 9. Soll „Alle auswählen" alle Treffer markieren oder nur die sichtbaren?
A.3 aus `ENTWURF_MEHRFACHAUSWAHL.md` ist nicht eingebaut. Heute markiert `chkAlleAuswählen.OnCheck` nur `galAlleTischbuchungen.AllItems`, also die geladene Teilmenge. Der Einbau kostet einen zusätzlichen Lesevorgang. Bei kurzen Listen ist der Fehler ohne Wirkung.

### 10. Sollen Serien an Samstagen und Sonntagen möglich sein?
`varTagSa` und `varTagSo` existieren und werden in beiden Speichern-Knöpfen ausgewertet, aber es gibt **keine** Schalter dafür in der Oberfläche (nur `tglTagMo` bis `tglTagFr`). Beide Variablen werden nur auf `false` gesetzt. Entweder Schalter ergänzen oder die Variablen entfernen.

### 11. Soll der tote Raumcode bleiben?
`conRaumBuchungenPanel`, `conRaumBestätigen` und `galRaumbuchungenHeute` sind über `Visible: =false` unerreichbar, bringen aber 21 Steuerelemente mit Verhaltensformeln, 24 Delegationswarnungen und die beiden Listen `Räume` und `Raumbuchungen` mit. Vor dem Go-Live entfernen oder als künftige Funktion behalten?

---

## B — Technisch Unsicheres (Messung oder Test nötig)

### 12. Macht `Patch(Quelle; Tabelle)` bei SharePoint einen oder N Netzwerkaufrufe?
Die Streitfrage aus dem Briefing (Ü5 gegen die Blog-Quelle). Am Quellcode nicht entscheidbar. **Messung:** Power-Apps-Monitor, Serie mit 1, 5 und 14 Tagen. Günstig: `btnSpeichern` (Sammel-`Patch`) und `btnSpeichernTischePanel` (`ForAll` mit `Patch`) sind gerade der direkte A/B-Vergleich in derselben App.

### 13. Werden `Person` und `Tisch` beim Sammel-`Patch` korrekt geschrieben?
Offene Frage 2 des Briefings. `btnSpeichern.OnSelect` schreibt `Person` **ohne** `'@odata.type'`. Die einzige Stelle in der App, die es mitschreibt, ist `btnSpeichernRaumPanel` (toter Raumcode, Z. 2306). **Test:** Serie speichern, dann unter „Meine Buchungen" nachsehen (die Ansichten filtern auf `Person.Email = User().Email` — fehlt das Personenfeld, verschwinden die Buchungen aus allen Ansichten).

### 14. Was passiert bei einem Teilausfall mitten im Sammel-`Patch`?
`IfError` fängt den Fehler, aber die Zahl tatsächlich geschriebener Zeilen wird nie ermittelt (Ü1). Erst eine `SerienID` mit Nachlese würde das beantworten.

### 15. Warum hat `galAlleTischbuchungen.Items` ein Delegationsdreieck?
Offene Frage 7 des Briefings. Die Formel ist `SortByColumns(Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()), "Startzeit", SortOrder.Ascending)`. Beide Filterbedingungen sind laut Doku delegierbar. Verdächtig: `SortByColumns` auf einer gefilterten Tabelle, oder das umschließende `With({erzwingeNeuaufbau: varGalleryNeuAufbauen}, …)`. In Studio klären (Formel schrittweise vereinfachen und sehen, wann das Dreieck verschwindet).

### 16. Erzeugt `chkAuswahl.OnCheck` Dubletten in `colAusgewaehlteBuchungen`?
`Default` ist `!IsBlank(LookUp(colAusgewaehlteBuchungen, ID = ThisItem.ID))`, `OnCheck` ist `Collect(colAusgewaehlteBuchungen, ThisItem)` ohne Duplikatprüfung. Ob Power Apps `OnCheck` auch auslöst, wenn `Default` auf `true` wechselt (etwa beim Neuaufbau der Galerie durch `varGalleryNeuAufbauen`), ist nicht belegt. **Test:** Drei Haken setzen, Auswahlmodus aus und wieder an, `CountRows(colAusgewaehlteBuchungen)` prüfen.

### 17. Löscht das Abwählen einer einzelnen Zeile die gesamte Auswahl?
`chkAlleAuswählen.Default` ist `CountRows(colAusgewaehlteBuchungen) > 0 && CountRows(colAusgewaehlteBuchungen) = galAlleTischbuchungen.AllItemsCount`. Wird bei vollständiger Auswahl eine Zeile abgewählt, wechselt `Default` auf `false`. Feuert dabei `OnUncheck` (`Clear(colAusgewaehlteBuchungen)`), wäre die ganze Auswahl weg. **Test:** alle auswählen, eine Zeile abwählen, Zahl im Dialogtitel prüfen.

### 18. Löst `Reset(tglAuswahlModus)` dessen `OnChange` aus?
`btnStornierenKlein` und `btnSchließenKlein` setzen `varAuswahlModusAktiv` auf `false` **und** rufen `Reset(tglAuswahlModus)`. Der `OnChange` des Schalters würde noch einmal aufräumen und `varGalleryNeuAufbauen` hochzählen. Harmlos, aber unklar.

### 19. Wie viele Zeilen lädt `galAlleTischbuchungen` tatsächlich?
Steht nicht im Quellcode. Entscheidet, wie dringend A.3 ist (Frage 9).

### 20. Verhält sich ein Start-Override außerhalb der Dropdown-Liste korrekt?
`btn5Std`/`btn9Std` setzen `varStartOverridePanel` auf die aktuelle Uhrzeit, auch wenn in `dpDatumTischePanel` ein künftiger Tag gewählt ist. Für künftige Tage beginnt `ddStartTischePanel.Items` aber bei 08:00. Ein Override wie „06:30" steht dann nicht in der Liste. **Test:** morgen früh um 07:00 ein künftiges Datum wählen und „5 Std" drücken.

### 21. Behält `ddTischePanel` seine Auswahl beim erneuten Öffnen des Panels?
`btnTischHinzufügen` macht kein `Reset(ddTischePanel)`, und das Dropdown hat kein `Default`. Ob die vorherige Auswahl stehen bleibt, ist nicht belegt. Wenn ja: Der Nutzer könnte versehentlich den zuletzt gewählten Tisch erneut buchen.

### 22. Was passiert bei `Remove` auf eine bereits gelöschte Buchung?
`btnStornieren` (Grundriss) hat kein `IfError` und kein `Refresh`; es löscht über die Variable `varSelectedBuchung`. Zeigt die App dann einen rohen Konnektor-Fehler?

### 23. Kann `varAusgewaehltePlusDauer = 0` eine Null-Verlängerung auslösen?
`ddStockwerk.OnSelect` setzt `Set(varAusgewaehltePlusDauer, 0)`. Beide Verlängern-Knöpfe prüfen nur `IsBlank(varAusgewaehltePlusDauer)`; `0` ist nicht leer. **Test:** Stockwerk wechseln, dann im Buchungen-Tab eine Buchung verwalten und ohne Dauerwahl „Speichern" drücken. Erwartung ohne Fehler: Warnung „Bitte eine Dauer auswählen." Tritt stattdessen ein `Patch` mit `+0 Minuten` auf, ist der Befund bestätigt.

### 24. Wie viele Zeilen hat die Liste `Tische` wirklich?
`colTischPositionen` (16) und `colTischPositionenUG` (18) sind fest einprogrammiert, also 34 Positionen. Ob die SharePoint-Liste genauso viele Zeilen hat, steht nicht im Export. Ein Tisch in `Tische` ohne Eintrag in der Positions-Collection bekäme im Grundriss die Koordinaten `Blank()`.

---

## Was aus dem Briefing bereits beantwortet ist

- **Offene Frage 6 („Ist `varMehrfachAuswahlModus` tot?"):** Ja, tot. Sie wird in `App.OnStart` und `btnVerlängern_1.OnSelect` geschrieben und nirgends gelesen (per Skript geprüft, bestätigt durch `app-UnusedVariables` in `AppCheckerResult.sarif`).
- **Offene Frage 5 („Zeile-für-Zeile für (B) bauen?"):** Mit dem Auftrag vom 06.10. ist das überholt. Gebaut wird die Vorprüfung mit Alternativtischen für die Serienbuchung (A), nicht das Mehrfach-Verlängern (B).
