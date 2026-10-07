# AUFGABE_UEBERGABE.md — Vollständige Übergabe der Tischbuchungs-App

Stand: 06.10.2026. Speichern als `C:\tischbuchung_work\AUFGABE_UEBERGABE.md`.

## Worum es geht

Die Power-Apps-Canvas-App „Tischbuchung" wird an einen anderen Claude-Nutzer übergeben. Der soll die App komplett durcharbeiten und verbessern. Dafür braucht er **alles**: jede Formel jedes Steuerelements im Originalwortlaut, jede Variable, jede Datenquelle, den aktuellen Änderungsstand, alle bisherigen Analysen und ein neues Konzept für die Mehrfachbuchung.

**Deine Rolle:** Du dokumentierst, analysierst und ordnest. Du baust nichts um. Die App wird **nicht geöffnet, nicht bearbeitet und nicht zurückgepackt.** Power Apps Studio wird nicht bedient.

**Die richtige App** heißt „Tischbuchung", App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. Es gibt zwei fast identische Klone („App", „App – Kopie"). Prüfe im Exportpaket (Manifest/Properties), dass es die richtige ist. Wenn nicht: `STOPP.md` schreiben und beenden.

---

## Schritt 1 — Quellcode holen

1. Suche im Download-Ordner von Josias das **neueste** Exportpaket der App vom 06.10.2026 oder später (`*.msapp` oder `*.zip`). Ältere Exporte (z. B. `Tischbuchung_2026-09-30_Analyse.zip`) zählen nicht, die App hat sich seitdem geändert. Gibt es keinen Export vom 06.10. oder später: `STOPP.md` mit Begründung und beenden.
2. Kopiere das Paket nach `C:\tischbuchung_work\UEBERGABE_2026-10-06\paket\`.
3. Entpacke es nach `C:\tischbuchung_work\UEBERGABE_2026-10-06\src\`. Nimm den Weg, der beim Inventar (siehe `INVENTAR.md`) funktioniert hat. Ein `.msapp` ist ein ZIP-Archiv; ein Paket-ZIP enthält das `.msapp` weiter innen.
4. Nur lesen. Nie `pac canvas pack`, nie etwas zurückschreiben.

## Schritt 2 — Mechanisch extrahieren, nicht abtippen

**Alle Formeln werden per Skript aus den YAML-/JSON-Quelldateien gezogen**, nicht von Hand übertragen. Abgetippte oder gekürzte Formeln sind in diesem Projekt schon mehrfach Fehlerquelle gewesen. Formeln werden **wortgetreu** übernommen, inklusive Zeilenumbrüchen. Kein `…`, keine Kürzung, keine Zusammenfassung an Stelle des Originals.

## Schritt 3 — Die Dateien

Alles in `C:\tischbuchung_work\UEBERGABE_2026-10-06\`:

### `00_LIESMICH.md`
Inhaltsverzeichnis des Pakets, Stand und Herkunft des Exports (Dateiname, Datum, App-ID), wie man es benutzt, was belegt und was Vermutung ist. Höchstens zwei Seiten.

### `01_APP_KOMPLETT.md` — das Herzstück
**Jedes** Steuerelement der App mit **allen** gesetzten Properties, wortgetreu. Gliederung nach Baum: App → Screens → Container → Kinder (Einrückung oder Pfad wie `Screen1 / conBuchungDialog / btnSpeichern`). Pro Steuerelement:
- Name, Typ (Button, Label, Gallery, Icon, Container, Checkbox, Toggle, DatePicker, Dropdown, Rectangle, Image, Timer …), Elternelement
- jede gesetzte Property mit vollständiger Formel als Codeblock, z. B. `OnSelect`, `OnChange`, `OnCheck`, `OnUncheck`, `OnVisible`, `OnHidden`, `OnTimerEnd`, `Items`, `Default`, `DefaultDate`, `DisplayMode`, `Visible`, `Text`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `DisabledColor`, `BorderColor`, `BorderThickness`, `X`, `Y`, `Width`, `Height`, `Size`, `Font`, `RadiusTopLeft` …
- Galerien: auch alle Properties der Vorlagen-Kinder
- Außerdem: `App.OnStart`, `App.Formulas` (Named Formulas), `App.StartScreen`, `App.OnError`, Screen-Properties (`OnVisible`, `Fill`, `LoadingSpinner` …), App-Einstellungen aus den Metadaten (Datenzeilenlimit, `powerfxv1`, Feature-Flags), Komponenten falls vorhanden.

### `02_BUTTONS.md` — jeder Knopf einmal durchgegangen
Für **jedes** Steuerelement mit einer Verhaltensformel (`OnSelect`, `OnChange`, `OnCheck`, `OnUncheck`, `OnTimerEnd`, `OnVisible` …), auch Icons, Rechtecke mit `OnSelect`, Checkboxen, Toggles, Dropdowns, Galerie-Elemente:
1. Pfad und Typ
2. Was er für den Nutzer tut, in zwei bis drei Sätzen Klartext
3. Die Verhaltensformel(n) vollständig
4. `DisplayMode`, `Visible`, `Fill`, `DisabledFill`, `HoverFill`, `PressedFill`, `Color`, `Text` vollständig
5. Gelesene und geschriebene Variablen und Collections, berührte Datenquellen mit Operation (Filter, LookUp, Patch, Collect, Remove, RemoveIf, Refresh)
6. Netzwerkzugriffe, die ein Klick auslöst (geschätzt, als Schätzung gekennzeichnet)
7. Befunde: Fehler, Risiken, Doppelbuchungswege, fehlendes `IfError`, `varIsLoading` nicht auf jedem Pfad zurückgesetzt, Kopierfehler (falsche Offset-Zahl in einer von mehreren Properties), Variable des falschen Dialogs, toter Code. Jeder Befund ist markiert als **BELEGT** (mit Zitat der Stelle) oder **VERMUTUNG**.

Gruppiere nach Bereich: Header/Tabs, Dashboard, Grundriss, Buchungsdialog, Tische-Panel, Buchungen-Tab inkl. Mehrfachauswahl, Verwalten-Dialoge, Check-in, Details-Popup, toter Raumcode.

### `03_VARIABLEN.md`
Jede globale Variable (`Set`), jede Kontextvariable (`UpdateContext`, `Navigate`-Kontext), jede Collection (`Collect`, `ClearCollect`, `Clear`, `Remove`, `RemoveIf`, `Patch` auf Collections), jede Named Formula. Pro Eintrag: Typ, wo geschrieben (Steuerelement.Property), wo gelesen. Markiere: geschrieben, aber nie gelesen; gelesen, aber nie geschrieben; mit zwei verschiedenen Record-Typen befüllt; zwei Variablen für denselben Zweck (z. B. `varMehrfachAuswahlModus` / `varAuswahlModusAktiv`); dieselbe Variable von zwei Dialogen benutzt (`varSelectedBuchung` / `varSelectedBuchungTab`).

### `04_DATENQUELLEN.md`
Alle Datenquellen mit den tatsächlich benutzten Spalten (interne Namen aus dem Quellcode, z. B. `Titel`, `Geschoss`, `Checkedin`, `SerienID`). Dann **jede** Abfrage und **jede** Schreiboperation auf eine Datenquelle mit Fundort und Einschätzung der Delegierbarkeit nach der Microsoft-Tabelle für SharePoint (`=` auf Text/Lookup/DateTime delegierbar; `<`/`>` auf DateTime ja; auf dem ID-Feld nur `=`; `IsBlank` im Filterprädikat nicht; Person nur `Email`/`DisplayName`; `Not` nicht). Kennzeichne, was du aus der Doku belegst und was du schlussfolgerst.

### `05_STAND_DER_AENDERUNGEN.md`
Prüfe im neuen Quellcode, welche der folgenden Änderungen **tatsächlich drinstehen**, mit Zitat:
- Stornieren-Neubau „Entwurf A" in `btnStornierenKlein.OnSelect` (Kennzeichen `colStornoFrisch`, `colStornoZiele`, `IfError(Remove(...))`), dazu A.2 bis A.4 aus `ENTWURF_MEHRFACHAUSWAHL.md`
- K1 bis K5 aus `ENTWURF_SPEICHERN.md` (K1: `Set(varSelectedBuchung; ThisItem)` in `btnVerwalten_2.OnSelect`; K2/K3: neue Verlängern-Formeln; K4: Zeitgrenze, `>` statt `<>`, `IfError`, kombinierte Meldung; K5: `DisplayMode` mit `varIsLoading`)
- Sammel-`Patch` in `btnSpeichern.OnSelect` (Kennzeichen `neueDatensaetze`, `speicherStatus`)
- alles andere, was sich gegenüber `INVENTAR.md` geändert hat (Diff der Formeln gegen den Export vom 30.09., falls der alte Quellcode noch in `C:\tischbuchung_work\src\` liegt)

### `06_KONZEPT_MEHRFACHBUCHUNG.md`
Das Konzept unten, ergänzt um die **technischen Anker aus dem Quellcode**: welche vorhandenen Steuerelemente, Variablen und Collections betroffen sind, wo die Prüfung andocken muss (beide Speichern-Wege: `btnSpeichern` im Grundriss-Dialog und `btnSpeichernTischePanel` im Tische-Panel), wie Geschoss/Stockwerk im Code abgebildet ist (`varAusgewaehltesStockwerk` = „OG"/„UG" gegen `Tische.Geschoss`, `colTischPositionen`/`colTischPositionenUG`, „Big Table"), welche Daten das Alternativen-Fenster braucht, wie die Abfragen delegierbar bleiben, und welche Fallen aus `BRIEFING_Mehrfachspeichern.md` (Ü1–Ü8) und `VERWORFEN_SPEICHERN.md` gelten. **Keine fertigen Formeln** — das macht der nächste Claude. Eine grobe Skizze der Bausteine (Collections, Container, Knöpfe) ist erwünscht.

### `07_OFFENE_FRAGEN.md`
Alles, was du als `UNSICHER` markiert hast, plus fachliche Entscheidungen, die Josias treffen muss. Nummeriert.

### Außerdem in den Ordner kopieren (unverändert)
`BRIEFING_Mehrfachspeichern.md`, `INVENTAR.md`, `ENTWURF_MEHRFACHAUSWAHL.md`, `VERWORFEN.md`, `ENTWURF_SPEICHERN.md`, `VERWORFEN_SPEICHERN.md`, `ENTWUERFE_ROHFASSUNG.md`, `ARBEITSSTAND_SPEICHERN.md`, `KONTEXT.md`, `KORREKTUR.md`, sofern vorhanden. Fehlende Dateien in `00_LIESMICH.md` vermerken.

### `VERIFIKATION.md`
Belege die Vollständigkeit mit Zahlen, die ein Skript ermittelt:
- Anzahl Steuerelemente im Quellcode = Anzahl Steuerelemente in `01_APP_KOMPLETT.md`
- Anzahl gesetzter Properties im Quellcode = Anzahl Properties in `01_APP_KOMPLETT.md`
- Anzahl Steuerelemente mit Verhaltensformel im Quellcode = Anzahl Einträge in `02_BUTTONS.md`
- 15 zufällig gewählte Formeln: Zeichen-für-Zeichen-Vergleich Quellcode gegen Dokument, Ergebnis je Formel
- Liste der Quelldateien, die gelesen wurden, und der Dateien, die nicht gelesen werden konnten

Stimmt eine Zahl nicht, wird nachgearbeitet, bis sie stimmt.

## Schritt 4 — Paket schnüren

Den ganzen Ordner `UEBERGABE_2026-10-06` (inklusive `src\` und `paket\`) als `C:\tischbuchung_work\UEBERGABE_2026-10-06.zip` packen. Bestehende Dateien außerhalb dieses Ordners nicht verändern oder löschen. Nichts in den Obsidian-Ordner kopieren.

---

## Das Konzept: Vorprüfung mit Alternativtischen

**Problem heute:** Bei einer Serienbuchung wird sofort gespeichert. Belegte Tage werden still übersprungen und erst am Ende als Zahl gemeldet. Der Nutzer erfährt nicht, welche Tage fehlen, und hat keine Alternative.

**Gewünschter Ablauf (Josias, 06.10.2026):**

1. Der Nutzer wählt wie heute Tisch, Datum, Uhrzeit und Wiederholung.
2. **Zuerst kommt eine Prüfung**, nicht das Speichern. Der Knopf heißt z. B. „Verfügbarkeit prüfen". Er ermittelt alle Termine der Serie und prüft für jeden Termin, ob der gewählte Tisch zu dieser Uhrzeit frei ist.
3. **Alles frei:** Der Speichern-Knopf wird freigegeben.
4. **Nicht alles frei:** Ein Fenster geht auf. Es nennt jeden Konflikttag („Am Mi 14.10. ist OG Desk 5 von 08:00 bis 12:00 schon belegt") und bietet für genau diesen Tag und diese Uhrzeit die **Alternativtische an, die dann frei sind**. Der Nutzer kann pro Tag einen Alternativtisch wählen.
5. Im Fenster gibt es einen Knopf **„Nicht buchbare Tage verwerfen"**. Er entfernt alle Konflikttage, für die keine Alternative gewählt wurde.
6. **Erst dann kann gespeichert werden:** Speichern ist gesperrt, bis jeder Konflikttag entweder einen Alternativtisch hat oder verworfen ist.
7. Ein Abbrechen-Knopf schließt das Fenster ohne Speichern.

**Anforderungen, die sich aus dem bisherigen Projekt ergeben** (für den nächsten Claude, nicht von dir umzusetzen):
- Zwischen Prüfung und Speichern können Minuten liegen. Beim Speichern muss **erneut** geprüft werden, sonst entsteht genau dort eine Doppelbuchung.
- Ändert der Nutzer nach der Prüfung Datum, Uhrzeit, Tisch oder Wiederholung, ist das Prüfergebnis ungültig und Speichern wieder gesperrt.
- Das Ergebnis wird **pro Tag** aus dem gemeldet, was SharePoint tatsächlich enthält (Nachlese, z. B. über `SerienID`), nicht aus einem Zähler (Ü1).
- Personen- und Nachschlagefelder korrekt schreiben (Ü6), `varIsLoading` auf jedem Pfad zurücksetzen (1B/2C-Falle), Doppelklick sperren (Ü4), beide Speichern-Wege abdecken (Ü8).
- Die Belegung für den ganzen Serienzeitraum **einmal** delegierbar laden (z. B. `Startzeit < Zeitraumende && Endzeit > Zeitraumbeginn`, Datumsgrenzen vorher in Variablen) und dann lokal rechnen. Die Liste `Tische` ist klein (ca. 30 Einträge).
- Termine, an denen der Nutzer selbst schon am Tisch gebucht hat, sind kein fremder Konflikt und müssen anders behandelt werden (sonst meldet die App nach einem Teilausfall die eigenen Buchungen als Kollision).

**Entscheidungen von Josias (06.10.2026)** — gelten als Vorgabe, in `06_KONZEPT_MEHRFACHBUCHUNG.md` übernehmen:

1. **Reihenfolge der Alternativtische:** zuerst freie Tische im **selben Geschoss**, sortiert nach Nähe zum gewünschten Tisch (Abstand aus den Koordinaten in `colTischPositionen` / `colTischPositionenUG`). Danach freie Tische im **anderen Geschoss**, sichtbar abgesetzt (z. B. „UG – anderes Geschoss").
2. **Ein Ersatztisch für alle Konflikttage:** Es gibt einen Knopf „Diesen Ersatztisch für alle Konflikttage". Als Vorschlag erscheint der Tisch, der an den meisten Konflikttagen frei ist. Pro Tag bleibt eine abweichende Wahl möglich.
3. **„Big Table" wird nicht als Alternative angeboten.**
4. **Tage ohne jeden freien Tisch** zeigen „kein Tisch frei" und können nur verworfen werden.
5. **Eine Serie darf über mehrere Tische laufen.** Alle Termine einer Serie bekommen dieselbe `SerienID`, egal an welchem Tisch. Daraus folgt:
   - Die `SerienID` darf nirgends an den Tisch gekoppelt werden. Eine Nachlese nach dem Speichern filtert auf `SerienID` und Person, **nicht** zusätzlich auf den Tisch (sonst werden Termine am Ersatztisch als „nicht gespeichert" gemeldet).
   - Die Prüfung lädt die Belegung **aller** Tische im Serienzeitraum, nicht nur des gewählten Tisches.
   - Beim Speichern wird jeder Termin mit **seinem** Tisch erneut geprüft, das Ergebnis wird pro Tag gemeldet.
   - Spätere Funktionen wie „ganze Serie stornieren" müssen mit gemischten Tischen umgehen können.

**Noch offene fachliche Fragen** (in `07_OFFENE_FRAGEN.md` aufnehmen):
- Gilt die Vorprüfung auch für die Einzelbuchung?
- Was zeigt das Fenster über fremde Buchungen (Name oder nur „belegt")? Datenschutz.

---

## Regeln

- **Nichts erfinden.** Kein Steuerelement-, Spalten- oder Variablenname, der nicht im Quellcode steht. Was du nicht belegen kannst, ist `UNSICHER`.
- Deutsche Locale in allen Formeln: `;` trennt Argumente, `,` ist Dezimaltrenner, `;;` verkettet. Keine Kommentare in Power Fx.
- Spaltenname ist `Titel` (nicht `Title`), `Tische` hat `Geschoss` (nicht `Standort`) und kein `Aktiv`, Check-in-Spalte intern `Checkedin`.
- Umlaute (ä, ö, ü, ß) in allen Texten normal verwenden.
- Josias liest lange Texte ungern: Jede Datei beginnt mit einer Kurzfassung von höchstens fünf Sätzen.
- Wenn `src` nicht lesbar ist oder das Paket die falsche App enthält: `STOPP.md` mit Begründung, dann beenden.
