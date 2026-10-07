# 04 — Datenquellen, Spalten, Abfragen, Delegierbarkeit

**Kurzfassung:** Die App hängt an vier SharePoint-Listen derselben Site (`Tischbuchungen`, `Tische`, `Raumbuchungen`, `Räume`). Benutzt werden tatsächlich nur `Tischbuchungen` und `Tische`; die beiden Raum-Listen gehören zum toten Raumcode. Diese Datei listet die Spalten mit internen Namen aus den Metadaten des Exports, dann **jede** Lese- und Schreiboperation mit Fundort und Einschätzung der Delegierbarkeit. Die Delegationsregeln sind aus der Microsoft-Doku belegt, die Anwendung auf die konkrete Formel ist meine Schlussfolgerung und als solche markiert. Die App-Prüfung meldet 56 Delegationswarnungen (`AppCheckerResult.sarif`).

## Die Datenquellen

Alle vier Listen liegen unter `https://technoformgroup.sharepoint.com/sites/IMSKonzept` (aus `src/References/DataSources.json`). Verbindung: `shared_sharepointonline`, Standard-Tarif.

| Liste | Operationen im Code | benutzt |
|---|---|---|
| `Tischbuchungen` | 73 | ja |
| `Tische` | 3 | ja |
| `Raumbuchungen` | 41 | nur im toten Raumcode |
| `Räume` | 0 | nur im toten Raumcode |

## Spalten

Interne Namen aus `DataEntityMetadataJson` im Export. Systemspalten (`Created`, `Modified`, `Author`, `Editor`, `{…}`-Felder) sind weggelassen. Die Spalte „in der App" ist eine **Näherung**: Sie steht auf „ja", wenn der interne Name **oder** der Anzeigename in derselben Formel vorkommt wie der Listenname. Da `Titel` und `Startzeit` in mehreren Listen gleich heißen, kann das bei den Raum-Listen zu viel anzeigen; maßgeblich ist der Abschnitt „Jede Operation" weiter unten.

### `Tische`

Tabellen-ID: `2616c57d-887d-4d28-8188-6736c3ac21e9`

| interner Name | Anzeigename | Typ | Zugriff | Unterfelder | in der App |
|---|---|---|---|---|---|
| `ID` | ID | integer/int64 | read-only | — | nein |
| `Title` | Titel | string | read-write | — | ja |
| `Ausrichtung#Id` | Ausrichtung Id | integer/int64 | read-only | — | nein |
| `Ausrichtung` | Ausrichtung | object | read-write | `@odata.type, Value, Id` | nein |
| `Geschoss#Id` | Geschoss Id | integer/int64 | read-only | — | nein |
| `Geschoss` | Geschoss | object | read-write | `@odata.type, Value, Id` | ja |
| `Ausrichtung2#Id` | Ausrichtung 2 Id | integer/int64 | read-only | — | nein |
| `Ausrichtung2` | Ausrichtung 2 | object | read-write | `@odata.type, Value, Id` | nein |
| `X` | X | number/double | read-write | — | nein |
| `Y` | Y | number/double | read-write | — | nein |

### `Tischbuchungen`

Tabellen-ID: `76791681-4416-481c-81a7-9dd8c2f1bded`

| interner Name | Anzeigename | Typ | Zugriff | Unterfelder | in der App |
|---|---|---|---|---|---|
| `ID` | ID | integer/int64 | read-only | — | ja |
| `Title` | Titel | string | read-write | — | ja |
| `Tisch#Id` | Tisch Id | integer/int64 | read-only | — | nein |
| `Tisch` | Tisch | object | read-write | `@odata.type, Id, Value` | ja |
| `Startzeit` | Startzeit | string/date-time | read-write | — | ja |
| `Endzeit` | Endzeit | string/date-time | read-write | — | ja |
| `SerienID` | SerienID | string | read-write | — | nein |
| `Checkedin` | CheckedIn | boolean | read-write | — | ja |
| `Person#Claims` | Person Claims | string | read-only | — | nein |
| `Person` | Person | object | read-write | `@odata.type, Claims, DisplayName, Email, Picture, Department, JobTitle` | ja |

### `Räume`

Tabellen-ID: `88536ba1-0a1f-4d49-9b4d-7c108e901932`

| interner Name | Anzeigename | Typ | Zugriff | Unterfelder | in der App |
|---|---|---|---|---|---|
| `ID` | ID | integer/int64 | read-only | — | nein |
| `Title` | Titel | string | read-write | — | ja |

### `Raumbuchungen`

Tabellen-ID: `0b5b1083-d01c-4121-8fda-d7fbc316c7c8`

| interner Name | Anzeigename | Typ | Zugriff | Unterfelder | in der App |
|---|---|---|---|---|---|
| `ID` | ID | integer/int64 | read-only | — | ja |
| `Title` | Titel | string | read-write | — | ja |
| `Raum#Id` | Raum Id | integer/int64 | read-only | — | nein |
| `Raum` | Raum | object | read-write | `@odata.type, Id, Value` | ja |
| `Startzeit` | Startzeit | string/date-time | read-write | — | ja |
| `Endzeit` | Endzeit | string/date-time | read-write | — | ja |
| `Person#Claims` | Person Claims | string | read-only | — | nein |
| `Person` | Person | object | read-write | `@odata.type, Claims, DisplayName, Email, Picture, Department, JobTitle` | ja |

Drei Namensfallen, alle im Quellcode belegt:

- Die Textspalte heißt intern `Title`, der Anzeigename ist `Titel`. **Die App schreibt überall `Titel`** (Anzeigename), nicht `Title`. Das funktioniert, weil `usedisplaynamemetadata` in `Properties.json` auf `true` steht. Ausnahme: `ddTischePanel.Items.Value: =Title` benutzt den internen Namen.
- Die Check-in-Spalte heißt intern `Checkedin` (kleines i), Anzeigename `CheckedIn`. **Die App schreibt `CheckedIn`.** Power-Automate-Flows müssen `Checkedin` verwenden.
- `Tische` hat `Geschoss` (Nachschlagefeld mit `Id`/`Value`), **kein** `Standort` und **kein** `Aktiv`.

`Tischbuchungen.SerienID` existiert (Text, les- und schreibbar) und wird in der ganzen App **nicht** benutzt — die freie Zutat für Serienbuchungen.

`Tische` hat die Spalten `X`, `Y`, `Ausrichtung` und `Ausrichtung2`. Die App liest sie nicht; die Koordinaten stehen fest einprogrammiert in `colTischPositionen`/`colTischPositionenUG` (`App.OnStart`).

## Delegierbarkeit: die Regeln

**BELEGT** (Microsoft Learn, SharePoint-Verbindung und Delegations-Übersicht, Stand der Recherche vom 05./06.10.2026 laut `BRIEFING_Mehrfachspeichern.md`):

| Was | delegierbar bei SharePoint |
|---|---|
| `=` auf Text, Nachschlagefeld, Zahl, DateTime | ja |
| `<`, `<=`, `>`, `>=` auf DateTime | ja |
| `<`, `<=`, `<>`, `>`, `>=` auf Zahl | ja, **auf dem Feld `ID` nur `=`** |
| `IsBlank` im Filterprädikat | nein |
| `Not` / `!` | nein |
| Personenspalte | nur `Email` und `DisplayName` |
| `Today()` | wird als Konstante gesendet, blockiert nicht |

**GESCHLUSSFOLGERT:** `CountRows(Filter(…))` schickt den inneren `Filter` an den Server und zählt lokal; das steht nicht in der offiziellen Doku (siehe `BRIEFING_Mehrfachspeichern.md`, Abschnitt 9). Für die Bewertung unten heißt das: Ist der `Filter` delegierbar, ist auch das `CountRows` unkritisch — **unter dieser unbelegten Annahme**.

**UNSICHER:** Warum `galAlleTischbuchungen.Items` in Studio ein Delegationsdreieck zeigt, lässt sich am Quellcode nicht entscheiden. Die Formel ist `SortByColumns(Filter(Tischbuchungen, Person.Email = User().Email && Endzeit >= Now()), "Startzeit", SortOrder.Ascending)`. `Person.Email = …` und `Endzeit >= Now()` sind nach der Tabelle oben delegierbar; verdächtig bleiben `SortByColumns` auf einer gefilterten Tabelle und das `With({erzwingeNeuaufbau: …}, …)` darum herum.

## Jede Operation auf eine Datenquelle

Per Skript aus allen Formeln gezogen (`skripte/analyse.js`): 117 Operationen. Sortiert nach Datenquelle und Fundort.

### `Tischbuchungen` (73)

**btn5Std.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btn5Std.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btn9Std.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btn9Std.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = ddTischePanel.Selected.Titel && Startzeit < endeZeit && Endzeit > startZeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnEinchecken.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
aktuelleBuchung
```

Schreiboperation; Delegation nicht anwendbar.

**btnEinchecken.OnSelect** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnHitArea_1.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnHitArea.OnSelect** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnHitArea.OnSelect** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus1Std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus1Std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus2Std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus2Std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus3std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnMinus3std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std_1.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std_1.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std_1.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std_1.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus1Std.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 60, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std_1.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std_1.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std_1.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std_1.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus2Std.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 120, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std_1.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std_1.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std_1.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std_1.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = tischWert && Startzeit < neueEndzeit && Endzeit > endeAlt
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std.DisplayMode** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std.DisplayMode** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < neueEndzeit && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std.Fill** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnPlus3Std.Fill** — `Filter` (lesen)

```powerfx
Tisch.Value = aktuelleBuchung.Tisch.Value && Startzeit < DateAdd(aktuelleBuchung.Endzeit, 180, TimeUnit.Minutes) && Endzeit > aktuelleBuchung.Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSpeichern.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
ForAll(neueDatensaetze, Defaults(Tischbuchungen))
```

Schreiboperation; Delegation nicht anwendbar.

**btnSpeichern.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnSpeichern.OnSelect** — `Filter` (lesen)

```powerfx
Tisch.Value = varSelectedTisch.Titel
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSpeichern.OnSelect** — `Defaults` (lesen)

Liefert einen leeren Datensatz, kein Netzwerkzugriff.

**btnSpeichernTischePanel.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
Defaults(Tischbuchungen)
```

Schreiboperation; Delegation nicht anwendbar.

**btnSpeichernTischePanel.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnSpeichernTischePanel.OnSelect** — `Filter` (lesen)

```powerfx
Tisch.Value = ddTischePanel.Selected.Titel
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSpeichernTischePanel.OnSelect** — `Defaults` (lesen)

Liefert einen leeren Datensatz, kein Netzwerkzugriff.

**btnStornieren_1.OnSelect** — `Remove` (schreiben/steuern)

```powerfx
varSelectedBuchungTab
```

Schreiboperation; Delegation nicht anwendbar.

**btnStornieren_1.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnStornieren.OnSelect** — `Remove` (schreiben/steuern)

```powerfx
varSelectedBuchung
```

Schreiboperation; Delegation nicht anwendbar.

**btnStornierenKlein.OnSelect** — `Remove` (schreiben/steuern)

```powerfx
colStornoZiele
```

Schreiboperation; Delegation nicht anwendbar.

**btnStornierenKlein.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnStornierenKlein.OnSelect** — `Filter` (lesen)

```powerfx
Person.Email = User().Email && Endzeit >= Now()
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnVerlängern_1.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
aktuelleBuchung
```

Schreiboperation; Delegation nicht anwendbar.

**btnVerlängern_1.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**btnVerlängern_1.OnSelect** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchungTab.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnVerlängern.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
aktuelleBuchung
```

Schreiboperation; Delegation nicht anwendbar.

**btnVerlängern.OnSelect** — `LookUp` (lesen)

```powerfx
ID = varSelectedBuchung.ID
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.BorderColor** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.BorderStyle** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Now() >= Startzeit && Now() <= Endzeit
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.BorderStyle** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.BorderStyle** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit > Now() && Startzeit <= DateAdd(Now(), 60, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.Fill** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Circle1.Fill** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**galAlleTischbuchungen.Items** — `Filter` (lesen)

```powerfx
Person.Email = User().Email && Endzeit >= Now()
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**galTischbuchungenHeute.Items** — `Filter` (lesen)

```powerfx
Person.Email = User().Email && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days) && (varAnsichtsDatum <> Today() || Endzeit >= Now())
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Icon1_1.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**Icon1.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**Image6.OnSelect** — `Refresh` (schreiben/steuern)

Lädt die Liste neu; Umfang durch das Datenzeilenlimit begrenzt (`DefaultConnectedDataSourceMaxGetRowsCount: 1000`).

**Label1.Text** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Label1.Text** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Rectangle1.Fill** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Endzeit >= Now() && Startzeit <= DateAdd(Now(), 30, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Rectangle1.Fill** — `LookUp` (lesen)

```powerfx
Tisch.Value = ThisItem.Titel && Startzeit >= varAnsichtsDatum && Startzeit < DateAdd(varAnsichtsDatum, 1, TimeUnit.Days)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

### `Tische` (3)

**App.Formulas** — `Filter` (lesen)

```powerfx
Geschoss.Value = "OG"
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**App.Formulas** — `Filter` (lesen)

```powerfx
Geschoss.Value = "UG"
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Gallery1.Items** — `Filter` (lesen)

```powerfx
Geschoss.Value = varAusgewaehltesStockwerk
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

### `Raumbuchungen` (41)

**btnSlot1.DisplayMode** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot1.Fill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot1.Fill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot1.HoverFill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot1.OnSelect** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot1.Y** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot2.DisplayMode** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot2.Fill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot2.HoverFill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot2.OnSelect** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot2.Y** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot3.DisplayMode** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot3.Fill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot3.HoverFill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot3.OnSelect** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot3.Y** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot4.DisplayMode** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit <= slotStart && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot4.Fill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot4.HoverFill** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot4.OnSelect** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSlot4.Y** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**btnSpeichernRaumPanel.OnSelect** — `Patch` (schreiben/steuern)

```powerfx
Defaults(Raumbuchungen)
```

Schreiboperation; Delegation nicht anwendbar.

**btnSpeichernRaumPanel.OnSelect** — `Defaults` (lesen)

Liefert einen leeren Datensatz, kein Netzwerkzugriff.

**galRaumbuchungenHeute.Items** — `Filter` (lesen)

```powerfx
Person.Email = User().Email && Startzeit >= Today() && Startzeit < DateAdd(Today(), 1, TimeUnit.Days) && Endzeit >= Now()
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**galRäume.Items** — `Filter` (lesen)

```powerfx
Raum.Value = R.Titel && Startzeit < slotEnde && Endzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Label4.Text** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**Label5.Text** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot1Info.Text** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot1Info.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot2Info.Text** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot2Info.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot3Info.Text** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot3Info.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot4Info.Text** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**lblSlot4Info.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = ThisItem.Titel && Startzeit > slotStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDanach1.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < DateAdd(varAusgewählteEndzeit, 90, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDanach1.Width** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDanach1.X** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Startzeit >= varAusgewählteEndzeit && Startzeit < fensterEnde
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDavor1.Visible** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > DateAdd(varAusgewählteStartzeit, -90, TimeUnit.Minutes)
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDavor1.Width** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).

**recBuchungDavor1.X** — `Filter` (lesen)

```powerfx
Raum.Value = varAusgewähltRaum.Titel && Endzeit <= varAusgewählteStartzeit && Endzeit > fensterStart
```

GESCHLUSSFOLGERT: delegierbar (nur `=`, `<`, `>` auf Text, DateTime, Nachschlagefeld oder `Person.Email`).
