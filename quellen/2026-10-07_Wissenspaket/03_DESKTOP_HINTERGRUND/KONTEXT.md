# KONTEXT.md — Tischbuchungs-App Technoform

> **Lies zuerst `KORREKTUR.md`.** Sie sticht diese Datei, wo sie sich widersprechen — insbesondere bei Abschnitt 2.

**Stand: 30.09.2026**

---

## 1. Worum es geht

Eine Power-Apps-Canvas-App zur Tischbuchung bei Technoform Kunststoffprofile GmbH. Sie ersetzt das zugekaufte Produkt GoBright. Datenquelle sind SharePoint-Listen. Entwickler ist eine Person (Werkstudent, Wirtschaftsinformatik).

**Ziel des laufenden Umbaus:** Die App soll strukturell sauber, schnell und fehlerfrei werden. Priorität in dieser Reihenfolge:

1. **Funktionale Korrektheit** — keine Doppelbuchungen, keine Lags, keine rohen Fehlermeldungen
2. **App-Ladezeit beim Start**
3. **Speicher- und Stornierzeit bei Mehrfachauswahl**
4. Danach: neue Features (nur freie Tische im Dropdown, Handy-Ansicht mit Dashboard, Kosmetik)

---

## 2. ⚠ Hypothesen zum Ist-Stand — NICHT verifiziert

**Alles in diesem Abschnitt stammt aus der falschen App** („App", `fc32c6b0…`), nicht aus der richtigen („Tischbuchung", `d247d18b…`). Siehe `KORREKTUR.md`.

Behandle jede Angabe hier als **Vermutung, die du gegen den Quellcode prüfst**. Abweichungen sind das erwartete Ergebnis, nicht ein Fehler.

### Screens und Container (vermutet)

Ein einziger Screen: `Screen1`. Direkte Kinder, in dieser Reihenfolge:

| Container | Zweck | Status |
|---|---|---|
| `conLadeOverlay` | Lade-Overlay, enthält `imgSpinner` | aktiv |
| `conHeader` | Kopfzeile mit Tabs | aktiv |
| `conBuchungen` | Buchungen-Tab, inkl. Mehrfachauswahl | aktiv |
| `conVerwaltenDialog` | Stornieren, verlängern, verkürzen | aktiv |
| `conDetailsPopup` | Details bei Klick auf belegten Tisch | aktiv, laut Doku unvollständig |
| `conCheckinDialog` | Ein-/Auschecken | aktiv |
| `conBuchungDialog` | Buchungsdialog vom Grundriss aus | aktiv |
| `conRaumBestätigen` | Raumbuchung Bestätigung | **vermutlich TOT** |
| `conRaumBuchungenPanel` | Raumbuchungen Panel | **vermutlich TOT** |
| `conTischBuchungenPanel` | Buchungspanel für Tische | aktiv |
| `conDashboard` | Dashboard | aktiv |
| `conGrundriss` | Interaktiver Grundriss mit Tischkacheln | aktiv |

### App.OnStart (vermutet)

Rund 60 `Set(...)`-Aufrufe plus zwei `ClearCollect`-Aufrufe mit **hartcodierten** Tischkoordinaten. **Kein Laden aus SharePoint in `OnStart`** — die Daten kommen erst beim Rendern der Galerien.

Vermutete Variablen:

```
varSelectedTisch, varSelectedBuchung
varZeigeDialog, varZeigeDetails, varZeigeCheckin, varZeigeVerwalten, varZeigeVerlaengern
varAktiverTab = "dashboard"
varWiederholen, varWiederholenModus = "Wochentage"
varTagMo … varTagSo
varWiederholenBis = Today() + 14
varWiederholenBisGewaehlt
varAusgewaehltePlusDauer, varAusgewaehltePanelDauer
varAnsichtsDatum = Today()
varAusgewaehltesStockwerk = "OG"
varStockwerkDropdownOffen
varStartOverride, varEndeOverride, varStartOverridePanel, varEndeOverridePanel
varZeigeVerwaltenTab, varZeigeVerwaltenKlein, varGeklickteBuchungKlein
varMehrfachAuswahlModus, varAuswahlModusAktiv
varGalleryNeuAufbauen = 0
varIsLoading = false
varSpinnerWinkel = 0
varProfilFarbe
colAusgewaehlteBuchungen   (per Clear() initialisiert)
colTischPositionen         (OG, 13 Einträge, hartcodiert)
colTischPositionenUG       (UG, 17 Einträge + "Big Table", hartcodiert)
```

Struktur der Koordinaten-Collections:
```
{Tisch: "OG Desk 1"; X: 1380; Y: 270; Ausrichtung: "Vertikal"}
{Tisch: "Big Table"; X: 1254; Y: 630; Ausrichtung: "BigTable"}
```
Ausrichtungswerte: `"Vertikal"`, `"Horizontal"`, `"BigTable"`.

### Vermuteter toter Code

```
varZeigeRaumBuchungForm, varAusgewähltRaum, varAusgewählteStartzeit,
varAusgewählteEndzeit, varZeigeRaumBestätigung, varZeigeRaumInfo,
varZeigeRaumVerwalten     ← Raumbuchungen, aus Scope gestrichen
varZoom, varPanX, varPanY ← Zoom/Pan-Konzept, laut Doku „entfernt" — war es nicht
```

### Offene Auffälligkeiten

1. **Viele gelbe Warndreiecke auf dem Canvas** — rund 15–18, vermutlich Delegierungswarnungen.
2. **`App.Formulas` hat Inhalt** — Named Formulas werden bereits genutzt, Inhalt unbekannt.
3. **`varSpinnerWinkel`** wird gesetzt, aber es war kein Timer zu finden. Relevant für den Bug „doppeltes Ladesymbol".
4. **`varGalleryNeuAufbauen`** ist ein Zähler, der einen Galerie-Neuaufbau erzwingt. Solche Hacks sind teuer.
5. **`varProfilFarbe` nutzt `RandBetween(1; 8)`** — die Avatarfarbe ist bei jedem Start zufällig. Vermutlich unbeabsichtigt.
6. **Zwei Variablen für denselben Zweck:** `varMehrfachAuswahlModus` und `varAuswahlModusAktiv`.

---

## 3. Datenmodell (SharePoint)

| Liste | Spalten |
|---|---|
| `Tischbuchungen` | `Tisch` (Lookup → Tische.Title), `Startzeit` (DateTime), `Endzeit` (DateTime), `Person` (Person, keine Gruppen), Check-in-Spalte (⚠ Schreibweise ungeklärt) |
| `Tische` | `Title`, `Standort`, `X`, `Y`, `Ausrichtung` (Choice), `Aktiv` |
| `Räume`, `Raumbuchungen` | aus dem Scope gestrichen, Listen existieren noch |

**⚠ Offen:** Der interne Name der Check-in-Spalte ist unklar — in Notizen steht sowohl `CheckedIn` als auch `Checkedin`. Ein falsch geschriebener Feldname wird von SharePoint **still ignoriert**, ohne Fehler.

**⚠ Wichtig:** Die Liste `Tische` hat `X`- und `Y`-Spalten, aber die App benutzt sie **nicht** — die Koordinaten liegen hartcodiert in `App.OnStart`. Doppelte Wahrheit im Datenmodell.

**Aufräum-Flow** (Power Automate, täglich 03:00): löscht Buchungen, deren Endzeit mehr als 7 Tage zurückliegt. Existiert nur, um unter der Delegationsgrenze zu bleiben. Vernichtet damit die Auslastungshistorie.

**Datenzeilenlimit** der App wurde von 500 auf 2000 erhöht.

---

## 4. Die zentralen technischen Probleme

### 4.1 Nicht delegierbare Abfragen (Hauptproblem)

Die Master-Bedingung der Grundriss-Kacheln lautet sinngemäß:

```
LookUp(Tischbuchungen;
    Tisch.Value = ThisItem.Title        ← Lookup-Spalte: NICHT delegierbar
    && Endzeit >= Now()                  ← Now(): NICHT delegierbar
    && Startzeit <= DateAdd(Now(); 30; TimeUnit.Minutes))   ← DateAdd(): NICHT delegierbar
```

Folge: Power Apps lädt bis zu **2000 Zeilen** herunter und filtert erst lokal. Bei erwarteten 200–400 Einträgen (Spitze 600–800 durch Serienbuchungen) geht beim Rendern der komplette Bestand über die Leitung, obwohl nur die Buchungen eines Tages gebraucht werden.

**Die Zeilenzahl ist nicht das Problem — die fehlende Delegation ist es.**

**Lösungsmuster:** Datumsgrenzen zuerst in Variablen schreiben, dann gegen die Variablen filtern. Ein Vergleich Datumsspalte gegen **Variable** ist delegierbar; `Today()` oder `Now()` direkt in der Formel ist es nicht.

```
Set(varTagStart; varAnsichtsDatum);;
Set(varTagEnde;  DateAdd(varAnsichtsDatum; 1; TimeUnit.Days))
```
```
ClearCollect(colBuchungenTag;
    Filter(Tischbuchungen; Startzeit >= varTagStart && Startzeit < varTagEnde))
```

**Kontrolle:** Kein gelbes Warndreieck mehr neben der Formel = delegiert.

### 4.2 Master-Bedingung an sechs Stellen wortgleich

Laut Dokumentation steht dieselbe Bedingung wortgleich in:
`Rectangle1.Fill` · `Circle1.Fill` · `Circle1.BorderColor` · `Label1.Text` · `btnHitArea.OnSelect` · `btnEincheckenHeute.Visible`

Die Zahl stammt aus älterer Doku und ist **zu verifizieren**. `LookUp()` in einer Galerie-Vorlage wird pro Zeile ausgewertet.

### 4.3 Schreibpfad

- `Refresh(<Liste>)` wird laut Doku als Standardlösung nach jedem `Patch` eingesetzt. **Steht davon eines innerhalb einer `ForAll`-Schleife, ist das die Ursache der extrem langsamen Serienbuchung.**
- Serienbuchung und Mehrfachauswahl arbeiten vermutlich mit einer Schleife aus Einzel-Operationen statt mit einem Sammelaufruf.

**Korrekte Muster:**
- Neue Datensätze in Menge → `Collect(Datenquelle; Tabelle)`
- Bestehende in Menge ändern → `Patch(Datenquelle; Tabelle)`, Tabelle **muss** `ID`-Spalte enthalten
- Mehrere löschen → `Remove(Datenquelle; Tabelle)`

### 4.4 Doppelbuchung möglich

Die Kollisionsprüfung ist ein clientseitiges Read-then-Write. Zwischen `CountRows` und `Patch` liegt ein Zeitfenster; SharePoint kennt keine Transaktionen. Zwei gleichzeitige Buchungen desselben Tisches können beide durchgehen, beide mit Erfolgsmeldung.

### 4.5 Keine Fehlerbehandlung

`IfError` kommt in der Dokumentation nirgends vor. Nutzer sehen rohe Connector-Fehler inklusive `clientRequestId`.

---

## 5. Gemeldete offene Bugs (30.09.2026)

1. **Serienbuchung extrem langsam.** Einzelbuchung schnell. Unregelmäßig: bei 10 Wiederholungen waren 6 und 7 deutlich langsamer, der Rest schnell. → Typisch für SharePoint-Drosselung (429 mit stillem Retry), kein Formelfehler. Gegenmaßnahme: weniger, größere Schreibvorgänge.
2. **Ladesymbol erscheint doppelt** an verschiedenen Stellen.
3. **Buchungen-Tab zeigt manchmal keine Einträge**, obwohl eine Buchung sichtbar existiert. Delegation ist der Hauptverdacht.
4. **`Remove` wirft „Item Not Found"** bei einem noch sichtbaren Eintrag. Anzeige und Datenbestand laufen auseinander.
5. **Einchecken dauert manchmal lange**, obwohl es ein einzelner kleiner Statusupdate sein sollte.

---

## 6. Power Fx — Regeln für dieses Projekt

Diese Fehler sind in diesem Projekt alle schon mindestens einmal passiert:

- **Deutsche Locale:** `;` trennt Argumente, `,` ist Dezimaltrenner (`RGBA(0; 0; 0; 0,4)`), `;;` verkettet.
- **Keine Kommentare in Power Fx.** Ein `//` erzeugt app-weite Fehler.
- **Beim Anhängen an `App.OnStart` immer prüfen, ob die vorherige Zeile mit `;;` endet.** Fehlt es, erscheint die Fehlermeldung an einer völlig unbeteiligten Stelle. Ist zweimal in einer Session passiert.
- **`With()`-Felder werden gleichzeitig ausgewertet.** Abhängige Zwischenwerte brauchen verschachtelte `With`.
- **Lookup-Feld schreiben:** immer `{Id: ...; Value: ...}`.
- **Personenfeld schreiben:** immer das volle Schema:
  ```
  { '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser";
    Claims: "i:0#.f|membership|" & Lower(User().Email);
    DisplayName: User().FullName; Email: User().Email;
    JobTitle: ""; Department: ""; Picture: "" }
  ```
- **Kein eigener `TimeZoneOffset`-Workaround.** Power Apps rechnet lokal→UTC beim Patch selbst.
- **`Fill` wird ignoriert, wenn `DisplayMode = Disabled`.** Dann greift `DisabledFill`.
- **`Set(var; false)` setzt eine Checkbox nicht zurück.** Zusätzlich `Reset(control)`, am besten beim **Öffnen** des Dialogs.
- **Eine Variable nie mit zwei verschiedenen Record-Typen befüllen.** Power Apps leitet den Typ app-weit aus allen `Set`-Aufrufen ab; die Vermischung bleibt kleben.
- **`Patch` immer auf frischem `LookUp(...; ID = ...)`**, nicht direkt auf eine Variable.
- **Nach jedem Kopieren die variierende Zahl in ALLEN Properties prüfen.**
- **Named Formulas (`App.Formulas`) können keine `Set()`-Variablen referenzieren** und keine Verhaltensfunktionen enthalten. Steuerelement-Properties und `Now()` sind erlaubt. Jede Definition endet mit `;`.
- **`Host.OSType`**, nicht `Host.OSName`.
- Interner Spaltenname ist immer **`Title`**, nie `Titel`.

---

## 7. Arbeitsweise

- **Kleine Schritte.** Power Apps Studio hat keinen Debugger, keinen Stacktrace und keine Diff-Ansicht. Wer sechs Dinge gleichzeitig ändert und danach einen Fehler hat, kann nur alles zurückrollen oder raten.
- **Vorher und nachher messen.** Ohne Zahlen ist Performancearbeit Glaubenssache.
- **Nie Feld-, Steuerelement- oder Aktionsnamen raten.** Quellen: Autovervollständigung, Strukturansicht, REST, ausgepackter Quellcode.
- **Immer vollständigen, direkt einsetzbaren Code liefern**, ohne Platzhalter.
- **Sackgassen sofort benennen.** Nach mehreren erfolglosen Runden den Ansatz verwerfen statt weiter zu flicken.

---

## 8. Was Claude Code kann und was nicht

**Kann nicht:** Power Apps Studio bedienen. Das ist eine Weboberfläche; die App wird ausschließlich dort bearbeitet. Jedes Einfügen einer Formel macht Josias von Hand.

**Kann:** Das `.msapp` ist ein Paket, das sich entpacken lässt — mit jeder Formel jedes Steuerelements im Klartext. Darauf kann Claude Code suchen, zählen, vergleichen und vollständige Ersatzformeln schreiben.

**⚠ Wichtig:** Entpacken ist zum **Lesen**. **Zurückpacken einer bearbeiteten App ist unsicher** — `Connections`, `DataSources`, `pkgs` und `CanvasManifest.json` sind bekannte Bruchstellen. Der ausgepackte Quellcode ist ein **Röntgenbild, kein Bearbeitungsformat.**

Arbeitsteilung: Claude Code analysiert und schreibt Formeln. Josias fügt sie im Studio ein und testet.
