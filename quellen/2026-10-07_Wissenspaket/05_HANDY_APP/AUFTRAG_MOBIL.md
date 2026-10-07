# AUFTRAG_MOBIL.md — Die Handy-App für die Tischbuchung

**Auftraggeber:** Josias Assefaw (Werkstudent Digitalisierung, Technoform Kunststoffprofile GmbH)
**Stand:** 06.10.2026
**Ablage:** `C:\tischbuchung_work\MOBIL\AUFTRAG_MOBIL.md`

Diese Datei ist dein Auftrag. Sie ist verbindlich und du veränderst sie nicht. Lies sie einmal ganz, bevor du irgendetwas tust. Lies nach jeder Kontext-Kompaktierung mindestens die Abschnitte 4 (Leitplanken), 7 (Doppelbuchungen) und 8 (Abnahme) erneut, dazu deine eigene `FORTSCHRITT.md`.

---

## 1. Deine Rolle

Du bist ab jetzt der **leitende Entwickler** dieser Handy-App. Du hast die Desktop-App „Tischbuchung" in den letzten Sitzungen gründlicher analysiert als jeder andere, du kennst ihren Code besser als Josias und besser als der Chat-Claude, der diesen Auftrag geschrieben hat. Nutze dieses Wissen und vertraue ihm, aber prüfe es gegen den Quellcode, bevor du dich darauf verlässt.

Arbeite so, wie ein erfahrener Senior-Entwickler eine App für ein Team baut, das sie danach selbst warten muss:

- Du **entscheidest selbst**, wie du baust. Josias hat dir bewusst viel Freiheit gegeben (Abschnitt 3).
- Du **prüfst alles nach**. Eine Formel ist erst fertig, wenn du gesehen hast, dass sie zur Laufzeit das Richtige tut. Kompilierfehlerfrei heißt noch nicht fertig.
- Du **dokumentierst alles** so, dass Josias jeden Schritt nachvollziehen und rückgängig machen kann (Abschnitt 5.4). Das ist für ihn wichtiger als Tempo.
- Du bist **ehrlich**. Was du nicht belegt hast, nennst du ungetestet. Eine falsche Erfolgsmeldung ist in diesem Projekt der teuerste Fehler, den es gibt; er ist schon mehrfach passiert.
- Du **hältst die App einfach**. Josias ist Werkstudent und wird diese App allein weiterpflegen. Lieber eine klare Formel mehr als ein cleverer Trick, den niemand versteht.

---

## 2. Die Vision

### 2.1 Worum es geht

Die Desktop-App ist ein Planungswerkzeug: Grundriss, OG/UG, Serienbuchung, Mehrfachauswahl. Am Handy braucht das niemand. Am Handy will man in **zehn Sekunden** eines von vier Dingen erledigen:

| Moment | Was die App dann können muss |
|---|---|
| Morgens auf dem Weg ins Büro | Auf einen Blick sehen: Habe ich heute einen Tisch? Welchen, von wann bis wann? |
| Im Büro, spontan | Einen freien Tisch finden und buchen, ohne Grundriss |
| Am Tisch angekommen | Mit einem Tipp einchecken |
| Plan geändert | Stornieren, verlängern oder früher beenden |

**Die Handy-App ist keine verkleinerte Desktop-App, sondern eine eigene, bewusst kleine App für genau diese vier Momente.** Sie läuft nur auf Handys (Hochformat). Sie nutzt dieselben SharePoint-Listen wie die Desktop-App, sodass beide immer denselben Stand zeigen.

### 2.2 Was die App zeigt

Josias' Wunsch in seinen Worten: nur das Panel Tischbuchung, das Panel Tischbuchungen heute, dazu der Header und eine abgewandelte Form von tabBuchungen. Kein `conGrundriss`. Daraus folgen vier Bereiche:

**Header**
- Technoform-Logo, App-Name, Initialen des Nutzers (wie in der Desktop-App)
- Ein Knopf zum Aktualisieren

**„Heute"** (Startansicht, abgeleitet aus dem Panel Tischbuchungen heute / `galTischbuchungenHeute`)
- Die eigenen Buchungen von heute als große Karten: Tisch, Zeit, Status
- **Einchecken mit einem Tipp direkt auf der Karte**, wenn die Buchung im Check-in-Zeitfenster liegt
- Zugang zum Verwalten (stornieren, verlängern, früher beenden)
- Wenn heute nichts gebucht ist: ein klarer Hinweis und ein direkter Weg zum Buchen

**„Buchen"** (abgeleitet aus dem Panel Tischbuchung / `conTischBuchungenPanel`)
- Reihenfolge am Handy: **Datum → Uhrzeit → Tisch**, nicht umgekehrt. Ohne Grundriss muss die Tischauswahl zeigen, **was im gewählten Zeitraum frei ist**. Belegte Tische erscheinen nicht.
- Vor dem Tippen auf „Buchen" sieht der Nutzer in einem Satz, was er bucht („OG Desk 5 · Mi 08.10. · 08:00–17:00")
- Keine Serienbuchung

**„Meine Buchungen"** (abgewandelte Form von tabBuchungen / `conBuchungen`)
- Alle eigenen kommenden Buchungen, chronologisch, mit Wochentag
- Je Eintrag: Verwalten
- Keine Mehrfachauswahl

**Navigation:** eine Tab-Leiste unten (Daumenreichweite), die zwischen den drei Bereichen umschaltet.

### 2.3 Vorgaben zu den offenen Fachfragen

Josias hat diese Punkte noch nicht endgültig entschieden. Bis er es tut, gilt der Standard. Du darfst begründet abweichen, wenn du einen besseren Weg siehst; dann trägst du das in `ENTSCHEIDUNGEN.md` ein **und** als Frage in `FRAGEN_AN_JOSIAS.md`.

| # | Frage | Standard |
|---|---|---|
| V1 | Buchen nur für heute oder auch für andere Tage? | Auch andere Tage, keine Serie |
| V2 | Check-in-Zeitfenster | ab 30 Min vor Start bis Ende (passt zur 30-Min-Logik des Grundrisses) |
| V3 | Zweiter Tipp auf Einchecken | darf **nicht** auschecken (die Desktop-App schaltet heute um) |
| V4 | Auschecken / früher gehen | „Jetzt beenden" setzt die Endzeit auf jetzt; der Tisch wird wirklich frei |
| V5 | Verlängern | +1 Std und +2 Std, nie über 22:00 |
| V6 | Darf eine Person zur selben Zeit zwei Tische haben? | Nein, die Handy-App verhindert das |
| V7 | Big Table | am Handy nicht buchbar |
| V8 | Stornieren | mit Bestätigung (Fehltipps am Handy sind häufig) |
| V9 | Schnellwahl-Knöpfe | erlaubt, aber ohne die teuren Mehrfachabfragen der Desktop-Knöpfe `btn5Std`/`btn9Std` |

### 2.4 Was die App nicht hat

Grundriss, OG/UG-Umschalter, Serienbuchung, Mehrfachauswahl, Raumbuchung, Detail-Popup bei Tischklick. Wer das braucht, nimmt den Laptop.

### 2.5 Aussehen und Bedienung

- Technoform-Blau `#171496` als Leitfarbe; Statusfarben wie in der Desktop-App (frei grün `#00A96B`, fällig orange `#FFA500`, eingecheckt/belegt rot `#EB3951`)
- Eine Spalte, alles untereinander, große Schrift, Tippflächen mindestens so groß wie die Fingerkuppe (≈ 44–48 pt)
- Keine Hover-Effekte als Informationsträger (gibt es am Handy nicht), sichtbare Zustände über Farbe **und** Text
- Rückmeldungen als kurze, deutsche, verständliche Meldungen; nie rohe Fehlertexte
- Die App muss sich gut anfühlen. Josias will sie seinen Kollegen zeigen können. Du darfst hier gestalterisch eigene Ideen einbringen.

### 2.6 Qualitätsanspruch in der Reihenfolge seiner Wichtigkeit

1. **Keine Doppelbuchungen, keine unsichtbaren Buchungen, keine lügenden Meldungen** (Abschnitt 7)
2. Schneller Start und schnelle Reaktion auch im Mobilnetz
3. Einfach wartbar
4. Schön

---

## 3. Dein Spielraum

Josias gibt dir ausdrücklich viele Freiheiten:

**Architektur.** Du entscheidest, ob du
- eine **neue Canvas-App** baust,
- eine **Kopie der jetzigen App** anlegst (z. B. „Speichern unter") und sie auf die Handy-Ansicht reduzierst, oder
- einen anderen Weg gehst, den du für besser hältst.

Begründe die Wahl in `ENTSCHEIDUNGEN.md`. Einziger Ausschluss: **Power Apps Code Apps** (das „Mobile Apps"-/„Code Apps"-Plugin). Sie brauchen eine Premium-Lizenz pro Nutzer und eine Admin-Freischaltung; beides gibt es hier nicht.

**Werkzeuge.** Nutze, was am besten funktioniert, und probiere aus:
- **Canvas Authoring MCP** von Microsoft (Plugin `canvas-apps@power-platform-skills`, Marketplace `microsoft/power-platform-skills`, braucht .NET 10 SDK und Co-Authoring in der App). Damit kannst du `.pa.yaml` direkt in eine offene Studio-Sitzung schreiben, mit `compile_canvas` prüfen und mit `sync_canvas` abgleichen. Das ist voraussichtlich der stärkste Weg. Status: Public Preview.
- **Browser-Steuerung** (Claude in Chrome), um Power Apps Studio zu bedienen, Einstellungen zu setzen, zu speichern, zu veröffentlichen und die App in der Geräteemulation zu testen
- **YAML einfügen** über die Code-Ansicht im Studio als Rückfallweg
- `pac` CLI, PowerShell, Python, Skripte, Git
- **Subagenten** für Recherche, parallele Arbeit und unabhängige Prüfungen

**Dein Rechner.** Du darfst den ganzen PC von Josias durchsuchen und lesen: Downloads, OneDrive, Obsidian-Journale, alte Exporte, Notizen. Du darfst Werkzeuge installieren, die du brauchst (z. B. .NET 10 SDK, Plugins), und protokollierst jede Installation in `FORTSCHRITT.md`.

**Power Apps.** Du darfst eine Bearbeitungssperre („App wird von … bearbeitet") für die **Handy-App** aufheben bzw. übernehmen, Co-Authoring aktivieren und Einstellungen ändern. Du darfst die Handy-App speichern und veröffentlichen, damit du sie testen kannst.

**Inhalt.** Der Bauplan in `hintergrund\` ist ein Vorschlag vom Chat-Claude, nicht bindend. Er basiert auf dem Export vom 30.09. und weiß weniger als du. Wo du Besseres siehst, mach es besser und schreib auf, warum.

---

## 4. Die Leitplanken

Diese Grenzen gelten ohne Ausnahme. Jede hat einen Grund.

**L1 — Die produktive App bleibt unangetastet.** Die App „Tischbuchung" (ID `d247d18b-d36f-4a44-975a-7839695b2f12`) geht am 14.10.2026 live. Du darfst sie öffnen, lesen und exportieren. Du speicherst sie nicht, veröffentlichst sie nicht, änderst keine Einstellung und keine Formel. Dasselbe gilt für die Klone „App" und „App – Kopie". Falls du eine Kopie als Ausgangspunkt nimmst, entsteht sie über „Speichern unter" oder Export/Import als **neue** App mit eigenem Namen, und du prüfst danach anhand der App-ID, dass du in der Kopie arbeitest. *Grund:* Ein versehentlicher Fix an der falschen App ist hier schon einmal passiert.

**L2 — Die SharePoint-Daten sind echt.** `Tischbuchungen` und `Tische` sind die Produktivlisten; Kollegen buchen dort.
- Keine Spalten anlegen, ändern oder löschen, keine Listeneinstellungen ändern
- Keine fremden Einträge ändern oder löschen
- Testbuchungen nur mit Josias' eigenem Konto, jede sofort in `TESTDATEN.md` eintragen (ID, Tisch, Zeitraum, Zweck)
- Testbuchungen wenn möglich auf ein **Wochenende mindestens drei Wochen in der Zukunft** legen, damit niemand blockiert wird. Tests, die „jetzt" brauchen (Einchecken, „Jetzt beenden"), kurz halten, auf einem freien Tisch und sofort danach löschen
- Am Ende sind alle Testbuchungen gelöscht, nachgewiesen durch eine Nachlese

Wenn du eine eigene Testliste brauchst und sie ohne zusätzliche Rechte anlegen kannst, darfst du das. Dokumentiere es und räume sie am Ende wieder ab oder kennzeichne sie klar als Test.

**L3 — Keine Wirkung nach außen.** Du gibst die Handy-App niemandem außer Josias frei. Du verschickst keine E-Mails, Teams-Nachrichten oder Einladungen.

**L4 — Keine Mandanten- oder Admin-Änderungen.** Keine Umgebungseinstellungen, keine DLP-Richtlinien, keine Premium-Konnektoren, keine Lizenzen. Fehlen Rechte, trägst du das in `FRAGEN_AN_JOSIAS.md` ein; solche Punkte gehen bei Technoform an den IT-Admin Michael.

**L5 — Schreiben nur in deinem Ordner.** Lesen darfst du überall. Schreiben, anlegen und löschen nur in `C:\tischbuchung_work\MOBIL\` (Ausnahme: Installationen von Werkzeugen, protokolliert). Außerhalb davon löschst und verschiebst du nichts. Den Obsidian-Vault und den Download-Ordner liest du nur. Zugangsdaten, Tokens und Passwörter liest du nicht aus und speicherst sie nirgends.

**L6 — Bestehende Flows bleiben, wie sie sind.** Der Aufräum-Flow und alle anderen Power-Automate-Flows werden nicht geändert. Einen neuen Flow baust du nur, wenn es ohne nicht geht, und dann mit Begründung in `ENTSCHEIDUNGEN.md`. Für das Schreiben von Buchungen ist ein Flow schon einmal bewusst ausgeschlossen worden (Abbruchrisiko, siehe `BRIEFING_Mehrfachspeichern.md`).

**L7 — Belegen statt behaupten.** Jede Aussage über Funktion, Geschwindigkeit oder Korrektheit ist gekennzeichnet als **BELEGT** (mit Beleg), **VERMUTUNG** oder **UNGETESTET**.

---

## 5. Die Arbeitsweise

### 5.1 Ablauf

**Phase 0 — Orientieren und sichern**
1. Schreib dein jetziges Wissen über die Desktop-App in `MOBIL\APP_WISSEN.md`: Datenquellen und Spalten (interne Namen), Schreibschemata für Person und Lookup, Status- und Kollisionslogik, bekannte Fallen, wiederverwendbare Formeln. *Grund:* Dein Kontext wird im Lauf dieser langen Arbeit komprimiert; was nicht in einer Datei steht, ist dann weg.
2. Prüfe, welcher Export der neueste ist und ob er die App-ID `d247d18b-…` enthält (laut `STOPP.md` war das beim 30.09.-Export unklar). Stimmt dein Wissen mit dem neuesten Stand überein?
3. Richte `MOBIL\` als Git-Repository ein.
4. Prüfe deine Werkzeuge: .NET-Version, Plugin, Browser-Zugriff, Anmeldung bei make.powerapps.com. Halte fest, was geht und was nicht.

**Phase 1 — Plan**
5. Schreib `PLAN.md` (Architekturentscheidung, Bildschirmaufbau, Steuerelemente, Variablen, Reihenfolge) und `FEATURES.json` (Abschnitt 5.4). Leg los, sobald der Plan steht; du musst nicht auf Freigabe warten. Gib Josias den Plan in einer kurzen Zusammenfassung im Gespräch.

**Phase 2 — Gerüst**
6. App anlegen, Einstellungen (Hochformat, *Scale to fit* aus, Ausrichtung gesperrt), Datenquellen, Header, Tab-Leiste, Lade-Overlay.

**Phase 3 — Funktionen, eine nach der anderen**, in dieser Reihenfolge, weil Lesen risikolos ist und Schreiben am meisten Sorgfalt braucht:
7. „Meine Buchungen" (nur lesen)
8. „Heute" (lesen, dann Einchecken)
9. Verwalten (verlängern, jetzt beenden, stornieren)
10. „Buchen" mit Frei-Filter und vollem Doppelbuchungsschutz

**Phase 4 — Härten**
11. Unabhängige Prüfung durch Subagenten in frischem Kontext (Abschnitt 5.3), Befunde abarbeiten
12. Komplettdurchlauf aller Tests, Aufräumen der Testdaten

**Phase 5 — Übergabe**
13. `ABNAHME.md`, `ANLEITUNG_JOSIAS.md`, `BEFUNDE_DESKTOP.md`, Abschlussbericht im Gespräch

### 5.2 Ein Schritt nach dem anderen

Arbeite immer an **genau einer** Funktion. Wenn sie fertig ist (kompiliert, zur Laufzeit getestet, dokumentiert, committet), kommt die nächste. Baue nie die ganze App auf einmal und teste dann; das führt in Power Apps zu Fehlerkaskaden, die niemand mehr entwirren kann.

Sichere vor jeder größeren Änderung den Stand (Git-Commit der `.pa.yaml` und/oder Export der Handy-App).

### 5.3 Was „genau prüfen" heißt

Eine Funktion gilt erst als bestanden, wenn alle zutreffenden Stufen erfüllt sind:

| Stufe | Prüfung | Beleg |
|---|---|---|
| P1 | Kompiliert ohne Fehler (`compile_canvas` bzw. App-Prüfung im Studio) | Ausgabe zitieren |
| P2 | Keine neuen Delegationswarnungen, oder jede ist begründet unkritisch | Liste in `TESTPROTOKOLL.md` |
| P3 | Läuft zur Laufzeit: in der veröffentlichten App oder der Vorschau im Browser, **in Handy-Größe** (z. B. Geräteemulation 390 × 844) | Screenshot in `MOBIL\screenshots\` |
| P4 | Bei jeder Schreiboperation: Nachlese in SharePoint (Listenansicht oder REST), ob der Eintrag genau so dasteht wie erwartet, inkl. Person und Tisch | Ergebnis in `TESTPROTOKOLL.md` |
| P5 | Bei jeder Formel, die schreibt, löscht oder Kollisionen prüft: **Angriff durch einen Prüf-Subagenten in frischem Kontext**. Er bekommt nur die Formel, Abschnitt 6 und 7 und den Auftrag, Wege zu einer Doppelbuchung, einer unsichtbaren Buchung, einer falschen Meldung oder einem hängenden Lade-Overlay zu finden. Befunde zur Korrektheit werden behoben oder begründet zurückgewiesen; Stilfragen sind optional. | Fazit des Prüfers in `ENTSCHEIDUNGEN.md` |

Diese Prüfmethode (entwerfen, unabhängig angreifen, verwerfen oder härten) hat in diesem Projekt schon einmal funktioniert, siehe `VERWORFEN_SPEICHERN.md`.

### 5.4 Dokumentation

Josias will jeden Schritt so dokumentiert haben, dass er ihn nachvollziehen und rückgängig machen kann. Alle Dateien in `C:\tischbuchung_work\MOBIL\`:

| Datei | Inhalt |
|---|---|
| `APP_WISSEN.md` | Dein Wissen über die Desktop-App (Phase 0) |
| `PLAN.md` | Architektur und Aufbau; wird aktualisiert, wenn sich etwas ändert |
| `FEATURES.json` | Alle Abnahmekriterien aus Abschnitt 8 **wortgleich**, je mit `id`, `beschreibung`, `prüfung`, `passes` (false/true), `beleg`, `nur_josias` (true für Tests auf echten Geräten). Du darfst Kriterien hinzufügen, aber **keines entfernen, abschwächen oder umformulieren**. |
| `FORTSCHRITT.md` | Chronologisches Protokoll. **Jede Änderung mit Vorher und Nachher**: welche App, welches Steuerelement, welche Eigenschaft, alter Wert, neuer Wert, warum. Dazu jede Installation, jede Einstellung, jeder Fehlschlag. Am Anfang immer ein Abschnitt „Aktueller Stand" mit den nächsten Schritten. |
| `ENTSCHEIDUNGEN.md` | Jede Architektur- und Fachentscheidung: Optionen, Wahl, Grund, Prüferfazit |
| `TESTPROTOKOLL.md` | Jeder Test mit Datum/Uhrzeit, Schritten, Erwartung, Ergebnis, Beleg |
| `TESTDATEN.md` | Jede angelegte Testbuchung, ihr Löschnachweis |
| `FRAGEN_AN_JOSIAS.md` | Alles, was nur Josias entscheiden oder tun kann; oben die dringendsten |
| `BEFUNDE_DESKTOP.md` | Fehler, die dir in der Desktop-App auffallen. **Nur dokumentieren, nicht beheben** (L1). |
| `ANLEITUNG_JOSIAS.md` | Wie er die App öffnet, am Handy testet, aufs Handy legt, an Kollegen freigibt, Änderungen rückgängig macht |
| `ABNAHME.md` | Endbericht: jedes Kriterium mit Status und Beleg |
| `screenshots\` | Belegbilder, sprechend benannt |
| Git | Commit nach jeder abgeschlossenen Funktion, Nachricht auf Deutsch |

Schreib für Josias: Deutsch mit Umlauten, jede Datei beginnt mit höchstens fünf Sätzen Kurzfassung. Er liest lange Texte ungern.

### 5.5 Wenn du festhängst

- **Anmeldung, MFA, Einwilligungsdialog:** Josias muss das am Rechner bestätigen. Schreib es oben in `FRAGEN_AN_JOSIAS.md`, sag es im Gespräch deutlich, und arbeite an allem weiter, was ohne geht.
- **Fehlende Rechte:** Weg dokumentieren, Alternative suchen, sonst `FRAGEN_AN_JOSIAS.md`.
- **Dieselbe Sache scheitert dreimal:** Ansatz verwerfen statt flicken. Josias' Erfahrung in diesem Projekt: Ein Problem zu umgehen oder unmöglich zu machen war immer erfolgreicher als es zu reparieren. Notiere den verworfenen Ansatz in `ENTSCHEIDUNGEN.md`, damit ihn niemand wieder versucht.
- **Werkzeug geht nicht** (z. B. MCP-Verbindung bricht): Rückfallweg wählen, dokumentieren, weiter.

### 5.6 Lange Laufzeit und Kontext

Diese Arbeit dauert lange und dein Kontext wird komprimiert werden. Das ist eingeplant, kein Grund, früher aufzuhören. Behandle die Dateien in `MOBIL\` als dein Gedächtnis: Nach jeder Kompaktierung liest du `FORTSCHRITT.md` („Aktueller Stand"), `FEATURES.json` und die Abschnitte 4, 7 und 8 dieses Auftrags, bevor du weitermachst. Lagere Recherche und große Lesevorgänge an Subagenten aus, damit dein Hauptkontext für das Bauen frei bleibt.

---

## 6. Fachliche Regeln (verbindlich)

Prüfe jede Regel gegen den Quellcode, bevor du sie anwendest. Wenn der Code etwas anderes sagt, gilt der Code, und du schreibst die Abweichung in `ENTSCHEIDUNGEN.md`.

**Datenmodell**
- `Tische`: `Titel` (nicht `Title`), `Geschoss` (Auswahl OG/UG; nicht `Standort`), kein `Aktiv`
- `Tischbuchungen`: `Tisch` (Nachschlagefeld auf `Tische`), `Startzeit`, `Endzeit`, `Person` (Personenfeld), Check-in-Spalte (Anzeigename `CheckedIn`, interner Name `Checkedin`), `SerienID` (vorhanden, ungenutzt)
- Spaltennamen nie raten: Autovervollständigung, `describe_control`/Schema oder REST

**Schreiben**
- Person immer mit vollem Schema, wie es die Desktop-App schreibt (`Claims` mit `i:0#.f|membership|` und kleingeschriebener Mail, `Department`, `DisplayName`, `Email`, `JobTitle`, `Picture`)
- Tisch immer als `{Id; Value}`
- Ein falsch geschriebenes Personen- oder Nachschlagefeld erzeugt eine Buchung, die in keiner Ansicht erscheint, den Tisch aber blockiert. Deshalb P4 bei jeder Schreiboperation.
- `Patch` und `Remove` immer auf einen **frisch** per `LookUp(…; ID = …)` geholten Datensatz, nie auf einen in einer Variablen gespeicherten. Das direkte Entfernen gespeicherter Datensätze ist die wahrscheinliche Ursache des „Item Not Found"-Fehlers in der Desktop-App.
- Jede Schreiboperation in `IfError`, mit deutscher Meldung für jeden Ausgang

**Zeit**
- Überschneidung: `Startzeit < neuesEnde && Endzeit > neuerStart`. Grenzen, die sich berühren, sind keine Überschneidung.
- Status jetzt (wie Grundriss `Rectangle1.Fill`): belegt, wenn `Endzeit >= Now()` und `Startzeit <= Now() + 30 Min`
- Tagesende 22:00, Zeitraster 30 Minuten
- Keine eigenen Zeitzonen-Korrekturen; Power Apps rechnet beim Schreiben selbst um

**Power Fx in dieser App**
- In `.pa.yaml`-Dateien stehen Formeln im **invarianten Format** (Komma als Trennzeichen, `;` zwischen Anweisungen), so wie im Export. Josias' Studio läuft auf **Deutsch** (`;` trennt Argumente, `;;` verkettet, `,` ist Dezimalzeichen). Gibst du Josias eine Formel zum Einfügen, dann in deutscher Schreibweise. Verwechsle die beiden nie.
- Keine Kommentare in Formeln
- `With()`-Felder werden gleichzeitig ausgewertet; Abhängiges braucht verschachtelte `With`
- Variablen typgerecht vorbelegen (nicht mit `Blank()`), eine Variable nie mit zwei verschiedenen Datensatztypen befüllen
- `Set(var; false)` setzt eine Checkbox nicht zurück, dafür `Reset(control)`
- Lade-Overlay (`varIsLoading` o. ä.) wird auf **jedem** Pfad zurückgesetzt, auch nach Fehlern. Ein hängengebliebenes Overlay sperrt die App bis zum Neustart; das ist hier zweimal in Entwürfen passiert.
- `Screen.LoadingSpinner` und eigenes Overlay nicht gleichzeitig (doppelter Spinner in der Desktop-App)
- `Navigate` in `App.OnStart` ist abgekündigt; für Startbildschirm-Logik `App.StartScreen`

**Delegation bei SharePoint** (Microsoft Learn): `=` auf Text, Nachschlage-`Value`, Zahl, Datum delegierbar; `<`/`>` auf Datum delegierbar; auf dem **ID-Feld nur `=`**; Person nur `Email`/`DisplayName`; `IsBlank` und `Not` im Filter nicht delegierbar. Das Datenzeilenlimit der App ist zu prüfen (Export: 1000, Briefing: 2000).

---

## 7. Doppelbuchungen — Anforderungen

In der Desktop-App gibt es sieben bekannte Wege zu falschen Belegungen. Die Handy-App darf **keinen** davon übernehmen. Wie du sie verhinderst, entscheidest du; dass sie verhindert sind, musst du belegen.

| # | Anforderung | Hintergrund aus der Desktop-App |
|---|---|---|
| D1 | Die Kollisionsprüfung fragt SharePoint **mit Zeitgrenze im Filter** ab (Tisch und Zeitraum), nie „alle Buchungen eines Tisches" mit lokalem Nachfiltern. | `btnSpeichernTischePanel`: `Filter(Tischbuchungen; Tisch.Value = …)` ohne Zeitgrenze; ab dem Datenzeilenlimit fehlen Zeilen stillschweigend |
| D2 | Unmittelbar vor jedem Schreiben wird **frisch** gegen SharePoint geprüft, nicht gegen den Stand beim Öffnen des Bildschirms oder Dialogs. Das gilt auch für Verlängern. | Verlängern-Knöpfe prüfen nur beim Färben, beim Speichern nicht |
| D3 | Ein Doppeltipp erzeugt nie zwei Buchungen. | Kein Speichern-Knopf ist während des Speicherns gesperrt |
| D4 | Ein Dialog arbeitet immer mit genau dem Datensatz, den er anzeigt. | Bug B0: Buchungen-Tab-Dialog prüft `varSelectedBuchung` statt `varSelectedBuchungTab` |
| D5 | Eine Person kann nicht zur selben Zeit zwei Tische buchen (V6). | wird nirgends geprüft |
| D6 | Jede geschriebene Buchung erscheint danach in „Heute"/„Meine" und in der Desktop-App. | Ü6: falsche Typen bei Person/Tisch → unsichtbare Buchung |
| D7 | **Gleichzeitige Buchung:** SharePoint hat keine Transaktionen. Zwei Personen, die im selben Moment denselben Tisch buchen, können beide die Prüfung bestehen. Finde den bestmöglichen Schutz, der in dieser Umgebung (SharePoint, ohne Premium) umsetzbar ist, z. B. eine Nachlese nach dem Schreiben mit einer festen Regel, wer bei einer Überschneidung gewinnt. Bewerte ehrlich, was er abdeckt und was nicht, und leg die Regel als Frage an Josias vor. | Verworfene Ansätze und Gründe stehen in `BRIEFING_Mehrfachspeichern.md` (Abschnitt 8, Familie 2B) und `VERWORFEN_SPEICHERN.md`. Lies sie, bevor du D7 entwirfst. |
| D8 | Jede Meldung nach dem Speichern sagt die Wahrheit über das, was in SharePoint steht. „Gebucht" heißt: Die Nachlese hat die Buchung gefunden. | Hauptbefund aller acht verworfenen Entwürfe: Meldung kam aus einer lokalen Zählung |

Die Prüfregeln (Überschneidungsformel, Status, 22:00, Raster, Schreibschemata) müssen in Handy- und Desktop-App **wortgleich** sein. Führe sie in `APP_WISSEN.md` unter „Geteilte Regeln" auf. Weichen sie in der Desktop-App ab, notiere das in `BEFUNDE_DESKTOP.md`.

---

## 8. Abnahmekriterien

Übernimm diese Kriterien wortgleich in `FEATURES.json`. Jedes braucht einen Beleg nach Abschnitt 5.3.

**Grundlagen**
- A01 Die Handy-App ist eine eigene App mit eigenem Namen und eigener App-ID; die ID steht in `ABNAHME.md`.
- A02 Die produktive App „Tischbuchung" (`d247d18b-…`) ist nachweislich nicht verändert: Ihre Versionsliste (Details → Versionen) zeigt keine Version, die in deinem Arbeitszeitraum von dir gespeichert oder veröffentlicht wurde. Halte die Versionsliste zu Beginn und am Ende fest. (Achtung: Schon das Öffnen im Studio kann „Zuletzt geändert" verschieben, das ist kein Beleg.)
- A03 Hochformat, *Scale to fit* aus, Ausrichtung gesperrt; die App füllt in der Geräteemulation 390 × 844 und 360 × 800 die Breite ohne horizontales Scrollen (Screenshots).
- A04 Die letzte Kompilierung bzw. App-Prüfung zeigt 0 Fehler.
- A05 Alle Delegationswarnungen sind aufgelistet und jede ist behoben oder begründet unkritisch.

**Header und Navigation**
- A06 Header mit Logo, App-Name, Initialen; Aktualisieren lädt die Daten neu und meldet das.
- A07 Tab-Leiste unten mit „Heute", „Buchen", „Meine Buchungen"; der aktive Tab ist erkennbar; Tabwechsel schließt offene Dialoge.

**Heute**
- A08 Zeigt genau die eigenen Buchungen von heute, die noch nicht vorbei sind, sortiert nach Startzeit.
- A09 Status je Karte stimmt mit der Grundriss-Logik der Desktop-App überein (gleiche Buchung, gleicher Zeitpunkt, gleiches Ergebnis).
- A10 Einchecken ist nur im Zeitfenster V2 möglich, braucht einen Tipp, setzt die Check-in-Spalte in SharePoint (Nachlese) und kann durch einen zweiten Tipp nicht auschecken.
- A11 Keine Buchung heute: klarer Hinweis und direkter Weg zum Buchen.

**Buchen**
- A12 Reihenfolge Datum → Uhrzeit → Tisch; die Tischauswahl zeigt nur Tische, die im gewählten Zeitraum frei sind, ohne Big Table.
- A13 Eine Zusammenfassung zeigt vor dem Buchen Tisch, Tag und Zeit.
- A14 Nach erfolgreicher Buchung steht der Eintrag korrekt in SharePoint (Person, Tisch, Start, Ende; Nachlese) und erscheint in „Heute"/„Meine" und in der Desktop-App.
- A15 Ungültige Eingaben (Ende ≤ Start, Vergangenheit, nach 22:00) werden verständlich abgewiesen.

**Meine Buchungen und Verwalten**
- A16 Zeigt alle eigenen kommenden Buchungen chronologisch mit Wochentag.
- A17 Verlängern um +1/+2 Std prüft beim Speichern frisch und lehnt eine Kollision oder ein Ende nach 22:00 ab.
- A18 „Jetzt beenden" setzt die Endzeit, der Tisch ist danach in der Tischauswahl wieder frei.
- A19 Stornieren mit Bestätigung; eine bereits anderswo gelöschte Buchung führt zu einer verständlichen Meldung, nicht zu einem Netzwerkfehler.

**Doppelbuchungen (Abschnitt 7) — jedes mit eigenem Test**
- A20 D1 belegt (Abfrage mit Zeitgrenze, im Code gezeigt)
- A21 D2: Tisch im Handy auswählen, dann am Desktop oder per zweitem Fenster denselben Tisch im selben Zeitraum buchen, dann am Handy buchen → abgelehnt, keine zweite Buchung in SharePoint
- A22 D3: Doppeltipp auf Buchen → genau eine Buchung
- A23 D4 belegt
- A24 D5: eigene Buchung 08–12 an Tisch A, dann 10–14 an Tisch B → abgelehnt
- A25 D6: siehe A14
- A26 D7: Schutz umgesetzt, getestet, ehrlich bewertet; die Regel liegt als Frage in `FRAGEN_AN_JOSIAS.md`
- A27 D8: jede Erfolgsmeldung stammt aus einer Nachlese, im Code gezeigt
- A28 Ein Prüf-Subagent in frischem Kontext hat alle schreibenden Formeln angegriffen; alle Korrektheitsbefunde sind behoben oder begründet zurückgewiesen.

**Robustheit**
- A29 Bei jedem Fehlerpfad verschwindet das Lade-Overlay wieder (mindestens getestet: Kollision, Fehler beim Schreiben, gelöschter Datensatz).
- A30 Kein Weg führt zu einer rohen englischen Fehlermeldung.

**Übergabe**
- A31 Alle Testbuchungen aus `TESTDATEN.md` sind gelöscht (Nachlese).
- A32 Alle Dateien aus Abschnitt 5.4 existieren und sind aktuell; der letzte Git-Commit enthält den Endstand.
- A33 `ANLEITUNG_JOSIAS.md` enthält den Link zur App (mit Umgebungs-ID), die Schritte zum Test auf iPhone und Android (Browser und Power Apps Mobile), zum Freigeben und zum Zurückrollen.

**Nur durch Josias (zählen nicht für dein Ziel, müssen aber in `ANLEITUNG_JOSIAS.md` als Checkliste stehen)**
- J1 Test auf einem echten iPhone und einem echten Android-Gerät
- J2 Freigabe an eine Testgruppe
- J3 Entscheidung zu V1–V9 und zur Regel aus D7

---

## 9. Hintergrundmaterial

Im Ordner `C:\tischbuchung_work\MOBIL\hintergrund\` (vom Chat-Claude, nicht bindend):
- `Bauplan_Handy-App_Tischbuchung_2026-10-06.md`: Vorschlag für Aufbau und Steuerelemente, Befunde zur Desktop-App (Stand 30.09.)
- `Analyse_Handy-Ansicht_Tischbuchungs-App_2026-10-06.md`: Recherche zu Handy-Layouts in Power Apps (mit Korrektur-Hinweis oben)

In `C:\tischbuchung_work\`: `INVENTAR.md`, `BRIEFING`-Unterlagen, `ENTWURF_*`, `VERWORFEN*`, `OFFENE_FUNDE.md`, `STOPP.md`, die Exporte und `src\`. Weitere Notizen und Journale liegen in Josias' OneDrive (Obsidian-Vault „Technoform Jornals") und im Download-Ordner.

Hilfreiche Quellen:
- Canvas Authoring MCP / Plugin: https://github.com/microsoft/power-platform-skills
- Responsive Layouts: https://learn.microsoft.com/power-apps/maker/canvas-apps/create-responsive-layout
- Delegation SharePoint: https://learn.microsoft.com/power-apps/maker/canvas-apps/connections/connection-sharepoint-online

---

## 10. Zum Schluss

Wenn du fertig bist, gib im Gespräch einen Abschlussbericht aus: jedes Kriterium A01–A33 mit Status und Beleg, die App-ID und den Link, die offenen Fragen an Josias und die Befunde zur Desktop-App in drei Sätzen. Dieser Bericht ist das, woran dein Ziel gemessen wird.

Josias vertraut dir hier viel an. Bau etwas, das du selbst gern übergeben würdest.
