# CLAUDE.md – Tischbuchungs-App (Power Apps Canvas, SharePoint) · Verbesserungsprojekt

Stand: 07.10.2026. Übergabe aus einer Analyse-Sitzung vom 06.10.2026. Alles hier ist **belegt** (Export/Messung/Doku), außer es steht ausdrücklich „geschlussfolgert“ oder „UNSICHER“ dabei.

## 1. Rahmen
- **Josias** (Werkstudent Digitalisierung, Technoform), einziger Entwickler. Will ehrliche, kurze Antworten, kleine Schritte, **vollständige** Formeln zum Einfügen, keine Rückfragen ohne Not. Liest lange Texte ungern.
- App „Tischbuchung“ (ersetzt GoBright), Umgebung „Personal Productivity“. Richtige App-ID `d247d18b-d36f-4a44-975a-7839695b2f12`. Es gibt Klone „App“ und „App – Kopie“ – nicht verwechseln.
- Listen: `Tischbuchungen` (~250 Einträge), `Tische` (OG 16, UG 18 inkl. „Big Table“), dazu toter Raumcode auf `Räume`/`Raumbuchungen`.
- **Go-Live: 14.10.2026.** Last: Montag ~8 Uhr viele Nutzer gleichzeitig.
- Prioritäten (Josias): 1. Korrektheit (keine Doppelbuchungen, keine Lags, keine rohen Fehler), 2. Ladezeit, 3. Speichern/Stornieren bei Mehrfachauswahl.
- Claude kann Studio nicht bedienen. Josias fügt jede Formel selbst ein und testet. Claude liest den Export.

## 2. Arbeitsweise (bewährt)
1. Josias exportiert die App (zip). Entpacken: zip → `Microsoft.PowerApps/apps/<id>/*-document.msapp` → nochmal entpacken (Backslash-Pfade, Warnung ignorieren) → `Src/Screen1.pa.yaml`, `Src/App.pa.yaml`, `References/DataSources.json`, `Properties.json`. YAML mit `yaml.BaseLoader` lesen (sonst Fehler an `Items.Value: =Value`).
2. Der Export ist in **englischer** Schreibweise (`,` / `;`). Josias arbeitet **deutsch**. Formeln **nie von Hand übersetzen**: `tools/build.py` enthält `to_de()` (Zeichenketten und `'…'` unangetastet, `;`→`;;`, `,`→`;`, Dezimalpunkt→Komma).
3. Formeln immer **aus dem Export erzeugen**, dann automatisch gegen das Original vergleichen (nur gewollte Änderungen?), Klammern prüfen.
4. Messen mit dem **Livemonitor**, Auswertung mit `tools/monitor.py`. Im JSON ist `time` das **Ende** der Antwort (= `response.endTime`). Dauer nicht doppelt zählen.
5. Wichtige Übergaben vor dem Einfügen von einem **unabhängigen Agenten** prüfen lassen (frischer Kontext, nur Dateien + Prüfauftrag). Hat am 06.10. vier echte Fehler gefunden.
6. Vor jeder Übergabe prüfen, ob der Export dem aktuellen Studio-Stand entspricht. Ganze Properties ersetzen überschreibt sonst still Josias’ Änderungen.

## 3. Formelregeln (alle schon einmal verletzt)
- Deutsch: `;` trennt, `;;` verkettet, `,` Dezimal. **Immer die ganze Property** liefern, nie Teilstücke.
- Keine Kommentare in Verhaltensformeln (in `App.Formulas` sind `//` erlaubt und vorhanden).
- `With()`-Felder werden gleichzeitig ausgewertet; Abhängiges verschachteln.
- Lookup-Spalte schreiben `{Id: …; Value: …}`, Person mit vollem Schema (Claims, Department, DisplayName, Email, JobTitle, Picture). **Belegt 06.10.:** Sammel-Patch schreibt beides korrekt **ohne** `'@odata.type'`.
- `Patch` auf frisches `LookUp(…; ID = …)`, nicht auf Variable. Eine Variable nie mit zwei Record-Typen füllen.
- `Set(var; false)` setzt keine Checkbox zurück → `Reset(control)`.
- Steuerelement- und Spaltennamen nie raten – im Export nachsehen.
- `btnSpeichern` und `btnSpeichernTischePanel` sind im Rechenteil gleich, im Aufräumteil **nicht** (12 vs. 23 Anweisungen).
- Unsichtbar ≠ nicht berechnet: versteckte Steuerelemente fragen trotzdem Daten ab (gemessen).
- `Now()` wird nur neu berechnet, wenn sich sonst etwas in der Formel ändert (MS Learn).
- App-Einstellungen: `powerfxv1 = false`, Formel-Fehlerbehandlung an, **nicht blockierendes OnStart** an (OnStart läuft parallel zu Bildschirmformeln).

## 4. Fakten aus dem Export (Stand 06.10.2026, 14:38)
- Ein Screen `Screen1`. Spalte heißt `Titel` (nicht `Title`).
- `Tischbuchungen`: `Tisch` (Lookup, **Pflicht**, Filter `eq`), `Person` (Person, Filter `eq` auf Email/DisplayName), `Startzeit`/`Endzeit` (DateTime, eq/gt/ge/lt/le/ne), `Checkedin` (Anzeigename `CheckedIn`), `SerienID` (Text, eq/startswith, **wird nirgends geschrieben**). Filter unterstützt `and`/`or`.
- Namen, die früher falsch kursierten: Panel-Endzeit heißt **`ddEndTischePanel`** (nicht `ddEndeTischePanel`). Panel-Bis-Datum `dpWiederholenBis_1`. Schließen im kleinen Verwalten-Dialog: `btnSchließenKlein` (leert die Auswahl).
- Grundriss: **eine** Galerie `Gallery1` (OG/UG über `Items = Filter(Tische; Geschoss.Value = varAusgewaehltesStockwerk)`), Kachel = `Rectangle1`, `Circle1`, `Label1`, `btnHitArea`.
- Schreibstellen auf `Tischbuchungen` (8): `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern` (Grundriss), `btnVerlängern_1` (Tab), `btnStornieren` (Grundriss), `btnStornieren_1` (Tab), `btnStornierenKlein` (Mehrfach), `btnEinchecken`.
- `Refresh(Tischbuchungen)` (9): `Icon1`, `Icon1_1`, `Image6`, `btnHitArea_1` (Aktualisieren), `btnSpeichern`, `btnSpeichernTischePanel`, `btnVerlängern_1`, `btnStornieren_1`, `btnStornierenKlein`.
- Datum: `varAnsichtsDatum` nur in `App.OnStart` und `dpAnsichtsDatum.OnChange`. Stockwerk nur in `App.OnStart` und `ddStockwerk.OnChange`.
- `btnSpeichern` enthält bereits Josias’ **Sammel-Patch** (`Patch(Tischbuchungen; ForAll(neueDatensaetze; Defaults(Tischbuchungen)); neueDatensaetze)`), `btnSpeichernTischePanel` noch die alte `ForAll`-Schleife. Keiner der beiden hat eine Doppelklick-Sperre.
- `colAusgewaehlteBuchungen` enthält ganze Datensätze (`Collect(…; ThisItem)`). `conVerwaltenKlein` ist fest 400×150.
- **K1 nicht eingebaut:** `btnVerwalten_2` setzt nur `varSelectedBuchungTab`; 12 Plus/Minus-Properties im Tab lesen `varSelectedBuchung` → stille Doppelbuchung **B0** möglich.
- Serienfenster ist Start + 14 Tage = **15 Tage** (gemessen: 06.–20.10. → 11 Werktage).

## 5. Messbefunde (Livemonitor 06.10., veröffentlichte App, 1 Nutzer, OG)
| Vorgang | Abfragen | Dauer |
|---|---|---|
| App-Start | ~150 (Grundriss ~102, Raumcode 36) | Netz ruhig nach 2,5–3,4 s |
| Aktualisieren | 103 (1 Grundriss-Welle) | 1,7 s |
| Einzelbuchung | 190 (2 Wellen: Schreiben + Refresh) | 2,6–4,6 s |
| Serie 11 Termine | 1.020 (12 Wellen = 11 Schreibvorgänge + 1 Refresh) | **~101 s**, Antwortzeiten Median 31 s, max 97 s, kein 429 |
- Ursache: Jede Kachel macht **6 eigene SharePoint-Abfragen** (`Rectangle1.Fill`, `Circle1.Fill`, `Circle1.BorderColor`, `Label1.Text` = 4× dieselbe Frage, + 2× `Circle1.BorderStyle`), `Now()` in jeder URL → kein Cache. **Jeder** Schreibvorgang löst eine volle Welle aus, auch beim Sammel-Patch.
- Das Schreiben selbst ist schnell: Kollisionsabfrage 0,2–1,7 s, `createRow` 0,25–0,47 s; Serie 11× `createRow` ≈ 1,6 s, gestaffelt/parallel.
- Versteckter Grundriss-Verwalten-Dialog (`btnPlus3Std` u. a.) lädt bei leerer `varSelectedBuchung` die **ganze Liste** (~250 Zeilen, ~290 KB) pro Aktualisierung; dazu Abfragen mit `ID eq null` / `Tisch eq null`.
- `Tische` wird 4× geladen (`TischNrOG`, `TischNrUG`, `Gallery1.Items`, `ddTischePanel.Items`).
- SharePoint-Limit 600 Aufrufe/60 s **pro Verbindung = pro Nutzer** (MS Learn).
- Monitor-Dateien: `PowerAppsTraceEvents.json` (Start, Aktualisieren, 2 Einzelbuchungen über Panel), `PowerAppsTraceEvents_1.json` (Start, Serie über Grundriss-Dialog). Liegen bei Josias.

## 6. Stand der Arbeit
### Fertig: L2 „Grundriss aus Collection“ – `UEBERGABE_Grundriss_L2_v0.3.md`
- Kacheln lesen aus `colGrundriss` (flach: `TischName`, `Startzeit`, `Endzeit`, `Eingecheckt`, `Name`), geladen mit **einer** delegierten Abfrage an 15 Stellen (OnStart am **Ende**, Datum, Stockwerk, 4× Aktualisieren, 8 Schreibstellen). Filter: Tag überlappend **oder** jetzt bis +60 min. Ersetzt `colGrundriss` nur bei Erfolg (`IsError(neu) || IsError(First(neu))`).
- Bewusst unverändert: `btnHitArea.OnSelect`, Kollisionsprüfungen, Listen-Galerien, alle `Refresh`.
- Schritt A (15 Ladestellen, unsichtbar) → Schritt B (5 Kachel-Properties). Erwartung: Einzelbuchung ~15 statt 190, Serie ~45 statt 1.020.
- Unabhängig geprüft (Urteil: einfügebereit nach Korrekturen, eingearbeitet). Gegen Export 06.10. 14:38 abgeglichen: alle 20 Properties unverändert. **Noch nicht eingefügt/getestet.** Status bei Josias erfragen.
- Verworfen: benannte Formel statt Collection (bekanntes MS-Problem mit nicht aktualisiertem Cache; für nach Go-Live).

### Offen (Backlog, Vorschlag zur Reihenfolge)
1. **L2 einbauen und messen** (Josias, mit Übergabe v0.3).
2. **K1** – `Set(varSelectedBuchung; ThisItem)` zusätzlich in `btnVerwalten_2` (Nicht-Auswahl-Zweig). Eine Zeile, schließt B0. Risiko: eine Variable bedient dann zwei Dialoge → in beide Richtungen testen.
3. **L3** – versteckte Dialoge nur rechnen lassen, wenn offen (`If(varZeigeVerwalten; …)` bzw. leere Variable abfangen). Beseitigt Ganze-Liste-Download und `eq null`-Abfragen.
4. **L4** – Raumcode stilllegen (`galRäume.Items`, `btnSlot1–4`, `recBuchungDavor1/Danach1`, `Label4/5`, `galRaumbuchungenHeute`): Start −36 Abfragen. Vorher bestätigen lassen, dass Raumbuchung wirklich nicht gebraucht wird.
5. **Doppelklick-Sperre** (`DisplayMode: If(varIsLoading; DisplayMode.Disabled; DisplayMode.Edit)`) an beiden Speichern-Knöpfen.
6. **Mehrfachauswahl zum Go-Live ausblenden** (Josias’ Idee, zu bestätigen) – Mehrfach-Verlängern (B) wird vor Go-Live **nicht** gebaut.
7. Serienbuchung ehrlich machen (nach Go-Live): `SerienID` schreiben + Nachlese; Panel-Knopf auf Sammel-Patch; „eigene Überschneidung“ ≠ „hatte schon“; Fehler Enddatum < Startdatum (`dpWiederholenBis` ohne DefaultDate).
8. Weitere „Wehwehchen“: Josias hat einen eigenen Bericht angekündigt – einarbeiten.
9. Livemonitor **aus Studio** öffnen (Erweiterte Tools → Livemonitor öffnen), damit ohne Veröffentlichen gemessen werden kann – Josias hat den Menüpunkt noch nicht gefunden.

## 7. Fehler, die passiert sind (nicht wiederholen)
- Namen aus Briefing übernommen statt im Export geprüft (`ddEndeTischePanel`).
- Teilersatz statt ganzer Property geliefert.
- Reihenfolge, die einen falschen Zwischenzustand erzeugt (Kacheln vor Ladestellen umstellen).
- Ladezeile mitten in OnStart (blockiert nachfolgende `Set`).
- Monitor-Dauern doppelt gezählt.
- Behauptungen als Fakt verkauft, die nur geschlussfolgert waren. Immer kennzeichnen: belegt / geschlussfolgert / UNSICHER.

## 8. Dateien in diesem Paket
- `UEBERGABE_Grundriss_L2_v0.3.md` – die Übergabe zum Einfügen.
- `tools/build.py` – erzeugt die 20 L2-Formeln aus `<export>/Src` → `out.json` (inkl. `to_de()`, Klammerprüfung).
- `tools/doc.py` – erzeugt die Übergabe aus `out.json`.
- `tools/monitor.py` – Livemonitor-Export auswerten (Anfragen je Aktion, Quellen, Steuerelemente).
- `out.json` – die 20 Formeln (deutsch, neu + Original).
- `BRIEFING_Mehrfachspeichern.md` – Vorgeschichte (Stand 06.10. morgens; teils überholt, siehe Abschnitte 4–7 hier).
