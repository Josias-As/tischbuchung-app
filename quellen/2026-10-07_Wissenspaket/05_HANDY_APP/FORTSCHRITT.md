# FORTSCHRITT.md — Arbeitsprotokoll Handy-App

**Kurzfassung:** Hier steht jeder Schritt mit Vorher und Nachher. Ganz oben der aktuelle Stand, darunter das Protokoll in zeitlicher Reihenfolge. Wenn mein Kontext komprimiert wurde, lese ich zuerst „Aktueller Stand", dann `FEATURES.json`, dann die Abschnitte 4, 7 und 8 von `AUFTRAG_MOBIL.md`. In Power Apps wurde nur die neue Handy-App angelegt und bearbeitet; die produktive App ist unberührt.

---

## Aktueller Stand

**Phase:** 3 (Funktionen) — alle drei Bereiche gebaut, Schreibtests stehen aus

**Die App ist funktional vollständig gebaut.** „Tischbuchung Handy", App-ID `e218702e-35cb-4dc8-813a-b9fd860c7f72`. Gerüst, Kopfzeile, Tab-Leiste, Lade-Overlay, „Heute" (mit Einchecken), „Buchen" (Datum → Uhrzeit → freier Tisch → Buchen mit Doppelbuchungsschutz), „Meine", Verwalten-Dialog (+1/+2 Std, Jetzt beenden, Stornieren) und Storno-Bestätigung. Alles gespeichert, **nicht veröffentlicht**.

**Fertig und belegt:**

| | |
|---|---|
| A01 | App angelegt, eigene ID — **bestanden** |
| A02 | Ausgangs-Versionsliste der produktiven App gesichert (höchste Version 23) — Teil 1 von 2 |
| A03 | 390 × 844 und 360 × 800 geprüft, kein horizontales Scrollen — Teilabweichung Ausrichtungssperre, E-04 |
| A04 | App-Prüfung: **keine Formelbefunde** (Stand nach Buchen, 16:15) |
| A05 | **keine Delegationswarnung**; drei Leistungshinweise, alle begründet unkritisch (TESTPROTOKOLL) |
| A12 | Tischauswahl zeigt nur freie Tische ohne Big Table — **mit SharePoint gegengeprüft** |
| A13 | Zusammenfassung Tisch, Tag, Zeit vor dem Buchen — Screenshot |
| A16 | „Meine" — **Vollständigkeit gegen SharePoint belegt** (23 von 23 IDs, gleiche Reihenfolge) |

**Als Nächstes (in dieser Reihenfolge):**
1. Testbuchungen nach `TESTDATEN.md` anlegen und alle Schreibwege zur Laufzeit prüfen (A14, A15, A17–A19, A21, A22, A24, A26, A29, A30), jede mit P4-Nachlese per REST-Lesezugriff
2. Prüf-Subagent in frischem Kontext auf alle schreibenden Formeln (A28)
3. Barrierefreiheitshinweise durchsehen, ANLEITUNG_JOSIAS.md, ABNAHME.md
4. Testbuchungen löschen und nachlesen (A31), Versionsliste der produktiven App prüfen (A02 Teil 2)

**Werkzeug für Nachlesen:** Ein reiner GET auf die SharePoint-REST-Schnittstelle im Browser (`/_api/web/lists/getbytitle('Tischbuchungen')/items?...`) liefert die Zeilen unabhängig von meiner App. Liest nur, schreibt nichts. Höchste ID vor meinen Tests: **495**.

---
## Frühere Stände

**Phase 0 erledigt:**
- `MOBIL\` ist ein Git-Repository (Git 2.53.0 über GitHub Desktop, nicht im PATH)
- `APP_WISSEN.md` geschrieben: Datenmodell, Schreibschemata, geteilte Regeln, 14 Fallen der Desktop-App, alles mit Fundstelle aus dem Export vom 06.10.2026
- `FEATURES.json` angelegt mit A01–A33 und J1–J3 wortgleich aus Abschnitt 8
- Auftrag gegen den Quellcode geprüft, fünf Abweichungen gefunden (siehe `ENTSCHEIDUNGEN.md` E-A09 und `BEFUNDE_DESKTOP.md`)
- Werkzeuge erfasst: Node v24.21.0 ✓, Chrome ✓, Git ✓ (nur über GitHub Desktop), **.NET SDK fehlt**, **pac CLI fehlt**

- **A02-Ausgangsbeleg gesichert:** Versionsliste der produktiven App am 06.10.2026 um ca. 14:35 Uhr, höchste Version = **23**. Screenshot `screenshots\A02_versionsliste_produktiv_BEGINN_2026-10-06_1435.jpg`
- Hintergrundmaterial ausgewertet (Subagent): enthält **keine fertigen Formeln**, nur Planung
- Chrome-Zugriff auf make.powerapps.com steht, Josias ist angemeldet

- `PLAN.md` geschrieben (Phase 1 abgeschlossen)
- **Die Handy-App existiert:** „Tischbuchung Handy", App-ID `e218702e-35cb-4dc8-813a-b9fd860c7f72`, angelegt 06.10.2026 um 14:46:21, Lizenz Standard. **A01 erfüllt.**
- App-Layout auf „Dynamisch" gesetzt (Scale to fit aus), Hochformat. Dabei Zielkonflikt in A03 gefunden, siehe `ENTSCHEIDUNGEN.md` E-04

**Läuft gerade:**
- Installation .NET 10 SDK über winget (Hintergrund, noch nicht abgeschlossen)

**Nächste Schritte:**
1. Datenquellen `Tischbuchungen` und `Tische` hinzufügen
2. Gerüst: `conRoot`, Header, Tab-Leiste, Lade-Overlay
3. „Meine Buchungen" (nur lesen) als erste Funktion
4. .NET-Installation prüfen; wenn sie scheitert, über die Code-Ansicht im Studio arbeiten

**Offene Blocker:** keine

**Wichtiger Fund, der Josias betrifft:** Die Desktop-App hat seit meiner Analyse drei neue Versionen bekommen (siehe unten, Abschnitt „A02"). Meine Übergabe-Dokumentation beschreibt Version 20, nicht den heutigen Entwurfsstand.

---

## Protokoll

### 2026-10-06 — Phase 0 begonnen

**Ausgangslage.** Ich habe in der vorangegangenen Sitzung die Desktop-App vollständig dokumentiert; das Ergebnis liegt in `C:\tischbuchung_work\UEBERGABE_2026-10-06\` (186 Steuerelemente, 1985 Properties, per Skript extrahiert und verifiziert). Dieses Wissen ist die Grundlage für die Handy-App. Die Übergabe-Dokumentation ist aktueller und genauer als das Material in `hintergrund\`, das auf dem Export vom 30.09. beruht.

**Prüfung des Auftrags gegen den Quellcode.** Bevor ich etwas gebaut habe, habe ich jeden Steuerelement-, Spalten- und Variablennamen aus `AUFTRAG_MOBIL.md` gegen `UEBERGABE_2026-10-06\src\` geprüft.

Bestätigt: `galTischbuchungenHeute`, `conTischBuchungenPanel`, `conBuchungen`, `conGrundriss`, `btn5Std`, `btn9Std`, alle Farbwerte, `Checkedin`/`CheckedIn`, `SerienID` ungenutzt, Überschneidungsformel, 30-Minuten-Fenster, 22:00-Grenze, 30-Minuten-Raster, Befund B0, doppelter Spinner, Kosten der Schnellwahl-Knöpfe.

Abweichungen (fünf), im Einzelnen dokumentiert in `ENTSCHEIDUNGEN.md` und `BEFUNDE_DESKTOP.md`:
1. A09 ist mehrdeutig (Grundriss-Status gegen Karten-Status) → E-A09
2. `Titel` ist Anzeigename, intern `Title` → in `APP_WISSEN.md` präzisiert
3. `Geschoss` als „Auswahl" bezeichnet, Metadaten deuten auf Nachschlagefeld → UNSICHER vermerkt
4. D1 nennt nur `btnSpeichernTischePanel`, `btnSpeichern` hat denselben Fehler → `BEFUNDE_DESKTOP.md` BD-01
5. `STOPP.md` existiert nicht mehr (von mir gelöscht, nachdem der gültige Export vorlag); die Frage dahinter ist in `UEBERGABE_2026-10-06\VERIFIKATION.md` beantwortet

**Datenzeilenlimit korrigiert.** Der Auftrag nennt „Export: 1000, Briefing: 2000" und lässt die Prüfung offen. Geprüft: `src/Properties.json` enthält `"DefaultConnectedDataSourceMaxGetRowsCount": 1000`. **Es gilt 1000.**

**Git eingerichtet.**
- Vorher: `C:\tischbuchung_work\MOBIL\` war kein Repository
- Nachher: `git init` ausgeführt, `user.name` = „Claude (Handy-App)", `user.email` = Josias' Adresse, Ordner `screenshots\` angelegt
- Hinweis: Git liegt nur unter `C:\Users\JAssefaw\AppData\Local\GitHubDesktop\app-3.6.6\resources\app\git\cmd\git.exe`. Der Pfad enthält die Versionsnummer und ändert sich bei einem Update von GitHub Desktop.

**Werkzeugprüfung.**

| Werkzeug | Stand |
|---|---|
| Node | v24.21.0, im PATH |
| Chrome | vorhanden |
| Git | 2.53.0, nur über GitHub Desktop |
| .NET SDK | **fehlt** — Installation gestartet |
| pac CLI | **fehlt** |

**Dateien angelegt (neu, vorher nicht vorhanden):** `APP_WISSEN.md`, `FEATURES.json`, `FORTSCHRITT.md`, `ENTSCHEIDUNGEN.md`, `BEFUNDE_DESKTOP.md`, `FRAGEN_AN_JOSIAS.md`, `TESTDATEN.md`, `TESTPROTOKOLL.md`, Ordner `screenshots\`.

**Installationen.** .NET 10 SDK über `winget install --id Microsoft.DotNet.SDK.10` (Ergebnis wird hier nachgetragen).

**An Power Apps wurde nichts verändert.** Keine App im Studio geöffnet, keine Einstellung geändert, keine Buchung angelegt.

---

### 2026-10-06, ca. 14:35 — A02: Versionsliste der produktiven App zu Beginn

**Gelesen über das Portal, nicht über das Studio.** Weg: Apps → Zeile „Tischbuchung" → Weitere Befehle → Details → Reiter Versionen. Die URL bestätigt dabei die App-ID: `…/apps/d247d18b-d36f-4a44-975a-7839695b2f12/versions`. Das ist die richtige App, nicht einer der Klone.

**Beleg:** `screenshots\A02_versionsliste_produktiv_BEGINN_2026-10-06_1435.jpg`

**Höchste Version zu Beginn meiner Arbeit: Version 23.**

| Version | Geändert | Von | Release | Veröffentlicht |
|---|---|---|---|---|
| 23 | 6.10.2026, 14:12:58 | Josias Assefaw | 3.26093.10 | |
| 22 | 6.10.2026, 14:09:32 | Josias Assefaw | 3.26093.10 | |
| 21 | 6.10.2026, 14:08:28 | Josias Assefaw | 3.26093.10 | |
| 20 | 5.10.2026, 13:58:19 | Josias Assefaw | 3.26093.10 | **Live** |
| 19 | 1.10.2026, 09:55:53 | Josias Assefaw | 3.26093.9 | |
| 18 | 1.10.2026, 09:53:25 | Josias Assefaw | 3.26093.9 | |
| 17 | 30.9.2026, 10:53:57 | Josias Assefaw | 3.26092.12 | |
| 16 bis 1 | 30.9.2026, 01:24:46 bis 09:28:49 | Josias Assefaw | 3.26092.12 | |

**Prüfkriterium für das Ende:** Es darf keine Version 24 oder höher geben, die von mir stammt. Alle 23 Versionen oben sind von Josias und liegen vor dem Beginn meiner Arbeit in Power Apps.

#### Zwei Erkenntnisse daraus

**1. Mein Exportstand ist Version 20, die veröffentlichte.** Der Zeitstempel von Version 20 (5.10.2026, 13:58:19 Ortszeit) entspricht exakt der `appVersion` meines Exports (`2026-10-05T11:58:19Z`, also 13:58:19 bei UTC+2). Das bestätigt rückwirkend: Ein Exportpaket liefert immer die **veröffentlichte** Version. Deshalb war der erste Export vom 06.10. um 11:03 inhaltlich der Stand vom 30.09. — zu dem Zeitpunkt war noch eine ältere Version live.

**2. Die Desktop-App hat sich seit meiner Analyse geändert.** Die Versionen 21, 22 und 23 sind heute zwischen 14:08:28 und 14:12:58 entstanden, also **nach** meinem Export um 11:28 und während ich an der Dokumentation gearbeitet habe. Sie stammen von Josias, nicht von mir; ich hatte Power Apps zu dieser Zeit nicht geöffnet.

**Folge, ehrlich benannt:** Die Übergabe-Dokumentation in `C:\tischbuchung_work\UEBERGABE_2026-10-06\` und alles, was ich in `APP_WISSEN.md` und `BEFUNDE_DESKTOP.md` über die Desktop-App schreibe, beschreibt **Version 20**. Was Josias in den Versionen 21 bis 23 geändert hat, weiß ich nicht. Diese drei Versionen sind nicht veröffentlicht, lassen sich also auch nicht per Exportpaket holen.

**Nachtrag, Auskunft von Josias am 06.10.2026:** Die Versionen 21 bis 23 enthalten „nur kleine Änderungen wie Basiskreisgröße etwas größer gemacht, 3 bis 4 solcher Änderungen". Das sind Layoutwerte in `App.Formulas` (`BasisKreisgroesse` und Verwandte). **Keine der geteilten Regeln ist davon berührt** — Überschneidungsformel, Schreibschemata, Statuslogik, 22:00-Grenze und das 30-Minuten-Raster bleiben wie dokumentiert. Die Befunde in `BEFUNDE_DESKTOP.md` bleiben damit ebenfalls gültig. Eingestuft als **VERMUTUNG** gestützt auf Josias' Auskunft, nicht am Quellcode nachgeprüft, weil die Versionen 21 bis 23 nicht veröffentlicht und damit nicht exportierbar sind.

**Was das praktisch bedeutet:**
- Für die Handy-App ist das Risiko gering (durch Josias' Auskunft oben inzwischen weiter entschärft). Ich übernehme aus der Desktop-App nur die geteilten Regeln (Überschneidungsformel, Schreibschemata, Farben, 22:00, 30-Minuten-Raster). Dass Josias ausgerechnet daran etwas geändert hat, ist unwahrscheinlich, aber nicht ausgeschlossen.
- Für `BEFUNDE_DESKTOP.md` gilt: Jeder Befund ist auf Version 20 belegt. Möglicherweise hat Josias einen davon inzwischen behoben.
- **Keine Maßnahme von mir**, weil L1 mir verbietet, die produktive App anzufassen, und ein Export nur die Live-Version liefert. Ich habe es Josias im Gespräch gesagt.

---

### 2026-10-06, 14:46 — Phase 2: Die Handy-App ist angelegt

**Vorher:** Es gab drei Apps in der Umgebung (`Tischbuchung`, `App`, `App – Kopie`).
**Nachher:** Es gibt vier. Neu ist `Tischbuchung Handy`.

| | |
|---|---|
| Name | Tischbuchung Handy |
| App-ID | `e218702e-35cb-4dc8-813a-b9fd860c7f72` |
| Erstellt | 06.10.2026, 14:46:21 |
| Besitzer | Josias Assefaw |
| Typ | Canvas |
| Lizenzbezeichnung | Standard (kein Premium nötig) |
| Weblink | `https://apps.powerapps.com/play/e/default-84e2e900-49ec-4416-85fb-299b258a5227/a/e218702e-35cb-4dc8-813a-b9fd860c7f72` |

**Weg:** `make.powerapps.com/e/<Umgebung>/canvas/?action=new-blank&form-factor=phone`, dann Strg+S und „Speichern unter" mit dem Namen `Tischbuchung Handy`.

**Wichtig zum Speichern-Dialog:** Der Dialog hat einen aufklappbaren Bereich **„Vorhandene ersetzen"**, der alle Apps der Umgebung mit Optionsfeldern listet, darunter die produktive `Tischbuchung`. Wäre dort eine App ausgewählt worden, hätte „Speichern" sie überschrieben. Ich habe vor dem Klick per Bildausschnitt geprüft, dass **kein** Optionsfeld gesetzt war. Für künftige Sitzungen: Diesen Bereich beim Speichern einer neuen App immer prüfen.

**Der Pfad `/create` taugt nicht:** Er leitet auf `canvas/?action=new-blank&form-factor=tablet` um und erzeugt eine Tablet-App. Das Phone-Format muss über den Parameter `form-factor=phone` erzwungen werden.

**Einstellung geändert (Einstellungen → Anzeige):**
- App-Layout: **vorher** „Fest", **nachher** „Dynamisch". Grund: „Fest" ist genau das Scale-to-fit, das A03 ausschließt.
- Ausrichtung: Hochformat (bei dynamischem Layout ausgegraut, Wert bleibt Hochformat)
- Seitenverhältnis sperren: Aus (automatisch, nicht änderbar)
- Ausrichtung sperren: Aus (**nicht setzbar**, siehe `ENTSCHEIDUNGEN.md` E-04)

Belege: `screenshots\A03_app_layout_dynamisch.jpg`, `screenshots\A03_anzeige_dynamisch_ausrichtung_gesperrt_deaktiviert.jpg`

**An der produktiven App wurde nichts verändert.** Ihre Zeile in der App-Liste zeigte während dieser Arbeit unverändert „vor 35 Minuten", also den Stand von 14:12 (Version 23).

---

### 2026-10-06, ca. 14:53 — Datenquellen hinzugefügt

**Vorher:** Die Handy-App hatte keine Datenquelle.
**Nachher:** Sie hat genau zwei: `Tischbuchungen` und `Tische`.

**Weg:** Daten hinzufügen → Suche „SharePoint" → vorhandene Verbindung von `josias.assefaw@technoform.com` → Adresse `https://technoformgroup.sharepoint.com/sites/IMSKonzept` → Listen auswählen.

**Bewusst nicht hinzugefügt:** `Raumbuchungen` und `Räume`. Die Handy-App hat keine Raumbuchung (Auftrag 2.4), und in der Desktop-App ist der gesamte Raumcode tot. Vor dem Klick auf „Verbinden" per Bildausschnitt geprüft, dass nur die beiden gewollten Listen angehakt waren.

**Bestätigung des Studios:** „Die Datenquelle ‚Tische' wurde Ihrer App hinzugefügt."

Die Verbindung ist dieselbe, die auch die Desktop-App benutzt (`shared_sharepointonline`, Standard-Tarif). Damit sehen beide Apps denselben Datenstand, wie in Auftrag 2.1 gefordert.

**Noch keine Buchung angelegt oder verändert.** `TESTDATEN.md` ist weiterhin leer.

---

### 2026-10-06, ca. 15:00 — .NET-Installation gescheitert, Entscheidung für den Studio-Weg

Die winget-Installation des .NET 10 SDK lief über 30 Minuten ohne Ergebnis und ohne Ausgabe; vermutlich hing sie an einer Rückfrage, die im stillen Modus nicht sichtbar war. Ich habe den Prozess beendet (Exit-Code 255).

**Folge:** Der Canvas Authoring MCP steht nicht zur Verfügung. Ich baue über Power Apps Studio im Browser. Nach Auftrag 5.5 („Werkzeug geht nicht: Rückfallweg wählen, dokumentieren, weiter") ist das der vorgesehene Weg.

**Der Rückfallweg ist besser als erwartet** (siehe nächster Abschnitt). Eine erneute Installation lohnt daher vorerst nicht.

---

### 2026-10-06, ca. 15:02 — Gerüst gebaut, und ein wichtiger Fund zur Arbeitsweise

**Fund: Studio nimmt YAML über die Zwischenablage entgegen.** Ich habe die Steuerelement-YAML per PowerShell in die Zwischenablage gelegt, in der Strukturansicht den Screen ausgewählt und Strg+V gedrückt — Studio hat den gesamten Containerbaum samt Kindern und Eigenschaften in einem Schritt angelegt. Damit entfällt das Zusammenklicken jedes einzelnen Steuerelements. Die exakte Syntax steht in `APP_WISSEN.md`, Abschnitt 8a.

Die Syntax habe ich nicht geraten: Ich habe einen vertikalen Container über das Menü eingefügt und mir über das Kontextmenü → **Ansichtscode** von Studio selbst zeigen lassen, wie er aussieht (`Variant: AutoLayout`, `LayoutDirection`, `LayoutAlignItems`, `Padding…`). Erst danach habe ich das Gerüst als YAML geschrieben.

**Vorher:** `Screen1` war leer (bis auf einen Test-Container `Container1`).
**Nachher:**

```
Screen1
└── conRoot            AutoLayout, vertikal, Width/Height = Parent, Fill #F7F7F7
    ├── conHeader      AutoLayout, horizontal, FillPortions 0, Höhe 150, weiß
    ├── conInhalt      AutoLayout, vertikal, FillPortions 1 (füllt den Rest)
    └── conTabLeiste   AutoLayout, horizontal, FillPortions 0, Höhe 160, weiß
```

`Container1` wurde danach gelöscht. **Bestätigt:** `FillPortions` wird beim Einfügen akzeptiert; die Leinwand zeigt oben und unten ein festes weißes Band und dazwischen eine mitwachsende Fläche.

**App.OnStart gesetzt.**
**Vorher:** leer.
**Nachher** (deutsche Schreibweise, so wie sie in der Formelleiste steht):

```powerfx
Set(varTab; "heute");; Set(varIsLoading; false);; Set(varBuchung; Defaults(Tischbuchungen));; Set(varBuchungID; 0);; Set(varZeigeVerwalten; false);; Set(varZeigeStorno; false);; Set(varNeuLaden; 0)
```

Alle sieben Variablen sind typgerecht vorbelegt, keine mit `Blank()`. `varBuchung` bekommt über `Defaults(Tischbuchungen)` den richtigen Datensatztyp ohne Netzwerkzugriff.

Die Formelleiste zeigte nach der Eingabe keine Fehlermarkierung. App gespeichert.

**Noch offen:** `conHeader`, `conInhalt` und `conTabLeiste` sind leer. Als Nächstes kommen Header-Inhalt, Tab-Leiste und Lade-Overlay.

---

### 2026-10-06, ca. 15:20 — Header, Tab-Leiste und Lade-Overlay gebaut

**Logo ohne Upload gelöst.** Der Datei-Upload im Medienbereich des Studios ist für die Automatisierung nicht erreichbar: Studio rendert seine Oberfläche so, dass das Dateieingabefeld nicht im Zugänglichkeitsbaum erscheint, und ein Klick auf „Hochladen" würde einen Betriebssystem-Dialog öffnen, den ich nicht bedienen kann. Statt Josias dafür zu unterbrechen, habe ich das Logo aus dem Export der Desktop-App (`614892e2-….png`, 2000 × 520) auf 400 × 104 verkleinert (7,8 KB) und als Base64-Daten-URI direkt in die `Image`-Eigenschaft gelegt. Dateien in `MOBIL\medien\`.

*Vorteil:* kein Upload nötig, die App trägt das Logo in sich. *Nachteil:* eine lange Zeichenkette in der Eigenschaft. Josias muss sie nie anfassen. Wenn er das Logo lieber als Mediendatei hätte, zieht er die Datei einmal ins Studio und ersetzt die Eigenschaft durch den Ressourcennamen.

**conHeader** (horizontal, Höhe 150, weiß, Abstand 24 links und rechts, Lücke 12):

| Element | Inhalt |
|---|---|
| `imgLogo` | Technoform-Logo, 170 × 44, als Daten-URI |
| `lblKopfTitel` | „Tischbuchung", Größe 17, halbfett, Technoform-Blau, `FillPortions: =1` |
| `icoAktualisieren` | `Icon.Sync`, 84 × 84, blau. `OnSelect` setzt `varIsLoading`, aktualisiert **beide** Datenquellen, zählt `varNeuLaden` hoch, setzt `varIsLoading` zurück und meldet „Aktualisiert." |
| `btnInitialen` | runder Knopf 84 × 84 (Radius 42), Technoform-Blau, zeigt die Initialen aus `User().FullName`, `DisplayMode.View` (nicht anklickbar), QuickInfo = voller Name |

**conTabLeiste** (horizontal, Höhe 160, weiß) mit `btnTabHeute`, `btnTabBuchen`, `btnTabMeine`, je `FillPortions: =1`, also gleich breit. Aktiver Zustand über **Farbe und Schriftschnitt**, nicht über Hover (Auftrag 2.5): aktiv = blauer Hintergrund, weiße halbfette Schrift; inaktiv = weiß mit grauer Schrift. `HoverFill` und `HoverColor` sind bewusst gleich dem Normalzustand gesetzt, damit Hover keine Information trägt. Jeder `OnSelect` setzt `varTab` **und** schließt beide Dialoge (`varZeigeVerwalten`, `varZeigeStorno`) — damit ist die Anforderung aus A07 „Tabwechsel schließt offene Dialoge" schon im Gerüst erfüllt.

**conLadeOverlay** liegt **direkt im Screen**, nicht in `conRoot`: In einem Auto-Layout-Container würden `X` und `Y` ignoriert und das Overlay würde einsortiert statt überlagert. `Variant: ManualLayout`, volle Bildschirmgröße, `Fill: =RGBA(0, 0, 0, 0.45)`, `Visible: =varIsLoading`. Darin eine weiße abgerundete Box mit „Bitte warten ...".

**Bewusst kein animierter Spinner und kein `Screen.LoadingSpinner`.** Die Desktop-App hat beides gleichzeitig (Befund BD-13, doppelter Spinner). Hier bleibt es bei einer Anzeige.

**Drei Fehlschläge beim Einfügen, alle behoben und in `APP_WISSEN.md` Abschnitt 8a festgehalten:**

1. `PA1001 YamlInvalidSyntax` — `{ teile: Split(...) }` enthält `: ` und bricht die YAML-Syntax. Lösung: Blockwert `|-`.
2. Das Titel-Label drückte Symbol und Initialen aus dem Bild. Ursache: `Mindestbreite` steht bei Labels standardmäßig auf **560** und wirkt stärker als `FillPortions`. Lösung: `LayoutMinWidth: =0`.
3. `PA2108 : Unknown property 'RadiusBottomLeft' for control type 'Rectangle@2.3.0'` — `Rectangle` kennt keine Radius-Eigenschaften. Lösung: `GroupContainer` statt `Rectangle` für die abgerundete Box.

**Baumstand:**

```
Screen1
├── conLadeOverlay       ManualLayout, Visible = varIsLoading
│   └── conLadeBox
│       └── lblLadeText
└── conRoot
    ├── conHeader        imgLogo, lblKopfTitel, icoAktualisieren, btnInitialen
    ├── conInhalt        noch leer
    └── conTabLeiste     btnTabHeute, btnTabBuchen, btnTabMeine
```

**UNGETESTET:** Ob `conLadeOverlay` zur Laufzeit wirklich über allem liegt. Die Strukturansicht listet es vor `conRoot`, und „Zum Ende verschieben" ändert daran nichts — das deutet darauf hin, dass die Liste bereits die Stapelreihenfolge abbildet. Wird beim Laufzeittest zu A29 geprüft.

---

### 2026-10-06, ca. 15:35 — „Meine Buchungen" gebaut und zur Laufzeit bestätigt

**conMeine** enthält jetzt `lblMeineTitel`, `lblMeineLeer` (nur sichtbar bei leerer Liste) und `galMeine`.

`galMeine.Items`:

```powerfx
=With(
  { neuLaden: varNeuLaden },
  SortByColumns(
    Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()),
    "Startzeit",
    SortOrder.Ascending
  )
)
```

Beide Filterbedingungen sind nach der Doku delegierbar (`Person.Email` und ein Datumsvergleich). Die Hülle `With({neuLaden: varNeuLaden}, ...)` zwingt die Galerie zum Neurechnen, wenn der Aktualisieren-Knopf gedrückt wurde — dasselbe Muster, das die Desktop-App mit `varGalleryNeuAufbauen` benutzt.

Die Karte je Zeile (`conKarteM`) zeigt Tischname, Wochentag mit Datum, Uhrzeit von–bis und einen Verwalten-Knopf. Der Knopf setzt `varBuchung`, `varBuchungID` und `varZeigeVerwalten`; der Dialog dazu kommt im nächsten Schritt.

**Der wichtigste Fund dieser Runde: das Koordinatensystem ist verdoppelt.**

Ich habe ein temporäres Diagnose-Label (`lblDebug` in `conHeute`) eingebaut, das `App.Width`, `App.Height` und `varTab` anzeigt. In der Geräteemulation iPhone 390 × 844 steht dort:

```
App 780 x 1688  |  Screen 780 x 1688  |  varTab: heute
```

**Eine App-Einheit ist ein halbes CSS-Pixel.** Mein erster Durchgang hatte deshalb durchgehend halb so große Schriften und Tippflächen wie beabsichtigt — Knöpfe von 84 Einheiten sind nur 42 Pixel und damit unter der geforderten Fingerkuppengröße von 44 bis 48.

**Korrektur in einem Durchgang:** Header, Tab-Leiste, Bereich „Meine" und Lade-Overlay neu eingefügt mit verdoppelten Werten. Tippflächen jetzt 96 Einheiten (48 px), Fließtext 24, Überschriften 30 bis 34, Kopfzeile 170, Tab-Leiste 180. Die Umrechnungstabelle steht in `APP_WISSEN.md`.

**Zwei Dinge sind mir dabei passiert und sind behoben:**
- Ein `Delete` hat nicht gegriffen, weil der Fokus nach dem Klick in der Leinwand statt in der Strukturansicht lag. Ergebnis: zwei Header (`conHeader` und `conHeader_1`). Der alte wurde gelöscht, der neue umbenannt. **Lehre:** Nach dem Auswählen in der Strukturansicht vor dem Löschen prüfen, dass wirklich das gewünschte Element markiert ist.
- Die Leinwand im Studio ist 640 × 1136 (Entwurfsgröße), die Laufzeit 780 × 1688. Elemente, die im Editor abgeschnitten wirken, passen zur Laufzeit. **Verlässlich ist nur die Geräteemulation**, nicht die Editoransicht.

**Laufzeittests bestanden (P3):**

| Gerät | Ergebnis | Beleg |
|---|---|---|
| iPhone 390 × 844 | Kopfzeile, Liste und Tab-Leiste vollständig, kein horizontales Scrollen | `screenshots\A03_A16_meine_390x844_korrekte_groessen.jpg` |
| 360 × 800 (benutzerdefiniert) | ebenso, kein horizontales Scrollen | `screenshots\A03_meine_360x800_kein_horizontales_scrollen.jpg` |

Bei 360 Breite war der Titel zunächst auf „Tischbuc..." abgeschnitten. Behoben durch ein schmaleres Logo (170 statt 215) und Schriftgröße 23 statt 26.

**Die Liste zeigt echte Daten**, chronologisch sortiert, mit Wochentag: OG Desk 1 am Dienstag 06.10. von 14:30 bis 19:30, OG Desk 8 am selben Tag von 15:30 bis 20:30, dann mehrere Termine an OG Desk 1 ab Mittwoch 07.10. Das deckt sich mit dem, was die Desktop-App für denselben Nutzer zeigt.

**App-Prüfung (P1):**
- **Formeln: „Keine Fehler gefunden"** — Beleg `screenshots\A04_app_pruefung_formeln_keine_fehler_2026-10-06.jpg`
- Leistung: 4 Warnungen, alle „Nicht verwendete Variable" (`varBuchung`, `varBuchungID`, `varZeigeVerwalten`, `varZeigeStorno`). Sie werden geschrieben, aber noch nicht gelesen, weil der Verwalten-Dialog fehlt. Lösen sich mit dem nächsten Schritt auf.
- **Keine Delegationswarnung.** Beleg `screenshots\A05_app_pruefung_leistung_4_unbenutzte_variablen.jpg`
- Barrierefreiheit: 21 Hinweise, noch nicht durchgesehen.

**Noch im Baum: `lblDebug`.** Das temporäre Diagnose-Label bleibt, bis das Layout steht, und wird vor der Übergabe entfernt.

**Nachtrag:** `lblDebug` wurde in der Runde „Heute" entfernt.

---

### 2026-10-06, ca. 15:48 — „Heute" gebaut: Status, Einchecken, Leerzustand (A08, A10, A11)

*Nachgetragen um 16:25 aus den Commits `ae1c85b` und `4bdeba8`; die Einträge waren beim Commit nur in den Commit-Nachrichten festgehalten.*

**Vorher:** `conHeute` leer. **Nachher:** `lblHeuteTitel`, `conHeuteLeer` (Hinweis plus Knopf „Zum Buchen", sichtbar nur ohne Buchung heute) und `galHeute` mit einer Karte je eigener Buchung von heute.

- Filter: eigene Buchungen mit `Endzeit >= Now()` und Start heute, sortiert nach Startzeit
- Status: „Eingecheckt" grün, „Nicht eingecheckt" orange (Entscheidung E-A09)
- `btnEincheckenH`: frisches `LookUp` über `varBuchungID`, Prüfung „gelöscht", „schon eingecheckt" (zweiter Tipp checkt nie aus, V3), Zeitfenster 30 Min vor Start bis Ende zum Klickzeitpunkt (V2), `IfError` um den `Patch`, Erfolgsmeldung erst nach Nachlese (D8), Sperre über `varIsLoading` (D3), `varIsLoading` auf jedem Pfad zurückgesetzt (A29)

**Fund:** `LookUp(Tischbuchungen, ID = frisch.ID)` mit `frisch` aus einem `With` ergab Delegierungswarnungen. Mit globaler Variable verschwinden sie. Beleg `screenshots\A05_delegierungswarnung_frisch_ID_vor_korrektur.jpg`.

**Laufzeit:** drei echte Buchungen von heute angezeigt (OG Desk 1, OG Desk 8, Quiet Desk 1), Statuszeile brach um → Breite 302, Größe 21, ohne Umbruch. Beleg `screenshots\A08_A10_heute_390x844_drei_buchungen.jpg`. **Einchecken noch nicht ausgelöst** (braucht Testbuchung).

---

### 2026-10-06, ca. 16:03 — Verwalten- und Storno-Dialog gebaut (A17, A18, A19, A23)

*Nachgetragen aus Commit `01b411c`.*

**Vorher:** Der Verwalten-Knopf setzte nur Variablen. **Nachher:** `conDlgHintergrund`, `conDlgVerwalten` (+1 Std, +2 Std, Jetzt beenden, Stornieren, Schließen) und `conDlgStorno` (Bestätigung, V8) liegen direkt im Screen. Quelltext `yaml\dialoge.yaml`.

Jeder Schreibweg liest den Datensatz unmittelbar vorher frisch über `varBuchungID` (D2, D4), prüft auf inzwischen gelöschte Buchung, schreibt in `IfError`, meldet Erfolg erst nach Nachlese (D8). Verlängern prüft die 22:00-Grenze und die Kollision nur gegen das neue Stück `[altes Ende, neues Ende)` — damit kollidiert die Buchung nicht mit sich selbst.

**Fund:** `CountRows` ist beim SharePoint-Konnektor nicht delegierbar („Der Vorgang ‚CountRows' wird durch diesen Connector nicht unterstützt"). Ersatz `!IsBlank(LookUp(...).ID)`. Erklärt die 56 Warnungen der Desktop-App (BD-27).

Stapelreihenfolge von oben: `conLadeOverlay`, `conDlgStorno`, `conDlgVerwalten`, `conDlgHintergrund`, `conRoot`. App-Prüfung danach ohne Befund. **Noch nicht zur Laufzeit ausgelöst.**

---

### 2026-10-06, ca. 16:05–16:25 — Bereich „Buchen" gebaut (A12, A13, A15, A20–A27 im Code)

**Vorher:** `conBuchen` leer. **Nachher:** `conBuchenForm` mit Datum, Von/Bis, freiem Tisch, Zusammenfassung und „Jetzt buchen". Quelltext `yaml\conBuchen.yaml`.

**OnStart ergänzt** (vorher 11 Variablen, nachher 14 plus eine Sammlung): `varBuchStart`, `varBuchEnde`, `varTischID`, `ClearCollect(colTische; Tische)`.

**Aufbau:**
- `ddDatum`: heute plus 59 Tage, Text „Heute, …" / „Morgen, …" / Wochentag mit Datum. Vergangene Tage sind nicht wählbar. Ab 22:00 beginnt die Liste mit morgen.
- `ddStart`: 30-Minuten-Raster bis 21:30. Heute ab der **laufenden** halben Stunde, sonst ab 08:00 (E-05).
- `ddEnde`: ab Start + 30 Min bis 22:00, vorbelegt mit 17:00, wenn der Start davor liegt (E-05, statt Schnellwahlknopf).
- `ddTisch`: **eine** delegierbare Abfrage `Filter(Tischbuchungen, Startzeit < Ende && Endzeit > Start)`, dann lokal gegen `colTische` gerechnet, Big Table ausgeschlossen, sortiert nach Geschoss, Tischart, Nummer.
- `lblZusammenfassung`: Tisch, Wochentag mit Datum, Uhrzeit; rot „kein Tisch frei", wenn nichts frei ist.
- `btnBuchen`: siehe `ENTSCHEIDUNGEN.md` E-06. Prüfreihenfolge: Pflichtangaben → Ende nach Beginn → nicht in der Vergangenheit → nicht nach 22:00 → Tisch frei (D1/D2, frisch zum Klickzeitpunkt) → keine eigene Überschneidung (D5) → `Patch` mit vollständigem Person- und Tisch-Schema in `IfError` → Nachlese aller Buchungen dieses Tisches im Zeitraum → eigene Zeile gefunden? → ältere fremde Zeile im selben Zeitraum? (D7) → erst dann Erfolg.

**Drei Delegationsfunde, alle behoben** (App-Prüfung meldete zuerst 6 Warnungen):
1. Zeitgrenzen aus einem `With`-Local im Filterprädikat → Warnung an `Startzeit`/`Endzeit`. Auch wenn das Local nur aus Steuerelementwerten berechnet ist. Behoben durch den Ausdruck direkt im Prädikat.
2. `ID < varBuchungID` → Warnung an `ID`. Beim SharePoint-Konnektor ist an `ID` nur `=` delegierbar.
3. `Startzeit = varBuchStart` im `LookUp` → Warnung.
2 und 3 behoben durch **eine** delegierbare Abfrage in `colKollision` und die Feinprüfung lokal darauf.

**Nach der Korrektur:** Formeln ohne Befund, keine Delegationswarnung. Leistung: drei Hinweise, begründet in `TESTPROTOKOLL.md`.

**Laufzeit (Vorschau):** zuerst leere Tischauswahl, weil die Vorschau `OnStart` nicht neu ausführt (`colTische` hatte 0 Zeilen). Nach „OnStart ausführen" 34 Zeilen. Danach zeigte die Auswahl 30 Tische. Erste Sortierung mischte „OG Desk 2" und „Quiet Desk 2" → Sortierschlüssel um die Tischart erweitert. Graue Rahmen um „Von"/„Bis" entfernt.

**Gegenprobe gegen SharePoint (A12) und Vollständigkeit „Meine" (T-01):** siehe `TESTPROTOKOLL.md`. Beide bestanden.

**Keine Buchung angelegt.** `TESTDATEN.md` ist weiterhin leer.

---

### 2026-10-06, 16:26–16:38 — Erste Schreibtests, ein echter Fehler gefunden und behoben (D3)

**Testbuchungen angelegt** (vorher in `TESTDATEN.md` eingetragen): TB-1 = ID **496** (UG Desk 17, Sa 31.10. 08–12), TB-2 = ID **497** (UG Desk 15, Sa 31.10. 14–15). Vorher war das Wochenende leer, höchste ID 495.

**Bestanden:**
- **A14/D6:** TB-1 per Handy gebucht. Meldung „Gebucht: UG Desk 17, 31.10., 08:00 bis 12:00 Uhr", Wechsel zu „Meine". REST-Nachlese: Tisch `{Id 30, „UG Desk 17"}` (= ID 30 in `Tische`), Start 07:00Z = 08:00 Ortszeit, Ende 12:00, Person Josias, angelegt von Josias, nicht eingecheckt, `Title` leer wie bei den Desktop-Buchungen 491–495.
- **A24/D5:** 31.10. 10–14 an UG Desk 16 → „Du hast in dieser Zeit schon einen Tisch gebucht.", Lade-Overlay weg, REST: **keine** neue Zeile.
- **A22/D3 (Buchen):** Doppeltipp plus dritter Tipp auf „Jetzt buchen" → REST: **genau eine** Zeile (497).

**Gefunden: Ein Doppeltipp wird nicht von der `DisplayMode`-Sperre abgefangen.** Beim Doppeltipp auf „Jetzt buchen" kam nach „Gebucht" noch „Der Tisch ist in dieser Zeit schon belegt". Der zweite Tipp war also **eingereiht** und lief **nach** dem ersten, als `varIsLoading` schon wieder `false` war. Beim Buchen hat die frische Tischprüfung ihn abgefangen. Beim Verlängern nicht:

- **Vorher:** TB-2 14:00–15:00, Doppeltipp auf „+1 Std" → **14:00–17:00**, also zweimal verlängert. REST bestätigt 17:00. Beleg `screenshots\D3_FEHLER_doppeltipp_plus1_verlaengert_doppelt_14-17.jpg`.
- **Ursache:** Power Apps reiht den zweiten Tipp ein, bevor die Oberfläche den gesperrten Zustand zeichnet. Danach läuft er mit frischem Datensatz durch alle Prüfungen, die er alle besteht.
- **Behebung (alle sechs schreibenden Handler):** Einchecken, +1 Std, +2 Std, Jetzt beenden, Stornieren, Jetzt buchen. Jeder ist jetzt umhüllt von `If(!varIsLoading && Now() >= varSperreBis, …)` und setzt am Ende `varSperreBis = Now() + 2 Sekunden`. Ein eingereihter Zweit-Tipp läuft damit ins Leere, ohne Meldung. `varSperreBis` in `OnStart` vorbelegt. Umbau per Skript an den YAML-Quellen, dann `conHeute`, die drei Dialoge und `conBuchenForm` neu eingefügt; `conLadeOverlay` wieder in den Vordergrund.
- **Nachher:** TB-2 14:00–17:00, Doppeltipp auf „+1 Std" → **14:00–18:00**, genau einmal verlängert. REST bestätigt 18:00. Beleg `screenshots\D3_KORRIGIERT_doppeltipp_plus1_genau_einmal_14-18.jpg`.
- App-Prüfung nach dem Umbau: Formeln ohne Befund.

**Nebenbefund Vorschau:** Nach 30 Mausrad-Schritten über der Galerie stand die App einmal verschoben da (Tab-Leiste in der Mitte, rechte Knöpfe abgeschnitten). Nach Schließen und Neustarten der Vorschau war alles normal. **VERMUTUNG:** Artefakt der Studio-Vorschau, nicht der App. Wird beim Test auf echten Geräten (J1) mit geprüft.

---

### 2026-10-06, 16:38–17:03 — Weitere Schreibtests, Handy-App veröffentlicht

- **A17/V5** bestanden: +2 bis genau 22:00 erlaubt, +1 darüber abgelehnt (TB-2). D3-Gegenprobe auf TB-1: Doppeltipp verlängert genau einmal, der erste Tipp war nachweislich registriert.
- **Handy-App veröffentlicht** um 16:41:43 (Version 30 „Live"), damit ein zweites Fenster möglich ist. Nicht freigegeben. Der Zustimmungsdialog beim ersten Start wurde **nicht** bestätigt (F-15). Stattdessen dient die Desktop-App im Wiedergabe-Modus als zweites Fenster; A21 erlaubt das ausdrücklich.
- **A02 Zwischenprüfung 16:43:** produktive App höchste Version weiterhin **23**, aber jetzt V23 „Live" statt V20 (F-14, VERMUTUNG: von Josias veröffentlicht). Beleg `screenshots\A02_versionsliste_produktiv_ZWISCHENSTAND_2026-10-06_1643_V23_live.jpg`
- **A21** bestanden (TB-4 = 498 über die Desktop-App, Handy lehnt ab, keine zweite Zeile). **A14** Querprobe Desktop ↔ Handy bestanden.
- **T-22/T-23** bestanden; kosmetischer Mangel (leerer Dialog nach „gibt es nicht mehr") im Quelltext `yaml\dialoge.yaml` behoben, noch nicht eingefügt. TB-4 gelöscht.
- **Studio-Probleme:** Die Vorschau reagiert zeitweise nicht, Bildschirmfotos laufen in Zeitüberschreitungen, die Anzeige verschiebt sich. Ursache gefunden: Das Chrome-Fenster ist zeitweise **verborgen** (`document.visibilityState = "hidden"`), dann rechnet die Vorschau mit falscher Größe und liefert keine Bilder. Kein Fehler der App.
- **A28 gestartet:** Prüf-Subagent in frischem Kontext greift alle schreibenden Formeln an (läuft).
- `ANLEITUNG_JOSIAS.md` geschrieben (A33).